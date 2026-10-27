import copy
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from local_llm_client import LocalMLXClient,snapshot_inventory

@pytest.fixture
def client(tmp_path):
    path=tmp_path/('a'*40);path.mkdir()
    (path/'config.json').write_text(json.dumps({'quantization':{'bits':4,'group_size':64},'max_position_embeddings':32768,'model_type':'qwen2'}))
    (path/'tokenizer_config.json').write_text(json.dumps({'chat_template':'synthetic-template'}))
    (path/'model.safetensors').write_bytes(b'SYNTHETIC NOT MODEL WEIGHTS')
    c=LocalMLXClient(path,snapshot_inventory(path),model_id='synthetic',seed=2027)
    return c

def test_inventory_rejects_weight_tampering(client):
    inventory=copy.deepcopy(client.inventory)
    (client.snapshot/'model.safetensors').write_bytes(b'changed')
    with pytest.raises(ValueError,match='bytes'):LocalMLXClient(client.snapshot,inventory,model_id='synthetic',seed=1)

def test_missing_chat_template_and_remote_code_are_rejected(client):
    (client.snapshot/'custom.py').write_text('')
    with pytest.raises(ValueError,match='Python'):snapshot_inventory(client.snapshot)
    (client.snapshot/'custom.py').unlink()
    (client.snapshot/'tokenizer_config.json').write_text('{}')
    with pytest.raises(ValueError,match='template'):snapshot_inventory(client.snapshot)

@pytest.mark.parametrize('kwargs',[{'retries':2},{'model':'other'},{'max_tokens':2001},{'temperature':float('nan')},{'reasoning_effort':'low'},{'paid_api':True}])
def test_invalid_requests_fail_before_model_load(client,monkeypatch,kwargs):
    def forbidden():pytest.fail('Model loaded for an invalid request')
    monkeypatch.setattr(client,'_load',forbidden)
    with pytest.raises(ValueError):client('prompt',**kwargs)

def mock_backend(c,monkeypatch,interrupt=False):
    seeds=[]
    # The mocked backend must stay runnable without optional GPU packages.
    monkeypatch.setattr('local_llm_client.importlib.metadata.version', lambda name: 'synthetic-test-version')
    mx=SimpleNamespace(random=SimpleNamespace(seed=seeds.append))
    monkeypatch.setitem(sys.modules,'mlx',SimpleNamespace(core=mx));monkeypatch.setitem(sys.modules,'mlx.core',mx)
    def stream(*args,**kwargs):
        yield SimpleNamespace(text='proof',token=7,generation_tokens=1,finish_reason='stop',peak_memory=0)
        if interrupt:raise KeyboardInterrupt()
    monkeypatch.setitem(sys.modules,'mlx_lm',SimpleNamespace(stream_generate=stream))
    monkeypatch.setitem(sys.modules,'mlx_lm.sample_utils',SimpleNamespace(make_sampler=lambda **kw:kw))
    c._model=object();c._tokenizer=SimpleNamespace(apply_chat_template=lambda messages,**kwargs:'CHAT:'+messages[0]['content'],encode=lambda text,**kwargs:list(range(len(text))))
    return seeds

def test_repeat_prompt_uses_distinct_context_seeds_and_no_context_replay(client,monkeypatch):
    seeds=mock_backend(client,monkeypatch)
    first=client('unchanged',generation_context='p/B/1')
    second=client('unchanged',generation_context='p/B/2')
    assert first.content=='proof' and seeds[0]!=seeds[1]
    assert first.metadata['prompt_tokens']==len('CHAT:unchanged')
    assert first.metadata['api_attempts']==0 and first.metadata['logical_generations']==1
    with pytest.raises(RuntimeError,match='already attempted'):client('unchanged',generation_context='p/B/1')

def test_context_overflow_prevents_generation(client,monkeypatch):
    mock_backend(client,monkeypatch);client.max_context_tokens=8
    with pytest.raises(RuntimeError,match='context budget'):client('long prompt')

def test_interrupted_stream_is_preserved_without_automatic_retry(client,monkeypatch,tmp_path):
    mock_backend(client,monkeypatch,interrupt=True);client.trace_directory=tmp_path
    with pytest.raises(KeyboardInterrupt):client('prompt',generation_context='p/C/1')
    rows=[json.loads(x) for x in next(tmp_path.glob('*.jsonl')).read_text().splitlines()]
    assert rows[1]['text']=='proof' and rows[-1]['status']=='interrupted'
    with pytest.raises(RuntimeError):client('prompt',generation_context='p/C/1')

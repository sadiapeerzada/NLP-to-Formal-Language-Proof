import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from local_protocol import validate_local_protocol,execution_context
from repair_experiment import run_experiment,_call_model
from model_client import CompletionResult
PROTOCOL=ROOT/'configs/repair_experiment_local_v0.3.0.json'

def test_proposed_protocol_validates_but_cannot_execute(tmp_path):
    p=validate_local_protocol(PROTOCOL)
    assert p['local_execution_enabled'] is False
    with pytest.raises(ValueError,match='supervisor approval'):
        execution_context(PROTOCOL,None,None,'x','theorem x : True := by sorry',None,phase='development_pilot')
    assert not list(tmp_path.iterdir())

@pytest.mark.parametrize('field,value',[('temperature',0.7),('max_completion_tokens',1000),('max_context_tokens',99999),('top_p',0.9)])
def test_local_protocol_rejects_decoding_drift(tmp_path,field,value):
    p=json.loads(PROTOCOL.read_text());p['decoding'][field]=value
    target=tmp_path/'changed.json';target.write_text(json.dumps(p))
    with pytest.raises(ValueError,match='decoding'):validate_local_protocol(target)

def test_local_mode_cannot_relabel_an_injected_generator(tmp_path):
    with pytest.raises(ValueError,match='genuine MLX'):
        run_experiment('x','theorem x : True := by sorry',ROOT/'lean_project',tmp_path/'must-not-exist',execution_mode='local',completion_fn=lambda *a,**kw:CompletionResult('fake',{}),local_protocol_path=PROTOCOL)
    assert not (tmp_path/'must-not-exist').exists()

def test_local_call_does_not_inherit_groq_transport_retries():
    calls=[]
    class Stub:
        provider='mlx_local'
        def __call__(self,prompt,**kwargs):calls.append(kwargs);return CompletionResult('synthetic',{})
    _call_model(Stub(),'prompt',model='qwen',generation_context='p/B/1')
    assert calls[0]['retries']==1 and calls[0]['reasoning_effort'] is None
    assert calls[0]['generation_context']=='p/B/1'

def test_local_import_and_plan_work_when_groq_is_not_installed():
    script="""import builtins,sys
sys.path.insert(0,'src')
original=builtins.__import__
def blocked(name,*a,**kw):
 if name=='groq':raise ImportError('Groq intentionally unavailable')
 return original(name,*a,**kw)
builtins.__import__=blocked
import repair_experiment,local_llm_client,model_client
assert repair_experiment.groq.Groq is None
"""
    result=subprocess.run([sys.executable,'-c',script],cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==0,result.stderr


def test_shared_local_lifecycle_retains_condition_isolation(tmp_path,monkeypatch):
    # Synthetic lifecycle only. Approval gate is substituted explicitly for this
    # offline test; no test manifest is stored in research result directories.
    import local_protocol
    from local_llm_client import LocalMLXClient
    from verify import VerificationResult
    from test_repair_experiment import failed_verification,successful_verification
    protocol=validate_local_protocol(PROTOCOL);calls=[]
    client=object.__new__(LocalMLXClient);client.model_id=protocol['model']['requested_model_id']
    def generated(self,prompt,**kwargs):
        calls.append((prompt,kwargs))
        return CompletionResult('theorem target : True := by trivial' if len(calls)>1 else 'theorem target : True := by contradiction',{})
    monkeypatch.setattr(LocalMLXClient,'__call__',generated)
    context={'protocol':{'sha256':'a'*64,'status':'SYNTHETIC_TEST_NOT_APPROVED','version':'test','path':str(PROTOCOL)},
        'provider':'mlx_local','model':protocol['model'],'decoding':protocol['decoding'],
        'prompt_templates':protocol['prompt_templates'],'input_natural_language':'Synthetic test problem only.'}
    monkeypatch.setattr(local_protocol,'execution_context',lambda *args,**kwargs:context)
    outcomes=iter([failed_verification('PRIVATE_DIAGNOSTIC'),successful_verification(),successful_verification()])
    path=run_experiment('synthetic','theorem target : True := by sorry',ROOT/'lean_project',tmp_path/'run',model=client.model_id,execution_mode='local',completion_fn=client,verification_fn=lambda *args,**kw:next(outcomes),local_protocol_path=PROTOCOL)
    run=json.loads(path.read_text())
    assert run['api_generation_confirmed'] is False and run['local_generation_confirmed'] is True
    assert run['provider']=='mlx_local'
    assert calls[0][1]['generation_context']=='synthetic/initial'
    assert calls[1][1]['generation_context']=='synthetic/B/1'
    assert calls[2][1]['generation_context']=='synthetic/C/1'
    assert 'PRIVATE_DIAGNOSTIC' not in calls[1][0] and 'PRIVATE_DIAGNOSTIC' in calls[2][0]
    assert all(call[1]['retries']==1 for call in calls)
    assert len({run['conditions'][c]['starting_candidate_sha256'] for c in 'ABC'})==1


def test_local_backend_errors_are_not_reported_as_paid_api_failures():
    from repair_experiment import _provider_error_record
    error=_provider_error_record(RuntimeError('Metal unavailable'),provider='mlx_local')
    assert error['error_category']=='local_backend_error'


def test_local_protocol_rejects_changed_definition_modules(tmp_path):
    p=json.loads(PROTOCOL.read_text());p['lean_environment']['candidate_definition_modules'][0]['sha256']='0'*64
    path=tmp_path/'protocol.json';path.write_text(json.dumps(p))
    with pytest.raises(ValueError,match='definition module'):validate_local_protocol(path)


def test_local_protocol_rejects_implementation_drift(tmp_path):
    p=json.loads(PROTOCOL.read_text());p['implementation_files'][0]['sha256']='0'*64
    path=tmp_path/'protocol.json';path.write_text(json.dumps(p))
    with pytest.raises(ValueError,match='implementation source'):validate_local_protocol(path)


def test_live_environment_rejects_a_different_checkout(monkeypatch):
    import local_protocol
    p=validate_local_protocol(PROTOCOL)
    values=iter(['Lean (version 4.32.0, fixture)','wrong-revision',''])
    monkeypatch.setattr(local_protocol.subprocess,'run',lambda *a,**kw:SimpleNamespace(returncode=0,stdout=next(values)))
    with pytest.raises(ValueError,match='Actual Lean'):local_protocol.live_lean_environment(p)

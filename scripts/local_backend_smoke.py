"""Neutral eight-token backend validation, explicitly outside the research pilot."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from local_llm_client import LocalMLXClient

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--snapshot',type=Path,required=True);p.add_argument('--inventory',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    a.output_dir.mkdir(parents=True,exist_ok=False)
    inventory=json.loads(a.inventory.read_text());client=LocalMLXClient(a.snapshot,inventory,model_id='mlx-community/Qwen2.5-7B-Instruct-4bit',seed=2027)
    client.trace_directory=a.output_dir/'stream';client.trace_directory.mkdir()
    prompt='Reply with the single word READY.'
    result={'purpose':'neutral_backend_smoke_not_a_pilot_or_mathematical_experiment','paid_inference_requests':0,'input':prompt,'platform':platform.platform(),
        'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'src/local_llm_client.py',ROOT/'src/model_client.py']},
        'package_versions':{n:importlib.metadata.version(n) for n in ['mlx','mlx-lm','transformers']}}
    try:
        import mlx.core as mx
        result['hardware']=mx.device_info()
        c=client(prompt,max_tokens=8,temperature=0.2,generation_context='neutral-smoke/initial')
        result.update(success=bool(c.content.strip()),response=c.content,metadata=c.metadata)
    except Exception as error:result.update(success=False,error_type=type(error).__name__,error=str(error))
    (a.output_dir/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

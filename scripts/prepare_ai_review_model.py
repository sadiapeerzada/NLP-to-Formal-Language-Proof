"""Reproduce a pinned free local reviewer download; no hosted inference calls."""
import argparse
import json
from pathlib import Path
import re
import ssl
import sys
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from local_llm_client import snapshot_inventory


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ('repo','revision','upstream','upstream-revision'):p.add_argument('--'+flag,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    for revision in (a.revision,a.upstream_revision):
        if not re.fullmatch('[0-9a-f]{40}',revision):p.error('Immutable 40-hex revisions required')
    a.output.mkdir(parents=True,exist_ok=False)
    import certifi
    from huggingface_hub import snapshot_download
    context=ssl.create_default_context(cafile=certifi.where())
    for local,repo,rev,remote in [('quantized_model_card.md',a.repo,a.revision,'README.md'),
            ('upstream_model_card.md',a.upstream,a.upstream_revision,'README.md'),
            ('upstream_LICENSE',a.upstream,a.upstream_revision,'LICENSE')]:
        url=f'https://huggingface.co/{repo}/resolve/{rev}/{remote}'
        with urllib.request.urlopen(url,context=context,timeout=90) as r:(a.output/local).write_bytes(r.read())
    snapshot=snapshot_download(repo_id=a.repo,revision=a.revision,
        allow_patterns=['*.json','*.safetensors','*.model','*.txt','README.md'],max_workers=2)
    inventory=snapshot_inventory(Path(snapshot))
    (a.output/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    (a.output/'local_snapshot_path.txt').write_text(snapshot+'\n')
    print('Pinned reviewer snapshot ready:',a.revision,'weight bytes:',inventory['weight_bytes'])


if __name__=='__main__':main()

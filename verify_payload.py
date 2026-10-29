"""Verify exact public payload membership and hashes; no original private data needed."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def main():
    manifest_path=ROOT/'PUBLIC_PAYLOAD_MANIFEST.json'
    m=json.loads(manifest_path.read_text())
    files={str(p.relative_to(ROOT)):p for p in ROOT.rglob('*') if p.is_file() and p.name!='.git' and p!=manifest_path and '.git' not in p.relative_to(ROOT).parts}
    assert set(files)==set(m['files']),'Payload membership differs from approved inventory'
    for rel,path in files.items():
        data=path.read_bytes();assert hashlib.sha256(data).hexdigest()==m['files'][rel]['sha256'],rel
        assert len(data)==m['files'][rel]['bytes'],rel
        if path.suffix not in {'.pdf','.png'}:
            text=data.decode('utf-8')
            assert not re.search(r'(?:/Users/|/home/)[A-Za-z0-9_.-]+',text),rel
            assert not re.search(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',text),rel
            assert not re.search(r'(?<![A-Za-z0-9])(?:sk-(?:proj-)?[A-Za-z0-9_-]{20,}|gsk_[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{15,})',text),rel
    result=subprocess.run([sys.executable,'-B',str(ROOT/'reanalyze.py')],cwd=ROOT,capture_output=True,text=True,check=True)
    r=json.loads(result.stdout);assert r['heldout_completed_calls_checked']==410
    print(json.dumps({'valid':True,'payload_files_excluding_manifest':len(files),'public_reanalysis':r,
                      'scope':'Exact approved file hashes, text token/home-path checks and redacted-view pairing. PDF text/metadata and PNG metadata/visual checks were performed separately during preparation.'},indent=2))


if __name__=='__main__':main()

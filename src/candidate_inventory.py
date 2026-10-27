"""Load versioned candidates and validated append-only proof-evidence overlays."""
import copy
import hashlib
import json
import re
from pathlib import Path
from dataset_validation import REQUIRED_LEAN_TOOLCHAIN, REQUIRED_MATHLIB_REVISION
from verify import _diagnostics,_axioms_from_diagnostics,_find_prohibited_source,DEFAULT_POLICY


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_candidates(root: Path) -> list[dict]:
    paths=[root/'data/research_dataset_draft_v0.1.0.json']
    paths+=sorted((root/'data/curation_batches').glob('*/candidate_records.json'))
    records=[r for p in paths for r in json.loads(p.read_text())]
    by_id={r['id']:r for r in records}
    if len(by_id)!=len(records):raise ValueError('Duplicate candidate IDs.')
    for path in sorted((root/'data/reference_verification').glob('*/proof_overlay.json')):
        overlay=json.loads(path.read_text())
        if overlay.get('lean_toolchain')!=REQUIRED_LEAN_TOOLCHAIN or overlay.get('mathlib_revision')!=REQUIRED_MATHLIB_REVISION:
            raise ValueError('Proof overlay uses a different pinned environment.')
        source=root/overlay['candidate_source'];checked=root/overlay['checked_source'];log=root/overlay['verification_file']
        if digest(source)!=overlay['candidate_source_sha256'] or digest(checked)!=overlay['checked_source_sha256'] or digest(log)!=overlay['verification_sha256']:
            raise ValueError('Proof-overlay evidence changed.')
        if _find_prohibited_source(source.read_text(),False,DEFAULT_POLICY) or not checked.read_text().startswith(source.read_text()):
            raise ValueError('Candidate source is unsafe or differs from the checked declarations.')
        verification=json.loads(log.read_text());messages,malformed=_diagnostics(verification['stdout'])
        if verification['exit_code']!=0 or verification['source_sha256']!=digest(checked) or malformed or any(d['severity']=='error' for d in messages):
            raise ValueError('Proof overlay lacks successful exact-statement verification.')
        for module in overlay.get('definition_modules',[]):
            if digest(root/module['path'])!=module['sha256']:
                raise ValueError('Candidate definition module changed.')
        for entry in overlay['records']:
            r=by_id.get(entry['id'])
            if r is None or hashlib.sha256(r['expected_lean_statement'].encode()).hexdigest()!=entry['statement_sha256']:
                raise ValueError('Proof overlay statement no longer matches its candidate.')
            resolved=entry.get('resolved_expected_lean_statement')
            if resolved is not None:
                if r['curation'].get('semantic_fidelity',{}).get('review_status')=='verified':
                    raise ValueError('Statement context changes require fresh independent review.')
                r['expected_lean_statement']=resolved
                r['statement_preparation_note']='Explicit candidate definition/import context added; independent review remains pending. Original statement and evidence retained in historical file.'
                r['required_definitions']=overlay.get('definition_modules',[])
            name=r['expected_lean_statement'].split('theorem ',1)[1].split()[0]
            qualified_name=overlay.get('candidate_namespace','')
            qualified_name=(qualified_name+'.' if qualified_name else '')+name
            expected_source=re.sub(r'(?m)^import [^\n]+\n?', '', r['expected_lean_statement']).strip()
            if expected_source+' := by sorry' not in checked.read_text():
                raise ValueError('Expected statement comparison is missing from Lean source.')
            if f'example : ReferenceExpected.{name} = {qualified_name} := by' not in checked.read_text():
                raise ValueError('Exact Lean theorem-type comparison is missing.')
            axioms=_axioms_from_diagnostics(messages,qualified_name)
            if axioms is None or set(axioms)-set(DEFAULT_POLICY.allowed_axioms):
                raise ValueError('Missing or unapproved theorem dependencies.')
            r['required_imports']=['Mathlib']+[module['import'] for module in overlay.get('definition_modules',[]) if resolved is not None]
            r['curation']['theorem_verification']={
                'status':'verified','success':True,'verification_scope':'strict_proof',
                'lean_toolchain':overlay['lean_toolchain'],'mathlib_revision':overlay['mathlib_revision'],
                'command':verification['command'],'theorem_sha256':hashlib.sha256(r['expected_lean_statement'].encode()).hexdigest(),
                'verification_source_sha256':digest(checked),'axiom_dependencies':axioms,
                'evidence':str(path.relative_to(root))+'; candidate source has no placeholders; exact-type comparison and target axiom inspection passed. ReferenceExpected placeholders check types only.'}
    return records

import hashlib
import json
from pathlib import Path
import shutil
import sys
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from candidate_inventory import load_candidates
from dataset_validation import validate_curation_draft


def test_reference_overlays_add_proof_evidence_without_rewriting_or_approving_reviews():
    original=ROOT/'data/research_dataset_draft_v0.1.0.json';before=original.read_bytes()
    records=load_candidates(ROOT);by_id={r['id']:r for r in records}
    assert by_id['arith_001']['curation']['theorem_verification']['verification_scope']=='strict_proof'
    assert by_id['arith_001']['curation']['semantic_fidelity']['review_status']=='pending'
    assert not validate_curation_draft(records).eligible_problem_ids
    assert original.read_bytes()==before


def test_overlay_rejects_changed_compiler_evidence(tmp_path):
    (tmp_path/'data').mkdir();shutil.copy2(ROOT/'data/research_dataset_draft_v0.1.0.json',tmp_path/'data')
    target=tmp_path/'data/reference_verification/v0.1.0'
    shutil.copytree(ROOT/'data/reference_verification/v0.1.0',target)
    with (target/'verification_checked.json').open('a') as f:f.write(' ')
    with pytest.raises(ValueError,match='evidence changed'):load_candidates(tmp_path)


def test_library_record_signatures_match_the_actual_compiled_reference_batch():
    batch=ROOT/'data/curation_batches/v0.2.0';source=(batch/'references_expanded.lean').read_text()
    result=json.loads((batch/'verification_expanded.json').read_text())
    assert result['exit_code']==0
    assert result['source_sha256']==hashlib.sha256(source.encode()).hexdigest()
    for record in json.loads((batch/'candidate_records.json').read_text()):
        declaration=record['reference_lean_code'].removeprefix('import Mathlib\nopen scoped BigOperators\n')
        assert declaration.strip() in source
        assert record['curation']['theorem_verification']['theorem_sha256']==hashlib.sha256(record['expected_lean_statement'].encode()).hexdigest()


def test_geometric_sum_has_explicit_unreviewed_definition_context():
    rows={r['id']:r for r in load_candidates(ROOT)}
    record=rows['ind_004']
    assert 'import Nl2Lean.CandidateDefinitions' in record['expected_lean_statement']
    assert 'def geomSum' in record['expected_lean_statement']
    assert record['curation']['theorem_verification']['verification_scope']=='strict_proof'
    assert record['curation']['semantic_fidelity']['review_status']=='pending'

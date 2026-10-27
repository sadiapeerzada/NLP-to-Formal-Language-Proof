import copy
from datetime import date
import hashlib
import json
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from semantic_review import binding,prepare_packets,validate_decisions,import_reviews,semantic_success

@pytest.fixture
def review_fixture(tmp_path):
    # Synthetic evidence only; never written into the research dataset.
    from test_dataset_validation import DatasetValidationTests
    r=DatasetValidationTests.curation_record('synthetic','family','development')
    artifact=tmp_path/'synthetic.txt';artifact.write_text('Synthetic regression evidence, not a real review.')
    evidence={'path':artifact.name,'sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()}
    registry={'status':'human_verified','verified_by':'SYNTHETIC_FIXTURE',
        'verification_artifact':evidence,'reviewers':[{'id':'fixture-reviewer','qualified_lean_reviewer':True}]}
    decision={'schema_version':1,'candidate_id':r['id'],'binding_sha256':binding(r),'review_type':'semantic_fidelity',
        'label':'faithful','reviewer_id':'fixture-reviewer','reviewer_kind':'independent_human_review',
        'reviewed_on':date.today().isoformat(),'independence_attestation':True,'evidence':'Synthetic test reasoning.','evidence_artifact':evidence}
    return r,decision,registry,tmp_path

def test_preparation_leaves_all_human_fields_pending(review_fixture):
    r,d,reg,root=review_fixture;out=root/'packets';prepare_packets([r],out)
    assert r['nl_statement'] in (out/'synthetic.md').read_text()
    template=json.loads((out/'synthetic.decision.json').read_text())
    assert template['label'] is None and template['reviewer_id'] is None
    with pytest.raises(FileExistsError):prepare_packets([r],out)

@pytest.mark.parametrize('field,value',[('label',None),('reviewer_id','unknown'),('reviewer_kind','assisted_review'),('independence_attestation',False),('reviewed_on','2099-01-01'),('binding_sha256','0'*64),('evidence','')])
def test_invalid_decisions_are_rejected(review_fixture,field,value):
    r,d,reg,root=review_fixture;d[field]=value
    with pytest.raises(ValueError):validate_decisions([r],[d],reg,evidence_base=root)

def test_review_must_bind_both_english_and_lean(review_fixture):
    r,d,reg,root=review_fixture;r['nl_statement']+=' Changed English.'
    with pytest.raises(ValueError,match='bind'):validate_decisions([r],[d],reg,evidence_base=root)

def test_compiling_but_unfaithful_is_never_semantic_success(review_fixture):
    r,d,reg,root=review_fixture
    assert not semantic_success(True,r,d)  # No authenticated registry.
    for label in ['not faithful','uncertain']:
        d['label']=label
        assert not semantic_success(True,r,d,registry=reg,evidence_base=root)
    d['label']='faithful'
    assert semantic_success(True,r,d,registry=reg,evidence_base=root)
    assert not semantic_success(False,r,d,registry=reg,evidence_base=root)

def test_import_does_not_approve_unrelated_eligibility(review_fixture):
    r,d,reg,root=review_fixture;before=copy.deepcopy(r);out=root/'imported'
    import_reviews([r],[d],reg,out,evidence_base=root)
    assert r==before
    imported=json.loads((out/'candidate_records.json').read_text())[0]
    assert imported['curation']['semantic_fidelity']['label']=='faithful'
    assert imported['curation']['split_status']=='pending'
    assert imported['curation']['source_license_verification_status']==before['curation']['source_license_verification_status']
    with pytest.raises(FileExistsError):import_reviews([r],[d],reg,out,evidence_base=root)

def test_changed_evidence_and_duplicate_decisions_are_rejected(review_fixture):
    r,d,reg,root=review_fixture
    with pytest.raises(ValueError):validate_decisions([r],[d,d],reg,evidence_base=root)
    (root/'synthetic.txt').write_text('Changed evidence.')
    with pytest.raises(ValueError):validate_decisions([r],[d],reg,evidence_base=root)


def test_review_binding_includes_definition_context(review_fixture):
    r,d,reg,root=review_fixture
    r['required_definitions']=[{'path':'candidate.lean','sha256':'a'*64}]
    with pytest.raises(ValueError,match='bind'):validate_decisions([r],[d],reg,evidence_base=root)


def test_generated_statements_never_inherit_reference_faithfulness(review_fixture):
    from semantic_review import generated_review_subjects
    r,d,reg,root=review_fixture;r['curation']['semantic_fidelity']={'review_status':'verified','label':'faithful'}
    path=root/'synthetic-results.jsonl';path.write_text(json.dumps({'id':r['id'],'run_id':'SYNTHETIC_ONLY','final_lean_statement':'theorem weaker : True := by trivial','solved':True})+'\n')
    subject=generated_review_subjects([r],path)[0]
    assert subject['curation']['semantic_fidelity']['label'] is None
    assert subject['generated_statement_provenance']['semantic_success'] is False
    assert subject['reference_lean_statement_for_comparison']==r['expected_lean_statement']
    assert not semantic_success(True,subject,d,registry=reg,evidence_base=root)

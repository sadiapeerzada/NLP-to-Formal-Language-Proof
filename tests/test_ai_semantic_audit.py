import copy
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from ai_semantic_audit import DIMENSIONS, digest, subject, parse_judgment, proposed_record, assert_unchanged_curation
from candidate_inventory import load_candidates
from ai_audit_quality import quality_flags, exact_duplicate_groups


def judgment():
    return {'label':'uncertain','issues':[], 'explanation':'Synthetic test judgment, not a real review.',
            **{k:'Synthetic substantive field.' for k in DIMENSIONS}}


def test_parser_refuses_incomplete_truncated_and_duplicate_judgments():
    value=judgment()
    assert parse_judgment(json.dumps(value)) == value
    with pytest.raises(ValueError):parse_judgment(json.dumps(value)[:-4])
    with pytest.raises(ValueError):parse_judgment('{"label":"faithful","label":"uncertain"}')
    for field in DIMENSIONS:
        broken=copy.deepcopy(value);del broken[field]
        with pytest.raises(ValueError):parse_judgment(json.dumps(broken))


def test_ai_snapshot_never_changes_curation_or_grants_human_status():
    record=load_candidates(ROOT)[0]
    audit={'candidate_id':record['id'],'subject_sha256':digest(subject(record)),
           'judgment':judgment(),'reviewer_kind':'independent_human_review','grants_eligibility':True}
    proposed=proposed_record(record,audit)
    assert proposed['ai_semantic_audit']['reviewer_kind']=='ai_only_not_independent_human'
    assert proposed['ai_semantic_audit']['grants_eligibility'] is False
    assert_unchanged_curation([record],[proposed])
    proposed['curation']['split_status']='verified'
    with pytest.raises(ValueError):assert_unchanged_curation([record],[proposed])


def test_stale_subject_binding_is_rejected():
    r=load_candidates(ROOT)[0]
    audit={'candidate_id':r['id'],'subject_sha256':digest(subject(r))}
    r['nl_statement']+=' CHANGED'
    with pytest.raises(ValueError):proposed_record(r,audit)


def test_template_echoes_are_flagged_without_rewriting_model_labels():
    value=judgment();value['quantifiers']='specific scope comparison'
    assert quality_flags(value)==['Prompt placeholder copied into quantifiers.']
    assert value['label']=='uncertain'
    assert quality_flags(None)


def test_exact_duplicate_detection_ignores_theorem_names():
    assert exact_duplicate_groups(load_candidates(ROOT))==[['arith_003','arith_003_mathlib']]


def test_faithful_label_with_issues_is_escalated_not_automatically_admitted():
    value=judgment();value.update(label='faithful',issues=['A claimed missing assumption.'])
    assert quality_flags(value)
    assert value['label']=='faithful'


def math_module():
    spec=importlib.util.spec_from_file_location('audit_math_checks',ROOT/'scripts/ai_audit_math_checks.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def test_math_probe_inventory_covers_every_candidate_once():
    module=math_module()
    assert set(module.specifications())=={r['id'] for r in load_candidates(ROOT)}


def test_math_probes_use_lean_totalized_arithmetic_and_catch_endpoint_mutations():
    m=math_module()
    assert m.mod(-5,0)==-5 and m.mod(-5,-3)==1
    assert m.ndiv(4,0)==0 and m.tsub(2,5)==0
    assert m.dvd(0,0) and not m.dvd(0,1)
    # Mutation controls: wrong index endpoint, strictness, sign and omitted premise.
    assert sum(range(1)) != 1*(1+1)//2
    assert not 0 < 0**2
    assert not (-1 <= 1 and 1/Fraction(-1) >= 1/Fraction(1))
    assert not m.tsub(2,5)+5==2


from fractions import Fraction

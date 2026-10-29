"""The primary reviewer must cover the entire inventory without replay."""
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit_assembly',ROOT/'scripts/assemble_ai_semantic_audit.py')
assembly=importlib.util.module_from_spec(spec);spec.loader.exec_module(assembly)


def prepared(tmp_path, events):
    records=[{'id':'synthetic_a'},{'id':'synthetic_b'}]
    path=tmp_path/'subjects.json';path.write_text(json.dumps(records))
    (tmp_path/'manifest.json').write_text(json.dumps({
        'subjects_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_sha256':{}}))
    (tmp_path/'journal.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events))
    return records


def test_primary_pass_cannot_assemble_a_partial_or_interrupted_audit(tmp_path):
    records=prepared(tmp_path,[{'event':'intent','candidate_id':'synthetic_a'},
        {'event':'interrupted','candidate_id':'synthetic_a'}])
    with pytest.raises(ValueError,match='Incomplete reviewer execution'):
        assembly.checked_pass(tmp_path,records)


def test_replayed_logical_review_context_is_rejected(tmp_path):
    records=prepared(tmp_path,[{'event':'intent','candidate_id':'synthetic_a'}]*2)
    with pytest.raises(ValueError,match='replayed'):
        assembly.checked_pass(tmp_path,records)

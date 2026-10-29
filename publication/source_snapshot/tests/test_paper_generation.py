"""Paper tables must reflect validator evidence rather than fixed zero counts."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('paper_tables', Path(__file__).resolve().parents[1] / 'paper/scripts/generate_inventory_tables.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_inventory_tracks_eligibility_changes_without_inventing_frozen_data():
    from test_dataset_validation import DatasetValidationTests
    fixture = DatasetValidationTests()
    record = fixture.curation_record('reviewed', 'family_one', 'development')
    pending_table = module.candidate_table([record])
    assert 'eligible total=0.' in pending_table
    fixture.complete_curation_review(record)
    reviewed_table = module.candidate_table([record])
    assert 'eligible total=1.' in reviewed_table
    assert 'development=1, test=0' in reviewed_table
    assert 'Eligible frozen test records (no freeze) & 0' in module.semantic_table([record])


def test_lean_excerpts_have_readable_ascii_glyphs_and_explicit_truncation():
    excerpt=module.code_excerpt('theorem t (n : ℕ) : n ≤ n ∨ True := by\n'+'x'*100)
    assert 'Nat' in excerpt and '<=' in excerpt and 'or' in excerpt
    assert 'ℕ' not in excerpt and '≤' not in excerpt
    assert '...' in excerpt and 'x'*56 not in excerpt

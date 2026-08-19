"""Regression test for eval/metrics.py crashing on an empty results file.

Background: main() computed `len(solved) / total` unconditionally. If the
results JSONL file is empty (or has no valid non-blank lines -- e.g. a run
that crashed before writing anything, or an accidentally-empty path), `total`
is 0 and this raised an unhandled ZeroDivisionError instead of a clear
message.
"""
from __future__ import annotations

import sys
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent.parent / "eval"
if str(EVAL_DIR) not in sys.path:
    sys.path.insert(0, str(EVAL_DIR))

import metrics  # noqa: E402


def test_empty_results_file_does_not_crash(tmp_path, capsys):
    empty_file = tmp_path / "empty.jsonl"
    empty_file.write_text("")

    metrics.main(str(empty_file))  # must not raise ZeroDivisionError

    out = capsys.readouterr().out
    assert "No results found" in out


def test_blank_lines_only_does_not_crash(tmp_path, capsys):
    blank_file = tmp_path / "blank.jsonl"
    blank_file.write_text("\n\n   \n")

    metrics.main(str(blank_file))  # must not raise ZeroDivisionError

    out = capsys.readouterr().out
    assert "No results found" in out


def test_nonempty_results_file_still_reports_normally(tmp_path, capsys):
    import json
    results_file = tmp_path / "run.jsonl"
    rows = [
        {"id": "a", "category": "cat1", "difficulty": 1, "solved": True,
         "repair_attempts": 0, "wall_clock_seconds": 1.0},
        {"id": "b", "category": "cat1", "difficulty": 1, "solved": False,
         "repair_attempts": 5, "wall_clock_seconds": None, "failure_stage": "synthesize"},
    ]
    results_file.write_text("\n".join(json.dumps(r) for r in rows))

    metrics.main(str(results_file))

    out = capsys.readouterr().out
    assert "Overall pass@1: 1/2 = 50.0%" in out


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))

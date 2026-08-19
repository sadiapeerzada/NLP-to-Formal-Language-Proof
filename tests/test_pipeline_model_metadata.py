"""Regression test for the results['model'] metadata bug.

Background: src/pipeline.py used to record a top-level MODEL_NAME sourced
from the GROQ_MODEL env var. After the strong/fast model split
(src/llm_client.py -> STRONG_MODEL / FAST_MODEL, used by Stage A/B and
Stage C/D respectively), that recorded value no longer matched what model
actually produced each result -- it was stale and misleading regardless of
which models were really used for a given run.

This test drives pipeline.run() end-to-end (with the LLM calls and Lean
compiler faked out, so it runs offline / without a GROQ_API_KEY or a Lean
toolchain) and asserts that every row written to the results JSONL records
the *actual* strong/fast models used for that run, honoring
GROQ_MODEL_STRONG / GROQ_MODEL_FAST overrides.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parent.parent / "src"

# llm_client.py constructs a groq.Groq(...) client at import time, which
# raises immediately if no API key is present anywhere in the environment.
# We never make a real network call in this test (all LLM-calling functions
# are faked out below), so a dummy key is sufficient and safe.
os.environ.setdefault("GROQ_API_KEY", "test-dummy-key")
os.environ["GROQ_MODEL_STRONG"] = "fake-strong-model"
os.environ["GROQ_MODEL_FAST"] = "fake-fast-model"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pipeline  # noqa: E402  (import after sys.path/env setup above)


def test_model_info_reflects_actual_strong_and_fast_models():
    assert pipeline.MODEL_INFO == {
        "formalize_sketch": "fake-strong-model",
        "synthesize": "fake-fast-model",
    }
    # The two stages must not collapse to the same value -- that was
    # exactly the shape of the original bug (a single stale model string).
    assert pipeline.MODEL_INFO["formalize_sketch"] != pipeline.MODEL_INFO["synthesize"]


def test_results_file_records_model_info_for_solved_and_failed_problems(tmp_path, monkeypatch):
    problems = [
        {"id": "p_solved", "category": "arithmetic_identity", "difficulty": 1,
         "nl_statement": "trivial true statement"},
        {"id": "p_stage_a_fail", "category": "arithmetic_identity", "difficulty": 1,
         "nl_statement": "statement that will not elaborate"},
    ]
    input_path = tmp_path / "seed_problems.json"
    input_path.write_text(json.dumps(problems))
    out_path = tmp_path / "results" / "run.jsonl"
    lean_project_dir = tmp_path / "lean_project"

    def fake_formalize(nl_statement, lean_project_dir, scratch_id, max_attempts=3):
        if scratch_id == "p_stage_a_fail":
            return False, "theorem broken := by sorry", [{"attempt": 1, "success": False, "errors": ["boom"]}]
        return True, "theorem trivial_true : True := by trivial", [{"attempt": 1, "success": True, "errors": []}]

    def fake_sketch(nl_statement, lean_statement):
        return "1. trivially true"

    def fake_synthesize_and_verify(nl_statement, lean_statement, proof_sketch_text,
                                    lean_project_dir, pid, max_repair=5):
        result = {
            "id": pid, "solved": True, "repair_attempts": 0, "wall_clock_seconds": 0.01,
            "final_proof": "theorem trivial_true : True := by trivial",
            "scratch_name": f"{pid}_attempt1",
        }
        return result, [{"attempt_number": 1, "proof_text": result["final_proof"], "success": True,
                          "compiler_errors": [], "timestamp": 0.0}]

    def fake_promote_scratch_to_final(lean_project_dir, scratch_name, final_id):
        dst = Path(lean_project_dir) / "generated" / f"{final_id}.lean"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text("theorem trivial_true : True := by trivial")
        return dst

    monkeypatch.setattr(pipeline, "formalize", fake_formalize)
    monkeypatch.setattr(pipeline, "sketch", fake_sketch)
    monkeypatch.setattr(pipeline, "synthesize_and_verify", fake_synthesize_and_verify)
    monkeypatch.setattr(pipeline, "promote_scratch_to_final", fake_promote_scratch_to_final)

    pipeline.run(input_path, out_path, lean_project_dir, max_repair=5)

    lines = [json.loads(line) for line in out_path.read_text().splitlines() if line.strip()]
    assert len(lines) == 2
    by_id = {r["id"]: r for r in lines}

    expected_model_info = {"formalize_sketch": "fake-strong-model", "synthesize": "fake-fast-model"}

    # Solved-problem row.
    assert by_id["p_solved"]["solved"] is True
    assert by_id["p_solved"]["model"] == expected_model_info

    # Stage-A-failure row must ALSO carry the correct model info -- this is
    # the code path the original bug's stale MODEL_NAME still touched too.
    assert by_id["p_stage_a_fail"]["solved"] is False
    assert by_id["p_stage_a_fail"]["failure_stage"] == "formalize"
    assert by_id["p_stage_a_fail"]["model"] == expected_model_info


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))

"""Regression tests for per-stage model metadata in schema-v2 results."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import pipeline


class PipelineModelMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.input_path = self.root / "seed_problems.json"
        self.output_path = self.root / "results" / "run.jsonl"
        self.lean_project_dir = self.root / "lean_project"
        self.input_path.write_text(json.dumps([
            {
                "id": "p_solved",
                "category": "arithmetic_identity",
                "difficulty": 1,
                "nl_statement": "trivial true statement",
            },
            {
                "id": "p_stage_a_fail",
                "category": "arithmetic_identity",
                "difficulty": 1,
                "nl_statement": "statement that will not elaborate",
            },
        ]))

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    @staticmethod
    def metadata(*_args, **_kwargs) -> dict:
        return {
            "schema_version": 2,
            "run_id": "model-metadata-test",
            "started_at_utc": "2026-01-01T00:00:00Z",
        }

    def test_stage_models_are_explicit(self) -> None:
        self.assertEqual(
            set(pipeline.STAGE_MODELS),
            {"formalize", "sketch", "synthesize", "repair"},
        )
        self.assertTrue(all(pipeline.STAGE_MODELS.values()))

    def test_results_record_models_for_solved_and_stage_a_failed_problems(self) -> None:
        expected_models = {
            "formalize": "fake-strong-model",
            "sketch": "fake-strong-model",
            "synthesize": "fake-fast-model",
            "repair": "fake-fast-model",
        }
        solved_result = {
            "id": "p_solved",
            "solved": True,
            "repair_attempts": 0,
            "initial_synthesis_success": True,
            "success_within_repair_budget": True,
            "total_synthesis_attempts": 1,
            "wall_clock_seconds": 0.01,
            "final_proof": "theorem trivial_true : True := by trivial",
            "scratch_name": "p_solved_attempt1",
        }

        def fake_formalize(_statement, _project, scratch_id, max_attempts=3):
            if scratch_id == "p_stage_a_fail":
                return False, "theorem broken : False := by sorry", []
            return True, "theorem trivial_true : True := by trivial", []

        def fake_promote(_project, _scratch, final_id, destination_dir):
            return Path(destination_dir) / f"{final_id}.lean"

        with (
            patch.object(pipeline, "STAGE_MODELS", expected_models),
            patch.object(pipeline, "new_run_metadata", self.metadata),
            patch.object(pipeline, "formalize", side_effect=fake_formalize),
            patch.object(pipeline, "sketch", return_value="1. trivially true"),
            patch.object(
                pipeline,
                "synthesize_and_verify",
                return_value=(solved_result, []),
            ),
            patch.object(pipeline, "promote_scratch_to_final", side_effect=fake_promote),
        ):
            pipeline.run(self.input_path, self.output_path, self.lean_project_dir, max_repair=5)

        rows = [
            json.loads(line)
            for line in self.output_path.read_text().splitlines()
            if line.strip()
        ]
        by_id = {row["id"]: row for row in rows}
        self.assertEqual(by_id["p_solved"]["models"], expected_models)
        self.assertTrue(by_id["p_solved"]["solved"])
        self.assertEqual(by_id["p_stage_a_fail"]["models"], expected_models)
        self.assertFalse(by_id["p_stage_a_fail"]["solved"])
        self.assertEqual(by_id["p_stage_a_fail"]["failure_stage"], "formalize")


if __name__ == "__main__":
    unittest.main()

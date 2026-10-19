from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import pipeline


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.input_path = self.root / "input.json"
        self.output_path = self.root / "results.jsonl"
        self.project = self.root / "lean_project"
        self.project.mkdir()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_input(self, problems: list[dict]) -> None:
        self.input_path.write_text(json.dumps(problems))

    @staticmethod
    def metadata(*_args, **_kwargs) -> dict:
        return {
            "schema_version": 2,
            "run_id": "test-run",
            "started_at_utc": "2026-01-01T00:00:00Z",
        }

    def test_duplicate_ids_fail_before_creating_run_artifacts(self) -> None:
        self.write_input([
            {"id": "same", "nl_statement": "one", "category": "cat", "difficulty": 1},
            {"id": "same", "nl_statement": "two", "category": "cat", "difficulty": 1},
        ])

        with self.assertRaisesRegex(ValueError, "duplicate problem IDs"):
            pipeline.run(self.input_path, self.output_path, self.project, max_repair=1)

        self.assertFalse(self.output_path.exists())
        self.assertFalse(self.output_path.with_suffix(".run.json").exists())

    def test_unsafe_id_fails_before_creating_run_artifacts(self) -> None:
        self.write_input([
            {"id": "../escape", "nl_statement": "one", "category": "cat", "difficulty": 1}
        ])

        with self.assertRaisesRegex(ValueError, "unsafe problem IDs"):
            pipeline.run(self.input_path, self.output_path, self.project, max_repair=1)

        self.assertFalse(self.output_path.exists())
        self.assertFalse(self.output_path.with_suffix(".run.json").exists())

    def test_existing_output_is_not_overwritten(self) -> None:
        self.write_input([])
        self.output_path.write_text("historical data\n")

        with self.assertRaisesRegex(FileExistsError, "Refusing to overwrite"):
            pipeline.run(self.input_path, self.output_path, self.project, max_repair=1)

        self.assertEqual(self.output_path.read_text(), "historical data\n")

    def test_stage_a_failure_writes_consistent_result_and_attempt(self) -> None:
        self.write_input([
            {"id": "p1", "nl_statement": "statement", "category": "cat", "difficulty": 1}
        ])
        statement_attempt = {
            "attempt": 1,
            "model": "strong",
            "success": False,
            "errors": ["bad statement"],
            "verification": {"exit_code": 1},
        }

        with (
            patch.object(pipeline, "new_run_metadata", self.metadata),
            patch.object(
                pipeline, "formalize", return_value=(False, "theorem bad : False := by sorry", [statement_attempt])
            ),
        ):
            pipeline.run(self.input_path, self.output_path, self.project, max_repair=1)

        result = json.loads(self.output_path.read_text())
        manifest = json.loads(self.output_path.with_suffix(".run.json").read_text())
        attempt = json.loads(
            (self.root / "attempts" / "test-run" / "p1.jsonl").read_text()
        )
        self.assertEqual(result["run_id"], manifest["run_id"])
        self.assertEqual(result["total_synthesis_attempts"], 0)
        self.assertIsNone(result["initial_synthesis_success"])
        self.assertEqual(attempt["stage"], "formalize")
        self.assertEqual(attempt["run_id"], "test-run")
        self.assertEqual(manifest["status"], "completed")

    def test_synthesis_and_repair_attempts_have_distinct_stages(self) -> None:
        self.write_input([
            {"id": "p1", "nl_statement": "statement", "category": "cat", "difficulty": 1}
        ])
        result = {
            "solved": False,
            "repair_attempts": 1,
            "initial_synthesis_success": False,
            "success_within_repair_budget": False,
            "total_synthesis_attempts": 2,
            "wall_clock_seconds": 1.0,
            "final_proof": "theorem p1 : True := by trivial",
            "scratch_name": None,
        }
        attempts = [
            {"is_initial_synthesis": True, "model": pipeline.FAST_MODEL, "verification": {}},
            {"is_initial_synthesis": False, "model": pipeline.FAST_MODEL, "verification": {}},
        ]

        with (
            patch.object(pipeline, "new_run_metadata", self.metadata),
            patch.object(pipeline, "formalize", return_value=(True, "theorem p1 : True := by sorry", [])),
            patch.object(pipeline, "sketch", return_value="sketch"),
            patch.object(pipeline, "synthesize_and_verify", return_value=(result, attempts)),
        ):
            pipeline.run(self.input_path, self.output_path, self.project, max_repair=1)

        records = [
            json.loads(line)
            for line in (self.root / "attempts" / "test-run" / "p1.jsonl").read_text().splitlines()
        ]
        self.assertEqual([record["stage"] for record in records], ["synthesize", "repair"])
        self.assertTrue(records[0]["is_initial_synthesis"])
        self.assertFalse(records[1]["is_initial_synthesis"])

    def test_exception_marks_manifest_failed(self) -> None:
        self.write_input([
            {"id": "p1", "nl_statement": "statement", "category": "cat", "difficulty": 1}
        ])

        with (
            patch.object(pipeline, "new_run_metadata", self.metadata),
            patch.object(pipeline, "formalize", side_effect=RuntimeError("provider unavailable")),
            self.assertRaisesRegex(RuntimeError, "provider unavailable"),
        ):
            pipeline.run(self.input_path, self.output_path, self.project, max_repair=1)

        manifest = json.loads(self.output_path.with_suffix(".run.json").read_text())
        self.assertEqual(manifest["status"], "failed")
        self.assertEqual(manifest["failure_type"], "RuntimeError")

    def test_attempt_directory_failure_does_not_create_running_manifest(self) -> None:
        self.write_input([])

        with (
            patch.object(pipeline, "new_run_metadata", self.metadata),
            patch.object(pipeline, "_create_attempts_dir", side_effect=OSError("disk full")),
            self.assertRaisesRegex(OSError, "disk full"),
        ):
            pipeline.run(self.input_path, self.output_path, self.project, max_repair=1)

        self.assertFalse(self.output_path.with_suffix(".run.json").exists())

    def test_initial_manifest_write_failure_cleans_new_attempt_directory(self) -> None:
        self.write_input([])

        with (
            patch.object(pipeline, "new_run_metadata", self.metadata),
            patch.object(pipeline, "_write_json", side_effect=OSError("disk full")),
            self.assertRaisesRegex(OSError, "disk full"),
        ):
            pipeline.run(self.input_path, self.output_path, self.project, max_repair=1)

        self.assertFalse(self.output_path.with_suffix(".run.json").exists())
        self.assertFalse((self.root / "attempts" / "test-run").exists())


if __name__ == "__main__":
    unittest.main()

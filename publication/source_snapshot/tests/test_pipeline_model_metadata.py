"""Regression tests for per-stage model metadata in schema-v2 results."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
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
            "configuration": {
                "experiment_config": _kwargs.get("experiment_config")
            },
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

        def fake_formalize(
            _statement, _project, scratch_id, max_attempts=3, model=None
        ):
            if scratch_id == "p_stage_a_fail":
                return False, "theorem broken : False := by sorry", []
            return True, "theorem trivial_true : True := by trivial", []

        def fake_promote(_project, _scratch, final_id, destination_dir):
            return Path(destination_dir) / f"{final_id}.lean"

        with (
            patch.object(pipeline, "STAGE_MODELS", expected_models),
            patch.object(pipeline, "new_run_metadata", self.metadata),
            patch.object(pipeline, "formalize", side_effect=fake_formalize),
            patch.object(
                pipeline,
                "sketch_with_metadata",
                return_value=SimpleNamespace(content="1. trivially true", metadata={}),
            ),
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
        self.assertEqual(by_id["p_solved"]["experiment_config"], "full_pipeline")
        self.assertTrue(by_id["p_solved"]["solved"])
        self.assertEqual(by_id["p_stage_a_fail"]["models"], expected_models)
        self.assertEqual(by_id["p_stage_a_fail"]["experiment_config"], "full_pipeline")
        self.assertFalse(by_id["p_stage_a_fail"]["solved"])
        self.assertEqual(by_id["p_stage_a_fail"]["failure_stage"], "formalize")
        manifest = json.loads(self.output_path.with_suffix(".run.json").read_text())
        self.assertEqual(
            manifest["configuration"]["experiment_config"], "full_pipeline"
        )

    def _run_single_problem(self, *, cli_args: list[str] | None = None, **kwargs):
        self.input_path.write_text(json.dumps([
            {
                "id": "p1",
                "category": "arithmetic_identity",
                "difficulty": 1,
                "nl_statement": "trivial true statement",
            }
        ]))
        synthesis_result = {
            "solved": True,
            "repair_attempts": 0,
            "initial_synthesis_success": True,
            "success_within_repair_budget": True,
            "total_synthesis_attempts": 1,
            "wall_clock_seconds": 0.01,
            "final_proof": "theorem p1 : True := by trivial",
            "scratch_name": "p1_attempt1",
        }
        synthesis_attempts = [
            {
                "is_initial_synthesis": True,
                "attempt_number": 1,
                "model": "synthesis-model",
            }
        ]

        with (
            patch.object(pipeline, "new_run_metadata", self.metadata),
            patch.object(
                pipeline,
                "formalize",
                return_value=(True, "theorem p1 : True := by sorry", []),
            ) as formalize_call,
            patch.object(
                pipeline,
                "sketch_with_metadata",
                return_value=SimpleNamespace(
                    content="a sketch",
                    metadata={"model": "sketch-model"},
                ),
            ) as sketch_call,
            patch.object(
                pipeline,
                "synthesize_and_verify",
                return_value=(synthesis_result, synthesis_attempts),
            ) as synthesize_call,
            patch.object(
                pipeline,
                "promote_scratch_to_final",
                return_value=self.root / "final.lean",
            ),
        ):
            if cli_args is not None:
                pipeline.main(cli_args)
            else:
                pipeline.run(
                    self.input_path,
                    self.output_path,
                    self.lean_project_dir,
                    max_repair=1,
                    **kwargs,
                )

        result = json.loads(self.output_path.read_text())
        manifest = json.loads(self.output_path.with_suffix(".run.json").read_text())
        attempt_records = [
            json.loads(line)
            for line in (
                self.root / "results" / "attempts" / "model-metadata-test" / "p1.jsonl"
            ).read_text().splitlines()
        ]
        return result, manifest, attempt_records, formalize_call, sketch_call, synthesize_call

    def test_no_sketch_cli_skips_only_sketch_stage(self) -> None:
        result, manifest, attempts, formalize, sketch, synthesize = (
            self._run_single_problem(
                cli_args=[
                    "--input", str(self.input_path),
                    "--out", str(self.output_path),
                    "--lean-project", str(self.lean_project_dir),
                    "--no-sketch",
                ]
            )
        )

        sketch.assert_not_called()
        self.assertEqual(formalize.call_args.kwargs["model"], pipeline.STRONG_MODEL)
        self.assertEqual(synthesize.call_args.args[2], "")
        self.assertEqual(synthesize.call_args.kwargs["model"], pipeline.FAST_MODEL)
        self.assertEqual(result["experiment_config"], "no_sketch")
        self.assertEqual(
            result["models"],
            {"formalize": pipeline.STRONG_MODEL,
             "synthesize": pipeline.FAST_MODEL,
             "repair": pipeline.FAST_MODEL},
        )
        self.assertEqual(
            manifest["configuration"]["experiment_config"], "no_sketch"
        )
        self.assertNotIn("sketch", [record["stage"] for record in attempts])
        self.assertTrue(
            all(record["experiment_config"] == "no_sketch" for record in attempts)
        )

    def test_fast_model_only_uses_fast_model_for_every_stage(self) -> None:
        result, manifest, _attempts, formalize, sketch, synthesize = (
            self._run_single_problem(experiment_config="fast_model_only")
        )

        self.assertEqual(formalize.call_args.kwargs["model"], pipeline.FAST_MODEL)
        self.assertEqual(sketch.call_args.kwargs["model"], pipeline.FAST_MODEL)
        self.assertEqual(synthesize.call_args.kwargs["model"], pipeline.FAST_MODEL)
        self.assertEqual(
            result["models"],
            {
                "formalize": pipeline.FAST_MODEL,
                "sketch": pipeline.FAST_MODEL,
                "synthesize": pipeline.FAST_MODEL,
                "repair": pipeline.FAST_MODEL,
            },
        )
        self.assertEqual(result["experiment_config"], "fast_model_only")
        self.assertEqual(
            manifest["configuration"]["experiment_config"], "fast_model_only"
        )

    def test_model_overrides_select_their_applicable_stages(self) -> None:
        result, _manifest, _attempts, formalize, sketch, synthesize = (
            self._run_single_problem(
                strong_model="custom-strong",
                fast_model="custom-fast",
            )
        )

        self.assertEqual(formalize.call_args.kwargs["model"], "custom-strong")
        self.assertEqual(sketch.call_args.kwargs["model"], "custom-strong")
        self.assertEqual(synthesize.call_args.kwargs["model"], "custom-fast")
        self.assertEqual(
            result["models"],
            {
                "formalize": "custom-strong",
                "sketch": "custom-strong",
                "synthesize": "custom-fast",
                "repair": "custom-fast",
            },
        )

    def test_contradictory_config_and_no_sketch_flag_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "--no-sketch conflicts"):
            pipeline.resolve_experiment_config(
                "fast_model_only",
                no_sketch=True,
            )
    def test_stage_settings_cover_only_active_stages_with_effective_values(self) -> None:
        full = pipeline.stage_settings_for(
            {
                "formalize": "openai/gpt-oss-120b",
                "sketch": "openai/gpt-oss-120b",
                "synthesize": "openai/gpt-oss-20b",
                "repair": "openai/gpt-oss-20b",
            }
        )
        self.assertEqual(set(full), {"formalize", "sketch", "synthesize", "repair"})
        self.assertEqual(full["formalize"]["max_completion_tokens"], 500)
        self.assertEqual(full["sketch"]["max_completion_tokens"], 600)
        self.assertEqual(full["sketch"]["temperature"], 0.3)
        self.assertIsNone(full["formalize"]["reasoning_effort"])
        self.assertEqual(full["synthesize"]["reasoning_effort"], "low")
        self.assertEqual(full["repair"], full["synthesize"])

        no_sketch = pipeline.stage_settings_for(
            {"formalize": "a", "synthesize": "b", "repair": "b"}
        )
        self.assertNotIn("sketch", no_sketch)
        self.assertIsNone(no_sketch["synthesize"]["reasoning_effort"])

    def test_run_passes_stage_settings_to_manifest_metadata(self) -> None:
        captured = {}

        original = PipelineModelMetadataTests.metadata

        def capture(*args, **kwargs):
            captured.update(kwargs)
            return original(*args, **kwargs)

        with patch.object(
            PipelineModelMetadataTests, "metadata", staticmethod(capture)
        ):
            self._run_single_problem(experiment_config="no_sketch")

        self.assertEqual(
            set(captured["stage_settings"]), {"formalize", "synthesize", "repair"}
        )


if __name__ == "__main__":
    unittest.main()

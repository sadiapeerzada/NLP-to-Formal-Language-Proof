from __future__ import annotations

import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "eval"))

import metrics


class TestFrozenRunCompleteness:
    expected_ids = ["test_a", "test_b"]
    configurations = ["full_pipeline", "no_sketch"]
    dataset_hash = "a" * 64

    def setup_method(self) -> None:
        self.tempdir = TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.manifest_path = self.root / "frozen-test-manifest.json"
        self.manifest_path.write_text(
            json.dumps(
                {
                    "dataset_version": "test-v1",
                    "expected_ids": self.expected_ids,
                    "dataset_sha256": self.dataset_hash,
                    "required_configurations": self.configurations,
                }
            )
        )

    def teardown_method(self) -> None:
        self.tempdir.cleanup()

    def write_run(
        self,
        configuration: str,
        records: list[dict],
        *,
        status: str = "completed",
        run_id: str | None = None,
        completed_problem_count: int | None = None,
    ) -> Path:
        run_id = run_id or f"run-{configuration}"
        results_path = self.root / f"{configuration}.jsonl"
        results_path.write_text(
            "\n".join(json.dumps(record) for record in records) + "\n"
        )
        results_path.with_suffix(".run.json").write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "run_id": run_id,
                    "status": status,
                    "completed_problem_count": (
                        len(records)
                        if completed_problem_count is None
                        else completed_problem_count
                    ),
                    "input": {"sha256": self.dataset_hash},
                    "configuration": {
                        "experiment_config": configuration,
                        "max_repair": 2,
                    },
                }
            )
        )
        return results_path

    @staticmethod
    def records(configuration: str, run_id: str, ids: list[str]) -> list[dict]:
        return [
            {
                "schema_version": 2,
                "run_id": run_id,
                "experiment_config": configuration,
                "id": problem_id,
                "category": "arithmetic",
                "difficulty": 1,
                "solved": False,
                "repair_attempts": 0,
                "initial_synthesis_success": None,
                "success_within_repair_budget": False,
                "total_synthesis_attempts": 0,
            }
            for problem_id in ids
        ]

    def complete_runs(self) -> list[Path]:
        paths = []
        for configuration in self.configurations:
            run_id = f"run-{configuration}"
            paths.append(
                self.write_run(
                    configuration,
                    self.records(configuration, run_id, self.expected_ids),
                )
            )
        return paths

    def check_fails(self, paths: list[Path], message: str) -> None:
        with pytest.raises(ValueError, match=message):
            metrics.validate_frozen_runs(paths, self.manifest_path)

    def test_complete_runs_pass_gate_and_frozen_analysis_reports_each_condition(
        self, capsys
    ) -> None:
        paths = self.complete_runs()

        runs = metrics.validate_frozen_runs(paths, self.manifest_path)

        assert set(runs) == set(self.configurations)
        for configuration in self.configurations:
            assert {record["id"] for record in runs[configuration]} == set(
                self.expected_ids
            )
        metrics.main(
            paths[0],
            frozen_manifest=self.manifest_path,
            additional_paths=paths[1:],
        )
        output = capsys.readouterr().out
        assert "Configuration: full_pipeline" in output
        assert "Configuration: no_sketch" in output

    def test_missing_result_is_incomplete(self) -> None:
        paths = self.complete_runs()
        incomplete = self.records("full_pipeline", "run-full_pipeline", ["test_a"])
        paths[0] = self.write_run("full_pipeline", incomplete)

        self.check_fails(paths, "missing expected result IDs: test_b")

    def test_duplicate_result_id_is_rejected(self) -> None:
        paths = self.complete_runs()
        duplicate_rows = self.records(
            "full_pipeline", "run-full_pipeline", ["test_a", "test_a"]
        )
        paths[0] = self.write_run("full_pipeline", duplicate_rows)

        self.check_fails(paths, "duplicate result IDs: test_a")

    def test_unexpected_result_id_is_rejected(self) -> None:
        paths = self.complete_runs()
        rows = self.records(
            "full_pipeline", "run-full_pipeline", ["test_a", "other"]
        )
        paths[0] = self.write_run("full_pipeline", rows)

        self.check_fails(paths, "unexpected result IDs: other")

    def test_result_configuration_identity_must_match_run_manifest(self) -> None:
        paths = self.complete_runs()
        rows = self.records("no_sketch", "run-full_pipeline", self.expected_ids)
        paths[0] = self.write_run("full_pipeline", rows)

        self.check_fails(paths, "experiment_config does not match")

    def test_failed_or_incomplete_run_status_is_rejected(self) -> None:
        paths = self.complete_runs()
        rows = self.records("full_pipeline", "run-full_pipeline", self.expected_ids)
        paths[0] = self.write_run(
            "full_pipeline",
            rows,
            status="failed",
            completed_problem_count=1,
        )

        with pytest.raises(ValueError) as error:
            metrics.validate_frozen_runs(paths, self.manifest_path)
        assert "status must be 'completed'" in str(error.value)
        assert "completed_problem_count must equal 2" in str(error.value)

    def test_missing_required_configuration_is_rejected(self) -> None:
        paths = [
            self.write_run(
                "full_pipeline",
                self.records("full_pipeline", "run-full_pipeline", self.expected_ids),
            )
        ]

        self.check_fails(paths, "Missing required configuration runs: no_sketch")

    def test_run_input_hash_must_match_frozen_dataset(self) -> None:
        paths = self.complete_runs()
        run_manifest_path = paths[0].with_suffix(".run.json")
        run_manifest = json.loads(run_manifest_path.read_text())
        run_manifest["input"]["sha256"] = "b" * 64
        run_manifest_path.write_text(json.dumps(run_manifest))

        self.check_fails(paths, "input.sha256 does not match frozen dataset_sha256")

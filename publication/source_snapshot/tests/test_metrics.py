from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parents[1] / "eval"))

import metrics


class MetricsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = TemporaryDirectory()
        self.path = Path(self.tempdir.name) / "results.jsonl"

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_records(self, records: list[dict]) -> None:
        self.path.write_text("\n".join(json.dumps(record) for record in records) + "\n")

    def test_historical_records_keep_recorded_final_rate_and_breakdowns(self) -> None:
        self.write_records([
            {
                "id": "a",
                "category": "arithmetic",
                "difficulty": 1,
                "solved": True,
                "repair_attempts": 1,
            },
            {
                "id": "b",
                "category": "divisibility",
                "difficulty": 2,
                "solved": False,
                "repair_attempts": 5,
                "failure_stage": "synthesize",
            },
        ])

        output = metrics.report(metrics.load(self.path))

        self.assertIn("Final verified successes: 1/2 = 50.0%", output)
        self.assertIn(
            "Historical recorded final solved rate (not attempt-0 pass@1)",
            output,
        )
        self.assertIn("Historical category breakdown", output)
        self.assertIn("difficulty 2: 0/1 = 0.0%", output)
        self.assertIn("Failure breakdown by stage:\n  synthesize: 1", output)

    def test_v2_reports_initial_and_repair_budget_rates_separately(self) -> None:
        self.write_records([
            {
                "schema_version": 2,
                "id": "a",
                "category": "arithmetic",
                "difficulty": 1,
                "solved": True,
                "repair_attempts": 0,
                "total_synthesis_attempts": 1,
                "initial_synthesis_success": True,
                "success_within_repair_budget": True,
            },
            {
                "schema_version": 2,
                "id": "b",
                "category": "arithmetic",
                "difficulty": 1,
                "solved": True,
                "repair_attempts": 1,
                "total_synthesis_attempts": 2,
                "initial_synthesis_success": False,
                "success_within_repair_budget": True,
            },
            {
                "schema_version": 2,
                "id": "c",
                "category": "induction",
                "difficulty": 3,
                "solved": False,
                "repair_attempts": 0,
                "total_synthesis_attempts": 0,
                "initial_synthesis_success": None,
                "success_within_repair_budget": False,
                "failure_stage": "formalize",
            },
        ])

        output = metrics.report(metrics.load(self.path))

        self.assertIn("Final verified successes: 2/3 = 66.7%", output)
        self.assertIn(
            "Attempt-0 success (initial synthesis candidate, among synthesized problems): "
            "1/2 = 50.0%",
            output,
        )
        self.assertIn(
            "Post-repair success within configured repair budget: 2/3 = 66.7%",
            output,
        )
        self.assertNotIn("pass@1", output)
        self.assertIn(
            "arithmetic            : initial 1/2 = 50.0%; within repair budget 2/2 = 100.0%",
            output,
        )
        self.assertIn(
            "difficulty 3: initial n/a (0 problems); within repair budget 0/1 = 0.0%",
            output,
        )
        self.assertIn("Avg total synthesis attempts (all problems): 1.00 (3 problems)", output)

    def test_post_repair_success_obeys_repair_budget_boundary(self) -> None:
        self.write_records([
            {
                "schema_version": 2,
                "id": "initial",
                "category": "arithmetic",
                "difficulty": 1,
                "solved": True,
                "repair_attempts": 0,
                "total_synthesis_attempts": 1,
                "initial_synthesis_success": True,
                "success_within_repair_budget": True,
            },
            {
                "schema_version": 2,
                "id": "last_allowed_repair",
                "category": "arithmetic",
                "difficulty": 1,
                "solved": True,
                "repair_attempts": 2,
                "total_synthesis_attempts": 3,
                "initial_synthesis_success": False,
                "success_within_repair_budget": True,
            },
        ])

        results = metrics.load(self.path)
        output = metrics.report(results, max_repair=2)

        self.assertIn("Attempt-0 success", output)
        self.assertIn("1/2 = 50.0%", output)
        self.assertIn(
            "Post-repair success within configured repair budget (2 repairs): "
            "2/2 = 100.0%",
            output,
        )
        with self.assertRaisesRegex(ValueError, "exceed configured repair budget"):
            metrics.report(results, max_repair=1)
        self.assertIn(
            "Post-repair success within configured repair budget (0 repairs): "
            "1/1 = 100.0%",
            metrics.report(results[:1], max_repair=0),
        )

    def test_synthesis_attempt_counts_must_include_initial_candidate(self) -> None:
        record = {
            "schema_version": 2,
            "id": "inconsistent",
            "category": "arithmetic",
            "difficulty": 1,
            "solved": False,
            "repair_attempts": 1,
            "total_synthesis_attempts": 1,
            "initial_synthesis_success": False,
            "success_within_repair_budget": False,
        }
        self.write_records([record])

        with self.assertRaisesRegex(ValueError, "must equal 'repair_attempts' \\+ 1"):
            metrics.load(self.path)

    def test_manifest_repair_budget_is_used_by_cli_report(self) -> None:
        self.write_records([
            {
                "schema_version": 2,
                "id": "boundary",
                "category": "arithmetic",
                "difficulty": 1,
                "solved": False,
                "repair_attempts": 1,
                "total_synthesis_attempts": 2,
                "initial_synthesis_success": False,
                "success_within_repair_budget": False,
            },
        ])
        self.path.with_suffix(".run.json").write_text(
            json.dumps({"configuration": {"max_repair": 1}})
        )

        output = metrics.report(
            metrics.load(self.path),
            max_repair=metrics._load_repair_budget(self.path),
        )

        self.assertIn(
            "Post-repair success within configured repair budget (1 repairs): "
            "0/1 = 0.0%",
            output,
        )

    def test_empty_file_has_no_division_by_zero(self) -> None:
        self.path.write_text("")

        output = metrics.report(metrics.load(self.path))

        self.assertEqual(
            output,
            "Total problems: 0\n"
            "Final verified successes: n/a (0 problems)\n"
            "Attempt-0 success (initial synthesis candidate): n/a (0 problems)\n"
            "Post-repair success within configured repair budget: n/a (0 problems)",
        )

    def test_malformed_json_reports_line_number(self) -> None:
        self.path.write_text('{"id": "ok"}\n{not json}\n')

        with self.assertRaisesRegex(ValueError, r"line 1: missing required field"):
            metrics.load(self.path)

        self.path.write_text("\n{not json}\n")
        with self.assertRaisesRegex(ValueError, r"line 2: invalid JSON"):
            metrics.load(self.path)


if __name__ == "__main__":
    unittest.main()

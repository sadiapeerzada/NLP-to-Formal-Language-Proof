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
        self.assertIn("Historical recorded final solved rate (legacy pass@1 label)", output)
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
            "Initial synthesis success rate (among synthesized problems): 1/2 = 50.0%",
            output,
        )
        self.assertIn("Success within repair budget: 2/3 = 66.7%", output)
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

    def test_empty_file_has_no_division_by_zero(self) -> None:
        self.path.write_text("")

        output = metrics.report(metrics.load(self.path))

        self.assertEqual(
            output,
            "Total problems: 0\nFinal verified successes: n/a (0 problems)",
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

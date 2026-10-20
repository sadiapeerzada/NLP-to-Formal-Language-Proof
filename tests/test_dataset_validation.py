from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from dataset_validation import validate_dataset


class DatasetValidationTests(unittest.TestCase):
    @staticmethod
    def legacy_problem(problem_id: str = "pilot_001") -> dict:
        return {
            "id": problem_id,
            "nl_statement": "A statement.",
            "category": "arithmetic_identity",
            "difficulty": 1,
            "expected_lean_statement": "theorem sample : True",
        }

    @staticmethod
    def documented_problem(problem_id: str = "research_001") -> dict:
        return {
            **DatasetValidationTests.legacy_problem(problem_id),
            "split": "development",
            "source_citation": "Verified hand-authored exercise.",
            "license": "CC0-1.0",
            "reference_lean_statement_provenance": (
                "Written and reviewed by the dataset authors."
            ),
        }

    def test_existing_pilot_records_remain_usable_as_legacy(self) -> None:
        pilot_path = (
            Path(__file__).parents[1]
            / "data"
            / "pilots"
            / "nl2lean-pilot-seed3-v1.json"
        )
        report = validate_dataset(json.loads(pilot_path.read_text()))

        self.assertTrue(report.is_valid)
        self.assertEqual(len(report.problems), 3)
        self.assertTrue(
            all(
                problem.status == "legacy_missing_provenance"
                for problem in report.problems
            )
        )
        self.assertTrue(all(problem.split is None for problem in report.problems))

    def test_documented_record_accepts_explicit_split_and_provenance(self) -> None:
        report = validate_dataset([self.documented_problem()])

        self.assertTrue(report.is_valid)
        self.assertEqual(report.problems[0].status, "documented")
        self.assertEqual(report.problems[0].split, "development")

    def test_source_url_can_substitute_for_source_citation(self) -> None:
        problem = self.documented_problem()
        del problem["source_citation"]
        problem["source_url"] = "https://example.org/reference"

        report = validate_dataset([problem], require_provenance=True)

        self.assertTrue(report.is_valid)
        self.assertEqual(report.problems[0].status, "documented")

    def test_invalid_source_url_identifies_problem_and_field(self) -> None:
        problem = self.documented_problem("bad_url")
        problem["source_url"] = "not-a-url"

        report = validate_dataset([problem], require_provenance=True)

        self.assertFalse(report.is_valid)
        self.assertEqual(report.problems[0].status, "invalid_provenance")
        self.assertEqual(report.problems[0].missing_fields, ())
        self.assertEqual(report.problems[0].invalid_fields, ("source_url",))
        self.assertTrue(
            any(
                "problem 'bad_url': field 'source_url'" in error
                for error in report.errors
            )
        )
        self.assertFalse(
            any("missing provenance field" in error for error in report.errors)
        )

    def test_invalid_supplied_license_prevents_documented_status(self) -> None:
        problem = self.documented_problem("bad_license")
        problem["license"] = " "

        report = validate_dataset([problem], require_provenance=True)

        self.assertFalse(report.is_valid)
        self.assertEqual(report.problems[0].status, "invalid_provenance")
        self.assertEqual(report.problems[0].missing_fields, ())
        self.assertEqual(report.problems[0].invalid_fields, ("license",))
        self.assertTrue(
            any(
                "problem 'bad_license': field 'license'" in error
                for error in report.errors
            )
        )
        self.assertFalse(
            any(
                "problem 'bad_license': missing provenance field 'license'"
                in error
                for error in report.errors
            )
        )

    def test_invalid_split_identifies_problem_and_field(self) -> None:
        problem = self.legacy_problem("bad_split")
        problem["split"] = "held_out"

        report = validate_dataset([problem])

        self.assertFalse(report.is_valid)
        self.assertIn(
            "problem 'bad_split': field 'split' must be one of development, "
            "test; got 'held_out'.",
            report.errors,
        )
        self.assertIsNone(report.problems[0].split)

    def test_non_string_split_is_reported_without_crashing(self) -> None:
        problem = self.legacy_problem("bad_split_type")
        problem["split"] = ["test"]

        report = validate_dataset([problem])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any(
                "problem 'bad_split_type': field 'split'" in error
                for error in report.errors
            )
        )
        self.assertIsNone(report.problems[0].split)

    def test_required_fields_and_unique_ids_are_validated_actionably(self) -> None:
        missing = {"id": "missing_required", "difficulty": 2}
        duplicate_a = self.legacy_problem("duplicate")
        duplicate_b = self.legacy_problem("duplicate")

        report = validate_dataset([missing, duplicate_a, duplicate_b])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any(
                "problem 'missing_required': missing required field 'nl_statement'"
                in error
                for error in report.errors
            )
        )
        self.assertIn(
            "problem 'duplicate': duplicate value for field 'id'.", report.errors
        )

    def test_strict_mode_reports_each_missing_provenance_requirement(self) -> None:
        report = validate_dataset(
            [self.legacy_problem("needs_provenance")],
            require_provenance=True,
        )

        self.assertFalse(report.is_valid)
        self.assertEqual(
            report.problems[0].status,
            "legacy_missing_provenance",
        )
        self.assertEqual(
            report.problems[0].missing_fields,
            (
                "source_citation or source_url",
                "license",
                "reference_lean_statement_provenance",
            ),
        )
        self.assertEqual(report.problems[0].invalid_fields, ())
        self.assertTrue(
            all("problem 'needs_provenance':" in error for error in report.errors)
        )

    def test_partial_provenance_is_classified_incomplete(self) -> None:
        problem = self.legacy_problem("partial")
        problem["license"] = "Verified license"

        report = validate_dataset([problem])

        self.assertTrue(report.is_valid)
        self.assertEqual(report.problems[0].status, "incomplete_provenance")
        self.assertEqual(
            report.problems[0].missing_fields,
            (
                "source_citation or source_url",
                "reference_lean_statement_provenance",
            ),
        )

    def test_invalid_required_values_produce_field_specific_errors(self) -> None:
        problem = self.legacy_problem("bad_values")
        problem["nl_statement"] = " "
        problem["difficulty"] = True
        problem["license"] = ""

        report = validate_dataset([problem])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any("problem 'bad_values': field 'nl_statement'" in error for error in report.errors)
        )
        self.assertTrue(
            any("problem 'bad_values': field 'difficulty'" in error for error in report.errors)
        )
        self.assertTrue(
            any("problem 'bad_values': field 'license'" in error for error in report.errors)
        )


if __name__ == "__main__":
    unittest.main()

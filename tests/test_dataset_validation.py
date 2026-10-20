from __future__ import annotations

import hashlib
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from dataset_validation import (
    main as dataset_validation_main,
    validate_dataset,
    validate_research_dataset,
)


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

    @staticmethod
    def research_manifest(
        problem_ids: list[str], dataset_hash: str = "a" * 64
    ) -> dict:
        return {
            "dataset_version": "research-v1",
            "expected_ids": problem_ids,
            "dataset_sha256": dataset_hash,
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

    def test_non_object_record_is_reported_in_compatibility_and_research_modes(
        self,
    ) -> None:
        problem = self.documented_problem("valid_after_malformed")
        dataset = [None, problem]

        compatibility_report = validate_dataset(dataset)
        research_report = validate_research_dataset(
            dataset,
            self.research_manifest(["valid_after_malformed"]),
            "a" * 64,
        )

        expected_error = "record 1: expected a JSON object."
        self.assertIn(expected_error, compatibility_report.errors)
        self.assertEqual(
            [record.problem_id for record in compatibility_report.problems],
            ["valid_after_malformed"],
        )
        self.assertIn(expected_error, research_report.errors)
        self.assertEqual(
            [record.problem_id for record in research_report.problems],
            ["valid_after_malformed"],
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

    def test_research_mode_accepts_complete_frozen_dataset_and_families(self) -> None:
        first = self.documented_problem("variant_a")
        second = self.documented_problem("variant_b")
        third = self.documented_problem("ungrouped")
        first["problem_family"] = "distributivity_nat"
        second["problem_family"] = "distributivity_nat"

        report = validate_research_dataset(
            [first, second, third],
            self.research_manifest(["variant_a", "variant_b", "ungrouped"]),
            "a" * 64,
        )

        self.assertTrue(report.is_valid)
        self.assertEqual(report.dataset_version, "research-v1")
        self.assertEqual(
            [problem.problem_family for problem in report.problems],
            ["distributivity_nat", "distributivity_nat", None],
        )

    def test_research_mode_reports_missing_provenance(self) -> None:
        problem = self.legacy_problem("missing_provenance")

        report = validate_research_dataset(
            [problem],
            self.research_manifest(["missing_provenance"]),
            "a" * 64,
        )

        self.assertFalse(report.is_valid)
        self.assertTrue(report.missing_errors)
        self.assertEqual(report.problems[0].status, "legacy_missing_provenance")

    def test_research_mode_reports_invalid_provenance_separately(self) -> None:
        problem = self.documented_problem("invalid_provenance")
        problem["source_url"] = "not-a-url"

        report = validate_research_dataset(
            [problem],
            self.research_manifest(["invalid_provenance"]),
            "a" * 64,
        )

        self.assertFalse(report.is_valid)
        self.assertTrue(report.invalid_errors)
        self.assertEqual(report.missing_errors, ())
        self.assertEqual(report.problems[0].status, "invalid_provenance")

    def test_research_mode_requires_explicit_split(self) -> None:
        problem = self.documented_problem("missing_split")
        del problem["split"]

        report = validate_research_dataset(
            [problem],
            self.research_manifest(["missing_split"]),
            "a" * 64,
        )

        self.assertFalse(report.is_valid)
        self.assertIn(
            "problem 'missing_split': missing required research split field 'split'.",
            report.split_errors,
        )

    def test_research_mode_reports_invalid_split_as_split_error(self) -> None:
        problem = self.documented_problem("invalid_split")
        problem["split"] = "held_out"

        report = validate_research_dataset(
            [problem],
            self.research_manifest(["invalid_split"]),
            "a" * 64,
        )

        self.assertFalse(report.is_valid)
        self.assertTrue(report.split_errors)

    def test_research_mode_reports_duplicate_problem_ids(self) -> None:
        first = self.documented_problem("duplicate")
        second = self.documented_problem("duplicate")

        report = validate_research_dataset(
            [first, second],
            self.research_manifest(["duplicate"]),
            "a" * 64,
        )

        self.assertFalse(report.is_valid)
        self.assertEqual(len(report.duplicate_errors), 1)

    def test_research_mode_rejects_wrong_dataset_hash(self) -> None:
        problem = self.documented_problem()

        report = validate_research_dataset(
            [problem],
            self.research_manifest(["research_001"], "b" * 64),
            "a" * 64,
        )

        self.assertIn(
            "manifest: dataset_sha256 does not match the dataset file.",
            report.manifest_errors,
        )

    def test_research_mode_requires_dataset_version_in_manifest(self) -> None:
        manifest = self.research_manifest(["research_001"])
        del manifest["dataset_version"]

        report = validate_research_dataset(
            [self.documented_problem()],
            manifest,
            "a" * 64,
        )

        self.assertIn(
            "manifest: field 'dataset_version' must be a non-empty string.",
            report.manifest_errors,
        )

    def test_research_mode_reports_missing_and_extra_manifest_ids(self) -> None:
        problem = self.documented_problem("present")
        extra = self.documented_problem("unexpected")

        report = validate_research_dataset(
            [problem, extra],
            self.research_manifest(["present", "missing"]),
            "a" * 64,
        )

        self.assertTrue(
            any("expected IDs missing from dataset: missing" in error
                for error in report.manifest_errors)
        )
        self.assertTrue(
            any("unexpected dataset IDs: unexpected" in error
                for error in report.manifest_errors)
        )

    def test_research_mode_rejects_invalid_optional_problem_family(self) -> None:
        problem = self.documented_problem()
        problem["problem_family"] = " "

        report = validate_research_dataset(
            [problem],
            self.research_manifest(["research_001"]),
            "a" * 64,
        )

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any("field 'problem_family'" in error for error in report.invalid_errors)
        )

    def test_research_cli_reports_error_category_counts(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            dataset_path = root / "dataset.json"
            manifest_path = root / "manifest.json"
            dataset_path.write_text(json.dumps([self.legacy_problem("legacy")]))
            manifest_path.write_text(
                json.dumps(self.research_manifest(["legacy"], "0" * 64))
            )
            stdout = StringIO()
            stderr = StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = dataset_validation_main(
                    [str(dataset_path), "--research-manifest", str(manifest_path)]
                )

        self.assertEqual(exit_code, 1)
        self.assertIn(
            "validation errors: missing=3, invalid=0, split=1, "
            "duplicate IDs=0, manifest=1",
            stdout.getvalue(),
        )

    def test_research_cli_accepts_matching_file_hash_and_manifest(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            dataset_path = root / "dataset.json"
            manifest_path = root / "manifest.json"
            raw_dataset = json.dumps([self.documented_problem()]).encode()
            dataset_path.write_bytes(raw_dataset)
            manifest_path.write_text(
                json.dumps(
                    self.research_manifest(
                        ["research_001"],
                        hashlib.sha256(raw_dataset).hexdigest(),
                    )
                )
            )
            stdout = StringIO()
            stderr = StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = dataset_validation_main(
                    [str(dataset_path), "--research-manifest", str(manifest_path)]
                )

        self.assertEqual(exit_code, 0, stderr.getvalue())
        self.assertIn("documented: 1", stdout.getvalue())
        self.assertIn(
            "validation errors: missing=0, invalid=0, split=0, "
            "duplicate IDs=0, manifest=0",
            stdout.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()

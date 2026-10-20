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
    validate_curation_draft,
    validate_research_dataset,
)
from build_research_dataset_draft import _eligible_counts, _family_proposals


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
    def curation_record(problem_id: str, family: str, split: str) -> dict:
        pending_review = {
            "status": "pending",
            "reviewer_provenance": None,
            "review_notes": None,
        }
        return {
            **DatasetValidationTests.legacy_problem(problem_id),
            "curation": {
                "source_url": None,
                "source_citation": None,
                "source_status": "pending",
                "source_license": None,
                "source_license_verification_status": "pending",
                "problem_family": family,
                "family_review_status": "needs_review",
                "family_review_note": None,
                "split": split,
                "split_status": "pending",
                "semantic_fidelity": {
                    "label": None,
                    "review_status": "pending",
                    "reviewer_provenance": None,
                    "evidence": None,
                },
                "theorem_statement_review": dict(pending_review),
                "assumption_mismatch_review": dict(pending_review),
                "self_containment_review": dict(pending_review),
                "duplicate_review": {
                    "candidate_group": None,
                    "related_ids": [],
                    "status": "pending",
                    "notes": None,
                },
            },
        }

    @staticmethod
    def complete_curation_review(record: dict) -> None:
        curation = record["curation"]
        curation.update(
            {
                "source_status": "verified",
                "source_url": "https://example.org/source",
                "source_license_verification_status": "verified",
                "source_license": "CC0",
                "family_review_status": "verified",
                "family_review_note": "Reviewed theorem-family grouping.",
                "family_reviewer_provenance": "reviewer:test",
                "split_status": "verified",
                "split_review_note": "Reviewed family-aware split assignment.",
                "split_reviewer_provenance": "reviewer:test",
            }
        )
        curation["semantic_fidelity"].update(
            {
                "review_status": "verified",
                "label": "uncertain",
                "reviewer_provenance": "reviewer:test",
                "evidence": "The reviewed pair remains semantically uncertain.",
            }
        )
        for review_field in (
            "theorem_statement_review",
            "assumption_mismatch_review",
            "self_containment_review",
        ):
            curation[review_field].update(
                {
                    "status": "verified",
                    "reviewer_provenance": "reviewer:test",
                    "review_notes": "Reviewed for the regression test.",
                }
            )
        curation["duplicate_review"].update(
            {
                "status": "verified",
                "reviewer_provenance": "reviewer:test",
                "notes": "Reviewed for the regression test.",
            }
        )

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

    def test_pending_curation_draft_metadata_is_valid_but_not_complete(self) -> None:
        record = self.curation_record("draft_001", "family_one", "development")

        report = validate_curation_draft([record])

        self.assertTrue(report.is_valid, report.errors)
        self.assertEqual(report.duplicate_candidate_groups, ())
        self.assertEqual(record["curation"]["semantic_fidelity"]["label"], None)
        self.assertEqual(record["curation"]["source_license"], None)
        self.assertEqual(report.eligible_problem_ids, ())

    def test_builder_eligibility_counts_match_validator_for_eligible_record(self) -> None:
        records = [
            self.curation_record("eligible_dev", "family_dev", "development"),
            self.curation_record("eligible_test", "family_test", "test"),
        ]
        records[0]["nl_statement"] = "A distinct development theorem."
        records[1]["nl_statement"] = "A distinct test theorem."
        for record in records:
            self.complete_curation_review(record)

        report = validate_curation_draft(records)
        counts, split_counts = _eligible_counts(records)
        expected_split_counts = {
            split: sum(
                record["id"] in report.eligible_problem_ids
                and record["curation"]["split"] == split
                for record in records
            )
            for split in ("development", "test")
        }

        self.assertEqual(counts, len(report.eligible_problem_ids))
        self.assertEqual(split_counts, expected_split_counts)
        self.assertEqual(counts, 2)
        self.assertEqual(split_counts, {"development": 1, "test": 1})

    def test_builder_eligibility_counts_exclude_unresolved_duplicates_and_incomplete_evidence(
        self,
    ) -> None:
        duplicate_a = self.curation_record(
            "unresolved_a", "duplicate_family", "test"
        )
        duplicate_b = self.curation_record(
            "unresolved_b", "duplicate_family", "test"
        )
        incomplete = self.curation_record(
            "incomplete", "incomplete_family", "development"
        )
        duplicate_b["nl_statement"] = duplicate_a["nl_statement"]
        incomplete["nl_statement"] = "A separate theorem with incomplete review."
        for record in (duplicate_a, duplicate_b, incomplete):
            self.complete_curation_review(record)
        for record, related_id in (
            (duplicate_a, "unresolved_b"),
            (duplicate_b, "unresolved_a"),
        ):
            record["curation"]["duplicate_review"].update(
                {
                    "status": "needs_review",
                    "reviewer_provenance": None,
                    "candidate_group": "unresolved_english",
                    "related_ids": [related_id],
                }
            )
        del incomplete["curation"]["split_reviewer_provenance"]

        report = validate_curation_draft([duplicate_a, duplicate_b, incomplete])
        counts, split_counts = _eligible_counts(
            [duplicate_a, duplicate_b, incomplete]
        )

        self.assertFalse(report.is_valid)
        self.assertEqual(report.eligible_problem_ids, ())
        self.assertEqual(counts, len(report.eligible_problem_ids))
        self.assertEqual(split_counts, {"development": 0, "test": 0})

    def test_completed_reviews_with_documented_evidence_are_eligible(self) -> None:
        record = self.curation_record("reviewed", "family_one", "development")
        self.complete_curation_review(record)

        report = validate_curation_draft([record])

        self.assertTrue(report.is_valid, report.errors)
        self.assertEqual(report.eligible_problem_ids, ("reviewed",))

    def test_family_is_ineligible_until_every_member_family_review_is_complete(
        self,
    ) -> None:
        reviewed = self.curation_record(
            "reviewed_member", "shared_family", "development"
        )
        pending = self.curation_record(
            "pending_member", "shared_family", "development"
        )
        reviewed["nl_statement"] = "A reviewed family theorem."
        pending["nl_statement"] = "A different family theorem."
        self.complete_curation_review(reviewed)

        report = validate_curation_draft([reviewed, pending])

        self.assertTrue(report.is_valid, report.errors)
        self.assertEqual(report.eligible_problem_ids, ())

    def test_consistently_reviewed_family_members_remain_eligible(self) -> None:
        first = self.curation_record("family_first", "shared_family", "test")
        second = self.curation_record("family_second", "shared_family", "test")
        first["nl_statement"] = "The first theorem in this family."
        second["nl_statement"] = "The second theorem in this family."
        self.complete_curation_review(first)
        self.complete_curation_review(second)

        report = validate_curation_draft([first, second])

        self.assertTrue(report.is_valid, report.errors)
        self.assertEqual(
            report.eligible_problem_ids, ("family_first", "family_second")
        )

    def test_builder_emits_one_deterministic_proposal_per_family(self) -> None:
        first = self.curation_record("family_a", "shared_family", "development")
        second = self.curation_record("family_b", "shared_family", "development")
        first["curation"]["family_review_note"] = "First rationale."
        second["curation"]["family_review_note"] = "Second rationale."

        proposals = _family_proposals([first, second])

        self.assertEqual(len(proposals), 1)
        self.assertEqual(
            proposals[0],
            {
                "problem_family": "shared_family",
                "split": "development",
                "member_ids": ["family_a", "family_b"],
                "status": "needs_review",
                "rationale": "First rationale.; Second rationale.",
            },
        )
        self.assertEqual(proposals, _family_proposals([first, second]))

    def test_builder_rejects_conflicting_splits_for_one_family(self) -> None:
        development = self.curation_record(
            "family_dev", "shared_family", "development"
        )
        test = self.curation_record("family_test", "shared_family", "test")

        with self.assertRaisesRegex(ValueError, "conflicting proposed splits"):
            _family_proposals([development, test])

    def test_curation_validator_detects_exact_english_duplicate_candidates(self) -> None:
        first = self.curation_record("duplicate_001", "same_family", "development")
        second = self.curation_record("duplicate_002", "same_family", "development")
        second["expected_lean_statement"] = "theorem renamed : True"
        for record, related_id in (
            (first, "duplicate_002"),
            (second, "duplicate_001"),
        ):
            record["curation"]["duplicate_review"]["status"] = "needs_review"
            record["curation"]["duplicate_review"].update(
                {
                    "candidate_group": "same_english",
                    "related_ids": [related_id],
                }
            )

        report = validate_curation_draft([first, second])

        self.assertTrue(report.is_valid, report.errors)
        self.assertEqual(
            report.duplicate_candidate_groups,
            (("duplicate_001", "duplicate_002"),),
        )

    def test_curation_validator_rejects_family_split_leakage(self) -> None:
        development = self.curation_record(
            "family_dev", "shared_family", "development"
        )
        test = self.curation_record("family_test", "shared_family", "test")

        report = validate_curation_draft([development, test])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any("family 'shared_family' is split across" in error for error in report.errors)
        )

    def test_curation_validator_rejects_invalid_status_and_fidelity_label(self) -> None:
        record = self.curation_record("invalid_review", "family_one", "development")
        record["curation"]["source_status"] = "guessed"
        record["curation"]["semantic_fidelity"]["label"] = "probably faithful"
        record["curation"]["self_containment_review"]["status"] = "done"

        report = validate_curation_draft([record])

        self.assertFalse(report.is_valid)
        self.assertTrue(any("source_status must be one of" in error for error in report.errors))
        self.assertTrue(any("semantic_fidelity.label is invalid" in error for error in report.errors))
        self.assertTrue(
            any("self_containment_review.status is invalid" in error
                for error in report.errors)
        )

    def test_curation_validator_rejects_unsupported_split_label(self) -> None:
        record = self.curation_record("bad_split", "family_one", "development")
        record["curation"]["split"] = "held_out"

        report = validate_curation_draft([record])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any("curation.split must be development or test" in error
                for error in report.errors)
        )

    def test_verified_fidelity_requires_label_and_reviewer_provenance(self) -> None:
        record = self.curation_record("unsubstantiated", "family_one", "development")
        record["curation"]["semantic_fidelity"].update(
            {"review_status": "verified", "label": "faithful"}
        )

        report = validate_curation_draft([record])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any("requires reviewer provenance" in error for error in report.errors)
        )

    def test_pending_fidelity_rejects_non_null_label(self) -> None:
        record = self.curation_record("pending_with_label", "family_one", "development")
        record["curation"]["semantic_fidelity"]["label"] = "uncertain"

        report = validate_curation_draft([record])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any("pending semantic fidelity must have a null label" in error
                for error in report.errors)
        )
        self.assertEqual(report.eligible_problem_ids, ())

    def test_verified_source_and_license_require_evidence_values(self) -> None:
        record = self.curation_record("no_evidence", "family_one", "development")
        record["curation"].update(
            {
                "source_status": "verified",
                "source_license_verification_status": "verified",
            }
        )

        report = validate_curation_draft([record])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any("verified source status requires a source URL or citation" in error
                for error in report.errors)
        )
        self.assertTrue(
            any("verified license status requires source_license" in error
                for error in report.errors)
        )

    def test_curation_validator_requires_explicit_nullable_metadata_fields(self) -> None:
        record = self.curation_record("missing_metadata", "family_one", "development")
        del record["curation"]["source_url"]
        del record["curation"]["semantic_fidelity"]["reviewer_provenance"]

        report = validate_curation_draft([record])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any("missing required curation field 'source_url'" in error
                for error in report.errors)
        )
        self.assertTrue(
            any("missing curation.semantic_fidelity.reviewer_provenance" in error
                for error in report.errors)
        )

    def test_curation_cli_uses_only_local_json_validation(self) -> None:
        record = self.curation_record("cli_draft", "family_one", "development")
        with TemporaryDirectory() as directory:
            dataset_path = Path(directory) / "draft.json"
            dataset_path.write_text(json.dumps([record]), encoding="utf-8")
            stdout = StringIO()
            stderr = StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = dataset_validation_main(
                    [str(dataset_path), "--validate-curation-draft"]
                )

        self.assertEqual(exit_code, 0, stderr.getvalue())
        self.assertIn("Records: 1; duplicate candidate groups: 0", stdout.getvalue())

    def test_verified_duplicate_group_counts_at_most_one_eligible_record(self) -> None:
        records = [
            self.curation_record("duplicate_b", "shared", "development"),
            self.curation_record("duplicate_a", "shared", "development"),
        ]
        for record, related_id in (
            (records[0], "duplicate_a"),
            (records[1], "duplicate_b"),
        ):
            self.complete_curation_review(record)
            record["curation"]["duplicate_review"].update(
                {
                    "candidate_group": "same_english",
                    "related_ids": [related_id],
                }
            )

        report = validate_curation_draft(records)

        self.assertTrue(report.is_valid, report.errors)
        self.assertEqual(report.eligible_problem_ids, ("duplicate_a",))

    def test_unresolved_exact_duplicate_group_has_no_eligible_member(self) -> None:
        records = [
            self.curation_record("unresolved_a", "shared", "development"),
            self.curation_record("unresolved_b", "shared", "development"),
        ]
        for record, related_id in (
            (records[0], "unresolved_b"),
            (records[1], "unresolved_a"),
        ):
            self.complete_curation_review(record)
            record["curation"]["duplicate_review"].update(
                {
                    "status": "needs_review",
                    "reviewer_provenance": None,
                    "candidate_group": "unresolved_pair",
                    "related_ids": [related_id],
                }
            )

        report = validate_curation_draft(records)

        self.assertTrue(report.is_valid, report.errors)
        self.assertEqual(report.eligible_problem_ids, ())

    def test_exact_duplicates_require_consistent_group_metadata(self) -> None:
        first = self.curation_record("group_a", "shared", "development")
        second = self.curation_record("group_b", "shared", "development")
        first["curation"]["duplicate_review"].update(
            {"candidate_group": "group_one", "related_ids": ["group_b"]}
        )
        second["curation"]["duplicate_review"].update(
            {"candidate_group": "group_two", "related_ids": ["group_a"]}
        )

        report = validate_curation_draft([first, second])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any("must share one duplicate_review.candidate_group" in error
                for error in report.errors)
        )
        self.assertEqual(report.eligible_problem_ids, ())

    def test_exact_duplicates_without_group_metadata_are_invalid(self) -> None:
        first = self.curation_record("no_group_a", "shared", "development")
        second = self.curation_record("no_group_b", "shared", "development")

        report = validate_curation_draft([first, second])

        self.assertFalse(report.is_valid)
        self.assertTrue(
            any("requires a non-empty duplicate_review.candidate_group" in error
                for error in report.errors)
        )
        self.assertEqual(report.eligible_problem_ids, ())

    def test_statuses_alone_do_not_make_record_eligible(self) -> None:
        record = self.curation_record("status_only", "family_one", "development")
        curation = record["curation"]
        curation.update(
            {
                "source_status": "verified",
                "source_url": "https://example.org/source",
                "source_license_verification_status": "verified",
                "source_license": "CC0",
                "family_review_status": "verified",
                "split_status": "verified",
            }
        )
        curation["semantic_fidelity"].update(
            {"review_status": "verified", "label": "faithful"}
        )
        for field in (
            "theorem_statement_review",
            "assumption_mismatch_review",
            "self_containment_review",
        ):
            curation[field]["status"] = "verified"
        curation["duplicate_review"]["status"] = "verified"

        report = validate_curation_draft([record])

        self.assertFalse(report.is_valid)
        self.assertEqual(report.eligible_problem_ids, ())
        self.assertTrue(
            any("family_reviewer_provenance" in error for error in report.errors)
        )
        self.assertTrue(
            any("split_reviewer_provenance" in error for error in report.errors)
        )
        self.assertTrue(
            any("requires evidence" in error for error in report.errors)
        )

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

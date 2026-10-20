"""Validation helpers for NL2Lean problem datasets.

This module is intentionally separate from the experiment pipeline so legacy
inputs remain usable until a dataset has been reviewed and documented.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REQUIRED_FIELDS = (
    "id",
    "nl_statement",
    "category",
    "difficulty",
    "expected_lean_statement",
)
ALLOWED_SPLITS = frozenset({"development", "test"})
PROVENANCE_FIELDS = (
    "source_citation",
    "source_url",
    "license",
    "reference_lean_statement_provenance",
)
CURATION_STATUSES = frozenset(
    {"pending", "verified", "rejected", "needs_review"}
)
SEMANTIC_FIDELITY_LABELS = frozenset(
    {"faithful", "not faithful", "uncertain"}
)


@dataclass(frozen=True)
class ProblemProvenance:
    problem_id: str
    status: str
    missing_fields: tuple[str, ...]
    invalid_fields: tuple[str, ...]
    split: str | None
    problem_family: str | None = None


@dataclass(frozen=True)
class DatasetValidationReport:
    errors: tuple[str, ...]
    problems: tuple[ProblemProvenance, ...]
    missing_errors: tuple[str, ...] = ()
    invalid_errors: tuple[str, ...] = ()
    split_errors: tuple[str, ...] = ()
    duplicate_errors: tuple[str, ...] = ()
    manifest_errors: tuple[str, ...] = ()
    dataset_version: str | None = None

    @property
    def is_valid(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class CurationDraftValidationReport:
    errors: tuple[str, ...]
    duplicate_candidate_groups: tuple[tuple[str, ...], ...]
    eligible_problem_ids: tuple[str, ...] = ()

    @property
    def is_valid(self) -> bool:
        return not self.errors


def _valid_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_source_url(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    url = value.strip()
    if any(character.isspace() for character in url):
        return False
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
            and parsed.hostname is not None
            and (parsed.port is None or 0 < parsed.port <= 65535)
        )
    except ValueError:
        return False


def _duplicate_candidate_key(record: dict[str, Any]) -> str | None:
    statement = record.get("nl_statement")
    if not _valid_text(statement):
        return None
    normalized = unicodedata.normalize("NFKC", statement).casefold()
    normalized = re.sub(r"[^\w]+", " ", normalized, flags=re.UNICODE)
    return " ".join(normalized.split())


def validate_curation_draft(value: object) -> CurationDraftValidationReport:
    """Validate research curation metadata without changing legacy validation."""
    base = validate_dataset(value)
    errors = list(base.errors)
    if not isinstance(value, list):
        return CurationDraftValidationReport(tuple(errors), ())

    family_splits: dict[str, tuple[str, str]] = {}
    family_problem_ids: dict[str, list[str]] = {}
    split_inconsistent_families: set[str] = set()
    records_by_duplicate_key: dict[str, list[dict[str, Any]]] = {}
    eligible_by_id: dict[str, bool] = {}
    status_fields = (
        "source_status",
        "source_license_verification_status",
        "family_review_status",
        "split_status",
    )

    for index, record in enumerate(value, start=1):
        if not isinstance(record, dict):
            continue
        problem_id = record.get("id")
        normalized_id = (
            problem_id.strip() if isinstance(problem_id, str) else ""
        )
        label = (
            f"problem {problem_id!r}"
            if isinstance(problem_id, str) and problem_id
            else f"record {index}"
        )
        record_error_count = len(errors)
        key = _duplicate_candidate_key(record)
        if key:
            records_by_duplicate_key.setdefault(key, []).append(record)

        curation = record.get("curation")
        if not isinstance(curation, dict):
            errors.append(f"{label}: missing required object 'curation'.")
            if normalized_id:
                eligible_by_id[normalized_id] = False
            continue

        required_curation_fields = (
            "source_url",
            "source_citation",
            "source_status",
            "source_license",
            "source_license_verification_status",
            "problem_family",
            "family_review_status",
            "family_review_note",
            "split",
            "split_status",
            "semantic_fidelity",
            "theorem_statement_review",
            "assumption_mismatch_review",
            "self_containment_review",
            "duplicate_review",
        )
        for field in required_curation_fields:
            if field not in curation:
                errors.append(f"{label}: missing required curation field {field!r}.")

        for field in status_fields:
            status = curation.get(field)
            if not isinstance(status, str) or status not in CURATION_STATUSES:
                errors.append(
                    f"{label}: curation.{field} must be one of "
                    f"{', '.join(sorted(CURATION_STATUSES))}."
                )

        for field in ("source_url", "source_citation", "source_license"):
            source_value = curation.get(field)
            if source_value is not None and not _valid_text(source_value):
                errors.append(
                    f"{label}: curation.{field} must be non-empty text or null."
                )
        source_url = curation.get("source_url")
        if source_url is not None and not _valid_source_url(source_url):
            errors.append(
                f"{label}: curation.source_url must be an absolute HTTP(S) URL."
            )
        if (
            curation.get("source_status") == "verified"
            and not (curation.get("source_url") or curation.get("source_citation"))
        ):
            errors.append(
                f"{label}: verified source status requires a source URL or citation."
            )
        if (
            curation.get("source_license_verification_status") == "verified"
            and not _valid_text(curation.get("source_license"))
        ):
            errors.append(
                f"{label}: verified license status requires source_license."
            )
        family_review_status = curation.get("family_review_status")
        if family_review_status == "verified":
            if not _valid_text(curation.get("family_review_note")):
                errors.append(
                    f"{label}: verified family review requires family_review_note."
                )
            if not _valid_text(curation.get("family_reviewer_provenance")):
                errors.append(
                    f"{label}: verified family review requires "
                    "family_reviewer_provenance."
                )
        split_review_status = curation.get("split_status")
        if split_review_status == "verified":
            if not _valid_text(curation.get("split_review_note")):
                errors.append(
                    f"{label}: verified split review requires split_review_note."
                )
            if not _valid_text(curation.get("split_reviewer_provenance")):
                errors.append(
                    f"{label}: verified split review requires "
                    "split_reviewer_provenance."
                )

        family = curation.get("problem_family")
        split = curation.get("split")
        if not _valid_text(family):
            errors.append(f"{label}: curation.problem_family must be non-empty text.")
        if not isinstance(split, str) or split not in ALLOWED_SPLITS:
            errors.append(f"{label}: curation.split must be development or test.")
        elif _valid_text(family):
            if normalized_id:
                family_problem_ids.setdefault(family, []).append(normalized_id)
            previous = family_splits.get(family)
            if previous is not None and previous[0] != split:
                split_inconsistent_families.add(family)
                errors.append(
                    f"{label}: family {family!r} is split across "
                    f"{previous[0]!r} and {split!r}."
                )
            else:
                family_splits[family] = (split, label)

        fidelity = curation.get("semantic_fidelity")
        if not isinstance(fidelity, dict):
            errors.append(f"{label}: missing object 'curation.semantic_fidelity'.")
        else:
            fidelity_status = fidelity.get("review_status")
            fidelity_label = fidelity.get("label")
            for field in ("label", "review_status", "reviewer_provenance", "evidence"):
                if field not in fidelity:
                    errors.append(
                        f"{label}: missing curation.semantic_fidelity.{field}."
                    )
            if (
                not isinstance(fidelity_status, str)
                or fidelity_status not in CURATION_STATUSES
            ):
                errors.append(
                    f"{label}: semantic_fidelity.review_status is invalid."
                )
            if (
                fidelity_label is not None
                and (
                    not isinstance(fidelity_label, str)
                    or fidelity_label not in SEMANTIC_FIDELITY_LABELS
                )
            ):
                errors.append(f"{label}: semantic_fidelity.label is invalid.")
            if fidelity_status == "pending" and fidelity_label is not None:
                errors.append(
                    f"{label}: pending semantic fidelity must have a null label."
                )
            if fidelity_status == "verified":
                if (
                    not isinstance(fidelity_label, str)
                    or fidelity_label not in SEMANTIC_FIDELITY_LABELS
                ):
                    errors.append(
                        f"{label}: verified semantic fidelity requires an allowed label."
                    )
                if not _valid_text(fidelity.get("reviewer_provenance")):
                    errors.append(
                        f"{label}: verified semantic fidelity requires reviewer provenance."
                    )
                if not _valid_text(fidelity.get("evidence")):
                    errors.append(
                        f"{label}: verified semantic fidelity requires evidence."
                    )

        for review_field in (
            "theorem_statement_review",
            "assumption_mismatch_review",
            "self_containment_review",
        ):
            review = curation.get(review_field)
            if not isinstance(review, dict):
                errors.append(f"{label}: missing object 'curation.{review_field}'.")
                continue
            status = review.get("status")
            if not isinstance(status, str) or status not in CURATION_STATUSES:
                errors.append(f"{label}: curation.{review_field}.status is invalid.")
            for field in ("reviewer_provenance", "review_notes"):
                if field not in review:
                    errors.append(
                        f"{label}: missing curation.{review_field}.{field}."
                    )
            if status == "verified" and not _valid_text(
                review.get("reviewer_provenance")
            ):
                errors.append(
                    f"{label}: verified {review_field} requires reviewer provenance."
                )
            if status == "verified" and not _valid_text(review.get("review_notes")):
                errors.append(
                    f"{label}: verified {review_field} requires review_notes evidence."
                )

        duplicate_review = curation.get("duplicate_review")
        if not isinstance(duplicate_review, dict):
            errors.append(f"{label}: missing object 'curation.duplicate_review'.")
        elif (
            not isinstance(duplicate_review.get("status"), str)
            or duplicate_review.get("status") not in CURATION_STATUSES
        ):
            errors.append(f"{label}: curation.duplicate_review.status is invalid.")
        else:
            if duplicate_review.get("status") == "verified":
                if not _valid_text(duplicate_review.get("reviewer_provenance")):
                    errors.append(
                        f"{label}: verified duplicate review requires reviewer provenance."
                    )
                if not _valid_text(duplicate_review.get("notes")):
                    errors.append(
                        f"{label}: verified duplicate review requires notes evidence."
                    )
            if "candidate_group" not in duplicate_review:
                errors.append(
                    f"{label}: missing curation.duplicate_review.candidate_group."
                )
            elif duplicate_review["candidate_group"] is not None and not _valid_text(
                duplicate_review["candidate_group"]
            ):
                errors.append(
                    f"{label}: curation.duplicate_review.candidate_group "
                    "must be non-empty text or null."
                )
            if not isinstance(duplicate_review.get("related_ids"), list) or not all(
                _valid_text(related_id)
                for related_id in duplicate_review.get("related_ids", [])
            ):
                errors.append(
                    f"{label}: curation.duplicate_review.related_ids must be "
                    "a list of non-empty IDs."
                )
            if "notes" not in duplicate_review:
                errors.append(f"{label}: missing curation.duplicate_review.notes.")

        eligible_by_id[normalized_id] = (
            _curation_has_eligibility_evidence(curation)
            and len(errors) == record_error_count
            and not base.errors
        )

    duplicate_groups: list[tuple[str, ...]] = []
    duplicate_group_keys: dict[str, str] = {}
    duplicate_group_members: dict[str, set[str]] = {}
    for duplicate_key, records in records_by_duplicate_key.items():
        if len(records) < 2:
            continue
        ids = tuple(
            record["id"].strip()
            for record in records
            if isinstance(record.get("id"), str)
        )
        duplicate_groups.append(ids)
        expected_related_ids = set(ids)
        group_ids: set[str] = set()
        group_statuses: list[str] = []
        metadata_valid = True
        for record in records:
            record_id = record.get("id")
            curation = record.get("curation")
            review = (
                curation.get("duplicate_review")
                if isinstance(curation, dict)
                else None
            )
            if (
                not isinstance(review, dict)
                or review.get("status") not in {"needs_review", "verified", "rejected"}
            ):
                errors.append(
                    f"problem {record.get('id')!r}: exact duplicate candidate "
                    "requires duplicate_review status needs_review, verified, or rejected."
                )
            if not isinstance(review, dict):
                if isinstance(record_id, str):
                    eligible_by_id[record_id.strip()] = False
                continue

            candidate_group = review.get("candidate_group")
            related_ids = review.get("related_ids")
            if not _valid_text(candidate_group):
                metadata_valid = False
                errors.append(
                    f"problem {record_id!r}: exact duplicate candidate requires "
                    "a non-empty duplicate_review.candidate_group."
                )
            else:
                group_ids.add(candidate_group.strip())
            if not isinstance(related_ids, list) or {
                related_id.strip()
                for related_id in related_ids
                if isinstance(related_id, str)
            } != expected_related_ids - {
                record_id.strip() if isinstance(record_id, str) else ""
            }:
                metadata_valid = False
                errors.append(
                    f"problem {record_id!r}: duplicate_review.related_ids must "
                    "list every other exact-English duplicate candidate."
                )
            group_status = review.get("status")
            if isinstance(group_status, str):
                group_statuses.append(group_status)
            if isinstance(record_id, str) and group_status != "verified":
                eligible_by_id[record_id.strip()] = False
        if len(group_ids) > 1:
            metadata_valid = False
            errors.append(
                "exact duplicate candidates must share one duplicate_review.candidate_group."
            )
        if len(group_ids) == 1:
            candidate_group = next(iter(group_ids))
            previous_key = duplicate_group_keys.get(candidate_group)
            if previous_key is not None and previous_key != duplicate_key:
                metadata_valid = False
                errors.append(
                    f"duplicate_review.candidate_group {candidate_group!r} "
                    "cannot identify multiple English statements."
                )
                for problem_id in duplicate_group_members[candidate_group]:
                    eligible_by_id[problem_id] = False
            duplicate_group_keys[candidate_group] = duplicate_key
            duplicate_group_members.setdefault(candidate_group, set()).update(
                expected_related_ids
            )
        if group_statuses and any(status != "verified" for status in group_statuses):
            for record_id in ids:
                eligible_by_id[record_id] = False
        elif not metadata_valid:
            for record_id in ids:
                eligible_by_id[record_id] = False
        elif len(ids) > 1:
            for record_id in sorted(ids)[1:]:
                eligible_by_id[record_id] = False

    for family in split_inconsistent_families:
        for problem_id in family_problem_ids.get(family, []):
            eligible_by_id[problem_id] = False

    return CurationDraftValidationReport(
        errors=tuple(errors),
        duplicate_candidate_groups=tuple(sorted(duplicate_groups)),
        eligible_problem_ids=tuple(
            sorted(problem_id for problem_id, is_eligible in eligible_by_id.items()
                   if problem_id and is_eligible)
        ),
    )


def _curation_has_eligibility_evidence(curation: dict[str, Any]) -> bool:
    """Return whether recorded curation fields support counting this record."""
    fidelity = curation.get("semantic_fidelity")
    duplicate_review = curation.get("duplicate_review")
    if not isinstance(fidelity, dict) or not isinstance(duplicate_review, dict):
        return False
    if not (
        curation.get("source_status") == "verified"
        and (
            _valid_text(curation.get("source_url"))
            or _valid_text(curation.get("source_citation"))
        )
        and curation.get("source_license_verification_status") == "verified"
        and _valid_text(curation.get("source_license"))
        and curation.get("family_review_status") == "verified"
        and _valid_text(curation.get("problem_family"))
        and _valid_text(curation.get("family_review_note"))
        and _valid_text(curation.get("family_reviewer_provenance"))
        and curation.get("split_status") == "verified"
        and _valid_text(curation.get("split_review_note"))
        and _valid_text(curation.get("split_reviewer_provenance"))
        and fidelity.get("review_status") == "verified"
        and fidelity.get("label") in SEMANTIC_FIDELITY_LABELS
        and _valid_text(fidelity.get("reviewer_provenance"))
        and _valid_text(fidelity.get("evidence"))
        and duplicate_review.get("status") == "verified"
        and _valid_text(duplicate_review.get("reviewer_provenance"))
        and _valid_text(duplicate_review.get("notes"))
        and isinstance(curation.get("split"), str)
        and curation.get("split") in ALLOWED_SPLITS
    ):
        return False
    return all(
        isinstance(review, dict)
        and review.get("status") == "verified"
        and _valid_text(review.get("reviewer_provenance"))
        and _valid_text(review.get("review_notes"))
        for review in (
            curation.get("theorem_statement_review"),
            curation.get("assumption_mismatch_review"),
            curation.get("self_containment_review"),
        )
    )


def validate_dataset(
    value: object, *, require_provenance: bool = False
) -> DatasetValidationReport:
    """Validate a dataset and classify each record's provenance completeness.

    Without ``require_provenance``, absent provenance is reported in the
    returned per-record classification but does not invalidate legacy inputs.
    """
    errors: list[str] = []
    missing_errors: list[str] = []
    invalid_errors: list[str] = []
    split_errors: list[str] = []
    duplicate_errors: list[str] = []

    def add_error(message: str, category: list[str]) -> None:
        errors.append(message)
        category.append(message)

    if not isinstance(value, list):
        message = "dataset: expected a JSON array of problem objects."
        return DatasetValidationReport(
            errors=(message,),
            problems=(),
            invalid_errors=(message,),
        )

    seen_ids: set[str] = set()
    problem_reports: list[ProblemProvenance] = []
    for index, record in enumerate(value, start=1):
        if not isinstance(record, dict):
            add_error(
                f"record {index}: expected a JSON object.",
                invalid_errors,
            )
            continue

        raw_id = record.get("id")
        problem_id = raw_id.strip() if isinstance(raw_id, str) else ""
        label = f"problem {problem_id!r}" if problem_id else f"record {index}"

        for field in REQUIRED_FIELDS:
            if field not in record:
                add_error(
                    f"{label}: missing required field {field!r}.",
                    missing_errors,
                )

        if not _valid_text(raw_id):
            add_error(
                f"{label}: field 'id' must be a non-empty string.",
                invalid_errors,
            )
        elif problem_id in seen_ids:
            add_error(
                f"problem {problem_id!r}: duplicate value for field 'id'.",
                duplicate_errors,
            )
        else:
            seen_ids.add(problem_id)

        for field in ("nl_statement", "category", "expected_lean_statement"):
            if field in record and not _valid_text(record[field]):
                add_error(
                    f"{label}: field {field!r} must be a non-empty string.",
                    invalid_errors,
                )

        if "difficulty" in record:
            difficulty = record["difficulty"]
            if (
                isinstance(difficulty, bool)
                or not isinstance(difficulty, int)
                or not 1 <= difficulty <= 5
            ):
                add_error(
                    f"{label}: field 'difficulty' must be an integer from 1 to 5.",
                    invalid_errors,
                )

        split = record.get("split")
        if "split" in record and (
            not isinstance(split, str) or split not in ALLOWED_SPLITS
        ):
            add_error(
                f"{label}: field 'split' must be one of "
                f"{', '.join(sorted(ALLOWED_SPLITS))}; got {split!r}.",
                split_errors,
            )

        invalid: list[str] = []
        if "source_citation" in record and not _valid_text(record["source_citation"]):
            invalid.append("source_citation")
            add_error(
                f"{label}: field 'source_citation' must be a non-empty string "
                "when supplied.",
                invalid_errors,
            )
        if "source_url" in record and not _valid_source_url(record["source_url"]):
            invalid.append("source_url")
            add_error(
                f"{label}: field 'source_url' must be an absolute HTTP(S) URL "
                "when supplied.",
                invalid_errors,
            )
        if "license" in record and not _valid_text(record["license"]):
            invalid.append("license")
            add_error(
                f"{label}: field 'license' must be a non-empty string when supplied.",
                invalid_errors,
            )
        if (
            "reference_lean_statement_provenance" in record
            and not _valid_text(record["reference_lean_statement_provenance"])
        ):
            invalid.append("reference_lean_statement_provenance")
            add_error(
                f"{label}: field 'reference_lean_statement_provenance' must be a "
                "non-empty string when supplied.",
                invalid_errors,
            )

        missing: list[str] = []
        if "source_citation" not in record and "source_url" not in record:
            missing.append("source_citation or source_url")
        for field in ("license", "reference_lean_statement_provenance"):
            if field not in record:
                missing.append(field)

        supplied_provenance = any(field in record for field in PROVENANCE_FIELDS)
        if invalid:
            status = "invalid_provenance"
        elif not supplied_provenance:
            status = "legacy_missing_provenance"
        elif missing:
            status = "incomplete_provenance"
        else:
            status = "documented"
        problem_reports.append(
            ProblemProvenance(
                problem_id=problem_id or f"record {index}",
                status=status,
                missing_fields=tuple(missing),
                invalid_fields=tuple(invalid),
                split=split if isinstance(split, str) and split in ALLOWED_SPLITS else None,
            )
        )
        if require_provenance:
            for field in missing:
                add_error(
                    f"{label}: missing provenance field {field!r}.",
                    missing_errors,
                )

    return DatasetValidationReport(
        errors=tuple(errors),
        problems=tuple(problem_reports),
        missing_errors=tuple(missing_errors),
        invalid_errors=tuple(invalid_errors),
        split_errors=tuple(split_errors),
        duplicate_errors=tuple(duplicate_errors),
    )


def validate_research_dataset(
    value: object,
    manifest: object,
    dataset_sha256: str,
) -> DatasetValidationReport:
    """Validate a research dataset against its frozen manifest.

    The manifest format is an object with ``dataset_version``, ``expected_ids``,
    and ``dataset_sha256`` fields. The hash must be computed from the exact
    dataset file bytes. Duplicate family identifiers are allowed so related
    variants can be kept as separate records while remaining groupable.
    """
    base = validate_dataset(value, require_provenance=True)
    errors = list(base.errors)
    invalid_errors = list(base.invalid_errors)
    split_errors = list(base.split_errors)
    duplicate_errors = list(base.duplicate_errors)
    manifest_errors: list[str] = []
    problems = list(base.problems)

    def add_manifest_error(message: str) -> None:
        errors.append(message)
        manifest_errors.append(message)

    if isinstance(value, list):
        problem_index = 0
        for index, record in enumerate(value, start=1):
            if not isinstance(record, dict):
                continue
            report = problems[problem_index]
            problem_index += 1
            label = f"problem {report.problem_id!r}"

            family = record.get("problem_family")
            if "problem_family" in record:
                if not isinstance(family, str) or not family.strip():
                    message = (
                        f"{label}: field 'problem_family' must be a non-empty "
                        "string when supplied."
                    )
                    errors.append(message)
                    invalid_errors.append(message)
                else:
                    problems[problem_index - 1] = ProblemProvenance(
                        problem_id=report.problem_id,
                        status=report.status,
                        missing_fields=report.missing_fields,
                        invalid_fields=report.invalid_fields,
                        split=report.split,
                        problem_family=family.strip(),
                    )

            if "split" not in record:
                message = f"{label}: missing required research split field 'split'."
                errors.append(message)
                split_errors.append(message)

    dataset_version: str | None = None
    if not isinstance(manifest, dict):
        add_manifest_error("manifest: expected a JSON object.")
    else:
        raw_version = manifest.get("dataset_version")
        if isinstance(raw_version, str) and raw_version.strip():
            dataset_version = raw_version.strip()
        else:
            add_manifest_error(
                "manifest: field 'dataset_version' must be a non-empty string."
            )

        expected_ids = manifest.get("expected_ids")
        valid_expected_ids: list[str] | None = None
        if not isinstance(expected_ids, list) or any(
            not isinstance(problem_id, str) or not problem_id.strip()
            for problem_id in expected_ids
        ):
            add_manifest_error(
                "manifest: field 'expected_ids' must be an array of non-empty strings."
            )
        else:
            valid_expected_ids = [problem_id.strip() for problem_id in expected_ids]
            if len(valid_expected_ids) != len(set(valid_expected_ids)):
                add_manifest_error(
                    "manifest: field 'expected_ids' contains duplicate IDs."
                )

        declared_hash = manifest.get("dataset_sha256")
        if not isinstance(declared_hash, str) or re.fullmatch(
            r"[0-9a-fA-F]{64}", declared_hash
        ) is None:
            add_manifest_error(
                "manifest: field 'dataset_sha256' must be a 64-character SHA-256 hex digest."
            )
        elif re.fullmatch(r"[0-9a-fA-F]{64}", dataset_sha256) is None:
            add_manifest_error(
                "dataset: supplied SHA-256 must be a 64-character hex digest."
            )
        elif declared_hash.lower() != dataset_sha256.lower():
            add_manifest_error(
                "manifest: dataset_sha256 does not match the dataset file."
            )

        if valid_expected_ids is not None and isinstance(value, list):
            actual_ids = {
                record["id"].strip()
                for record in value
                if isinstance(record, dict) and _valid_text(record.get("id"))
            }
            expected_id_set = set(valid_expected_ids)
            missing_ids = sorted(expected_id_set - actual_ids)
            extra_ids = sorted(actual_ids - expected_id_set)
            if missing_ids:
                add_manifest_error(
                    "manifest: expected IDs missing from dataset: "
                    + ", ".join(missing_ids)
                    + "."
                )
            if extra_ids:
                add_manifest_error(
                    "manifest: unexpected dataset IDs: "
                    + ", ".join(extra_ids)
                    + "."
                )

    return DatasetValidationReport(
        errors=tuple(errors),
        problems=tuple(problems),
        missing_errors=base.missing_errors,
        invalid_errors=tuple(invalid_errors),
        split_errors=tuple(split_errors),
        duplicate_errors=tuple(duplicate_errors),
        manifest_errors=tuple(manifest_errors),
        dataset_version=dataset_version,
    )


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{path}: could not read valid JSON: {error}") from error


def _load_json_with_hash(path: Path) -> tuple[object, str]:
    try:
        raw = path.read_bytes()
        return json.loads(raw), hashlib.sha256(raw).hexdigest()
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{path}: could not read valid JSON: {error}") from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate NL2Lean dataset schema and provenance."
    )
    parser.add_argument("dataset", type=Path, help="path to a JSON problem array")
    parser.add_argument(
        "--require-provenance",
        action="store_true",
        help="treat missing per-problem provenance as validation errors",
    )
    parser.add_argument(
        "--research-manifest",
        type=Path,
        help=(
            "enable strict research validation against a frozen JSON manifest "
            "with dataset_version, expected_ids, and dataset_sha256"
        ),
    )
    parser.add_argument(
        "--validate-curation-draft",
        action="store_true",
        help="validate nested research-curation draft metadata",
    )
    args = parser.parse_args(argv)

    if args.validate_curation_draft and args.research_manifest:
        parser.error("--validate-curation-draft cannot be combined with --research-manifest")

    if args.validate_curation_draft:
        try:
            value = _load_json(args.dataset)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 1
        report = validate_curation_draft(value)
        record_count = len(value) if isinstance(value, list) else 0
        print(
            f"Records: {record_count}; duplicate candidate groups: "
            f"{len(report.duplicate_candidate_groups)}; "
            f"eligible records: {len(report.eligible_problem_ids)}; "
            f"validation errors: {len(report.errors)}"
        )
        for error in report.errors:
            print(f"error: {error}", file=sys.stderr)
        return 0 if report.is_valid else 1
    if args.research_manifest:
        try:
            value, dataset_sha256 = _load_json_with_hash(args.dataset)
            manifest = _load_json(args.research_manifest)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 1
        report = validate_research_dataset(value, manifest, dataset_sha256)
    else:
        try:
            value = _load_json(args.dataset)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 1
        report = validate_dataset(value, require_provenance=args.require_provenance)
    counts = {
        status: sum(problem.status == status for problem in report.problems)
        for status in (
            "documented",
            "incomplete_provenance",
            "invalid_provenance",
            "legacy_missing_provenance",
        )
    }
    unsplit = sum(problem.split is None for problem in report.problems)
    print(
        f"Records: {len(report.problems)}; documented: {counts['documented']}; "
        f"incomplete provenance: {counts['incomplete_provenance']}; "
        f"legacy missing provenance: {counts['legacy_missing_provenance']}; "
        f"without split: {unsplit}; "
        f"validation errors: missing={len(report.missing_errors)}, "
        f"invalid={len(report.invalid_errors)}, "
        f"split={len(report.split_errors)}, "
        f"duplicate IDs={len(report.duplicate_errors)}, "
        f"manifest={len(report.manifest_errors)}"
    )
    if not args.require_provenance and not args.research_manifest:
        for problem in report.problems:
            if problem.missing_fields:
                print(
                    f"warning: problem {problem.problem_id!r}: missing provenance "
                    f"{', '.join(problem.missing_fields)}.",
                    file=sys.stderr,
                )
    for error in report.errors:
        print(f"error: {error}", file=sys.stderr)
    return 0 if report.is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())

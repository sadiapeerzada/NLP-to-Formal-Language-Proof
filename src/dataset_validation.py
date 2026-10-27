"""Validation helpers for NL2Lean problem datasets.

This module is intentionally separate from the experiment pipeline so legacy
inputs remain usable until a dataset has been reviewed and documented.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import date
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
RESEARCH_CATEGORIES = frozenset(
    {
        "arithmetic_identity",
        "divisibility",
        "modular_arithmetic",
        "induction",
        "inequality",
    }
)
MINIMUM_TEST_RECORDS = 60
MINIMUM_DEVELOPMENT_RECORDS = 15
MAXIMUM_DEVELOPMENT_RECORDS = 20
REQUIRED_LEAN_TOOLCHAIN = "leanprover/lean4:v4.32.0"
REQUIRED_MATHLIB_REVISION = "81a5d257c8e410db227a6665ed08f64fea08e997"
REQUIRED_INDEPENDENT_REVIEW_TYPES = frozenset(
    {
        "semantic_fidelity",
        "theorem_statement",
        "assumption_mismatch",
        "self_containment",
        "problem_family",
        "split_assignment",
        "duplicate_review",
    }
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
    candidate_split_counts: dict[str, int] | None = None
    eligible_split_counts: dict[str, int] | None = None
    review_warnings: tuple[str, ...] = ()

    @property
    def is_valid(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class FrozenCurationValidationReport:
    errors: tuple[str, ...]
    candidate_split_counts: dict[str, int]
    eligible_split_counts: dict[str, int]
    dataset_sha256: str
    development_dataset_sha256: str | None = None

    @property
    def is_valid(self) -> bool:
        return not self.errors


def _valid_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_iso_date(value: object) -> bool:
    if not _valid_text(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


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


def _review_record_errors(curation: dict[str, Any], label: str) -> list[str]:
    reviews = curation.get("review_records")
    if not isinstance(reviews, list):
        return [f"{label}: curation.review_records must be an array."]
    independent_types: set[str] = set()
    errors: list[str] = []
    for index, review in enumerate(reviews, start=1):
        review_label = f"{label}: review_records[{index}]"
        if not isinstance(review, dict):
            errors.append(f"{review_label} must be an object.")
            continue
        review_type = review.get("review_type")
        reviewer_kind = review.get("reviewer_kind")
        if not _valid_text(review_type):
            errors.append(f"{review_label}.review_type must be non-empty text.")
        if not isinstance(reviewer_kind, str) or reviewer_kind not in {
            "author_self_review",
            "assisted_review",
            "independent_human_review",
        }:
            errors.append(
                f"{review_label}.reviewer_kind must distinguish author_self_review, "
                "assisted_review, or independent_human_review."
            )
        for field in ("reviewer_id", "reviewed_on", "evidence"):
            if not _valid_text(review.get(field)):
                errors.append(f"{review_label}.{field} must be non-empty text.")
        if not _valid_iso_date(review.get("reviewed_on")):
            errors.append(f"{review_label}.reviewed_on must be an ISO date.")
        if reviewer_kind == "independent_human_review" and _valid_text(review_type):
            independent_types.add(review_type)
    missing = sorted(REQUIRED_INDEPENDENT_REVIEW_TYPES - independent_types)
    if missing:
        errors.append(
            f"{label}: missing independent human review records for "
            + ", ".join(missing)
            + "."
        )
    return errors


def _theorem_verification_is_valid(record: dict[str, Any]) -> bool:
    curation = record.get("curation")
    if not isinstance(curation, dict):
        return False
    verification = curation.get("theorem_verification")
    theorem_statement = record.get("expected_lean_statement")
    return (
        isinstance(verification, dict)
        and verification.get("status") == "verified"
        and verification.get("success") is True
        # Statement elaboration with a placeholder is not proof evidence.
        # Older strict-proof records omit scope; retain that legacy schema,
        # but never accept a scope explicitly limited to type elaboration.
        and (
            verification.get("verification_scope") is None
            or verification.get("verification_scope") == "strict_proof"
        )
        and verification.get("lean_toolchain") == REQUIRED_LEAN_TOOLCHAIN
        and verification.get("mathlib_revision") == REQUIRED_MATHLIB_REVISION
        and _valid_text(verification.get("command"))
        and re.fullmatch(
            r"[0-9a-fA-F]{64}",
            verification.get("theorem_sha256", "")
            if isinstance(verification.get("theorem_sha256"), str)
            else "",
        )
        is not None
        and isinstance(theorem_statement, str)
        and verification.get("theorem_sha256")
        == hashlib.sha256(theorem_statement.encode("utf-8")).hexdigest()
        and _valid_text(verification.get("evidence"))
    )


def _likely_duplicate_pairs(
    records: list[dict[str, Any]], threshold: float = 0.82
) -> tuple[tuple[str, str], ...]:
    pairs: set[tuple[str, str]] = set()
    for index, first in enumerate(records):
        first_id = first.get("id")
        if not _valid_text(first_id):
            continue
        for second in records[index + 1 :]:
            second_id = second.get("id")
            if not _valid_text(second_id) or first_id.strip() == second_id.strip():
                continue
            comparisons = (
                (first.get("nl_statement"), second.get("nl_statement")),
                (
                    first.get("expected_lean_statement"),
                    second.get("expected_lean_statement"),
                ),
            )
            for left, right in comparisons:
                if not (_valid_text(left) and _valid_text(right)):
                    continue
                left_key = re.sub(r"\s+", " ", left.strip().casefold())
                right_key = re.sub(r"\s+", " ", right.strip().casefold())
                if left_key == right_key:
                    continue
                similarity = difflib.SequenceMatcher(
                    None, left_key, right_key
                ).ratio()
                if similarity >= threshold:
                    pairs.add(tuple(sorted((first_id.strip(), second_id.strip()))))
                    break
    return tuple(sorted(pairs))


def _likely_duplicate_warnings(
    records: list[dict[str, Any]], threshold: float = 0.82
) -> tuple[str, ...]:
    warnings: list[str] = []
    for first_id, second_id in _likely_duplicate_pairs(records, threshold):
        warnings.append(
            f"Likely statement similarity between {first_id!r} and "
            f"{second_id!r}; human theorem/family duplicate review required."
        )
    return tuple(sorted(set(warnings)))


def validate_curation_draft(value: object) -> CurationDraftValidationReport:
    """Validate research curation metadata without changing legacy validation."""
    base = validate_dataset(value)
    errors = list(base.errors)
    if not isinstance(value, list):
        return CurationDraftValidationReport(
            tuple(errors),
            (),
            candidate_split_counts={"development": 0, "test": 0},
            eligible_split_counts={"development": 0, "test": 0},
        )

    family_splits: dict[str, tuple[str, str]] = {}
    family_problem_ids: dict[str, list[str]] = {}
    family_reviews_complete: dict[str, list[bool]] = {}
    split_inconsistent_families: set[str] = set()
    records_by_duplicate_key: dict[str, list[dict[str, Any]]] = {}
    eligible_by_id: dict[str, bool] = {}
    evidence_warnings: list[str] = []
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

        category = record.get("category")
        if not isinstance(category, str) or category not in RESEARCH_CATEGORIES:
            errors.append(
                f"{label}: category must be one of "
                + ", ".join(sorted(RESEARCH_CATEGORIES))
                + "."
            )
        difficulty = record.get("difficulty")
        if (
            isinstance(difficulty, bool)
            or not isinstance(difficulty, int)
            or not 1 <= difficulty <= 5
        ):
            errors.append(f"{label}: difficulty must be an integer from 1 to 5.")

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
        license_evidence = curation.get("source_license_evidence")
        theorem_statement = record.get("expected_lean_statement")
        source_license_statement_sha256 = (
            license_evidence.get("statement_sha256")
            if isinstance(license_evidence, dict)
            else None
        )
        license_evidence_complete = (
            isinstance(license_evidence, dict)
            and license_evidence.get("status") == "verified"
            and _valid_text(license_evidence.get("evidence_reference"))
            and _valid_iso_date(license_evidence.get("reviewed_on"))
            and isinstance(theorem_statement, str)
            and isinstance(source_license_statement_sha256, str)
            and re.fullmatch(r"[0-9a-fA-F]{64}", source_license_statement_sha256)
            is not None
            and source_license_statement_sha256.lower()
            == hashlib.sha256(theorem_statement.encode("utf-8")).hexdigest()
        )
        if (
            isinstance(license_evidence, dict)
            and license_evidence.get("status") == "verified"
            and not license_evidence_complete
        ):
            errors.append(
                f"{label}: verified source/license evidence must include a valid "
                "statement_sha256 matching the exact expected_lean_statement UTF-8 bytes."
            )
        review_evidence_errors = _review_record_errors(curation, label)
        theorem_verification_complete = _theorem_verification_is_valid(record)
        if not license_evidence_complete:
            evidence_warnings.append(
                f"{label}: source/license evidence is incomplete; record is ineligible."
            )
        if review_evidence_errors:
            evidence_warnings.extend(review_evidence_errors)
        if not theorem_verification_complete:
            evidence_warnings.append(
                f"{label}: successful pinned-environment theorem verification is "
                "missing; record is ineligible."
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
        else:
            if normalized_id:
                family_problem_ids.setdefault(family, []).append(normalized_id)
                family_reviews_complete.setdefault(family, []).append(
                    family_review_status == "verified"
                    and _valid_text(curation.get("family_review_note"))
                    and _valid_text(curation.get("family_reviewer_provenance"))
                    and split_review_status == "verified"
                    and _valid_text(curation.get("split_review_note"))
                    and _valid_text(curation.get("split_reviewer_provenance"))
                    and isinstance(split, str)
                    and split in ALLOWED_SPLITS
                )
            if not isinstance(split, str) or split not in ALLOWED_SPLITS:
                errors.append(f"{label}: curation.split must be development or test.")
            else:
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
            and license_evidence_complete
            and not review_evidence_errors
            and theorem_verification_complete
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
    for family, reviews_complete in family_reviews_complete.items():
        if not all(reviews_complete):
            for problem_id in family_problem_ids[family]:
                eligible_by_id[problem_id] = False

    candidate_split_counts = {
        split: sum(
            isinstance(record, dict)
            and isinstance(record.get("curation"), dict)
            and record["curation"].get("split") == split
            for record in value
        )
        for split in ALLOWED_SPLITS
    }
    eligible_split_counts = {
        split: sum(
            eligible_by_id.get(record_id, False)
            and isinstance(record, dict)
            and isinstance(record.get("curation"), dict)
            and record["curation"].get("split") == split
            for record in value
            for record_id in (
                [record["id"].strip()]
                if isinstance(record, dict) and _valid_text(record.get("id"))
                else [""]
            )
        )
        for split in ALLOWED_SPLITS
    }

    return CurationDraftValidationReport(
        errors=tuple(errors),
        duplicate_candidate_groups=tuple(sorted(duplicate_groups)),
        eligible_problem_ids=tuple(
            sorted(problem_id for problem_id, is_eligible in eligible_by_id.items()
                   if problem_id and is_eligible)
        ),
        candidate_split_counts=candidate_split_counts,
        eligible_split_counts=eligible_split_counts,
        review_warnings=tuple(
            sorted(set(evidence_warnings).union(_likely_duplicate_warnings(value)))
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
        and isinstance(curation.get("source_license_evidence"), dict)
        and curation["source_license_evidence"].get("status") == "verified"
        and _valid_text(
            curation["source_license_evidence"].get("evidence_reference")
        )
        and _valid_text(curation["source_license_evidence"].get("reviewed_on"))
        and isinstance(curation["source_license_evidence"].get("statement_sha256"), str)
        and isinstance(curation.get("theorem_verification"), dict)
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


def validate_frozen_curation(
    test_value: object,
    manifest: object,
    test_dataset_sha256: str,
    *,
    development_value: object | None = None,
    development_dataset_sha256: str | None = None,
) -> FrozenCurationValidationReport:
    """Require an explicitly frozen, independently reviewed research dataset."""
    errors: list[str] = []
    test_report = validate_curation_draft(test_value)
    errors.extend(test_report.errors)
    development_report = validate_curation_draft(development_value)
    errors.extend(development_report.errors)
    combined_records = [
        *(
            development_value
            if isinstance(development_value, list)
            else []
        ),
        *(test_value if isinstance(test_value, list) else []),
    ]
    combined_report = validate_curation_draft(combined_records)
    errors.extend(combined_report.errors)
    candidate_counts = {
        "development": (development_report.candidate_split_counts or {}).get(
            "development", 0
        ),
        "test": (test_report.candidate_split_counts or {}).get("test", 0),
    }
    eligible_counts = combined_report.eligible_split_counts or {
        "development": 0,
        "test": 0,
    }
    if development_value is None or development_dataset_sha256 is None:
        errors.append(
            "a separately supplied development dataset and its exact-byte hash are required."
        )

    for label, value, expected_split in (
        ("development", development_value, "development"),
        ("test", test_value, "test"),
    ):
        if isinstance(value, list):
            for record in value:
                if (
                    isinstance(record, dict)
                    and isinstance(record.get("curation"), dict)
                    and record["curation"].get("split") != expected_split
                ):
                    errors.append(
                        f"{label} dataset contains a record not assigned to "
                        f"{expected_split!r}."
                    )
    if not isinstance(manifest, dict):
        errors.append("freeze manifest must be an object.")
        return FrozenCurationValidationReport(
            tuple(errors),
            candidate_counts,
            eligible_counts,
            test_dataset_sha256,
            development_dataset_sha256,
        )

    if manifest.get("status") != "frozen":
        errors.append("freeze manifest status must be 'frozen'; draft/unfrozen sets are rejected.")
    if manifest.get("freeze_approved") is not True:
        errors.append("freeze manifest must record freeze_approved: true.")
    if not _valid_iso_date(manifest.get("frozen_on")):
        errors.append("freeze manifest frozen_on must be an ISO date.")
    if not _valid_text(manifest.get("freeze_approval_evidence")):
        errors.append("freeze manifest requires freeze_approval_evidence.")
    if not _valid_text(manifest.get("dataset_version")):
        errors.append("freeze manifest dataset_version must be non-empty.")
    dataset_records = {
        "development": (development_value, development_dataset_sha256),
        "test": (test_value, test_dataset_sha256),
    }
    for split, (records, actual_hash) in dataset_records.items():
        section = manifest.get(f"{split}_dataset")
        label = f"{split}_dataset"
        if not isinstance(section, dict):
            errors.append(f"freeze manifest {label} must be an object.")
            continue
        declared_hash = section.get("dataset_sha256")
        if (
            not isinstance(declared_hash, str)
            or re.fullmatch(r"[0-9a-fA-F]{64}", declared_hash) is None
        ):
            errors.append(f"{label}.dataset_sha256 must be a 64-character SHA-256.")
        elif not isinstance(actual_hash, str) or actual_hash.lower() != declared_hash.lower():
            errors.append(f"{label} hash does not match the exact dataset bytes.")
        expected_ids = section.get("expected_ids")
        actual_ids = [
            record["id"].strip()
            for record in records
            if isinstance(records, list)
            and isinstance(record, dict)
            and _valid_text(record.get("id"))
        ] if isinstance(records, list) else []
        if not isinstance(expected_ids, list) or any(
            not _valid_text(problem_id) for problem_id in expected_ids
        ):
            errors.append(f"{label}.expected_ids must be an array of non-empty IDs.")
        elif (
            len(expected_ids) != len(set(expected_ids))
            or expected_ids != actual_ids
        ):
            errors.append(f"{label}.expected_ids must exactly match unique dataset IDs.")
        if len(actual_ids) != len(set(actual_ids)):
            errors.append(f"{label} contains duplicate problem IDs.")

    if eligible_counts["test"] < MINIMUM_TEST_RECORDS:
        errors.append(
            f"frozen dataset requires at least {MINIMUM_TEST_RECORDS} eligible test records; "
            f"found {eligible_counts['test']}."
        )
    if not (
        MINIMUM_DEVELOPMENT_RECORDS
        <= eligible_counts["development"]
        <= MAXIMUM_DEVELOPMENT_RECORDS
    ):
        errors.append(
            f"frozen dataset requires {MINIMUM_DEVELOPMENT_RECORDS}–"
            f"{MAXIMUM_DEVELOPMENT_RECORDS} eligible development records; "
            f"found {eligible_counts['development']}."
        )
    if candidate_counts != {
        split: eligible_counts[split] for split in ("development", "test")
    }:
        errors.append(
            "frozen dataset contains candidate records that are not all eligible."
        )
    declared_counts = manifest.get("candidate_split_counts")
    if declared_counts != candidate_counts:
        errors.append(
            "manifest candidate_split_counts do not match current candidate counts."
        )
    declared_eligible = manifest.get("eligible_split_counts")
    if declared_eligible != eligible_counts:
        errors.append(
            "manifest eligible_split_counts do not match validated eligible counts."
        )

    authors = manifest.get("dataset_author_ids")
    if not isinstance(authors, list) or not authors or any(
        not _valid_text(author_id) for author_id in authors
    ):
        errors.append(
            "freeze manifest dataset_author_ids must identify dataset authors "
            "for reviewer-independence checks."
        )
        author_ids: set[str] = set()
    else:
        author_ids = set(authors)
        if len(authors) != len(author_ids):
            errors.append("freeze manifest dataset_author_ids must be unique.")

    for records, _ in dataset_records.values():
        if isinstance(records, list):
            for record in records:
                if not isinstance(record, dict) or not isinstance(
                    record.get("curation"), dict
                ):
                    continue
                review_records = record["curation"].get("review_records", [])
                if not isinstance(review_records, list):
                    continue
                for review in review_records:
                    if (
                        isinstance(review, dict)
                        and review.get("reviewer_kind") == "independent_human_review"
                        and review.get("reviewer_id") in author_ids
                    ):
                        errors.append(
                            f"problem {record.get('id')!r}: independent reviewer ID "
                            "is listed as a dataset author."
                        )

    protocol_hash = manifest.get("locked_protocol_sha256")
    if not isinstance(protocol_hash, str) or re.fullmatch(
        r"[0-9a-fA-F]{64}", protocol_hash
    ) is None:
        errors.append("freeze manifest requires locked_protocol_sha256.")
    test_policy = manifest.get("test_access_policy")
    if (
        not isinstance(test_policy, dict)
        or test_policy.get("test_results_excluded_from_tuning") is not True
        or test_policy.get("test_inputs_restricted_until_protocol_lock") is not True
        or not _valid_text(test_policy.get("procedure"))
    ):
        errors.append(
            "freeze manifest requires a test_access_policy excluding test results "
            "from tuning and restricting inputs until protocol lock."
        )
    dispositions = manifest.get("likely_duplicate_dispositions")
    if not isinstance(dispositions, list):
        errors.append(
            "freeze manifest likely_duplicate_dispositions must be an array."
        )
    else:
        expected_pairs = set(_likely_duplicate_pairs(combined_records))
        disposition_pairs: set[tuple[str, str]] = set()
        for index, disposition in enumerate(dispositions, start=1):
            label = f"likely_duplicate_dispositions[{index}]"
            if not isinstance(disposition, dict):
                errors.append(f"{label} must be an object.")
                continue
            pair_ids = disposition.get("problem_ids")
            if (
                not isinstance(pair_ids, list)
                or len(pair_ids) != 2
                or any(not _valid_text(problem_id) for problem_id in pair_ids)
                or pair_ids != sorted(pair_ids)
                or pair_ids[0] == pair_ids[1]
            ):
                errors.append(
                    f"{label}.problem_ids must contain two distinct IDs in "
                    "lexicographic order."
                )
                continue
            pair = (pair_ids[0], pair_ids[1])
            if pair in disposition_pairs:
                errors.append(f"{label} duplicates a likely-duplicate disposition.")
            disposition_pairs.add(pair)
            if pair not in expected_pairs:
                errors.append(
                    f"{label} does not match a currently flagged likely-duplicate pair."
                )
            if disposition.get("decision") not in {"duplicate", "not_duplicate"}:
                errors.append(
                    f"{label}.decision must be 'duplicate' or 'not_duplicate'."
                )
            if disposition.get("reviewer_kind") != "independent_human_review":
                errors.append(
                    f"{label}.reviewer_kind must be 'independent_human_review'."
                )
            if not _valid_text(disposition.get("reviewer_id")):
                errors.append(f"{label}.reviewer_id must be non-empty text.")
            elif disposition.get("reviewer_id") in author_ids:
                errors.append(f"{label}.reviewer_id must not identify a dataset author.")
            if not _valid_iso_date(disposition.get("reviewed_on")):
                errors.append(f"{label}.reviewed_on must be an ISO date.")
            if not _valid_text(disposition.get("evidence")):
                errors.append(f"{label}.evidence must be non-empty text.")
            if disposition.get("decision") == "duplicate":
                errors.append(
                    f"{label} identifies a duplicate pair; remove or exclude one "
                    "record before freezing the dataset."
                )
        missing_pairs = expected_pairs - disposition_pairs
        for first_id, second_id in sorted(missing_pairs):
            errors.append(
                f"likely-duplicate pair {first_id!r}, {second_id!r} lacks an "
                "independent human disposition."
            )
    return FrozenCurationValidationReport(
        tuple(errors),
        candidate_counts,
        eligible_counts,
        test_dataset_sha256,
        development_dataset_sha256,
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
    parser.add_argument(
        "--validate-frozen-curation",
        action="store_true",
        help="validate eligibility, minimum sizes, independence, and freeze controls",
    )
    parser.add_argument(
        "--freeze-manifest",
        type=Path,
        help="freeze manifest required by --validate-frozen-curation",
    )
    parser.add_argument(
        "--development-dataset",
        type=Path,
        help="separate development JSON file required by freeze validation",
    )
    args = parser.parse_args(argv)

    if args.validate_curation_draft and (
        args.research_manifest or args.validate_frozen_curation
    ):
        parser.error(
            "--validate-curation-draft cannot be combined with strict/frozen validation"
        )
    if args.validate_frozen_curation and (
        not args.freeze_manifest or not args.development_dataset or args.research_manifest
    ):
        parser.error(
            "--validate-frozen-curation requires --freeze-manifest and "
            "--development-dataset, and cannot be combined with --research-manifest"
        )
    if args.freeze_manifest and not args.validate_frozen_curation:
        parser.error("--freeze-manifest requires --validate-frozen-curation")
    if args.development_dataset and not args.validate_frozen_curation:
        parser.error("--development-dataset requires --validate-frozen-curation")

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
            f"candidate development/test: {report.candidate_split_counts}; "
            f"eligible development/test: {report.eligible_split_counts}; "
            f"validation errors: {len(report.errors)}"
        )
        for error in report.errors:
            print(f"error: {error}", file=sys.stderr)
        for warning in report.review_warnings:
            print(f"review queue: {warning}", file=sys.stderr)
        return 0 if report.is_valid else 1
    if args.validate_frozen_curation:
        try:
            test_value, test_dataset_sha256 = _load_json_with_hash(args.dataset)
            development_value, development_dataset_sha256 = _load_json_with_hash(
                args.development_dataset
            )
            manifest = _load_json(args.freeze_manifest)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 1
        report = validate_frozen_curation(
            test_value,
            manifest,
            test_dataset_sha256,
            development_value=development_value,
            development_dataset_sha256=development_dataset_sha256,
        )
        print(
            f"SHA-256 development/test: {report.development_dataset_sha256}/"
            f"{report.dataset_sha256}; candidate development/test: "
            f"{report.candidate_split_counts}; eligible development/test: "
            f"{report.eligible_split_counts}; validation errors: "
            f"{len(report.errors)}"
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

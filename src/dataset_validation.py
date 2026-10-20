"""Validation helpers for NL2Lean problem datasets.

This module is intentionally separate from the experiment pipeline so legacy
inputs remain usable until a dataset has been reviewed and documented.
"""
from __future__ import annotations

import argparse
import json
import sys
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


@dataclass(frozen=True)
class ProblemProvenance:
    problem_id: str
    status: str
    missing_fields: tuple[str, ...]
    invalid_fields: tuple[str, ...]
    split: str | None


@dataclass(frozen=True)
class DatasetValidationReport:
    errors: tuple[str, ...]
    problems: tuple[ProblemProvenance, ...]

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


def validate_dataset(
    value: object, *, require_provenance: bool = False
) -> DatasetValidationReport:
    """Validate a dataset and classify each record's provenance completeness.

    Without ``require_provenance``, absent provenance is reported in the
    returned per-record classification but does not invalidate legacy inputs.
    """
    errors: list[str] = []
    if not isinstance(value, list):
        return DatasetValidationReport(
            errors=("dataset: expected a JSON array of problem objects.",),
            problems=(),
        )

    seen_ids: set[str] = set()
    problem_reports: list[ProblemProvenance] = []
    for index, record in enumerate(value, start=1):
        if not isinstance(record, dict):
            errors.append(f"record {index}: expected a JSON object.")
            continue

        raw_id = record.get("id")
        problem_id = raw_id.strip() if isinstance(raw_id, str) else ""
        label = f"problem {problem_id!r}" if problem_id else f"record {index}"

        for field in REQUIRED_FIELDS:
            if field not in record:
                errors.append(f"{label}: missing required field {field!r}.")

        if not _valid_text(raw_id):
            errors.append(f"{label}: field 'id' must be a non-empty string.")
        elif problem_id in seen_ids:
            errors.append(f"problem {problem_id!r}: duplicate value for field 'id'.")
        else:
            seen_ids.add(problem_id)

        for field in ("nl_statement", "category", "expected_lean_statement"):
            if field in record and not _valid_text(record[field]):
                errors.append(
                    f"{label}: field {field!r} must be a non-empty string."
                )

        if "difficulty" in record:
            difficulty = record["difficulty"]
            if (
                isinstance(difficulty, bool)
                or not isinstance(difficulty, int)
                or not 1 <= difficulty <= 5
            ):
                errors.append(
                    f"{label}: field 'difficulty' must be an integer from 1 to 5."
                )

        split = record.get("split")
        if "split" in record and (
            not isinstance(split, str) or split not in ALLOWED_SPLITS
        ):
            errors.append(
                f"{label}: field 'split' must be one of "
                f"{', '.join(sorted(ALLOWED_SPLITS))}; got {split!r}."
            )

        invalid: list[str] = []
        if "source_citation" in record and not _valid_text(record["source_citation"]):
            invalid.append("source_citation")
            errors.append(
                f"{label}: field 'source_citation' must be a non-empty string "
                "when supplied."
            )
        if "source_url" in record and not _valid_source_url(record["source_url"]):
            invalid.append("source_url")
            errors.append(
                f"{label}: field 'source_url' must be an absolute HTTP(S) URL "
                "when supplied."
            )
        if "license" in record and not _valid_text(record["license"]):
            invalid.append("license")
            errors.append(
                f"{label}: field 'license' must be a non-empty string when supplied."
            )
        if (
            "reference_lean_statement_provenance" in record
            and not _valid_text(record["reference_lean_statement_provenance"])
        ):
            invalid.append("reference_lean_statement_provenance")
            errors.append(
                f"{label}: field 'reference_lean_statement_provenance' must be a "
                "non-empty string when supplied."
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
                errors.append(
                    f"{label}: missing provenance field {field!r}."
                )

    return DatasetValidationReport(tuple(errors), tuple(problem_reports))


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
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
    args = parser.parse_args(argv)

    try:
        value: Any = _load_json(args.dataset)
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
        f"without split: {unsplit}"
    )
    if not args.require_provenance:
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

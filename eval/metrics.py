"""Report schema-aware metrics for NL2Lean result JSONL files.

Usage: python eval/metrics.py data/results/run.jsonl
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any


COMMON_REQUIRED_FIELDS = ("id", "category", "difficulty", "solved", "repair_attempts")
V2_REQUIRED_FIELDS = (
    "initial_synthesis_success",
    "success_within_repair_budget",
    "total_synthesis_attempts",
)


def _validate_record(record: object, line_number: int, path: Path) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError(f"{path}: line {line_number}: expected a JSON object.")

    missing = [field for field in COMMON_REQUIRED_FIELDS if field not in record]
    if missing:
        raise ValueError(
            f"{path}: line {line_number}: missing required field(s): {', '.join(missing)}."
        )
    if not isinstance(record["solved"], bool):
        raise ValueError(f"{path}: line {line_number}: 'solved' must be a boolean.")
    if not isinstance(record["repair_attempts"], int) or record["repair_attempts"] < 0:
        raise ValueError(
            f"{path}: line {line_number}: 'repair_attempts' must be a non-negative integer."
        )

    schema_version = record.get("schema_version")
    if schema_version is None:
        return record
    if schema_version != 2:
        raise ValueError(
            f"{path}: line {line_number}: unsupported schema_version {schema_version!r}."
        )

    missing = [field for field in V2_REQUIRED_FIELDS if field not in record]
    if missing:
        raise ValueError(
            f"{path}: line {line_number}: schema-v2 record is missing field(s): "
            f"{', '.join(missing)}."
        )
    initial_success = record["initial_synthesis_success"]
    if initial_success is not None and not isinstance(initial_success, bool):
        raise ValueError(
            f"{path}: line {line_number}: 'initial_synthesis_success' must be boolean or null."
        )
    if not isinstance(record["success_within_repair_budget"], bool):
        raise ValueError(
            f"{path}: line {line_number}: 'success_within_repair_budget' must be boolean."
        )
    if (
        not isinstance(record["total_synthesis_attempts"], int)
        or record["total_synthesis_attempts"] < 0
    ):
        raise ValueError(
            f"{path}: line {line_number}: 'total_synthesis_attempts' must be a "
            "non-negative integer."
        )
    return record


def load(path: str | Path) -> list[dict[str, Any]]:
    """Load and validate result JSONL, reporting malformed input line numbers."""

    results = []
    result_path = Path(path)
    with result_path.open() as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"{result_path}: line {line_number}: invalid JSON: {error.msg}."
                ) from error
            results.append(_validate_record(record, line_number, result_path))
    return results


def _rate(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "n/a (0 problems)"
    return f"{numerator}/{denominator} = {numerator / denominator:.1%}"


def _average(values: Iterable[int]) -> str:
    collected = list(values)
    if not collected:
        return "n/a (0 problems)"
    return f"{sum(collected) / len(collected):.2f} ({len(collected)} problems)"


def _group_by(results: list[dict[str, Any]], field: str) -> dict[Any, list[dict[str, Any]]]:
    grouped: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for result in results:
        grouped[result[field]].append(result)
    return grouped


def _append_historical_breakdown(lines: list[str], results: list[dict[str, Any]]) -> None:
    lines.append("Historical category breakdown (recorded final solved rate):")
    for category, records in sorted(_group_by(results, "category").items()):
        solved = sum(record["solved"] for record in records)
        lines.append(f"  {category:22s} {_rate(solved, len(records))}")

    lines.append("Historical difficulty breakdown (recorded final solved rate):")
    for difficulty, records in sorted(_group_by(results, "difficulty").items()):
        solved = sum(record["solved"] for record in records)
        lines.append(f"  difficulty {difficulty}: {_rate(solved, len(records))}")


def _append_v2_breakdown(lines: list[str], results: list[dict[str, Any]]) -> None:
    for field, label in (("category", "category"), ("difficulty", "difficulty")):
        lines.append(f"Schema-v2 {label} breakdown:")
        for value, records in sorted(_group_by(results, field).items()):
            initial_records = [
                record
                for record in records
                if record["initial_synthesis_success"] is not None
            ]
            initial_successes = sum(
                record["initial_synthesis_success"] for record in initial_records
            )
            repair_budget_successes = sum(
                record["success_within_repair_budget"] for record in records
            )
            prefix = f"difficulty {value}" if field == "difficulty" else f"{value:22s}"
            lines.append(
                f"  {prefix}: initial {_rate(initial_successes, len(initial_records))}; "
                f"within repair budget {_rate(repair_budget_successes, len(records))}"
            )


def _append_attempt_averages(lines: list[str], results: list[dict[str, Any]]) -> None:
    solved = [record for record in results if record["solved"]]
    lines.append(
        "Avg repair attempts (all problems): "
        + _average(record["repair_attempts"] for record in results)
    )
    lines.append(
        "Avg repair attempts (solved problems): "
        + _average(record["repair_attempts"] for record in solved)
    )
    if all(record.get("schema_version") == 2 for record in results):
        lines.append(
            "Avg total synthesis attempts (all problems): "
            + _average(record["total_synthesis_attempts"] for record in results)
        )
        lines.append(
            "Avg total synthesis attempts (solved problems): "
            + _average(record["total_synthesis_attempts"] for record in solved)
        )


def report(results: list[dict[str, Any]]) -> str:
    """Render metrics without treating repaired schema-v2 success as pass@1."""

    lines = [f"Total problems: {len(results)}"]
    final_successes = sum(record["solved"] for record in results)
    lines.append(f"Final verified successes: {_rate(final_successes, len(results))}")
    if not results:
        return "\n".join(lines)

    historical = [record for record in results if "schema_version" not in record]
    v2 = [record for record in results if record.get("schema_version") == 2]

    if historical:
        historical_successes = sum(record["solved"] for record in historical)
        lines.append(
            "Historical recorded final solved rate "
            f"(legacy pass@1 label): {_rate(historical_successes, len(historical))}"
        )
        _append_historical_breakdown(lines, historical)
        _append_attempt_averages(lines, historical)

    if v2:
        initial_records = [
            record for record in v2 if record["initial_synthesis_success"] is not None
        ]
        initial_successes = sum(
            record["initial_synthesis_success"] for record in initial_records
        )
        repair_budget_successes = sum(
            record["success_within_repair_budget"] for record in v2
        )
        lines.append("Schema-v2 results:")
        lines.append(
            "Initial synthesis success rate (among synthesized problems): "
            + _rate(initial_successes, len(initial_records))
        )
        lines.append(
            "Success within repair budget: "
            + _rate(repair_budget_successes, len(v2))
        )
        _append_attempt_averages(lines, v2)
        _append_v2_breakdown(lines, v2)

    failures = [record for record in results if not record["solved"]]
    if failures and any("failure_stage" in record for record in results):
        lines.append("Failure breakdown by stage:")
        breakdown: dict[str, int] = defaultdict(int)
        for record in failures:
            breakdown[str(record.get("failure_stage", "unknown"))] += 1
        for stage, count in sorted(breakdown.items()):
            lines.append(f"  {stage}: {count}")

    return "\n".join(lines)


def main(path: str | Path) -> None:
    print(report(load(path)))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python eval/metrics.py <results.jsonl>")
        sys.exit(1)
    main(sys.argv[1])

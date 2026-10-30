"""Report schema-aware metrics for NL2Lean result JSONL files.

Usage: python eval/metrics.py data/results/run.jsonl
"""
from __future__ import annotations

import json
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
    if (
        isinstance(record["repair_attempts"], bool)
        or not isinstance(record["repair_attempts"], int)
        or record["repair_attempts"] < 0
    ):
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
        isinstance(record["total_synthesis_attempts"], bool)
        or not isinstance(record["total_synthesis_attempts"], int)
        or record["total_synthesis_attempts"] < 0
    ):
        raise ValueError(
            f"{path}: line {line_number}: 'total_synthesis_attempts' must be a "
            "non-negative integer."
        )
    total_attempts = record["total_synthesis_attempts"]
    repair_attempts = record["repair_attempts"]
    success_within_budget = record["success_within_repair_budget"]
    solved = record["solved"]
    if initial_success is None:
        if total_attempts != 0 or repair_attempts != 0 or success_within_budget or solved:
            raise ValueError(
                f"{path}: line {line_number}: a problem without an initial synthesis "
                "attempt must have zero attempts and no success."
            )
    elif total_attempts != repair_attempts + 1:
        raise ValueError(
            f"{path}: line {line_number}: 'total_synthesis_attempts' must equal "
            "'repair_attempts' + 1 for synthesized problems."
        )
    if success_within_budget != solved:
        raise ValueError(
            f"{path}: line {line_number}: 'solved' must match "
            "'success_within_repair_budget'."
        )
    if initial_success and (not success_within_budget or total_attempts != 1):
        raise ValueError(
            f"{path}: line {line_number}: initial synthesis success must be a "
            "one-attempt success within the repair budget."
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


def _load_repair_budget(path: str | Path) -> int | None:
    manifest_path = Path(path).with_suffix(".run.json")
    if not manifest_path.exists():
        return None
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{manifest_path}: could not read valid run metadata: {error}") from error

    configuration = manifest.get("configuration") if isinstance(manifest, dict) else None
    max_repair = (
        configuration.get("max_repair")
        if isinstance(configuration, dict)
        else None
    )
    if max_repair is None:
        return None
    if isinstance(max_repair, bool) or not isinstance(max_repair, int) or max_repair < 0:
        raise ValueError(
            f"{manifest_path}: configuration.max_repair must be a non-negative integer."
        )
    return max_repair


def _load_frozen_analysis_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(
            f"{manifest_path}: could not read valid frozen analysis manifest: {error}"
        ) from error

    if not isinstance(manifest, dict):
        raise ValueError(f"{manifest_path}: frozen analysis manifest must be a JSON object.")
    if not isinstance(manifest.get("dataset_version"), str) or not manifest[
        "dataset_version"
    ].strip():
        raise ValueError(
            f"{manifest_path}: dataset_version must be a non-empty string."
        )

    expected_ids = manifest.get("expected_ids")
    if (
        not isinstance(expected_ids, list)
        or not expected_ids
        or any(
            not isinstance(problem_id, str)
            or not problem_id.strip()
            or problem_id != problem_id.strip()
            for problem_id in expected_ids
        )
    ):
        raise ValueError(
            f"{manifest_path}: expected_ids must be a non-empty array of "
            "trimmed, non-empty strings."
        )
    if len(expected_ids) != len(set(expected_ids)):
        raise ValueError(f"{manifest_path}: expected_ids contains duplicate IDs.")

    dataset_sha256 = manifest.get("dataset_sha256")
    if not isinstance(dataset_sha256, str) or len(dataset_sha256) != 64 or any(
        character not in "0123456789abcdefABCDEF" for character in dataset_sha256
    ):
        raise ValueError(
            f"{manifest_path}: dataset_sha256 must be a 64-character SHA-256 hex digest."
        )

    configurations = manifest.get("required_configurations")
    if (
        not isinstance(configurations, list)
        or not configurations
        or any(
            not isinstance(configuration, str)
            or not configuration.strip()
            or configuration != configuration.strip()
            for configuration in configurations
        )
    ):
        raise ValueError(
            f"{manifest_path}: required_configurations must be a non-empty array "
            "of trimmed, non-empty strings."
        )
    if len(configurations) != len(set(configurations)):
        raise ValueError(
            f"{manifest_path}: required_configurations contains duplicates."
        )
    return manifest


def validate_frozen_runs(
    result_paths: Iterable[str | Path], frozen_manifest_path: str | Path
) -> dict[str, list[dict[str, Any]]]:
    """Require one complete schema-v2 run for every frozen condition."""
    manifest_path = Path(frozen_manifest_path)
    manifest = _load_frozen_analysis_manifest(manifest_path)
    expected_ids = set(manifest["expected_ids"])
    required_configurations = manifest["required_configurations"]
    expected_hash = manifest["dataset_sha256"].lower()
    results_by_configuration: dict[str, list[dict[str, Any]]] = {}
    errors: list[str] = []

    for raw_path in result_paths:
        result_path = Path(raw_path)
        run_manifest_path = result_path.with_suffix(".run.json")
        try:
            run_manifest = json.loads(run_manifest_path.read_text())
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            errors.append(
                f"{run_manifest_path}: missing or invalid run manifest: {error}"
            )
            continue
        if not isinstance(run_manifest, dict):
            errors.append(f"{run_manifest_path}: run manifest must be a JSON object.")
            continue
        if run_manifest.get("schema_version") != 2:
            errors.append(f"{run_manifest_path}: run manifest must use schema version 2.")

        configuration_block = run_manifest.get("configuration")
        configuration = (
            configuration_block.get("experiment_config")
            if isinstance(configuration_block, dict)
            else None
        )
        if not isinstance(configuration, str) or not configuration:
            errors.append(
                f"{run_manifest_path}: missing configuration.experiment_config."
            )
            continue
        if configuration not in required_configurations:
            errors.append(
                f"{run_manifest_path}: unexpected configuration {configuration!r}."
            )
        if configuration in results_by_configuration:
            errors.append(
                f"{run_manifest_path}: duplicate run for configuration "
                f"{configuration!r}."
            )
        else:
            results_by_configuration[configuration] = []

        if run_manifest.get("status") != "completed":
            errors.append(
                f"{run_manifest_path}: run status must be 'completed'; got "
                f"{run_manifest.get('status')!r}."
            )

        input_block = run_manifest.get("input")
        input_hash = input_block.get("sha256") if isinstance(input_block, dict) else None
        if not isinstance(input_hash, str) or input_hash.lower() != expected_hash:
            errors.append(
                f"{run_manifest_path}: input.sha256 does not match frozen "
                "dataset_sha256."
            )

        run_id = run_manifest.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            errors.append(f"{run_manifest_path}: missing non-empty run_id.")

        try:
            records = load(result_path)
        except (OSError, ValueError) as error:
            errors.append(str(error))
            continue

        completed_count = run_manifest.get("completed_problem_count")
        if (
            isinstance(completed_count, bool)
            or not isinstance(completed_count, int)
            or completed_count != len(expected_ids)
        ):
            errors.append(
                f"{run_manifest_path}: completed_problem_count must equal "
                f"{len(expected_ids)}; got {completed_count!r}."
            )

        if not records:
            errors.append(f"{result_path}: contains no final result records.")
        ids: list[str] = []
        for line_number, record in enumerate(records, start=1):
            problem_id = record.get("id")
            if not isinstance(problem_id, str) or not problem_id:
                errors.append(
                    f"{result_path}: result record {line_number} has no valid string id."
                )
                continue
            ids.append(problem_id)
            if record.get("schema_version") != 2:
                errors.append(
                    f"{result_path}: result record {line_number} is not schema version 2."
                )
            if record.get("run_id") != run_id:
                errors.append(
                    f"{result_path}: result record {line_number} run_id does not "
                    "match its run manifest."
                )
            if record.get("experiment_config") != configuration:
                errors.append(
                    f"{result_path}: result record {line_number} experiment_config "
                    f"does not match run configuration {configuration!r}."
                )

        duplicates = sorted(
            {problem_id for problem_id in ids if ids.count(problem_id) > 1}
        )
        if duplicates:
            errors.append(
                f"{result_path}: duplicate result IDs: {', '.join(duplicates)}."
            )
        actual_ids = set(ids)
        missing_ids = sorted(expected_ids - actual_ids)
        unexpected_ids = sorted(actual_ids - expected_ids)
        if missing_ids:
            errors.append(
                f"{result_path}: missing expected result IDs: {', '.join(missing_ids)}."
            )
        if unexpected_ids:
            errors.append(
                f"{result_path}: unexpected result IDs: {', '.join(unexpected_ids)}."
            )

        if (
            configuration in required_configurations
            and configuration in results_by_configuration
        ):
            if not results_by_configuration[configuration]:
                results_by_configuration[configuration] = records

    missing_configurations = sorted(
        set(required_configurations) - set(results_by_configuration)
    )
    if missing_configurations:
        errors.append(
            "Missing required configuration runs: "
            + ", ".join(missing_configurations)
            + "."
        )

    if errors:
        raise ValueError("Frozen run completeness check failed:\n- " + "\n- ".join(errors))
    return results_by_configuration


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


def report(
    results: list[dict[str, Any]], *, max_repair: int | None = None
) -> str:
    """Render metrics without treating repaired schema-v2 success as pass@1."""

    if max_repair is not None and (
        isinstance(max_repair, bool) or not isinstance(max_repair, int) or max_repair < 0
    ):
        raise ValueError("max_repair must be a non-negative integer or None.")

    lines = [f"Total problems: {len(results)}"]
    final_successes = sum(record["solved"] for record in results)
    lines.append(f"Final verified successes: {_rate(final_successes, len(results))}")
    if not results:
        lines.append(
            "Attempt-0 success (initial synthesis candidate): "
            + _rate(0, 0)
        )
        lines.append(
            "Post-repair success within configured repair budget: "
            + _rate(0, 0)
        )
        return "\n".join(lines)

    historical = [record for record in results if "schema_version" not in record]
    v2 = [record for record in results if record.get("schema_version") == 2]

    if historical:
        historical_successes = sum(record["solved"] for record in historical)
        lines.append(
            "Historical recorded final solved rate "
            f"(not attempt-0 pass@1): {_rate(historical_successes, len(historical))}"
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
        if max_repair is not None:
            over_budget = [
                record
                for record in v2
                if record["repair_attempts"] > max_repair
            ]
            if over_budget:
                problem_ids = ", ".join(str(record["id"]) for record in over_budget)
                raise ValueError(
                    "Schema-v2 records exceed configured repair budget "
                    f"({max_repair}): {problem_ids}."
                )
        lines.append("Schema-v2 results:")
        lines.append(
            "Attempt-0 success (initial synthesis candidate, among synthesized problems): "
            + _rate(initial_successes, len(initial_records))
        )
        lines.append(
            "Post-repair success within configured repair budget"
            + (f" ({max_repair} repairs): " if max_repair is not None else ": ")
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


def main(
    path: str | Path,
    *,
    frozen_manifest: str | Path | None = None,
    additional_paths: Iterable[str | Path] = (),
) -> None:
    if frozen_manifest is None:
        if tuple(additional_paths):
            raise ValueError("additional result paths require --frozen-manifest.")
        print(report(load(path), max_repair=_load_repair_budget(path)))
        return

    paths = [path, *additional_paths]
    results_by_configuration = validate_frozen_runs(paths, frozen_manifest)
    paths_by_configuration: dict[str, Path] = {}
    for candidate in paths:
        run_manifest = json.loads(
            Path(candidate).with_suffix(".run.json").read_text()
        )
        configuration = run_manifest["configuration"]["experiment_config"]
        paths_by_configuration[configuration] = Path(candidate)
    for configuration in sorted(results_by_configuration):
        print(f"Configuration: {configuration}")
        print(
            report(
                results_by_configuration[configuration],
                max_repair=_load_repair_budget(paths_by_configuration[configuration]),
            )
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Report NL2Lean metrics, optionally requiring frozen-run completeness."
    )
    parser.add_argument("results", nargs="+", type=Path, help="one or more result JSONL files")
    parser.add_argument(
        "--frozen-manifest",
        type=Path,
        help=(
            "require complete schema-v2 runs matching this frozen dataset manifest "
            "and its required_configurations"
        ),
    )
    args = parser.parse_args()
    try:
        main(
            args.results[0],
            frozen_manifest=args.frozen_manifest,
            additional_paths=args.results[1:],
        )
    except ValueError as error:
        parser.error(str(error))

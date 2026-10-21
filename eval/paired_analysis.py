"""Reproducible problem-level analysis for frozen paired A/B/C run artifacts.

Study outputs are emitted only when a frozen development/test dataset validates.
Legacy pipeline JSONL files and mock/manual runs are retained in the audit trail,
but never treated as autonomous A/B/C model outcomes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 1
BOOTSTRAP_RESAMPLES = 10_000
BOOTSTRAP_SEED = 20271021
CATEGORY_MIN_N = 5
CONDITIONS = ("A", "B", "C")
COMPARISONS = (("C", "B"), ("C", "A"), ("B", "A"))
APPROVED_PROTOCOL_STATUSES = {"approved_and_preregistered", "frozen_and_preregistered"}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def wilson_interval(successes: int, denominator: int, z: float = 1.959963984540054) -> tuple[float, float] | None:
    """Wilson score interval; None when there are no observations."""
    if denominator <= 0:
        return None
    p = successes / denominator
    z2 = z * z
    scale = 1 + z2 / denominator
    center = (p + z2 / (2 * denominator)) / scale
    half = z * math.sqrt(p * (1 - p) / denominator + z2 / (4 * denominator**2)) / scale
    return max(0.0, center - half), min(1.0, center + half)


def exact_mcnemar_p(discordant_first_only: int, discordant_second_only: int) -> float | None:
    """Two-sided exact McNemar/binomial p-value; None if no discordant pairs."""
    n = discordant_first_only + discordant_second_only
    if n == 0:
        return None
    lower = min(discordant_first_only, discordant_second_only)
    tail = sum(math.comb(n, k) for k in range(lower + 1)) / (2**n)
    return min(1.0, 2 * tail)


def holm_adjust(p_values: list[float | None]) -> list[float | None]:
    """Holm step-down adjusted p-values, preserving None for non-informative tests."""
    result: list[float | None] = [None] * len(p_values)
    indexed = sorted(
        ((1.0 if p is None else p, index, p is not None) for index, p in enumerate(p_values)),
        key=lambda item: item[0],
    )
    running = 0.0
    count = len(indexed)
    for rank, (p_value, original_index, is_informative) in enumerate(indexed):
        running = max(running, min(1.0, (count - rank) * p_value))
        if is_informative:
            result[original_index] = running
    return result


def paired_bootstrap_interval(
    differences: list[float], *, resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[float, float] | None:
    """Percentile CI resampling problems, not attempts or repeated seeds."""
    if not differences:
        return None
    rng = random.Random(seed)
    n = len(differences)
    means = sorted(
        sum(differences[rng.randrange(n)] for _ in range(n)) / n
        for _ in range(resamples)
    )
    lo = means[max(0, math.floor(0.025 * resamples))]
    hi = means[min(resamples - 1, math.ceil(0.975 * resamples) - 1)]
    return lo, hi


def paired_comparison_summary(
    first: list[bool | None], second: list[bool | None],
) -> dict[str, Any]:
    """Summarize aligned problem outcomes; missing is excluded only from McNemar."""
    if len(first) != len(second):
        raise ValueError("Paired outcome vectors must have equal length.")
    complete = [(a, b) for a, b in zip(first, second) if a is not None and b is not None]
    first_only = sum(a is True and b is False for a, b in complete)
    second_only = sum(a is False and b is True for a, b in complete)
    p_value = exact_mcnemar_p(first_only, second_only)
    # Conservative full-denominator sensitivity analysis: any missing outcome is failure.
    differences = [float(a is True) - float(b is True) for a, b in zip(first, second)]
    interval = paired_bootstrap_interval(differences)
    return {
        "first_only": first_only,
        "second_only": second_only,
        "complete_pairs": len(complete),
        "missing_pairs": len(first) - len(complete),
        "eligible_denominator": len(first),
        "absolute_difference_missing_as_failure": sum(differences) / len(first) if first else None,
        "bootstrap_interval": interval,
        "mcnemar_p": p_value,
    }


def success_at_budget(condition: object, budget: int) -> bool | None:
    """Return verified success by repair budget, or None if outcome is missing."""
    if not isinstance(condition, dict):
        return None
    milestones = condition.get("milestones")
    if not isinstance(milestones, dict):
        return None
    status = condition.get("status")
    observed = False
    for repair_count in range(budget + 1):
        milestone = milestones.get(str(repair_count))
        if not isinstance(milestone, dict):
            continue
        value = milestone.get("success")
        if isinstance(value, bool):
            observed = True
            if value:
                return True
    if status in {
        "provider_error", "incomplete", "timeout", "infrastructure_error",
        "verifier_error", "invalid_input", "not_run_initial_provider_error",
    }:
        if budget > max((int(key) for key in milestones if str(key).isdigit()), default=-1):
            return None
    if observed:
        return False
    if status in {
        "compiler_failure", "proof_rejected", "repair_budget_exhausted",
        "empty_output", "missing_compiler_diagnostics", "not_eligible_initial_failure",
        "not_needed_initial_success",
    }:
        if status == "not_needed_initial_success":
            return True
        return False
    return None


def first_attempt_success(run: object) -> bool | None:
    if not isinstance(run, dict):
        return None
    initial = run.get("initial_verification")
    if not isinstance(initial, dict) or not isinstance(initial.get("success"), bool):
        return None
    if initial.get("status") in {
        "timeout", "infrastructure_error", "verifier_error", "invalid_input"
    }:
        return None
    return initial["success"]


def classify_compiler_error(text: str) -> str:
    """Stable descriptive taxonomy; raw diagnostic text is preserved separately."""
    value = text.casefold()
    if any(token in value for token in ("unexpected token", "expected command", "parse error", "invalid syntax")):
        return "syntax_or_parser"
    if any(token in value for token in ("unknown identifier", "unknown constant", "unknown namespace")):
        return "unknown_identifier_or_name"
    if any(token in value for token in ("type mismatch", "application type mismatch", "function expected")):
        return "type_mismatch_or_elaboration"
    if any(token in value for token in ("unsolved goals", "tactic", "no goals to be solved")):
        return "tactic_or_unsolved_goal"
    if "timeout" in value or "timed out" in value:
        return "timeout"
    return "other_compiler_error"


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{path}: cannot read JSON: {error}") from error


def load_run_manifests(runs_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    runs: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for path in sorted(runs_dir.rglob("*.json")) if runs_dir.exists() else []:
        try:
            value = load_json(path)
        except ValueError as error:
            errors.append({"path": str(path), "error": str(error)})
            continue
        if not isinstance(value, dict):
            errors.append({"path": str(path), "error": "run manifest must be a JSON object"})
            continue
        if value.get("experiment_type") != "paired_compiler_guided_repair":
            continue
        value["_artifact_path"] = str(path)
        value["_artifact_sha256"] = sha256_file(path)
        runs.append(value)
    return runs, errors


def repeated_problem_runs(runs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        problem_id = run.get("problem_id")
        if isinstance(problem_id, str):
            grouped[problem_id].append(run)
    return {problem_id: values for problem_id, values in grouped.items() if len(values) > 1}


def _write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _manifest_success_by_budget(run: dict[str, Any], condition: str, budget: int) -> bool | None:
    conditions = run.get("conditions")
    return success_at_budget(conditions.get(condition) if isinstance(conditions, dict) else None, budget)


def _bootstrap_summary(values: list[float]) -> dict[str, float] | None:
    interval = paired_bootstrap_interval(values)
    if interval is None:
        return None
    return {"lower": interval[0], "upper": interval[1]}


def _semantic_label(record: dict[str, Any]) -> str:
    curation = record.get("curation", {})
    fidelity = curation.get("semantic_fidelity", {}) if isinstance(curation, dict) else {}
    label = fidelity.get("label") if isinstance(fidelity, dict) else None
    status = fidelity.get("review_status") if isinstance(fidelity, dict) else None
    return str(label) if label and status == "verified" else "pending_or_unreviewed"


def _diagnostics_for_run(run: dict[str, Any]) -> list[str]:
    values: list[str] = []
    initial = run.get("initial_verification", {})
    if isinstance(initial, dict):
        for diagnostic in initial.get("diagnostics") or []:
            if isinstance(diagnostic, dict) and diagnostic.get("severity") == "error":
                data = diagnostic.get("data")
                if isinstance(data, str):
                    values.append(data)
        if not values and isinstance(initial.get("diagnostic_text"), str):
            values.append(initial["diagnostic_text"])
    return values


def _make_svg(path: Path, counts: dict[int, dict[str, int]]) -> None:
    width, height = 760, 420
    left, top, chart_w, chart_h = 80, 45, 630, 280
    colors = {"A": "#4c78a8", "B": "#f58518", "C": "#54a24b"}
    bars: list[str] = []
    bars.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    bars.append('<rect width="100%" height="100%" fill="white"/>')
    bars.append('<text x="380" y="25" text-anchor="middle" font-family="sans-serif" font-size="18">Verified success by repair-call budget</text>')
    bars.append(f'<line x1="{left}" y1="{top+chart_h}" x2="{left+chart_w}" y2="{top+chart_h}" stroke="#333"/>')
    bars.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+chart_h}" stroke="#333"/>')
    for fraction in (0, .25, .5, .75, 1):
        y = top + chart_h * (1 - fraction)
        bars.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left+chart_w}" y2="{y:.1f}" stroke="#ddd"/>')
        bars.append(f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" font-family="sans-serif" font-size="11">{fraction:.0%}</text>')
    group_w = chart_w / 4
    bar_w = 34
    for budget in range(4):
        center = left + group_w * (budget + .5)
        bars.append(f'<text x="{center:.1f}" y="{top+chart_h+23}" text-anchor="middle" font-family="sans-serif" font-size="12">{budget} repairs</text>')
        d = counts[budget]["denominator"]
        for j, condition in enumerate(CONDITIONS):
            n_success = counts[budget][condition]
            rate = n_success / d if d else 0.0
            x = center + (j - 1) * (bar_w + 5) - bar_w / 2
            bar_h = chart_h * rate
            y = top + chart_h - bar_h
            bars.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{bar_h:.1f}" fill="{colors[condition]}"/>')
            bars.append(f'<title>{condition}: {n_success}/{d}; incomplete counted as failure</title>')
    for j, condition in enumerate(CONDITIONS):
        x = left + j * 100
        bars.append(f'<rect x="{x}" y="385" width="14" height="14" fill="{colors[condition]}"/>')
        bars.append(f'<text x="{x+20}" y="397" font-family="sans-serif" font-size="12">{condition}</text>')
    bars.append(f'<text x="{left+chart_w/2}" y="{height-5}" text-anchor="middle" font-family="sans-serif" font-size="11">Each bar uses the full eligible test denominator; missing outcomes count as failures</text>')
    bars.append('</svg>')
    path.write_text("\n".join(bars) + "\n", encoding="utf-8")


def analyze_frozen(
    *, test_path: Path, development_path: Path, freeze_manifest_path: Path,
    runs_dir: Path, output_dir: Path,
) -> dict[str, Any]:
    """Validate frozen inputs, then write tables/figure and a provenance manifest."""
    import sys
    sys.path.insert(0, str(REPOSITORY_ROOT / "src"))
    from dataset_validation import validate_frozen_curation

    test_records = load_json(test_path)
    dev_records = load_json(development_path)
    freeze_manifest = load_json(freeze_manifest_path)
    test_hash, dev_hash = sha256_file(test_path), sha256_file(development_path)
    validation = validate_frozen_curation(
        test_records, freeze_manifest, test_hash,
        development_value=dev_records, development_dataset_sha256=dev_hash,
    )
    if not validation.is_valid:
        raise ValueError("Frozen dataset validation failed:\n- " + "\n- ".join(validation.errors))
    if not isinstance(test_records, list) or not isinstance(dev_records, list):
        raise ValueError("Development and test dataset files must contain JSON arrays.")

    eligible_ids = [record["id"] for record in test_records]
    runs, malformed = load_run_manifests(runs_dir)
    paired_runs = [run for run in runs if run.get("execution_mode") == "api"]
    excluded_mode_runs = [run for run in runs if run.get("execution_mode") != "api"]
    by_problem: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in paired_runs:
        problem_id = run.get("problem_id")
        if isinstance(problem_id, str):
            by_problem[problem_id].append(run)
    repeated = repeated_problem_runs(paired_runs)
    if repeated:
        raise ValueError(
            "Repeated runs for one problem detected; planned protocol has one replicate. "
            "Do not count repetitions as independent problems: "
            + ", ".join(f"{key}={len(value)}" for key, value in sorted(repeated.items()))
        )
    run_by_problem = {key: values[0] for key, values in by_problem.items()}
    mismatches = []
    protocol_hashes: set[str] = set()
    config_hashes: set[str] = set()
    run_ids: set[str] = set()
    for problem_id, run in run_by_problem.items():
        if problem_id not in eligible_ids:
            mismatches.append(f"unexpected test problem {problem_id}")
        if run.get("dataset_sha256") != test_hash:
            mismatches.append(f"{problem_id}: dataset SHA-256 differs from frozen test file")
        protocol = run.get("protocol")
        if isinstance(protocol, dict) and isinstance(protocol.get("sha256"), str):
            protocol_hashes.add(protocol["sha256"])
            if protocol.get("status") not in APPROVED_PROTOCOL_STATUSES:
                mismatches.append(f"{problem_id}: protocol is not approved and preregistered")
            protocol_path = protocol.get("path")
            if isinstance(protocol_path, str):
                referenced_protocol = (REPOSITORY_ROOT / protocol_path).resolve()
                if not referenced_protocol.is_file() or sha256_file(referenced_protocol) != protocol["sha256"]:
                    mismatches.append(f"{problem_id}: referenced protocol file is missing or hash-mismatched")
            else:
                mismatches.append(f"{problem_id}: protocol path missing")
        else:
            mismatches.append(f"{problem_id}: protocol hash missing")
        config_hash = run.get("configuration_sha256")
        if isinstance(config_hash, str):
            config_hashes.add(config_hash)
            configuration = run.get("configuration")
            if not isinstance(configuration, dict):
                mismatches.append(f"{problem_id}: configuration object missing")
            else:
                config_bytes = json.dumps(configuration, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
                if sha256_bytes(config_bytes) != config_hash:
                    mismatches.append(f"{problem_id}: configuration hash does not match configuration object")
        else:
            mismatches.append(f"{problem_id}: configuration hash missing")
        run_id = run.get("experiment_id")
        if not isinstance(run_id, str) or not run_id:
            mismatches.append(f"{problem_id}: experiment ID missing")
        elif run_id in run_ids:
            mismatches.append(f"{problem_id}: duplicate experiment ID {run_id}")
        else:
            run_ids.add(run_id)
        conditions = run.get("conditions")
        initial = run.get("initial_candidate")
        initial_hash = initial.get("candidate_sha256") if isinstance(initial, dict) else None
        if not isinstance(conditions, dict) or not isinstance(initial_hash, str):
            mismatches.append(f"{problem_id}: conditions or initial candidate hash missing")
        else:
            for condition_name in CONDITIONS:
                condition = conditions.get(condition_name)
                if not isinstance(condition, dict):
                    mismatches.append(f"{problem_id}: condition {condition_name} missing")
                    continue
                not_run = str(condition.get("status", "")).startswith("not_run_")
                if not_run and not initial_hash:
                    # Preserve an incomplete run whose shared initial call failed.
                    continue
                if condition.get("starting_candidate_sha256") != initial_hash:
                    mismatches.append(f"{problem_id}: {condition_name} does not use the shared initial candidate")
                attempts = condition.get("attempts")
                if not_run and attempts is None:
                    continue
                if not isinstance(attempts, list):
                    mismatches.append(f"{problem_id}: {condition_name} attempt trace missing")
                elif condition_name == "A" and attempts:
                    mismatches.append(f"{problem_id}: A contains repair attempts")
                elif condition_name in {"B", "C"} and len(attempts) > 3:
                    mismatches.append(f"{problem_id}: {condition_name} exceeds the three-call repair budget")
        model = run.get("model_identifier")
        if not isinstance(model, str) or not model:
            mismatches.append(f"{problem_id}: model identifier missing")
        if run.get("status") == "running":
            # Kept in denominator; outcomes lacking verified milestones are missing.
            pass
    if len(protocol_hashes) > 1:
        mismatches.append("runs use inconsistent protocol hashes")
    if len(config_hashes) > 1:
        mismatches.append("runs use inconsistent configuration hashes")

    # A mismatch is preserved and prevents inferential output.
    if mismatches:
        raise ValueError("Run artifact validation failed:\n- " + "\n- ".join(mismatches))

    output_dir.mkdir(parents=True, exist_ok=False)
    composition: list[dict[str, Any]] = []
    for split, records in (("development", dev_records), ("test", test_records)):
        grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
        for record in records:
            curation = record.get("curation", {})
            source_metadata = curation.get("source_metadata", {}) if isinstance(curation, dict) else {}
            source = (
                source_metadata.get("source_title")
                or curation.get("source_id")
                or curation.get("source_url")
                or curation.get("source_citation")
                or record.get("source_item_id")
                or "unknown"
            )
            grouped[(record.get("category", "unknown"), str(record.get("difficulty", "unknown")), str(source))].append(record)
        for (category, difficulty, source), group in sorted(grouped.items()):
            composition.append({"split": split, "category": category, "difficulty": difficulty, "source": source, "count": len(group), "problem_ids": ";".join(r["id"] for r in group)})
    _write_csv(output_dir / "dataset_composition.csv", composition, ["split", "category", "difficulty", "source", "count", "problem_ids"])

    eligible_n = len(eligible_ids)
    success_by_condition: dict[str, dict[str, bool | None]] = {condition: {} for condition in CONDITIONS}
    budget_counts: dict[int, dict[str, int]] = {budget: {condition: 0 for condition in CONDITIONS} | {"denominator": eligible_n, "missing": 0} for budget in range(4)}
    metric_rows: list[dict[str, Any]] = []
    initial_successes = sum(first_attempt_success(run_by_problem.get(pid)) is True for pid in eligible_ids)
    initial_observed = sum(first_attempt_success(run_by_problem.get(pid)) is not None for pid in eligible_ids)
    initial_interval = wilson_interval(initial_successes, eligible_n)
    metric_rows.append({
        "condition": "shared_initial",
        "metric": "first_attempt_verified_success",
        "repair_budget": 0,
        "successes_including_missing_as_failure": initial_successes,
        "eligible_test_denominator": eligible_n,
        "observed_outcomes": initial_observed,
        "missing_or_incomplete": eligible_n - initial_observed,
        "rate": initial_successes / eligible_n if eligible_n else None,
        "wilson_95_lower": initial_interval[0] if initial_interval else None,
        "wilson_95_upper": initial_interval[1] if initial_interval else None,
        "missing_policy": "full eligible denominator; missing outcomes counted as failures",
    })
    for condition in CONDITIONS:
        for budget in range(4):
            successes = observed = 0
            for problem_id in eligible_ids:
                run = run_by_problem.get(problem_id)
                value = _manifest_success_by_budget(run, condition, budget) if run else None
                if value is True:
                    successes += 1
                    observed += 1
                elif value is False:
                    observed += 1
            budget_counts[budget][condition] = successes
            if condition == "A" and budget == 0:
                for problem_id in eligible_ids:
                    run = run_by_problem.get(problem_id)
                    success_by_condition[condition][problem_id] = first_attempt_success(run) if run else None
            else:
                for problem_id in eligible_ids:
                    run = run_by_problem.get(problem_id)
                    success_by_condition[condition][problem_id] = _manifest_success_by_budget(run, condition, budget) if run else None
            interval = wilson_interval(successes, eligible_n)
            metric_rows.append({
                "condition": condition,
                "metric": "verified_success_by_repair_budget",
                "repair_budget": budget,
                "successes_including_missing_as_failure": successes,
                "eligible_test_denominator": eligible_n,
                "observed_outcomes": observed,
                "missing_or_incomplete": eligible_n - observed,
                "rate": successes / eligible_n if eligible_n else None,
                "wilson_95_lower": interval[0] if interval else None,
                "wilson_95_upper": interval[1] if interval else None,
                "missing_policy": "full eligible denominator; missing outcomes counted as failures",
            })
    _write_csv(output_dir / "success_by_repair_budget.csv", metric_rows, list(metric_rows[0]) if metric_rows else ["condition", "metric"])
    _make_svg(output_dir / "success_by_repair_budget.svg", budget_counts)

    resource_rows: list[dict[str, Any]] = []
    for condition in CONDITIONS:
        known_tokens = 0
        missing_token_calls = 0
        latency_values: list[float] = []
        attempt_wall_values: list[float] = []
        http_attempts_observed = 0
        calls_missing_http_attempt_count = 0
        repair_calls = 0
        logical_completions = 0
        present_runs = 0
        run_wall_clock: list[float] = []
        for problem_id in eligible_ids:
            run = run_by_problem.get(problem_id)
            if not run:
                missing_token_calls += 1
                continue
            present_runs += 1
            initial = run.get("initial_candidate", {})
            if isinstance(initial, dict) and initial:
                logical_completions += 1
                initial_http = initial.get("transport_api_attempts")
                if isinstance(initial_http, int) and not isinstance(initial_http, bool):
                    http_attempts_observed += initial_http
                else:
                    calls_missing_http_attempt_count += 1
            condition_map = run.get("conditions", {})
            condition_record = condition_map.get(condition, {}) if isinstance(condition_map, dict) else {}
            attempts = condition_record.get("attempts", []) if isinstance(condition_record, dict) else []
            repair_calls += len(attempts) if isinstance(attempts, list) else 0
            logical_completions += len(attempts) if isinstance(attempts, list) else 0
            logical_records = [initial] + [a for a in attempts if isinstance(a, dict)]
            for call_record in logical_records:
                metadata = call_record.get("completion_metadata", {})
                total_tokens = metadata.get("total_tokens") if isinstance(metadata, dict) else call_record.get("total_tokens")
                if isinstance(total_tokens, int) and not isinstance(total_tokens, bool):
                    known_tokens += total_tokens
                else:
                    missing_token_calls += 1
                http_count = call_record.get("transport_api_attempts")
                if isinstance(http_count, int) and not isinstance(http_count, bool):
                    http_attempts_observed += http_count
                else:
                    calls_missing_http_attempt_count += 1
                latency = metadata.get("latency_seconds") if isinstance(metadata, dict) else None
                if isinstance(latency, (int, float)) and not isinstance(latency, bool):
                    latency_values.append(float(latency))
                attempt_wall = call_record.get("wall_clock_seconds")
                if isinstance(attempt_wall, (int, float)) and not isinstance(attempt_wall, bool):
                    attempt_wall_values.append(float(attempt_wall))
            wall = run.get("wall_clock_seconds")
            if isinstance(wall, (int, float)) and not isinstance(wall, bool):
                run_wall_clock.append(float(wall))
        resource_rows.append({
            "condition": condition,
            "eligible_test_denominator": eligible_n,
            "runs_present": present_runs,
            "missing_runs": eligible_n - present_runs,
            "repair_calls_observed": repair_calls,
            "repair_calls_per_eligible_problem": repair_calls / eligible_n if eligible_n else None,
            "logical_completions_observed": logical_completions,
            "http_attempts_observed": http_attempts_observed,
            "logical_calls_missing_http_attempt_count": calls_missing_http_attempt_count,
            "total_tokens_reported": known_tokens,
            "completion_calls_missing_token_usage": missing_token_calls,
            "mean_attempt_latency_seconds": sum(latency_values) / len(latency_values) if latency_values else None,
            "attempt_latency_observations": len(latency_values),
            "mean_call_wall_clock_seconds": sum(attempt_wall_values) / len(attempt_wall_values) if attempt_wall_values else None,
            "call_wall_clock_observations": len(attempt_wall_values),
            "mean_paired_run_wall_clock_seconds": sum(run_wall_clock) / len(run_wall_clock) if run_wall_clock else None,
            "run_wall_clock_observations": len(run_wall_clock),
            "wall_clock_scope": "whole A/B/C run; not condition-attributable",
            "shared_initial_included": True,
            "token_scope": "shared initial plus condition repairs; do not sum condition rows to obtain run total",
            "estimated_cost": None,
            "estimated_cost_status": "unavailable_without_human_reviewed_model_specific_pricing_input",
        })
    _write_csv(output_dir / "resource_metrics.csv", resource_rows, list(resource_rows[0]) if resource_rows else ["condition"])

    paired_rows: list[dict[str, Any]] = []
    p_values: list[float | None] = []
    for first, second in COMPARISONS:
        first_map = success_by_condition[first]
        second_map = success_by_condition[second]
        summary = paired_comparison_summary(
            [first_map[i] for i in eligible_ids],
            [second_map[i] for i in eligible_ids],
        )
        p_value = summary["mcnemar_p"]
        p_values.append(p_value)
        ci = summary["bootstrap_interval"]
        paired_rows.append({
            "comparison": f"{first}_over_{second}",
            "first_condition": first,
            "second_condition": second,
            "first_only_success_complete_pairs": summary["first_only"],
            "second_only_success_complete_pairs": summary["second_only"],
            "complete_matched_pairs": summary["complete_pairs"],
            "eligible_test_denominator": summary["eligible_denominator"],
            "missing_pairs": summary["missing_pairs"],
            "absolute_difference_itt_missing_as_failure": summary["absolute_difference_missing_as_failure"],
            "relative_difference_itt_missing_as_failure": (
                summary["absolute_difference_missing_as_failure"]
                / (sum(value is True for value in [second_map[i] for i in eligible_ids]) / eligible_n)
                if eligible_n and sum(value is True for value in [second_map[i] for i in eligible_ids]) > 0
                else None
            ),
            "paired_bootstrap_95_lower": ci[0] if ci else None,
            "paired_bootstrap_95_upper": ci[1] if ci else None,
            "mcnemar_exact_two_sided_p": p_value,
            "test_status": "non_informative_no_discordant_pairs" if p_value is None else "complete_case_exact_mcnemar",
        })
    adjusted = holm_adjust(p_values)
    for row, adjusted_p in zip(paired_rows, adjusted):
        row["mcnemar_holm_adjusted_p"] = adjusted_p
    _write_csv(output_dir / "paired_comparisons.csv", paired_rows, list(paired_rows[0]) if paired_rows else ["comparison"])

    # The first compiler failure taxonomy uses raw initial verifier diagnostics.
    error_groups: dict[str, list[str]] = defaultdict(list)
    for problem_id, run in run_by_problem.items():
        if first_attempt_success(run) is False:
            diagnostics = _diagnostics_for_run(run)
            if diagnostics:
                error_groups[classify_compiler_error(diagnostics[0])].append(problem_id)
    error_rows = []
    for category in sorted(error_groups):
        ids = sorted(set(error_groups[category]))
        for condition in CONDITIONS:
            successes = sum(
                _manifest_success_by_budget(run_by_problem.get(problem_id), condition, 3) is True
                for problem_id in ids
            )
            interval = wilson_interval(successes, len(ids))
            error_rows.append({
                "compiler_error_category": category,
                "condition": condition,
                "initial_failed_problems": len(ids),
                "successes_within_repair_budget": successes,
                "denominator": len(ids),
                "problem_ids": ";".join(ids),
                "representation": "sufficient" if len(ids) >= CATEGORY_MIN_N else "sparse_descriptive_only",
                "success_rate": successes / len(ids) if ids else None,
                "wilson_95_lower": interval[0] if interval else None,
                "wilson_95_upper": interval[1] if interval else None,
                "missing_policy": "unknown outcomes count as failures; category is first initial error diagnostic",
            })
    _write_csv(output_dir / "error_taxonomy.csv", error_rows, ["compiler_error_category", "condition", "initial_failed_problems", "successes_within_repair_budget", "denominator", "problem_ids", "representation", "success_rate", "wilson_95_lower", "wilson_95_upper", "missing_policy"])

    semantic_counts = Counter(_semantic_label(record) for record in test_records)
    semantic_rows = []
    for label, count in sorted(semantic_counts.items()):
        interval = wilson_interval(count, eligible_n)
        semantic_rows.append({
            "semantic_fidelity_label": label,
            "count": count,
            "eligible_test_denominator": eligible_n,
            "rate": count / eligible_n if eligible_n else None,
            "wilson_95_lower": interval[0] if interval else None,
            "wilson_95_upper": interval[1] if interval else None,
            "end_to_end_verified_success": None,
            "end_to_end_missing": eligible_n,
            "note": "fixed-theorem repair outcomes are reported separately; end-to-end outcome is unavailable unless raw run artifacts record it",
        })
    _write_csv(output_dir / "semantic_fidelity.csv", semantic_rows, ["semantic_fidelity_label", "count", "eligible_test_denominator", "rate", "wilson_95_lower", "wilson_95_upper", "end_to_end_verified_success", "end_to_end_missing", "note"])

    qualitative = []
    for problem_id, run in run_by_problem.items():
        conditions = run.get("conditions", {})
        c = conditions.get("C", {}) if isinstance(conditions, dict) else {}
        for attempt in c.get("attempts", []) if isinstance(c, dict) else []:
            if not isinstance(attempt, dict):
                continue
            diagnostics = attempt.get("compiler_diagnostics_supplied_text")
            previous, candidate = attempt.get("previous_candidate_text"), attempt.get("candidate_text")
            if isinstance(diagnostics, str) and isinstance(previous, str) and isinstance(candidate, str):
                qualitative.append({"problem_id": problem_id, "attempt_id": attempt.get("attempt_id"), "diagnostic": diagnostics, "previous_candidate": previous, "candidate_after_repair": candidate, "verification_status": attempt.get("status")})
    (output_dir / "qualitative_examples.json").write_text(json.dumps(qualitative, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    audit = {
        "schema_version": SCHEMA_VERSION,
        "status": "complete_with_incomplete_runs" if malformed or set(eligible_ids) - set(run_by_problem) or any(run.get("status") != "completed" for run in paired_runs) else "complete",
        "eligible_test_problem_count": eligible_n,
        "paired_api_run_count": len(paired_runs),
        "missing_test_problem_ids": sorted(set(eligible_ids) - set(run_by_problem)),
        "incomplete_or_failed_run_ids": [run.get("experiment_id") for run in paired_runs if run.get("status") != "completed"],
        "malformed_run_artifacts": malformed,
        "excluded_non_api_run_count": len(excluded_mode_runs),
        "excluded_non_api_run_modes": dict(Counter(str(run.get("execution_mode")) for run in excluded_mode_runs)),
        "repeated_runs_policy": "one replicate per problem required; repeated runs block analysis rather than being counted as independent problems",
        "missing_outcomes_policy": "full eligible denominator with missing as failure; complete-case exact McNemar also reported",
        "first_attempt_success_definition": "shared fixed-theorem initial candidate verifier success, counted once per problem",
        "semantic_fidelity_is_separate": True,
        "end_to_end_success_available": False,
    }
    (output_dir / "run_audit.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    source_artifacts = [test_path, development_path, freeze_manifest_path]
    if runs_dir.exists():
        source_artifacts.extend(path for path in runs_dir.rglob("*") if path.is_file())
    source_artifacts.extend(Path(item["path"]) for item in malformed if Path(item["path"]).is_file())
    analysis_manifest = {
        "analysis_schema_version": SCHEMA_VERSION,
        "analysis_script": str(Path(__file__).relative_to(REPOSITORY_ROOT)),
        "analysis_script_sha256": sha256_file(Path(__file__)),
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "dataset_version": freeze_manifest.get("dataset_version"),
        "development_sha256": dev_hash,
        "test_sha256": test_hash,
        "protocol_hashes": sorted(protocol_hashes),
        "configuration_hashes": sorted(config_hashes),
        "source_artifact_hashes": {str(path): sha256_file(path) for path in sorted(set(source_artifacts))},
        "statistics": {"wilson_confidence": 0.95, "paired_bootstrap_resamples": BOOTSTRAP_RESAMPLES, "paired_bootstrap_seed": BOOTSTRAP_SEED, "mcnemar": "two-sided exact; complete pairs only", "holm_comparisons": [f"{a}_over_{b}" for a, b in COMPARISONS], "category_minimum_n": CATEGORY_MIN_N},
        "outputs": ["dataset_composition.csv", "success_by_repair_budget.csv", "success_by_repair_budget.svg", "paired_comparisons.csv", "resource_metrics.csv", "error_taxonomy.csv", "semantic_fidelity.csv", "qualitative_examples.json", "run_audit.json"],
    }
    output_artifacts = sorted(
        path for path in output_dir.iterdir()
        if path.is_file() and path.name != "analysis_manifest.json"
    )
    analysis_manifest["output_artifact_hashes"] = {
        path.name: sha256_file(path) for path in output_artifacts
    }
    (output_dir / "analysis_manifest.json").write_text(json.dumps(analysis_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return audit


def audit_current_repository(output_dir: Path) -> dict[str, Any]:
    """Write a readiness audit only; never turn legacy runs into study findings."""
    draft_manifest_path = REPOSITORY_ROOT / "data/research_dataset_manifest_v0.1.0.json"
    draft_manifest = load_json(draft_manifest_path)
    paired_runs, malformed = load_run_manifests(REPOSITORY_ROOT / "data/experiments")
    legacy_run_paths = sorted((REPOSITORY_ROOT / "data/results/pilots").glob("*.run.json"))
    legacy = []
    for path in legacy_run_paths:
        value = load_json(path)
        legacy.append({"path": str(path.relative_to(REPOSITORY_ROOT)), "sha256": sha256_file(path), "schema_version": value.get("schema_version"), "status": value.get("status"), "execution_mode": value.get("execution_mode", "not_recorded"), "has_paired_conditions": isinstance(value.get("conditions"), dict) and all(k in value["conditions"] for k in CONDITIONS)})
    legacy_jsonl = []
    for path in sorted((REPOSITORY_ROOT / "data/results").rglob("*.jsonl")):
        lines = path.read_text(encoding="utf-8").splitlines()
        nonempty = [line for line in lines if line.strip()]
        malformed_lines = 0
        for line in nonempty:
            try:
                json.loads(line)
            except json.JSONDecodeError:
                malformed_lines += 1
        legacy_jsonl.append({
            "path": str(path.relative_to(REPOSITORY_ROOT)),
            "sha256": sha256_file(path),
            "nonempty_record_lines": len(nonempty),
            "malformed_lines": malformed_lines,
        })
    draft_records = load_json(REPOSITORY_ROOT / "data/research_dataset_draft_v0.1.0.json")
    batch_records: list[dict[str, Any]] = []
    for path in sorted((REPOSITORY_ROOT / "data/curation_batches").glob("*/candidate_records.json")):
        value = load_json(path)
        if isinstance(value, list):
            batch_records.extend(value)
    total_candidates = len(draft_records) + len(batch_records) if isinstance(draft_records, list) else None
    result = {
        "analysis_status": "blocked_no_frozen_dataset_or_paired_api_runs",
        "frozen_dataset_manifest_status": draft_manifest.get("status"),
        "draft_candidate_count": len(draft_records) if isinstance(draft_records, list) else None,
        "acquisition_batch_candidate_count": len(batch_records),
        "all_current_candidate_count": total_candidates,
        "draft_eligible_count": draft_manifest.get("eligible_record_count"),
        "draft_eligible_split_counts": draft_manifest.get("eligible_split_counts"),
        "paired_experiment_manifests_found": len(paired_runs),
        "legacy_pipeline_run_manifests": legacy,
        "legacy_jsonl_artifacts": legacy_jsonl,
        "legacy_jsonl_record_line_count": sum(item["nonempty_record_lines"] for item in legacy_jsonl),
        "legacy_runs_used_as_paired_results": 0,
        "malformed_paired_manifests": malformed,
        "metrics_computed": False,
        "study_tables_or_figure_generated": False,
        "blockers": [
            "The research dataset manifest is draft and declares zero eligible records.",
            "No saved manifests matching the paired A/B/C experiment schema were found under data/experiments.",
            "Existing pilot manifests are legacy pipeline runs without execution_mode and paired conditions; they are excluded, not treated as API model pass@1.",
        ],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "analysis_readiness_v0.1.0.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--test-dataset", type=Path)
    parser.add_argument("--development-dataset", type=Path)
    parser.add_argument("--freeze-manifest", type=Path)
    parser.add_argument("--runs-dir", type=Path, default=REPOSITORY_ROOT / "data/experiments")
    parser.add_argument("--output-dir", type=Path, default=REPOSITORY_ROOT / "data/analysis")
    parser.add_argument("--audit-current", action="store_true", help="write only a repository readiness audit; no study metrics")
    args = parser.parse_args(argv)
    if args.audit_current:
        print(json.dumps(audit_current_repository(args.output_dir), indent=2))
        return
    if not args.test_dataset or not args.development_dataset or not args.freeze_manifest:
        parser.error("--test-dataset, --development-dataset, and --freeze-manifest are required unless --audit-current is used")
    try:
        result = analyze_frozen(
            test_path=args.test_dataset,
            development_path=args.development_dataset,
            freeze_manifest_path=args.freeze_manifest,
            runs_dir=args.runs_dir,
            output_dir=args.output_dir,
        )
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

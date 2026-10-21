from __future__ import annotations

import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "eval"))

import paired_analysis as analysis


def run_fixture(
    problem_id: str,
    *,
    status: str = "completed",
    outcomes: dict[str, list[bool | None]] | None = None,
    token_counts: dict[str, int | None] | None = None,
) -> dict:
    outcomes = outcomes or {"A": [False], "B": [False, True], "C": [False, True]}
    token_counts = token_counts or {"initial": 10, "repair": 5}
    conditions = {}
    for name in "ABC":
        values = outcomes.get(name)
        if values is None:
            continue
        milestones = {
            str(i): {"success": value, "repair_calls": i}
            for i, value in enumerate(values)
            if value is not None
        }
        conditions[name] = {
            "status": "success" if any(v is True for v in values) else "repair_budget_exhausted",
            "repair_calls_made": max(0, len(values) - 1),
            "milestones": milestones,
            "attempts": [
                {
                    "completion_metadata": {"total_tokens": token_counts.get("repair")},
                    "wall_clock_seconds": 2.0,
                }
                for _ in range(max(0, len(values) - 1))
            ],
        }
    initial = outcomes.get("A", [None])[0]
    return {
        "experiment_type": "paired_compiler_guided_repair",
        "experiment_id": f"run-{problem_id}",
        "problem_id": problem_id,
        "execution_mode": "api",
        "status": status,
        "dataset_sha256": "d" * 64,
        "protocol": {"sha256": "p" * 64},
        "configuration_sha256": "c" * 64,
        "initial_verification": {"success": initial},
        "initial_candidate": {
            "completion_metadata": {"total_tokens": token_counts.get("initial")},
            "wall_clock_seconds": 1.0,
        },
        "wall_clock_seconds": 8.0,
        "conditions": conditions,
    }


def test_wilson_interval_known_values_and_empty_denominator() -> None:
    interval = analysis.wilson_interval(5, 10)
    assert interval is not None
    assert interval[0] == pytest.approx(0.2366, abs=0.001)
    assert interval[1] == pytest.approx(0.7634, abs=0.001)
    assert analysis.wilson_interval(0, 0) is None


def test_exact_mcnemar_and_holm_correction() -> None:
    assert analysis.exact_mcnemar_p(5, 0) == pytest.approx(0.0625)
    assert analysis.exact_mcnemar_p(0, 0) is None
    assert analysis.holm_adjust([0.01, 0.03, None]) == [0.03, 0.06, None]


def test_problem_level_bootstrap_is_seeded_and_handles_empty_pairs() -> None:
    first = analysis.paired_bootstrap_interval([1.0, 0.0, -1.0], resamples=1000, seed=17)
    second = analysis.paired_bootstrap_interval([1.0, 0.0, -1.0], resamples=1000, seed=17)
    assert first == second
    assert first is not None
    assert analysis.paired_bootstrap_interval([]) is None


def test_paired_comparison_uses_complete_pairs_for_mcnemar_and_full_denominator_sensitivity() -> None:
    summary = analysis.paired_comparison_summary(
        [True, False, None, True],
        [False, True, True, True],
    )
    assert summary["first_only"] == 1
    assert summary["second_only"] == 1
    assert summary["complete_pairs"] == 3
    assert summary["missing_pairs"] == 1
    assert summary["eligible_denominator"] == 4
    assert summary["absolute_difference_missing_as_failure"] == pytest.approx(-0.25)
    assert summary["mcnemar_p"] == 1.0
    with pytest.raises(ValueError, match="equal length"):
        analysis.paired_comparison_summary([True], [True, False])


def test_budget_success_handles_success_failure_and_incomplete_milestones() -> None:
    condition = {
        "status": "repair_budget_exhausted",
        "milestones": {"0": {"success": False}, "1": {"success": True}},
    }
    assert analysis.success_at_budget(condition, 0) is False
    assert analysis.success_at_budget(condition, 1) is True
    assert analysis.success_at_budget(condition, 3) is True
    assert analysis.success_at_budget({"status": "incomplete", "milestones": {}}, 3) is None
    assert analysis.success_at_budget(
        {"status": "provider_error", "milestones": {"0": {"success": False}}}, 3
    ) is None
    assert analysis.success_at_budget(None, 3) is None
    assert analysis.first_attempt_success(
        {"initial_verification": {"success": False, "status": "timeout"}}
    ) is None


def test_fixture_covers_unpaired_and_missing_token_counts() -> None:
    run = run_fixture(
        "p1",
        outcomes={"A": [False], "B": [False, True]},
        token_counts={"initial": None, "repair": 4},
    )
    assert analysis.first_attempt_success(run) is False
    assert analysis.success_at_budget(run["conditions"]["B"], 1) is True
    assert analysis.success_at_budget(run["conditions"].get("C"), 1) is None
    assert run["initial_candidate"]["completion_metadata"]["total_tokens"] is None


def test_load_manifests_keeps_incomplete_runs_and_records_malformed_files() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "incomplete.json").write_text(json.dumps(run_fixture("p1", status="running")))
        (root / "malformed.json").write_text("{bad json")
        runs, errors = analysis.load_run_manifests(root)
    assert len(runs) == 1
    assert runs[0]["status"] == "running"
    assert len(errors) == 1
    assert "cannot read JSON" in errors[0]["error"]


def test_repeated_problem_runs_are_detected_not_counted_as_independent() -> None:
    run = run_fixture("p1")
    duplicated = [run, dict(run, experiment_id="run-p1-seed2")]
    repeated = analysis.repeated_problem_runs(duplicated)
    assert list(repeated) == ["p1"]
    assert len(repeated["p1"]) == 2


def test_empty_and_sparse_error_categories_are_classified_descriptively() -> None:
    assert analysis.classify_compiler_error("unknown identifier 'foo'") == (
        "unknown_identifier_or_name"
    )
    assert analysis.classify_compiler_error("odd diagnostic") == "other_compiler_error"
    assert analysis.CATEGORY_MIN_N == 5


def test_current_repository_audit_does_not_emit_fake_metrics(tmp_path: Path) -> None:
    report = analysis.audit_current_repository(tmp_path)
    assert report["analysis_status"].startswith("blocked")
    assert report["all_current_candidate_count"] == 31
    assert report["draft_eligible_count"] == 0
    assert report["paired_experiment_manifests_found"] == 0
    assert report["metrics_computed"] is False
    assert report["study_tables_or_figure_generated"] is False
    assert (tmp_path / "analysis_readiness_v0.1.0.json").is_file()

from __future__ import annotations

import hashlib
import os
import sys
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import llm_client
import repair_experiment
from cost_guard import (
    CostGuardConfig,
    CostGuardConfigurationError,
    CostReservationError,
    CostReservationGuard,
)


def config(**overrides: object) -> CostGuardConfig:
    values: dict[str, object] = {
        "model_id": "openai/gpt-oss-120b",
        "input_usd_per_million_tokens": Decimal("1"),
        "output_usd_per_million_tokens": Decimal("2"),
        "max_input_tokens": 100,
        "max_output_tokens": 20,
        "input_overhead_token_bound": 4,
        "max_cost_per_http_attempt_usd": Decimal("0.0002"),
        "per_problem_budget_usd": Decimal("0.01"),
        "total_budget_usd": Decimal("0.01"),
        "wrapper_attempts_per_completion": 3,
        "sdk_max_retries_per_wrapper_attempt": 2,
        "pricing_source_url": "https://console.groq.com/docs/models",
        "pricing_retrieved_on": "2026-10-21",
        "pricing_currency": "USD",
        "pricing_review_status": "human_reviewed",
        "pricing_reviewed_on": "2026-10-21",
        "pricing_reviewer_id": "test-fixture-reviewer",
        "pricing_evidence_path": "test-fixture",
        "pricing_evidence_sha256": "a" * 64,
        "input_bound_review_status": "human_reviewed",
        "input_bound_reviewed_on": "2026-10-21",
        "input_bound_reviewer_id": "test-fixture-reviewer",
        "input_bound_evidence": "synthetic test fixture; no real bound asserted",
    }
    values.update(overrides)
    return CostGuardConfig(**values)  # type: ignore[arg-type]


def test_environment_configuration_fails_closed_when_pricing_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in tuple(os.environ):
        if name.startswith("GROQ_COST_"):
            monkeypatch.delenv(name, raising=False)

    with pytest.raises(CostGuardConfigurationError, match="GROQ_COST_INPUT"):
        CostGuardConfig.from_environment(
            model_id="openai/gpt-oss-120b",
            wrapper_attempts_per_completion=3,
            sdk_max_retries_per_wrapper_attempt=2,
        )


def test_api_stays_blocked_even_with_complete_declared_cost_configuration(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    evidence = tmp_path / "official-pricing-evidence.html"
    evidence.write_text("test fixture only; not actual Groq pricing", encoding="utf-8")
    evidence_sha256 = hashlib.sha256(evidence.read_bytes()).hexdigest()
    settings = {
        "GROQ_COST_INPUT_USD_PER_MILLION_TOKENS": "0.01",
        "GROQ_COST_OUTPUT_USD_PER_MILLION_TOKENS": "0.01",
        "GROQ_COST_MAX_INPUT_TOKENS": "2500",
        "GROQ_COST_MAX_OUTPUT_TOKENS": "2000",
        "GROQ_COST_INPUT_OVERHEAD_TOKEN_BOUND": "128",
        "GROQ_COST_MAX_PER_HTTP_ATTEMPT_USD": "0.00005",
        "GROQ_COST_PER_PROBLEM_BUDGET_USD": "0.10",
        "GROQ_COST_TOTAL_BUDGET_USD": "0.10",
        "GROQ_COST_PRICING_SOURCE_URL": "https://groq.com/pricing",
        "GROQ_COST_PRICING_MODEL_ID": "openai/gpt-oss-120b",
        "GROQ_COST_PRICING_RETRIEVED_ON": "2026-10-21",
        "GROQ_COST_PRICING_CURRENCY": "USD",
        "GROQ_COST_PRICING_REVIEW_STATUS": "human_reviewed",
        "GROQ_COST_PRICING_REVIEWED_ON": "2026-10-21",
        "GROQ_COST_PRICING_REVIEWER_ID": "test-fixture-reviewer",
        "GROQ_COST_PRICING_EVIDENCE_PATH": str(evidence),
        "GROQ_COST_PRICING_EVIDENCE_SHA256": evidence_sha256,
        "GROQ_COST_INPUT_BOUND_REVIEW_STATUS": "human_reviewed",
        "GROQ_COST_INPUT_BOUND_REVIEWED_ON": "2026-10-21",
        "GROQ_COST_INPUT_BOUND_REVIEWER_ID": "test-fixture-reviewer",
        "GROQ_COST_INPUT_BOUND_EVIDENCE": "synthetic test fixture only",
    }
    for name, value in settings.items():
        monkeypatch.setenv(name, value)
    output_root = tmp_path / "never-created"
    client_factory = Mock(side_effect=AssertionError("API client must not be created"))

    with (
        patch.object(llm_client, "_get_client", client_factory),
        pytest.raises(ValueError, match="API execution remains disabled"),
    ):
        repair_experiment.run_experiment(
            "problem_001",
            "theorem target : True := by sorry",
            tmp_path / "lean_project",
            output_root,
            execution_mode="api",
        )

    client_factory.assert_not_called()
    assert not output_root.exists()


@pytest.mark.parametrize(
    "field,value",
    [
        ("input_usd_per_million_tokens", Decimal("-0.1")),
        ("output_usd_per_million_tokens", Decimal("NaN")),
        ("input_usd_per_million_tokens", Decimal("Infinity")),
        ("per_problem_budget_usd", Decimal("-1")),
        ("total_budget_usd", Decimal("NaN")),
        ("max_input_tokens", 0),
        ("max_output_tokens", -1),
        ("input_overhead_token_bound", -1),
    ],
)
def test_invalid_rates_budgets_and_token_bounds_fail_closed(
    field: str, value: object
) -> None:
    with pytest.raises(CostGuardConfigurationError):
        config(**{field: value})


def test_invalid_pricing_source_or_model_evidence_fails_closed() -> None:
    with pytest.raises(CostGuardConfigurationError, match="official HTTPS"):
        config(pricing_source_url="https://example.com/pricing")
    with pytest.raises(CostGuardConfigurationError, match="SHA-256"):
        config(pricing_evidence_sha256="not-a-hash")
    with pytest.raises(CostGuardConfigurationError, match="human_reviewed"):
        config(pricing_review_status="unreviewed")
    with pytest.raises(CostGuardConfigurationError, match="currency must be USD"):
        config(pricing_currency="EUR")
    with pytest.raises(CostGuardConfigurationError, match="input_bound_review_status"):
        config(input_bound_review_status="pending")


def test_attempt_rate_limit_must_cover_the_conservative_estimate() -> None:
    with pytest.raises(CostGuardConfigurationError, match="estimate exceeds"):
        config(max_cost_per_http_attempt_usd=Decimal("0.000001"))


def test_input_and_output_token_overflow_are_rejected_before_request() -> None:
    guard = CostReservationGuard(config(), persist_snapshot=lambda _snapshot: None)

    with pytest.raises(CostReservationError, match="input-token"):
        guard.reserve_wrapper_attempt(
            "x" * 97,
            requested_output_tokens=20,
            wrapper_attempt_number=1,
        )
    with pytest.raises(CostReservationError, match="output token"):
        guard.reserve_wrapper_attempt(
            "short",
            requested_output_tokens=21,
            wrapper_attempt_number=1,
        )


def test_model_must_match_pricing_evidence_before_client_use() -> None:
    client = Mock()
    with (
        patch.object(llm_client, "_client", client),
        patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}),
        pytest.raises(ValueError, match="does not match"),
    ):
        llm_client.complete_with_metadata(
            "prompt",
            max_tokens=20,
            model="different-model",
            cost_guard=CostReservationGuard(
                config(), persist_snapshot=lambda _snapshot: None
            ),
        )

    client.chat.completions.create.assert_not_called()


def test_one_wrapper_reserves_each_possible_sdk_http_attempt() -> None:
    guard = CostReservationGuard(config(), persist_snapshot=lambda _snapshot: None)

    reservation = guard.reserve_wrapper_attempt(
        "short",
        requested_output_tokens=20,
        wrapper_attempt_number=1,
    )

    assert reservation["reserved_http_attempts"] == 3
    snapshot = guard.snapshot()
    assert len(snapshot["reservations"]) == 3
    assert all(
        item["may_have_been_billed"] is True
        for item in snapshot["reservations"]
    )


def test_reservation_is_persisted_before_each_transmission() -> None:
    events: list[str] = []
    guard = CostReservationGuard(
        config(),
        persist_snapshot=lambda snapshot: events.append(
            str(snapshot["reservations"][-1]["status"])
        ),
    )
    client = Mock()
    client.chat.completions.create.side_effect = lambda **_kwargs: (
        events.append("http_transmission") or llm_client_test_response()
    )

    with (
        patch.object(llm_client, "_client", client),
        patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}),
    ):
        llm_client.complete_with_metadata(
            "prompt",
            max_tokens=20,
            model="openai/gpt-oss-120b",
            cost_guard=guard,
            sleep=lambda _delay: None,
        )

    assert events[0] == "reserved_before_transmission"
    assert events[1] == "http_transmission"
    statuses = [item["status"] for item in guard.snapshot()["reservations"]]
    assert statuses == [
        "response_received_at_least_one_unknown",
        "unused_or_ambiguous_may_be_billed",
        "unused_or_ambiguous_may_be_billed",
    ]


def test_failed_reservation_persistence_prevents_client_transmission() -> None:
    def fail_persist(_snapshot: dict[str, object]) -> None:
        raise OSError("reservation store unavailable")

    guard = CostReservationGuard(config(), persist_snapshot=fail_persist)
    client = Mock()
    with (
        patch.object(llm_client, "_get_client", return_value=client),
        patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}),
        pytest.raises(OSError, match="reservation store unavailable"),
    ):
        llm_client.complete_with_metadata(
            "prompt", max_tokens=20, model="openai/gpt-oss-120b", cost_guard=guard
        )

    client.chat.completions.create.assert_not_called()


def llm_client_test_response() -> SimpleNamespace:
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="proof"))]
    )


def test_unpersisted_or_missing_guard_blocks_before_client_use() -> None:
    client = Mock()
    with (
        patch.object(llm_client, "_get_client", return_value=client) as get_client,
        pytest.raises(CostReservationError, match="persisted cost guard"),
    ):
        llm_client.complete_with_metadata("prompt")

    get_client.assert_not_called()
    client.chat.completions.create.assert_not_called()

    unpersisted = CostReservationGuard(config())
    with (
        patch.object(llm_client, "_get_client", return_value=client) as get_client,
        pytest.raises(CostReservationError, match="must persist reservations"),
    ):
        llm_client.complete_with_metadata("prompt", cost_guard=unpersisted)

    get_client.assert_not_called()


def test_sdk_retry_mismatch_blocks_before_client_use() -> None:
    guard = CostReservationGuard(
        config(sdk_max_retries_per_wrapper_attempt=1),
        persist_snapshot=lambda _snapshot: None,
    )
    client = Mock()
    with (
        patch.object(llm_client, "_get_client", return_value=client) as get_client,
        pytest.raises(ValueError, match="SDK retry count does not match"),
    ):
        llm_client.complete_with_metadata("prompt", cost_guard=guard)

    get_client.assert_not_called()
    client.chat.completions.create.assert_not_called()


def test_budget_exhaustion_rejects_before_next_wrapper_transmission() -> None:
    class FakeRateLimitError(Exception):
        pass

    estimate = config().estimated_http_attempt_cost_usd
    guarded = CostReservationGuard(
        config(
            per_problem_budget_usd=estimate * 3,
            total_budget_usd=estimate * 3,
        ),
        persist_snapshot=lambda _snapshot: None,
    )
    client = Mock()
    client.chat.completions.create.side_effect = FakeRateLimitError("rate limit")

    with (
        patch.object(llm_client, "_client", client),
        patch.object(llm_client.groq, "RateLimitError", FakeRateLimitError),
        patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}),
        pytest.raises(CostReservationError, match="Insufficient remaining budget"),
    ):
        llm_client.complete_with_metadata(
            "prompt",
            max_tokens=20,
            retries=3,
            model="openai/gpt-oss-120b",
            cost_guard=guarded,
            sleep=lambda _delay: None,
        )

    assert client.chat.completions.create.call_count == 1
    assert len(guarded.snapshot()["reservations"]) == 3


def test_transport_retries_reserve_wrapper_and_sdk_attempts() -> None:
    class FakeRateLimitError(Exception):
        pass

    guarded = CostReservationGuard(config(), persist_snapshot=lambda _snapshot: None)
    client = Mock()
    client.chat.completions.create.side_effect = FakeRateLimitError("rate limit")

    with (
        patch.object(llm_client, "_client", client),
        patch.object(llm_client.groq, "RateLimitError", FakeRateLimitError),
        patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}),
        pytest.raises(RuntimeError, match="after 3 attempts"),
    ):
        llm_client.complete_with_metadata(
            "prompt",
            max_tokens=20,
            retries=3,
            model="openai/gpt-oss-120b",
            cost_guard=guarded,
            sleep=lambda _delay: None,
        )

    assert client.chat.completions.create.call_count == 3
    snapshot = guarded.snapshot()
    assert len(snapshot["reservations"]) == 9
    assert snapshot["reserved_per_problem_usd"] == str(
        config().estimated_http_attempt_cost_usd * 9
    )
    assert all(
        item["status"] == "ambiguous_may_be_billed"
        for item in snapshot["reservations"]
    )


def test_ambiguous_timeout_keeps_reservations_and_stops_before_budget_overrun() -> None:
    estimate = config().estimated_http_attempt_cost_usd
    persisted_snapshots: list[dict[str, object]] = []
    guarded = CostReservationGuard(
        config(
            per_problem_budget_usd=estimate * 3,
            total_budget_usd=estimate * 3,
        ),
        persist_snapshot=persisted_snapshots.append,
    )
    client = Mock()
    client.chat.completions.create.side_effect = TimeoutError("request timed out")

    with (
        patch.object(llm_client, "_client", client),
        patch.dict(os.environ, {"GROQ_API_KEY": "test-key"}),
        pytest.raises(TimeoutError),
    ):
        llm_client.complete_with_metadata(
            "prompt",
            max_tokens=20,
            retries=3,
            model="openai/gpt-oss-120b",
            cost_guard=guarded,
            sleep=lambda _delay: None,
        )

    snapshot = guarded.snapshot()
    assert client.chat.completions.create.call_count == 1
    assert len(snapshot["reservations"]) == 3
    assert all(
        item["status"] == "ambiguous_may_be_billed"
        and item["may_have_been_billed"] is True
        for item in snapshot["reservations"]
    )
    assert persisted_snapshots[0]["reservations"][0]["status"] == (
        "reserved_before_transmission"
    )
    assert persisted_snapshots[-1]["reservations"][0]["status"] == (
        "ambiguous_may_be_billed"
    )

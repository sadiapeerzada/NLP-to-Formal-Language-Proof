from __future__ import annotations

import hashlib
import os
import sys
from decimal import Decimal
from pathlib import Path
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
        "pricing_verified_at_utc": "2026-10-21T12:00:00Z",
        "pricing_evidence_path": "test-fixture",
        "pricing_evidence_sha256": "a" * 64,
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
        "GROQ_COST_PRICING_VERIFIED_AT_UTC": "2026-10-21T12:00:00Z",
        "GROQ_COST_PRICING_EVIDENCE_PATH": str(evidence),
        "GROQ_COST_PRICING_EVIDENCE_SHA256": evidence_sha256,
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


def test_attempt_rate_limit_must_cover_the_conservative_estimate() -> None:
    with pytest.raises(CostGuardConfigurationError, match="estimate exceeds"):
        config(max_cost_per_http_attempt_usd=Decimal("0.000001"))


def test_input_and_output_token_overflow_are_rejected_before_request() -> None:
    guard = CostReservationGuard(config())

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
            cost_guard=CostReservationGuard(config()),
        )

    client.chat.completions.create.assert_not_called()


def test_one_wrapper_reserves_each_possible_sdk_http_attempt() -> None:
    guard = CostReservationGuard(config())

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


def test_budget_exhaustion_rejects_before_next_wrapper_transmission() -> None:
    class FakeRateLimitError(Exception):
        pass

    estimate = config().estimated_http_attempt_cost_usd
    guarded = CostReservationGuard(
        config(
            per_problem_budget_usd=estimate * 3,
            total_budget_usd=estimate * 3,
        )
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

    guarded = CostReservationGuard(config())
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

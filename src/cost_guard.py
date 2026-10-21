"""Fail-closed token-based cost reservations for Groq completions."""
from __future__ import annotations

import hashlib
import os
import re
import threading
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse


MILLION = Decimal(1_000_000)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class CostGuardConfigurationError(ValueError):
    """Raised when cost guard configuration is absent or invalid."""


class CostReservationError(RuntimeError):
    """Raised before transmission when an attempt cannot be reserved."""


def _positive_int(name: str, value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CostGuardConfigurationError(f"{name} must be a positive integer.")
    return value


def _non_negative_int(name: str, value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise CostGuardConfigurationError(
            f"{name} must be a non-negative integer."
        )
    return value


def _positive_decimal(name: str, value: object) -> Decimal:
    if isinstance(value, bool):
        raise CostGuardConfigurationError(f"{name} must be a finite positive number.")
    try:
        parsed = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise CostGuardConfigurationError(
            f"{name} must be a finite positive number."
        ) from None
    if not parsed.is_finite() or parsed <= 0:
        raise CostGuardConfigurationError(f"{name} must be a finite positive number.")
    return parsed


def _required_environment(name: str) -> str:
    value = os.environ.get(name)
    if value is None or not value.strip():
        raise CostGuardConfigurationError(
            f"Required cost guard setting {name} is missing."
        )
    return value.strip()


@dataclass(frozen=True)
class CostGuardConfig:
    model_id: str
    input_usd_per_million_tokens: Decimal
    output_usd_per_million_tokens: Decimal
    max_input_tokens: int
    max_output_tokens: int
    input_overhead_token_bound: int
    max_cost_per_http_attempt_usd: Decimal
    per_problem_budget_usd: Decimal
    total_budget_usd: Decimal
    wrapper_attempts_per_completion: int
    sdk_max_retries_per_wrapper_attempt: int
    pricing_source_url: str
    pricing_verified_at_utc: str
    pricing_evidence_path: str
    pricing_evidence_sha256: str

    def __post_init__(self) -> None:
        if not isinstance(self.model_id, str) or not self.model_id.strip():
            raise CostGuardConfigurationError("model_id must be a non-empty string.")
        for name in (
            "input_usd_per_million_tokens",
            "output_usd_per_million_tokens",
            "max_cost_per_http_attempt_usd",
            "per_problem_budget_usd",
            "total_budget_usd",
        ):
            object.__setattr__(
                self, name, _positive_decimal(name, getattr(self, name))
            )
        for name in ("max_input_tokens", "max_output_tokens"):
            _positive_int(name, getattr(self, name))
        for name in (
            "input_overhead_token_bound",
            "sdk_max_retries_per_wrapper_attempt",
        ):
            _non_negative_int(name, getattr(self, name))
        _positive_int(
            "wrapper_attempts_per_completion",
            self.wrapper_attempts_per_completion,
        )
        parsed_url = urlparse(self.pricing_source_url)
        if (
            parsed_url.scheme != "https"
            or parsed_url.hostname
            not in {"groq.com", "www.groq.com", "console.groq.com"}
            or parsed_url.username is not None
            or parsed_url.password is not None
            or parsed_url.query
            or parsed_url.fragment
        ):
            raise CostGuardConfigurationError(
                "pricing_source_url must reference an official HTTPS Groq domain."
            )
        if self.pricing_verified_at_utc:
            try:
                verified_at = datetime.fromisoformat(
                    self.pricing_verified_at_utc.replace("Z", "+00:00")
                )
            except ValueError:
                raise CostGuardConfigurationError(
                    "pricing_verified_at_utc must be an ISO-8601 timestamp."
                ) from None
            if verified_at.tzinfo is None:
                raise CostGuardConfigurationError(
                    "pricing_verified_at_utc must include a timezone."
                )
        else:
            raise CostGuardConfigurationError(
                "pricing_verified_at_utc must be a non-empty ISO-8601 timestamp."
            )
        if not SHA256_RE.fullmatch(self.pricing_evidence_sha256):
            raise CostGuardConfigurationError(
                "pricing_evidence_sha256 must be a lowercase SHA-256 digest."
            )
        if (
            not isinstance(self.pricing_evidence_path, str)
            or not self.pricing_evidence_path.strip()
        ):
            raise CostGuardConfigurationError(
                "pricing_evidence_path must be a non-empty archived evidence path."
            )
        if self.estimated_http_attempt_cost_usd > self.max_cost_per_http_attempt_usd:
            raise CostGuardConfigurationError(
                "The worst-case request estimate exceeds "
                "max_cost_per_http_attempt_usd."
            )
        if self.per_problem_budget_usd > self.total_budget_usd:
            raise CostGuardConfigurationError(
                "per_problem_budget_usd cannot exceed total_budget_usd."
            )

    @property
    def estimated_http_attempt_cost_usd(self) -> Decimal:
        token_cost = (
            self.max_input_tokens * self.input_usd_per_million_tokens
            + self.max_output_tokens * self.output_usd_per_million_tokens
        )
        return token_cost / MILLION

    @property
    def max_http_attempts_per_completion(self) -> int:
        return self.wrapper_attempts_per_completion * (
            self.sdk_max_retries_per_wrapper_attempt + 1
        )

    @classmethod
    def from_environment(
        cls,
        *,
        model_id: str,
        wrapper_attempts_per_completion: int,
        sdk_max_retries_per_wrapper_attempt: int,
    ) -> CostGuardConfig:
        required = {
            "GROQ_COST_INPUT_USD_PER_MILLION_TOKENS": "input_usd_per_million_tokens",
            "GROQ_COST_OUTPUT_USD_PER_MILLION_TOKENS": "output_usd_per_million_tokens",
            "GROQ_COST_MAX_INPUT_TOKENS": "max_input_tokens",
            "GROQ_COST_MAX_OUTPUT_TOKENS": "max_output_tokens",
            "GROQ_COST_INPUT_OVERHEAD_TOKEN_BOUND": "input_overhead_token_bound",
            "GROQ_COST_MAX_PER_HTTP_ATTEMPT_USD": "max_cost_per_http_attempt_usd",
            "GROQ_COST_PER_PROBLEM_BUDGET_USD": "per_problem_budget_usd",
            "GROQ_COST_TOTAL_BUDGET_USD": "total_budget_usd",
            "GROQ_COST_PRICING_SOURCE_URL": "pricing_source_url",
            "GROQ_COST_PRICING_MODEL_ID": "pricing_model_id",
            "GROQ_COST_PRICING_VERIFIED_AT_UTC": "pricing_verified_at_utc",
            "GROQ_COST_PRICING_EVIDENCE_PATH": "pricing_evidence_path",
            "GROQ_COST_PRICING_EVIDENCE_SHA256": "pricing_evidence_sha256",
        }
        values = {name: _required_environment(name) for name in required}
        if values["GROQ_COST_PRICING_MODEL_ID"] != model_id:
            raise CostGuardConfigurationError(
                "Pricing evidence model ID does not exactly match the requested model."
            )
        evidence_path = Path(values["GROQ_COST_PRICING_EVIDENCE_PATH"]).expanduser()
        try:
            evidence_sha256 = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
        except OSError as error:
            raise CostGuardConfigurationError(
                "Archived pricing evidence cannot be read."
            ) from error
        if evidence_sha256 != values["GROQ_COST_PRICING_EVIDENCE_SHA256"]:
            raise CostGuardConfigurationError(
                "Pricing evidence SHA-256 does not match the archived evidence file."
            )
        int_names = {
            "GROQ_COST_MAX_INPUT_TOKENS",
            "GROQ_COST_MAX_OUTPUT_TOKENS",
            "GROQ_COST_INPUT_OVERHEAD_TOKEN_BOUND",
        }
        decimal_names = {
            "GROQ_COST_INPUT_USD_PER_MILLION_TOKENS",
            "GROQ_COST_OUTPUT_USD_PER_MILLION_TOKENS",
            "GROQ_COST_MAX_PER_HTTP_ATTEMPT_USD",
            "GROQ_COST_PER_PROBLEM_BUDGET_USD",
            "GROQ_COST_TOTAL_BUDGET_USD",
        }
        parsed: dict[str, object] = {}
        for env_name, value in values.items():
            if env_name in int_names:
                try:
                    parsed[required[env_name]] = int(value)
                except ValueError:
                    raise CostGuardConfigurationError(
                        f"{env_name} must be an integer."
                    ) from None
            elif env_name in decimal_names:
                parsed[required[env_name]] = value
            elif env_name != "GROQ_COST_PRICING_MODEL_ID":
                parsed[required[env_name]] = value
        return cls(
            model_id=model_id,
            input_usd_per_million_tokens=parsed["input_usd_per_million_tokens"],
            output_usd_per_million_tokens=parsed["output_usd_per_million_tokens"],
            max_input_tokens=parsed["max_input_tokens"],
            max_output_tokens=parsed["max_output_tokens"],
            input_overhead_token_bound=parsed["input_overhead_token_bound"],
            max_cost_per_http_attempt_usd=parsed["max_cost_per_http_attempt_usd"],
            per_problem_budget_usd=parsed["per_problem_budget_usd"],
            total_budget_usd=parsed["total_budget_usd"],
            wrapper_attempts_per_completion=wrapper_attempts_per_completion,
            sdk_max_retries_per_wrapper_attempt=sdk_max_retries_per_wrapper_attempt,
            pricing_source_url=parsed["pricing_source_url"],
            pricing_verified_at_utc=parsed["pricing_verified_at_utc"],
            pricing_evidence_path=parsed["pricing_evidence_path"],
            pricing_evidence_sha256=parsed["pricing_evidence_sha256"],
        )


class CostReservationGuard:
    """Reserve all possible SDK requests before each wrapper transmission.

    SDK-internal request counts are not observable through the current client,
    so each wrapper attempt reserves for every configured SDK attempt and never
    releases unused or ambiguous reservations.
    """

    def __init__(
        self,
        config: CostGuardConfig,
        persist_snapshot: Callable[[dict[str, object]], None] | None = None,
    ) -> None:
        self.config = config
        self._persist_snapshot = persist_snapshot
        self._lock = threading.Lock()
        self._reserved_per_problem = Decimal(0)
        self._reserved_total = Decimal(0)
        self._reservations: list[dict[str, object]] = []

    def reserve_wrapper_attempt(
        self,
        prompt: str,
        *,
        requested_output_tokens: int,
        wrapper_attempt_number: int,
    ) -> dict[str, object]:
        if not isinstance(prompt, str):
            raise CostReservationError("Prompt must be text to enforce input bounds.")
        if (
            isinstance(requested_output_tokens, bool)
            or not isinstance(requested_output_tokens, int)
            or requested_output_tokens <= 0
            or requested_output_tokens > self.config.max_output_tokens
        ):
            raise CostReservationError(
                "Requested output token limit is invalid or exceeds the configured bound."
            )
        if (
            isinstance(wrapper_attempt_number, bool)
            or not isinstance(wrapper_attempt_number, int)
            or not 1 <= wrapper_attempt_number
            <= self.config.wrapper_attempts_per_completion
        ):
            raise CostReservationError("Wrapper attempt number exceeds its configured limit.")
        try:
            input_token_upper_bound = len(prompt.encode("utf-8")) + (
                self.config.input_overhead_token_bound
            )
        except UnicodeEncodeError:
            raise CostReservationError("Prompt cannot be encoded as UTF-8.") from None
        if input_token_upper_bound > self.config.max_input_tokens:
            raise CostReservationError(
                "Prompt input-token upper bound exceeds the configured limit."
            )

        attempts_to_reserve = self.config.sdk_max_retries_per_wrapper_attempt + 1
        attempt_cost = self.config.estimated_http_attempt_cost_usd
        reservation_cost = attempt_cost * attempts_to_reserve
        with self._lock:
            if (
                self._reserved_per_problem + reservation_cost
                > self.config.per_problem_budget_usd
                or self._reserved_total + reservation_cost
                > self.config.total_budget_usd
            ):
                raise CostReservationError(
                    "Insufficient remaining budget to reserve every possible SDK HTTP attempt."
                )
            batch_id = f"wrapper-{wrapper_attempt_number}-{len(self._reservations) + 1}"
            for sdk_attempt in range(1, attempts_to_reserve + 1):
                self._reservations.append(
                    {
                        "reservation_id": f"{batch_id}-http-{sdk_attempt}",
                        "wrapper_attempt_number": wrapper_attempt_number,
                        "sdk_http_attempt_number": sdk_attempt,
                        "reserved_usd": str(attempt_cost),
                        "status": "reserved_before_transmission",
                        "may_have_been_billed": True,
                    }
                )
            self._reserved_per_problem += reservation_cost
            self._reserved_total += reservation_cost
        self._persist()
        return {
            "reservation_batch_id": batch_id,
            "reserved_http_attempts": attempts_to_reserve,
            "reserved_usd": str(reservation_cost),
            "input_token_upper_bound": input_token_upper_bound,
            "status": "reserved_before_transmission",
        }

    def record_wrapper_outcome(
        self, reservation_batch_id: str, *, outcome: str
    ) -> None:
        if outcome not in {"response_received", "ambiguous_may_be_billed"}:
            raise ValueError("Unsupported reservation outcome.")
        with self._lock:
            for reservation in self._reservations:
                if reservation["reservation_id"].startswith(
                    f"{reservation_batch_id}-http-"
                ):
                    reservation["status"] = outcome
        self._persist()

    def set_persist_callback(
        self, callback: Callable[[dict[str, object]], None]
    ) -> None:
        self._persist_snapshot = callback

    def _persist(self) -> None:
        if self._persist_snapshot is not None:
            self._persist_snapshot(self.snapshot())

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            return {
                "model_id": self.config.model_id,
                "pricing_source_url": self.config.pricing_source_url,
                "pricing_verified_at_utc": self.config.pricing_verified_at_utc,
                "pricing_evidence_path": self.config.pricing_evidence_path,
                "pricing_evidence_sha256": self.config.pricing_evidence_sha256,
                "input_usd_per_million_tokens": str(
                    self.config.input_usd_per_million_tokens
                ),
                "output_usd_per_million_tokens": str(
                    self.config.output_usd_per_million_tokens
                ),
                "max_input_tokens": self.config.max_input_tokens,
                "max_output_tokens": self.config.max_output_tokens,
                "estimated_http_attempt_cost_usd": str(
                    self.config.estimated_http_attempt_cost_usd
                ),
                "max_cost_per_http_attempt_usd": str(
                    self.config.max_cost_per_http_attempt_usd
                ),
                "per_problem_budget_usd": str(
                    self.config.per_problem_budget_usd
                ),
                "total_budget_usd": str(self.config.total_budget_usd),
                "reserved_per_problem_usd": str(self._reserved_per_problem),
                "reserved_total_usd": str(self._reserved_total),
                "reservations": [dict(item) for item in self._reservations],
            }

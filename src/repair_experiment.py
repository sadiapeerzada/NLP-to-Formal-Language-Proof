"""Controlled paired one-shot, blind-retry, and compiler-guided experiment.

Unlike the end-to-end pipeline, this runner takes a fixed Lean theorem and
generates one initial candidate shared by all three conditions.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Literal
from uuid import uuid4

import groq

from cost_guard import (
    CostGuardConfig,
    CostGuardConfigurationError,
    CostReservationGuard,
)
from llm_client import (
    CompletionResult,
    MissingGroqApiKeyError,
    SDK_MAX_RETRIES,
    complete_with_metadata,
    extract_lean_block,
    reasoning_effort_for_model,
)
from verify import VerificationResult, check_lean_file_detailed
from verify import DEFAULT_POLICY


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATHS = {
    "initial": REPOSITORY_ROOT / "prompts" / "repair_experiment_initial.txt",
    "blind": REPOSITORY_ROOT / "prompts" / "repair_experiment_blind.txt",
    "compiler_guided": (
        REPOSITORY_ROOT / "prompts" / "repair_experiment_compiler_guided.txt"
    ),
}
PROTOCOL_PATH = (
    REPOSITORY_ROOT / "configs" / "repair_experiment_protocol_v0.2.0.json"
)
INITIAL_PROMPT_TEMPLATE = PROMPT_PATHS["initial"].read_text()
BLIND_PROMPT_TEMPLATE = PROMPT_PATHS["blind"].read_text()
COMPILER_GUIDED_PROMPT_TEMPLATE = PROMPT_PATHS["compiler_guided"].read_text()
DEFAULT_MODEL = "openai/gpt-oss-120b"
MODEL_PROVIDER = "groq"
DEFAULT_MAX_REPAIRS = 3
DEFAULT_MAX_COMPLETION_TOKENS = 2000
DEFAULT_TEMPERATURE = 0.2
TRANSPORT_ATTEMPTS = 3
PILOT_BUDGET_USD = 0.10
API_EXECUTION_ENABLED = False
API_EXECUTION_BLOCKED_REASON = (
    "API execution remains disabled pending human approval, verified official "
    "model pricing, and audit of the cost guard."
)
BLIND_FEEDBACK_FIELD = "No compiler diagnostics are provided in the blind-retry condition."

CompletionFunction = Callable[..., CompletionResult]
VerificationFunction = Callable[..., VerificationResult]
ExecutionMode = Literal["api", "mock", "manual"]


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _canonical_sha256(value: object) -> str:
    serialized = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _safe_id(value: str) -> bool:
    return (
        bool(value)
        and value not in {".", ".."}
        and Path(value).name == value
        and "\\" not in value
    )


def _new_experiment_id() -> str:
    now = datetime.now(UTC)
    return f"{now:%Y%m%dT%H%M%S%fZ}-{uuid4().hex[:12]}"


def _prompt_hashes() -> dict[str, str]:
    return {
        name: hashlib.sha256(path.read_bytes()).hexdigest()
        for name, path in PROMPT_PATHS.items()
    }


def _protocol_metadata() -> dict[str, str]:
    """Validate and identify the machine-readable protocol bound to a run."""
    protocol_bytes = PROTOCOL_PATH.read_bytes()
    try:
        protocol = json.loads(protocol_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Experiment protocol is not valid JSON: {error}") from error
    if not isinstance(protocol, dict):
        raise RuntimeError("Experiment protocol must be a JSON object.")

    expected_prompt_hashes = {
        name: value.get("sha256")
        for name, value in protocol.get("prompt_templates", {}).items()
        if isinstance(value, dict)
    }
    if expected_prompt_hashes != _prompt_hashes():
        raise RuntimeError(
            "Experiment prompt files do not match the hashes in the locked protocol."
        )
    model = protocol.get("model", {})
    decoding = protocol.get("decoding", {})
    retry = protocol.get("retry_and_stopping", {})
    execution_gate = protocol.get("execution_gate", {})
    if (
        not isinstance(model, dict)
        or model.get("requested_model_id") != DEFAULT_MODEL
        or model.get("provider") != MODEL_PROVIDER
        or not isinstance(decoding, dict)
        or decoding.get("temperature") != DEFAULT_TEMPERATURE
        or decoding.get("max_completion_tokens") != DEFAULT_MAX_COMPLETION_TOKENS
        or decoding.get("reasoning_effort") != reasoning_effort_for_model(DEFAULT_MODEL)
        or not isinstance(retry, dict)
        or retry.get("maximum_wrapper_attempts_per_logical_completion")
        != TRANSPORT_ATTEMPTS
        or retry.get("maximum_groq_sdk_retries_per_wrapper_attempt")
        != SDK_MAX_RETRIES
        or protocol.get("conditions", {}).get("B", {}).get(
            "maximum_repair_calls"
        )
        != DEFAULT_MAX_REPAIRS
        or protocol.get("conditions", {}).get("C", {}).get(
            "maximum_repair_calls"
        )
        != DEFAULT_MAX_REPAIRS
        or not isinstance(execution_gate, dict)
        or execution_gate.get("api_execution_enabled") != API_EXECUTION_ENABLED
    ):
        raise RuntimeError(
            "Experiment runner settings do not match the locked protocol."
        )

    environment = protocol.get("lean_environment", {})
    expected_environment_hashes = {
        "lean-toolchain": environment.get("lean_toolchain_sha256"),
        "lake-manifest.json": environment.get("lake_manifest_sha256"),
        "lakefile.toml": environment.get("lakefile_sha256"),
    } if isinstance(environment, dict) else {}
    actual_environment_hashes = {
        "lean-toolchain": hashlib.sha256(
            (REPOSITORY_ROOT / "lean_project" / "lean-toolchain").read_bytes()
        ).hexdigest(),
        "lake-manifest.json": hashlib.sha256(
            (REPOSITORY_ROOT / "lean_project" / "lake-manifest.json").read_bytes()
        ).hexdigest(),
        "lakefile.toml": hashlib.sha256(
            (REPOSITORY_ROOT / "lean_project" / "lakefile.toml").read_bytes()
        ).hexdigest(),
    }
    if expected_environment_hashes != actual_environment_hashes:
        raise RuntimeError(
            "Lean/Mathlib project files do not match the locked protocol."
        )
    if protocol.get("proof_safety") != {
        "forbidden_source_tokens": list(DEFAULT_POLICY.prohibited_proof_tokens),
        "forbidden_declarations": list(DEFAULT_POLICY.prohibited_declarations),
        "allowed_axiom_dependencies": list(DEFAULT_POLICY.allowed_axioms),
        "lean_compilation_establishes_semantic_fidelity": False,
    }:
        raise RuntimeError(
            "Verifier proof-safety policy does not match the locked protocol."
        )
    return {
        "version": str(protocol.get("protocol_version", "")),
        "status": str(protocol.get("protocol_status", "")),
        "path": str(PROTOCOL_PATH.relative_to(REPOSITORY_ROOT)),
        "sha256": hashlib.sha256(protocol_bytes).hexdigest(),
    }


def _render_initial_prompt(theorem_statement: str) -> str:
    return INITIAL_PROMPT_TEMPLATE.format(theorem_statement=theorem_statement)


def _render_blind_prompt(
    theorem_statement: str, previous_candidate: str
) -> str:
    return BLIND_PROMPT_TEMPLATE.format(
        theorem_statement=theorem_statement,
        previous_candidate=previous_candidate,
        feedback=BLIND_FEEDBACK_FIELD,
    )


def _render_compiler_guided_prompt(
    theorem_statement: str,
    previous_candidate: str,
    compiler_diagnostics: str,
) -> str:
    return COMPILER_GUIDED_PROMPT_TEMPLATE.format(
        theorem_statement=theorem_statement,
        previous_candidate=previous_candidate,
        feedback=compiler_diagnostics,
    )


def _candidate_diagnostics(verification: VerificationResult) -> list:
    """Diagnostics about the candidate, excluding the reference-theorem sorry warning."""
    return [
        item
        for item in (verification.diagnostics or [])
        if item.get("kind") != "hasSorry"
    ]


def _compiler_diagnostic_payload(verification: VerificationResult) -> str:
    if verification.diagnostic_state != "available" or not verification.diagnostics:
        raise ValueError("Only available structured Lean diagnostics can be supplied.")
    # The fixed reference theorem is compiled with `sorry`, and candidates that
    # contain `sorry` are rejected before compilation. Any hasSorry warning
    # therefore describes the reference, not the candidate, and is not feedback.
    diagnostics = _candidate_diagnostics(verification)
    if not diagnostics:
        raise ValueError("No candidate-related Lean diagnostics are available.")
    return json.dumps(
        {
            "diagnostic_state": verification.diagnostic_state,
            "diagnostics": diagnostics,
        },
        ensure_ascii=False,
        indent=2,
    )


def _completion_settings(model: str) -> dict[str, object]:
    return {
        "provider": MODEL_PROVIDER,
        "requested_model": model,
        "temperature": DEFAULT_TEMPERATURE,
        "max_completion_tokens": DEFAULT_MAX_COMPLETION_TOKENS,
        "reasoning_effort": reasoning_effort_for_model(model),
        "max_transport_attempts": TRANSPORT_ATTEMPTS,
    }


def _call_model(
    completion_fn: CompletionFunction,
    prompt: str,
    *,
    model: str,
    cost_guard: CostReservationGuard | None = None,
) -> CompletionResult:
    arguments: dict[str, object] = {
        "max_tokens": DEFAULT_MAX_COMPLETION_TOKENS,
        "temperature": DEFAULT_TEMPERATURE,
        "retries": TRANSPORT_ATTEMPTS,
        "model": model,
        "reasoning_effort": reasoning_effort_for_model(model),
    }
    if cost_guard is not None:
        arguments["cost_guard"] = cost_guard
    return completion_fn(prompt, **arguments)


def _candidate_id(problem_id: str, candidate_sha256: str) -> str:
    return f"{problem_id}-{candidate_sha256}"


def _lean_environment(lean_project_dir: Path) -> dict[str, object]:
    toolchain_path = lean_project_dir / "lean-toolchain"
    manifest_path = lean_project_dir / "lake-manifest.json"
    lakefile_path = lean_project_dir / "lakefile.toml"
    toolchain = toolchain_path.read_text().strip() if toolchain_path.is_file() else None
    manifest_sha256 = (
        hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        if manifest_path.is_file()
        else None
    )
    lakefile_sha256 = (
        hashlib.sha256(lakefile_path.read_bytes()).hexdigest()
        if lakefile_path.is_file()
        else None
    )
    mathlib_revision = None
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text())
        packages = manifest.get("packages", []) if isinstance(manifest, dict) else []
        if isinstance(packages, list):
            mathlib = next(
                (
                    package
                    for package in packages
                    if isinstance(package, dict) and package.get("name") == "mathlib"
                ),
                None,
            )
            if isinstance(mathlib, dict):
                mathlib_revision = mathlib.get("rev")
    try:
        groq_sdk_version = importlib.metadata.version("groq")
    except importlib.metadata.PackageNotFoundError:
        groq_sdk_version = None
    return {
        "lean_toolchain": toolchain,
        "mathlib_revision": mathlib_revision,
        "lake_manifest_sha256": manifest_sha256,
        "lakefile_sha256": lakefile_sha256,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "groq_sdk_version": groq_sdk_version,
    }


def _verification_status(verification: VerificationResult) -> str:
    if verification.success:
        return "success"
    return {
        "compiler_error": "compiler_failure",
        "proof_rejected": "proof_rejected",
        "timeout": "timeout",
        "infrastructure_error": "infrastructure_error",
        "verifier_error": "verifier_error",
        "input_error": "invalid_input",
    }.get(verification.failure_kind, "verification_failure")


def _verification_record(verification: VerificationResult) -> dict[str, object]:
    return verification.to_record()


def _review_record_summary(problem_id: str) -> dict[str, str]:
    review_path = REPOSITORY_ROOT / "data" / "pilot_inputs" / f"{problem_id}_review.json"
    if not review_path.is_file():
        return {
            "review_record_status": "not_provided",
            "review_independence": "not_established",
        }
    review_record = json.loads(review_path.read_text(encoding="utf-8"))
    semantic_fidelity = review_record.get("semantic_fidelity", {})
    review_status = semantic_fidelity.get("review_status")
    reviewer_provenance = semantic_fidelity.get("reviewer_provenance", "")
    independence = (
        "not_independent"
        if isinstance(reviewer_provenance, str)
        and "not independent" in reviewer_provenance.lower()
        else "not_established"
    )
    return {
        "review_record_status": (
            review_status if isinstance(review_status, str) else "not_recorded"
        ),
        "review_independence": independence,
    }


def _atomic_manifest_update(manifest_path: Path, manifest: dict[str, object]) -> None:
    temporary_path = manifest_path.with_name(
        f".{manifest_path.name}.{uuid4().hex}.tmp"
    )
    with temporary_path.open("x", encoding="utf-8") as output:
        output.write(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary_path, manifest_path)


def _write_initial_manifest(
    manifest_path: Path, manifest: dict[str, object]
) -> None:
    with manifest_path.open("x", encoding="utf-8") as output:
        output.write(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        output.flush()
        os.fsync(output.fileno())


def _write_candidate(path: Path, candidate: str) -> None:
    with path.open("x", encoding="utf-8", newline="") as output:
        output.write(candidate)
        output.flush()
        os.fsync(output.fileno())


def _stamp_condition_context(
    manifest: dict[str, object],
    *,
    dataset_sha256: str | None,
    dataset_hash_status: str,
    protocol_sha256: str,
    configuration_sha256: str,
) -> None:
    conditions = manifest.get("conditions")
    if not isinstance(conditions, dict):
        return
    for result in conditions.values():
        if isinstance(result, dict):
            result["dataset_sha256"] = dataset_sha256
            result["dataset_hash_status"] = dataset_hash_status
            result["protocol_sha256"] = protocol_sha256
            result["configuration_sha256"] = configuration_sha256
            if result.get("stopping_reason") is None:
                result["stopping_reason"] = (
                    f"terminal_status_{result.get('status', 'unknown')}"
                )


def _provider_error_record(error: Exception) -> dict[str, object]:
    cause = error.__cause__
    underlying = cause if cause is not None else error
    status_code = getattr(underlying, "status_code", None)
    if isinstance(error, MissingGroqApiKeyError):
        error_category = "missing_credentials"
    elif isinstance(underlying, groq.RateLimitError):
        error_category = "rate_limit"
    elif "timeout" in type(underlying).__name__.lower():
        error_category = "timeout"
    elif status_code in {401, 403}:
        error_category = "authentication"
    elif status_code == 404:
        error_category = "model_access"
    else:
        error_category = "api_error"
    record: dict[str, object] = {
        "failure_kind": "provider_error",
        "error_category": error_category,
        "error_type": type(error).__name__,
        "underlying_error_type": type(underlying).__name__,
        "status_code": status_code if isinstance(status_code, int) else None,
        "transport_retry_events": getattr(error, "metadata", {}).get(
            "wrapper_retry_events"
        ) if isinstance(getattr(error, "metadata", None), dict) else None,
        "transport_attempt_metadata": getattr(error, "metadata", None),
        "raw_response_status": "unavailable_request_returned_no_response_object",
        "token_usage_status": "unavailable_no_response_metadata",
    }
    if isinstance(error, MissingGroqApiKeyError):
        record["error_code"] = "missing_groq_api_key"
        record["action"] = (
            "Set GROQ_API_KEY in the environment before starting the API run."
        )
    elif error_category == "authentication":
        record["action"] = (
            "Verify that GROQ_API_KEY is valid and authorized for this model."
        )
    elif error_category == "model_access":
        record["action"] = (
            "Verify the configured model ID and account access; no fallback model "
            "was selected."
        )
    elif error_category == "rate_limit":
        record["action"] = (
            "Review Groq rate limits and quota; no fallback model was selected."
        )
    elif error_category == "timeout":
        record["action"] = (
            "Check provider/network availability and retry only under the approved "
            "experiment protocol."
        )
    return record


def _run_condition(
    *,
    condition: str,
    theorem_statement: str,
    initial_candidate: str,
    initial_candidate_id: str,
    initial_candidate_sha256: str,
    initial_verification: VerificationResult,
    experiment_dir: Path,
    run_id: str,
    problem_id: str,
    lean_project_dir: Path,
    model: str,
    max_repair: int,
    execution_mode: ExecutionMode,
    completion_fn: CompletionFunction,
    cost_guard: CostReservationGuard | None,
    verification_fn: VerificationFunction,
    manifest: dict[str, object],
    manifest_path: Path,
    dataset_sha256: str | None,
    dataset_hash_status: str,
    configuration_sha256: str,
    protocol_sha256: str,
) -> dict[str, object]:
    initial_status = _verification_status(initial_verification)
    condition_result: dict[str, object] = {
        "condition": condition,
        "starting_candidate_id": initial_candidate_id,
        "starting_candidate_sha256": initial_candidate_sha256,
        "repair_call_limit": max_repair,
        "repair_calls_made": 0,
        "status": "not_run",
        "milestones": {
            "0": {
                "repair_calls": 0,
                "candidate_id": initial_candidate_id,
                "candidate_sha256": initial_candidate_sha256,
                "status": initial_status,
                "success": initial_verification.success,
                "verification": _verification_record(initial_verification),
            }
        },
        "attempts": [],
        "stopping_reason": None,
    }
    conditions = manifest["conditions"]
    assert isinstance(conditions, dict)
    conditions[condition] = condition_result
    if initial_verification.success:
        condition_result["status"] = "not_needed_initial_success"
        condition_result["stopping_reason"] = "shared_initial_candidate_verified"
        return condition_result
    if initial_verification.failure_kind != "compiler_error":
        condition_result["status"] = "not_eligible_initial_failure"
        condition_result["stopping_reason"] = f"initial_verification_{initial_status}"
        return condition_result

    diagnostic_state = initial_verification.diagnostic_state
    diagnostics = _candidate_diagnostics(initial_verification)
    if condition == "C" and (
        diagnostic_state != "available" or not diagnostics
    ):
        condition_result["diagnostic_state"] = diagnostic_state
        condition_result["status"] = (
            "missing_compiler_diagnostics"
            if diagnostic_state == "absent"
            else f"{diagnostic_state}_compiler_diagnostics"
        )
        condition_result["stopping_reason"] = "guided_diagnostics_unavailable"
        return condition_result

    current_candidate = initial_candidate
    condition_dir = experiment_dir / condition
    condition_dir.mkdir(exist_ok=False)
    for repair_call_number in range(1, max_repair + 1):
        if condition == "B":
            prompt = _render_blind_prompt(
                theorem_statement,
                current_candidate,
            )
        else:
            diagnostic_payload = _compiler_diagnostic_payload(
                initial_verification
                if repair_call_number == 1
                else previous_verification
            )
            prompt = _render_compiler_guided_prompt(
                theorem_statement,
                current_candidate,
                diagnostic_payload,
            )

        prompt_sha256 = _sha256_text(prompt)
        attempt_started = datetime.now(UTC).isoformat()
        attempt_started_monotonic = time.monotonic()
        attempt: dict[str, object] = {
            "attempt_id": f"{run_id}-{condition}-repair-{repair_call_number}",
            "generation_source": execution_mode,
            "repair_call_number": repair_call_number,
            "prompt_sha256": prompt_sha256,
            "started_at_utc": attempt_started,
            "provider": MODEL_PROVIDER if execution_mode == "api" else None,
            "configured_provider": MODEL_PROVIDER,
            "requested_model": model,
            "compiler_diagnostics_supplied": condition == "C",
            "compiler_diagnostics_status": (
                "supplied" if condition == "C" else "not_supplied_by_design"
            ),
            "dataset_sha256": dataset_sha256,
            "dataset_hash_status": dataset_hash_status,
            "protocol_sha256": protocol_sha256,
            "configuration_sha256": configuration_sha256,
            "attempt_index": repair_call_number,
            "retry_reason": (
                "previous_candidate_failed_compilation"
                if condition == "B"
                else "previous_candidate_failed_compilation_with_diagnostics"
            ),
            "previous_candidate_text": current_candidate,
            "previous_candidate_sha256": _sha256_text(current_candidate),
            "prompt_text": prompt,
        }
        if condition == "C":
            attempt["compiler_diagnostics_payload"] = diagnostic_payload
            attempt["compiler_diagnostics_payload_kind"] = "raw_structured_json"
            attempt["compiler_diagnostics_supplied_text"] = diagnostic_payload
            diagnostic_source = (
                initial_verification
                if repair_call_number == 1
                else previous_verification
            )
            attempt["compiler_diagnostics_candidate_sha256"] = _sha256_text(
                current_candidate
            )
            attempt["compiler_diagnostics_verification_source_sha256"] = (
                diagnostic_source.verification_source_sha256
            )
        else:
            attempt["compiler_diagnostics_payload"] = None
            attempt["compiler_diagnostics_candidate_sha256"] = None

        attempts = condition_result["attempts"]
        assert isinstance(attempts, list)
        attempts.append(attempt)
        condition_result["repair_calls_made"] = repair_call_number
        _atomic_manifest_update(manifest_path, manifest)
        try:
            completion = _call_model(
                completion_fn, prompt, model=model, cost_guard=cost_guard
            )
        except (groq.APIError, RuntimeError) as error:
            attempt.update(_provider_error_record(error))
            if cost_guard is not None:
                attempt["cost_guard"] = cost_guard.snapshot()
            attempt["finished_at_utc"] = datetime.now(UTC).isoformat()
            attempt["wall_clock_seconds"] = round(
                time.monotonic() - attempt_started_monotonic, 3
            )
            condition_result["status"] = "provider_error"
            condition_result["stopping_reason"] = "model_completion_failed"
            milestones = condition_result["milestones"]
            assert isinstance(milestones, dict)
            milestones[str(repair_call_number)] = {
                "repair_calls": repair_call_number,
                "candidate_id": None,
                "candidate_sha256": None,
                "status": "provider_error",
                "success": None,
            }
            _atomic_manifest_update(manifest_path, manifest)
            return condition_result

        candidate = extract_lean_block(completion.content)
        candidate_sha256 = _sha256_text(candidate)
        candidate_id = _candidate_id(problem_id, candidate_sha256)
        candidate_path = condition_dir / f"repair_{repair_call_number}.lean"
        _write_candidate(candidate_path, candidate)
        attempt.update(
            {
                "candidate_id": candidate_id,
                "candidate_sha256": candidate_sha256,
                "candidate_text": candidate,
                "candidate_path": str(candidate_path),
                "response_text": completion.content,
                "completion_metadata": completion.metadata,
                "prompt_tokens": completion.metadata.get("prompt_tokens"),
                "completion_tokens": completion.metadata.get("completion_tokens"),
                "total_tokens": completion.metadata.get("total_tokens"),
                "transport_api_attempts": completion.metadata.get("api_attempts"),
                "transport_retry_events": completion.metadata.get("retry_events"),
                "returned_model": completion.metadata.get("response_model"),
            }
        )
        _atomic_manifest_update(manifest_path, manifest)

        if not candidate:
            attempt["status"] = "empty_output"
            attempt["finished_at_utc"] = datetime.now(UTC).isoformat()
            attempt["wall_clock_seconds"] = round(
                time.monotonic() - attempt_started_monotonic, 3
            )
            condition_result["status"] = "empty_output"
            condition_result["stopping_reason"] = "empty_or_malformed_model_output"
            milestones = condition_result["milestones"]
            assert isinstance(milestones, dict)
            milestones[str(repair_call_number)] = {
                "repair_calls": repair_call_number,
                "candidate_id": candidate_id,
                "candidate_sha256": candidate_sha256,
                "status": "empty_output",
                "success": None,
            }
            _atomic_manifest_update(manifest_path, manifest)
            return condition_result

        scratch_name = f"repair_exp_{run_id}_{condition}_{repair_call_number}"
        try:
            verification = verification_fn(
                candidate,
                lean_project_dir,
                scratch_name,
                expected_statement=theorem_statement,
            )
        except OSError as error:
            attempt["status"] = "infrastructure_error"
            attempt["verification_error_type"] = type(error).__name__
            attempt["finished_at_utc"] = datetime.now(UTC).isoformat()
            attempt["wall_clock_seconds"] = round(
                time.monotonic() - attempt_started_monotonic, 3
            )
            condition_result["status"] = "infrastructure_error"
            condition_result["stopping_reason"] = "verifier_infrastructure_error"
            milestones = condition_result["milestones"]
            assert isinstance(milestones, dict)
            milestones[str(repair_call_number)] = {
                "repair_calls": repair_call_number,
                "candidate_id": candidate_id,
                "candidate_sha256": candidate_sha256,
                "status": "infrastructure_error",
                "success": None,
            }
            _atomic_manifest_update(manifest_path, manifest)
            return condition_result

        verification_status = _verification_status(verification)
        attempt.update(
            {
                "status": verification_status,
                "verification": _verification_record(verification),
                "verification_source_sha256": (
                    verification.verification_source_sha256
                ),
                "finished_at_utc": datetime.now(UTC).isoformat(),
                "wall_clock_seconds": round(
                    time.monotonic() - attempt_started_monotonic, 3
                ),
            }
        )
        milestones = condition_result["milestones"]
        assert isinstance(milestones, dict)
        milestones[str(repair_call_number)] = {
            "repair_calls": repair_call_number,
            "candidate_id": candidate_id,
            "candidate_sha256": candidate_sha256,
            "verification_source_sha256": verification.verification_source_sha256,
            "status": verification_status,
            "success": verification.success,
            "verification": _verification_record(verification),
        }
        _atomic_manifest_update(manifest_path, manifest)

        if verification.success:
            condition_result["status"] = "success"
            condition_result["stopping_reason"] = "verified_success"
            return condition_result
        if verification.failure_kind != "compiler_error":
            condition_result["status"] = verification_status
            condition_result["stopping_reason"] = f"verifier_{verification_status}"
            return condition_result

        if condition == "C" and (
            verification.diagnostic_state != "available"
            or not _candidate_diagnostics(verification)
        ):
            condition_result["diagnostic_state"] = verification.diagnostic_state
            condition_result["status"] = (
                "missing_compiler_diagnostics"
                if verification.diagnostic_state == "absent"
                else f"{verification.diagnostic_state}_compiler_diagnostics"
            )
            condition_result["stopping_reason"] = "guided_diagnostics_unavailable"
            return condition_result
        previous_verification = verification
        current_candidate = candidate

    condition_result["status"] = "repair_budget_exhausted"
    condition_result["stopping_reason"] = "maximum_repair_calls_reached"
    return condition_result


def run_experiment(
    problem_id: str,
    theorem_statement: str,
    lean_project_dir: Path,
    output_root: Path,
    *,
    model: str = DEFAULT_MODEL,
    max_repair: int = DEFAULT_MAX_REPAIRS,
    execution_mode: ExecutionMode = "api",
    completion_fn: CompletionFunction = complete_with_metadata,
    verification_fn: VerificationFunction = check_lean_file_detailed,
    experiment_id: str | None = None,
    dataset_sha256: str | None = None,
    dataset_path: Path | None = None,
) -> Path:
    """Run A/B/C, returning the run manifest path.

    API and verifier failures are persisted as explicit terminal/incomplete
    outcomes. Unexpected exceptions propagate and leave status as ``running``.
    """
    if not _safe_id(problem_id):
        raise ValueError("Problem ID must be a safe filename component.")
    if not theorem_statement.strip():
        raise ValueError("The fixed Lean theorem statement must not be empty.")
    if dataset_sha256 is not None and not re.fullmatch(
        r"[0-9a-f]{64}", dataset_sha256
    ):
        raise ValueError("dataset_sha256 must be a lowercase SHA-256 digest.")
    if dataset_path is not None:
        dataset_path = Path(dataset_path).resolve()
        if not dataset_path.is_file():
            raise ValueError("dataset_path must reference an existing dataset file.")
        computed_dataset_sha256 = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
        if dataset_sha256 is not None and dataset_sha256 != computed_dataset_sha256:
            raise ValueError("dataset_sha256 does not match the dataset file bytes.")
        dataset_sha256 = computed_dataset_sha256
    dataset_hash_status = (
        "computed_from_file"
        if dataset_path
        else "caller_supplied_unverified"
        if dataset_sha256
        else "unavailable_mock_or_manual_run"
    )
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model identifier must be a non-empty string.")
    if execution_mode not in {"api", "mock", "manual"}:
        raise ValueError("execution_mode must be 'api', 'mock', or 'manual'.")
    if (execution_mode == "api") != (completion_fn is complete_with_metadata):
        raise ValueError(
            "API mode requires the Groq completion client; injected completion "
            "functions must be labeled 'mock' or 'manual'."
        )
    if isinstance(max_repair, bool) or not isinstance(max_repair, int) or not 0 <= max_repair <= 3:
        raise ValueError("max_repair must be an integer from 0 through 3.")

    protocol_record = _protocol_metadata()
    if execution_mode == "api" and model != DEFAULT_MODEL:
        raise ValueError(
            "API mode requires the primary model recorded in the locked protocol."
        )
    if execution_mode == "api" and max_repair != DEFAULT_MAX_REPAIRS:
        raise ValueError(
            "API mode requires the locked three-repair budget for conditions B and C."
        )

    cost_guard: CostReservationGuard | None = None
    if execution_mode == "api":
        try:
            cost_guard = CostReservationGuard(
                CostGuardConfig.from_environment(
                    model_id=model,
                    wrapper_attempts_per_completion=TRANSPORT_ATTEMPTS,
                    sdk_max_retries_per_wrapper_attempt=SDK_MAX_RETRIES,
                )
            )
        except CostGuardConfigurationError as error:
            raise ValueError(
                "Official pricing or cost-guard configuration is missing or "
                f"unverified: {error}"
            ) from error
        if not API_EXECUTION_ENABLED:
            raise ValueError(API_EXECUTION_BLOCKED_REASON)
        if dataset_path is None:
            raise ValueError(
                "API execution requires the exact frozen dataset artifact file."
            )

    run_id = experiment_id or _new_experiment_id()
    if not _safe_id(run_id):
        raise ValueError("Experiment ID must be a safe filename component.")
    lean_project_dir = Path(lean_project_dir).resolve()
    environment = _lean_environment(lean_project_dir)
    output_root = Path(output_root).resolve()
    experiment_dir = output_root / run_id
    output_root.mkdir(parents=True, exist_ok=False)
    experiment_dir.mkdir(exist_ok=False)
    manifest_path = experiment_dir / "manifest.json"
    started_at = datetime.now(UTC)
    started_monotonic = time.monotonic()
    api_completion = execution_mode == "api"
    theorem_sha256 = _sha256_text(theorem_statement)
    configuration = {
        "provider": MODEL_PROVIDER,
        "requested_model": model,
        "temperature": DEFAULT_TEMPERATURE,
        "max_completion_tokens": DEFAULT_MAX_COMPLETION_TOKENS,
        "reasoning_effort": reasoning_effort_for_model(model),
        "max_repair_calls": max_repair,
        "transport_attempts_per_model_call": TRANSPORT_ATTEMPTS,
        "groq_sdk_max_retries": SDK_MAX_RETRIES,
        "lean_project_dir": str(lean_project_dir),
        "execution_mode": execution_mode,
        "dataset_sha256": dataset_sha256,
    }
    configuration_sha256 = _canonical_sha256(configuration)
    manifest: dict[str, object] = {
        "schema_version": 1,
        "experiment_type": "paired_compiler_guided_repair",
        "protocol": protocol_record,
        "experiment_id": run_id,
        "provider": MODEL_PROVIDER if api_completion else None,
        "configured_provider": MODEL_PROVIDER,
        "model_identifier": model,
        "execution_mode": execution_mode,
        "api_generation_confirmed": False,
        "problem_id": problem_id,
        "dataset_sha256": dataset_sha256,
        "dataset_hash_status": dataset_hash_status,
        "dataset_path": str(dataset_path) if dataset_path else None,
        "configuration_sha256": configuration_sha256,
        "status": "running",
        "started_at_utc": started_at.isoformat().replace("+00:00", "Z"),
        "finished_at_utc": None,
        "wall_clock_seconds": None,
        "theorem_statement": theorem_statement,
        "theorem_sha256": theorem_sha256,
        "theorem_review_status": "not_verified_by_harness",
        "prompt_templates": {
            name: {
                "path": str(path),
                "sha256": _prompt_hashes()[name],
            }
            for name, path in PROMPT_PATHS.items()
        },
        "model_identifier_semantics": "provider_alias_not_pinned",
        "configuration": configuration,
        "environment": environment,
        "cost_guard": cost_guard.snapshot() if cost_guard is not None else None,
        "initial_candidate": None,
        "initial_verification": None,
        "conditions": {},
    }
    _write_initial_manifest(manifest_path, manifest)
    if cost_guard is not None:
        def persist_cost_guard(snapshot: dict[str, object]) -> None:
            manifest["cost_guard"] = snapshot
            _atomic_manifest_update(manifest_path, manifest)

        cost_guard.set_persist_callback(persist_cost_guard)

    initial_prompt = _render_initial_prompt(theorem_statement)
    initial_prompt_sha256 = _sha256_text(initial_prompt)
    initial_attempt_id = f"{run_id}-initial"
    initial_started = time.monotonic()
    initial_started_at = datetime.now(UTC).isoformat()
    try:
        initial_completion = _call_model(
            completion_fn,
            initial_prompt,
            model=model,
            cost_guard=cost_guard,
        )
    except (groq.APIError, RuntimeError) as error:
        manifest["initial_candidate"] = {
            "status": "provider_error",
            "attempt_id": initial_attempt_id,
            "generation_source": execution_mode,
            "prompt_sha256": initial_prompt_sha256,
            "prompt_text": initial_prompt,
            "dataset_sha256": dataset_sha256,
            "protocol_sha256": protocol_record["sha256"],
            "configuration_sha256": configuration_sha256,
            "attempt_index": 0,
            "retry_reason": "initial_generation",
            "provider": MODEL_PROVIDER if api_completion else None,
            "configured_provider": MODEL_PROVIDER,
            "requested_model": model,
            "started_at_utc": initial_started_at,
            **_provider_error_record(error),
            "cost_guard": cost_guard.snapshot() if cost_guard is not None else None,
            "finished_at_utc": datetime.now(UTC).isoformat(),
            "wall_clock_seconds": round(time.monotonic() - initial_started, 3),
        }
        manifest["conditions"] = {
            "A": {
                "condition": "A",
                "status": "provider_error",
                "repair_calls_made": 0,
            },
            "B": {
                "condition": "B",
                "status": "not_run_initial_provider_error",
                "repair_calls_made": 0,
                "starting_candidate_id": None,
                "starting_candidate_sha256": None,
            },
            "C": {
                "condition": "C",
                "status": "not_run_initial_provider_error",
                "repair_calls_made": 0,
                "starting_candidate_id": None,
                "starting_candidate_sha256": None,
            },
        }
        manifest["status"] = "incomplete"
        manifest["incomplete_reason"] = "initial_provider_error"
        manifest["finished_at_utc"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        manifest["wall_clock_seconds"] = round(time.monotonic() - started_monotonic, 3)
        _stamp_condition_context(
            manifest,
            dataset_sha256=dataset_sha256,
            dataset_hash_status=dataset_hash_status,
            protocol_sha256=protocol_record["sha256"],
            configuration_sha256=configuration_sha256,
        )
        _atomic_manifest_update(manifest_path, manifest)
        return manifest_path

    initial_candidate = extract_lean_block(initial_completion.content)
    manifest["api_generation_confirmed"] = api_completion
    initial_candidate_sha256 = _sha256_text(initial_candidate)
    initial_candidate_id = _candidate_id(problem_id, initial_candidate_sha256)
    initial_candidate_path = experiment_dir / "initial_candidate.lean"
    _write_candidate(initial_candidate_path, initial_candidate)
    manifest["initial_candidate"] = {
        "status": "empty_output" if not initial_candidate else "generated",
        "attempt_id": initial_attempt_id,
        "generation_source": execution_mode,
        "dataset_sha256": dataset_sha256,
        "dataset_hash_status": dataset_hash_status,
        "protocol_sha256": protocol_record["sha256"],
        "configuration_sha256": configuration_sha256,
        "attempt_index": 0,
        "retry_reason": "initial_generation",
        "candidate_id": initial_candidate_id,
        "candidate_sha256": initial_candidate_sha256,
        "candidate_text": initial_candidate,
        "candidate_path": str(initial_candidate_path),
        "response_text": initial_completion.content,
        "prompt_sha256": initial_prompt_sha256,
        "prompt_text": initial_prompt,
        "provider": MODEL_PROVIDER if api_completion else None,
        "requested_model": model,
        "returned_model": initial_completion.metadata.get("response_model"),
        "completion_metadata": initial_completion.metadata,
        "prompt_tokens": initial_completion.metadata.get("prompt_tokens"),
        "completion_tokens": initial_completion.metadata.get("completion_tokens"),
        "total_tokens": initial_completion.metadata.get("total_tokens"),
        "transport_api_attempts": initial_completion.metadata.get("api_attempts"),
        "transport_retry_events": initial_completion.metadata.get("retry_events"),
        "started_at_utc": initial_started_at,
        "finished_at_utc": datetime.now(UTC).isoformat(),
        "wall_clock_seconds": round(time.monotonic() - initial_started, 3),
    }
    manifest["initial_candidate_id"] = initial_candidate_id
    _atomic_manifest_update(manifest_path, manifest)

    if not initial_candidate:
        manifest["conditions"] = {
            "A": {
                "condition": "A",
                "status": "empty_output",
                "repair_calls_made": 0,
                "starting_candidate_id": initial_candidate_id,
                "starting_candidate_sha256": initial_candidate_sha256,
                "milestones": {
                    "0": {
                        "repair_calls": 0,
                        "candidate_id": initial_candidate_id,
                        "candidate_sha256": initial_candidate_sha256,
                        "status": "empty_output",
                        "success": None,
                    }
                },
            },
            "B": {
                "condition": "B",
                "status": "not_run_empty_initial_output",
                "repair_calls_made": 0,
                "starting_candidate_id": initial_candidate_id,
                "starting_candidate_sha256": initial_candidate_sha256,
            },
            "C": {
                "condition": "C",
                "status": "not_run_empty_initial_output",
                "repair_calls_made": 0,
                "starting_candidate_id": initial_candidate_id,
                "starting_candidate_sha256": initial_candidate_sha256,
            },
        }
        manifest["status"] = "completed_with_failures"
        manifest["finished_at_utc"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        manifest["wall_clock_seconds"] = round(time.monotonic() - started_monotonic, 3)
        _stamp_condition_context(
            manifest,
            dataset_sha256=dataset_sha256,
            dataset_hash_status=dataset_hash_status,
            protocol_sha256=protocol_record["sha256"],
            configuration_sha256=configuration_sha256,
        )
        _atomic_manifest_update(manifest_path, manifest)
        return manifest_path

    initial_scratch_name = f"repair_exp_{run_id}_initial"
    initial_verification_started = time.monotonic()
    initial_verification_started_at = datetime.now(UTC).isoformat()
    try:
        initial_verification = verification_fn(
            initial_candidate,
            Path(lean_project_dir),
            initial_scratch_name,
            expected_statement=theorem_statement,
        )
    except OSError as error:
        initial_verification = VerificationResult(
            success=False,
            errors=[f"Verifier infrastructure error: {type(error).__name__}"],
            elapsed_seconds=time.monotonic() - initial_verification_started,
            failure_kind="infrastructure_error",
        )
    manifest["initial_verification"] = {
        **_verification_record(initial_verification),
        "candidate_id": initial_candidate_id,
        "candidate_sha256": initial_candidate_sha256,
        "verification_source_sha256": (
            initial_verification.verification_source_sha256
        ),
        "status": _verification_status(initial_verification),
        "started_at_utc": initial_verification_started_at,
        "finished_at_utc": datetime.now(UTC).isoformat(),
        "wall_clock_seconds": round(
            time.monotonic() - initial_verification_started, 3
        ),
    }
    manifest["conditions"] = {
        "A": {
            "condition": "A",
            "status": _verification_status(initial_verification),
            "repair_calls_made": 0,
            "starting_candidate_id": initial_candidate_id,
            "starting_candidate_sha256": initial_candidate_sha256,
            "milestones": {
                "0": {
                    "repair_calls": 0,
                    "candidate_id": initial_candidate_id,
                    "candidate_sha256": initial_candidate_sha256,
                    "verification_source_sha256": (
                        initial_verification.verification_source_sha256
                    ),
                    "status": _verification_status(initial_verification),
                    "success": initial_verification.success,
                    "verification": _verification_record(initial_verification),
                }
            },
        }
    }
    _atomic_manifest_update(manifest_path, manifest)

    if initial_verification.failure_kind in {
        "timeout",
        "infrastructure_error",
        "verifier_error",
        "input_error",
    }:
        manifest["conditions"].update(
            {
                "B": {
                    "condition": "B",
                    "status": "not_run_initial_verification_unavailable",
                    "repair_calls_made": 0,
                    "starting_candidate_id": initial_candidate_id,
                    "starting_candidate_sha256": initial_candidate_sha256,
                },
                "C": {
                    "condition": "C",
                    "status": "not_run_initial_verification_unavailable",
                    "repair_calls_made": 0,
                    "starting_candidate_id": initial_candidate_id,
                    "starting_candidate_sha256": initial_candidate_sha256,
                },
            }
        )
        manifest["status"] = "incomplete"
        manifest["incomplete_reason"] = "initial_verification_unavailable"
        manifest["finished_at_utc"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        manifest["wall_clock_seconds"] = round(time.monotonic() - started_monotonic, 3)
        _stamp_condition_context(
            manifest,
            dataset_sha256=dataset_sha256,
            dataset_hash_status=dataset_hash_status,
            protocol_sha256=protocol_record["sha256"],
            configuration_sha256=configuration_sha256,
        )
        _atomic_manifest_update(manifest_path, manifest)
        return manifest_path

    conditions = manifest["conditions"]
    assert isinstance(conditions, dict)
    if initial_verification.success:
        conditions["B"] = {
            "condition": "B",
            "status": "not_needed_initial_success",
            "repair_calls_made": 0,
            "starting_candidate_id": initial_candidate_id,
            "starting_candidate_sha256": initial_candidate_sha256,
            "milestones": {"0": {"repair_calls": 0, "status": "success", "success": True}},
        }
        conditions["C"] = {
            "condition": "C",
            "status": "not_needed_initial_success",
            "repair_calls_made": 0,
            "starting_candidate_id": initial_candidate_id,
            "starting_candidate_sha256": initial_candidate_sha256,
            "milestones": {"0": {"repair_calls": 0, "status": "success", "success": True}},
        }
    elif initial_verification.failure_kind == "compiler_error":
        for condition in ("B", "C"):
            conditions[condition] = _run_condition(
                condition=condition,
                theorem_statement=theorem_statement,
                initial_candidate=initial_candidate,
                initial_candidate_id=initial_candidate_id,
                initial_candidate_sha256=initial_candidate_sha256,
                initial_verification=initial_verification,
                experiment_dir=experiment_dir,
                run_id=run_id,
                problem_id=problem_id,
                lean_project_dir=Path(lean_project_dir),
                model=model,
                max_repair=max_repair,
                execution_mode=execution_mode,
                completion_fn=completion_fn,
                cost_guard=cost_guard,
                verification_fn=verification_fn,
                manifest=manifest,
                manifest_path=manifest_path,
                dataset_sha256=dataset_sha256,
                dataset_hash_status=dataset_hash_status,
                configuration_sha256=configuration_sha256,
                protocol_sha256=protocol_record["sha256"],
            )
            _atomic_manifest_update(manifest_path, manifest)
    else:
        for condition in ("B", "C"):
            conditions[condition] = {
                "condition": condition,
                "status": "not_eligible_initial_failure",
                "repair_calls_made": 0,
                "starting_candidate_id": initial_candidate_id,
                "starting_candidate_sha256": initial_candidate_sha256,
                "milestones": {
                    "0": {
                        "repair_calls": 0,
                        "candidate_id": initial_candidate_id,
                        "candidate_sha256": initial_candidate_sha256,
                        "status": _verification_status(initial_verification),
                        "success": False,
                        "verification": _verification_record(initial_verification),
                    }
                },
            }

    complete_statuses = {
        "success",
        "repair_budget_exhausted",
        "not_needed_initial_success",
    }
    manifest["status"] = (
        "completed"
        if all(
            isinstance(conditions.get(condition), dict)
            and conditions[condition].get("status") in complete_statuses
            for condition in ("B", "C")
        )
        else "completed_with_failures"
    )
    manifest["finished_at_utc"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    manifest["wall_clock_seconds"] = round(time.monotonic() - started_monotonic, 3)
    _stamp_condition_context(
        manifest,
        dataset_sha256=dataset_sha256,
        dataset_hash_status=dataset_hash_status,
        protocol_sha256=protocol_record["sha256"],
        configuration_sha256=configuration_sha256,
    )
    _atomic_manifest_update(manifest_path, manifest)
    return manifest_path


def _plan(
    problem_id: str,
    theorem_statement: str,
    model: str,
    max_repair: int,
    output_root: Path | None = None,
    dataset_sha256: str | None = None,
    dataset_path: Path | None = None,
) -> dict[str, object]:
    if not _safe_id(problem_id):
        raise ValueError("Problem ID must be a safe filename component.")
    if not theorem_statement.strip():
        raise ValueError("The fixed Lean theorem statement must not be empty.")
    if dataset_sha256 is not None and not re.fullmatch(
        r"[0-9a-f]{64}", dataset_sha256
    ):
        raise ValueError("dataset_sha256 must be a lowercase SHA-256 digest.")
    if dataset_path is not None:
        dataset_path = Path(dataset_path).resolve()
        if not dataset_path.is_file():
            raise ValueError("dataset_path must reference an existing dataset file.")
        actual_sha256 = hashlib.sha256(dataset_path.read_bytes()).hexdigest()
        if dataset_sha256 is not None and dataset_sha256 != actual_sha256:
            raise ValueError("dataset_sha256 does not match the dataset file bytes.")
        dataset_sha256 = actual_sha256
    dataset_hash_status = (
        "computed_from_file"
        if dataset_path
        else "caller_supplied_unverified"
        if dataset_sha256
        else "not_provided"
    )
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model identifier must be a non-empty string.")
    if isinstance(max_repair, bool) or not isinstance(max_repair, int) or not 0 <= max_repair <= 3:
        raise ValueError("max_repair must be an integer from 0 through 3.")
    protocol_record = _protocol_metadata()
    if model != DEFAULT_MODEL:
        raise ValueError("Plan must use the primary model recorded in the protocol.")
    if max_repair != DEFAULT_MAX_REPAIRS:
        raise ValueError("Plan must use the locked three-repair budget for B and C.")
    max_logical_completions = 1 + (2 * max_repair)
    max_http_attempts_per_completion = TRANSPORT_ATTEMPTS * (SDK_MAX_RETRIES + 1)
    return {
        "experiment_type": "paired_compiler_guided_repair",
        "protocol": protocol_record,
        "problem_id": problem_id,
        "dataset_sha256": dataset_sha256,
        "dataset_hash_status": dataset_hash_status,
        "dataset_path": str(dataset_path) if dataset_path else None,
        "theorem_sha256": _sha256_text(theorem_statement),
        "theorem_review_status": "not_verified_by_harness",
        **_review_record_summary(problem_id),
        "model_identifier_semantics": "provider_alias_not_pinned",
        "provider": MODEL_PROVIDER,
        "model_identifier": model,
        "execution_mode": "plan_only",
        "output_root": str(Path(output_root).resolve()) if output_root else None,
        "output_root_is_fresh": (
            not Path(output_root).exists() if output_root else None
        ),
        "configuration": {
            **_completion_settings(model),
            "max_repair_calls": max_repair,
            "groq_sdk_max_retries": SDK_MAX_RETRIES,
            "dataset_sha256": dataset_sha256,
        },
        "worst_case_call_bounds": {
            "initial_completion_shared_across_conditions": True,
            "maximum_logical_completions": max_logical_completions,
            "wrapper_attempts_per_completion": TRANSPORT_ATTEMPTS,
            "groq_sdk_retries_per_wrapper_attempt": SDK_MAX_RETRIES,
            "maximum_http_attempts_per_completion": max_http_attempts_per_completion,
            "maximum_http_attempts_total": (
                max_logical_completions * max_http_attempts_per_completion
            ),
        },
        "cost_guard": {
            "status": "blocked_preflight_only",
            "budget_usd": PILOT_BUDGET_USD,
            "pricing_status": "unverified",
            "estimated_max_cost_usd": None,
            "pricing_source": None,
            "reason": API_EXECUTION_BLOCKED_REASON,
        },
        "prompt_templates": _prompt_hashes(),
        "api_calls_will_be_made": False,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Run a paired one-shot/blind/compiler-guided Lean repair experiment."
    )
    parser.add_argument("--problem-id", required=True)
    parser.add_argument("--theorem-file", required=True, type=Path)
    parser.add_argument("--lean-project", type=Path, default=REPOSITORY_ROOT / "lean_project")
    parser.add_argument("--output-root", type=Path, default=REPOSITORY_ROOT / "data/experiments")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="explicit model ID for every A/B/C call (default: proposed primary candidate)",
    )
    parser.add_argument("--max-repair", type=int, default=DEFAULT_MAX_REPAIRS)
    parser.add_argument(
        "--dataset-sha256",
        help="Optional SHA-256 check for the exact frozen dataset artifact file",
    )
    parser.add_argument(
        "--dataset-file",
        type=Path,
        help="Exact dataset artifact file; its SHA-256 is computed into the run record",
    )
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="validate and print configuration without writing files or calling the API",
    )
    args = parser.parse_args(argv)
    theorem_statement = args.theorem_file.read_text()
    try:
        if args.plan_only:
            print(
                json.dumps(
                    _plan(
                        args.problem_id,
                        theorem_statement,
                        args.model,
                        args.max_repair,
                        args.output_root,
                        args.dataset_sha256,
                        args.dataset_file,
                    ),
                    indent=2,
                )
            )
            return
        manifest_path = run_experiment(
            args.problem_id,
            theorem_statement,
            args.lean_project,
            args.output_root,
            model=args.model,
            max_repair=args.max_repair,
            dataset_sha256=args.dataset_sha256,
            dataset_path=args.dataset_file,
        )
    except ValueError as error:
        parser.error(str(error))
    print(manifest_path)


if __name__ == "__main__":
    main()

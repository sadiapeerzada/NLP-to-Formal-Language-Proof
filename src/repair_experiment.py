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
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Literal
from uuid import uuid4

import groq

from llm_client import (
    CompletionResult,
    MissingGroqApiKeyError,
    complete_with_metadata,
    extract_lean_block,
    reasoning_effort_for_model,
)
from verify import VerificationResult, check_lean_file_detailed


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATHS = {
    "initial": REPOSITORY_ROOT / "prompts" / "repair_experiment_initial.txt",
    "blind": REPOSITORY_ROOT / "prompts" / "repair_experiment_blind.txt",
    "compiler_guided": (
        REPOSITORY_ROOT / "prompts" / "repair_experiment_compiler_guided.txt"
    ),
}
INITIAL_PROMPT_TEMPLATE = PROMPT_PATHS["initial"].read_text()
BLIND_PROMPT_TEMPLATE = PROMPT_PATHS["blind"].read_text()
COMPILER_GUIDED_PROMPT_TEMPLATE = PROMPT_PATHS["compiler_guided"].read_text()
DEFAULT_MODEL = "openai/gpt-oss-120b"
MODEL_PROVIDER = "groq"
DEFAULT_MAX_REPAIRS = 3
DEFAULT_MAX_COMPLETION_TOKENS = 2000
DEFAULT_TEMPERATURE = 0.2
TRANSPORT_RETRIES = 3
BLIND_FEEDBACK_FIELD = "No compiler diagnostics are provided in the blind-retry condition."

CompletionFunction = Callable[..., CompletionResult]
VerificationFunction = Callable[..., VerificationResult]
ExecutionMode = Literal["api", "mock", "manual"]


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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
        "max_transport_retries": TRANSPORT_RETRIES,
    }


def _call_model(
    completion_fn: CompletionFunction,
    prompt: str,
    *,
    model: str,
) -> CompletionResult:
    return completion_fn(
        prompt,
        max_tokens=DEFAULT_MAX_COMPLETION_TOKENS,
        temperature=DEFAULT_TEMPERATURE,
        retries=TRANSPORT_RETRIES,
        model=model,
        reasoning_effort=reasoning_effort_for_model(model),
    )


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
        "transport_retry_events": None,
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
    verification_fn: VerificationFunction,
    manifest: dict[str, object],
    manifest_path: Path,
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
    }
    conditions = manifest["conditions"]
    assert isinstance(conditions, dict)
    conditions[condition] = condition_result
    if initial_verification.success:
        condition_result["status"] = "not_needed_initial_success"
        return condition_result
    if initial_verification.failure_kind != "compiler_error":
        condition_result["status"] = "not_eligible_initial_failure"
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
        }
        if condition == "C":
            attempt["compiler_diagnostics_payload"] = diagnostic_payload
            attempt["compiler_diagnostics_payload_kind"] = "raw_structured_json"
            attempt["compiler_diagnostics_supplied_text"] = diagnostic_payload

        attempts = condition_result["attempts"]
        assert isinstance(attempts, list)
        attempts.append(attempt)
        condition_result["repair_calls_made"] = repair_call_number
        _atomic_manifest_update(manifest_path, manifest)
        try:
            completion = _call_model(completion_fn, prompt, model=model)
        except (groq.APIError, RuntimeError) as error:
            attempt.update(_provider_error_record(error))
            attempt["finished_at_utc"] = datetime.now(UTC).isoformat()
            attempt["wall_clock_seconds"] = round(
                time.monotonic() - attempt_started_monotonic, 3
            )
            condition_result["status"] = "provider_error"
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
            return condition_result
        if verification.failure_kind != "compiler_error":
            condition_result["status"] = verification_status
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
            return condition_result
        previous_verification = verification
        current_candidate = candidate

    condition_result["status"] = "repair_budget_exhausted"
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
) -> Path:
    """Run A/B/C, returning the run manifest path.

    API and verifier failures are persisted as explicit terminal/incomplete
    outcomes. Unexpected exceptions propagate and leave status as ``running``.
    """
    if not _safe_id(problem_id):
        raise ValueError("Problem ID must be a safe filename component.")
    if not theorem_statement.strip():
        raise ValueError("The fixed Lean theorem statement must not be empty.")
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

    run_id = experiment_id or _new_experiment_id()
    if not _safe_id(run_id):
        raise ValueError("Experiment ID must be a safe filename component.")
    lean_project_dir = Path(lean_project_dir).resolve()
    environment = _lean_environment(lean_project_dir)
    output_root = Path(output_root).resolve()
    experiment_dir = output_root / run_id
    output_root.mkdir(parents=True, exist_ok=True)
    experiment_dir.mkdir(exist_ok=False)
    manifest_path = experiment_dir / "manifest.json"
    started_at = datetime.now(UTC)
    started_monotonic = time.monotonic()
    api_completion = execution_mode == "api"
    theorem_sha256 = _sha256_text(theorem_statement)
    manifest: dict[str, object] = {
        "schema_version": 1,
        "experiment_type": "paired_compiler_guided_repair",
        "experiment_id": run_id,
        "provider": MODEL_PROVIDER if api_completion else None,
        "configured_provider": MODEL_PROVIDER,
        "model_identifier": model,
        "execution_mode": execution_mode,
        "api_generation_confirmed": False,
        "problem_id": problem_id,
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
        "configuration": {
            "provider": MODEL_PROVIDER,
            "requested_model": model,
            "temperature": DEFAULT_TEMPERATURE,
            "max_completion_tokens": DEFAULT_MAX_COMPLETION_TOKENS,
            "reasoning_effort": reasoning_effort_for_model(model),
            "max_repair_calls": max_repair,
            "transport_retries_per_model_call": TRANSPORT_RETRIES,
            "lean_project_dir": str(Path(lean_project_dir).resolve()),
        },
        "environment": environment,
        "initial_candidate": None,
        "initial_verification": None,
        "conditions": {},
    }
    _write_initial_manifest(manifest_path, manifest)

    initial_prompt = _render_initial_prompt(theorem_statement)
    initial_prompt_sha256 = _sha256_text(initial_prompt)
    initial_attempt_id = f"{run_id}-initial"
    initial_started = time.monotonic()
    initial_started_at = datetime.now(UTC).isoformat()
    try:
        initial_completion = _call_model(completion_fn, initial_prompt, model=model)
    except (groq.APIError, RuntimeError) as error:
        manifest["initial_candidate"] = {
            "status": "provider_error",
            "attempt_id": initial_attempt_id,
            "generation_source": execution_mode,
            "prompt_sha256": initial_prompt_sha256,
            "provider": MODEL_PROVIDER if api_completion else None,
            "configured_provider": MODEL_PROVIDER,
            "requested_model": model,
            "started_at_utc": initial_started_at,
            **_provider_error_record(error),
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
        "candidate_id": initial_candidate_id,
        "candidate_sha256": initial_candidate_sha256,
        "candidate_text": initial_candidate,
        "candidate_path": str(initial_candidate_path),
        "response_text": initial_completion.content,
        "prompt_sha256": initial_prompt_sha256,
        "provider": MODEL_PROVIDER,
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
                verification_fn=verification_fn,
                manifest=manifest,
                manifest_path=manifest_path,
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
    _atomic_manifest_update(manifest_path, manifest)
    return manifest_path


def _plan(
    problem_id: str,
    theorem_statement: str,
    model: str,
    max_repair: int,
) -> dict[str, object]:
    if not _safe_id(problem_id):
        raise ValueError("Problem ID must be a safe filename component.")
    if not theorem_statement.strip():
        raise ValueError("The fixed Lean theorem statement must not be empty.")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model identifier must be a non-empty string.")
    if isinstance(max_repair, bool) or not isinstance(max_repair, int) or not 0 <= max_repair <= 3:
        raise ValueError("max_repair must be an integer from 0 through 3.")
    return {
        "experiment_type": "paired_compiler_guided_repair",
        "problem_id": problem_id,
        "theorem_sha256": _sha256_text(theorem_statement),
        "theorem_review_status": "not_verified_by_harness",
        "model_identifier_semantics": "provider_alias_not_pinned",
        "provider": MODEL_PROVIDER,
        "model_identifier": model,
        "execution_mode": "plan_only",
        "configuration": {
            **_completion_settings(model),
            "max_repair_calls": max_repair,
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
                    _plan(args.problem_id, theorem_statement, args.model, args.max_repair),
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
        )
    except ValueError as error:
        parser.error(str(error))
    print(manifest_path)


if __name__ == "__main__":
    main()

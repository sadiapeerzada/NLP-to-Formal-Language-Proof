from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import llm_client
import repair_experiment as experiment
import verify as verifier
from llm_client import CompletionResult
from verify import VerificationResult


THEOREM = "theorem target : True := by sorry"
INITIAL_CANDIDATE = "theorem target : True := by exact False.elim (by trivial)"
DIAGNOSTIC_INITIAL = "line 1: initial Lean diagnostic"
DIAGNOSTIC_LATEST = "line 2: latest Lean diagnostic"


def completion(content: str, *, prompt_tokens: int | None = 17) -> CompletionResult:
    return CompletionResult(
        content=content,
        metadata={
            "model": experiment.DEFAULT_MODEL,
            "response_model": "provider-returned-model",
            "prompt_tokens": prompt_tokens,
            "completion_tokens": 23,
            "total_tokens": 40 if prompt_tokens is not None else None,
            "api_attempts": 1,
            "retry_events": [],
        },
    )


def failed_verification(diagnostic: str = DIAGNOSTIC_INITIAL) -> VerificationResult:
    return VerificationResult(
        success=False,
        errors=[diagnostic],
        exit_code=1,
        diagnostics_parsed=1,
        failure_kind="compiler_error",
        diagnostic_text=diagnostic,
        diagnostics=[
            {
                "severity": "error",
                "data": diagnostic,
                "pos": {"line": 1, "column": 3},
            }
        ],
        diagnostic_state="available",
    )


def successful_verification() -> VerificationResult:
    return VerificationResult(
        success=True,
        exit_code=0,
        diagnostics_parsed=1,
        failure_kind=None,
    )


def run_in(
    root: Path,
    completion_fn,
    verification_fn,
    *,
    max_repair: int = 3,
    experiment_id: str | None = None,
    execution_mode: experiment.ExecutionMode = "mock",
) -> Path:
    return experiment.run_experiment(
        "problem_001",
        THEOREM,
        root / "lean_project",
        root / "runs",
        completion_fn=completion_fn,
        verification_fn=verification_fn,
        max_repair=max_repair,
        execution_mode=execution_mode,
        experiment_id=experiment_id,
    )


def read_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def test_one_shot_makes_no_repair_calls_and_verifies_initial_once(tmp_path: Path) -> None:
    completion_fn = Mock(return_value=completion(INITIAL_CANDIDATE))
    verification_fn = Mock(return_value=successful_verification())

    path = run_in(tmp_path, completion_fn, verification_fn)
    manifest = read_manifest(path)

    assert completion_fn.call_count == 1
    assert verification_fn.call_count == 1
    assert manifest["conditions"]["A"]["repair_calls_made"] == 0
    assert manifest["conditions"]["B"]["status"] == "not_needed_initial_success"
    assert manifest["conditions"]["C"]["status"] == "not_needed_initial_success"
    assert manifest["status"] == "completed"
    assert manifest["execution_mode"] == "mock"
    assert manifest["api_generation_confirmed"] is False
    assert manifest["initial_candidate"]["generation_source"] == "mock"


def test_blind_and_guided_share_initial_candidate_and_hash(tmp_path: Path) -> None:
    completion_fn = Mock(
        side_effect=[
            completion(f"```lean\n{INITIAL_CANDIDATE}\n```"),
            completion("theorem target : True := by trivial"),
            completion("theorem target : True := by trivial"),
        ]
    )
    verification_fn = Mock(
        side_effect=[failed_verification(), successful_verification(), successful_verification()]
    )

    manifest = read_manifest(run_in(tmp_path, completion_fn, verification_fn, max_repair=1))
    initial = manifest["initial_candidate"]
    initial_bytes = Path(initial["candidate_path"]).read_bytes()
    initial_hash = hashlib.sha256(initial_bytes).hexdigest()

    assert initial_bytes.decode() == INITIAL_CANDIDATE
    assert initial["candidate_sha256"] == initial_hash
    assert initial["candidate_id"] == f"problem_001-{initial_hash}"
    assert initial["response_text"] == f"```lean\n{INITIAL_CANDIDATE}\n```"
    assert initial["candidate_text"] == INITIAL_CANDIDATE
    assert initial["attempt_id"].endswith("-initial")
    for condition in ("A", "B", "C"):
        result = manifest["conditions"][condition]
        assert result["starting_candidate_id"] == initial["candidate_id"]
        assert result["starting_candidate_sha256"] == initial_hash
    assert manifest["conditions"]["B"]["milestones"]["0"]["candidate_sha256"] == initial_hash
    assert manifest["conditions"]["C"]["milestones"]["0"]["candidate_sha256"] == initial_hash


def test_blind_prompt_never_receives_compiler_diagnostics(tmp_path: Path) -> None:
    prompts: list[str] = []

    def complete_fn(prompt: str, **_kwargs) -> CompletionResult:
        prompts.append(prompt)
        return completion(
            INITIAL_CANDIDATE
            if len(prompts) == 1
            else "theorem target : True := by trivial"
        )

    def verify_fn(candidate: str, *_args, **_kwargs) -> VerificationResult:
        if candidate == INITIAL_CANDIDATE:
            result = failed_verification("SECRET_DIAGNOSTIC_TEXT")
            result.errors = ["VERIFIER_EXCEPTION_DETAIL must never reach B"]
            return result
        return successful_verification()

    run_in(tmp_path, complete_fn, verify_fn, max_repair=1)

    blind_prompt = prompts[1]
    guided_prompt = prompts[2]
    assert "SECRET_DIAGNOSTIC_TEXT" not in blind_prompt
    assert "VERIFIER_EXCEPTION_DETAIL" not in blind_prompt
    assert experiment.BLIND_FEEDBACK_FIELD in blind_prompt
    assert "SECRET_DIAGNOSTIC_TEXT" in guided_prompt
    assert "VERIFIER_EXCEPTION_DETAIL" not in guided_prompt
    assert "SECRET_DIAGNOSTIC_TEXT" not in prompts[0]


def test_compiler_guided_receives_initial_and_latest_actual_diagnostics(
    tmp_path: Path,
) -> None:
    prompts: list[str] = []
    repair_responses = iter(
        [
            "theorem target : True := by trivial",
            "theorem target : True := by exact True.intro",
            "theorem target : True := by trivial",
        ]
    )

    def complete_fn(prompt: str, **_kwargs) -> CompletionResult:
        prompts.append(prompt)
        if len(prompts) == 1:
            return completion(INITIAL_CANDIDATE)
        return completion(next(repair_responses))

    def verify_fn(
        candidate: str, _project: Path, scratch_name: str, **_kwargs
    ) -> VerificationResult:
        if candidate == INITIAL_CANDIDATE:
            return failed_verification(DIAGNOSTIC_INITIAL)
        if "_B_" in scratch_name:
            return successful_verification()
        if "_C_1" in scratch_name:
            return failed_verification(DIAGNOSTIC_LATEST)
        return successful_verification()

    manifest = read_manifest(
        run_in(tmp_path, complete_fn, verify_fn, max_repair=2)
    )

    assert DIAGNOSTIC_INITIAL in prompts[2]
    assert DIAGNOSTIC_LATEST in prompts[3]
    first_payload = manifest["conditions"]["C"]["attempts"][0][
        "compiler_diagnostics_payload"
    ]
    second_payload = manifest["conditions"]["C"]["attempts"][1][
        "compiler_diagnostics_payload"
    ]
    assert json.loads(first_payload)["diagnostics"][0]["data"] == DIAGNOSTIC_INITIAL
    assert json.loads(second_payload)["diagnostics"][0]["data"] == DIAGNOSTIC_LATEST
    assert manifest["conditions"]["C"]["attempts"][0][
        "compiler_diagnostics_payload_kind"
    ] == "raw_structured_json"
    assert manifest["conditions"]["C"]["attempts"][0][
        "compiler_diagnostics_supplied_text"
    ] == first_payload
    assert first_payload in prompts[2]
    assert second_payload in prompts[3]
    assert manifest["conditions"]["C"]["status"] == "success"
    assert manifest["conditions"]["C"]["repair_calls_made"] == 2


def test_b_and_c_share_model_decoding_and_three_call_limit(tmp_path: Path) -> None:
    prompts: list[str] = []

    def complete_fn(prompt: str, **kwargs) -> CompletionResult:
        prompts.append(prompt)
        assert kwargs == {
            "max_tokens": experiment.DEFAULT_MAX_COMPLETION_TOKENS,
            "temperature": experiment.DEFAULT_TEMPERATURE,
            "retries": experiment.TRANSPORT_ATTEMPTS,
            "model": experiment.DEFAULT_MODEL,
            "reasoning_effort": "low",
        }
        candidate = INITIAL_CANDIDATE if len(prompts) == 1 else (
            f"theorem target : True := by trivial -- response {len(prompts)}"
        )
        return completion(candidate, prompt_tokens=None)

    completion_fn = Mock(side_effect=complete_fn)
    verification_fn = Mock(side_effect=lambda *_args, **_kwargs: failed_verification())

    manifest = read_manifest(run_in(tmp_path, completion_fn, verification_fn))

    assert len(prompts) == 1 + 2 * 3
    assert manifest["protocol"]["version"] == "0.2.0"
    assert manifest["protocol"]["sha256"] == experiment._protocol_metadata()[
        "sha256"
    ]
    for condition in ("B", "C"):
        result = manifest["conditions"][condition]
        assert result["repair_calls_made"] == 3
        assert len(result["attempts"]) == 3
        assert result["status"] == "repair_budget_exhausted"
        assert [item["repair_calls"] for item in result["milestones"].values()] == [0, 1, 2, 3]
        assert all(item["prompt_tokens"] is None for item in result["attempts"])
    assert manifest["configuration"]["max_repair_calls"] == 3
    assert manifest["provider"] is None
    assert manifest["configured_provider"] == "groq"
    assert manifest["model_identifier"] == experiment.DEFAULT_MODEL
    assert manifest["execution_mode"] == "mock"
    assert manifest["initial_candidate"]["generation_source"] == "mock"
    assert manifest["initial_candidate"]["requested_model"] == manifest["model_identifier"]
    assert manifest["provider"] is None
    assert manifest["configured_provider"] == "groq"
    attempts = [
        manifest["initial_candidate"],
        *(
            attempt
            for condition in ("B", "C")
            for attempt in manifest["conditions"][condition]["attempts"]
        ),
    ]
    assert len({attempt["attempt_id"] for attempt in attempts}) == len(attempts)
    assert all(
        attempt["started_at_utc"] and attempt["finished_at_utc"]
        for attempt in attempts
    )
    assert all(
        attempt["provider"] is None
        and attempt["configured_provider"] == "groq"
        and attempt["requested_model"] == manifest["model_identifier"]
        and attempt["response_text"]
        and attempt["attempt_id"]
        for condition in ("B", "C")
        for attempt in manifest["conditions"][condition]["attempts"]
    )
    assert manifest["status"] == "completed"


def test_success_stops_repairs_and_repair_prompt_hashes_are_logged(
    tmp_path: Path,
) -> None:
    completion_fn = Mock(
        side_effect=[
            completion(INITIAL_CANDIDATE),
            completion("theorem target : True := by trivial"),
            completion("theorem target : True := by trivial"),
        ]
    )
    verification_fn = Mock(
        side_effect=[failed_verification(), successful_verification(), successful_verification()]
    )

    manifest = read_manifest(run_in(tmp_path, completion_fn, verification_fn))

    assert manifest["conditions"]["B"]["repair_calls_made"] == 1
    assert manifest["conditions"]["C"]["repair_calls_made"] == 1
    assert all(item["status"] == "success" for condition in ("B", "C")
               for item in manifest["conditions"][condition]["attempts"])
    assert all(
        item["verification"]["success"] is True
        and item["finished_at_utc"]
        for condition in ("B", "C")
        for item in manifest["conditions"][condition]["attempts"]
    )
    assert all(
        len(item["prompt_sha256"]) == 64
        for condition in ("B", "C")
        for item in manifest["conditions"][condition]["attempts"]
    )
    assert manifest["status"] == "completed"


def test_empty_repair_output_is_distinct_and_stops_that_condition(
    tmp_path: Path,
) -> None:
    completion_fn = Mock(
        side_effect=[
            completion(INITIAL_CANDIDATE),
            completion(""),
            completion(""),
        ]
    )
    verification_fn = Mock(return_value=failed_verification())

    manifest = read_manifest(run_in(tmp_path, completion_fn, verification_fn))

    assert manifest["conditions"]["B"]["status"] == "empty_output"
    assert manifest["conditions"]["C"]["status"] == "empty_output"
    assert manifest["conditions"]["B"]["repair_calls_made"] == 1
    assert verification_fn.call_count == 1
    assert manifest["status"] == "completed_with_failures"


def test_provider_error_is_not_recorded_as_a_proof_failure(tmp_path: Path) -> None:
    calls = 0

    def complete_fn(_prompt: str, **_kwargs) -> CompletionResult:
        nonlocal calls
        calls += 1
        if calls == 1:
            return completion(INITIAL_CANDIDATE)
        if calls == 2:
            raise RuntimeError("provider unavailable")
        return completion("")

    manifest = read_manifest(
        run_in(tmp_path, complete_fn, lambda *_args, **_kwargs: failed_verification(), max_repair=1)
    )

    assert manifest["conditions"]["B"]["status"] == "provider_error"
    assert manifest["conditions"]["B"]["attempts"][0]["failure_kind"] == "provider_error"
    assert manifest["conditions"]["C"]["status"] == "empty_output"
    assert manifest["status"] == "completed_with_failures"


def test_provider_timeout_and_model_access_errors_are_classified_actionably() -> None:
    class ModelNotAvailableError(RuntimeError):
        status_code = 404

    timeout_record = experiment._provider_error_record(TimeoutError("timed out"))
    model_record = experiment._provider_error_record(
        ModelNotAvailableError("model unavailable")
    )

    assert timeout_record["error_category"] == "timeout"
    assert "retry only under" in timeout_record["action"]
    assert model_record["error_category"] == "model_access"
    assert model_record["status_code"] == 404
    assert "no fallback model" in model_record["action"]


def test_timeout_and_compiler_failure_are_distinct_and_timeout_is_incomplete(
    tmp_path: Path,
) -> None:
    completion_fn = Mock(return_value=completion(INITIAL_CANDIDATE))
    timeout = VerificationResult(
        success=False,
        errors=["Compilation timed out."],
        failure_kind="timeout",
    )
    verification_fn = Mock(return_value=timeout)

    manifest = read_manifest(run_in(tmp_path, completion_fn, verification_fn))

    assert manifest["initial_verification"]["status"] == "timeout"
    assert manifest["status"] == "incomplete"
    assert manifest["conditions"]["B"]["status"] == "not_run_initial_verification_unavailable"
    assert completion_fn.call_count == 1
    assert verification_fn.call_count == 1
    assert failed_verification().failure_kind == "compiler_error"


def test_interrupted_run_remains_running_not_completed(tmp_path: Path) -> None:
    def interrupt(_prompt: str, **_kwargs) -> CompletionResult:
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        run_in(
            tmp_path,
            interrupt,
            lambda *_args, **_kwargs: successful_verification(),
            experiment_id="interrupted",
        )

    manifest = read_manifest(tmp_path / "runs/interrupted/manifest.json")
    assert manifest["status"] == "running"
    assert manifest["finished_at_utc"] is None


def test_interrupted_c_call_has_its_exact_payload_persisted(tmp_path: Path) -> None:
    calls = 0
    prompts: list[str] = []

    def complete_fn(prompt: str, **_kwargs) -> CompletionResult:
        nonlocal calls
        calls += 1
        prompts.append(prompt)
        if calls == 1:
            return completion(INITIAL_CANDIDATE)
        if calls == 2:
            return completion("theorem target : True := by trivial")
        raise KeyboardInterrupt

    def verify_fn(candidate: str, *_args, **_kwargs) -> VerificationResult:
        if candidate == INITIAL_CANDIDATE:
            return failed_verification("INITIAL_RAW_DIAGNOSTIC")
        return successful_verification()

    with pytest.raises(KeyboardInterrupt):
        run_in(
            tmp_path,
            complete_fn,
            verify_fn,
            max_repair=1,
            experiment_id="interrupted-guided-call",
        )

    manifest = read_manifest(
        tmp_path / "runs/interrupted-guided-call/manifest.json"
    )
    c_attempt = manifest["conditions"]["C"]["attempts"][0]
    assert manifest["status"] == "running"
    assert c_attempt["compiler_diagnostics_payload_kind"] == "raw_structured_json"
    assert c_attempt["compiler_diagnostics_payload"] in prompts[2]
    assert c_attempt["compiler_diagnostics_payload"] == (
        c_attempt["compiler_diagnostics_supplied_text"]
    )


def test_existing_experiment_artifacts_are_not_overwritten(tmp_path: Path) -> None:
    path = run_in(
        tmp_path,
        Mock(return_value=completion(INITIAL_CANDIDATE)),
        Mock(return_value=successful_verification()),
        experiment_id="existing-run",
    )
    before = path.read_bytes()

    with pytest.raises(FileExistsError):
        run_in(
            tmp_path,
            Mock(return_value=completion("replacement")),
            Mock(return_value=successful_verification()),
            experiment_id="existing-run",
        )

    assert path.read_bytes() == before


def test_existing_output_root_is_rejected_without_modification(tmp_path: Path) -> None:
    output_root = tmp_path / "runs"
    output_root.mkdir()
    marker = output_root / "preserve.txt"
    marker.write_text("existing pilot data", encoding="utf-8")

    with pytest.raises(FileExistsError):
        experiment.run_experiment(
            "problem_001",
            THEOREM,
            tmp_path / "lean_project",
            output_root,
            completion_fn=Mock(return_value=completion(INITIAL_CANDIDATE)),
            verification_fn=Mock(return_value=successful_verification()),
            execution_mode="mock",
            experiment_id="new-run",
        )

    assert marker.read_text(encoding="utf-8") == "existing pilot data"
    assert sorted(path.name for path in output_root.iterdir()) == ["preserve.txt"]


def test_plan_only_has_prompt_hashes_and_is_explicitly_api_free() -> None:
    plan = experiment._plan("arith_001", THEOREM, experiment.DEFAULT_MODEL, 3)

    assert plan["api_calls_will_be_made"] is False
    assert plan["protocol"]["version"] == "0.2.0"
    assert plan["protocol"]["status"] == (
        "proposed_locked_for_review_not_preregistered"
    )
    assert len(plan["protocol"]["sha256"]) == 64
    assert plan["protocol"]["path"] == (
        "configs/repair_experiment_protocol_v0.2.0.json"
    )
    assert plan["provider"] == "groq"
    assert plan["model_identifier"] == experiment.DEFAULT_MODEL
    assert plan["review_record_status"] == "needs_review"
    assert plan["review_independence"] == "not_independent"
    assert plan["worst_case_call_bounds"] == {
        "initial_completion_shared_across_conditions": True,
        "maximum_logical_completions": 7,
        "wrapper_attempts_per_completion": 3,
        "groq_sdk_retries_per_wrapper_attempt": 2,
        "maximum_http_attempts_per_completion": 9,
        "maximum_http_attempts_total": 63,
    }
    assert plan["cost_guard"]["status"] == "blocked_preflight_only"
    assert plan["cost_guard"]["budget_usd"] == 0.10
    assert plan["cost_guard"]["pricing_status"] == "unverified"
    assert plan["cost_guard"]["estimated_max_cost_usd"] is None
    assert set(plan["prompt_templates"]) == {"initial", "blind", "compiler_guided"}
    assert plan["prompt_templates"] == {
        "initial": "00ec7bc08fdf14274d021a308ebc27a51e17e46198b4dbc29002b958a1e04990",
        "blind": "98f5f2ca17094874da1b89f5b4cfc4f7eff00753dc56ac8d8cb7161fdaa57745",
        "compiler_guided": "98f5f2ca17094874da1b89f5b4cfc4f7eff00753dc56ac8d8cb7161fdaa57745",
    }
    assert plan["prompt_templates"]["blind"] == plan["prompt_templates"]["compiler_guided"]
    assert experiment.BLIND_PROMPT_TEMPLATE == experiment.COMPILER_GUIDED_PROMPT_TEMPLATE


def test_protocol_rejects_runner_configuration_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(experiment, "DEFAULT_TEMPERATURE", 0.7)

    with pytest.raises(RuntimeError, match="do not match the locked protocol"):
        experiment._protocol_metadata()


def test_plan_rejects_non_protocol_repair_budget() -> None:
    with pytest.raises(ValueError, match="locked three-repair budget"):
        experiment._plan("arith_001", THEOREM, experiment.DEFAULT_MODEL, 2)


def test_plan_only_cli_does_not_start_api_or_write_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    theorem_file = tmp_path / "statement.lean"
    theorem_file.write_text(THEOREM, encoding="utf-8")
    output_root = tmp_path / "fresh-output"
    run = Mock()
    monkeypatch.setattr(experiment, "run_experiment", run)

    experiment.main(
        [
            "--problem-id",
            "problem_001",
            "--theorem-file",
            str(theorem_file),
            "--output-root",
            str(output_root),
            "--plan-only",
        ]
    )

    plan = json.loads(capsys.readouterr().out)
    run.assert_not_called()
    assert plan["api_calls_will_be_made"] is False
    assert plan["output_root_is_fresh"] is True
    assert not output_root.exists()


def test_unverified_pricing_blocks_api_before_client_or_output(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "runs"
    with patch.object(llm_client, "_get_client", side_effect=AssertionError("must not transmit")) as get_client:
        with pytest.raises(ValueError, match="pricing.*verified"):
            experiment.run_experiment(
                "problem_001",
                THEOREM,
                tmp_path / "lean_project",
                output_root,
                execution_mode="api",
                verification_fn=Mock(return_value=successful_verification()),
                experiment_id="pricing-unverified",
            )

    get_client.assert_not_called()
    assert not output_root.exists()


def test_api_key_is_not_written_to_mock_run_manifest(
    tmp_path: Path,
) -> None:
    secret = "test-secret-never-persist"
    with patch.dict("os.environ", {"GROQ_API_KEY": secret}):
        path = run_in(
            tmp_path,
            Mock(return_value=completion(INITIAL_CANDIDATE)),
            Mock(return_value=successful_verification()),
        )

    assert secret not in path.read_text(encoding="utf-8")


def test_verifier_structured_diagnostics_reach_only_c_and_are_logged_exactly(
    tmp_path: Path,
) -> None:
    raw_diagnostic = {
        "severity": "error",
        "data": "mocked Lean error",
        "pos": {"line": 8, "column": 11},
        "endPos": {"line": 8, "column": 16},
        "fileName": "generated.lean",
        "extensionField": {"kept": ["as", "returned"]},
    }
    diagnostic_line = json.dumps(raw_diagnostic)
    prompts: list[str] = []

    def complete_fn(prompt: str, **_kwargs) -> CompletionResult:
        prompts.append(prompt)
        return completion(INITIAL_CANDIDATE)

    def verification_fn(
        candidate: str, project: Path, scratch_name: str, **kwargs
    ) -> VerificationResult:
        with patch(
            "verify.subprocess.run",
            return_value=subprocess.CompletedProcess(
                [], 1, stdout=diagnostic_line, stderr=""
            ),
        ):
            return verifier.check_lean_file_detailed(
                candidate, project, scratch_name, **kwargs
            )

    manifest = read_manifest(
        run_in(
            tmp_path,
            complete_fn,
            verification_fn,
            max_repair=1,
        )
    )

    assert len(prompts) == 3
    assert "mocked Lean error" not in prompts[1]
    assert "extensionField" not in prompts[1]
    c_attempt = manifest["conditions"]["C"]["attempts"][0]
    supplied_payload = c_attempt["compiler_diagnostics_payload"]
    assert c_attempt["compiler_diagnostics_payload_kind"] == "raw_structured_json"
    assert supplied_payload in prompts[2]
    parsed_payload = json.loads(supplied_payload)
    assert parsed_payload["diagnostics"] == [raw_diagnostic]
    assert c_attempt["compiler_diagnostics_supplied_text"] == supplied_payload
    assert manifest["initial_verification"]["diagnostics"] == [raw_diagnostic]
    assert manifest["initial_verification"]["diagnostic_state"] == "available"
    initial_verification = manifest["initial_verification"]
    initial_source_bytes = initial_verification["verification_source_text"].encode("utf-8")
    assert initial_verification["verification_source_sha256"] == hashlib.sha256(
        initial_source_bytes
    ).hexdigest()
    assert initial_verification["candidate_sha256"] == manifest["initial_candidate"][
        "candidate_sha256"
    ]
    assert initial_verification["candidate_sha256"] != initial_verification[
        "verification_source_sha256"
    ]
    repair_verification = c_attempt["verification"]
    assert repair_verification["verification_source_sha256"] == hashlib.sha256(
        repair_verification["verification_source_text"].encode("utf-8")
    ).hexdigest()
    assert c_attempt["verification_source_sha256"] == repair_verification[
        "verification_source_sha256"
    ]


def test_blind_retries_continue_without_diagnostics_but_guided_condition_stops(
    tmp_path: Path,
) -> None:
    verification = VerificationResult(
        success=False,
        errors=["Lean emitted malformed diagnostics."],
        failure_kind="compiler_error",
        diagnostics=[],
        malformed_diagnostics=["not-json"],
        diagnostic_state="malformed",
    )
    prompts: list[str] = []

    def complete_fn(prompt: str, **_kwargs) -> CompletionResult:
        prompts.append(prompt)
        return completion(INITIAL_CANDIDATE)

    completion_fn = Mock(side_effect=complete_fn)
    verification_fn = Mock(return_value=verification)

    manifest = read_manifest(run_in(tmp_path, completion_fn, verification_fn))

    assert manifest["initial_verification"]["diagnostic_state"] == "malformed"
    assert manifest["initial_verification"]["malformed_diagnostics"] == ["not-json"]
    assert manifest["conditions"]["B"]["status"] == "repair_budget_exhausted"
    assert manifest["conditions"]["B"]["repair_calls_made"] == 3
    assert manifest["conditions"]["C"]["status"] == "malformed_compiler_diagnostics"
    assert completion_fn.call_count == 1 + 3
    assert verification_fn.call_count == 1 + 3
    assert "Lean emitted malformed diagnostics." not in prompts[1]


def test_api_run_is_blocked_before_missing_credentials_are_consulted(
    tmp_path: Path,
) -> None:
    with (
        patch.dict("os.environ", {"GROQ_API_KEY": ""}),
        patch.object(
            llm_client,
            "_get_client",
            side_effect=AssertionError("pricing gate must stop execution first"),
        ) as get_client,
        pytest.raises(ValueError, match="pricing.*verified"),
    ):
        experiment.run_experiment(
            "problem_001",
            THEOREM,
            tmp_path / "lean_project",
            tmp_path / "runs",
            model=experiment.DEFAULT_MODEL,
            execution_mode="api",
            verification_fn=Mock(return_value=successful_verification()),
            experiment_id="pricing-unverified",
        )

    get_client.assert_not_called()
    assert not (tmp_path / "runs").exists()


def test_injected_completion_cannot_be_labeled_as_api(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="API mode requires the Groq completion client"):
        run_in(
            tmp_path,
            Mock(return_value=completion(INITIAL_CANDIDATE)),
            Mock(return_value=successful_verification()),
            execution_mode="api",
            experiment_id="injected-as-api",
        )

    assert not (tmp_path / "runs").exists()


def test_manual_completion_is_distinct_from_api_and_mock(tmp_path: Path) -> None:
    path = run_in(
        tmp_path,
        Mock(return_value=completion(INITIAL_CANDIDATE)),
        Mock(return_value=successful_verification()),
        execution_mode="manual",
    )

    manifest = read_manifest(path)
    assert manifest["execution_mode"] == "manual"
    assert manifest["api_generation_confirmed"] is False
    assert manifest["provider"] is None
    assert manifest["initial_candidate"]["generation_source"] == "manual"


def test_invalid_repair_budget_fails_before_creating_output(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="from 0 through 3"):
        run_in(
            tmp_path,
            Mock(),
            Mock(),
            max_repair=4,
            experiment_id="invalid-budget",
        )

    assert not (tmp_path / "runs").exists()


def test_compiler_payload_drops_reference_sorry_warning() -> None:
    import json
    from types import SimpleNamespace

    verification = SimpleNamespace(
        diagnostic_state="available",
        diagnostics=[
            {"kind": "hasSorry", "severity": "warning", "data": "declaration uses `sorry`"},
            {"kind": "[anonymous]", "severity": "error", "data": "unsolved goals"},
        ],
    )

    payload = json.loads(experiment._compiler_diagnostic_payload(verification))

    assert [item["data"] for item in payload["diagnostics"]] == ["unsolved goals"]


def test_candidate_diagnostics_handles_only_reference_sorry_and_none() -> None:
    from types import SimpleNamespace

    only_sorry = SimpleNamespace(
        diagnostic_state="available",
        diagnostics=[{"kind": "hasSorry", "severity": "warning", "data": "x"}],
    )
    missing = SimpleNamespace(diagnostic_state="absent", diagnostics=None)

    assert experiment._candidate_diagnostics(only_sorry) == []
    assert experiment._candidate_diagnostics(missing) == []

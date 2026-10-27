from __future__ import annotations

import json
import os
import sys
import unittest
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import llm_client
from cost_guard import CostGuardConfig, CostReservationError, CostReservationGuard


class FakeRateLimitError(Exception):
    pass


class LlmClientRetryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api_key_patch = patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
        self.api_key_patch.start()
        self.addCleanup(self.api_key_patch.stop)
        self.sleep = Mock()
        self.create = Mock()
        self.client = SimpleNamespace(
            chat=SimpleNamespace(completions=SimpleNamespace(create=self.create))
        )
        self.rate_limit = patch.object(
            llm_client.groq, "RateLimitError", FakeRateLimitError
        )
        self.rate_limit.start()
        self.addCleanup(self.rate_limit.stop)
        self.client_patch = patch.object(llm_client, "_client", self.client)
        self.client_patch.start()
        self.addCleanup(self.client_patch.stop)

    @staticmethod
    def cost_guard(
        model: str = "llama-3.3-70b-versatile", retries: int = 3, sdk_retries: int = 2
    ) -> CostReservationGuard:
        config = CostGuardConfig(
            model_id=model,
            input_usd_per_million_tokens=Decimal("1"),
            output_usd_per_million_tokens=Decimal("1"),
            max_input_tokens=10000,
            max_output_tokens=2000,
            input_overhead_token_bound=128,
            max_cost_per_http_attempt_usd=Decimal("1"),
            per_problem_budget_usd=Decimal("100"),
            total_budget_usd=Decimal("100"),
            wrapper_attempts_per_completion=retries,
            sdk_max_retries_per_wrapper_attempt=sdk_retries,
            pricing_source_url="https://console.groq.com/docs/model/openai/gpt-oss-120b",
            pricing_retrieved_on="2026-10-21",
            pricing_currency="USD",
            pricing_review_status="human_reviewed",
            pricing_reviewed_on="2026-10-21",
            pricing_reviewer_id="test-fixture-reviewer",
            pricing_evidence_path="synthetic-test-fixture",
            pricing_evidence_sha256="a" * 64,
            input_bound_review_status="human_reviewed",
            input_bound_reviewed_on="2026-10-21",
            input_bound_reviewer_id="test-fixture-reviewer",
            input_bound_evidence="synthetic test fixture only",
        )
        return CostReservationGuard(config, persist_snapshot=lambda _snapshot: None)

    @staticmethod
    def response(
        text: str,
        *,
        finish_reason: str | None = None,
        completion_tokens: int | None = None,
        refusal: str | None = None,
        reasoning: str | None = None,
        tool_calls: object | None = None,
    ) -> SimpleNamespace:
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    finish_reason=finish_reason,
                    message=SimpleNamespace(
                        content=text,
                        refusal=refusal,
                        reasoning=reasoning,
                        tool_calls=tool_calls,
                    ),
                )
            ],
            usage=SimpleNamespace(completion_tokens=completion_tokens),
        )

    def test_repeated_parseable_rate_limits_stop_at_attempt_limit(self) -> None:
        self.create.side_effect = [
            FakeRateLimitError("Please try again in 2s."),
            FakeRateLimitError("Please try again in 2s."),
            FakeRateLimitError("Please try again in 2s."),
        ]

        with self.assertRaisesRegex(RuntimeError, "after 3 attempts") as context:
            llm_client.complete(
                "prompt", retries=3, sleep=self.sleep, cost_guard=self.cost_guard()
            )

        self.assertIsInstance(context.exception.__cause__, FakeRateLimitError)
        self.assertEqual(
            context.exception.metadata["wrapper_attempts_made"], 3
        )
        self.assertEqual(len(context.exception.metadata["wrapper_retry_events"]), 2)
        self.assertIsNone(context.exception.metadata["sdk_http_attempt_count"])
        self.assertEqual(
            context.exception.metadata["sdk_http_attempt_count_status"],
            "not_exposed_by_groq_sdk",
        )
        self.assertEqual(
            len(context.exception.metadata["cost_reservation"]["reservations"]), 9
        )
        self.assertEqual(self.create.call_count, 3)
        self.assertEqual(self.sleep.call_args_list, [((2.0,), {}), ((2.0,), {})])

    def test_permanent_http_error_is_not_retransmitted(self) -> None:
        import httpx
        error = llm_client.groq.BadRequestError(
            "SECRET provider body", response=httpx.Response(
                400, request=httpx.Request("POST", "https://api.groq.com")
            ), body=None,
        )
        self.create.side_effect = error
        with self.assertRaises(llm_client.CompletionRequestError) as caught:
            llm_client.complete("prompt", cost_guard=self.cost_guard(), sleep=self.sleep)
        self.assertEqual(self.create.call_count, 1)
        self.sleep.assert_not_called()
        self.assertNotIn("SECRET", str(caught.exception))
        self.assertEqual(caught.exception.metadata["wrapper_attempts_made"], 1)

    def test_exhausted_error_does_not_copy_provider_body(self) -> None:
        self.create.side_effect = FakeRateLimitError("SECRET provider body")
        with self.assertRaises(llm_client.CompletionRequestError) as caught:
            llm_client.complete("prompt", cost_guard=self.cost_guard(), sleep=self.sleep)
        self.assertNotIn("SECRET", str(caught.exception))

    def test_immediate_success_uses_one_total_attempt(self) -> None:
        self.create.return_value = self.response("completed")

        result = llm_client.complete(
            "prompt", retries=3, sleep=self.sleep, cost_guard=self.cost_guard()
        )

        self.assertEqual(result, "completed")
        self.assertEqual(self.create.call_count, 1)
        self.sleep.assert_not_called()

    def test_empty_content_logs_safe_response_metadata(self) -> None:
        self.create.return_value = self.response(
            "",
            finish_reason="length",
            completion_tokens=2000,
            refusal="",
            reasoning="private reasoning",
            tool_calls=[object()],
        )

        with patch("builtins.print") as printed:
            result = llm_client.complete(
                "prompt",
                model="openai/gpt-oss-20b",
                cost_guard=self.cost_guard(model="openai/gpt-oss-20b"),
            )

        self.assertEqual(result, "")
        message = printed.call_args.args[0]
        self.assertTrue(message.startswith("[llm_client] empty_response "))
        metadata = json.loads(message.removeprefix("[llm_client] empty_response "))
        self.assertEqual(metadata["model"], "openai/gpt-oss-20b")
        self.assertEqual(metadata["finish_reason"], "length")
        self.assertEqual(metadata["completion_tokens"], 2000)
        self.assertTrue(metadata["content_empty"])
        self.assertTrue(metadata["refusal_present"])
        self.assertTrue(metadata["reasoning_present"])
        self.assertEqual(metadata["reasoning_length"], len("private reasoning"))
        self.assertTrue(metadata["tool_calls_present"])
        self.assertNotIn("private reasoning", message)
        self.assertEqual(
            self.create.call_args.kwargs["max_completion_tokens"], 2000
        )
        self.assertNotIn("max_tokens", self.create.call_args.kwargs)

    def test_whitespace_content_logs_with_missing_optional_metadata(self) -> None:
        self.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=" \n\t"))]
        )

        with patch("builtins.print") as printed:
            result = llm_client.complete("prompt", cost_guard=self.cost_guard())

        self.assertEqual(result, " \n\t")
        metadata = json.loads(
            printed.call_args.args[0].removeprefix("[llm_client] empty_response ")
        )
        self.assertTrue(metadata["content_empty"])
        self.assertIsNone(metadata["finish_reason"])
        self.assertIsNone(metadata["completion_tokens"])
        self.assertFalse(metadata["refusal_present"])
        self.assertFalse(metadata["reasoning_present"])
        self.assertEqual(metadata["reasoning_length"], 0)
        self.assertFalse(metadata["tool_calls_present"])

    def test_normal_content_does_not_log_empty_response_metadata(self) -> None:
        self.create.return_value = self.response("theorem valid : True := by trivial")

        with patch("builtins.print") as printed:
            result = llm_client.complete("prompt", cost_guard=self.cost_guard())

        self.assertEqual(result, "theorem valid : True := by trivial")
        printed.assert_not_called()

    def test_missing_api_key_fails_actionably_without_request(self) -> None:
        with patch.dict(os.environ, {"GROQ_API_KEY": ""}):
            with self.assertRaisesRegex(
                llm_client.MissingGroqApiKeyError, "GROQ_API_KEY is not set"
            ):
                llm_client.complete_with_metadata(
                    "prompt", cost_guard=self.cost_guard()
                )

        self.create.assert_not_called()

    def test_missing_cost_guard_blocks_before_client_or_http_request(self) -> None:
        with (
            patch.object(llm_client, "_get_client") as get_client,
            self.assertRaisesRegex(CostReservationError, "persisted cost guard"),
        ):
            llm_client.complete_with_metadata("prompt")

        get_client.assert_not_called()
        self.create.assert_not_called()

    def test_sdk_retry_limit_is_explicit_and_matches_audited_default(self) -> None:
        fake_client = object()
        with (
            patch.object(llm_client, "_client", None),
            patch.object(llm_client.groq, "Groq", return_value=fake_client) as factory,
        ):
            client = llm_client._get_client()

        self.assertIs(client, fake_client)
        factory.assert_called_once_with(api_key="test-key", max_retries=2)

    def test_gpt_oss_reasoning_effort_is_supported_and_other_models_omit_it(self) -> None:
        self.create.return_value = self.response("proof")

        llm_client.complete_with_metadata(
            "prompt",
            model="openai/gpt-oss-20b",
            reasoning_effort=llm_client.reasoning_effort_for_model(
                "openai/gpt-oss-20b"
            ),
            cost_guard=self.cost_guard(model="openai/gpt-oss-20b"),
        )
        self.assertEqual(self.create.call_args.kwargs["reasoning_effort"], "low")

        self.create.reset_mock()
        llm_client.complete_with_metadata(
            "prompt",
            model="llama-3.1-8b-instant",
            reasoning_effort=llm_client.reasoning_effort_for_model(
                "llama-3.1-8b-instant"
            ),
            cost_guard=self.cost_guard(model="llama-3.1-8b-instant"),
        )
        self.assertNotIn("reasoning_effort", self.create.call_args.kwargs)

    def test_final_attempt_failure_uses_exactly_requested_total_attempts(self) -> None:
        self.create.side_effect = [
            FakeRateLimitError("rate limit"),
            FakeRateLimitError("rate limit"),
            FakeRateLimitError("rate limit"),
        ]

        with self.assertRaisesRegex(RuntimeError, "after 3 attempts") as context:
            llm_client.complete(
                "prompt", retries=3, sleep=self.sleep, cost_guard=self.cost_guard()
            )

        self.assertIsInstance(context.exception.__cause__, FakeRateLimitError)
        self.assertEqual(self.create.call_count, 3)
        self.assertEqual(self.sleep.call_args_list, [((1.0,), {}), ((2.0,), {})])

    def test_excessive_server_delay_fails_without_sleeping(self) -> None:
        self.create.side_effect = FakeRateLimitError("Please try again in 301s.")

        with self.assertRaisesRegex(RuntimeError, "per-retry budget") as context:
            llm_client.complete(
                "prompt",
                max_retry_after_seconds=300,
                sleep=self.sleep,
                cost_guard=self.cost_guard(),
            )

        self.assertIsInstance(context.exception.__cause__, FakeRateLimitError)
        self.sleep.assert_not_called()
        self.assertEqual(self.create.call_count, 1)

    def test_unparseable_rate_limit_uses_exponential_backoff_then_succeeds(self) -> None:
        self.create.side_effect = [
            FakeRateLimitError("rate limit"),
            FakeRateLimitError("rate limit"),
            self.response("completed"),
        ]

        result = llm_client.complete(
            "prompt", retries=3, sleep=self.sleep, cost_guard=self.cost_guard()
        )

        self.assertEqual(result, "completed")
        self.assertEqual(self.sleep.call_args_list, [((1.0,), {}), ((2.0,), {})])

    def test_parseable_rate_limit_can_eventually_succeed(self) -> None:
        self.create.side_effect = [
            FakeRateLimitError("Please try again in 4s."),
            self.response("completed"),
        ]

        result = llm_client.complete(
            "prompt", retries=2, sleep=self.sleep, cost_guard=self.cost_guard(retries=2)
        )

        self.assertEqual(result, "completed")
        self.sleep.assert_called_once_with(4.0)

    def test_cumulative_wait_budget_is_enforced(self) -> None:
        self.create.side_effect = [
            FakeRateLimitError("Please try again in 4s."),
            FakeRateLimitError("Please try again in 4s."),
        ]

        with self.assertRaisesRegex(RuntimeError, "wait budget"):
            llm_client.complete(
                "prompt",
                retries=3,
                max_total_wait_seconds=5,
                sleep=self.sleep,
                cost_guard=self.cost_guard(),
            )

        self.sleep.assert_called_once_with(4.0)
    def test_metadata_records_usage_settings_latency_and_served_model(self) -> None:
        response = self.response(
            "proof", finish_reason="stop", completion_tokens=7
        )
        response.usage.prompt_tokens = 30
        response.usage.total_tokens = 37
        response.model = "provider-served-model"
        response.system_fingerprint = "fp_abc"
        self.create.return_value = response

        result = llm_client.complete_with_metadata(
            "SECRET PROMPT TEXT",
            max_tokens=123,
            temperature=0.3,
            model="alias-model",
            reasoning_effort="low",
            cost_guard=self.cost_guard(model="alias-model"),
        )

        metadata = result.metadata
        self.assertEqual(metadata["model"], "alias-model")
        self.assertEqual(metadata["response_model"], "provider-served-model")
        self.assertEqual(metadata["system_fingerprint"], "fp_abc")
        self.assertEqual(metadata["prompt_tokens"], 30)
        self.assertEqual(metadata["completion_tokens"], 7)
        self.assertEqual(metadata["total_tokens"], 37)
        self.assertEqual(metadata["max_completion_tokens"], 123)
        self.assertEqual(metadata["temperature"], 0.3)
        self.assertEqual(metadata["reasoning_effort"], "low")
        self.assertIsInstance(metadata["latency_seconds"], float)
        self.assertGreaterEqual(metadata["latency_seconds"], 0)
        self.assertEqual(metadata["api_attempts"], 1)
        self.assertEqual(metadata["retry_events"], [])
        serialized = json.dumps(metadata)
        self.assertNotIn("SECRET PROMPT TEXT", serialized)
        self.assertNotIn("api_key", serialized.lower())

    def test_absent_optional_telemetry_is_none_not_zero(self) -> None:
        self.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="proof"))]
        )

        metadata = llm_client.complete_with_metadata(
            "prompt", cost_guard=self.cost_guard()
        ).metadata

        for field in (
            "prompt_tokens",
            "completion_tokens",
            "total_tokens",
            "response_model",
            "system_fingerprint",
            "finish_reason",
            "reasoning_effort",
        ):
            self.assertIsNone(metadata[field], field)

    def test_retry_events_record_safe_failure_details_only(self) -> None:
        rate_limit = FakeRateLimitError("Please try again in 4s. key=SECRET")
        rate_limit.status_code = 429
        self.create.side_effect = [rate_limit, self.response("completed")]

        metadata = llm_client.complete_with_metadata(
            "prompt",
            retries=2,
            sleep=self.sleep,
            cost_guard=self.cost_guard(retries=2),
        ).metadata

        self.assertEqual(metadata["api_attempts"], 2)
        self.assertEqual(
            metadata["retry_events"],
            [
                {
                    "api_attempt": 1,
                    "error_type": "FakeRateLimitError",
                    "status_code": 429,
                    "delay_seconds": 4.0,
                }
            ],
        )
        self.assertNotIn("SECRET", json.dumps(metadata))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import llm_client


class FakeRateLimitError(Exception):
    pass


class LlmClientRetryTests(unittest.TestCase):
    def setUp(self) -> None:
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
            llm_client.complete("prompt", retries=3, sleep=self.sleep)

        self.assertIsInstance(context.exception.__cause__, FakeRateLimitError)
        self.assertEqual(self.create.call_count, 3)
        self.assertEqual(self.sleep.call_args_list, [((2.0,), {}), ((2.0,), {})])

    def test_immediate_success_uses_one_total_attempt(self) -> None:
        self.create.return_value = self.response("completed")

        result = llm_client.complete("prompt", retries=3, sleep=self.sleep)

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
            result = llm_client.complete("prompt", model="openai/gpt-oss-20b")

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
            result = llm_client.complete("prompt")

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
            result = llm_client.complete("prompt")

        self.assertEqual(result, "theorem valid : True := by trivial")
        printed.assert_not_called()

    def test_gpt_oss_reasoning_effort_is_supported_and_other_models_omit_it(self) -> None:
        self.create.return_value = self.response("proof")

        llm_client.complete_with_metadata(
            "prompt",
            model="openai/gpt-oss-20b",
            reasoning_effort=llm_client.reasoning_effort_for_model(
                "openai/gpt-oss-20b"
            ),
        )
        self.assertEqual(self.create.call_args.kwargs["reasoning_effort"], "low")

        self.create.reset_mock()
        llm_client.complete_with_metadata(
            "prompt",
            model="llama-3.1-8b-instant",
            reasoning_effort=llm_client.reasoning_effort_for_model(
                "llama-3.1-8b-instant"
            ),
        )
        self.assertNotIn("reasoning_effort", self.create.call_args.kwargs)

    def test_final_attempt_failure_uses_exactly_requested_total_attempts(self) -> None:
        self.create.side_effect = [
            FakeRateLimitError("rate limit"),
            FakeRateLimitError("rate limit"),
            FakeRateLimitError("rate limit"),
        ]

        with self.assertRaisesRegex(RuntimeError, "after 3 attempts") as context:
            llm_client.complete("prompt", retries=3, sleep=self.sleep)

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

        result = llm_client.complete("prompt", retries=3, sleep=self.sleep)

        self.assertEqual(result, "completed")
        self.assertEqual(self.sleep.call_args_list, [((1.0,), {}), ((2.0,), {})])

    def test_parseable_rate_limit_can_eventually_succeed(self) -> None:
        self.create.side_effect = [
            FakeRateLimitError("Please try again in 4s."),
            self.response("completed"),
        ]

        result = llm_client.complete("prompt", retries=2, sleep=self.sleep)

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
            )

        self.sleep.assert_called_once_with(4.0)


if __name__ == "__main__":
    unittest.main()

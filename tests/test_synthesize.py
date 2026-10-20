from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from llm_client import CompletionResult
import synthesize


class SynthesizeTests(unittest.TestCase):
    @staticmethod
    def completion(text: str) -> CompletionResult:
        return CompletionResult(
            content=text,
            metadata={
                "model": synthesize.FAST_MODEL,
                "finish_reason": "stop",
                "completion_tokens": 24,
                "content_empty": not text.strip(),
                "refusal_present": False,
                "reasoning_present": False,
                "reasoning_length": 0,
                "tool_calls_present": False,
            },
        )

    def test_empty_output_skips_lean_verification_and_records_output_failure(self) -> None:
        completion = CompletionResult(
            content="  \n",
            metadata={
                "model": synthesize.FAST_MODEL,
                "finish_reason": "length",
                "completion_tokens": 2000,
                "content_empty": True,
                "refusal_present": False,
                "reasoning_present": True,
                "reasoning_length": 128,
                "tool_calls_present": False,
            },
        )
        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    synthesize,
                    "complete_with_metadata",
                    return_value=completion,
                ) as complete,
                patch.object(synthesize, "check_lean_file_detailed") as verify,
            ):
                result, attempts = synthesize.synthesize_and_verify(
                    "natural-language statement",
                    "theorem target : True := by sorry",
                    "proof sketch",
                    Path(directory),
                    "problem",
                    max_repair=2,
                )

        verify.assert_not_called()
        self.assertEqual(complete.call_count, 1)
        self.assertFalse(result["solved"])
        self.assertEqual(result["failure_stage"], "llm_output")
        self.assertEqual(result["total_synthesis_attempts"], 1)
        self.assertEqual(result["repair_attempts"], 0)
        self.assertEqual(attempts[0]["failure_stage"], "llm_output")
        self.assertEqual(attempts[0]["output_error"], synthesize.EMPTY_OUTPUT_ERROR)
        self.assertEqual(attempts[0]["compiler_errors"], [])
        self.assertIsNone(attempts[0]["verification"])
        self.assertEqual(attempts[0]["finish_reason"], "length")
        self.assertTrue(attempts[0]["content_empty"])
        self.assertTrue(attempts[0]["reasoning_present"])
        self.assertNotIn("reasoning", attempts[0])

    def test_empty_repair_output_stops_and_counts_only_calls_made(self) -> None:
        completions = [
            CompletionResult(
                content="theorem unfinished : True := by sorry",
                metadata={
                    "model": synthesize.FAST_MODEL,
                    "finish_reason": "stop",
                    "completion_tokens": 20,
                    "content_empty": False,
                    "refusal_present": False,
                    "reasoning_present": False,
                    "reasoning_length": 0,
                    "tool_calls_present": False,
                },
            ),
            CompletionResult(
                content="",
                metadata={
                    "model": synthesize.FAST_MODEL,
                    "finish_reason": "length",
                    "completion_tokens": 2000,
                    "content_empty": True,
                    "refusal_present": False,
                    "reasoning_present": True,
                    "reasoning_length": 100,
                    "tool_calls_present": False,
                },
            ),
        ]
        verification = SimpleNamespace(
            success=False,
            errors=["proof does not verify"],
            to_record=lambda: {"success": False},
        )
        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    synthesize,
                    "complete_with_metadata",
                    side_effect=completions,
                ) as complete,
                patch.object(
                    synthesize,
                    "check_lean_file_detailed",
                    return_value=verification,
                ),
            ):
                result, attempts = synthesize.synthesize_and_verify(
                    "natural-language statement",
                    "theorem target : True := by sorry",
                    "proof sketch",
                    Path(directory),
                    "problem",
                    max_repair=2,
                )

        self.assertEqual(complete.call_count, 2)
        self.assertFalse(result["solved"])
        self.assertEqual(result["failure_stage"], "llm_output")
        self.assertEqual(result["total_synthesis_attempts"], 2)
        self.assertEqual(result["repair_attempts"], 1)
        self.assertEqual(
            [attempt["is_initial_synthesis"] for attempt in attempts],
            [True, False],
        )
        self.assertEqual(
            [attempt["repair_number"] for attempt in attempts],
            [0, 1],
        )

    def test_initial_success_records_one_synthesis_call_and_no_repairs(self) -> None:
        verification = SimpleNamespace(
            success=True,
            errors=[],
            to_record=lambda: {"success": True},
        )
        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    synthesize,
                    "complete_with_metadata",
                    return_value=self.completion(
                        "theorem target : True := by trivial"
                    ),
                ) as complete,
                patch.object(
                    synthesize,
                    "check_lean_file_detailed",
                    return_value=verification,
                ),
            ):
                result, attempts = synthesize.synthesize_and_verify(
                    "natural-language statement",
                    "theorem target : True := by sorry",
                    "proof sketch",
                    Path(directory),
                    "problem",
                    max_repair=2,
                )

        self.assertTrue(result["solved"])
        self.assertTrue(result["initial_synthesis_success"])
        self.assertTrue(result["success_within_repair_budget"])
        self.assertEqual(result["total_synthesis_attempts"], 1)
        self.assertEqual(result["repair_attempts"], 0)
        self.assertEqual(complete.call_count, 1)
        self.assertEqual(attempts[0]["completion_tokens"], 24)
        self.assertFalse(attempts[0]["content_empty"])

    def test_success_after_repair_counts_two_calls_and_one_repair(self) -> None:
        verifications = [
            SimpleNamespace(
                success=False,
                errors=["proof needs repair"],
                to_record=lambda: {"success": False},
            ),
            SimpleNamespace(
                success=True,
                errors=[],
                to_record=lambda: {"success": True},
            ),
        ]
        with TemporaryDirectory() as directory:
            with (
                patch.object(
                    synthesize,
                    "complete_with_metadata",
                    side_effect=[
                        self.completion("theorem target : True := by"),
                        self.completion("theorem target : True := by trivial"),
                    ],
                ) as complete,
                patch.object(
                    synthesize,
                    "check_lean_file_detailed",
                    side_effect=verifications,
                ),
            ):
                result, attempts = synthesize.synthesize_and_verify(
                    "natural-language statement",
                    "theorem target : True := by sorry",
                    "proof sketch",
                    Path(directory),
                    "problem",
                    max_repair=2,
                )

        self.assertTrue(result["solved"])
        self.assertFalse(result["initial_synthesis_success"])
        self.assertTrue(result["success_within_repair_budget"])
        self.assertEqual(result["total_synthesis_attempts"], 2)
        self.assertEqual(result["repair_attempts"], 1)
        self.assertEqual(complete.call_count, 2)
        self.assertEqual(
            [attempt["is_initial_synthesis"] for attempt in attempts],
            [True, False],
        )


if __name__ == "__main__":
    unittest.main()

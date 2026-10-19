from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import synthesize


class SynthesizeTests(unittest.TestCase):
    def test_empty_output_skips_lean_verification_and_records_output_failure(self) -> None:
        with TemporaryDirectory() as directory:
            with (
                patch.object(synthesize, "complete", return_value=" \n\t "),
                patch.object(synthesize, "check_lean_file_detailed") as verify,
            ):
                result, attempts = synthesize.synthesize_and_verify(
                    "natural-language statement",
                    "theorem target : True := by sorry",
                    "proof sketch",
                    Path(directory),
                    "problem",
                    max_repair=0,
                )

        verify.assert_not_called()
        self.assertFalse(result["solved"])
        self.assertEqual(result["failure_stage"], "llm_output")
        self.assertEqual(attempts[0]["failure_stage"], "llm_output")
        self.assertEqual(attempts[0]["output_error"], synthesize.EMPTY_OUTPUT_ERROR)
        self.assertEqual(attempts[0]["compiler_errors"], [])
        self.assertIsNone(attempts[0]["verification"])


if __name__ == "__main__":
    unittest.main()

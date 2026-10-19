from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from verify import check_lean_file_detailed


def json_diagnostic(severity: str, data: str = "", line: int = 1) -> str:
    return f'{{"severity": "{severity}", "data": "{data}", "pos": {{"line": {line}}}}}'


class VerifyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = TemporaryDirectory()
        self.project = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_result(
        self, code: str, process: subprocess.CompletedProcess[str], *, allow_sorry: bool = False
    ):
        with patch("verify.subprocess.run", return_value=process):
            return check_lean_file_detailed(code, self.project, "candidate", allow_sorry)

    def test_valid_named_theorem_with_allowed_axioms_succeeds(self) -> None:
        process = subprocess.CompletedProcess(
            [],
            0,
            stdout=json_diagnostic(
                "information",
                "'valid' depends on axioms: [propext, Classical.choice, Quot.sound]",
            ),
            stderr="",
        )
        result = self.run_result("theorem valid : True := by trivial", process)
        self.assertTrue(result.success)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.axiom_dependencies, ["propext", "Classical.choice", "Quot.sound"])

    def test_unapproved_axiom_dependency_fails(self) -> None:
        process = subprocess.CompletedProcess(
            [],
            0,
            stdout=json_diagnostic(
                "information",
                "'valid' depends on axioms: [propext, attacker.unsound]",
            ),
            stderr="",
        )
        result = self.run_result("theorem valid : True := by trivial", process)
        self.assertFalse(result.success)
        self.assertIn("attacker.unsound", result.errors[0])

    def test_invalid_lean_error_fails(self) -> None:
        process = subprocess.CompletedProcess(
            [], 1, stdout=json_diagnostic("error", "unexpected token", 3), stderr=""
        )
        result = self.run_result("theorem bad : True := by", process)
        self.assertFalse(result.success)
        self.assertIn("line 3", result.errors[0])

    def test_dependency_failure_with_empty_output_fails(self) -> None:
        result = self.run_result(
            "theorem bad : True := by trivial",
            subprocess.CompletedProcess([], 1, stdout="", stderr="dependency failure"),
        )
        self.assertFalse(result.success)
        self.assertIn("nonzero without a parseable", result.errors[0])

    def test_nonzero_unparseable_output_fails(self) -> None:
        result = self.run_result(
            "theorem bad : True := by trivial",
            subprocess.CompletedProcess([], 1, stdout="not JSON", stderr=""),
        )
        self.assertFalse(result.success)
        self.assertIn("nonzero without a parseable", result.errors[0])

    def test_malformed_json_on_zero_exit_fails(self) -> None:
        result = self.run_result(
            "theorem bad : True := by trivial",
            subprocess.CompletedProcess([], 0, stdout="not JSON", stderr=""),
        )
        self.assertFalse(result.success)
        self.assertIn("malformed", result.errors[0])

    def test_success_with_ambiguous_stderr_fails(self) -> None:
        result = self.run_result(
            "theorem bad : True := by trivial",
            subprocess.CompletedProcess(
                [],
                0,
                stdout=json_diagnostic("information", "'bad' does not depend on any axioms"),
                stderr="unexpected dependency warning",
            ),
        )
        self.assertFalse(result.success)
        self.assertIn("ambiguous stderr", result.errors[0])

    def test_success_with_warning_stderr_is_accepted(self) -> None:
        result = self.run_result(
            "theorem valid : True := by trivial",
            subprocess.CompletedProcess(
                [],
                0,
                stdout=json_diagnostic("information", "'valid' does not depend on any axioms"),
                stderr="warning: harmless environment message",
            ),
        )
        self.assertTrue(result.success)

    def test_timeout_fails(self) -> None:
        with patch("verify.subprocess.run", side_effect=subprocess.TimeoutExpired([], 60)):
            result = check_lean_file_detailed("theorem valid : True := by trivial", self.project, "candidate")
        self.assertFalse(result.success)
        self.assertIn("timed out", result.errors[0])

    def test_missing_executable_fails(self) -> None:
        with patch("verify.subprocess.run", side_effect=FileNotFoundError("lake")):
            result = check_lean_file_detailed("theorem valid : True := by trivial", self.project, "candidate")
        self.assertFalse(result.success)
        self.assertIn("Could not invoke Lean", result.errors[0])

    def test_placeholder_tokens_are_rejected_for_final_proofs(self) -> None:
        process = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        for token in ("sorry", "admit", "sorryAx"):
            with self.subTest(token=token):
                result = self.run_result(f"theorem bad : True := by {token}", process)
                self.assertFalse(result.success)
                self.assertIn(token, result.errors[0])

    def test_injected_axiom_is_rejected_before_compilation(self) -> None:
        process = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        result = self.run_result(
            "axiom unsound : False\ntheorem bad : True := False.elim unsound", process
        )
        self.assertFalse(result.success)
        self.assertIn("axiom", result.errors[0])

    def test_scratch_name_cannot_escape_scratch_directory(self) -> None:
        process = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        with patch("verify.subprocess.run", return_value=process):
            result = check_lean_file_detailed(
                "theorem valid : True := by trivial",
                self.project,
                "../outside",
            )
        self.assertFalse(result.success)
        self.assertIn("path separator", result.errors[0])
        self.assertFalse((self.project / "generated").exists())

    def test_unrelated_axiom_diagnostic_does_not_satisfy_inspection(self) -> None:
        result = self.run_result(
            "theorem valid : True := by trivial",
            subprocess.CompletedProcess(
                [],
                0,
                stdout=json_diagnostic(
                    "information", "'other' does not depend on any axioms"
                ),
                stderr="",
            ),
        )
        self.assertFalse(result.success)
        self.assertIn("axiom inspection", result.errors[0])

    def test_stage_a_allows_sorry_but_not_admit(self) -> None:
        process = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        with patch("verify.subprocess.run", return_value=process):
            accepted = check_lean_file_detailed(
                "theorem statement_only : True := by sorry",
                self.project,
                "statement",
                allow_sorry=True,
            )
        self.assertTrue(accepted.success)
        rejected = self.run_result(
            "theorem statement_only : True := by admit", process, allow_sorry=True
        )
        self.assertFalse(rejected.success)

    @unittest.skipUnless(which("lake"), "lake is not installed")
    def test_real_lean_accepts_a_valid_theorem(self) -> None:
        project = Path(__file__).parents[1] / "lean_project"
        scratch = project / "generated" / "_scratch" / "test_verify_integration.lean"
        try:
            result = check_lean_file_detailed(
                "theorem test_verify_integration : True := by trivial",
                project,
                "test_verify_integration",
            )
        finally:
            scratch.unlink(missing_ok=True)
        self.assertTrue(result.success, result.errors)
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()

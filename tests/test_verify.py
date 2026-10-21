from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory
from unittest.mock import patch
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from verify import (
    DEFAULT_POLICY,
    VerificationPolicy,
    check_lean_file_detailed,
    promote_scratch_to_final,
)


def json_diagnostic(severity: str, data: str = "", line: int = 1) -> str:
    return f'{{"severity": "{severity}", "data": "{data}", "pos": {{"line": {line}}}}}'


class VerifyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = TemporaryDirectory()
        self.project = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_default_timeout_has_headroom_for_pinned_mathlib_startup(self) -> None:
        # A valid theorem took 63.64 seconds to verify in the pinned environment.
        self.assertGreaterEqual(DEFAULT_POLICY.timeout_seconds, 120)
        self.assertEqual(
            DEFAULT_POLICY.timeout_seconds,
            VerificationPolicy().timeout_seconds,
        )

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

    def test_expected_statement_selects_matching_theorem_not_first_theorem(self) -> None:
        code = (
            "theorem helper : True := by trivial\n"
            "theorem target (n : Nat) : n = n := by rfl"
        )
        expected = "theorem target (n : Nat) : n = n := by sorry"

        def compile_candidate(command, **_kwargs):
            source = Path(command[-1]).read_text()
            self.assertIn(
                "example : Nl2LeanExpected.target = Nl2LeanCandidate.target := by",
                source,
            )
            self.assertIn("#print axioms Nl2LeanCandidate.target", source)
            return subprocess.CompletedProcess(
                command,
                0,
                stdout=json_diagnostic(
                    "information",
                    "'Nl2LeanCandidate.target' does not depend on any axioms",
                ),
                stderr="",
            )

        with patch("verify.subprocess.run", side_effect=compile_candidate):
            result = check_lean_file_detailed(
                code,
                self.project,
                "statement_match",
                expected_statement=expected,
            )

        self.assertTrue(result.success, result.errors)
        self.assertEqual(result.axiom_dependencies, [])

    def test_expected_statement_mismatch_fails_lean_type_check(self) -> None:
        code = "theorem target : False := by contradiction"
        expected = "theorem target : True := by sorry"

        def compile_candidate(command, **_kwargs):
            source = Path(command[-1]).read_text()
            self.assertIn(
                "example : Nl2LeanExpected.target = Nl2LeanCandidate.target := by",
                source,
            )
            return subprocess.CompletedProcess(
                command,
                1,
                stdout=json_diagnostic("error", "type mismatch", 12),
                stderr="",
            )

        with patch("verify.subprocess.run", side_effect=compile_candidate):
            result = check_lean_file_detailed(
                code,
                self.project,
                "statement_mismatch",
                expected_statement=expected,
            )

        self.assertFalse(result.success)
        self.assertIn("type mismatch", result.errors[0])
        self.assertEqual(result.diagnostic_state, "available")

    def test_source_hash_matches_exact_written_bytes_and_candidate_hash_is_separate(self) -> None:
        candidate = "theorem target : True := by trivial"
        expected = "theorem target : True := by sorry"
        captured: dict[str, bytes] = {}
        raw_diagnostic = {
            "severity": "error",
            "data": "type mismatch",
            "pos": {"line": 4, "column": 7},
            "endPos": {"line": 4, "column": 12},
            "fileName": "Generated.lean",
            "customField": {"preserved": True},
        }

        def compile_candidate(command, **_kwargs):
            source_path = Path(command[-1])
            captured["source"] = source_path.read_bytes()
            return subprocess.CompletedProcess(
                command, 1, stdout=json.dumps(raw_diagnostic), stderr=""
            )

        with patch("verify.subprocess.run", side_effect=compile_candidate):
            result = check_lean_file_detailed(
                candidate,
                self.project,
                "exact_source",
                expected_statement=expected,
            )

        source_bytes = captured["source"]
        self.assertEqual(
            result.verification_source_sha256,
            hashlib.sha256(source_bytes).hexdigest(),
        )
        self.assertEqual(result.verification_source_text.encode("utf-8"), source_bytes)
        self.assertEqual(
            result.candidate_sha256,
            hashlib.sha256(candidate.encode("utf-8")).hexdigest(),
        )
        self.assertNotEqual(result.candidate_sha256, result.verification_source_sha256)
        self.assertEqual(result.diagnostics, [raw_diagnostic])
        self.assertEqual(result.diagnostic_state, "available")
        self.assertEqual(result.diagnostic_text, "line 4: type mismatch")

    def test_expected_statement_path_preserves_final_proof_safety_policy(self) -> None:
        expected = "theorem target : True := by sorry"
        for code, token in (
            ("theorem target : True := by sorryAx", "sorryAx"),
            ("theorem target : True := by admit", "admit"),
            ("opaque hidden : False\ntheorem target : True := by trivial", "opaque"),
            ("constant hidden : False\ntheorem target : True := by trivial", "constant"),
            ("axiom hidden : False\ntheorem target : True := by trivial", "axiom"),
        ):
            with self.subTest(token=token):
                result = check_lean_file_detailed(
                    code,
                    self.project,
                    f"unsafe_{token}",
                    expected_statement=expected,
                )
                self.assertFalse(result.success)
                self.assertIn(token, result.errors[0])

    def test_expected_statement_path_rejects_unapproved_theorem_axioms(self) -> None:
        with patch(
            "verify.subprocess.run",
            return_value=subprocess.CompletedProcess(
                [],
                0,
                stdout=json_diagnostic(
                    "information",
                    "'Nl2LeanCandidate.target' depends on axioms: "
                    "[propext, attacker.unsound]",
                ),
                stderr="",
            ),
        ):
            result = check_lean_file_detailed(
                "theorem target : True := by trivial",
                self.project,
                "unapproved_expected_axiom",
                expected_statement="theorem target : True := by sorry",
            )
        self.assertFalse(result.success)
        self.assertIn("attacker.unsound", result.errors[0])

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
        self.assertEqual(result.failure_kind, "compiler_error")
        self.assertEqual(result.diagnostic_text, result.errors[0])

    def test_dependency_failure_with_empty_output_fails(self) -> None:
        result = self.run_result(
            "theorem bad : True := by trivial",
            subprocess.CompletedProcess([], 1, stdout="", stderr="dependency failure"),
        )
        self.assertFalse(result.success)
        self.assertIn("nonzero without a parseable", result.errors[0])
        self.assertEqual(result.failure_kind, "infrastructure_error")

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
        self.assertEqual(result.diagnostic_state, "malformed")
        self.assertEqual(result.malformed_diagnostics, ["not JSON"])
        self.assertEqual(result.diagnostics, [])

    def test_absent_diagnostics_are_explicit(self) -> None:
        result = self.run_result(
            "theorem bad : True := by trivial",
            subprocess.CompletedProcess([], 0, stdout="", stderr=""),
            allow_sorry=True,
        )
        self.assertTrue(result.success)
        self.assertEqual(result.diagnostic_state, "absent")
        self.assertEqual(result.diagnostics, [])

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
        self.assertEqual(result.failure_kind, "infrastructure_error")

    def test_lean_timeout_is_classified_separately(self) -> None:
        with patch(
            "verify.subprocess.run",
            side_effect=subprocess.TimeoutExpired(["lake", "lean"], 60),
        ):
            result = check_lean_file_detailed(
                "theorem valid : True := by trivial", self.project, "lean_timeout"
            )
        self.assertFalse(result.success)
        self.assertEqual(result.failure_kind, "timeout")
        self.assertEqual(result.diagnostic_state, "unavailable")
        self.assertIsNone(result.diagnostics)

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

    def test_existing_run_specific_final_proof_fails_without_overwrite(self) -> None:
        scratch = self.project / "generated" / "_scratch" / "candidate.lean"
        destination = self.project / "generated" / "runs" / "run-1"
        scratch.parent.mkdir(parents=True)
        destination.mkdir(parents=True)
        scratch.write_text("theorem candidate : True := by trivial")
        existing = destination / "proof.lean"
        existing.write_text("existing proof")

        with self.assertRaises(FileExistsError):
            promote_scratch_to_final(self.project, "candidate", "proof", destination)

        self.assertEqual(existing.read_text(), "existing proof")

    def test_shared_runs_root_is_not_a_final_proof_destination(self) -> None:
        scratch = self.project / "generated" / "_scratch" / "candidate.lean"
        destination = self.project / "generated" / "runs"
        scratch.parent.mkdir(parents=True)
        destination.mkdir(parents=True)
        scratch.write_text("theorem candidate : True := by trivial")

        with self.assertRaises(ValueError):
            promote_scratch_to_final(self.project, "candidate", "proof", destination)

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

    @unittest.skipUnless(which("lake"), "lake is not installed")
    def test_real_lean_checks_stage_a_statement_and_selects_named_theorem(self) -> None:
        project = Path(__file__).parents[1] / "lean_project"
        scratch_dir = project / "generated" / "_scratch"
        suffix = uuid4().hex
        scratch_names = (
            f"test_verify_statement_match_{suffix}",
            f"test_verify_statement_mismatch_{suffix}",
        )
        try:
            matching = check_lean_file_detailed(
                "theorem helper : True := by trivial\n"
                "theorem target (n : Nat) : n = n := by rfl",
                project,
                scratch_names[0],
                expected_statement=(
                    "theorem target (n : Nat) : n = n := by sorry"
                ),
            )
            mismatch = check_lean_file_detailed(
                "theorem target : 1 = 1 := by rfl",
                project,
                scratch_names[1],
                expected_statement="theorem target : True := by sorry",
            )
        finally:
            for scratch_name in scratch_names:
                (scratch_dir / f"{scratch_name}.lean").unlink(missing_ok=True)

        self.assertTrue(matching.success, matching.errors)
        self.assertFalse(mismatch.success)
        self.assertTrue(mismatch.errors)


if __name__ == "__main__":
    unittest.main()

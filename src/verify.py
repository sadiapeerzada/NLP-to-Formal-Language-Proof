"""Run generated Lean candidates through a strict, auditable verifier."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class VerificationPolicy:
    """Source-level policy for generated final-proof candidates.

    Lean's kernel accepts declarations introduced with `axiom`, `constant`,
    and opaque declarations without a value. Generated candidates are not
    allowed to introduce any of them. This deliberately does not ban tactics
    such as `native_decide` or commands such as `set_option`.

    `allowed_axioms` contains Lean's standard trusted classical axioms. Any
    additional theorem dependency reported by `#print axioms` is rejected.
    """

    prohibited_proof_tokens: tuple[str, ...] = ("sorry", "sorryAx", "admit")
    prohibited_declarations: tuple[str, ...] = ("axiom", "constant", "opaque")
    allowed_axioms: tuple[str, ...] = (
        "propext",
        "Classical.choice",
        "Quot.sound",
    )
    timeout_seconds: int = 60
    inspect_axioms: bool = True


DEFAULT_POLICY = VerificationPolicy()
_BENIGN_STDERR_LINE = re.compile(r"^(warning|info):", re.IGNORECASE)


@dataclass
class VerificationResult:
    success: bool
    errors: list[str] = field(default_factory=list)
    exit_code: int | None = None
    elapsed_seconds: float = 0.0
    diagnostics_parsed: int = 0
    axiom_dependencies: list[str] | None = None
    failure_kind: str | None = None
    diagnostic_text: str | None = None
    candidate_sha256: str | None = None
    verification_source_text: str | None = None
    verification_source_sha256: str | None = None
    diagnostics: list[dict[str, object]] | None = None
    malformed_diagnostics: list[str] = field(default_factory=list)
    diagnostic_state: str = "unavailable"

    def to_record(self) -> dict[str, object]:
        return {
            "success": self.success,
            "errors": self.errors,
            "exit_code": self.exit_code,
            "elapsed_seconds": round(self.elapsed_seconds, 3),
            "diagnostics_parsed": self.diagnostics_parsed,
            "axiom_dependencies": self.axiom_dependencies,
            "failure_kind": self.failure_kind,
            "diagnostic_text": self.diagnostic_text,
            "candidate_sha256": self.candidate_sha256,
            "verification_source_text": self.verification_source_text,
            "verification_source_sha256": self.verification_source_sha256,
            "diagnostics": self.diagnostics,
            "malformed_diagnostics": self.malformed_diagnostics,
            "diagnostic_state": self.diagnostic_state,
        }


def _find_prohibited_source(
    lean_code: str, allow_sorry: bool, policy: VerificationPolicy
) -> str | None:
    for token in policy.prohibited_proof_tokens:
        if allow_sorry and token == "sorry":
            continue
        if re.search(rf"\b{re.escape(token)}\b", lean_code):
            return token

    for declaration in policy.prohibited_declarations:
        if re.search(rf"(?m)^\s*{re.escape(declaration)}\b", lean_code):
            return declaration
    return None


def _theorem_name(lean_code: str) -> str | None:
    match = re.search(r"(?m)^\s*theorem\s+([A-Za-z_][A-Za-z0-9_'.]*)\b", lean_code)
    return match.group(1) if match else None


def _theorem_names(lean_code: str) -> list[str]:
    return re.findall(
        r"(?m)^\s*theorem\s+([A-Za-z_][A-Za-z0-9_'.]*)\b",
        lean_code,
    )


def _verification_source(
    lean_code: str,
    expected_statement: str,
    theorem_name: str,
    *,
    inspect_axioms: bool,
) -> tuple[str, str]:
    imports: set[str] = set()

    def remove_imports(source: str) -> str:
        def collect(match: re.Match[str]) -> str:
            imports.update(match.group(1).split())
            return ""

        return re.sub(r"(?m)^\s*import\s+([^\n]+)\s*$", collect, source)

    expected_source = remove_imports(expected_statement)
    candidate_source = remove_imports(lean_code)
    if "Mathlib" not in imports:
        imports.add("Mathlib")

    expected_theorem = f"Nl2LeanExpected.{theorem_name}"
    candidate_theorem = f"Nl2LeanCandidate.{theorem_name}"
    source = (
        "\n".join(f"import {module}" for module in sorted(imports))
        + "\n\nnamespace Nl2LeanExpected\n"
        + expected_source
        + "\nend Nl2LeanExpected\n\nnamespace Nl2LeanCandidate\n"
        + candidate_source
        + "\nend Nl2LeanCandidate\n\n"
        + f"example : {expected_theorem} = {candidate_theorem} := by\n"
        + "  exact Subsingleton.elim _ _\n"
    )
    if inspect_axioms:
        source += f"#print axioms {candidate_theorem}\n"
    return source, candidate_theorem


def _diagnostics(stdout: str) -> tuple[list[dict[str, object]], list[str]]:
    diagnostics = []
    malformed = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            malformed.append(line)
            continue
        if not isinstance(message, dict) or not isinstance(message.get("severity"), str):
            malformed.append(line)
            continue
        diagnostics.append(message)
    return diagnostics, malformed


def _format_diagnostic(message: dict[str, object]) -> str:
    position = message.get("pos")
    line = position.get("line", "?") if isinstance(position, dict) else "?"
    return f"line {line}: {message.get('data', '')}"


def _axioms_from_diagnostics(
    diagnostics: list[dict[str, object]], theorem_name: str
) -> list[str] | None:
    expected_prefix = f"'{theorem_name}' "
    for diagnostic in diagnostics:
        data = diagnostic.get("data")
        if not isinstance(data, str) or not data.startswith(expected_prefix):
            continue
        if "axioms:" not in data:
            if "does not depend on any axioms" in data:
                return []
            continue
        match = re.search(r"axioms:\s*\[([^\]]*)\]", data)
        if match is None:
            return None
        return [item.strip() for item in match.group(1).split(",") if item.strip()]
    return None


def _safe_filename_component(value: str) -> bool:
    return (
        bool(value)
        and value not in {".", ".."}
        and Path(value).name == value
        and "\\" not in value
    )


def _stderr_error(stderr: str) -> str | None:
    lines = [line for line in stderr.splitlines() if line.strip()]
    if not lines:
        return None
    ambiguous = [line for line in lines if not _BENIGN_STDERR_LINE.match(line)]
    if ambiguous:
        return "Lean exited successfully but wrote ambiguous stderr: " + "\n".join(ambiguous)
    return None


def check_lean_file_detailed(
    lean_code: str,
    lean_project_dir: Path,
    scratch_name: str,
    allow_sorry: bool = False,
    policy: VerificationPolicy = DEFAULT_POLICY,
    expected_statement: str | None = None,
) -> VerificationResult:
    """Compile one candidate and, for final proofs, inspect theorem axioms.

    Successful exit status is necessary but not sufficient: malformed JSON
    diagnostics, compiler errors, unavailable executables, and unparseable
    axiom inspection all fail closed. Stage A uses ``allow_sorry=True`` to
    check only statement elaboration; final proofs must be named theorems so
    their dependencies can be checked with Lean's ``#print axioms`` command.
    When ``expected_statement`` is supplied, Lean must also establish that
    the named final theorem has the same elaborated type as Stage A.
    """
    candidate_sha256 = hashlib.sha256(lean_code.encode("utf-8")).hexdigest()
    prohibited = _find_prohibited_source(lean_code, allow_sorry, policy)
    if prohibited:
        return VerificationResult(
            False,
            [
                f"Candidate rejected before compilation: prohibited source token "
                f"or declaration '{prohibited}'."
            ],
            failure_kind="proof_rejected",
            candidate_sha256=candidate_sha256,
        )

    theorem_name = _theorem_name(lean_code)
    if not allow_sorry and policy.inspect_axioms and theorem_name is None:
        return VerificationResult(
            False,
            ["Final proof must declare a named theorem for axiom inspection."],
            failure_kind="proof_rejected",
            candidate_sha256=candidate_sha256,
        )

    if expected_statement is not None:
        expected_names = _theorem_names(expected_statement)
        if len(expected_names) != 1:
            return VerificationResult(
                False,
                [
                    "Stage A statement must declare exactly one named theorem "
                    "for final statement comparison."
                ],
                failure_kind="input_error",
                candidate_sha256=candidate_sha256,
            )
        theorem_name = expected_names[0]
        if _theorem_names(lean_code).count(theorem_name) != 1:
            return VerificationResult(
                False,
                [
                    "Final proof must declare the Stage A theorem "
                    f"'{theorem_name}' exactly once."
                ],
                failure_kind="proof_rejected",
                candidate_sha256=candidate_sha256,
            )
        source, theorem_name = _verification_source(
            lean_code,
            expected_statement,
            theorem_name,
            inspect_axioms=not allow_sorry and policy.inspect_axioms,
        )
    else:
        source = lean_code
        if "import Mathlib" not in source:
            source = "import Mathlib\n\n" + source
        if not allow_sorry and policy.inspect_axioms:
            source = f"{source.rstrip()}\n\n#print axioms {theorem_name}\n"

    if not _safe_filename_component(scratch_name):
        return VerificationResult(
            False,
            ["Scratch name must not contain a path separator."],
            failure_kind="input_error",
            candidate_sha256=candidate_sha256,
        )
    lean_project_dir = Path(lean_project_dir).resolve()
    scratch_dir = lean_project_dir / "generated" / "_scratch"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    file_path = scratch_dir / f"{scratch_name}.lean"
    source_bytes = source.encode("utf-8")
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    file_path.write_bytes(source_bytes)
    source_provenance = {
        "candidate_sha256": candidate_sha256,
        "verification_source_text": source_bytes.decode("utf-8"),
        "verification_source_sha256": source_sha256,
    }

    started = time.monotonic()
    try:
        process = subprocess.run(
            ["lake", "env", "lean", "--json", str(file_path)],
            cwd=str(lean_project_dir),
            capture_output=True,
            text=True,
            timeout=policy.timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return VerificationResult(
            False,
            [f"Compilation timed out after {policy.timeout_seconds}s."],
            elapsed_seconds=time.monotonic() - started,
            failure_kind="timeout",
            **source_provenance,
        )
    except OSError as error:
        return VerificationResult(
            False,
            [f"Could not invoke Lean via lake: {error}"],
            elapsed_seconds=time.monotonic() - started,
            failure_kind="infrastructure_error",
            **source_provenance,
        )

    elapsed = time.monotonic() - started
    diagnostics, malformed = _diagnostics(process.stdout or "")
    diagnostic_state = (
        "malformed" if malformed else "available" if diagnostics else "absent"
    )
    diagnostic_provenance = {
        "diagnostics": diagnostics,
        "malformed_diagnostics": malformed,
        "diagnostic_state": diagnostic_state,
    }
    errors = [
        _format_diagnostic(diagnostic)
        for diagnostic in diagnostics
        if diagnostic["severity"] == "error"
    ]

    if process.returncode != 0:
        has_compiler_errors = bool(errors)
        if not errors:
            errors.append(
                "Lean exited nonzero without a parseable error diagnostic. "
                f"stderr: {process.stderr.strip() or '<empty>'}"
            )
        return VerificationResult(
            False,
            errors,
            exit_code=process.returncode,
            elapsed_seconds=elapsed,
            diagnostics_parsed=len(diagnostics),
            failure_kind="compiler_error" if has_compiler_errors else "infrastructure_error",
            diagnostic_text="\n".join(errors) if has_compiler_errors else None,
            **source_provenance,
            **diagnostic_provenance,
        )

    if malformed:
        return VerificationResult(
            False,
            ["Lean emitted malformed or uninterpretable JSON diagnostics."],
            exit_code=process.returncode,
            elapsed_seconds=elapsed,
            diagnostics_parsed=len(diagnostics),
            failure_kind="verifier_error",
            **source_provenance,
            **diagnostic_provenance,
        )

    stderr_error = _stderr_error(process.stderr or "")
    if stderr_error:
        return VerificationResult(
            False,
            [stderr_error],
            exit_code=process.returncode,
            elapsed_seconds=elapsed,
            diagnostics_parsed=len(diagnostics),
            failure_kind="infrastructure_error",
            **source_provenance,
            **diagnostic_provenance,
        )

    if errors:
        return VerificationResult(
            False,
            errors,
            exit_code=process.returncode,
            elapsed_seconds=elapsed,
            diagnostics_parsed=len(diagnostics),
            failure_kind="compiler_error",
            diagnostic_text="\n".join(errors),
            **source_provenance,
            **diagnostic_provenance,
        )

    axiom_dependencies = None
    if not allow_sorry and policy.inspect_axioms:
        axiom_dependencies = _axioms_from_diagnostics(diagnostics, theorem_name)
        if axiom_dependencies is None:
            return VerificationResult(
                False,
                ["Lean axiom inspection did not produce a parseable dependency list."],
                exit_code=process.returncode,
                elapsed_seconds=elapsed,
                diagnostics_parsed=len(diagnostics),
                failure_kind="verifier_error",
                **source_provenance,
                **diagnostic_provenance,
            )
        unapproved = sorted(set(axiom_dependencies) - set(policy.allowed_axioms))
        if unapproved:
            return VerificationResult(
                False,
                [f"Final theorem depends on unapproved axioms: {', '.join(unapproved)}."],
                exit_code=process.returncode,
                elapsed_seconds=elapsed,
                diagnostics_parsed=len(diagnostics),
                axiom_dependencies=axiom_dependencies,
                failure_kind="proof_rejected",
                **source_provenance,
                **diagnostic_provenance,
            )

    return VerificationResult(
        True,
        exit_code=process.returncode,
        elapsed_seconds=elapsed,
        diagnostics_parsed=len(diagnostics),
        axiom_dependencies=axiom_dependencies,
        **source_provenance,
        **diagnostic_provenance,
    )


def check_lean_file(
    lean_code: str,
    lean_project_dir: Path,
    scratch_name: str,
    allow_sorry: bool = False,
) -> tuple[bool, list[str]]:
    """Backward-compatible verifier interface for existing callers."""

    result = check_lean_file_detailed(
        lean_code,
        lean_project_dir,
        scratch_name,
        allow_sorry=allow_sorry,
    )
    return result.success, result.errors


def promote_scratch_to_final(
    lean_project_dir: Path,
    scratch_name: str,
    final_id: str,
    destination_dir: Path,
) -> Path:
    """Copy a verified scratch proof into the final generated-proof directory.

    The destination must be an existing run-specific directory beneath
    ``generated/runs``. This prevents a new experiment from replacing the
    committed generated proof corpus.
    """

    if not _safe_filename_component(scratch_name) or not _safe_filename_component(final_id):
        raise ValueError("Scratch and final IDs must be safe filename components.")
    lean_project_dir = Path(lean_project_dir).resolve()
    destination_dir = Path(destination_dir).resolve()
    allowed_root = (lean_project_dir / "generated" / "runs").resolve()
    if (
        not destination_dir.is_relative_to(allowed_root)
        or destination_dir.parent != allowed_root
        or not _safe_filename_component(destination_dir.name)
    ):
        raise ValueError(
            "Final proof destination must be a safe run directory beneath generated/runs."
        )
    if not destination_dir.is_dir():
        raise FileNotFoundError(
            f"Final proof destination does not exist: {destination_dir}"
        )
    src = lean_project_dir / "generated" / "_scratch" / f"{scratch_name}.lean"
    dst = destination_dir / f"{final_id}.lean"
    with dst.open("x") as output:
        output.write(src.read_text())
    return dst

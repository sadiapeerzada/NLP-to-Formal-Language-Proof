"""Stage D core: run a candidate Lean file through the real compiler.

This is the module that makes the whole project honest. Nothing is counted
as "solved" unless this function returns success=True.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

FORBIDDEN_TOKENS = ("sorry", "sorryAx", "admit")


def _contains_forbidden(lean_code: str) -> str | None:
    for tok in FORBIDDEN_TOKENS:
        # word-boundary match so we don't false-positive on e.g. "admittance"
        if re.search(rf"\b{tok}\b", lean_code):
            return tok
    return None


def check_lean_file(lean_code: str, lean_project_dir: Path, scratch_name: str):
    """Writes `lean_code` to a scratch file inside the Lean project and runs
    `lake env lean --json` on it.

    Returns (success: bool, error_messages: list[str]).
    """
    forbidden = _contains_forbidden(lean_code)
    if forbidden:
        return False, [
            f"Proof rejected before compilation: contains forbidden token '{forbidden}'. "
            f"A proof using sorry/sorryAx/admit is not verified, regardless of compiler output."
        ]

    scratch_dir = lean_project_dir / "generated" / "_scratch"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    file_path = scratch_dir / f"{scratch_name}.lean"
    file_path.write_text(lean_code)

    try:
        result = subprocess.run(
            ["lake", "env", "lean", "--json", str(file_path)],
            cwd=str(lean_project_dir),
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return False, ["Compilation timed out after 60s (likely a non-terminating tactic like a bad `simp` loop)."]

    if result.returncode != 0 and not result.stdout.strip():
        # lake/lean crashed before producing JSON diagnostics (e.g. missing import)
        return False, [result.stderr.strip() or "Unknown build error, no stdout/stderr captured."]

    errors = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("severity") == "error":
            errors.append(f"line {msg.get('pos', {}).get('line', '?')}: {msg.get('data', '')}")

    return (len(errors) == 0), errors


def promote_scratch_to_final(lean_project_dir: Path, scratch_name: str, final_id: str) -> Path:
    """Once a proof is verified, copy it out of the scratch folder into
    generated/<id>.lean as the permanent record."""
    src = lean_project_dir / "generated" / "_scratch" / f"{scratch_name}.lean"
    dst_dir = lean_project_dir / "generated"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / f"{final_id}.lean"
    dst.write_text(src.read_text())
    return dst

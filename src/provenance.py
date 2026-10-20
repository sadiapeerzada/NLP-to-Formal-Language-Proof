"""Collect reproducibility metadata for newly launched pipeline runs."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


UNAVAILABLE = "unavailable"
COMMAND_TIMEOUT_SECONDS = 10


def _command_output(command: list[str], cwd: Path) -> str | None:
    try:
        process = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if process.returncode != 0:
        return None
    return process.stdout.strip() or None


def _git_metadata(repository_root: Path) -> dict[str, object]:
    commit = _command_output(["git", "rev-parse", "HEAD"], repository_root)
    status = _command_output(["git", "status", "--porcelain"], repository_root)
    return {
        "commit": commit or UNAVAILABLE,
        "dirty": UNAVAILABLE if status is None else bool(status),
    }


def _lean_metadata(lean_project_dir: Path) -> dict[str, str]:
    lean_version = (
        _command_output(["lake", "env", "lean", "--version"], lean_project_dir)
        or UNAVAILABLE
    )
    mathlib_revision = UNAVAILABLE
    manifest = lean_project_dir / "lake-manifest.json"
    if manifest.exists():
        try:
            packages = json.loads(manifest.read_text()).get("packages", [])
            mathlib = next(package for package in packages if package["name"] == "mathlib")
            mathlib_revision = mathlib.get("rev") or UNAVAILABLE
        except (json.JSONDecodeError, KeyError, StopIteration, TypeError):
            mathlib_revision = UNAVAILABLE
    return {"lean_version": lean_version, "mathlib_revision": mathlib_revision}


def new_run_metadata(
    repository_root: Path,
    input_path: Path,
    lean_project_dir: Path,
    prompt_paths: dict[str, Path],
    stage_models: dict[str, str],
    max_repair: int,
    synthesis_max_completion_tokens: int = 2000,
    synthesis_reasoning_effort: str | None = None,
    experiment_config: str = "full_pipeline",
) -> dict[str, object]:
    started_at = datetime.now(UTC)
    return {
        "schema_version": 2,
        "run_id": f"{started_at:%Y%m%dT%H%M%SZ}-{uuid4().hex[:8]}",
        "started_at_utc": started_at.isoformat().replace("+00:00", "Z"),
        "git": _git_metadata(repository_root),
        "input": {
            "path": str(input_path),
            "sha256": sha256_file(input_path),
        },
        "prompts": {
            stage: {"path": str(path), "sha256": sha256_file(path)}
            for stage, path in prompt_paths.items()
        },
        "lean": _lean_metadata(lean_project_dir),
        "models": stage_models,
        "configuration": {
            "experiment_config": experiment_config,
            "max_repair": max_repair,
            "formalize_max_attempts": 3,
            "synthesis_max_completion_tokens": synthesis_max_completion_tokens,
            "synthesis_reasoning_effort": synthesis_reasoning_effort or "model_default",
            "synthesis_temperature": 0.2,
        },
    }

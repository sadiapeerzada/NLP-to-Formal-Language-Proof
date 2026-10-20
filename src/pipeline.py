"""End-to-end runner: NL problems in -> verified Lean proofs out.

Usage:
    python src/pipeline.py --input data/seed_problems.json \
        --out data/results/run1.jsonl --max-repair 5
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from formalize import formalize
from llm_client import FAST_MODEL, STRONG_MODEL
from proof_sketch import sketch_with_metadata
from provenance import new_run_metadata
from synthesize import (
    SYNTHESIS_MAX_COMPLETION_TOKENS,
    SYNTHESIS_REASONING_EFFORT,
    synthesize_and_verify,
)
from verify import promote_scratch_to_final

REPOSITORY_ROOT = Path(__file__).parent.parent
PROMPT_PATHS = {
    "formalize": REPOSITORY_ROOT / "prompts" / "stage_a_formalize.txt",
    "sketch": REPOSITORY_ROOT / "prompts" / "stage_b_sketch.txt",
    "synthesize": REPOSITORY_ROOT / "prompts" / "stage_c_synthesize.txt",
    "repair": REPOSITORY_ROOT / "prompts" / "stage_d_repair.txt",
}
STAGE_MODELS = {
    "formalize": STRONG_MODEL,
    "sketch": STRONG_MODEL,
    "synthesize": FAST_MODEL,
    "repair": FAST_MODEL,
}


def _write_json(path: Path, value: object) -> None:
    temporary_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary_path.write_text(json.dumps(value, indent=2) + "\n")
    temporary_path.replace(path)


def _write_results(path: Path, results: list[dict]) -> None:
    temporary_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary_path.write_text("\n".join(json.dumps(result) for result in results) + "\n")
    temporary_path.replace(path)


def _safe_problem_id(problem_id: object) -> bool:
    return (
        isinstance(problem_id, str)
        and bool(problem_id)
        and problem_id not in {".", ".."}
        and Path(problem_id).name == problem_id
        and "\\" not in problem_id
    )


def _create_attempts_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=False)


def _create_final_proofs_dir(lean_project_dir: Path, run_id: str) -> Path:
    if not _safe_problem_id(run_id):
        raise ValueError("Run ID is not safe for a proof-output directory.")
    destination_dir = lean_project_dir / "generated" / "runs" / run_id
    destination_dir.mkdir(parents=True, exist_ok=False)
    return destination_dir


def run(input_path: Path, out_path: Path, lean_project_dir: Path, max_repair: int):
    input_path = input_path.resolve()
    out_path = out_path.resolve()
    lean_project_dir = lean_project_dir.resolve()
    problems = json.loads(input_path.read_text())
    problem_ids = [problem["id"] for problem in problems]
    invalid_ids = [problem_id for problem_id in problem_ids if not _safe_problem_id(problem_id)]
    if invalid_ids:
        raise ValueError("Input contains unsafe problem IDs.")
    duplicate_ids = sorted({problem_id for problem_id in problem_ids if problem_ids.count(problem_id) > 1})
    if duplicate_ids:
        raise ValueError(f"Input contains duplicate problem IDs: {', '.join(duplicate_ids)}")
    if out_path.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing results file: {out_path}. "
            "Use a new --out path for each schema-v2 run."
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    run_metadata = new_run_metadata(
        REPOSITORY_ROOT,
        input_path,
        lean_project_dir,
        PROMPT_PATHS,
        STAGE_MODELS,
        max_repair,
        synthesis_max_completion_tokens=SYNTHESIS_MAX_COMPLETION_TOKENS,
        synthesis_reasoning_effort=SYNTHESIS_REASONING_EFFORT,
    )
    run_metadata["status"] = "running"
    run_metadata["completed_problem_count"] = 0
    metadata_path = out_path.with_suffix(".run.json")
    if metadata_path.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing run manifest: {metadata_path}."
        )
    attempts_dir = out_path.parent / "attempts" / run_metadata["run_id"]
    _create_attempts_dir(attempts_dir)
    try:
        final_proofs_dir = _create_final_proofs_dir(
            lean_project_dir, run_metadata["run_id"]
        )
    except BaseException:
        attempts_dir.rmdir()
        raise
    run_metadata["final_proofs_dir"] = str(final_proofs_dir)
    try:
        _write_json(metadata_path, run_metadata)
    except BaseException:
        attempts_dir.rmdir()
        final_proofs_dir.rmdir()
        raise

    def write_attempts(problem_id: str, attempts: list[dict]) -> None:
        records = [
            {
                "schema_version": 2,
                "run_id": run_metadata["run_id"],
                **attempt,
            }
            for attempt in attempts
        ]
        (attempts_dir / f"{problem_id}.jsonl").write_text(
            "\n".join(json.dumps(record) for record in records) + "\n"
        )

    results = []
    try:
        for problem in problems:
            pid = problem["id"]
            print(f"[{pid}] Stage A: formalizing...")
            stmt_ok, lean_statement, stmt_attempts = formalize(
                problem["nl_statement"], lean_project_dir, pid
            )
            if not stmt_ok:
                print(f"[{pid}] FAILED at Stage A (statement wouldn't elaborate)")
                write_attempts(pid, [{"stage": "formalize", **attempt} for attempt in stmt_attempts])
                results.append({
                    "schema_version": 2, "run_id": run_metadata["run_id"],
                    "id": pid, "category": problem["category"], "difficulty": problem["difficulty"],
                    "models": STAGE_MODELS, "solved": False, "repair_attempts": 0,
                    "initial_synthesis_success": None, "success_within_repair_budget": False,
                    "total_synthesis_attempts": 0, "wall_clock_seconds": 0,
                    "final_lean_statement": lean_statement, "final_proof": None,
                    "lean_file_path": None, "failure_stage": "formalize",
                })
                _write_results(out_path, results)
                run_metadata["completed_problem_count"] = len(results)
                _write_json(metadata_path, run_metadata)
                continue

            print(f"[{pid}] Stage B: sketching proof...")
            sketch_completion = sketch_with_metadata(
                problem["nl_statement"], lean_statement
            )
            proof_sketch_text = sketch_completion.content

            print(f"[{pid}] Stage C/D: synthesizing + verifying (max {max_repair} repairs)...")
            result, attempts_log = synthesize_and_verify(
                problem["nl_statement"], lean_statement, proof_sketch_text,
                lean_project_dir, pid, max_repair=max_repair,
            )

            write_attempts(
                pid,
                [{"stage": "formalize", **attempt} for attempt in stmt_attempts]
                + [
                    {
                        "stage": "sketch",
                        "attempt_number": 1,
                        **sketch_completion.metadata,
                    }
                ]
                + [
                    {
                        "stage": "synthesize" if attempt["is_initial_synthesis"] else "repair",
                        **attempt,
                    }
                    for attempt in attempts_log
                ],
            )

            lean_file_path = None
            if result["solved"]:
                final_path = promote_scratch_to_final(
                    lean_project_dir,
                    result["scratch_name"],
                    pid,
                    final_proofs_dir,
                )
                lean_file_path = str(final_path)
                print(f"[{pid}] SOLVED after {result['repair_attempts']} repair(s) -> {final_path}")
            else:
                print(f"[{pid}] FAILED after {result['repair_attempts']} repair attempts")

            results.append({
                "schema_version": 2, "run_id": run_metadata["run_id"],
                "id": pid, "category": problem["category"], "difficulty": problem["difficulty"],
                "models": STAGE_MODELS,
                "solved": result["solved"], "repair_attempts": result["repair_attempts"],
                "initial_synthesis_success": result["initial_synthesis_success"],
                "success_within_repair_budget": result["success_within_repair_budget"],
                "total_synthesis_attempts": result["total_synthesis_attempts"],
                "wall_clock_seconds": result["wall_clock_seconds"],
                "final_lean_statement": lean_statement, "final_proof": result["final_proof"],
                "lean_file_path": lean_file_path,
                "failure_stage": (
                    None if result["solved"] else result.get("failure_stage", "synthesize")
                ),
            })

            _write_results(out_path, results)
            run_metadata["completed_problem_count"] = len(results)
            _write_json(metadata_path, run_metadata)
    except BaseException as error:
        run_metadata["status"] = "failed"
        run_metadata["failure_type"] = type(error).__name__
        run_metadata["completed_problem_count"] = len(results)
        _write_json(metadata_path, run_metadata)
        raise

    run_metadata["status"] = "completed"
    run_metadata["completed_problem_count"] = len(results)
    _write_json(metadata_path, run_metadata)

    solved = sum(1 for r in results if r["solved"])
    print(f"\nDone: {solved}/{len(results)} solved. Results written to {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Run NL2Lean with immutable result artifacts and run-isolated "
            "promoted proofs under lean_project/generated/runs/<run-id>."
        )
    )
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--lean-project", type=Path, default=Path(__file__).parent.parent / "lean_project")
    ap.add_argument("--max-repair", type=int, default=5)
    args = ap.parse_args()
    run(args.input, args.out, args.lean_project, args.max_repair)

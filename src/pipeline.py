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
from proof_sketch import sketch
from synthesize import synthesize_and_verify
from verify import promote_scratch_to_final

MODEL_NAME = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
PROMPT_VERSION = "v1"


def run(input_path: Path, out_path: Path, lean_project_dir: Path, max_repair: int):
    problems = json.loads(input_path.read_text())
    out_path.parent.mkdir(parents=True, exist_ok=True)
    attempts_dir = out_path.parent / "attempts"
    attempts_dir.mkdir(parents=True, exist_ok=True)

    results = []
    already_done = set()
    if out_path.exists():
        for line in out_path.read_text().splitlines():
            if line.strip():
                prior = json.loads(line)
                if prior.get("solved"):
                    results.append(prior)
                    already_done.add(prior["id"])
                # unsolved prior entries are NOT kept and NOT skipped --
                # they get genuinely retried below, and their old failed
                # entry will be replaced by whatever this run produces
        print(f"Resuming: {len(already_done)} already-SOLVED problem(s) found, skipping those. Everything else (including prior failures) will be retried.")
    for problem in problems:
        pid = problem["id"]
        if pid in already_done:
            print(f"[{pid}] already in results file, skipping")
            continue
        print(f"[{pid}] Stage A: formalizing...")
        stmt_ok, lean_statement, stmt_attempts = formalize(
            problem["nl_statement"], lean_project_dir, pid
        )
        if not stmt_ok:
            print(f"[{pid}] FAILED at Stage A (statement wouldn't elaborate)")
            results.append({
                "id": pid, "category": problem["category"], "difficulty": problem["difficulty"],
                "model": MODEL_NAME, "prompt_version": PROMPT_VERSION,
                "solved": False, "repair_attempts": 0, "wall_clock_seconds": 0,
                "final_lean_statement": lean_statement, "final_proof": None,
                "lean_file_path": None, "failure_stage": "formalize",
            })
            continue

        print(f"[{pid}] Stage B: sketching proof...")
        proof_sketch_text = sketch(problem["nl_statement"], lean_statement)

        print(f"[{pid}] Stage C/D: synthesizing + verifying (max {max_repair} repairs)...")
        result, attempts_log = synthesize_and_verify(
            problem["nl_statement"], lean_statement, proof_sketch_text,
            lean_project_dir, pid, max_repair=max_repair,
        )

        (attempts_dir / f"{pid}.jsonl").write_text(
            "\n".join(json.dumps(a) for a in attempts_log)
        )

        lean_file_path = None
        if result["solved"]:
            final_path = promote_scratch_to_final(lean_project_dir, result["scratch_name"], pid)
            lean_file_path = str(final_path)
            print(f"[{pid}] SOLVED after {result['repair_attempts']} repair(s) -> {final_path}")
        else:
            print(f"[{pid}] FAILED after {max_repair} repair attempts")

        results.append({
            "id": pid, "category": problem["category"], "difficulty": problem["difficulty"],
            "model": MODEL_NAME, "prompt_version": PROMPT_VERSION,
            "solved": result["solved"], "repair_attempts": result["repair_attempts"],
            "wall_clock_seconds": result["wall_clock_seconds"],
            "final_lean_statement": lean_statement, "final_proof": result["final_proof"],
            "lean_file_path": lean_file_path, "failure_stage": None if result["solved"] else "synthesize",
        })

        # write after EVERY problem, not just at the end -- a crash or rate
        # limit mid-run should never lose progress already made
        with out_path.open("w") as f:
            for r in results:
                f.write(json.dumps(r) + "\n")

    with out_path.open("w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    solved = sum(1 for r in results if r["solved"])
    print(f"\nDone: {solved}/{len(results)} solved. Results written to {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--lean-project", type=Path, default=Path(__file__).parent.parent / "lean_project")
    ap.add_argument("--max-repair", type=int, default=5)
    args = ap.parse_args()
    run(args.input, args.out, args.lean_project, args.max_repair)

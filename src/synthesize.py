"""Stage C (initial synthesis) + Stage D repair loop (feed compiler errors
back to the model, capped retries).

This module is the core of the repair-loop mechanism -- most of
the interesting failure/success data comes from here.
"""
from __future__ import annotations

import time
from pathlib import Path

from llm_client import complete, extract_lean_block
from verify import check_lean_file

SYNTH_PROMPT = Path(__file__).parent.parent.joinpath(
    "prompts", "stage_c_synthesize.txt"
).read_text()
REPAIR_PROMPT = Path(__file__).parent.parent.joinpath(
    "prompts", "stage_d_repair.txt"
).read_text()


def synthesize_and_verify(
    nl_statement: str,
    lean_statement: str,
    proof_sketch: str,
    lean_project_dir: Path,
    problem_id: str,
    max_repair: int = 5,
):
    """Returns a dict matching the results/<run>.jsonl schema (minus the
    top-level 'model'/'prompt_version' fields, added by the caller) plus the
    full per-attempt log for data/results/attempts/<id>.jsonl.
    """
    start = time.time()
    attempts_log = []

    prompt = SYNTH_PROMPT.format(
        nl_statement=nl_statement,
        lean_statement=lean_statement,
        proof_sketch=proof_sketch,
    )

    current_proof = None
    for attempt in range(1, max_repair + 2):  # +1 initial synth, then max_repair repairs
        raw = complete(prompt, max_tokens=2000, temperature=0.2)
        current_proof = extract_lean_block(raw)

        ok, errors = check_lean_file(
            current_proof, lean_project_dir, f"{problem_id}_attempt{attempt}"
        )
        attempts_log.append({
            "attempt_number": attempt,
            "proof_text": current_proof,
            "success": ok,
            "compiler_errors": errors,
            "timestamp": time.time(),
        })

        if ok:
            return {
                "id": problem_id,
                "solved": True,
                "repair_attempts": attempt - 1,
                "wall_clock_seconds": round(time.time() - start, 2),
                "final_proof": current_proof,
                "scratch_name": f"{problem_id}_attempt{attempt}",
            }, attempts_log

        if attempt > max_repair:
            break

        prompt = REPAIR_PROMPT.format(
            nl_statement=nl_statement,
            lean_statement=lean_statement,
            failed_proof=current_proof,
            compiler_errors="\n".join(errors),
            attempt_number=attempt,
            max_attempts=max_repair,
        )

    return {
        "id": problem_id,
        "solved": False,
        "repair_attempts": max_repair,
        "wall_clock_seconds": round(time.time() - start, 2),
        "final_proof": current_proof,
        "scratch_name": None,
    }, attempts_log

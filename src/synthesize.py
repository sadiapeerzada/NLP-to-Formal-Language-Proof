"""Stage C (initial synthesis) + Stage D repair loop (feed compiler errors
back to the model, capped retries).
This module is the core of the repair-loop mechanism -- most of
the interesting failure/success data comes from here.
"""
from __future__ import annotations

import time
from pathlib import Path

from llm_client import (
    FAST_MODEL,
    complete_with_metadata,
    extract_lean_block,
    reasoning_effort_for_model,
)
from verify import check_lean_file_detailed

SYNTH_PROMPT = Path(__file__).parent.parent.joinpath(
    "prompts", "stage_c_synthesize.txt"
).read_text()
REPAIR_PROMPT = Path(__file__).parent.parent.joinpath(
    "prompts", "stage_d_repair.txt"
).read_text()
EMPTY_OUTPUT_ERROR = (
    "LLM returned empty or whitespace-only assistant content; reasoning is not "
    "used as proof, Lean verification was not run, and no further repair call "
    "was sent."
)
SYNTHESIS_MAX_COMPLETION_TOKENS = 2000
SYNTHESIS_REASONING_EFFORT = reasoning_effort_for_model(FAST_MODEL)


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
    failure_stage = "synthesize"
    for attempt in range(1, max_repair + 2):  # +1 initial synth, then max_repair repairs
        completion = complete_with_metadata(
            prompt,
            max_tokens=SYNTHESIS_MAX_COMPLETION_TOKENS,
            temperature=0.2,
            model=FAST_MODEL,
            reasoning_effort=SYNTHESIS_REASONING_EFFORT,
        )
        current_proof = extract_lean_block(completion.content)
        if not current_proof:
            failure_stage = "llm_output"
            attempts_log.append(
                {
                    "attempt_number": attempt,
                    "repair_number": attempt - 1,
                    "is_initial_synthesis": attempt == 1,
                    "model": FAST_MODEL,
                    "proof_text": current_proof,
                    **completion.metadata,
                    "success": False,
                    "failure_stage": failure_stage,
                    "output_error": EMPTY_OUTPUT_ERROR,
                    "compiler_errors": [],
                    "verification": None,
                    "timestamp": time.time(),
                }
            )
            repair_feedback = EMPTY_OUTPUT_ERROR
        else:
            verification = check_lean_file_detailed(
                current_proof, lean_project_dir, f"{problem_id}_attempt{attempt}"
            )
            failure_stage = "synthesize"
            attempts_log.append(
                {
                    "attempt_number": attempt,
                    "repair_number": attempt - 1,
                    "is_initial_synthesis": attempt == 1,
                    "model": FAST_MODEL,
                    "proof_text": current_proof,
                    **completion.metadata,
                    "success": verification.success,
                    "compiler_errors": verification.errors,
                    "verification": verification.to_record(),
                    "timestamp": time.time(),
                }
            )
            if verification.success:
                return {
                    "id": problem_id,
                    "solved": True,
                    "initial_synthesis_success": attempt == 1,
                    "success_within_repair_budget": True,
                    "total_synthesis_attempts": attempt,
                    "repair_attempts": attempt - 1,
                    "wall_clock_seconds": round(time.time() - start, 2),
                    "final_proof": current_proof,
                    "scratch_name": f"{problem_id}_attempt{attempt}",
                }, attempts_log
            repair_feedback = "\n".join(verification.errors)
        if failure_stage == "llm_output":
            break
        if attempt > max_repair:
            break
        prompt = REPAIR_PROMPT.format(
            nl_statement=nl_statement,
            lean_statement=lean_statement,
            failed_proof=current_proof,
            compiler_errors=repair_feedback,
            attempt_number=attempt,
            max_attempts=max_repair,
        )
    return {
        "id": problem_id,
        "solved": False,
        "initial_synthesis_success": False,
        "success_within_repair_budget": False,
        "total_synthesis_attempts": len(attempts_log),
        "repair_attempts": max(0, len(attempts_log) - 1),
        "wall_clock_seconds": round(time.time() - start, 2),
        "final_proof": current_proof,
        "scratch_name": None,
        "failure_stage": failure_stage,
    }, attempts_log
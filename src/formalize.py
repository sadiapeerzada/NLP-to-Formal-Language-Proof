"""Stage A: natural language -> Lean 4 theorem statement (signature only).

The statement is considered accepted once it elaborates with `sorry` as the
body -- i.e. Lean agrees the types check, even though nothing is proved yet.
"""
from __future__ import annotations

from pathlib import Path

from llm_client import complete, extract_lean_block, STRONG_MODEL
from verify import check_lean_file_detailed

PROMPT_TEMPLATE = Path(__file__).parent.parent.joinpath(
    "prompts", "stage_a_formalize.txt"
).read_text()


def formalize(nl_statement: str, lean_project_dir: Path, scratch_id: str, max_attempts: int = 3):
    """Returns (success: bool, lean_statement: str, attempts_log: list[dict])."""
    prompt = PROMPT_TEMPLATE.format(nl_statement=nl_statement)
    attempts_log = []

    for attempt in range(1, max_attempts + 1):
        raw = complete(prompt, max_tokens=500, model=STRONG_MODEL)
        lean_code = extract_lean_block(raw)

        verification = check_lean_file_detailed(
            lean_code,
            lean_project_dir,
            f"{scratch_id}_stmt_check",
            allow_sorry=True,
        )
        attempts_log.append({
            "attempt": attempt,
            "model": STRONG_MODEL,
            "lean_code": lean_code,
            "success": verification.success,
            "errors": verification.errors,
            "verification": verification.to_record(),
        })

        if verification.success:
            return True, lean_code, attempts_log

        # feed the elaboration error back and ask for a fix
        prompt = (
            f"{PROMPT_TEMPLATE.format(nl_statement=nl_statement)}\n\n"
            f"Your previous attempt failed to elaborate:\n```lean\n{lean_code}\n```\n"
            f"Error:\n```\n{chr(10).join(verification.errors)}\n```\n"
            f"Fix the statement (still `:= by sorry` for the body) and output "
            f"only the corrected Lean 4 code block."
        )

    return False, lean_code, attempts_log

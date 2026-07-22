"""Stage B: elaborated Lean statement -> ordered plain-English proof sketch.

Deliberately NOT Lean yet. This intermediate artifact is what a human reviews
when Stage C keeps failing -- it tells you whether the model's *reasoning*
is wrong (fix the sketch / try a different problem) versus its *tactic
knowledge* is wrong (a repair-loop problem, handled in Stage D).
"""
from __future__ import annotations

from pathlib import Path

from llm_client import complete, STRONG_MODEL

PROMPT_TEMPLATE = Path(__file__).parent.parent.joinpath(
    "prompts", "stage_b_sketch.txt"
).read_text()


def sketch(nl_statement: str, lean_statement: str) -> str:
    prompt = PROMPT_TEMPLATE.format(
        nl_statement=nl_statement, lean_statement=lean_statement
    )
    return complete(prompt, max_tokens=600, temperature=0.3, model=STRONG_MODEL)

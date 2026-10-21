"""Stage B: elaborated Lean statement -> ordered plain-English proof sketch.

Deliberately NOT Lean yet. This intermediate artifact is what a human reviews
when Stage C keeps failing -- it tells you whether the model's *reasoning*
is wrong (fix the sketch / try a different problem) versus its *tactic
knowledge* is wrong (a repair-loop problem, handled in Stage D).
"""
from __future__ import annotations

from pathlib import Path

from llm_client import (
    STRONG_MODEL,
    CompletionResult,
    complete,
    complete_with_metadata,
)

PROMPT_TEMPLATE = Path(__file__).parent.parent.joinpath(
    "prompts", "stage_b_sketch.txt"
).read_text()


SKETCH_MAX_COMPLETION_TOKENS = 600
SKETCH_TEMPERATURE = 0.3


def sketch_with_metadata(
    nl_statement: str, lean_statement: str, model: str | None = None
) -> CompletionResult:
    prompt = PROMPT_TEMPLATE.format(
        nl_statement=nl_statement, lean_statement=lean_statement
    )
    return complete_with_metadata(
        prompt,
        max_tokens=SKETCH_MAX_COMPLETION_TOKENS,
        temperature=SKETCH_TEMPERATURE,
        model=model or STRONG_MODEL,
    )


def sketch(nl_statement: str, lean_statement: str) -> str:
    return sketch_with_metadata(nl_statement, lean_statement).content

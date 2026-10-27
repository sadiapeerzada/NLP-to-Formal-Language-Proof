"""Provider-independent completion interface and Lean response extraction."""
from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Protocol

@dataclass(frozen=True)
class CompletionResult:
    content: str
    metadata: dict[str, object]

class ModelClient(Protocol):
    def __call__(self, prompt: str, **kwargs: object) -> CompletionResult: ...

def extract_lean_block(text: str) -> str:
    match = re.search(r"```lean\s*(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

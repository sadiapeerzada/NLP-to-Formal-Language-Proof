from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import proof_sketch


def test_sketch_module_imports_and_calls_completion_interface() -> None:
    expected = proof_sketch.CompletionResult(content="A short proof sketch.", metadata={})
    with patch.object(proof_sketch, "complete_with_metadata", return_value=expected) as complete:
        result = proof_sketch.sketch_with_metadata(
            "Every number equals itself.",
            "theorem identity (n : Nat) : n = n := by sorry",
            model="test-model",
        )

    assert result is expected
    complete.assert_called_once()
    args, kwargs = complete.call_args
    assert "Every number equals itself." in args[0]
    assert "theorem identity" in args[0]
    assert kwargs == {
        "max_tokens": proof_sketch.SKETCH_MAX_COMPLETION_TOKENS,
        "temperature": proof_sketch.SKETCH_TEMPERATURE,
        "model": "test-model",
    }

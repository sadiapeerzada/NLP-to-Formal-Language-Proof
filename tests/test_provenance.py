from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import provenance


class ProvenanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_command_timeout_is_unavailable(self) -> None:
        with patch(
            "provenance.subprocess.run",
            side_effect=subprocess.TimeoutExpired(["git"], 10),
        ):
            self.assertIsNone(provenance._command_output(["git"], self.root))

    def test_metadata_marks_unavailable_provenance_without_secrets(self) -> None:
        input_path = self.root / "input.json"
        prompt_path = self.root / "prompt.txt"
        input_path.write_text("[]")
        prompt_path.write_text("prompt")

        with patch("provenance._command_output", return_value=None):
            metadata = provenance.new_run_metadata(
                self.root,
                input_path,
                self.root,
                {"formalize": prompt_path},
                {"formalize": "model-name"},
                max_repair=1,
                synthesis_max_completion_tokens=2000,
                synthesis_reasoning_effort="low",
            )

        self.assertRegex(metadata["started_at_utc"], r"Z$")
        self.assertIn("-", metadata["run_id"])
        self.assertEqual(metadata["git"]["commit"], provenance.UNAVAILABLE)
        self.assertEqual(metadata["git"]["dirty"], provenance.UNAVAILABLE)
        self.assertEqual(metadata["lean"]["lean_version"], provenance.UNAVAILABLE)
        self.assertEqual(metadata["lean"]["mathlib_revision"], provenance.UNAVAILABLE)
        self.assertEqual(metadata["input"]["sha256"], provenance.sha256_file(input_path))
        self.assertEqual(
            metadata["configuration"]["synthesis_max_completion_tokens"], 2000
        )
        self.assertEqual(
            metadata["configuration"]["synthesis_reasoning_effort"],
            "low",
        )
        self.assertNotIn("GROQ_API_KEY", json.dumps(metadata))


if __name__ == "__main__":
    unittest.main()

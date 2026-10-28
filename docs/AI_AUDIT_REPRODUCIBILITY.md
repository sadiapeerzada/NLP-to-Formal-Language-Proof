# Reproducing the AI-only audit

Use the pinned existing Lean 4.32.0 / Mathlib checkout and Python environment. Optional MLX dependencies are in `requirements-local.txt`; raw runtime versions and immutable model inventories are under `data/ai_semantic_audit/20261028/`. This audit never calls the study runner or imports AI decisions through the independent-human review importer.

The two model selection files record exact converted and upstream revisions, and their directories contain original cards and MIT license evidence. Model weights live in the local Hugging Face cache and are not committed. To restore a model elsewhere, run `scripts/prepare_ai_review_model.py` with the repo, converted revision, upstream repo/revision from its selection file and a fresh output directory. Compare every inventory hash before using the restored snapshot; a local absolute path is not provenance. Example:

```sh
HF_HUB_DISABLE_XET=1 .venv/bin/python scripts/prepare_ai_review_model.py \
  --repo mlx-community/Phi-3.5-mini-instruct-4bit \
  --revision 7b2052fd882fe017300d4d42a4eb06a27b816af4 \
  --upstream microsoft/Phi-3.5-mini-instruct \
  --upstream-revision 2fe192450127e6a83f7441aef6e3ca586c338b77 \
  --output /tmp/restored-phi35-reviewer
```

The audit runners read the model directory constants shown in their source. On another machine restore the matching snapshots, compare the recorded inventories, and update only the machine-local `local_snapshot_path.txt` locator to the restored snapshot; the loader rechecks all bytes. Use fresh audit output roots and do not edit recorded scientific manifests. GPU/Metal access may be needed on the host. Temperature is zero; base seed is 284729 and per-call seeds derive from the exact prompt and logical context. Deterministic settings do not guarantee bit-identical outputs on different runtime/hardware versions.

From the repository root, use fresh output directories:

```sh
.venv/bin/python scripts/ai_audit_lean_checks.py --output /tmp/audit-lean-new
.venv/bin/python scripts/ai_audit_math_checks.py --output /tmp/audit-math-new
.venv/bin/python scripts/ai_semantic_audit.py prepare --output /tmp/phi35-audit-new
.venv/bin/python scripts/ai_semantic_audit.py run --output /tmp/phi35-audit-new
.venv/bin/python scripts/ai_semantic_audit_phi4.py prepare --output /tmp/phi4-audit-new
.venv/bin/python scripts/ai_semantic_audit_phi4.py run --output /tmp/phi4-audit-new
.venv/bin/python scripts/ai_audit_calibration.py prepare --output /tmp/ai-controls-new
.venv/bin/python scripts/ai_audit_calibration.py run --output /tmp/ai-controls-new
.venv/bin/python -m pytest -q
```

Each preparation freezes exact subjects, prompts, seed/settings, snapshot inventory and implementation hashes. Each call writes/fsyncs an intent before inference and a per-token stream plus actual completion/metadata afterward. Interrupted intents consume their context; resuming never silently regenerates an attempted judgment. A genuinely new attempt requires a new audit directory and explicit provenance. Strict JSON parsing rejects missing fields, duplicate keys, trailing prose and truncation; a failed response is never inferred to be faithful. Raw judgments may contain unsupported claims and remain untrusted data.

The assembler validates subject, response, prompt, model and source hashes against both pass journals and preserves all original candidate/curation fields. It requires a complete primary Phi-4 pass and refuses missing/replayed/interrupted primary responses. The exploratory Phi-3.5 pass was explicitly retired after 68 completions, with one interruption and 27 unattempted candidates; its retirement disposition binds the actual journal hash. Missing exploratory judgments are explicitly absent, never fabricated or counted as reviews. A fresh full exploratory rerun is also supported without a retirement disposition. Use the recorded directory layout or a fresh base with matching `phi_pass1`, `phi4_pass2`, `math_checks`, `lean_reference_check` and static-assessment artifacts:

```sh
.venv/bin/python scripts/assemble_ai_semantic_audit.py \
  --base data/ai_semantic_audit/20261028 \
  --output /tmp/assembled-audit-new
```

The existing semantic-review bindings are separate from AI audit subject bindings. No AI-only field sets a human-review status, changes a split, freezes a dataset or satisfies an approval gate. The gate-file before/after manifest and curation invariance tests provide concrete checks of this boundary.

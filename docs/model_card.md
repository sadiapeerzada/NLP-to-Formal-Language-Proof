# NL2Lean System Card

## System status

This repository contains a research prototype, not a released or validated
model. It has an end-to-end natural-language-to-Lean pipeline and a separate
paired repair runner. No completed paired A/B/C evaluation exists. The current
dataset inventory has 35 candidates and zero eligible examples; no frozen
test set or paired API run manifests exist.

## Model and provider configuration

The paired protocol v0.2.0 proposes the Groq alias
`openai/gpt-oss-120b` for initial generation and all repairs. The alias is
mutable; account-specific generation access and an immutable model revision
are unverified. Protocol status remains
`proposed_locked_for_review_not_preregistered`; API execution is disabled.
The ordinary pipeline uses separate configurable strong/fast model aliases
from `src/llm_client.py` and is not the paired experiment. A model string in a
historical run manifest does not by itself prove that the provider was called.

## Intended use and limitations

The intended research task is proof repair for undergraduate-level
mathematical statements after a human-reviewed Lean theorem has been fixed.
This research tool is not a substitute for mathematical or formal-methods
review. A Lean-accepted proof establishes proof validity for the supplied Lean
statement under the recorded environment; it does not establish that the
statement faithfully formalizes the English problem.

Historical manually authored proofs and compiler checks are demonstrations of
the verification workflow only. They are not autonomous model pass@1, model
repair success, or evidence of a controlled A/B/C comparison.

## Evaluation and safety

The proposed A/B/C design shares one initial candidate: A makes no repair, B
uses at most three blind repairs, and C uses at most three repairs with real
Lean diagnostics. No experimental outcomes are available. No success rate,
error-category effect, token usage, latency, or cost estimate is reported.
Pricing evidence and generation access remain unverified. The cost guard and
API-off execution gate remain in place.

The verifier rejects `sorry`, `sorryAx`, and `admit`, plus unapproved
assumptions under its configured policy. Independent semantic-fidelity review
is required separately; no current dataset candidate has a completed
semantic review.

## Reproduction identifiers

- Protocol: `configs/repair_experiment_protocol_v0.2.0.json`.
- Prompt files: `prompts/repair_experiment_initial.txt`,
  `prompts/repair_experiment_blind.txt`, and
  `prompts/repair_experiment_compiler_guided.txt`, with hashes in the protocol.
- Lean toolchain: `lean_project/lean-toolchain`.
- Mathlib lock: `lean_project/lake-manifest.json`.
- Analysis: `eval/paired_analysis.py`; currently it can produce only a
  readiness audit because there is no validated frozen dataset.

No benchmark performance or deployment capability is claimed.

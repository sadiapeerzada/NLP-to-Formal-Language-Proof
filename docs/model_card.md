# NL2Lean Pipeline Card

This isn't a fine-tuned model -- it's a prompting + verification pipeline on
top of a Groq-hosted model (default `llama-3.3-70b-versatile`, see
GROQ_MODEL). Documenting it like a model card anyway because
reviewers will ask the same questions.

## Intended use
Research prototype for studying LLM-assisted formalization and automated
theorem proving on a curated set of undergraduate-level number theory and
arithmetic problems. Not intended as a general-purpose autoformalization tool
for research-level mathematics.

## Pipeline stages
See README.md for the diagram. Four stages: formalize, sketch, synthesize,
verify+repair. Prompts are versioned in `prompts/` -- report `prompt_version`
alongside every result, since prompt changes materially affect pass@1.

## Evaluation
Schema-v2 `initial_synthesis_success` is the first Stage C call's verified
outcome and is `null` when Stage A did not produce an elaborating statement.
The reported initial-synthesis rate is conditional on Stage A having succeeded;
it is the no-repair Stage C pass@1, not the rate after repair. A no-repair
success uses exactly one Stage C model call and no Stage D calls.
`success_within_repair_budget` is the verified outcome after the initial call
and up to the configured number of Stage D calls. `total_synthesis_attempts`
counts actual Stage C/Stage D calls, and `repair_attempts` counts actual Stage D
calls, including an empty response. Empty assistant content terminates the
sequence immediately rather than prompting the model again with identical
empty-output feedback. Stage A failures are excluded from conditional Stage C
pass@1, but remain failures in the end-to-end verified-success rate.

Legacy result files do not distinguish initial synthesis from repaired success;
their recorded final solved rate must not be interpreted as pass@1.

Metrics also include per-category and per-difficulty breakdown,
repair-attempts-to-success, and failure taxonomy.
[Insert final numbers once the n=500 run is complete.]

## Completion diagnostics
Attempt JSONL records add safe scalar API metadata alongside stage output and
verification records: requested model, finish reason, completion-token count,
whether assistant content was empty, refusal presence, reasoning-field
presence and length, and tool-call presence. Reasoning content, prompts, and
credentials are never stored in these metadata fields.
GPT-OSS synthesis/repair requests use Groq's `max_completion_tokens` with the
existing 2,000-token cap and `reasoning_effort="low"`; other configured models
omit the unsupported reasoning-effort parameter. Reasoning output is never
treated as a Lean proof.

## Verification guarantee
A result is marked `solved: true` if and only if `lake env lean` returned
zero errors on the final proof AND the proof contains none of
`sorry`/`sorryAx`/`admit`. This is checked automatically in `src/verify.py`,
not asserted by the LLM.

## Known failure modes
[Fill in from the failure taxonomy chart -- be specific about categories,
not just "sometimes it fails."]

## Compute / cost
[Fill in: total API calls, total tokens, approximate cost for the n=500 run,
average repair attempts, so someone reproducing this can budget correctly.]

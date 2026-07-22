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
Metrics defined in `eval/metrics.py`: pass@1, pass@k, per-category and
per-difficulty breakdown, repair-attempts-to-success, failure taxonomy.
[Insert final numbers once the n=500 run is complete.]

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

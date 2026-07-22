---
license: mit
task_categories:
  - text-generation
tags:
  - lean4
  - formal-verification
  - mathematical-reasoning
  - theorem-proving
---

# NL2Lean Dataset

## Dataset summary
[Fill in once you have real numbers] A dataset of N natural-language math
problems paired with (a) a human-reference Lean 4 formalization, (b) an
LLM-generated proof sketch, and (c) verified Lean 4 proofs where the pipeline
succeeded, plus full attempt logs (including failures) for every problem.

## Supported tasks
- Autoformalization (NL statement -> Lean 4 theorem statement)
- Formal theorem proving (Lean 4 statement -> tactic proof)
- Proof repair (failed proof + compiler error -> fixed proof)

## Dataset structure
See `data/schema.md` in the repo for exact field definitions.

## Splits
- `seed` (n=10): hand-curated, used for pipeline development
- `templated` (n=?): programmatically varied from seed problems
- `held_out` (n=?): hand-curated, never used during prompt iteration --
  report this number separately, it's the honest number

## Category breakdown
[table: category, count, difficulty distribution]

## How this was collected
Generated via the NL2Lean pipeline (see repo README) using
`llama-3.3-70b-versatile` via Groq (or whichever `GROQ_MODEL` was set).
Every proof marked `solved: true` has been independently
verified to compile against Mathlib commit `[fill in exact commit hash]`
with zero errors and no `sorry`/`admit`. Failed attempts are retained in
full for failure-mode research.

## Known limitations
[Fill in honestly once you have data -- e.g. "pipeline struggles with
problems requiring case splits on parity beyond depth 2" or similar specific
findings, not generic hedging.]

## Licensing / attribution
Problems sourced from [list sources: Project Euler, textbook name + edition,
hand-written]. Respect original licensing of any textbook-derived problems --
paraphrase rather than copy verbatim problem text where the source isn't
public domain.

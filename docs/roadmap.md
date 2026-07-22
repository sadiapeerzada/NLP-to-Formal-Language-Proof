# Roadmap

## Week 1 — prove the pipeline works at all -- DONE
- Lean environment set up, sanity theorem compiles.
- 20 problems across 5 categories (arithmetic identity, divisibility,
  induction, inequality, modular arithmetic) solved end-to-end, every proof
  independently re-verified by the real compiler. See `RUN_REPORT.md` for
  the honest numbers, repair-attempt stats, and what's still simulated
  (the LLM stages were hand-run rather than API-driven so far -- see below).
- inequality has already been added early (originally a Week 2 item) since
  it turned out to be easy to formalize with core-Lean tactics.

## Week 2 — get Mathlib working, run the pipeline for real
- The current 20-problem set was built without Mathlib (see `RUN_REPORT.md`
  for why, in the sandbox this was originally developed in -- your own
  machine likely won't hit that blocker). First priority: get
  `lake exe cache get` working and confirm the sanity theorem in
  `lean_project/Nl2Lean/Basic.lean` compiles with Mathlib imported.
- Second priority: set `GROQ_API_KEY` and actually run
  `python src/pipeline.py` end-to-end for the first time. Compare its
  first-attempt pass rate and repair-iteration counts against the numbers
  in `RUN_REPORT.md` -- expect it to do *worse* on the trickier problems
  (`mod_002`, `arith_004`, `div_006`) since those took several real repair
  attempts even for a proof-writer that already knew the exact tactic
  landscape going in.

## Week 3 — scale to 50, add categories
- Expand categories: add `combinatorics_basic` (counting identities, simple
  pigeonhole) and richer inequalities (AM-GM style, needs Mathlib).
- Source problems from: Project Euler problems 1-20 (restated as NL claims,
  not "compute the answer" — reframe as "prove property X holds"), intro
  number theory textbook exercise sets (e.g. early chapters of Burton or
  Niven), and manual variations on the seed set (swap `Nat` for `Int`, change
  bounds, negate a hypothesis to check the model doesn't "prove" false
  statements).
- Publish v0: repo + README + a short dataset card, even before results are
  great. Getting this in front of your senior partner and getting Lean-side
  feedback early is more valuable than a few more solo days of tuning.

## Week 3-4 — scale to 500, build the failure taxonomy
- Add synthetic variation generation: template the seed problems
  programmatically (vary variable names, bounds, +/- signs) to get volume
  without writing 500 problems by hand — but keep a held-out hand-curated
  set of ~50 so you can report accuracy on both "templated" and "genuinely
  novel" splits separately. Reviewers will ask about this; answer it
  pre-emptively.
- Full eval run, generate all 5 figures in `docs/architecture.md`.
- Draft dataset card + model card.

## Week 5 — write it up
- Repo polish: pin dependency versions, add a LICENSE, make sure a stranger
  can clone and reproduce your headline number in under 30 minutes
  (this is the actual bar for "publishable," not the number itself).
- Push dataset to Hugging Face (dataset card in `docs/dataset_card.md`).
- Short paper-style writeup: abstract, related work (LeanDojo, DeepSeek-Prover,
  AlphaProof/AlphaGeometry for context — cite honestly, don't overclaim
  novelty on the pipeline pattern itself, the contribution is the dataset +
  results + failure analysis at this scale), method, results (the 5 figures),
  limitations (be specific: which categories failed hardest and why).

## Ownership split reminder
- You: everything in `src/`, `eval/`, `data/`, the LLM prompt iteration, infra.
- Senior/formal-methods partner: reviewing `lean_project/` for Mathlib idiom
  quality, sanity-checking that "verified" proofs aren't gaming the checker
  (e.g. flag if `decide` is being used on something that shouldn't be
  decidable that fast — a red flag for a mis-stated theorem), curating which
  Mathlib lemmas to hint in Stage B sketches.

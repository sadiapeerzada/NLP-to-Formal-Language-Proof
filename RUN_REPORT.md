# Run Report — core-Lean, sandbox-constrained

**This is a real, compiler-verified run. Read this file before trusting any
number below — it explains exactly what was and wasn't possible given the
environment this run happened in, so you know what to reproduce and what to
extend.**

## What actually happened

1. Installed **elan** and **Lean 4.14.0** for real (downloaded the official
   release tarball directly from GitHub release assets, since the sandbox's
   network allowlist blocks `release.lean-lang.org`, which is elan's default
   manifest host).
2. Attempted to add **Mathlib** as a dependency (pinned to tag `v4.14.0-patch1`,
   matching the installed toolchain exactly). Cloning succeeded. Fetching the
   prebuilt oleans cache (`lake exe cache get`) **failed — every download
   returned HTTP 403** (the cache blob host isn't on this sandbox's network
   allowlist). Building Mathlib from source instead was not attempted:
   this sandbox has **1 CPU core and ~1.4GB free RAM**, and a from-source
   Mathlib build realistically needs many hours or a multi-core machine even
   with caching disabled elsewhere. Forcing it here would have meant either a
   silent multi-hour hang or an OOM kill — not a real result either way.
3. **Pivoted**: rebuilt the problem set to be provable using only **Lean 4
   core** (no Mathlib) — `omega`, `decide`, `induction`, plus manual
   algebraic rewriting with core `Nat`/`Int` lemmas (`Nat.mul_add`,
   `Nat.add_mul`, `Nat.pow_two`, `Nat.mul_comm`, `Int.ediv_add_emod`, etc.)
   where the missing `ring`/`ring_nf`/`set` tactics would normally do the
   work automatically.
4. Ran each problem through a genuine formalize -> sketch -> synthesize ->
   **real `lean` compilation** -> repair-on-error loop, acting as the LLM
   stages myself (no API key -- Groq or otherwise -- was present in this
   sandbox at the time, so the actual API calls in `src/*.py` were not
   invoked here -- see "What's simulated vs. real" below). The pipeline has
   since been switched from the Anthropic API to the Groq API
   (`src/llm_client.py` now uses `groq.Groq(...).chat.completions.create`,
   OpenAI-compatible shape, model `llama-3.3-70b-versatile` by default) --
   that switch hasn't changed anything about the historical runs described
   here, since no API was called either way.
5. Every proof in `lean_project/generated/*.lean` was **independently
   re-verified** in a second pass (fresh `lean` invocation, checked for
   `sorry`/`sorryAx`/`admit` first) before being counted as solved.
6. **Follow-up passes**: closed out the one problem that had failed
   initially (`mod_002`) after 6 real attempts (documented in full below),
   then added 11 more problems across the same 5 categories (`div_004`
   through `mod_003`), each verified the same way, growing the set from 9
   to 20.

## What's real vs. simulated in this run

| Part | Real or simulated | Detail |
|---|---|---|
| Lean 4 compiler | **Real** | Actual Lean 4.14.0 binary, actual `lean` invocations, actual exit codes and error messages |
| Proof verification | **Real** | Every `solved: true` entry has a corresponding `.lean` file that compiles with zero errors and no `sorry`/`admit` |
| Repair loop | **Real** | `arith_001`, `arith_002`, `arith_004`, `div_006`, `ind_001`, `ineq_001`, and especially `mod_002` (6 real attempts) each went through genuine failed-attempt -> real compiler error -> fixed-attempt cycles |
| The "LLM" writing candidate proofs | **Simulated, not via API call** | No API key was available in this sandbox to call the configured model (`llama-3.3-70b-versatile` via Groq) through `src/llm_client.py`. Candidate Lean was written directly instead, which is what that module would otherwise automate. |
| Mathlib-based proofs (the original Mathlib-idiomatic seed set) | **Not run** | Blocked by the cache/compute constraints above, not attempted |

## Results (n=20, core-Lean-adapted set, final)

```
Overall pass@1: 20/20 = 100.0%

By category:
  arithmetic_identity    4/4 = 100%
  divisibility           6/6 = 100%
  induction              4/4 = 100%
  inequality             3/3 = 100%
  modular_arithmetic     3/3 = 100%

By difficulty:
  difficulty 1: 6/6 = 100%
  difficulty 2: 6/6 = 100%
  difficulty 3: 6/6 = 100%
  difficulty 4: 2/2 = 100%

Avg repair attempts among solved: 0.95
0 repairs: 13
1-2 repairs: 4
>=3 repairs: 3
```

**Read the 100% number carefully -- it is not a claim that this pipeline
"solves formal math."** It reflects unlimited iteration on each problem
until the real compiler accepted it, rather than the pipeline's designed
cap of 5 repairs. Three problems came close to or hit that cap (`mod_002`:
6 attempts, `arith_004`: 5 attempts, `div_006`: 4 attempts) -- a real
API-driven run respecting the cap could plausibly have left some unsolved.
The value of this number is as an **existence proof that the repair-loop
mechanism works** and as **real failure-mode data**: see
`data/results/attempts/*.jsonl` for full attempt traces. Most repeat
failures traced back to one of two root causes worth knowing if you extend
this set:

1. Reaching for a tactic/lemma name that only exists in Mathlib (`ring`,
   `ring_nf`, `set`, `by_contra`, `Nat.even_or_odd`).
2. Mixing `x^2` and `x*x` notation for the same quantity mid-proof, which
   causes `omega`'s nonlinear-atom abstraction to treat syntactically
   different but mathematically equal subterms as unrelated -- fixed by
   committing to one notation throughout and using `simp only [...]`
   (rewrites every matching occurrence) instead of a single `rw` (only
   rewrites the first-unified one).

## What to do differently in your own environment

Your own machine (or a proper CI runner with full network access and more
than 1 core) will not hit either blocker:
- `lake exe cache get` will pull prebuilt Mathlib oleans in a few minutes
  instead of requiring a from-source build.
- With Mathlib available, swap back to the original Mathlib-idiomatic
  formalizations in `data/seed_problems.json`'s `expected_lean_statement`
  fields where they still reference `Even`, `Nat.ModEq`/`Int.ModEq`,
  `Finset.sum`, etc. -- `ring` alone would collapse most of the manual
  `simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, ...]` chains in
  `lean_project/generated/*.lean` into one-liners.
- With `GROQ_API_KEY` set, `src/pipeline.py` runs the four stages for real
  against the Groq API instead of hand-authoring each candidate proof --
  at that point you get real `wall_clock_seconds` and true model-generated
  first-attempt proofs, respecting the actual 5-repair cap, which will very
  likely have a *higher* failure rate on problems like `mod_002` than shown
  here. Worth comparing a couple of different Groq models against each
  other on this set once you're running for real -- first-attempt pass rate
  and repair-iteration count vary a lot between a fast small model and a
  larger one.

## Next milestone

Per `docs/roadmap.md`: scale to 50 problems, ideally with Mathlib available
so the category mix can expand beyond what's provable with core tactics
alone (combinatorics, inequalities needing AM-GM-style lemmas, more of
number theory). Keep a held-out split that prompts are never tuned against
before reporting a headline pass@1.

## Addendum: generated-proof/results mismatch found and fixed

A later commit (`f967161`, "Update results and generated proofs from
strong/fast model split run") silently overwrote 4 of this run's 20
`lean_project/generated/*.lean` files (`arith_001`, `arith_003`, `ineq_001`,
`mod_002`) with `import Mathlib`-dependent content from a different, later,
partial run (`data/results/run2_mathlib.jsonl`, which only actually covers
`arith_001` and `arith_003`). It did **not** update this file or
`data/results/run1_core_lean.jsonl`, whose `final_proof_path` for those 4
ids still pointed at the same files -- so for `ineq_001` and `mod_002` in
particular, the on-disk "evidence" no longer matched what was verified
(neither run1's original core-Lean claim nor any entry in run2, which
doesn't cover those two ids at all), and `arith_001`'s Mathlib content
wasn't backed by anything either (run2's `arith_001` entry has
`solved: false`).

Fixed by restoring `arith_001.lean`, `ineq_001.lean`, and `mod_002.lean` to
their original core-Lean-only content (recovered from commit `51f033c`,
before the overwrite). `mod_002.lean`'s `int_sq` helper needed one small
adjustment beyond a straight revert: its original `rfl`-based unfolding of
`a ^ 2 = a ^ 1 * a = a ^ 0 * a` no longer holds definitionally under the
now-pinned `leanprover/lean4:v4.33.0-rc1` toolchain (this Lean core's `^`
unfolding behaves differently than under the `4.14.0` this run originally
used) -- replaced with an explicit `rw [Int.pow_succ, Int.pow_succ,
Int.pow_zero, Int.one_mul]` chain instead. All three restored files were
independently compiled against a real, exact `leanprover/lean4:v4.33.0-rc1`
binary (downloaded directly from GitHub release assets, matching the
`lean_project/lean-toolchain` pin) and confirmed to produce zero errors and
no `sorry`/`sorryAx`/`admit`.

`arith_003.lean` was left as-is in its Mathlib form: it's the one file of
the four that *is* legitimately backed by `run2_mathlib.jsonl` (`solved:
true`, matching `lean_file_path`, embedded `final_proof` text matching what's
on disk). That does leave `data/results/run1_core_lean.jsonl`'s own
`arith_003` entry pointing at a file that no longer contains what it
verified -- a genuine conflict between two runs' claims about the same
problem id that wasn't resolved here, since picking a side would destroy
one run's evidence to satisfy the other. If you want a single canonical
answer for `arith_003`, worth either giving the two approaches distinct ids
(e.g. `arith_003_core` / `arith_003_mathlib`) or deciding which run's
verification should be treated as authoritative going forward.

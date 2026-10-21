# Compiler-Guided Repair: Implementation Plan

**Research title:** Compiler-Guided Repair for Natural-Language-to-Lean
Formalization

**Revision baseline:** 20 October 2026 major-revision report
**Current status:** Phase 0 complete; Phase 1 preparation complete (no API pilot
run); later phases have not been implemented or certified by this plan. This document records repository evidence and decisions
that must be reviewed before the 22 October milestone. It is not evidence that
the experiments or dataset are complete.

## Phase 0 — baseline and protocol decisions

### Worktree and scope

At inspection, the worktree had no reported tracked modifications. It did
contain untracked artifacts under `data/results/pilots/` and
`lean_project/generated/runs/` (including run manifests, attempt logs, and Lean
proofs). These files were left untouched. No dataset, paper, historical report,
prompt, code, or Lean source was changed in Phase 0.

No API calls, package installations, experiment runs, commits, or pushes were
made. The offline test commands and outcomes are recorded below. A Lean version
probe outside the project attempted to download an unpinned elan default
toolchain; it was stopped. No Lean build or compiler invocation was made.

### Existing functionality to reuse

- `src/llm_client.py` is a Groq chat-completions client. Its current configured
  defaults are `llama-3.3-70b-versatile` for the strong model and
  `llama-3.1-8b-instant` for the fast model; environment variables can override
  these aliases. Successful responses can include returned model, token
  counts, latency, and transport retry metadata. Model aliases are not pinned
  immutable revisions.
- `src/pipeline.py` runs natural language through formalization, optional
  proof sketch, synthesis, repair, and Lean verification. It supports
  `full_pipeline`, `no_sketch`, and `fast_model_only`, model overrides,
  per-run manifests, per-problem attempt logs, and run-isolated proof outputs.
- `src/formalize.py`, `src/proof_sketch.py`, `src/synthesize.py`, and
  `src/verify.py` implement those stages. Synthesis already records completion
  metadata and verification records; the verifier checks candidate source for
  `sorry`, `admit`, `axiom`, `constant`, and `opaque`, then inspects theorem
  axioms. These checks do not establish semantic faithfulness.
- `src/repair_experiment.py` already implements a fixed-theorem paired A/B/C
  structure: one initial candidate is reused, A makes no repairs, B is blind,
  C can receive structured diagnostics from verification, and the repair limit
  is constrained to 0–3. Existing tests cover shared candidates and diagnostic
  separation. Its default model is `openai/gpt-oss-120b`, distinct from the
  ordinary pipeline's Groq model defaults.
- `src/provenance.py` hashes inputs and prompts, records configuration,
  environment, git status, Lean version, and Mathlib revision. Completion
  metadata and verifier outputs are available from existing pipeline stages.
- `src/dataset_validation.py`, the curation guide, draft, and manifest provide
  a curation/validation foundation. The manifest identifies a 21-record draft,
  zero eligible records, proposed 15/6 development/test counts, and unresolved
  human-review fields. It is not a frozen or eligible experimental dataset.
- `docs/verification.md` documents current proof-safety behavior. `RUN_REPORT.md`
  explicitly identifies historical LLM-authored proofs as manual rather than
  API-generated; its historical numbers must not be relabeled as model pass@1.

### Offline baseline

Environment observed: Python 3.13.7, pytest 9.1.1. The Groq Python package was
not installed in this interpreter.

| Check | Outcome |
|---|---|
| `python3 -m pytest -q tests/test_dataset_validation.py tests/test_metrics.py tests/test_metrics_completeness.py tests/test_metrics_empty_results.py tests/test_provenance.py tests/test_verify.py` | **Passed:** 95 tests, 8 subtests |
| `python3 -m pytest -q` | **Blocked at collection:** six modules importing pipeline/client/experiment code fail with `ModuleNotFoundError: No module named 'groq'`; no package was installed |
| `python3 src/pipeline.py --help` and `python3 src/repair_experiment.py --help` | **Blocked at import** by the same missing Groq package |
| `elan toolchain list` | Installed toolchains include Lean 4.14.0, 4.32.0, and 4.33.0-rc1 |
| Repository Lean configuration | `lean_project/lean-toolchain` pins `leanprover/lean4:v4.33.0-rc1`; `lake-manifest.json` pins Mathlib to commit `46ff937713b1d85cf6642ff8164d212292e30f6b` |

The installed 4.32.0 is a stable candidate to investigate, not a compatibility
decision. Compatibility of any stable Lean release with the pinned Mathlib
revision has not been verified. Historical `RUN_REPORT.md` describes earlier
Lean 4.14.0 work, which is not the current project pin.

### Protocol decisions to freeze before paid/held-out runs

1. **Primary model and provider.** Select one model for the paired A/B/C
   comparison, with its exact provider identifier and immutable model revision
   or an explicit statement that the provider only exposes a mutable alias.
   Record the selection date and response-reported model identifiers. Current
   defaults disagree across the pipeline and experiment runner, and the
   current aliases are not immutable pins. Do not infer that a configured
   default is available, stable, or the approved primary model.
2. **Lean/Mathlib environment.** Select one stable Lean version and the
   compatible exact Mathlib revision; pin both in repository configuration.
   Validate that the actual execution version matches the recorded version.
   The existing release-candidate pin is not the stable environment decision.
3. **Condition controls.** Freeze one initial prompt, model, theorem statement,
   generation settings, and maximum of three repair calls for B and C. A is
   the same initial candidate with zero repairs. B receives no compiler
   diagnostics; C receives the genuine diagnostics from that candidate's
   corresponding Lean verification. Keep transport retries distinct from
   repair calls in all reporting.
4. **Dataset boundary.** Keep development items separate from held-out test
   items and freeze/hash the test set only after source/license, reference
   theorem, family/split, duplicate, and statement review. The current draft
   does not meet the minimum of 60 eligible held-out problems and 15
   development problems; do not use its current proposed split as a frozen
   evaluation set.
5. **Success interpretation.** Track verified Lean proof success separately
   from human semantic-faithfulness labels (`faithful`, `not faithful`, or
   `uncertain`). Compilation alone is not a faithfulness label. Separately
   report end-to-end formalization and proof success on a fixed,
   human-reviewed theorem.
6. **Spend approval.** No API smoke run or paid experiment should be launched
   until the user explicitly approves the model, input, call/repair budget,
   and expected spend. Do not expose API keys in commands, logs, or manifests.

## Phase 1 — preparation status (21 October 2026)

### Model and provider

`openai/gpt-oss-120b` remains the proposed primary model. The account-authenticated,
non-generative Groq model-list endpoint returned HTTP 200 and included that
identifier. This confirms it is listed for the credential used, not that a
generation request will succeed. No completion endpoint was called; generation
access remains unconfirmed pending explicit approval for a bounded pilot.
The model is a provider alias, not an immutable revision.
The checked endpoint was `https://api.groq.com/openai/v1/models`; only the HTTP
status and candidate-ID match were retained, not the credential or full body.

The paired runner already sends one `model` value to the initial call and every
B/C repair call; it does not switch between pipeline strong/fast models.
Manifests now record provider, exact requested model, execution mode, and
whether an API-generated candidate was actually received. Injected/mock
completion functions must be explicitly labeled `mock` or `manual`; they
cannot be passed as API mode. API mode requires the canonical Groq client.
Non-API runs have `provider: null`, with `configured_provider` separately
recorded, and leave `api_generation_confirmed` false. Raw model responses,
attempt IDs, timestamps, prompt hashes, compiler inputs/results, and the
requested/returned model metadata are retained. Missing `GROQ_API_KEY` raises
an actionable exception and is recorded as an incomplete provider error, not
a generated success.

### Lean/Mathlib pin and evidence

The previous project pin was Lean `v4.33.0-rc1` with Mathlib commit
`46ff937713b1d85cf6642ff8164d212292e30f6b`. Official Mathlib release metadata
identifies stable tag `v4.32.0` at commit
`81a5d257c8e410db227a6665ed08f64fea08e997`; the release's `lean-toolchain`
specifies `leanprover/lean4:v4.32.0`. The matching Lean release is marked
non-prerelease. Official references:
[Mathlib v4.32.0](https://github.com/leanprover-community/mathlib4/tree/v4.32.0)
and [Lean v4.32.0 release](https://github.com/leanprover/lean4/releases/tag/v4.32.0).

After verifying the pair in an isolated Mathlib worktree, the project is now
pinned to Lean `v4.32.0` and Mathlib commit
`81a5d257c8e410db227a6665ed08f64fea08e997`. `lake update` locked the full
dependency manifest to that release's compatible revisions. Verification:

```text
cd /tmp/nl2lean-mathlib-v4.32-check
lake exe cache get
lake env lean --version
lake build Mathlib
lake env lean /Users/sadiapeerzada/NLP-to-Formal-Language-Proof/lean_project/Nl2Lean/Basic.lean

cd /Users/sadiapeerzada/NLP-to-Formal-Language-Proof/lean_project
lake update
lake env lean --version
lake build Nl2Lean.Basic
```

The stable Mathlib cache fetched/decompressed 8,638 files in the project
environment; Mathlib built successfully (8,654 jobs). The documented
`Nl2Lean.Basic` target built successfully, and `generated/arith_001.lean`
compiled when checked with `import Mathlib` under Lean 4.32.0. The library-root target
initially failed with “some modules have bad imports” because no root module
existed. Adding `lean_project/Nl2Lean.lean` (which imports `Nl2Lean.Basic`)
fixed this, and `lake build Nl2Lean` now passes (8,657 jobs).

### Test and CLI validation

The repository `.venv` uses Groq SDK 1.5.0, satisfying the existing
`groq>=0.9.0` requirement. No dependency was installed or changed. The earlier
global `python3` lacks Groq; use the repository virtual environment for tests.

```text
.venv/bin/python -m pytest -q tests/test_llm_client.py tests/test_repair_experiment.py tests/test_verify.py
.venv/bin/python -m pytest -q
.venv/bin/python src/repair_experiment.py --help
.venv/bin/python src/repair_experiment.py --problem-id phase1-check --theorem-file lean_project/Nl2Lean/Basic.lean --model openai/gpt-oss-120b --plan-only
```

Final full-suite result after the changes: **158 passed, 8 subtests passed**.
Plan-only reported `api_calls_will_be_made: false`; no API generation was
performed. The verifier's existing checks against `sorry`, `admit`, disallowed
axioms, and theorem-statement mismatch remain covered by the passing tests.
An initial focused run exposed and corrected a raw-response assertion error.
A subsequent verifier test timed out while the isolated Mathlib build was
competing for resources; the standalone verifier tests later passed (26 tests,
8 subtests), and the final full suite passed without that timeout.

### Files changed in Phase 1 preparation

- `lean_project/lean-toolchain`, `lean_project/lakefile.toml`, and
  `lean_project/lake-manifest.json`: pin Lean/Mathlib to the verified stable
  pair and lock compatible dependencies.
- `src/llm_client.py`: defer client creation until a request, require the API
  key with a clear error, and include provider metadata.
- `src/repair_experiment.py`: record provider/model, API-vs-injected mode,
  generation confirmation, raw responses, stable attempt IDs/timestamps, and
  safe missing-key/rate-limit/timeout classifications. Blind B retries now
  continue without diagnostics when C must stop because compiler diagnostics
  are absent or malformed.
- `tests/test_llm_client.py` and `tests/test_repair_experiment.py`: deterministic
  coverage for missing credentials, injected-run provenance, raw-response and
  attempt persistence, same-model use, and blind retry behavior without
  diagnostics.

The ordinary NL-to-Lean pipeline still uses separate strong/fast model
defaults, whereas the paired fixed-theorem runner uses the single explicit
`openai/gpt-oss-120b` identifier. Keep those tasks/results separate; do not
present pipeline outcomes as the paired repair comparison.

### Pilot remains gated

The draft dataset is still not a source-verified or reviewed split: the
manifest has 21 records and zero eligible records, with proposed 15/6
development/test counts. No human-reviewed fixed theorem or approved
development problem is selected. A pilot is therefore not ready to run, even
though the Lean environment and paired runner are prepared.

After selecting and reviewing one development theorem, use a new, unused
output root and obtain explicit approval for the model, exact input, maximum
spend, and calls before running:

```text
.venv/bin/python src/repair_experiment.py --problem-id <approved-development-id> --theorem-file <reviewed-fixed-theorem.lean> --lean-project lean_project --output-root data/experiments/phase1-pilot-<unique-id> --model openai/gpt-oss-120b --max-repair 3
```

This command was not run. At most, it makes seven logical completion calls
(one shared initial call, then up to three repairs in each of B and C), with
up to three transport attempts per logical call. Estimate cost using current
account pricing before approval. Do not place a real API key in shell history
or output.

## Phase 1 — protocol fixes before the pilot (21 October 2026)

- **Repair templates.** `prompts/repair_experiment_blind.txt` and
  `prompts/repair_experiment_compiler_guided.txt` are byte-identical, so the
  B and C prompts differ only in the `{feedback}` field. The shared
  instruction no longer says to assume no compiler feedback, which would have
  contradicted condition C.
- **Reference-theorem warning.** The fixed theorem is compiled with `sorry` as
  a reference, so Lean reports a `hasSorry` warning that describes the
  reference, not the candidate. Candidates containing `sorry` are rejected
  before compilation. Condition C feedback now excludes `hasSorry`
  diagnostics. If nothing else remains, C stops with a recorded status
  instead of raising. Raw verifier output is unchanged.
- **Statement-only pilot input.** `data/pilot_inputs/arith_001_statement.lean`
  holds the theorem statement with a `sorry` body. The historical manual proof
  in `lean_project/generated/arith_001.lean` must not be used as pilot input,
  because the runner places the file contents in the prompt. An offline check
  accepted the manual proof against this reference and rejected a candidate
  containing `sorry`; no API call was made.
- **Tests.** Full suite: 160 passed, 8 subtests passed.

Status: no API generation has run, and `arith_001` has no recorded
human review (its curation fields remain pending).

## Later phases — gated, not completed

- **Phase 2:** enforce and test matched A/B/C traces using the selected single
  model, same initial candidate/theorem/settings, and no more than three
  repairs per repaired condition.
- **Phase 3:** conduct source-verified, human-reviewed dataset curation;
  maintain development/held-out separation; freeze and hash only after the
  required counts and reviews are complete.
- **Phase 4:** collect structured semantic-faithfulness judgments and report
  them independently of Lean compilation.
- **Phase 5:** derive metrics only from validated raw traces; include
  denominators, uncertainty intervals, paired comparisons (such as McNemar's
  test), error-category outcomes, calls, tokens, and time.
- **Phase 6:** maintain the pinned stable Lean/Mathlib environment, expand
  proof-safety tests, and preserve artifact hashes.
- **Phase 7:** reconcile README and historical reporting with validated
  experiment artifacts. Never present manually achieved historical success
  as model pass@1.

## Next step

Phase 1 implementation and environment preparation are complete, but no
genuine API generation or pilot has run. Before launch, review the proposed
model, select a human-reviewed development theorem, reserve a new output
directory, and explicitly approve the API-call and spend budget. Held-out
dataset curation and all later research phases remain incomplete.

## Focused pilot safety audit (21 October 2026)

The requested `arith_001` plan-only invocation was run with:

```text
.venv/bin/python src/repair_experiment.py --problem-id arith_001 --theorem-file data/pilot_inputs/arith_001_statement.lean --lean-project lean_project --output-root data/experiments/phase1-pilot-001 --model openai/gpt-oss-120b --max-repair 3 --plan-only
```

It reported the reviewed statement-file SHA-256
`5e12ab27a670e19eafb7fa1c597cff6c18b18c132df53b0fdf78e0fd2d363669`.
The record at `data/pilot_inputs/arith_001_review.json` is an author
self-review, marked `needs_review`, and explicitly says it is not independent.
It is not an independent semantic review.

### Execution and retry audit

- The initial completion is generated once. Its candidate is then used for A,
  B, and C; A performs no repair, while B and C each allow up to three repairs.
- The maximum is seven logical completions: one shared initial completion and
  six repairs.
- The runner calls the Groq wrapper up to three total attempts per logical
  completion. Groq SDK 1.5.0 separately defaults to two retries (three HTTP
  attempts per wrapper call). The SDK retry count is now explicit, not implicit.
- Therefore the current worst-case bound is 63 HTTP attempts for the
  one-problem A/B/C run. Existing completion metadata records the wrapper-level
  attempt count and retry events, but not a complete trace of SDK-internal
  attempts. No experiment has run under this path.
- The initial candidate is shared across conditions; B does not receive
  compiler diagnostics, and C receives the recorded diagnostics from its
  corresponding Lean verification. Existing tests exercise those invariants.

### Cost and output safeguards

The available official Groq model documentation
(`https://console.groq.com/docs/models`) did not expose a per-token price for
`openai/gpt-oss-120b`; `https://groq.com/pricing` redirected to the general
homepage during this audit. No price was inferred. Consequently, the runner
now fails closed before creating output or invoking the API until a dated
official input/output price is verified and a per-attempt reservation guard is
available. Plan-only records the $0.10 intended budget, unknown pricing, and
no cost estimate. This is a preflight-only restriction, not a billing cap.
Even after a future local token estimate is added, it cannot guarantee the
provider's final bill exactly.

The runner now requires the output root itself to be new, so an existing
directory cannot be reused as an output location. The requested path
`data/experiments/phase1-pilot-001` was absent during this audit. Plan-only
does not create it. No existing pilot result or generated Lean run artifact was
modified.

The next required steps are to verify the model's published token prices from
an official source, implement and test per-HTTP-attempt budget reservation
using a conservative input-token bound, and obtain independent semantic review
of the theorem. No API generation or paid experiment was run.

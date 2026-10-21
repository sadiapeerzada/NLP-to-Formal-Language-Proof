# Compiler-Guided Repair Experiment Protocol

**Status:** proposed machine-readable specification; implementation-locked for
reproducibility checks, but not independently reviewed, preregistered, or
authorized for API execution.
**Version:** 0.2.0
**Prepared:** 21 October 2026  
**Study:** *Compiler-Guided Repair for Natural-Language-to-Lean
Formalization*

This document defines the intended empirical comparison and its execution
gates. It records protocol decisions separately from implemented safeguards.
No experiment result, independent review, dataset freeze, pricing verification,
or API pilot is asserted here.

The machine-readable specification is
[`configs/repair_experiment_protocol_v0.2.0.json`](../configs/repair_experiment_protocol_v0.2.0.json).
It identifies exact prompt files by SHA-256, the requested model alias,
decoding, retry limits, analysis plan, and pinned Lean/Mathlib project files.
Each run plan and manifest records that configuration's SHA-256. Hashes bind
bytes to an identifier; they do not authenticate pricing, reviewers, or other
claims in those bytes.

## 1. Research question and outcomes

**Primary question:** For a fixed, independently reviewed Lean theorem and a
shared initial model-generated proof candidate, does providing real Lean
compiler diagnostics improve verified proof success over equally budgeted
blind retries and one-shot generation?

The fixed-theorem repair experiment measures proof construction and repair. It
does not establish that a natural-language statement was formalized faithfully.
End-to-end formalization is a separate outcome: a generated theorem statement
must receive independent semantic review and its proof must compile. Proof
compilation alone is not a fidelity label.

## 2. Provider, model, and decoding

- **Proposed provider:** Groq.
- **Proposed requested model ID:** `openai/gpt-oss-120b`.
- This is a mutable provider alias. Account-specific generation access and an
  immutable model revision are unverified; model-list membership is not proof
  of generation access. There is no fallback model.
- The model choice remains **provisional** until an explicitly approved,
  cost-limited real generation pilot completes successfully and the returned
  provider/model metadata are audited.
- Record the requested model ID and the exact returned model ID for every
  successful API response, together with provider metadata, Groq SDK version,
  timestamps, finish reason, usage, decoding parameters, and errors. Missing
  response metadata remains missing; it is not replaced with the requested ID.
- Locked runner settings are temperature `0.2`, maximum completion tokens
  `2000`, and `reasoning_effort="low"` for GPT-OSS. The run configuration must
  record the actual values sent. The ordinary end-to-end pipeline uses
  separately configurable strong/fast model defaults and is not the paired
  experiment.
- Treat the model string as a provider alias, not an immutable model snapshot.
  Record it exactly, but do not claim that it pins model weights or a serving
  implementation.
- No generation seed is sent, so provider sampling is not claimed deterministic.
  The protocol uses one matched trajectory per problem; transport attempts are
  not independent samples. The paired bootstrap uses 10,000 problem-level
  resamples and seed `20271021`. No API call is authorized by this document.

## 3. Paired A/B/C design

For each eligible problem, generate exactly one initial candidate from one
shared initial prompt. Preserve its response, candidate bytes, ID, and SHA-256
unchanged across all conditions. Use the same fixed theorem, requested model,
decoding settings, and Lean project for A, B, and C.

| Condition | Initial candidate | Repair policy | Maximum repair calls |
|---|---|---|---:|
| A — One-shot | Shared candidate | Verify once; no repairs | 0 |
| B — Blind retries | Same shared candidate | Retry without compiler diagnostics | 3 |
| C — Compiler-guided repair | Same shared candidate | Each repair receives genuine diagnostics from the immediately preceding failed Lean verification | 3 |

Repair calls are condition-specific: B may make up to three and C may make up
to three. These are additional to the one shared initial completion. Therefore
the maximum is seven logical completions per problem (one initial plus three
in each repaired condition). A repair call is not an independent sample.

**Information boundary:** Each B repair may receive the theorem, current
candidate, and the fixed blind-feedback text only. It must not receive
diagnostics, error text, verifier exception detail, diagnostic-derived
summaries, or prior assistant/tool messages that contain such information.
Use a fresh stateless request per repair or demonstrate that the complete
provider conversation context contains no diagnostics. C receives only
structured diagnostics produced by the corresponding failed Lean compilation;
record the exact diagnostic payload and verification record that produced it.
If C has no usable candidate diagnostics, do not invent feedback or substitute
another condition.

**Termination and failure handling:**

- Initial transport/provider failure: mark the problem's paired run incomplete;
  do not start conditions without a shared candidate.
- Any transport retry stays inside the same logical completion and is logged
  as a transport attempt, not a new model sample or repair call. If retries
  exhaust, persist the error and stop the affected condition; do not silently
  substitute a model.
- Empty or malformed model output consumes that logical completion. Record it
  as an output failure, do not accept it as a proof, and do not silently
  regenerate an identical request. Other conditions may proceed only when
  their required prior state exists and the experiment runner can preserve the
  paired trace.
- A valid non-empty candidate that fails Lean compilation may be repaired
  within the condition's remaining budget. A Lean timeout, verifier
  infrastructure error, input error, or unavailable diagnostics is not a
  compiler error eligible for guided feedback. Record its failure category
  and terminate that condition; do not treat a timeout as a proof failure
  with usable diagnostics.
- Stop a condition on verified success, non-repairable verification failure,
  API failure, malformed/empty output, or exhausted repair budget. Keep all
  attempted calls and terminal reasons.
- The analysis must report incomplete/missing conditions explicitly. It must
  not silently drop failed API calls or transport attempts from accounting.

## 4. Lean verification and semantic fidelity

Use one pinned Lean toolchain and one exact Mathlib dependency state for all
conditions and problems in a run. Record the `lean-toolchain`, complete
`lake-manifest.json` SHA-256, Mathlib revision, project configuration hash,
Lean executable/version, and verification command. Do not compare conditions
run under different environments.

Every final proof candidate must pass the repository verifier on the same
fixed theorem. Reject candidates containing `sorry`, `sorryAx`, or `admit`,
or introducing unapproved `axiom`, `constant`, or `opaque` declarations.
Inspect theorem axioms and allow only the repository-approved standard
dependencies (`propext`, `Classical.choice`, and `Quot.sound`). Preserve the
exact generated source, verification source, compiler diagnostics, exit code,
and failure reason. A successful compiler result is evidence of proof
verification only, not English/Lean equivalence.

For each English/Lean reference pair, a reviewer other than the author must
independently inspect quantifiers, types, assumptions, notation, coercions,
domain boundaries, edge cases, imports, and self-containment. Record one
label: `faithful`, `not faithful`, or `uncertain`, with reviewer ID, date, and
evidence. Author self-review and Copilot-assisted review do not qualify as
independent review. Preserve disagreement and adjudication evidence; if
reviewers disagree, an independent adjudicator records the resolution. An
unresolved judgment remains `uncertain` and is not counted as faithful.

## 5. Metrics and analysis plan

The experimental unit is the problem. For each problem, retain matched binary
outcomes for A, B, and C.

### Predefined outcomes

1. **Initial-candidate verified success:** number of shared initial candidates
   accepted by Lean and the proof-safety checks divided by the number of
   eligible problems with an initial candidate and completed verification.
   This is the common no-repair outcome and corresponds to A.
2. **Verified success within budget:** for each condition, number of problems
   with an accepted verified proof by that condition's stopping point divided
   by its analyzable denominator. A includes only the initial candidate; B and
   C include their repairs.
3. **Absolute paired difference:** for each pair of conditions, the difference
   in their matched success proportions, reported in percentage points.
4. **Relative difference:** `(rate_new - rate_reference) / rate_reference`,
   reported only when the reference rate is nonzero; otherwise mark undefined,
   not zero or infinite.
5. **Compiler-error outcomes:** first-attempt compiler-error categories and
   repair outcomes by category, with the number of problems/candidates in each
   category and explicit denominators. Categories derive from actual Lean
   diagnostics; unclear/unparsed categories remain `other` or
   `unclassified`.
6. **Cost and effort:** logical completions, underlying HTTP attempts,
   prompt/completion tokens when returned, missing usage metadata, estimated
   cost, and wall-clock time per problem and condition. Retried transport
   attempts are included in resource accounting.
7. **End-to-end faithful formalization:** a separate count/rate requiring a
   `faithful` human label and a verified proof for the generated statement.
   Report `not faithful` and `uncertain` separately; do not infer faithfulness
   from compilation.

### Denominators, intervals, and tests

- Report the number of eligible frozen records, attempted runs, complete
  matched triples, and missing/incomplete runs for every outcome. Predefine
  exclusions before test access. API, model, malformed-output, compiler, and
  repair-budget failures remain reported outcomes; they are not removed to
  improve success rates.
- Report Wilson 95% intervals for individual binary proportions and paired
  problem-level bootstrap 95% intervals for absolute rate differences. State
  resampling unit (problem), number of resamples, and deterministic seed in
  the analysis manifest.
- Use two-sided exact McNemar tests on complete matched binary outcomes.
  `C` versus `B` is the primary comparison; `C` versus `A` and `B` versus `A`
  are secondary. Apply Holm correction across these three planned tests.
  Report discordant-pair counts and both raw and adjusted p-values. If a
  comparison has no discordant pairs, report the test as non-informative
  rather than implying evidence of equivalence.
- Category analyses are descriptive unless explicitly preregistered as
  confirmatory. Show category denominators and intervals; do not infer a
  category effect from a small cell without qualification.
- Preserve the full eligible-set denominator and a complete-case paired
  analysis. Also provide a conservative sensitivity analysis counting
  incomplete runs as failures in each condition, identifying this separately
  from the complete-case McNemar test.
- Historical manually authored proofs are development/debugging artifacts,
  not model-generated outputs and never model pass@1 results.

## 6. Dataset and freeze requirements

Use the curation schema and validator in [schema.md](../data/schema.md),
[curation_guide.md](../data/curation_guide.md), and
`src/dataset_validation.py`. The target is at least 60 eligible, frozen test
problems and 15–20 separate eligible development problems. Candidate counts
must remain distinct from eligible counts.

Each eligible record requires verified source and item-level license/rights
evidence; source/license evidence bound to the exact Lean statement with
SHA-256 of its exact UTF-8 bytes; successful Lean reference-theorem
verification with matching statement hash and pinned environment metadata;
category and difficulty labels; independent semantic, theorem-statement,
assumption, self-containment, family, split, and duplicate reviews; and an
explicit family-aware split assignment.

Keep each mathematical family wholly in one split. Treat exact and
similarity-based duplicate checks as review aids, not semantic decisions.
Before freeze, record an independent human disposition for every flagged
similarity pair; unresolved pairs block freezing. Freeze development and test
as separate files. Record exact-byte SHA-256 hashes, exact ordered IDs,
candidate and eligible counts, freeze date and approval evidence, dataset
author IDs, locked protocol hash, and test-access policy. Validate with the
frozen-curation command. No current draft record is promoted by this
protocol; dataset eligibility and freeze remain manual-review gates.

Development data may be used for prompt/model/policy development. Lock the
prompts, model configuration, repair policy, analysis plan, and protocol hash
before the test custodian releases the held-out set. Test statements, labels,
answers, and results must not be used for tuning. This is a procedural access
control; a manifest declaration alone cannot enforce it.

## 7. Cost and API safety

### Price reference and verification status

The model-specific official reference is Groq's [GPT-OSS 120B model
documentation](https://console.groq.com/docs/model/openai/gpt-oss-120b). Its
displayed rates were observed during preparation, but the page has not been
archived in this repository or independently reviewed, account/region terms
have not been checked, and no pricing values are configured. Therefore rates
and billable behavior remain **unverified** and must not be used to authorize a
run. A model-list response establishes neither generation access nor pricing.

Before any future run, archive official evidence showing the exact model ID,
input and output rates, currency, and any applicable account/region
conditions. Record its retrieval date, source URL, and SHA-256, then have a
named human reviewer inspect the archived bytes and model-specific rates.
Cached
input discounts must not be assumed; calculate with the non-cached input rate.
The implementation requires these declarations through `GROQ_COST_*`
environment settings. A hash only checks byte identity; it cannot prove that
the archived source is official, current, model-specific, or interpreted
correctly. Human-review status and reviewer fields are assertions, not
cryptographic authentication. API execution remains disabled in code even
when configuration is present.

### Conservative reservation formula

The fail-closed `src/cost_guard.py` requires configured maximum input/output
tokens, a per-HTTP-attempt reservation ceiling, per-problem and total budgets,
official pricing source/model/timestamp/evidence hash, and an input-framing
overhead bound. For each request it requires the UTF-8 prompt byte length plus
the configured overhead bound to fit the input-token limit. This is a local
conservative bound on prompt text, not a provider tokenizer or verified bound
on undisclosed request framing. A researcher must justify the overhead bound;
if it cannot be defended, execution must remain blocked. The estimated
per-request cost uses the configured maximum input and output tokens at the
verified non-cached input and output rates:

```text
(maximum input tokens * input USD/M + maximum output tokens * output USD/M)
/ 1,000,000
```

The computed amount must not exceed the configured maximum reservation per
HTTP attempt. Configuration rejects absent, non-finite, zero/negative rates or
budgets, invalid token limits, mismatched pricing model IDs, non-official
source domains, malformed verification timestamps, and malformed evidence
hashes. These fields are declarations and do not authenticate the underlying
pricing evidence; a human must inspect the archived official source. The guard
reserves for each possible SDK HTTP attempt before calling the SDK; because
SDK-internal retries are opaque, it reserves all configured SDK retries plus
the initial request as a batch before each wrapper attempt. Reservations are
not released after success, failure, or ambiguous timeout, which intentionally
overestimates when fewer requests were sent.

Required settings are
`GROQ_COST_INPUT_USD_PER_MILLION_TOKENS`,
`GROQ_COST_OUTPUT_USD_PER_MILLION_TOKENS`,
`GROQ_COST_MAX_INPUT_TOKENS`, `GROQ_COST_MAX_OUTPUT_TOKENS`,
`GROQ_COST_INPUT_OVERHEAD_TOKEN_BOUND`,
`GROQ_COST_MAX_PER_HTTP_ATTEMPT_USD`,
`GROQ_COST_PER_PROBLEM_BUDGET_USD`, `GROQ_COST_TOTAL_BUDGET_USD`,
`GROQ_COST_PRICING_SOURCE_URL`, `GROQ_COST_PRICING_MODEL_ID`, retrieval date,
currency, pricing review status/date/reviewer, archived evidence path/hash,
and input-bound review status/date/reviewer/evidence. No pricing values or
reviewed bounds are presently configured. The evidence path must be readable
and its exact bytes
must match the declared SHA-256. This integrity check does not validate that
the archived content is genuine official pricing evidence. The input check
counts UTF-8 prompt bytes plus the operator-supplied
framing overhead bound; it is conservative for the text payload but not a
verified model tokenizer or bound on provider-side framing. If that framing
bound cannot be substantiated, API execution must remain blocked.

The current runner allows at most seven logical completions per problem. It
has three wrapper attempts per logical completion; the Groq SDK is configured
with two retries per wrapper attempt (three HTTP attempts total). If both
layers reach their configured maximum, reserve for:

```text
7 logical completions * 3 wrapper attempts * 3 SDK HTTP attempts
= 63 HTTP attempts
63 * configured per-HTTP-attempt estimate
```

The intended pilot ceiling remains **$0.10 per problem** and **$0.10 total**,
but exact fit is unknown until official rates and validated request bounds are
available. Configure the caps explicitly and reserve against both before
transmission. The experiment runner still has `API_EXECUTION_ENABLED = False`;
this guard does not authorize or enable a pilot. The local estimate cannot
guarantee Groq's final invoice because tokenizer/framing and billing treatment
may differ. Preserve estimates, reservations, observed usage when available,
and potentially billable timeout outcomes.

## 8. Reproducibility record

Each run manifest and its immutable associated logs must include, where
available and explicitly null/unknown otherwise:

- protocol version/hash, dataset version and exact development/test hashes,
  problem ID, ordered split membership, source/reference statement hash,
  semantic-review label and review evidence reference;
- run ID, execution mode (`api`, `mock`, or `manual`), start/end timestamps,
  provider, requested and returned model IDs, SDK/client versions, system
  metadata, temperature, reasoning effort, token limits, and all other
  request configuration;
- initial prompt/template hashes and rendered-prompt hashes; preserve exact
  prompts or an auditable secure prompt artifact reference; raw initial and
  repair responses; candidate text, stable attempt IDs, candidate hashes,
  timestamps, model usage, latency, and errors;
- each logical completion, each transport/SDK HTTP attempt and retry event,
  status/error/timeout, whether potentially billable, and reserved/estimated
  cost. Do not log API keys or secrets;
- exact Lean toolchain, Mathlib revision, Lake manifest/project hashes,
  operating environment, verifier policy, compiler command, verification
  source bytes/hash, exit status, structured/raw compiler diagnostics, proof
  safety result, verdict, failure category, and elapsed time;
- A/B/C starting-candidate IDs and hashes, repair counts/budgets, prompt
  hashes, diagnostic provenance, condition milestones, final outcomes, and
  missing/incomplete reasons;
- analysis script/version/hash, preregistered metrics and exclusions,
  manifest validation results, and hashes for raw logs and derived outputs.

Raw artifacts are append-only and must be written to a new unique output
directory. Mock/manual/API provenance must remain distinguishable. Missing
metadata is recorded as missing, never inferred from configuration. Preserve
failed and timed-out attempts, not only successful outcomes.

## 9. Execution gates

No larger experiment may begin until all gates have documented approval:

1. **Protocol reviewed and frozen:** resolve protocol decisions, record
   reviewer approval and protocol hash, and lock prompts, model settings,
   analysis, failure rules, and budgets before test access.
2. **Dataset validated and frozen:** satisfy the eligible development/test
   counts, independent review and duplicate disposition requirements, family
   separation, exact hashes, and access controls. Current draft status does
   not pass this gate.
3. **Pricing and cost guard verified:** archive and human-review official
   model-specific pricing and account terms; substantiate input framing/token
   bounds; verify fail-closed per-HTTP-attempt reservations persisted before
   transmission, retry accounting, ambiguous timeout treatment, and
   per-problem/total caps. Mock tests cover these controls, but evidence and
   bounds remain unreviewed and API execution remains disabled.
4. **One approved, cost-limited API pilot succeeds end to end:** obtain
   explicit approval for the exact development problem, model, request
   settings, fresh output directory, and maximum spend; then verify genuine
   API provenance, returned metadata, A/B/C traces, Lean logs, and cost
   records. No pilot has been run under this protocol.
5. **Pilot traces audited before scale-up:** independently inspect raw
   requests/responses, diagnostics, retry attempts, manifests, safety checks,
   costs, and failure handling. Any mismatch blocks larger runs.

Passing one gate does not imply that later gates pass. This document alone
does not authorize API use, establish implementation completeness, freeze the
dataset, or support research claims.

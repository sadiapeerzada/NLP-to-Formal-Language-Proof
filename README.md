# Compiler-Guided Proof Repair in Lean 4

### A Controlled Local-Model Pilot on Fixed Theorem Types

> **Research status:** A bounded empirical **proof-synthesis pilot**, not an autonomous natural-language-to-Lean translation benchmark. The frozen held-out study **does not establish a robust verified-proof advantage** for compiler-guided retries over blind retries. Later process results are **exploratory and suggestive**, not proof that the model uses compiler diagnostics.
>
> **Current manuscript:** [updated anonymous LaTeX source (review branch)](https://github.com/sadiapeerzada/NLP-to-Formal-Language-Proof/blob/manuscript/exploratory-process-update-20261030/publication/paper/main.tex) · [manuscript change log](https://github.com/sadiapeerzada/NLP-to-Formal-Language-Proof/blob/manuscript/exploratory-process-update-20261030/publication/post_hoc/outputs/post_hoc/MANUSCRIPT_CHANGES.md). This manuscript update is **not merged into main**, and conference-submission readiness has not been independently established.

## Contents

- [Overview and research question](#overview-and-research-question)
- [Study design](#study-design)
- [Dataset, model and environment](#dataset-model-and-environment)
- [Primary verification results](#primary-verification-results)
- [Exploratory post-hoc process findings](#exploratory-post-hoc-process-findings)
- [Development placebo](#development-placebo)
- [Interpretation and limitations](#interpretation-and-limitations)
- [Repository structure](#repository-structure)
- [Reproduce and audit](#reproduce-and-audit)
- [Manuscript status](#manuscript-status)
- [Rights, attribution and provenance](#rights-attribution-and-provenance)

## Overview and research question

**Question:** Once an initial Lean proof candidate fails, does presenting genuine compiler diagnostics produce **more strictly verified proofs** than allowing an otherwise comparable **blind retry**?

Compiler messages can describe syntax errors, unknown identifiers, type mismatches or unsolved goals. However, a model might also change its output simply because it gets another generation call. The study separates those two possibilities by comparing a diagnostic-guided repair arm against a retry arm that receives **no compiler messages**.

Each example pairs English text with a **fixed, AI-reviewed Lean theorem type**. The model supplies proof text for that type. The verifier enforces an exact target type, rejects proof placeholders and unauthorized declarations, and checks axiom dependencies. The study therefore assesses **proof synthesis and repair given a theorem type**. It does **not** measure autonomous translation from English into theorem statements or independent human accuracy of those statements.

**Contributions:** A controlled shared-initial comparison, strict compiler/kernel verification, explicit missingness accounting, authentic failure taxonomy and qualitative cases, measured resource costs, and a transparently labeled post-hoc process analysis with a development placebo.

## Study design

| Condition | Feedback and behavior | Maximum repair calls | Role |
|---|---|---:|---|
| **A: one-shot** | Generate one proof for the fixed theorem type | **0** | Initial generation baseline |
| **B: blind retry** | Retry using its previous candidate and constant blind-feedback text; **never receives compiler diagnostics** | **3** | Controls for the value of additional calls |
| **C: compiler-guided repair** | Retry using its previous candidate and **actual structured errors from its immediately preceding Lean verification** | **3** | Tests diagnostic-conditioned repair |

For a given theorem, **B and C start from the identical initial candidate bytes**. Each branch then follows its own repair history and independent context-derived random streams. The first repair is thus the **only step comparing identical predecessor candidates**; repairs 2 and 3 usually start from different predecessors.

The study uses fixed context and output caps, but **does not match actual total input-token costs**: C's real diagnostics lengthen its prompts. The branches were executed **B before C** rather than in randomized order. Successful branches stop. Interrupted or over-budget calls are recorded explicitly rather than silently regenerated.

**Strict verification:** the target must have the exact reviewed theorem type; placeholders such as sorry are rejected, and axiom dependencies must remain within the allowed standard set (propext, Classical.choice and Quot.sound). Compilation by itself cannot certify that the English wording and fixed Lean statement mean the same thing.

## Dataset, model and environment

| Property | Recorded value |
|---|---|
| Curated eligible statements | **75** |
| Development / held-out test | **15 / 60** |
| Curated family clusters | **5 development / 54 test** (no family overlap across splits) |
| Evaluated task | Proof synthesis against **fixed reviewed theorem types** |
| Local model | **mlx-community/Qwen2.5-7B-Instruct-4bit** |
| Execution | Offline local MLX, one primary seed **2027** |
| Sampling | Temperature **0.2**, top-p **1** |
| Context / output limits | **8,192** total context tokens / **2,000** maximum output tokens |
| Repair budget | At most **3** per repair branch |
| Lean environment | Lean **4.32.0**, pinned Mathlib |
| Hardware class | Local Apple M4 with **16 GiB** physical memory |

The dataset and protocol were **internally frozen before held-out generation** with stored hashes and source records. They were **not publicly preregistered**. Dataset semantic screening relied on an AI-assisted adjudication policy **without independent human-gold labels**. No autonomous model-generated theorem-type accuracy was measured.

**Two different development phases:** the pre-test **three-case protocol pilot** was used to check syntax/memory/procedural controls before held-out inference. The later **15-problem post-hoc development placebo** is a separate exploratory control and must not be conflated with that pilot.

## Primary verification results

### Held-out success and missingness

| Condition | Verified / observed cases | Unavailable cases | Observed success rate |
|---|---:|---:|---:|
| **A** | **0/60** | 0 | **0.00%** |
| **B** | **1/60** | 0 | **1.67%** |
| **C** | **1/58** | **2** | **1.72%** |

C has **57 known failures and two unavailable outcomes**. The separate, planned **missing-as-failure sensitivity** is **C = 1/60 (1.67%)**; it does not replace the primary observed rate **1/58**.

Across **58 complete paired B/C trajectories**, both conditions verified **1/58 (1.72%)**, and they succeeded on the **same theorem**. Thus:

- Observed paired **C minus B success difference: 0.00 percentage points**.
- Discordant pairs: **zero**; conventional exact two-sided **McNemar p = 1.0**, **non-informative for equivalence**.
- Conditional empirical problem/family bootstrap C−B interval: **[0.00, 0.00] pp**. Its degeneracy reflects identical observed paired outcomes, **not precise evidence of equivalence**.
- Independent-pair Newcombe paired method-10 sensitivity interval: **[−6.83, +6.83] pp** (assumption-dependent, not family-cluster inference).
- Full-cohort missingness identification bounds: **0 to +3.33 pp** for C−B, distinct from any confidence interval.

**Primary interpretation:** The data establish neither a robust **verified-success superiority** of C over B nor **equivalence** between the two methods. With only one solved paired target, power to distinguish the conditions is severely limited.

See [final experiment results](publication/docs/FINAL_EXPERIMENT_RESULTS.md), [paired comparison audit](publication/docs/PAIRED_COMPARISON_AUDIT.md), and [public case records](publication/results/cases.json).

## Exploratory post-hoc process findings

These metrics were **defined after observing the held-out outcomes**, computed from existing stored artifacts, and are **not confirmatory tests**. No new inference, replay, or imputation was performed.

### Byte-identical proof retries

A retry counts as identical only when its proof candidate is **byte-for-byte equal to the immediately preceding candidate**.

| Held-out completed repair group | B (blind) | C (real diagnostics) |
|---|---:|---:|
| **All repair indices pooled** | **90/178 (50.6%)** | **70/172 (40.7%)** |
| **First repair only** | **17/60 (28.3%)** | **10/58 (17.2%)** |
| **Repairs 2 and 3 pooled** | **73/118 (61.9%)** | **60/114 (52.6%)** |

The pooled exploratory **C−B repetition difference is −9.86 percentage points**, with a whole-family cluster-bootstrap **95% CI [−19.77, −0.50] pp**. The CI upper endpoint barely excludes zero; the result is among several post-hoc contrasts, **without multiplicity adjustment**.

For **first repairs only**, where the initial candidate is shared, C−B is **−11.09 pp**, with whole-family bootstrap **95% CI [−22.00, −0.86] pp**. **Two unavailable C first repairs were excluded** from its denominator. Both bootstrap analyses use **10,000 whole-family resamples, seed 20271021**.

For repairs **2–3**, each branch can have a **different preceding candidate**, so the pooled comparison partly reflects different candidate histories. **Fewer repeated bytes are a suggestive process association, not proof of diagnostic-content use or increased verified success.**

### Unknown-name removal is not evidence of diagnostic use

A preceding unknown name disappeared in **12/76** eligible B repairs and **14/70** C repairs. **B never saw compiler diagnostics:** its preceding messages were available **only to the analyst**, supplying a chance baseline. Syntactic disappearance of a name, fewer compiler messages or greater edit distance **does not demonstrate a verified mathematical fix**.

Supporting sources: [held-out repair metrics](publication/post_hoc/outputs/post_hoc/post_hoc_repair_metrics.csv), [post-hoc summary](publication/post_hoc/outputs/post_hoc/SUMMARY.md) and [manuscript-update numbers](publication/post_hoc/outputs/post_hoc/manuscript_update_numbers.csv).

## Development placebo

A separate **post-hoc development-only control** used **15 problems**, **five family clusters**, **one seed**, and genuine **different-problem/family donor diagnostics** in a placebo arm. The real compiler-message content was retained; only filename metadata was normalized consistently.

| Development process result | B (blind) | C (real) | C_placebo (mismatched) |
|---|---:|---:|---:|
| **Exact-copy repetition** | **22/45 (48.9%)** | **23/45 (51.1%)** | **32/45 (71.1%)** |
| **Preceding unknown-name removal** | **1/18** | **3/19** | **2/17** |
| **Verified proofs** | **0/15** | **0/15** | **0/15** |

Development **A also verified 0/15**.

Real diagnostics were associated with **less repetition than mismatched diagnostics**, **not less than blind B**. The higher copying rate under placebo may indicate **confusion from irrelevant feedback**; this control cannot distinguish that possibility from ignoring feedback. The name-removal contrast **3/19 vs 2/17 is only a one-event difference**, not evidence that the model used diagnostic content.

This comparison is strictly **descriptive (15 problems, five families, one seed, no hypothesis test)** and did **not** improve verified proof success. See [development metrics](publication/post_hoc/outputs/post_hoc/post_hoc_dev_repair_metrics.csv), [development summary](publication/post_hoc/outputs/post_hoc/post_hoc_dev_summary.json) and [placebo protocol and code](publication/post_hoc/extensions/).

## Interpretation and limitations

**What the observations support:** Under the frozen bounded configuration, guided retries were **associated with fewer byte-identical candidates**, including at the first repair, while **verified-success advantage was not established**.

**What they do not support:**

1. Proof that the model understood, attended to, or used compiler-message content.
2. Proof that an edit or vanished unknown name repaired the underlying theorem.
3. A causal claim that diagnostics improve correctness, speed or token efficiency.
4. Equivalence of B and C from zero discordant outcomes.
5. Generalization to other models, random seeds, mathematical domains, or unlimited search.
6. Independent validation of English-to-Lean semantics or autonomous statement translation.

**Additional constraints:** related theorem families; a single local model and seed; B-before-C ordering; unequal realized diagnostic prompt lengths; very sparse verified success; two unavailable guided outcomes; post-hoc selection and unadjusted multiple contrasts; no independent human semantic labels; and privacy-limited public replay.

The **two unavailable C trajectories cannot be backfilled** under the no-replay freeze. One involved a prompt exceeding its context budget; the other has only a durable stream header and no generated candidate to verify. They are not transformed into failures or fabricated responses.

## Repository structure

The **publication directory is the source of truth for the 60-case reviewed fixed-theorem study**. The top-level preparation files and earlier reports document **historical** work under different tasks/settings; do **not** combine their prototype or hand-authored successes with the final model-run results.

| Path | Purpose |
|---|---|
| [publication/README.md](publication/README.md) | Published bundle overview and historical revision notes |
| [publication/paper/](publication/paper/) | Paper source, BibTeX references, generated tables/figures and **historical PDF snapshots** |
| [publication/dataset/](publication/dataset/) | Source-attributed 75-item dataset views |
| [publication/results/](publication/results/) | Held-out outcomes, pair/sensitivity summaries |
| [publication/evidence/](publication/evidence/) | Privacy-redacted evidence views |
| [publication/source_snapshot/](publication/source_snapshot/) | Archived scientific implementation |
| [publication/provenance/](publication/provenance/) | Dataset, protocol and model inventory commitments |
| [publication/third_party/](publication/third_party/) | Rights, attribution and license notices |
| [publication/docs/](publication/docs/) | Experiment, audit, submission-gate and reproducibility documentation |
| [publication/post_hoc/analysis/](publication/post_hoc/analysis/) | Post-hoc metric scripts and cluster bootstrap code |
| [publication/post_hoc/extensions/](publication/post_hoc/extensions/) | Separate development placebo implementation |
| [publication/post_hoc/outputs/post_hoc/](publication/post_hoc/outputs/post_hoc/) | Derived exploratory tables, CSVs, audit summaries |
| [RUN_REPORT.md](RUN_REPORT.md) | **Historical core-Lean hand-authored/partly simulated run**, **not** final-model evidence |
| [paper/](paper/) | Early manuscript artifacts, not the latest reviewed study |

**Latest anonymous manuscript:** [review-branch main.tex](https://github.com/sadiapeerzada/NLP-to-Formal-Language-Proof/blob/manuscript/exploratory-process-update-20261030/publication/paper/main.tex) and [MANUSCRIPT_CHANGES.md](https://github.com/sadiapeerzada/NLP-to-Formal-Language-Proof/blob/manuscript/exploratory-process-update-20261030/publication/post_hoc/outputs/post_hoc/MANUSCRIPT_CHANGES.md). The original paper and PDF files on the default branch **should not be represented as already rebuilt from the newer review source**.

## Reproduce and audit

### 1. Public aggregate reanalysis — no model calls

With Python 3 and a clone of this repository, run from the repository root:

    git clone https://github.com/sadiapeerzada/NLP-to-Formal-Language-Proof.git
    cd NLP-to-Formal-Language-Proof
    python3 publication/reanalyze.py

The [public reanalysis script](publication/reanalyze.py) uses the **Python standard library** to check disclosed 60-case outcome counts, complete-pair identities, recorded hashes and redacted evidence relationships. It does **not** reload the model, rerun Lean proofs, regenerate responses, or prove fidelity to withheld private original bytes.

### 2. Reproduce manuscript-specific exploratory counts

The [numbers CSV](publication/post_hoc/outputs/post_hoc/manuscript_update_numbers.csv) gives each new numerator/denominator, contrast, source CSV, bootstrap endpoints and code path. The [rerunnable analysis script](publication/post_hoc/analysis/manuscript_update_numbers.py) reads stored derived repair-level CSVs and calls the existing **NumPy** whole-family bootstrap routine. It invokes **no inference**.

**Never overwrite existing research outputs.** The script intentionally refuses to replace its destination CSV. Reproduce it only from a **disposable copy** of the post-hoc directory where the *copied* derived destination is absent. From that copied directory:

    python3 -m analysis.manuscript_update_numbers

For the full historical analysis workflows and prerequisites, read [post-hoc analysis instructions](publication/post_hoc/analysis/README.md). Original-byte prompt/token reconstruction requires privately retained inputs and the pinned tokenizer; public derivatives must **not** be treated as identical to withheld originals.

### 3. Historical exact-public-payload verification

The [payload verifier](publication/verify_payload.py) compares file membership and SHA-256 hashes against the original approved [public payload manifest](publication/PUBLIC_PAYLOAD_MANIFEST.json). It is **snapshot-specific**: more recent post-hoc outputs were added under publication/, so its exact-membership check can **fail on a newer checkout** despite unchanged historical files. Run it only on the **matching historical release**, not as an unqualified validation of this expanded checkout. Do **not** rewrite the frozen manifest to mask additions.

### 4. Manuscript build

The [LaTeX source](publication/paper/main.tex) uses Springer LNCS/CCIS, generated tables/figures and [BibTeX references](publication/paper/references.bib). [Build metadata](publication/paper/build_manifest.json) records the historical engine and input hashes.

The **updated review-branch source has not yet received a confirmed exact-repository LaTeX/BibTeX build**. A standalone review copy was built separately, but does not establish the repository manuscript's page count or submission compliance. In particular, **whether appendices are excluded from the venue page limit is unverified**. Review the new manuscript and compile its exact repository assets before submission.

## Manuscript status

**Title:** *Compiler-Guided Proof Repair in Lean 4: A Controlled Local-Model Pilot on Fixed Theorem Types*.

- **Format:** anonymous Springer LNCS / CCIS review copy.
- **Current edits:** [exploratory process manuscript branch](https://github.com/sadiapeerzada/NLP-to-Formal-Language-Proof/tree/manuscript/exploratory-process-update-20261030), distinct from the default branch.
- **Audit trail:** [manuscript change log](https://github.com/sadiapeerzada/NLP-to-Formal-Language-Proof/blob/manuscript/exploratory-process-update-20261030/publication/post_hoc/outputs/post_hoc/MANUSCRIPT_CHANGES.md).
- **Publication gate:** the [recorded review gate](publication/docs/FINAL_SUBMISSION_GATE.md) does **not** claim full original M1–M7 compliance or unconditional submission authorization.
- **Future research:** multiple seeds, other model sizes, independent human semantic review and further diagnostic-content controls would require separately approved studies. No additional held-out model execution is claimed; Study 2 remains deferred.

## Rights, attribution and provenance

Of 75 eligible pairs, **16** are textbook-derived and **59** are adaptations of pinned formal-library statements. Their attribution and applicable licenses are preserved separately. See [rights and attribution](publication/third_party/RIGHTS_AND_ATTRIBUTION.md), [dataset attribution](publication/dataset/ATTRIBUTION.json), and [public reproducibility/privacy boundary](publication/post_hoc/PUBLIC_REPRODUCIBILITY_BOUNDARY.md).

Publication or access to this repository does **not** imply blanket relicensing, unverified publisher permission, independent human approval, or release of the private original prompts/host identifiers. The research freeze is an **internal commitment**, not external preregistration.

---

**Takeaway:** Compiler-guided repair in this low-resource, fixed-theorem Lean 4 pilot was **associated with fewer exact-copy retries**, a **suggestive exploratory pattern**, but the recorded study **does not establish a robust increase in verified proofs or demonstrate diagnostic-content use**.

# Dataset curation and freeze plan

**Status:** proposed workflow; no new problem records reviewed or admitted.  
**Prepared:** 21 October 2026  
**Acceptance target:** at least 60 eligible, independent held-out test
problems and 15–20 eligible development problems, with mathematical families
kept within one split.

This plan is supplementary to the existing curation guide and audit. It does
not change the current draft, manifest, ledger, or any experiment artifact.
Nothing here certifies dataset eligibility, source rights, statement
faithfulness, or an independent review.

## 1. Read-only repository audit

The revision baseline in `docs/implementation_plan.md` identifies the major
revision report dated 20 October 2026. No separate professor-report file was
located in the repository during this audit; requirements below follow that
recorded baseline and the requested dataset target.

The existing draft has 21 records, five observed categories, difficulty
values 1–4, and a proposed 15/6 development/test split. Its exact-byte
SHA-256 is
`fec50bc77cb2782edba29ce08b680c63eb145092868853b3fc5efb947f025514`.
The manifest declares `draft`, `not_frozen: true`, and zero eligible records.
All source and license review statuses are pending, all semantic-fidelity
labels are null, and family and split decisions remain proposals. The
`arith_003` / `arith_003_mathlib` exact-English duplicate group is unresolved.
The proposed split therefore does not count as a test set.

The legacy record shape requires `id`, `nl_statement`, `category`,
`difficulty`, and `expected_lean_statement`; the legacy validator permits any
non-empty category and constrains difficulty to integer 1–5. The nested
curation object additionally records source and license status, family and
split, semantic-fidelity review, theorem-statement review,
assumption-mismatch review, self-containment review, and duplicate review.
The curation guide requires reviewer provenance and evidence for completed
reviews. The eligibility helper checks these recorded values, including
family-level completion and duplicate adjudication, but a non-empty reviewer
provenance string is enough: it does **not** establish that the reviewer was
independent.

Other limits of current tooling:

- Exact duplicate detection normalizes English text; it cannot find
  paraphrases or mathematical equivalence.
- Family checks only enforce one split per identical family label. They cannot
  verify that the labels describe the actual theorem families.
- Structural draft validation reports eligible IDs but does not enforce the
  minimum split sizes or a frozen/unfrozen state.
- Strict research-manifest validation checks required fields, IDs, and
  exact-byte dataset SHA-256. It does not enforce the 60/15 counts or by itself
  establish that test data was kept out of prompt tuning.
- The manifest's hash identifies the exact JSON bytes. It is not a signature,
  source-rights check, or review certification.

No records or decisions should be promoted solely because a validator accepts
their structure.

## 2. Candidate sources to investigate

These are research leads, not approved sources or license determinations for
individual problems. Repository-level licenses below were checked against the
repositories' `LICENSE` files on 21 October 2026. Before copying any item,
review its original source and the rights to that particular text separately.

| Candidate | Dataset fit and attribution lead | Repository license evidence | Limitation before reuse |
|---|---|---|---|
| [ProofNet](https://github.com/zhangir-azerbayev/ProofNet) | The README describes 371 undergraduate mathematics examples with natural-language statements, Lean 3 theorem statements, and natural-language proofs. It cites Azerbayev et al., *ProofNet: Autoformalizing and Formally Proving Undergraduate-Level Mathematics* (2023), [arXiv:2302.12433](https://arxiv.org/abs/2302.12433). | The repository's [LICENSE](https://github.com/zhangir-azerbayev/ProofNet/blob/main/LICENSE) is MIT and states the copyright notice must accompany copies/substantial portions. | The README says items are primarily drawn from undergraduate textbooks and points to a Hugging Face dataset. The repository MIT license does not by itself resolve rights in each textbook-derived statement. It is Lean 3; a Lean 4 port/revalidation is needed. Verify the specific source and redistribution rights for every retained item. |
| [Google DeepMind miniF2F](https://github.com/google-deepmind/miniF2F) | The README describes Lean 4 translations and natural-language docstrings, citing *MiniF2F: a cross-system benchmark for formal olympiad-level mathematics*, [arXiv:2109.00110](https://arxiv.org/abs/2109.00110). It identifies AoPS contest-collection archives and the Hendrycks MATH dataset among likely sources of descriptions. | The repository's [LICENSE](https://github.com/google-deepmind/miniF2F/blob/main/LICENSE) is Apache-2.0. | The README itself says descriptions are from “best estimates” and source material can come from other collections. Trace each item to its original source and verify underlying rights and attribution before redistribution. The Lean 4 format is useful, but does not replace statement, import, or semantic review. |

The candidate repositories' licenses are not blanket proof that their
upstream textbook, contest, or benchmark text can be redistributed under the
same license. The licensing reviewer must capture the applicable source
license/rights evidence per record and decide the allowed use. If that cannot
be established, exclude the candidate from the released dataset; do not fill
in an assumed license.

## 3. Versioned record schema and eligibility

Keep the existing required top-level fields for compatibility:

- `id`: stable unique ID.
- `nl_statement`: exact natural-language input used for the task.
- `category`: one controlled primary category.
- `difficulty`: integer 1–5, assigned using the rubric below.
- `expected_lean_statement`: reference theorem only; do not use it as an
  implicit prompt-tuning aid for held-out items.

For the next dataset version, retain the existing `curation` fields and add
evidence fields rather than overloading status strings:

- source dataset/repository, immutable commit or release, source record ID,
  original bibliographic source, and retrieval date;
- exact license/rights text, license URL or source evidence citation,
  evidence capture date, and redistribution decision;
- reference theorem origin, authoring/edit history, Lean version, Mathlib
  revision, imports/local definitions, and a reference-file SHA-256;
- reviewer identity/provenance, role, review date, and review evidence for
  statement meaning, assumptions, self-containment, semantic fidelity,
  duplicate/family, and split decisions;
- duplicate/family group IDs, related record IDs, and decision rationale.

Do not alter the current schema silently: version any schema expansion and
update its validator and tests first. Do not record private reviewer details
in public data without consent; use stable, auditable reviewer IDs where
appropriate, retaining the identity mapping under controlled access.

A record counts toward the target only when all of the following are
documented and accepted:

1. Stable primary source or verified author-created provenance; exact
   attribution and source revision.
2. Rights/license evidence permitting the intended storage, redistribution,
   and publication use of the included wording and derived Lean statement.
3. A complete reference theorem that compiles in the pinned project with
   required imports and definitions recorded; no missing names or hidden
   local context.
4. Independent comparison of complete English and Lean meanings: quantifiers,
   types, notation, assumptions, coercions, domain boundaries, and edge cases.
   Record one of `faithful`, `not faithful`, or `uncertain`; uncertain is
   recorded honestly and not recoded as faithful.
5. Separate evidenced checks for theorem-statement match, assumption
   mismatch, and self-containment.
6. Exact duplicate resolution and human review for likely paraphrase or
   mathematically related theorems. A duplicate group contributes at most one
   independent example unless a reviewed distinction justifies otherwise.
7. Reviewed family membership and split assignment, with every family wholly
   in one split.
8. Complete reviewer provenance and evidence. An author self-review is not an
   independent review and cannot satisfy an independence requirement.

The curation validator now checks for these declared evidence fields,
controlled category/difficulty values, statement-hash-matched theorem
verification, and independent-human review records for each required review
dimension. It does not authenticate sources, reviewers, review events, or
Lean execution, so retain the cited evidence and independent sign-offs; a
passing validator is not itself a content or identity audit.

Verified source/license evidence must include `statement_sha256` computed
from the exact `expected_lean_statement` UTF-8 bytes without normalization.
The freeze validator compares `expected_ids` with the exact ordered IDs in
each file and requires an independent-human `likely_duplicate_dispositions`
record for every heuristically flagged pair. Dispositions record
lexicographically ordered `problem_ids`, a `duplicate` or `not_duplicate`
decision, reviewer identity/kind, date, and evidence. Similarity never
establishes the decision; a `duplicate` disposition blocks freezing until
one item is removed or excluded and the dataset hashes are recomputed.

## 4. Categories, difficulty, and family separation

Retain the five observed primary categories where appropriate:
`arithmetic_identity`, `divisibility`, `modular_arithmetic`, `induction`, and
`inequality`. Add a category only when a candidate needs it, define it in the
versioned schema, and use one primary label plus optional controlled tags if
cross-cutting concepts need representation. Do not assign category based on
the theorem's ID prefix alone.

Use a written, calibrated rubric for the existing 1–5 difficulty field.
Proposed operational scale (difficulty of the Lean proof obligation, not
model success probability):

1. Direct definitional, normalization, or single standard tactic proof.
2. One routine lemma or short algebraic transformation.
3. Several routine steps or a small structured case split.
4. Induction or a nontrivial case split with multiple supporting steps.
5. Multiple substantial lemmas, nested structure, or substantial domain
   reasoning.

Reviewers should pilot this rubric on a small development-only sample, discuss
disagreements, then freeze rubric wording before assigning final labels.
Record disagreement rather than tuning labels to produce balanced bins.

Define `problem_family` by the underlying mathematical proposition/theorem
family, not wording, source, tactic, or theorem name. Near-duplicates and
specializations/generalizations should be conservatively grouped when
exposure of one could reveal the solution strategy for another. Review
families before assigning splits. Split the family as a unit; if uncertain,
keep it in development or exclude it from the held-out set.

## 5. Curation stages and held-out protection

1. **Source discovery:** create a candidate ledger separate from the frozen
   dataset. Record exact source revisions, candidate IDs, and rights-check
   status. Do not copy records with unresolved provenance into a release file.
2. **Rights triage:** check repository license plus each upstream source's
   terms. Exclude candidates with unclear redistribution rights unless
   institutional review resolves the issue.
3. **Normalization and theorem validation:** preserve original wording,
   record any transcription/translation, review the reference Lean statement,
   and compile under the single pinned Lean/Mathlib environment.
4. **Deduplication and family review:** run exact-text detection as a lead,
   manually review mathematical similarity, adjudicate groups, then assign
   whole families to a proposed split.
5. **Independent review:** use reviewers other than the author for semantic,
   theorem-statement, assumption, family, and split checks. Capture evidence
   and disagreements. An author may curate and adjudicate but must not be
   mislabeled as an independent reviewer.
6. **Development set:** approve 15–20 eligible records in its own file and
   manifest. Use only development items for prompt development, rubric
   calibration, and workflow debugging.
7. **Held-out test set:** select at least 60 eligible problems by family from
   sources/families not used in development. Keep statements, reference
   theorems, labels, and answer keys access-controlled. Do not inspect test
   examples to tune prompts, models, or settings. Freeze the test ID list and
   hash only after protocol and prompts are locked. A custodian not involved
   in tuning should release test inputs once for the preregistered evaluation.
8. **Post-freeze changes:** never edit a frozen test file in place. Corrections
   require a new version, a documented change log, regenerated hash, and
   explicit approval; keep the previous frozen artifact.

The validator checks a declared test-access policy but does not technically
prevent test-set access or prompt tuning. Enforce the boundary operationally
with separate development/test files, access controls, a test custodian, and
recorded protocol/prompt hashes.

## 6. Candidate collection estimate

The existing pool has zero eligible items, so its observed yield is not a
useful estimate of future curation attrition. Plan with an explicit
assumption, then update it from actual reviewed candidates. For a conservative
initial planning target, assume **50%** of unique candidate problems survive
rights, duplicate/family, theorem, and semantic review:

| Desired eligible set | At 40% yield | At 50% yield | At 60% yield |
|---|---:|---:|---:|
| 60 held-out test problems | 150 candidates | 120 candidates | 100 candidates |
| 15 development problems | 38 candidates | 30 candidates | 25 candidates |
| 20 development problems | 50 candidates | 40 candidates | 34 candidates |

These are `ceil(target / assumed_yield)` planning calculations, not evidence
about actual source quality or approval rates. Start by sourcing approximately
120 unique test-family candidates and 30–40 development candidates if the
50% planning assumption is used. Increase collection if candidate families
cluster, duplicate groups collapse, or license/review exclusions lower yield.
Count only unique eligible problems after all exclusions; do not split a
family just to meet the number.

## 7. Validation and freeze procedure

Current draft checks and frozen validation:

```bash
.venv/bin/python src/dataset_validation.py --validate-curation-draft \
  data/research_dataset_draft_v0.1.0.json
.venv/bin/python -m pytest -q tests/test_dataset_validation.py
```

For a future versioned candidate file, first run the draft validator and
review every error and duplicate/family review-queue warning. Candidate and
eligible counts are reported separately by split. Independently verify
reviewer sign-offs and source, license, semantic, theorem, and execution
evidence. Do not call those records frozen.

Only after eligibility, independence, licensing, split counts, and protocol
checks pass:

1. Write new, versioned development and test JSON arrays; never replace the
   current draft or existing run artifacts.
2. Compute exact-byte hashes with `shasum -a 256` (and independently with
   `sha256sum` or Python `hashlib`); record ordered IDs, counts by split,
   category, difficulty and family, and source/rights evidence references.
3. Create separate development and test JSON arrays with strict manifests
   containing `dataset_version`, the exact ordered IDs, and exact-byte hashes.
   Keep the test file and answer key inaccessible to the tuning team.
4. Create one freeze manifest with separate `development_dataset` and
   `test_dataset` sections. Validate both separate files together using the
   new frozen-curation command below. Independently recompute hashes and
   compare ordered IDs, family-level split assignments, reviewer sign-offs,
   and thresholds: at least 60 test and 15–20 development records.
5. Mark a new manifest frozen only after the custodial/access-control and
   human approval steps are documented. Preserve the draft and all prior
   versions unchanged.

Current draft validation result (21 October 2026): 21 structurally valid
records, one exact-English duplicate-candidate group, zero eligible records,
and zero validation errors. It remains a draft and is not an evaluation set.

## Validator support added (21 October 2026)

`src/dataset_validation.py --validate-curation-draft` now prints candidate
counts separately from eligible counts and emits a review queue. Eligibility
requires category/difficulty validity, verified license evidence, a
successful Lean theorem-verification record whose hash matches the exact
reference statement, and independent-human review records for semantic
fidelity, theorem statement, assumption mismatch, self-containment, family,
split assignment, and duplicate review. Self-review and assisted-review
records remain distinguishable and do not satisfy those independent review
requirements. The exact text similarity queue is a warning aid only; it is
not a duplicate adjudicator.

An explicitly separate `--validate-frozen-curation --freeze-manifest ...`
mode requires `status: frozen`, explicit approval, 60 or more eligible test
records, 15–20 eligible development records, exact matching IDs and
dataset-byte SHA-256, count agreement, dataset author IDs for cross-checking
reviewer IDs, an ISO `frozen_on` date and `freeze_approval_evidence`, exact
ordered IDs, a `likely_duplicate_dispositions` entry for every flagged pair,
a locked protocol hash, and a test access/tuning policy. The
command accepts separate development and test JSON files. The existing
versioned draft and manifest remain unchanged, and the current 21-record
draft remains at zero eligible records.

```bash
.venv/bin/python src/dataset_validation.py --validate-frozen-curation \
  --freeze-manifest data/research_dataset_manifest_vX.json \
  --development-dataset data/research_dataset_dev_vX.json \
  data/research_dataset_test_vX.json
```

The code enforces recorded fields, counts, hashes, family/split consistency,
and the policy declaration. It cannot authenticate reviewer identity or
independence, independently reproduce an undocumented review, restrict
filesystem access, or prevent held-out data/results from being used outside
the validator. Those require documented human sign-off and a separate
test-set custodian/access procedure. These tools do not upgrade the current
draft to a frozen dataset or make it available for experiments.

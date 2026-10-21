# Research dataset curation guide

The versioned research dataset is a review draft, not an experiment-ready or
frozen dataset. Keep the seed file unchanged. Record every decision in the
corresponding record's `curation` object and its entry in the versioned
curation ledger. Do not infer missing evidence. Use `pending` while work has
not begun, `needs_review` when evidence or a decision is unresolved, `verified`
only after documenting the review, and `rejected` when a candidate is
explicitly excluded.

## Source and license

For each record, identify the actual source of the English problem and
reference Lean statement. Record a source URL or a precise bibliographic
citation only after checking that it identifies the relevant material.
Separately inspect the source's rights or license statement and record its
exact license wording and verification status. A page being publicly
accessible is not evidence that its contents may be redistributed. If the
source or rights cannot be verified, leave the value null and status `pending`
or `needs_review`; do not create a citation or license from memory.

## Theorem statement, assumptions, and self-containment

Have a Lean/math reviewer compare the complete English claim with the complete
Lean declaration, including quantifiers, types, hypotheses, coercions,
notation, imports, and boundary cases. Check that assumptions stated in the
English are represented in Lean and that Lean does not establish a materially
different or stronger claim. Record theorem-statement and
assumption-mismatch review independently.

Check whether the declaration can be understood from the project environment:
all referenced names and definitions must be available through documented
imports or an explicitly included local definition. Record unresolved names
such as `geomSum` as `needs_review`; do not treat a name's apparent meaning as
a definition.

For every `verified` review, record reviewer provenance and concise evidence in
the corresponding review object. If an issue cannot be resolved, use
`needs_review` or `rejected`; do not force a positive certification.

For eligibility-sensitive review, also add a `curation.review_records` entry
with `review_type`, `reviewer_kind`, `reviewer_id`, ISO `reviewed_on`, and
evidence. Use `author_self_review`, `assisted_review`, or
`independent_human_review` explicitly. Only the last kind can satisfy the
required independent checks. At freeze validation, reviewer IDs are compared
with `dataset_author_ids`; an ID listed as an author cannot qualify as
independent. Do not infer independence from a non-empty name/provenance field.
The validator checks recorded declarations, not personal identity, conflicts,
or the actual occurrence of a review; retain reviewer sign-off evidence.

Record source/license evidence separately as
`curation.source_license_evidence` with `status: "verified"`,
`evidence_reference`, `reviewed_on`, and `statement_sha256`. Compute
`statement_sha256` from the exact `expected_lean_statement` string encoded as
UTF-8; do not trim, normalize, or alter line endings. Record successful
reference theorem verification in `curation.theorem_verification`, including
`success: true`, the pinned Lean toolchain, Mathlib revision, command,
evidence, and a SHA-256 of the same exact statement string. A Lean success is
only theorem verification evidence; it does not establish English/Lean
semantic faithfulness.

For family and split decisions, the current record shape stores the decision
status separately from its evidence. When either status is `verified`, populate
`family_reviewer_provenance` and `family_review_note`, or
`split_reviewer_provenance` and `split_review_note`, respectively. The
validator requires these fields before including a record in its eligible-ID
result. A pending semantic-fidelity review must have a null `label`; a
completed review requires a label, reviewer provenance, and evidence.

## Families, duplicates, and splits

Use `problem_family` for the underlying mathematical theorem family, not just
shared vocabulary. Similarity is a lead for human comparison, not proof that
two records are equivalent. Record the rationale and reviewer decision in the
ledger. Keep every accepted family wholly within one split. The deterministic
split map in the draft builder is a proposal only; a human curator must review
both family membership and split assignment before freezing.

The validator flags normalized exact-English duplicate candidates. Review
their Lean statements and provenance, then explicitly resolve each
`duplicate_review`. Count an adjudicated duplicate group as at most one
independent example unless a documented distinction justifies otherwise.
Near-duplicates and related theorems also require manual family/leakage review;
the exact-text detector cannot establish semantic equivalence or find all
related statements. The curation validator now emits a string-similarity
review queue for likely English or Lean statement duplicates; this is only a
heuristic and must be manually adjudicated, including false-positive
disposition. Before freeze, record one `likely_duplicate_dispositions` entry
for every flagged pair across both files. Each entry must contain the two
lexicographically ordered `problem_ids`, `decision` (`duplicate` or
`not_duplicate`), `reviewer_kind: "independent_human_review"`, `reviewer_id`,
ISO `reviewed_on`, and non-empty `evidence`. A `not_duplicate` decision must
explain the human distinction and can satisfy the review gate. A `duplicate`
decision blocks freezing until one item is removed or excluded and the files
and hashes are recomputed. Similarity never supplies the decision. Keep the
reviewer's rationale in the curation record/ledger as well as the freeze
manifest so the adjudication remains auditable.

## Semantic fidelity

Use only `faithful`, `not faithful`, or `uncertain` as a reviewed label.
`uncertain` is a legitimate outcome when the evidence does not support a
binary judgment. Leave `label` null while review is pending. Record reviewer
provenance and evidence for a completed review; do not derive a fidelity label
from successful compilation alone.

## Eligibility and freezing

Run the curation draft validator after edits:

```text
.venv/bin/python src/dataset_validation.py --validate-curation-draft \
  data/research_dataset_draft_v0.1.0.json
```

A successful draft validation checks record shape, statuses, IDs, approved
category/difficulty, declared source/license evidence, theorem-verification
metadata and statement hash, required independent-human review records,
duplicate candidates, and family/split consistency. It cannot authenticate
the sources, rights, reviewers, reviews, or actual Lean execution; nor can
compilation establish semantic fidelity. Its eligible-ID result is
conservative: missing evidence makes a record ineligible, exact-English
duplicate candidates must share complete group metadata, and an unresolved
candidate group contributes no eligible item (a reviewed exact-duplicate
group contributes at most one). Candidate and eligible counts are reported
separately. Eligibility is a curation accounting check, not proof of
mathematical or licensing correctness.
Do not mark the dataset frozen or use it for primary experiments until those
reviews are complete and the target held-out count is met: at least 60
eligible test records and 15–20 eligible development records, with theorem
families kept together. The current 21 seed records (including a duplicate
candidate pair) are insufficient for that target.

### Freeze and held-out boundary

Keep development and test data in separate versioned files. Use development
items only for prompt, model, and repair-policy tuning. Before opening the
held-out test file, lock the prompts/configuration and hash the protocol.
Restrict test access to a custodian who does not tune the system; release the
test data only for the preregistered evaluation and preserve an access log.
Never feed test results back into tuning. These access and non-use controls
are procedural; the validator can check manifest declarations but cannot
enforce actual file access or prevent out-of-band tuning.

After all reviews and independent counts pass, create separate versioned
development and test JSON files and a manifest containing `status: "frozen"`,
`freeze_approved: true`, an ISO `frozen_on` date,
`freeze_approval_evidence`, and `development_dataset` and `test_dataset` sections
(each with ordered `expected_ids` and exact-byte `dataset_sha256`), candidate
and eligible counts by split, `dataset_author_ids`,
`likely_duplicate_dispositions`,
`locked_protocol_sha256`, and `test_access_policy`. Validate both files
together with:

```text
.venv/bin/python src/dataset_validation.py --validate-frozen-curation \
  --freeze-manifest data/research_dataset_manifest_vX.json \
  --development-dataset data/research_dataset_dev_vX.json \
  data/research_dataset_test_vX.json
```

Freeze validation enforces at least 60 eligible test records and 15–20
eligible development records and verifies the dataset hash, IDs, counts,
review evidence declarations, exact ID order, duplicate dispositions, and
family/split consistency. It rejects a draft/unfrozen manifest. Independently
recompute the exact-byte hash and review the evidence and access log before
approval.

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
related statements.

## Semantic fidelity

Use only `faithful`, `not faithful`, or `uncertain` as a reviewed label.
`uncertain` is a legitimate outcome when the evidence does not support a
binary judgment. Leave `label` null while review is pending. Record reviewer
provenance and evidence for a completed review; do not derive a fidelity label
from successful compilation alone.

## Eligibility and freezing

Run the structural draft validator after edits:

```text
python src/dataset_validation.py --validate-curation-draft \
  data/research_dataset_draft_v0.1.0.json
```

A successful structural validation checks shape, statuses, IDs, duplicate
candidates, and family/split consistency only. It does not verify sources,
licenses, theorem correctness, semantic fidelity, or the proposed splits.
Its eligible-ID result is conservative: verified fields without their
documented evidence are not eligible, exact-English duplicate candidates must
share complete group metadata, and an unresolved candidate group contributes
no eligible item (a reviewed exact-duplicate group contributes at most one).
Eligibility is a curation accounting check, not a proof of mathematical or
licensing correctness.
Do not mark the dataset frozen or use it for primary experiments until those
reviews are complete and the target held-out count is met: at least 60
eligible test records and 15 development records, with theorem families kept
together. The current 21 seed records (including a duplicate candidate pair)
are insufficient for that target.

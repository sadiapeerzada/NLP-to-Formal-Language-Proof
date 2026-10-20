# Research dataset curation audit v0.1.1

**Status: draft audit; dataset not frozen and not eligible for experiments.**

This audit records repository evidence for the 21-record draft at
[`research_dataset_draft_v0.1.0.json`](./research_dataset_draft_v0.1.0.json),
using the rules in [`schema.md`](./schema.md), [`curation_guide.md`](./curation_guide.md),
and [`curation_ledger_v0.1.0.json`](./curation_ledger_v0.1.0.json). It does
not certify sources, rights, mathematical correctness, compilation, or
English/Lean semantic equivalence. No external source research or Lean
compilation was performed for this audit.

## Inventory and current status

The draft and manifest list 21 records with 21 unique IDs and five categories.
The current manifest's exact-byte draft SHA-256 is
`fec50bc77cb2782edba29ce08b680c63eb145092868853b3fc5efb947f025514`.
The draft retains the original seed records; no candidate has been removed.
The manifest reports 0 eligible records, with 0 eligible in either proposed
split. The split map contains 15 development and 6 test candidates, but all
split reviews are pending. Excluding one member of the exact-English duplicate
pair gives a maximum of 20 independent candidates if that pair is adjudicated
as one problem; this is only an arithmetic upper bound, not an eligibility
finding.

The source URL, citation, and license values are null for every record. The
source and license-verification statuses are `pending` for all 21. The
theorem-statement, assumption-mismatch, self-containment, and semantic-fidelity
reviews are also pending for every record; no fidelity label is asserted. The
family and split assignments are proposals, not verified human decisions.

| ID | Proposed family | Proposed split | Record-specific audit lead (not a verdict) |
|---|---|---|---|
| `arith_001` | `nat_square_identities` | development | Compare the universal natural-number identity with the English claim; provenance and meaning remain unreviewed. |
| `arith_002` | `nat_square_identities` | development | Lean condition `b ≤ a` corresponds to the English condition; natural subtraction semantics need review. |
| `div_001` | `nat_square_identities` | development | Check `Even`, its import/context, and the English-to-Lean correspondence. |
| `div_002` | `nat_parity_products` | test | Review product ordering and whether `Even` expresses the stated parity claim. |
| `div_003` | `nat_divisibility_factorization` | test | Review divisibility conventions and the conjunction corresponding to “both.” |
| `mod_001` | `integer_congruence_translation` | test | English says `m` is positive; the recorded Lean statement has no positivity hypothesis. Resolve the possible assumption mismatch. |
| `mod_002` | `square_residue_classes` | test | Review remainder/congruence convention for negative integers and modulo 4. |
| `ind_001` | `nat_finite_sum_identities` | development | Review the range endpoint, doubled-sum identity, quotient, and indexing convention. |
| `ind_002` | `nat_finite_sum_identities` | development | “First n odd numbers” depends on indexing; Lean uses `range n` and terms `2*i+1`. |
| `ind_003` | `nat_power_growth` | development | Review the inequality, theorem assumptions, and boundary case. |
| `div_004` | `nat_parity_products` | test | Review the odd-number witness encoding and its correspondence to ordinary oddness. |
| `ineq_001` | `nat_square_identities` | development | Review the universal claim at `n = 0` and compare against the Lean statement. |
| `arith_003` | `nat_distributivity` | development | Exact-English duplicate candidate `arith_003_mathlib`; adjudicate the pair before counting. |
| `arith_003_mathlib` | `nat_distributivity` | development | Exact-English duplicate candidate `arith_003`; determine whether any documented formulation distinction exists. |
| `arith_004` | `nat_square_identities` | development | Review natural-number truncated subtraction and whether `b ≤ a` is sufficient. |
| `div_005` | `nat_square_identities` | development | Review the existential witness encoding of oddness and required definitions/imports. |
| `div_006` | `nat_square_identities` | development | Review both directions of the even-square equivalence, witness encodings, and boundary cases. |
| `ineq_002` | `nat_product_bound` | development | Review the “at most” translation, expanded product, and boundary cases. |
| `ineq_003` | `nat_power_growth` | development | Review `n ≥ 1`, the bound, and the smallest permitted case. |
| `ind_004` | `nat_finite_sum_identities` | development | Lean refers to `geomSum n`; the dataset record does not define it. Self-containment is unestablished. |
| `mod_003` | `square_residue_classes` | test | Review the modulo-3 remainder formulation and its relation to the English statement. |

The record-specific leads above reproduce the pending findings and actions in
the ledger; they are not independent mathematical certifications.

## Provenance and licensing

**Verified in repository:** for all 21 draft records, `curation.source_url`,
`curation.source_citation`, and `curation.source_license` are null, while
`source_status` and `source_license_verification_status` are `pending`.
The ledger records that this offline pass added no source or license evidence.

**Not verified:** no primary source, citation, rights statement, redistribution
permission, or source-specific license is established for any candidate.
Accordingly, every record still needs source identification and rights/license
review. Do not interpret an accessible page, if later found, as permission to
redistribute its text.

## Duplicate and family review leads

- **Exact-English duplicate candidate (observed):** `arith_003` and
  `arith_003_mathlib` have identical English statements in the draft and are
  listed together by the manifest as `exact_english_duplicate_arith_003`.
  Their Lean declaration names differ. They must not count as two independent
  examples absent a documented, human-reviewed distinction. Their
  mathematical equivalence or any environment-specific distinction remains
  unadjudicated.
- **Potentially related families (hypotheses only):** the proposed family IDs
  group square identities/parity (`arith_001`, `arith_002`, `arith_004`,
  `div_001`, `div_005`, `div_006`, `ineq_001`); finite sums (`ind_001`,
  `ind_002`, `ind_004`); power growth (`ind_003`, `ineq_003`); parity results
  (`div_002`, `div_004`); and square-residue statements (`mod_002`,
  `mod_003`). These share apparent mathematical themes, but the groupings are
  not established as theorem-family equivalence by string similarity or this
  audit. Every family assignment, including singleton families, remains
  `needs_review`.
- **Leakage risk:** the proposed `nat_distributivity` family places the exact
  English duplicate pair together in development, which avoids a cross-split
  leak if the family decision is upheld. The `square_residue_classes`,
  `nat_square_identities`, `nat_finite_sum_identities`, and
  `nat_power_growth` memberships require human review before the split can be
  considered family-safe. The current validator checks split consistency for
  records sharing a family ID; it cannot determine whether the family labels
  themselves are mathematically correct.

## Validator and ledger safeguard review

The committed ledger contains 19 family-proposal rows but only 9 distinct
family identifiers. Repeated rows arose from separate member rationales; the
validator checks each record's `curation.problem_family` and `curation.split`,
not those ledger rows, so the repetition alone did not create a validation
conflict. It was nevertheless ambiguous to maintain. The builder now
consolidates generated proposals to one deterministic row per family and
raises an error if members of one family are assigned different splits.

The validator also previously decided eligibility per record: a fully reviewed
member could be counted while another member with the same family ID still
had a pending family/split review. Eligibility is now conservative at the
family-group level: every member must have completed, evidenced family and
split reviews, or none of that family is counted. This does not approve any
current family assignment, and the existing draft, ledger, and manifest were
not regenerated or altered.

## Split proposal and target gap

The manifest proposes 15 development and 6 test candidates. These are
unreviewed assignments. Since both exact-English duplicates are currently
placed in development, counting that pair at most once yields at most 14
independent development candidates and 6 test candidates. The minimum
research target is 15 reviewed development and 60 reviewed held-out test
records. Thus the proposed candidate pool is short by at least 1 development
and 54 test candidates even under the optimistic one-per-duplicate-group
count. At the current validator eligibility count of zero, the eligible-count
shortfall is 15 development and 60 test records. These counts do not authorize
splitting related family members across sets or manufacturing records.

## Structural validation is not research eligibility

The validator can check record shape, allowed status/label values, unique IDs,
duplicate-candidate metadata, and family-to-split consistency. Passing those
checks does not establish source authenticity, redistribution rights,
mathematical correctness, self-containment in a pinned Lean environment, or
semantic fidelity. The manifest is explicitly a draft, reports no eligible
records, and is not a freeze artifact. The exact manifest hash describes the
existing draft bytes; it is not evidence that the dataset is complete or
approved.

## Evidence required before any record can be eligible

For each candidate, retain evidence and reviewer provenance for each item:

- [ ] Identify the original source or document verified hand-authored
  provenance; record an accurate URL or bibliographic citation.
- [ ] Inspect and record the applicable license/rights evidence and verify
  redistribution and publication use; do not infer permission from access.
- [ ] Have a qualified reviewer compare the full English claim and Lean
  statement, including types, quantifiers, assumptions, notation, and boundary
  cases; record a fidelity label (`faithful`, `not faithful`, or `uncertain`)
  with evidence. `uncertain` is valid and must not be coerced to a positive
  label.
- [ ] Independently review theorem-statement wording and assumption mismatch.
- [ ] Verify definitions, imports, notation, and self-containment in the
  intended pinned environment; record the environment and evidence. No
  compilation is claimed by this audit.
- [ ] Adjudicate exact and likely mathematical duplicates, with group metadata
  and a documented distinction if multiple records are to count independently.
- [ ] Review family membership and split together, with reviewer provenance;
  place each accepted family wholly within one split.

## Freeze checklist

- [ ] All included records have verified source and rights/license evidence.
- [ ] Theorem statement, assumptions, self-containment, and semantic-fidelity
  reviews are complete and evidenced; unresolved cases remain excluded or
  explicitly uncertain under the approved protocol.
- [ ] Exact duplicates and likely mathematical duplicates are adjudicated;
  family groupings and their evidence are reviewed.
- [ ] The family-aware development/test split is reviewed, deterministic, and
  has no family leakage.
- [ ] The minimum of 15 development and 60 independent held-out test records
  is met after exclusions; duplicate candidates do not inflate the count.
- [ ] A reproducible manifest is generated from the reviewed dataset, its
  exact-byte SHA-256 is independently checked, and all counts agree.
- [ ] The version is explicitly approved for freezing only after all above
  checks are complete.

**Results disclaimer:** this audit claims no research experiment results and
no theorem compilation results.

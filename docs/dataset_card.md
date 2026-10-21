# NL2Lean Research Dataset Card

## Status and intended use

Dataset construction is in progress. This repository does not currently
contain a released or frozen research dataset. The inventory contains 31
candidate records and zero eligible records. Do not use the candidate pool as
a held-out benchmark or report metrics on its proposed test labels.

The target is at least 60 eligible held-out test problems and 15–20 separate
eligible development problems, spanning at least five meaningful categories
with no mathematical-family leakage. The planned use is evaluation of Lean
proof repair and, separately, human-reviewed natural-language-to-Lean
faithfulness.

## Current candidate inventory

- 21 baseline draft candidates and 10 candidates in acquisition batches.
- Proposed split counts: 23 development and 8 test; these are not frozen
  split counts.
- Category counts: divisibility 11, arithmetic identity 6, induction 6,
  inequality 4, modular arithmetic 4.
- Difficulty counts: level 1: 10; level 2: 12; level 3: 7; level 4: 2.
- The construction inventory records 10 Lean-verified candidates, zero
  completed independent human-review records, and zero eligible records.
- Ten candidates carry item-level citations to Oscar Levin's
  *Discrete Mathematics: An Open Introduction*; the remaining 21 baseline
  records have no item-level citation in their current records.

The source identifies a CC BY-SA 4.0 license. Independent rights and
redistribution review remains incomplete, and the exact source text/page bytes
and source-page hashes have not been archived for the latest batch. This card
does not clear any record for reuse or publication. See
[`data/source_acquisition_ledger_v0.1.0.json`](../data/source_acquisition_ledger_v0.1.0.json)
and `data/curation_batches/` for provenance status.

## Eligibility, splits, and review

The strict curation validator requires source and rights evidence; exact-byte
statement provenance; pinned-environment Lean verification; category and
difficulty; independent semantic, theorem, assumption, self-containment,
family, split, and duplicate reviews; and resolved family/similarity checks.
All current records remain ineligible. At least one exact-English duplicate
pair and additional similarity warnings remain unresolved. No human review is
inferred from repository inspection or successful compilation.

The required development and test sets must be frozen as separate files with
ordered IDs and exact SHA-256 hashes. The held-out test set must not be used
for prompt tuning, model selection, or debugging.

## Data format and reproduction

See `data/schema.md`, `data/curation_guide.md`, and
`src/dataset_validation.py` for the schema and checks. To inspect the current
draft without promoting any candidate:

```sh
PYTHONDONTWRITEBYTECODE=1 ./.venv/bin/python src/dataset_validation.py \
  data/research_dataset_draft_v0.1.0.json --validate-curation-draft
```

A successful structural validation is not evidence of semantic correctness,
rights clearance, or theorem compilation. Frozen validation cannot pass until
all curation gates are satisfied.

## Limitations

There are no eligible records, no frozen split, and no completed semantic
reviews. The proposed test set is far below the target. Consequently, there
are no dataset-level A/B/C results, and no statement about performance or
faithfulness can be made.

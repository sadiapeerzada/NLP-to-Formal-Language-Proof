# Curation audit v0.1.3 — 21 October 2026

This audit covers the 21-record baseline draft and source-backed batches v0.1.0–v0.1.7. It is a candidate inventory, not a freeze or independent review.

## Current counts

- Candidates: 35 total (21 baseline + 14 source-cited DMOI3 records).
- Proposed split: 27 development, 8 test; every assignment is still pending review.
- Categories: arithmetic identity 6, divisibility 11, induction 9, inequality 4, modular arithmetic 5.
- Difficulty: level 1: 10; level 2: 13; level 3: 9; level 4: 3.
- Lean evidence: 10 candidates have recorded strict theorem-proof verification. Four additional propositions (`mod_005`, `ind_007`–`ind_009`) have only statement-type elaboration checks using `sorry` placeholders; no proof was verified for them. Twenty-one baseline candidates lack pinned theorem-verification metadata.
- Independent human reviews complete: 0. Eligible development: 0. Eligible test: 0. Dataset remains unfrozen.
- Review packets for all 35 current candidates are under `data/review_packets/current_pool_v0.2.2/`.

## Source, license, and review blockers

Fourteen candidate records cite DMOI3; 21 baseline records lack item-level source citations. The metadata contains seven `verified` source/license-evidence field values, seven `needs_review`, and 21 missing/pending. No independent rights-clearance decision is recorded. Source webpage/PDF bytes and page hashes are absent for batches v0.1.6 and v0.1.7. A direct read-only `curl` capture on 2026-10-21 failed with DNS resolution error `Could not resolve host: discrete.openmathbooks.org`; no byte hash is available. Complete actual source attribution and rights review before redistribution or inclusion.

Every candidate still lacks the required independent semantic, theorem-statement, assumption-mismatch, self-containment, family, split, and duplicate reviews. For `mod_005` and `ind_007`–`ind_009`, the exact English-to-Lean mapping also needs review; Lean proposition elaboration is not semantic validation.

## Duplicate and family queue

The aggregate validator reports likely similarity for:

- `arith_003` / `arith_003_mathlib`
- `div_001` / `div_005`
- `mod_002` / `mod_003`

These require independent adjudication. The source exercise for the screened-out `ineq_005` lead duplicates `ineq_004`. Batch v0.1.7 separately records the geometric-sum exercise as an index-shifted `ind_004` duplicate, the handshake-count exercise as the existing triangular-number `ind_001` family, and the Pascal-row exercise as the exact `ind_005` item. These four screened-out source items remain in `screened_out_items.json`/the acquisition ledger for independent confirmation and are not counted as candidates.

The inventory separately flags a possible cross-split family relation between `mod_001` (test proposal) and `mod_004` (development proposal); the existing family labels have not been independently adjudicated. All proposed families and splits remain pending.

## Exact shortfall and next actions

The target is 15–20 eligible development and at least 60 eligible held-out test items. There are 0 eligible in either split. Although 27 development and 8 test candidates are proposed, none may enter a split without the required evidence. At least 52 additional test candidates would be needed even if all eight current test proposals later qualified; further acquisition is likely necessary.

1. Source and license: identify/source the 21 baseline items; independently review rights and attribution for the 14 DMOI3 records; capture and hash source pages for v0.1.6 and v0.1.7.
2. Lean: run and preserve pinned verifier evidence for the 21 baseline records; obtain actual proofs for the four statement-only checks if proof verification is part of the inclusion criterion.
3. Human review: complete the seven required independent review dimensions using the 35 packets; do not fill reviewer IDs/dates until actual reviews occur.
4. Duplicates/families: adjudicate the three validator similarity pairs, the four screened source items, and the `mod_001`/`mod_004` family/split concern.
5. Acquisition: add distinct, licensed, source-backed test candidates in batches; keep family assignments together and rerun aggregate validation after each batch.

Aggregate draft validation currently reports zero structural errors, 87 review/evidence warnings, one exact duplicate group, and zero eligible IDs. The detailed warning list and current hashes are retained in `data/research_dataset_inventory_v0.2.2.json`. No freeze or held-out evaluation was performed.

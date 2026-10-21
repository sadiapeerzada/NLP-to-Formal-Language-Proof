# Curation audit v0.1.2 — 21 October 2026

This audit covers the 21-record baseline draft and candidate batches v0.1.0–v0.1.6. It is an inventory, not a freeze or independent review.

- Aggregate candidate records: 32 (21 baseline + 11 source-batch candidates).
- Proposed split counts: development 24, test 8; all remain unreviewed proposals.
- Categories: arithmetic identity 6, divisibility 11, induction 6, inequality 4, modular arithmetic 5.
- Lean evidence: 10 candidates have recorded strict theorem-proof verification; `mod_005` has a separate statement-type elaboration check with a `sorry` placeholder, not a checked proof. Twenty-one baseline records lack pinned theorem verification metadata.
- Source leads: 11 candidates cite DMOI3; 21 baseline records have no item-level source citation. Seven records carry a `verified` source/license evidence field, four are marked `needs_review`, and 21 lack that evidence. No independent rights-clearance decision is recorded.
- Source/license next actions: independently review redistribution/attribution compatibility for the 11 DMOI3 records (`div_007`–`div_009`, `ind_005`, `ineq_004`, `mod_004`, `arith_005`, `ind_006`, `div_010`, `div_011`, `mod_005`); complete or audit the four `needs_review` evidence records (`ind_006`, `div_010`, `div_011`, `mod_005`); identify and source the 21 baseline items before use.
- Missing Lean verification: all 21 baseline IDs (`arith_001`, `arith_002`, `div_001`–`div_006`, `ind_001`–`ind_004`, `ineq_001`–`ineq_003`, `mod_001`–`mod_003`) need pinned theorem checks. `mod_005` has only a statement-type check. The ten prior DMOI3 proofs have recorded strict verifier results.
- Independent semantic/theorem/assumption/self-containment/family/split/duplicate review: none is complete across the 32 candidates. The exact/similarity review queue is listed above; additionally adjudicate the screened-out Exercise 13 versus `ineq_004` before deciding whether to retain the screen-out.
- Completed independent reviews: 0. Eligible development: 0. Eligible test: 0. Dataset remains unfrozen.
- Source-page/PDF bytes archived for batch v0.1.6: no. License compatibility and semantic/family/split reviews: pending.
- Likely-duplicate pairs still awaiting human adjudication: arith_003 / arith_003_mathlib; div_001 / div_005; mod_002 / mod_003. The proposed mod_005 family and split also require independent review.
- DMOI3 §2.5 Exercise 13 was screened out because it duplicates the existing ineq_004 claim; it is recorded in batch `screened_out_items.json` and excluded from the candidate count.

Difficulty counts: level 1: 10; level 2: 13; level 3: 7; level 4: 2. The strict aggregate validator reports zero structural errors but zero eligible items. Its warnings are retained in `research_dataset_inventory_v0.2.1.json`. Record-level review packets for the current pool are under `data/review_packets/current_pool_v0.2.1/`; all reviewer and decision fields remain pending.

Shortfall against targets: at least 15 eligible development items remain (target range 15–20), and at least 60 eligible test items remain. The current proposal has eight test candidates, but none eligible.

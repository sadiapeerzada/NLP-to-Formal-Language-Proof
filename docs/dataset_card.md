# Research dataset card — current preparation

Status: unreviewed candidate pool, not a released/frozen benchmark. Current evidence is `data/analysis/m1_m7_delivery_20261028/summary.json` and `docs/FINAL_DATASET_COMPLETION.md`.

There are 96 candidates, proposed 30 development / 66 test, across five categories. All 96 prepared reference statements now have strict proof evidence in Lean 4.32.0 / pinned Mathlib. Twenty-five original reference checks are added through immutable evidence overlays; the geometric-sum candidate now has explicit hash-pinned definition context without rewriting its historical file. There are zero independently reviewed, eligible or frozen records.

The pool comprises 21 original draft statements, 16 textbook acquisitions and 59 formal-library-derived candidates. Original source files, copyright/license notices, exact theorem/source/proof hashes, assumptions/imports, provisional difficulty/families and pending review metadata are preserved. The 59 English paraphrases are author-assisted adaptations, not falsely attributed source quotations. The original 21 statements still lack adequate item-level source provenance. Independent rights/API-or-local-input compatibility review is not inferred from public accessibility or a copied license notice.

Category counts: arithmetic identities 18, divisibility 24, induction 16, inequalities 16, modular arithmetic 15. Sixty proposed test IDs do not establish sixty independent eligible examples. Human family/duplicate review may merge or exclude generalizations; exposure to Mathlib/pretraining and named reference lemmas must be assessed. No new candidate was used for model selection, prompt tuning or mathematical inference.

Review Markdown/JSON and blank decisions: `data/review_packets/m1_m7_delivery_20261028/README.md`. Required labels are faithful / not faithful / uncertain. Imported decisions require genuine independent reviewer provenance and current content/evidence hashes. End-to-end faithfulness additionally requires review of actual generated statements, not just reference proofs.

Targets remain at least 60 independent eligible held-out examples (preferably 100) and 15–20 separate eligible development examples. No freeze is allowed until all evidence, counts, whole-family separation, reviews and exact ordered-byte manifest checks pass. Current frozen validation deliberately fails.

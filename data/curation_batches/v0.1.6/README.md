# Candidate batch v0.1.6

This batch adds one source-located candidate, `mod_005`, from Oscar Levin's
*Discrete Mathematics: An Open Introduction*, 3rd edition, section 2.5,
Exercise 3. The source page asks to prove that `7^n - 1` is a multiple of 6
for natural `n`; its solution explicitly treats the base case `n = 0`.
The corresponding Lean proposition is `6 ∣ 7 ^ n - 1` over `ℕ`.

The publisher-hosted page and its [colophon](https://discrete.openmathbooks.org/dmoi3/front-colophon.html)
were inspected on 2026-10-21. The colophon identifies CC BY-SA 4.0. This is
recorded as observed license evidence, not independent rights clearance or a
decision that redistribution is compatible with the intended release. The
source-page/PDF bytes were not captured, so no page-byte hash is claimed.
The exact source wording transcription, item locator, attribution, adaptation
history, and UTF-8 hashes are in `candidate_records.json` and
`source_statement_transcriptions.txt`.

`statement_check.lean` was run with the pinned project command in
`verification.log`. Lean exited 0 while emitting a `hasSorry` warning. The
placeholder checks elaboration of the theorem proposition only; it does not
verify a proof. It is not a proof artifact and must not be used as one.

`screened_out_items.json` records DMOI3 section 2.5 Exercise 13, which was
excluded from the active batch because it duplicates existing `ineq_004`.
Independent duplicate adjudication is still pending.

The record remains ineligible. Source/license compatibility, semantic
faithfulness, exact theorem review, assumptions, self-containment,
category/difficulty, theorem family, split, and duplicate review all require
independent human review. The evidence-prefilled review packet is in
`data/review_packets/current_pool_v0.2.1/mod_005.json`.

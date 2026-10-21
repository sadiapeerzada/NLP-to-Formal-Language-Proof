# Candidate batch v0.1.7

This batch adds three source-located DMOI3 section 2.5 exercises by Oscar
Levin: Exercise 10 (sum of squares), Exercise 19 (representation by distinct
powers of two), and Exercise 24 (the hockey-stick binomial identity). The
publisher page and item locators were inspected on 2026-10-21. The exact
transcriptions, source URLs, attribution text, adaptations, and transcription
hashes are recorded in `candidate_records.json` and
`source_statement_transcriptions.txt`.

The publisher's [colophon](https://discrete.openmathbooks.org/dmoi3/front-colophon.html)
identifies CC BY-SA 4.0. This is observed source-license evidence only; no
independent rights/redistribution compatibility review is recorded. The HTML
page/PDF bytes were not archived or hashed. All three proposed records remain
in development with pending split/family review.

`statement_check.lean` was run under the repository's pinned Lean/Mathlib
project. It exited 0 with `hasSorry` warnings for the three explicit proof
placeholders. This checks proposition elaboration only. It does not verify
proofs, inspect proof axioms, or establish English-to-Lean semantic fidelity.
See `verification.log` for command, result, diagnostic output, and hashes.

Three overlapping source items were screened out and retained in
`screened_out_items.json`: Exercise 2 duplicates the existing geometric-sum
family `ind_004`; Exercise 21 overlaps the triangular-number formula `ind_001`;
Exercise 23 is the existing Pascal-row sum item `ind_005`. The independent
reviewer must confirm these screen-outs; none was assigned a new candidate ID.

All required source/license, semantic, theorem, assumption, self-containment,
category/difficulty, family/split, and duplicate reviews remain pending. The
three full-pool review packets are in
`data/review_packets/current_pool_v0.2.2/ind_007.json`, `ind_008.json`, and
`ind_009.json`.

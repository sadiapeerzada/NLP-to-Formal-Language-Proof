# Candidate batch v0.1.5

This three-record batch extends the existing DMOI3 discovery work with
`ind_006`, `div_010`, and `div_011`. Each candidate has an item locator, an
adapted English statement, a Lean reference statement, source attribution,
source-statement transcription hash, and exact Lean-statement hash. The batch
is a candidate set only.

Source: Oscar Levin, *Discrete Mathematics: An Open Introduction*, 3rd
edition, section 2.5 (postage-stamp induction claim) and section 5.2 (exercises
1 and 2). The publisher identifies the 3rd edition as appropriate for first- or
second-year undergraduate mathematics/computer-science courses and states
CC BY-SA 4.0 with attribution. See the source and license URLs in each record.
The source page/PDF bytes were not archived or hashed. The license status for
these records remains `needs_review`; the observed license statement is not a
legal compatibility decision or independent rights review.

All three Lean reference theorems passed the repository strict verifier in
Lean `leanprover/lean4:v4.32.0` with Mathlib revision
`81a5d257c8e410db227a6665ed08f64fea08e997`. The checker type-compared each
candidate against its statement and inspected theorem axioms. Full hashes and
results are in `verification.log`. Compilation does not establish semantic
faithfulness.

Family, split, category/difficulty, source/license, semantic, theorem,
assumption, self-containment, and duplicate reviews remain pending. The two
divisibility candidates are provisionally grouped in the test split; this
assignment is not an independent holdout decision. The postage candidate is
provisionally in development. Eligible count: zero.

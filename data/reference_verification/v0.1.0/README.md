# Additional reference proof checks

Twenty original candidate statements now have strict reference-proof evidence in the pinned environment. These are authored/reused reference proofs, not LLM outputs. Historical records and manual generated files are unchanged. `proof_overlay.json` adds only hash-bound automated proof metadata when constructing the current inventory.

`references.lean` contains complete candidate proofs with no forbidden shortcuts. `references_checked.lean` preserves those exact declarations and appends isolated `ReferenceExpected` statement-elaboration placeholders and Lean proof-type comparisons against the exact recorded statements. Only expected statements use placeholders; the twenty target theorem axiom lists contain no sorryAx. Overall compiler exit was 0. The loader rejects changed evidence bytes, missing exact statements, compiler errors and unapproved target axioms.

The original geometric-sum candidate still lacks a self-contained definition of `geomSum`; it was deliberately excluded rather than silently changing its statement. Four other candidates still have statement-elaboration-only evidence. Independent meaning, source, family, split and license reviews remain outstanding for every candidate.

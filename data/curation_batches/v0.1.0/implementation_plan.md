# First curation batch implementation plan

## Repository baseline

- The versioned research draft has 21 candidates and the manifest reports zero
  eligible records. Its proposed split is 15 development and 6 test, with one
  unresolved exact-English duplicate pair.
- The validator's research categories are currently fixed to `arithmetic_identity`,
  `divisibility`, `modular_arithmetic`, `induction`, and `inequality`.
- The existing source-lead ledger has no candidate theorem records. Its
  ProofNet and miniF2F leads still need item-level upstream rights tracing;
  the OpenStax lead has CC BY-NC-SA terms that need compatibility review.
- The project pins Lean `leanprover/lean4:v4.32.0` and Mathlib revision
  `81a5d257c8e410db227a6665ed08f64fea08e997`. Its verifier rejects
  `sorry`/`admit`, added `axiom`/`constant`/`opaque` declarations, and
  unapproved theorem axioms.

## Steps for this batch

1. Use an edition whose own license and item source can be inspected. The
   selected source is Oscar Levin's *Discrete Mathematics: An Open
   Introduction*, 3rd edition, 5th printing, with CC BY-SA 4.0 stated in the
   PDF and on the official edition page. Preserve attribution and apply
   share-alike to this adapted batch.
2. Select two exact source claims, capture their source locations and source
   statement hashes, and keep them in a separate candidate file. Do not edit
   the existing draft or manifest.
3. Create standalone Lean files, compile under the pinned project, then use
   the repository's strict verifier to inspect prohibited shortcuts and
   theorem axioms. Record the commands and hashes.
4. Keep all human-review-dependent fields pending. Assign both candidates to
   proposed development and one conservative family so they cannot leak
   across splits.
5. Run the draft validator and focused dataset-validation tests. Report
   candidates and eligible records separately. Do not freeze or expose test
   material.

## Limits

This batch is deliberately limited to the currently supported `divisibility`
category. The task's desired category breadth will require sourced examples
and likely a versioned schema/validator expansion. No category or validation
rule is added here. No independent reviewer is available in this batch, so
the records remain ineligible regardless of source and compilation evidence.

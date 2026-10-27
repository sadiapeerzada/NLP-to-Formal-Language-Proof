# lib_q_finite_inclusion: independent review

## English statement

```text
For finite sets s and t of natural numbers, if s is contained in t then the number of elements of s is at most the number of elements of t.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_q_finite_inclusion (s t : Finset ℕ) (h : s ⊆ t) : s.card ≤ t.card
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (s t",
  "required_imports": [
    "Mathlib"
  ],
  "category": "inequality",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Finset/Card.lean:66, formal item card_le_card. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Finset/Card.lean#L66",
  "source_license": "Apache-2.0",
  "problem_family": "finite_set_inclusion_cardinality",
  "split": "test",
  "theorem_verification": {
    "status": "verified",
    "success": true,
    "verification_scope": "strict_proof",
    "lean_toolchain": "leanprover/lean4:v4.32.0",
    "mathlib_revision": "81a5d257c8e410db227a6665ed08f64fea08e997",
    "command": [
      "lake",
      "env",
      "lean",
      "--json",
      "/Users/sadiapeerzada/NLP-to-Formal-Language-Proof/data/curation_batches/v0.2.0/references_expanded.lean"
    ],
    "theorem_sha256": "de1cd1e448e05bfd1e24797802adccd110260fce5c4b6e60bfa77d328911fbd5",
    "reference_code_sha256": "6b1157c42b4e5e488512b7de5335e70a5c1cfa8022194708f6e0d648b29afe55",
    "verification_source_sha256": "7b116ce104b59338fdcdf3e736fe4392c39b77f32db73dabef9afcd005680367",
    "axiom_dependencies": [
      "propext",
      "Quot.sound"
    ],
    "evidence": "data/curation_batches/v0.2.0/verification_expanded.json; overall exit 0, zero error/malformed diagnostics, explicit per-theorem axiom inspection; no placeholder proofs."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `4e13629266e07292e90794c22ccd79a8a06e8f68b1e586de98c68a9edf6a6c6a`. Fill `lib_q_finite_inclusion.decision.json`; do not edit source fields.

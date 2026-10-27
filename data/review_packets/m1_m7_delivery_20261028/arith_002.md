# arith_002: independent review

## English statement

```text
For any natural numbers a and b, a squared minus b squared equals (a + b) times (a - b), assuming a is at least b.
```

## Lean reference

```lean
theorem sq_sub_sq_nat (a b : ℕ) (h : b ≤ a) : a ^ 2 - b ^ 2 = (a + b) * (a - b)
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": null,
  "required_imports": [
    "Mathlib"
  ],
  "required_definitions": null,
  "category": "arithmetic_identity",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": null,
  "source_url": null,
  "source_license": null,
  "problem_family": "nat_square_identities",
  "split": "development",
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
      "/Users/sadiapeerzada/NLP-to-Formal-Language-Proof/data/reference_verification/v0.1.0/references_checked.lean"
    ],
    "theorem_sha256": "ade996b0fd58fc4c5dd9cadf71cd51ed001593a261ea5e6b8c922362384d6eaa",
    "verification_source_sha256": "49f07b252d75fda1e573c8a2738118c095ecd2efba04b1dfaf5579a37fbaf139",
    "axiom_dependencies": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "evidence": "data/reference_verification/v0.1.0/proof_overlay.json; candidate source has no placeholders; exact-type comparison and target axiom inspection passed. ReferenceExpected placeholders check types only."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `3d3a18b676ec29888604641961d444e478f5d8ae3eadf7baaf07d050c6b8b1b2`. Fill `arith_002.decision.json`; do not edit source fields.

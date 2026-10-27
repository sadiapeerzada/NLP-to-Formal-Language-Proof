# arith_003: independent review

## English statement

```text
For any natural numbers a, b, and c, a times (b plus c) equals a times b plus a times c.
```

## Lean reference

```lean
theorem mul_distrib_left (a b c : ℕ) : a * (b + c) = a * b + a * c
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": null,
  "required_imports": [
    "Mathlib"
  ],
  "category": "arithmetic_identity",
  "difficulty": 1
}
```

## Source and proof evidence

```json
{
  "source_citation": null,
  "source_url": null,
  "source_license": null,
  "problem_family": "nat_distributivity",
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
    "theorem_sha256": "f6753dfc6a44f9da8a9408aee308175c68c5b27769f1e043ffdb3ce8c0aba0f5",
    "verification_source_sha256": "49f07b252d75fda1e573c8a2738118c095ecd2efba04b1dfaf5579a37fbaf139",
    "axiom_dependencies": [],
    "evidence": "data/reference_verification/v0.1.0/proof_overlay.json; candidate source has no placeholders; exact-type comparison and target axiom inspection passed. ReferenceExpected placeholders check types only."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `ff822b8e121475d8f5e9d86582f18ca566647dd24a26d9dd45f9a51487ba7acd`. Fill `arith_003.decision.json`; do not edit source fields.

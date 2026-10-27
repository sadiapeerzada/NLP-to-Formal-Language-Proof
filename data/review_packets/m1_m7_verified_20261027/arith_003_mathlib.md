# arith_003_mathlib: independent review

## English statement

```text
For any natural numbers a, b, and c, a times (b plus c) equals a times b plus a times c.
```

## Lean reference

```lean
theorem distributive_nat (a b c : ℕ) : a * (b + c) = a * b + a * c
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
    "theorem_sha256": "c3ebe91cf40cfdf918706406b345be1ccfc1eab8e15fc45311379bffb9613faa",
    "verification_source_sha256": "49f07b252d75fda1e573c8a2738118c095ecd2efba04b1dfaf5579a37fbaf139",
    "axiom_dependencies": [],
    "evidence": "data/reference_verification/v0.1.0/proof_overlay.json; candidate source has no placeholders; exact-type comparison and target axiom inspection passed. ReferenceExpected placeholders check types only."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `1180bb97f45791e9c7c994ff1376bea9741c838a3348e7b5f4726458132a15cf`. Fill `arith_003_mathlib.decision.json`; do not edit source fields.

# ineq_002: independent review

## English statement

```text
For any natural numbers a and b, a times b plus 1 is at most (a+1) times (b+1).
```

## Lean reference

```lean
theorem prod_succ_ge (a b : ℕ) : a * b + 1 ≤ (a + 1) * (b + 1)
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
  "category": "inequality",
  "difficulty": 1
}
```

## Source and proof evidence

```json
{
  "source_citation": null,
  "source_url": null,
  "source_license": null,
  "problem_family": "nat_product_bound",
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
    "theorem_sha256": "529e4bf97f0d8c867d05933e0b4a46d91eb6c234f7bf05d85a8eb4fcb41f6d68",
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

Binding SHA-256: `cf25e6f11c2ba9ce83044a55a6caf8de4e150212302f3c8248838f0521fb8709`. Fill `ineq_002.decision.json`; do not edit source fields.

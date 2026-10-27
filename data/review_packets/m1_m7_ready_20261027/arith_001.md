# arith_001: independent review

## English statement

```text
For any natural numbers a and b, (a + b) squared equals a squared plus 2ab plus b squared.
```

## Lean reference

```lean
theorem add_sq_nat (a b : ℕ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2
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
  "difficulty": 1
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
    "theorem_sha256": "8aa2507ef8087049c265267ab36560cfbf928f35a0c321d5f2023006e753d649",
    "verification_source_sha256": "49f07b252d75fda1e573c8a2738118c095ecd2efba04b1dfaf5579a37fbaf139",
    "axiom_dependencies": [
      "propext"
    ],
    "evidence": "data/reference_verification/v0.1.0/proof_overlay.json; candidate source has no placeholders; exact-type comparison and target axiom inspection passed. ReferenceExpected placeholders check types only."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `8a861a2e967c2245ef038be30b0d984759fdae2ee5aa6aa8defe8478ab3fbd47`. Fill `arith_001.decision.json`; do not edit source fields.

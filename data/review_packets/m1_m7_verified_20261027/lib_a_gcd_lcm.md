# lib_a_gcd_lcm: independent review

## English statement

```text
For natural numbers a and b, their greatest common divisor times their least common multiple equals their product.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_a_gcd_lcm (a b : ℕ) : Nat.gcd a b * Nat.lcm a b = a * b
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (a b",
  "required_imports": [
    "Mathlib"
  ],
  "category": "arithmetic_identity",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover/lean4 at 8c9756b28d64dab099da31a4c09229a9e6a2ef35, Init/Data/Nat/Lcm.lean:38, formal item gcd_mul_lcm. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover/lean4/blob/8c9756b28d64dab099da31a4c09229a9e6a2ef35/src/lean/Init/Data/Nat/Lcm.lean#L38",
  "source_license": "Apache-2.0",
  "problem_family": "gcd_lcm_product_identity",
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
    "theorem_sha256": "f991ff09cea83a0a3704eeb3f7249b285e714788b34d6ef35cd604ae8dbb4c3c",
    "reference_code_sha256": "82ad2b48913a269b24f31ecc789b7f900afb607416d620a8654c21e025553424",
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

Binding SHA-256: `2c50cb3ad658402803a66356dd65706c2fd3012894350098d7bb885ee89c5829`. Fill `lib_a_gcd_lcm.decision.json`; do not edit source fields.

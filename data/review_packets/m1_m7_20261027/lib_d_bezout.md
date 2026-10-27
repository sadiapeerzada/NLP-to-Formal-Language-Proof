# lib_d_bezout: independent review

## English statement

```text
For integers a and b, their nonnegative greatest common divisor is an integer linear combination of a and b.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_d_bezout (a b : ℤ) : ∃ x y : ℤ, (Int.gcd a b : ℤ) = a * x + b * y
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (a b",
  "required_imports": [
    "Mathlib"
  ],
  "category": "divisibility",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Int/GCD.lean:172, formal item gcd_eq_gcd_ab. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Int/GCD.lean#L172",
  "source_license": "Apache-2.0",
  "problem_family": "bezout_integer_representation",
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
    "theorem_sha256": "d5a20ebe7d43b88277a2d81ab2fdc1124fc18dd63e527c625d9151c61c261d51",
    "reference_code_sha256": "edcbec8a80653f0c52c5ad9ab46d133266f01b0a81ccb907b6e5eaea771ff890",
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

Binding SHA-256: `c6fca8cd64a7ab6227199a54f0709dc84bb7af3997d681f8cd35090e433d7d17`. Fill `lib_d_bezout.decision.json`; do not edit source fields.

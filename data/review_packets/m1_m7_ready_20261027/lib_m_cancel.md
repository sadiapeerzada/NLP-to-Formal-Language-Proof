# lib_m_cancel: independent review

## English statement

```text
For positive natural m, if c*a and c*b are congruent modulo m, then a and b are congruent modulo m/gcd(m,c).
```

## Lean reference

```lean
open scoped BigOperators
theorem study_m_cancel (m c a b : ℕ) (hm : 0 < m) (h : Nat.ModEq m (c * a) (c * b)) : Nat.ModEq (m / Nat.gcd m c) a b
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (m c a b",
  "required_imports": [
    "Mathlib"
  ],
  "required_definitions": null,
  "category": "modular_arithmetic",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/ModEq.lean:378, formal item cancel_left_div_gcd. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/ModEq.lean#L378",
  "source_license": "Apache-2.0",
  "problem_family": "congruence_cancellation_adjusted_modulus",
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
    "theorem_sha256": "f6bfb7af88db4221da91811170c6d1087522ef1e304522ad2d422be19cbc0e5a",
    "reference_code_sha256": "6370855da3cc6047277999ef90c068633754329f9704e6e476045c00f99ab155",
    "verification_source_sha256": "7b116ce104b59338fdcdf3e736fe4392c39b77f32db73dabef9afcd005680367",
    "axiom_dependencies": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "evidence": "data/curation_batches/v0.2.0/verification_expanded.json; overall exit 0, zero error/malformed diagnostics, explicit per-theorem axiom inspection; no placeholder proofs."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `bbc4819b1d6c41abb681b63f835bce64c564a3a37442b70782d44f080255c99c`. Fill `lib_m_cancel.decision.json`; do not edit source fields.

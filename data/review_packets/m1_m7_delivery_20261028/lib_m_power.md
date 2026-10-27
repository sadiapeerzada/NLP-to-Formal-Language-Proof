# lib_m_power: independent review

## English statement

```text
For integers a,b,m and a natural exponent n, congruence of a and b modulo m implies congruence of their nth powers modulo m.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_m_power (a b m : ℤ) (n : ℕ) (h : Int.ModEq m a b) : Int.ModEq m (a ^ n) (b ^ n)
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (a b m",
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Int/ModEq.lean:196, formal item ModEq.pow. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Int/ModEq.lean#L196",
  "source_license": "Apache-2.0",
  "problem_family": "congruence_power_preservation",
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
    "theorem_sha256": "c5ec70f85fc3052513ae63bba837b7f83f7a6a226e4a0e99c3080315f8b846eb",
    "reference_code_sha256": "db6532298b412b25218c74eaec5c679c525f6278f0badc05b7f822d0a72e553d",
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

Binding SHA-256: `d1f64481f7b53654f1f3585523180ff0ec4a35f3b03309896f702d84b5462bbf`. Fill `lib_m_power.decision.json`; do not edit source fields.

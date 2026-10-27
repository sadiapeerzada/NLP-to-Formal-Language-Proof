# lib_m_euler: independent review

## English statement

```text
For coprime natural a and m, a raised to Euler totient(m) is congruent to one modulo m.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_m_euler (a m : ℕ) (h : Nat.Coprime a m) : Nat.ModEq m (a ^ Nat.totient m) 1
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (a m",
  "required_imports": [
    "Mathlib"
  ],
  "category": "modular_arithmetic",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/FieldTheory/Finite/Basic.lean:564, formal item ModEq.pow_totient. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/FieldTheory/Finite/Basic.lean#L564",
  "source_license": "Apache-2.0",
  "problem_family": "euler_totient_unit_group_exponent",
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
    "theorem_sha256": "a721d25efc78fd7c656de9c555af40762375555835e801a3eee92be6a474da81",
    "reference_code_sha256": "0462382c5f08a0f1426187561e1b8048c5ee21da6019679a632f0aba34d38183",
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

Binding SHA-256: `d62c05ebb98e39c37d9ecbcb6eeb8ebc856f822b4bb2ca62dbb5f7125b1364d8`. Fill `lib_m_euler.decision.json`; do not edit source fields.

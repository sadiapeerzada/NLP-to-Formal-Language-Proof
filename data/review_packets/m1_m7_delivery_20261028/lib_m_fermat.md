# lib_m_fermat: independent review

## English statement

```text
For a natural prime p and integer a, a^p is congruent to a modulo p.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_m_fermat (p : ℕ) (hp : p.Prime) (a : ℤ) : Int.ModEq (p : ℤ) (a ^ p) a
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (p",
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/FieldTheory/Finite/Basic.lean:651, formal item pow_prime_eq_self. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/FieldTheory/Finite/Basic.lean#L651",
  "source_license": "Apache-2.0",
  "problem_family": "fermat_little_theorem",
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
    "theorem_sha256": "b4bc86f54028ef33430566e36522ab64f5b5591fe4d10539d4ef6be0098dd93c",
    "reference_code_sha256": "7583a4d7f2545f4a1a27ff1e2ee84400d710cae61b66c4f665aa5950271b6c59",
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

Binding SHA-256: `3d75d9cb9f13634602f9c7f9a89106545022b958572c072ac2de18147dd94410`. Fill `lib_m_fermat.decision.json`; do not edit source fields.

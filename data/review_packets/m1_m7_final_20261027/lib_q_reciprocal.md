# lib_q_reciprocal: independent review

## English statement

```text
If real numbers x and y satisfy 0<x and x≤y, then 1/y≤1/x.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_q_reciprocal (x y : ℝ) (hx : 0 < x) (hxy : x ≤ y) : 1 / y ≤ 1 / x
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (x y",
  "required_imports": [
    "Mathlib"
  ],
  "category": "inequality",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Algebra/Order/Field/Basic.lean:69, formal item one_div_le_one_div_of_le. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Algebra/Order/Field/Basic.lean#L69",
  "source_license": "Apache-2.0",
  "problem_family": "positive_reciprocal_antitone",
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
    "theorem_sha256": "9ff6511db53e6e5722a59dda87893c0b9d91f66cfa5971f11fc75ab436d96f86",
    "reference_code_sha256": "410916de18ce6b1d59afcda1d2a55b227e669781053ec27dc866b484fb3cc6b0",
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

Binding SHA-256: `106a78721bb01cabdb45031316c57a19e6d15d475a20f377e406fc52e5a6b11f`. Fill `lib_q_reciprocal.decision.json`; do not edit source fields.

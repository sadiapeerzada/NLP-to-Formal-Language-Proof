# lib_q_sqrt_monotone: independent review

## English statement

```text
For real x and y with x≤y, the principal square root of x is at most that of y, using the totalized real square root which is zero on negative inputs.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_q_sqrt_monotone (x y : ℝ) (h : x ≤ y) : Real.sqrt x ≤ Real.sqrt y
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (x y",
  "required_imports": [
    "Mathlib"
  ],
  "required_definitions": null,
  "category": "inequality",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Analysis/Real/Sqrt.lean:209, formal item sqrt_le_sqrt. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Analysis/Real/Sqrt.lean#L209",
  "source_license": "Apache-2.0",
  "problem_family": "principal_square_root_monotonicity",
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
    "theorem_sha256": "edb32f0bbce5046d878e749e99c21f43a6db694e3bc58bbd1b8f998884098126",
    "reference_code_sha256": "5b505c9fb99fb4ac60965d84d2eb04aaa5aa35f0a1ba34b6b139fd1d630c1d31",
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

Binding SHA-256: `296ac200763926bedc6dcc55d0abce8a4c7ae29091f56534122d7b420b90bdcf`. Fill `lib_q_sqrt_monotone.decision.json`; do not edit source fields.

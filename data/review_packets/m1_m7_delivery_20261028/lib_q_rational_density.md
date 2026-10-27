# lib_q_rational_density: independent review

## English statement

```text
Between any two distinct real numbers x<y there is a rational number q with x<q<y.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_q_rational_density (x y : ℝ) (h : x < y) : ∃ q : ℚ, x < q ∧ (q : ℝ) < y
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Algebra/Order/Archimedean/Basic.lean:372, formal item exists_rat_btwn. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Algebra/Order/Archimedean/Basic.lean#L372",
  "source_license": "Apache-2.0",
  "problem_family": "rational_density_in_reals",
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
      "/Users/sadiapeerzada/NLP-to-Formal-Language-Proof/data/curation_batches/v0.2.1/references_expanded.lean"
    ],
    "theorem_sha256": "8d7084c575cfd7dfda8c71eac727f8629c057a8909425ea37783cf163ef6a879",
    "reference_code_sha256": "71ee5ff048e19f926a515d8d6aff8a99d31a4973e959ed8a52ad6917c7729853",
    "verification_source_sha256": "45272f1c1eb3e1591fb15a57a854f4685b2dd191caee4a9918195ddab77d7ccf",
    "axiom_dependencies": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "evidence": "data/curation_batches/v0.2.1/verification_expanded.json; overall exit 0, zero error/malformed diagnostics, explicit per-theorem axiom inspection; no placeholder proofs."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `f64cfb32abe0c1f9010fd8302c0f54dbdd12679bc580697c3fbded2549e3bd0d`. Fill `lib_q_rational_density.decision.json`; do not edit source fields.

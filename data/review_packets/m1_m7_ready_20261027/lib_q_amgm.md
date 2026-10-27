# lib_q_amgm: independent review

## English statement

```text
For real numbers x and y, twice their product is at most the sum of their squares.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_q_amgm (x y : ℝ) : 2 * x * y ≤ x ^ 2 + y ^ 2
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Algebra/Order/Ring/Unbundled/Basic.lean:680, formal item two_mul_le_add_sq. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Algebra/Order/Ring/Unbundled/Basic.lean#L680",
  "source_license": "Apache-2.0",
  "problem_family": "two_variable_quadratic_amgm",
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
    "theorem_sha256": "1aab3d7670c2c0999b33c89faebe2bbb691579dd5315fcafbdf246900ab62499",
    "reference_code_sha256": "ce6a7088a43502d7a2ca2737ee58b21a536cbff1fcb747b090d7f2467c2e3192",
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

Binding SHA-256: `b726846889c03f9685ce1d69a71f5b5bd8d647f4cba7ef95065f5bbbbe847566`. Fill `lib_q_amgm.decision.json`; do not edit source fields.

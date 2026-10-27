# lib_i_bernoulli: independent review

## English statement

```text
For any real x at least -1 and natural number n, 1+n*x is at most (1+x)^n.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_i_bernoulli (x : ℝ) (n : ℕ) (h : -1 ≤ x) : 1 + (n : ℝ) * x ≤ (1 + x) ^ n
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (x",
  "required_imports": [
    "Mathlib"
  ],
  "category": "induction",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Algebra/Order/Ring/Pow.lean:100, formal item one_add_mul_le_pow. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Algebra/Order/Ring/Pow.lean#L100",
  "source_license": "Apache-2.0",
  "problem_family": "bernoulli_inequality",
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
    "theorem_sha256": "7b3fbb286e27e4dea355bf866b57268626464606a7e71a65e07654ba3e7cbf8d",
    "reference_code_sha256": "842fb23c7c9a55b54c416440547c5ee96d875ac865b9f86edf7d2f555bf9d903",
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

Binding SHA-256: `052c760263bb5993f58db980eced970d7c8382308feb31201e9257945828d0e3`. Fill `lib_i_bernoulli.decision.json`; do not edit source fields.

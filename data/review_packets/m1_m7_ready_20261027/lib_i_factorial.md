# lib_i_factorial: independent review

## English statement

```text
For every natural number n, (n+1) factorial equals (n+1) times n factorial.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_i_factorial (n : ℕ) : (n + 1).factorial = (n + 1) * n.factorial
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (n",
  "required_imports": [
    "Mathlib"
  ],
  "required_definitions": null,
  "category": "induction",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/Factorial/Basic.lean:55, formal item factorial_succ. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/Factorial/Basic.lean#L55",
  "source_license": "Apache-2.0",
  "problem_family": "factorial_successor_recurrence",
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
    "theorem_sha256": "865dcfa129360f658d43f67b29248300ecd2807a9d5fea9934bae22edd7cb471",
    "reference_code_sha256": "d15d9359c4123565eace3713227b9824bf5f6127e71e0753de99e33ade66ea26",
    "verification_source_sha256": "7b116ce104b59338fdcdf3e736fe4392c39b77f32db73dabef9afcd005680367",
    "axiom_dependencies": [],
    "evidence": "data/curation_batches/v0.2.0/verification_expanded.json; overall exit 0, zero error/malformed diagnostics, explicit per-theorem axiom inspection; no placeholder proofs."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `79b06d31d93f3f945d17e7c76d5fa17771660a7c1d0a95a79f3ce7c2fb01470f`. Fill `lib_i_factorial.decision.json`; do not edit source fields.

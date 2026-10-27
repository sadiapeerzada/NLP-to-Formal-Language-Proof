# lib_i_alternating_binomial: independent review

## English statement

```text
For every positive natural n, the alternating sum of the binomial coefficients in row n is zero, interpreted in the integers.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_i_alternating_binomial (n : ℕ) (hn : n ≠ 0) : (∑ k ∈ Finset.range (n + 1), ((-1 : ℤ) ^ k * (n.choose k : ℤ))) = 0
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (n",
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/Choose/Sum.lean:199, formal item alternating_sum_range_choose_of_ne. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/Choose/Sum.lean#L199",
  "source_license": "Apache-2.0",
  "problem_family": "alternating_binomial_cancellation",
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
    "theorem_sha256": "d0aa99b548a9992ab98f6dea07518d6d3126dd31a9c965fe8259991ae46107a8",
    "reference_code_sha256": "62fe31e5e1206580b0256c8c703e4aedabbfcb2dfbd3bd642e3b18ce5850b895",
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

Binding SHA-256: `43e7b248d794bb3117807c02be116d880fa0a3b0c0965d1ba128d6c1f4615dc7`. Fill `lib_i_alternating_binomial.decision.json`; do not edit source fields.

# lib_i_vandermonde: independent review

## English statement

```text
For natural numbers m, n and k, choosing k elements from m+n equals the sum, over i from 0 through k, of choose(m,i) times choose(n,k-i).
```

## Lean reference

```lean
open scoped BigOperators
theorem study_i_vandermonde (m n k : ℕ) : (m + n).choose k = ∑ i ∈ Finset.range (k + 1), m.choose i * n.choose (k - i)
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (m n k",
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/Choose/Vandermonde.lean:31, formal item add_choose_eq. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/Choose/Vandermonde.lean#L31",
  "source_license": "Apache-2.0",
  "problem_family": "vandermonde_convolution",
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
    "theorem_sha256": "0f95cd3cdb6c0d941e9c70c37b5ac0c772ab369d7384736a151e3e4f0a62a389",
    "reference_code_sha256": "974c6192b73f3ac0df643d19464ffedf7291460879720561b95775f7b3ff7508",
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

Binding SHA-256: `9c23bec0ef85641822b79930516402f0fce4371510a4036f089a50dd1ab2c13d`. Fill `lib_i_vandermonde.decision.json`; do not edit source fields.

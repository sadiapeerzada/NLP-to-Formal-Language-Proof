# lib_d_frobenius: independent review

## English statement

```text
If natural numbers m and n are coprime and a and b are nonzero natural numbers, m*a+n*b cannot equal m*n.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_d_frobenius (m n a b : ℕ) (h : Nat.Coprime m n) (ha : a ≠ 0) (hb : b ≠ 0) : m * a + n * b ≠ m * n
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (m n a b",
  "required_imports": [
    "Mathlib"
  ],
  "category": "divisibility",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/GCD/Basic.lean:233, formal item Coprime.mul_add_mul_ne_mul. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/GCD/Basic.lean#L233",
  "source_license": "Apache-2.0",
  "problem_family": "coprime_positive_combination_obstruction",
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
    "theorem_sha256": "804e480c36df84d1e0356e180f91ff47821d9d4431218c3bf6c6c56bfcfabd90",
    "reference_code_sha256": "16feffd0419c179e419730a671e8da1df688115194c10f6709194cae26cd8387",
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

Binding SHA-256: `a9bf8eb61f0e5ef2332c94d5a52b62fb6c2e1345b2415f2bf644771c1360deed`. Fill `lib_d_frobenius.decision.json`; do not edit source fields.

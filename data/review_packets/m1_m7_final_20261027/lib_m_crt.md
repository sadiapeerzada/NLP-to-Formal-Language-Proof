# lib_m_crt: independent review

## English statement

```text
If natural numbers a and b are congruent modulo gcd(n,m), there exists a natural number congruent to a modulo n and to b modulo m.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_m_crt (a b n m : ℕ) (h : Nat.ModEq (Nat.gcd n m) a b) : ∃ k : ℕ, Nat.ModEq n k a ∧ Nat.ModEq m k b
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (a b n m",
  "required_imports": [
    "Mathlib"
  ],
  "category": "modular_arithmetic",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/ModEq.lean:422, formal item chineseRemainder'. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/ModEq.lean#L422",
  "source_license": "Apache-2.0",
  "problem_family": "chinese_remainder_compatibility",
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
    "theorem_sha256": "dfedbbac87f761cd6776b65cf0aa41f0744099eb9d54d62a8f7170713dc5dcb9",
    "reference_code_sha256": "83bf0b4d439b8093db02a1b65a3410af3fc6f16c8de8f4911b19e466d7fd1468",
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

Binding SHA-256: `5a180e4cbab5d4d75fb0c403f0efcbb55562b3e4ed2aad7bf1a69c7cfce5b2f5`. Fill `lib_m_crt.decision.json`; do not edit source fields.

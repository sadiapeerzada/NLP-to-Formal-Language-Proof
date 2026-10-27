# lib_d_coprime_power: independent review

## English statement

```text
For natural numbers a and b and a positive natural exponent n, a^n is coprime to b if and only if a is coprime to b.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_d_coprime_power (a b n : ℕ) (hn : 0 < n) : Nat.Coprime (a ^ n) b ↔ Nat.Coprime a b
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (a b n",
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/GCD/Basic.lean:194, formal item coprime_pow_left_iff. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/GCD/Basic.lean#L194",
  "source_license": "Apache-2.0",
  "problem_family": "coprimality_power_invariance",
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
    "theorem_sha256": "a591b06d074e7135023daecdb752e25bd817a5afdb92947b6f20d51ca8bb5bc4",
    "reference_code_sha256": "2a549b56ac269a7dacbef303d45e74d4cf5fb4c43de924a439fcc4ea4cf33e7c",
    "verification_source_sha256": "7b116ce104b59338fdcdf3e736fe4392c39b77f32db73dabef9afcd005680367",
    "axiom_dependencies": [
      "propext",
      "Quot.sound"
    ],
    "evidence": "data/curation_batches/v0.2.0/verification_expanded.json; overall exit 0, zero error/malformed diagnostics, explicit per-theorem axiom inspection; no placeholder proofs."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `db4aa02738c5deeecedfd982745df37f69c50fb2d92040dbd1c02498bcf917c2`. Fill `lib_d_coprime_power.decision.json`; do not edit source fields.

# lib_d_mersenne_gcd: independent review

## English statement

```text
For natural numbers a, b and c, the greatest common divisor of a^b-1 and a^c-1 equals a raised to gcd(b,c), minus one; subtraction is natural-number subtraction.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_d_mersenne_gcd (a b c : ℕ) : Nat.gcd (a ^ b - 1) (a ^ c - 1) = a ^ Nat.gcd b c - 1
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (a b c",
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/GCD/Basic.lean:62, formal item pow_sub_one_gcd_pow_sub_one. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/GCD/Basic.lean#L62",
  "source_license": "Apache-2.0",
  "problem_family": "mersenne_gcd_exponents",
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
    "theorem_sha256": "831b9a27e6c36c82bb66c616ce003424dbe57acf7d7fb8ed402677eee4958d20",
    "reference_code_sha256": "1f6058717164f2f49a61104e1dfa0262d5f62bbf9d8c3e742a406e7a42a615b1",
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

Binding SHA-256: `5b798466b52f2f801bf5f52dd93e712ca763c05abe941048d57a50f29f372dcf`. Fill `lib_d_mersenne_gcd.decision.json`; do not edit source fields.

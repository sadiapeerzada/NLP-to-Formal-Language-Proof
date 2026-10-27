# lib_d_totient_sum: independent review

## English statement

```text
For every natural n, the sum of Euler totient(d) over the positive divisors d of n equals n; Mathlib assigns the empty divisor set to zero.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_d_totient_sum (n : ℕ) : (∑ d ∈ n.divisors, Nat.totient d) = n
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
  "category": "divisibility",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/Totient.lean:163, formal item sum_totient. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/Totient.lean#L163",
  "source_license": "Apache-2.0",
  "problem_family": "totient_divisor_sum",
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
    "theorem_sha256": "ef55f0d56c27a1fedbef11fd0f7f7ead42cffde9a66f80873c8062db8a303762",
    "reference_code_sha256": "c126ea60ef96ebb9b1738248ef5d4d9c1304b0b2a63c0be585d6038a38e1acbb",
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

Binding SHA-256: `33ceaa7099d40bf1d9e6d26ce33076009612a4ce09d582cefcd4da2c68f30511`. Fill `lib_d_totient_sum.decision.json`; do not edit source fields.

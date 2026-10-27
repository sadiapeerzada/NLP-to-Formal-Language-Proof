# lib_d_prime_factor_exists: independent review

## English statement

```text
Every natural number n at least two has a prime divisor.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_d_prime_factor_exists (n : ℕ) (hn : 2 ≤ n) : ∃ p : ℕ, p.Prime ∧ p ∣ n
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/Prime/Defs.lean:407, formal item exists_prime_and_dvd. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/Prime/Defs.lean#L407",
  "source_license": "Apache-2.0",
  "problem_family": "existence_of_prime_divisor",
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
      "/Users/sadiapeerzada/NLP-to-Formal-Language-Proof/data/curation_batches/v0.2.1/references_expanded.lean"
    ],
    "theorem_sha256": "40fdb2486c2e022d3850da2ed392590ab33b944fb4951c3a90114b6cb4357f63",
    "reference_code_sha256": "41de15c3452d8a80e7d8b3891efe14dc98082bf684403c6fe6873906808387b4",
    "verification_source_sha256": "45272f1c1eb3e1591fb15a57a854f4685b2dd191caee4a9918195ddab77d7ccf",
    "axiom_dependencies": [
      "propext",
      "Classical.choice",
      "Quot.sound"
    ],
    "evidence": "data/curation_batches/v0.2.1/verification_expanded.json; overall exit 0, zero error/malformed diagnostics, explicit per-theorem axiom inspection; no placeholder proofs."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `f0dd26658ce5b8c806d392cb746dcfbdd46c707278df3b4d782515f423a97903`. Fill `lib_d_prime_factor_exists.decision.json`; do not edit source fields.

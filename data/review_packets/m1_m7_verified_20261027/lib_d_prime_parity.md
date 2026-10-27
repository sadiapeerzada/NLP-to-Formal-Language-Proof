# lib_d_prime_parity: independent review

## English statement

```text
Every natural prime is either two or odd.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_d_prime_parity (p : ℕ) (hp : p.Prime) : p = 2 ∨ Odd p
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (p",
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/Prime/Basic.lean:41, formal item Prime.eq_two_or_odd. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/Prime/Basic.lean#L41",
  "source_license": "Apache-2.0",
  "problem_family": "prime_parity_dichotomy",
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
    "theorem_sha256": "ca87691f752f40ae8e7bb7708d89bf455e2b03c96c697174c29dae245247c490",
    "reference_code_sha256": "4edf440e65aeb71716487130e20975d1f3a7c24954312ad82fd27dae75332cb6",
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

Binding SHA-256: `efd8fcc4ddb6ed1be2d2a55c74244394eab4073bf8fc7329e1471796c4b10038`. Fill `lib_d_prime_parity.decision.json`; do not edit source fields.

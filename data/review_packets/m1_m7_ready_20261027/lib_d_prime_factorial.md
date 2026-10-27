# lib_d_prime_factorial: independent review

## English statement

```text
For a natural prime p and a natural number n, p divides n factorial if and only if p is at most n.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_d_prime_factorial (p n : ℕ) (hp : p.Prime) : p ∣ n.factorial ↔ p ≤ n
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (p n",
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/Prime/Factorial.lean:23, formal item Prime.dvd_factorial. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/Prime/Factorial.lean#L23",
  "source_license": "Apache-2.0",
  "problem_family": "prime_factorial_threshold",
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
    "theorem_sha256": "77571d97dfbf18c92274a848ae551b6b1a4f238641f5382e873e361f2fb23e52",
    "reference_code_sha256": "b9849ebe146ebe6d3645ef65a828ea83a6bfd7ec42ab62e3ced6f69f86ee7377",
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

Binding SHA-256: `66930f2d5c8e55e8a47930532d8b235bd4cedbeb74113adaf257958d7267e4e5`. Fill `lib_d_prime_factorial.decision.json`; do not edit source fields.

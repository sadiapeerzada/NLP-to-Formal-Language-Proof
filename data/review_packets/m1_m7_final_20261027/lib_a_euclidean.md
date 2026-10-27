# lib_a_euclidean: independent review

## English statement

```text
For any integers a and b, the remainder of a upon division by b plus b times the integer quotient equals a, including when b is zero.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_a_euclidean (a b : ℤ) : a % b + b * (a / b) = a
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (a b",
  "required_imports": [
    "Mathlib"
  ],
  "category": "arithmetic_identity",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover/lean4 at 8c9756b28d64dab099da31a4c09229a9e6a2ef35, Init/Data/Int/DivMod/Bootstrap.lean:100, formal item emod_add_mul_ediv. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover/lean4/blob/8c9756b28d64dab099da31a4c09229a9e6a2ef35/src/lean/Init/Data/Int/DivMod/Bootstrap.lean#L100",
  "source_license": "Apache-2.0",
  "problem_family": "integer_euclidean_reconstruction",
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
    "theorem_sha256": "74281691c6cc2b1f05b75f9d7cf3351ac0a6e5eb4d348444f7b7bfe00e376634",
    "reference_code_sha256": "82c915e1e2b44863ff115f481e9bb5d0a31550a85d86ec079bef53625919b66e",
    "verification_source_sha256": "7b116ce104b59338fdcdf3e736fe4392c39b77f32db73dabef9afcd005680367",
    "axiom_dependencies": [
      "propext"
    ],
    "evidence": "data/curation_batches/v0.2.0/verification_expanded.json; overall exit 0, zero error/malformed diagnostics, explicit per-theorem axiom inspection; no placeholder proofs."
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `e22a12c675a15053544e3f4a57a0af04ee008a860feb7f480631147923fc25e7`. Fill `lib_a_euclidean.decision.json`; do not edit source fields.

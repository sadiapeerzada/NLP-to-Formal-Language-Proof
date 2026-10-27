# lib_a_truncated_sub: independent review

## English statement

```text
For natural numbers a and b with b at most a, adding b to a-b recovers a.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_a_truncated_sub (a b : ℕ) (h : b ≤ a) : a - b + b = a
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (a b",
  "required_imports": [
    "Mathlib"
  ],
  "required_definitions": null,
  "category": "arithmetic_identity",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover/lean4 at 8c9756b28d64dab099da31a4c09229a9e6a2ef35, Init/Data/Nat/Basic.lean:991, formal item sub_add_cancel. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover/lean4/blob/8c9756b28d64dab099da31a4c09229a9e6a2ef35/src/lean/Init/Data/Nat/Basic.lean#L991",
  "source_license": "Apache-2.0",
  "problem_family": "truncated_subtraction_recovery",
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
    "theorem_sha256": "ec027b77e1b1aa02acb541550fcb37543faf5246df39fe04e110c4efa6545e6b",
    "reference_code_sha256": "c874139ccffc2efad8fdf943a7922949ac0879fbec496cd78af602c8223f0f38",
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

Binding SHA-256: `82648b9dac9b53849272465798d2978ba5976c883df73899e9d129ef8ea86871`. Fill `lib_a_truncated_sub.decision.json`; do not edit source fields.

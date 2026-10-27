# lib_a_choose_symmetry: independent review

## English statement

```text
For natural numbers n and k with k at most n, choosing k objects from n gives the same binomial coefficient as choosing n-k objects.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_a_choose_symmetry (n k : ℕ) (h : k ≤ n) : n.choose k = n.choose (n - k)
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (n k",
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
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Data/Nat/Choose/Basic.lean:198, formal item choose_symm. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Data/Nat/Choose/Basic.lean#L198",
  "source_license": "Apache-2.0",
  "problem_family": "binomial_complement_symmetry",
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
    "theorem_sha256": "8308329c75a1fd70bbe6afe30faa1994a15c0cebb39a06931cac7e76cc25ed91",
    "reference_code_sha256": "bb652552549d111d6d490ed7151d5c118e01dc55d55d002112001059606a5156",
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

Binding SHA-256: `d1896559928a98aa125e6c3e8c9786a312cb5e532090d86f04e4331d9d7be5cb`. Fill `lib_a_choose_symmetry.decision.json`; do not edit source fields.

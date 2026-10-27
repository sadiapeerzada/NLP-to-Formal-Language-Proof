# lib_m_wilson: independent review

## English statement

```text
For a natural prime p, the factorial of p-1 equals minus one in the ring of integers modulo p.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_m_wilson (p : ℕ) [Fact p.Prime] : ((p - 1).factorial : ZMod p) = -1
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (p",
  "required_imports": [
    "Mathlib"
  ],
  "required_definitions": null,
  "category": "modular_arithmetic",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/NumberTheory/Wilson.lean:43, formal item wilsons_lemma. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/NumberTheory/Wilson.lean#L43",
  "source_license": "Apache-2.0",
  "problem_family": "wilson_factorial_congruence",
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
    "theorem_sha256": "3d23e6905936c1662a9d6c05461022f37c4eef9ae902c4db8b27c9742e7bd4fc",
    "reference_code_sha256": "087a726be6792bde3d7b9eb8bac759b83cef071e9201084df6e427079b01b615",
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

Binding SHA-256: `c6ff509cada4cadf15ba0397484ed32e235738e8b6fe484cd3b828c8ae26a3f9`. Fill `lib_m_wilson.decision.json`; do not edit source fields.

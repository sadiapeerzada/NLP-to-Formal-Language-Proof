# lib_q_rearrangement: independent review

## English statement

```text
For real numbers a≤b and c≤d, a*d+b*c is at most a*c+b*d.
```

## Lean reference

```lean
open scoped BigOperators
theorem study_q_rearrangement (a b c d : ℝ) (hab : a ≤ b) (hcd : c ≤ d) : a * d + b * c ≤ a * c + b * d
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": "Exact binders/hypotheses: (a b c d",
  "required_imports": [
    "Mathlib"
  ],
  "required_definitions": null,
  "category": "inequality",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": "leanprover-community/mathlib4 at 81a5d257c8e410db227a6665ed08f64fea08e997, Mathlib/Algebra/Order/Ring/Unbundled/Basic.lean:294, formal item mul_add_mul_le_mul_add_mul. English is a new author-assisted paraphrase/adaptation, not a source quotation.",
  "source_url": "https://github.com/leanprover-community/mathlib4/blob/81a5d257c8e410db227a6665ed08f64fea08e997/Mathlib/Algebra/Order/Ring/Unbundled/Basic.lean#L294",
  "source_license": "Apache-2.0",
  "problem_family": "two_term_rearrangement",
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
    "theorem_sha256": "b25f77f78bc14bb1439dca4960c21a0b26fd2b32293980e8f1edc5ab0ad53b17",
    "reference_code_sha256": "58f4dd27a1b424e26fb52e443b7e7305fe70df2d00690ea04ec6d0807423fc2f",
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

Binding SHA-256: `24f3ca3b4e5059f3366dad31a91ebce1cab2055617a11e259e8add71f0867424`. Fill `lib_q_rearrangement.decision.json`; do not edit source fields.

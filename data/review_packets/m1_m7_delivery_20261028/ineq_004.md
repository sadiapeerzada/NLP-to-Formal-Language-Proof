# ineq_004: independent review

## English statement

```text
Prove that n + 3 < n + 7 for all values of n ∈ ℕ. You can do this proof with algebra (without induction), but the goal of this exercise is to write out a valid induction proof.
```

## Lean reference

```lean
theorem add_three_lt_add_seven (n : ℕ) : n + 3 < n + 7
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": null,
  "required_imports": null,
  "required_definitions": null,
  "category": "inequality",
  "difficulty": 1
}
```

## Source and proof evidence

```json
{
  "source_citation": "Levin, Oscar. Discrete Mathematics: An Open Introduction, 3rd ed., 5th printing, exercise 2.5.13, section 2.5, printed p. 189, University of Northern Colorado.",
  "source_url": "https://discrete.openmathbooks.org/pdfs/dmoi3-tablet.pdf",
  "source_license": "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)",
  "problem_family": "linear_inequality_by_induction",
  "split": "development",
  "theorem_verification": {
    "status": "verified",
    "success": true,
    "lean_toolchain": "leanprover/lean4:v4.32.0",
    "mathlib_revision": "81a5d257c8e410db227a6665ed08f64fea08e997",
    "command": "cd lean_project && lake env lean ../data/curation_batches/v0.1.2/ineq_004_linear_inequality.lean",
    "theorem_sha256": "4e211a2bdbb298f2e60e1c74bf395df4ca3a9bf5f0a84a22bf8efcd7371b0cc7",
    "evidence": "Repository strict verifier succeeded; exit_code=0; axiom_dependencies=[\"propext\", \"Quot.sound\"]; verification_source_sha256=c279934855ee88f2e042de13d558c0f9cd8993d65a9bdf6b58a8784650fa0874. Full record in data/curation_batches/v0.1.2/verification.log.",
    "strict_verifier_timeout_seconds": 180
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `b6d81a3fe37fc835b20a595f62ebf94dd628f45af7cfd05582e7818edda9c4f5`. Fill `ineq_004.decision.json`; do not edit source fields.

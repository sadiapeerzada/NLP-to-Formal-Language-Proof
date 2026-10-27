# arith_005: independent review

## English statement

```text
Explain why the binomial coefficient “n choose 0” equals 1 and the binomial coefficient “n choose n” equals 1.
```

## Lean reference

```lean
theorem choose_zero_and_self (n : ℕ) : Nat.choose n 0 = 1 ∧ Nat.choose n n = 1
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": null,
  "required_imports": null,
  "category": "arithmetic_identity",
  "difficulty": 1
}
```

## Source and proof evidence

```json
{
  "source_citation": "Levin, Oscar. Discrete Mathematics: An Open Introduction, 3rd ed., 5th printing, example 1.4.2, section 1.4, printed p. 92, University of Northern Colorado.",
  "source_url": "https://discrete.openmathbooks.org/pdfs/dmoi3-tablet.pdf",
  "source_license": "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)",
  "problem_family": "binomial_coefficient_boundary_values",
  "split": "development",
  "theorem_verification": {
    "status": "verified",
    "success": true,
    "lean_toolchain": "leanprover/lean4:v4.32.0",
    "mathlib_revision": "81a5d257c8e410db227a6665ed08f64fea08e997",
    "command": "cd lean_project && lake env lean ../data/curation_batches/v0.1.4/arith_005_binomial_boundary_values.lean",
    "theorem_sha256": "c500d07706cc31193ffc87b4d639d9d873b5dce2965cff1ffef62bef5055a851",
    "evidence": "Repository strict verifier succeeded; exit_code=0; axiom_dependencies=[\"propext\", \"Classical.choice\", \"Quot.sound\"]; verification_source_sha256=1a3c0db6d132e53da0c2359bbb3bcc88c3fe006dad8b6e1c29b80fb262091173. Full record in data/curation_batches/v0.1.4/verification.log.",
    "strict_verifier_timeout_seconds": 180
  }
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `834c00b9aba3ca343d6cb003f5baa880085ee8a5d371a804f3d899aeb4996114`. Fill `arith_005.decision.json`; do not edit source fields.

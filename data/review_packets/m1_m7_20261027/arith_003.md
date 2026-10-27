# arith_003: independent review

## English statement

```text
For any natural numbers a, b, and c, a times (b plus c) equals a times b plus a times c.
```

## Lean reference

```lean
theorem mul_distrib_left (a b c : ℕ) : a * (b + c) = a * b + a * c
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
  "source_citation": null,
  "source_url": null,
  "source_license": null,
  "problem_family": "nat_distributivity",
  "split": "development",
  "theorem_verification": null
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `dd09e4741d47e5ecdcdbfb33e8afae3bcb89202283d588f2dd0f3ec3895b1027`. Fill `arith_003.decision.json`; do not edit source fields.

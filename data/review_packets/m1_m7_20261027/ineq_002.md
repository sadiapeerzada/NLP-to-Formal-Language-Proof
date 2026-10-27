# ineq_002: independent review

## English statement

```text
For any natural numbers a and b, a times b plus 1 is at most (a+1) times (b+1).
```

## Lean reference

```lean
theorem prod_succ_ge (a b : ℕ) : a * b + 1 ≤ (a + 1) * (b + 1)
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": null,
  "required_imports": null,
  "category": "inequality",
  "difficulty": 1
}
```

## Source and proof evidence

```json
{
  "source_citation": null,
  "source_url": null,
  "source_license": null,
  "problem_family": "nat_product_bound",
  "split": "development",
  "theorem_verification": null
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `838e2d638cfa5eadd14a4c233fbe44530ef0a6a77532b55f8f013bc9484396df`. Fill `ineq_002.decision.json`; do not edit source fields.

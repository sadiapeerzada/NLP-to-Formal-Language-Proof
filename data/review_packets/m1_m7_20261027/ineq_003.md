# ineq_003: independent review

## English statement

```text
For any natural number n at least 1, n plus 1 is at most 2 to the power n.
```

## Lean reference

```lean
theorem succ_le_two_pow (n : ℕ) (h : 1 ≤ n) : n + 1 ≤ 2 ^ n
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": null,
  "required_imports": null,
  "category": "inequality",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": null,
  "source_url": null,
  "source_license": null,
  "problem_family": "nat_power_growth",
  "split": "development",
  "theorem_verification": null
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `a3952189e7e984b9ba8861eebac89c44127ded4e7e601db865f6bfcda91f4a7a`. Fill `ineq_003.decision.json`; do not edit source fields.

# arith_002: independent review

## English statement

```text
For any natural numbers a and b, a squared minus b squared equals (a + b) times (a - b), assuming a is at least b.
```

## Lean reference

```lean
theorem sq_sub_sq_nat (a b : ℕ) (h : b ≤ a) : a ^ 2 - b ^ 2 = (a + b) * (a - b)
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": null,
  "required_imports": null,
  "category": "arithmetic_identity",
  "difficulty": 2
}
```

## Source and proof evidence

```json
{
  "source_citation": null,
  "source_url": null,
  "source_license": null,
  "problem_family": "nat_square_identities",
  "split": "development",
  "theorem_verification": null
}
```

## Reviewer instructions

Check quantifiers, types, boundaries, notation, necessary and extra assumptions, self-containment, source adaptation, category/difficulty, family and split. Choose faithful / not faithful / uncertain. Record your actual identity, date, independence declaration, explanation, and a signed or otherwise verifiable decision artifact. Leave unreviewed items blank. Do not infer faithfulness from compilation or the supplied reference proof.

Binding SHA-256: `5c1d1d7a37640934ea38567b0c4dc8045f4e94b82c5bf28af4dab9a3a633bc2c`. Fill `arith_002.decision.json`; do not edit source fields.

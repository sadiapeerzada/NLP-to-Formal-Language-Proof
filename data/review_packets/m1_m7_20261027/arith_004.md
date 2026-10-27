# arith_004: independent review

## English statement

```text
For natural numbers a and b with b at most a, (a minus b) squared plus 2ab equals a squared plus b squared.
```

## Lean reference

```lean
theorem sq_sub_nat (a b : ℕ) (h : b ≤ a) : (a - b) ^ 2 + 2 * a * b = a ^ 2 + b ^ 2
```

## Quantifiers, assumptions and definitions

Read every explicit/implicit binder and typeclass in the theorem above. Compare its domains, existence/uniqueness, hypotheses and conclusion to English. The metadata below are author-assisted preparation, not reviewer findings.

```json
{
  "mathematical_assumptions": null,
  "required_imports": null,
  "category": "arithmetic_identity",
  "difficulty": 3
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

Binding SHA-256: `38acebab47cd6a890bb415e58ff1b05be795aceb12c7d48359b95fb2b8884ef5`. Fill `arith_004.decision.json`; do not edit source fields.

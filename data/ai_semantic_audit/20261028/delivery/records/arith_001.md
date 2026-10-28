# arith_001: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For any natural numbers a and b, (a + b) squared equals a squared plus 2ab plus b squared.
```

## Lean type

```lean
theorem add_sq_nat (a b : ℕ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Two universal natural inputs; polynomial expansion preserves every term and coefficient without extra hypotheses."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "arith_001",
  "theorem": "AuditReference0.add_sq_nat",
  "source": "data/reference_verification/v0.1.0/references.lean",
  "expected_type": "∀ (a b : ℕ), (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2",
  "axioms": [
    "propext"
  ],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "arith_001",
  "subject_sha256": "479fb3f939b02aeaca2df50f3b7e8e5a5c82c8fd61d33091b6a9fc14008ba89e",
  "kind": "exact_bounded_probe",
  "checked_assignments": 81,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Polynomial identity on all pairs 0..8.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 18 column 1 (char 981)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "universal quantification over ℕ for a and b",
  "domains": "ℕ for a and b",
  "assumptions": "none specified, default to natural numbers",
  "equivalence": "the provided English statement is not equivalent to the formalized Lean theorem",
  "strength": "the English statement is a weaker claim, lacking the squared term for (a + b)",
  "boundary_cases": "not specified, but zero and negative cases should be considered for completenency",
  "counterexample_search": "no counterexample needed as the English statement is incorrect",
  "explanation": "the English statement lacks the squared terms for (a + b) and for a and b, which are essential for the correct formula",
  "issues": [
    "omission of squared terms in the English statement",
    "lack of equivalence to the formalized Lean theorem",
    "missing squared terms for the binomial expansion",
    "absence of consideration for zero and negative values of a and b"
  ]
}
```

The English statement provided does not accurately represent the formalized Lean theorem because it omits the squared terms for (a + b) and a and b. The correct formula, as stated in the Lean theorem, includes these squared terms, which are essential for the binomial expansion (a + b)^2 = a^2 + 2ab + b^2. The English statement, therefore, does not match the mathematical content of the Lean theorem and is considered a weaker claim. There is no need for a counterexample as the English statement is inherently incorrect, and the discrepancy lies in the omission of critical mathematical components.

```json
{
  "label": "not faithful",
  "quantifiers": "universal quantification over ℕ for a and b",
  "domains": "ℕ for a and b",
  "assumptions": "none, default to natural numbers",
  "equivalence": "the provided English statement is not equivalent to the formalized Lean theorem",
  "strength": "the English statement is a weaker claim, lacking the squared terms for (a + b) and a and b",
  "boundary_cases": "absence of consideration for zero and negative cases",
  "counterexample_search": "no counterexample needed as the English statement is inherently incorrect",
  "explanation": "the English statement lacks the squared terms for (a + b) and for a and b, which are essential for the correct formula",
  "issues": [
    "omission of squared terms in the English statement",
    "lack of equivalence to the formalized Lean theorem",
    "missing squared terms for the binomial expansion",
    "absence of consideration for zero and negative values of a and b"
  ]
}
```
````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and the Lean theorem provided are equivalent in terms of mathematical meaning. Both assert that the square of the sum of two natural numbers equals the sum of the squares of the individual numbers plus twice the product of the numbers. This is a statement of the algebraic identity (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2, which is true for any natural numbers a and b. There are no omitted domain restrictions, and the statement is equivalent in strength to the Lean theorem provided.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and the Lean theorem provided are equivalent in terms of mathematical meaning. Both assert that the square of the sum of two natural numbers equals the sum of the squares of the individual numbers plus twice the product of the numbers. This is a statement of the algebraic identity (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2, which is true for any natural numbers a and b. There are no omitted domain restrictions, and the statement is equivalent in strength to the Lean theorem provided.",
  "issues": []
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


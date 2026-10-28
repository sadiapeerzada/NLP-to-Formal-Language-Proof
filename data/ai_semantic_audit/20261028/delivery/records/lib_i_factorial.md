# lib_i_factorial: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every natural number n, (n+1) factorial equals (n+1) times n factorial.
```

## Lean type

```lean
open scoped BigOperators
theorem study_i_factorial (n : ℕ) : (n + 1).factorial = (n + 1) * n.factorial
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal natural n; successor factorial equals successor times factorial, including n=0."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_i_factorial",
  "theorem": "AuditReference14.study_i_factorial",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (n : ℕ), (n + 1).factorial = (n + 1) * n.factorial",
  "axioms": [],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "lib_i_factorial",
  "subject_sha256": "5ef6d97bd334cf52c2558635f25a80cde3984ebb541d06cd23a5ffb8514f6e7e",
  "kind": "exact_bounded_probe",
  "checked_assignments": 9,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Zero endpoint.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 18 column 1 (char 1005)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "universal quantifier on n, existential quantifier on n+1",
  "domains": "ℕ, BigOperators",
  "assumptions": "n is a natural number, factorial is defined for natural numbers",
  "equivalence": "the English proposition does not account for the base case of n=0, where (0+1)! = 1, not equal to (0+1)*0! as suggested",
  "strength": "the English proposition suggests a stronger relationship than the Lean theorem",
  "boundary_cases": "n=0 case is not addressed",
  "counterexample_search": "n=0, where the English proposition fails",
  "explanation": "The English proposition implies that the product (n+1)*n! is always equal to (n+1)!, but this is not true for n=0 due to the factorial definition of 0! being 1.",
  "issues": [
    "Base case of n=0 not addressed",
    "Implicit assumption that n+1 is always natural",
    "Lack of clarity on factorial definition for 0",
    "English proposition suggests a stronger relationship than the Lean theorem"
  ]
}
```

The English proposition is "not faithful" to the Lean theorem because it fails to account for the base case of n=0, which is essential for the factorial definition. The Lean theorem correctly states that for every natural number n, (n+1)! equals (n+1) times n!. However, the English proposition incorrectly extends this to the case of n=0, where it would suggest that (0+1)! equals (0+1)*0!, which is not true since 0! is defined to be 1. The English proposition thus implies a stronger relationship than what is captured by the Lean theorem, and this discrepency is highlighted by the counterexample of n=0.

```json
{
  "label": "not faithful",
  "quantifiers": "universal quantifier on n, existential quantifier on n+1",
  "domains": "ℕ, BigOperators",
  "assumptions": "n is a natural number, factorial is defined for natural numbers",
  "equivalence": "the English proposition suggests a stronger relationship than the Lean theorem",
  "strength": "the English proposition implies a stronger relationship than the Lean theorem",
  "boundary_cases": "n=0 case is not addressed",
  "counterexample_search": "n=0, where the English proposition fails",
  "explanency": "The English proposition fails to consider the special case of n=0, where the factorial definition differs from the general rule stated.",
  "issues": [
    "Base case of n=0 not addressed",
    "Implicit assumption that n+1 is always natural",
    "Lack of clarity on factorial definition for 0",
    "English proposition suggests a stronger relationship than the Lean theorem"
  ]
}
```
````


## Phi-4-mini actual judgment

```json
null
```

Schema error: issues must be a string list

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "one each on sides",
  "domains": "ℕ",
  "assumptions": "none",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "none",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement and Lean theorem are equivalent in meaning and scope. Both assert that the factorial of n+1 is equal to (n+1) multiplied by n factorial for every natural number n. There are no omitted domain restrictions, and the statement is direct and clear in its equivalence."
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Phi-4 response quality: Frozen schema parse failed; no accepted judgment.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


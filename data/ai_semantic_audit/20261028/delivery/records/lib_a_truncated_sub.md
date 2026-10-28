# lib_a_truncated_sub: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural numbers a and b with b at most a, adding b to a-b recovers a.
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_truncated_sub (a b : ℕ) (h : b ≤ a) : a - b + b = a
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural a,b, b<=a premise and (a-b)+b=a conclusion match; the premise avoids truncation loss."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_truncated_sub",
  "theorem": "AuditReference14.study_a_truncated_sub",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b : ℕ) (h : b ≤ a), a - b + b = a",
  "axioms": [
    "propext"
  ],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "lib_a_truncated_sub",
  "subject_sha256": "99c5cc45c87cf7dbfc9f3f15ea111cb2ae89e740b86f6b95445573b8f4e04ce0",
  "kind": "exact_bounded_probe",
  "checked_assignments": 45,
  "filtered_by_assumptions": 36,
  "failures": [],
  "note": "b<=a required.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 19 column 1 (char 1069)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "universal quantifier for a and b, existential quantifier for h",
  "domains": "ℕ (natural numbers)",
  "assumptions": "b ≤ a",
  "equivalence": "not equivalent to the expected formalization",
  "strength": "omits consideration of boundary cases",
  "boundary_cases": "does not address the case when b = a",
  "counterexample_search": "b = a, h is trivially true",
  "explanency": "the provided JSON lacks necessary definitions and formalizes the statement insufficiently",
  "issues": [
    "The statement lacks formalization of the hypothesis and conclusion.",
    "The domain of b is not restricted to natural numbers, potentially including zero.",
    "The statement does not account for the case when b equals a, which is crucial for the property being discussed.",
    "The formalization does not use Lean's BigOperators or Mathlib's totalized operations, limiting its correctness.",
    "The statement does not address the case when b is zero, which could lead to undefined behavior in arithmetic operations."
  ]
}
```



```json
{
  "label": "not faithful",
  "quantifiers": "universal quantifier for a and b, existential quantifier for h",
  "domains": "ℕ (natural numbers excluding zero)",
  "assumptions": "b ≤ a",
  "equivalence": "not equivalent to the expected formalization",
  "strength": "omits consideration of boundary cases",
  "boundary_cases": "does not address the case when b = a",
  "counterexample_search": "b = a, h is trivially true",
  "explanency": "The provided JSON lacks necessary definitions and formalizes the statement insufficiently, missing key elements for a correct formalization in Lean.",
  "issues": [
    "The statement lacks formalization of the hypothesis and conclusion.",
    "The domain of b is not restricted to natural numbers, potentially including zero.",
    "The statement does not account for the case when b equals a, which is crucial for the property being discussed.",
    "The formalization does not use Lean's BigOperators or Mathlib's totalized operations, limiting its correctness.",
    "The statement does not address the case when b is zero, which could lead to undefined behavior in arithmetic operations."
  ]
}
```



```json
{
  "label": "not faithful",
  "quantifiers": "universal quantifier for a and b, existential quantifier for h",
    "domains": "ℕ (natural numbers excluding zero)",
    "assumptions": "b ≤ a",
    "equivalence": "not equivalent to the expected formalization",
    "strength": "omits consideration of boundary cases",
    "boundary_cases": "does not address the case when b = a",
    "counterexample_search": "b = a, h is trivially true",
    "explanency": "The provided JSON lacks necessary definitions and formalizes the statement insufficiently, missing key elements for a correct formalization in Lean.",
    "issues": [
      "The statement lacks formalization of the hypothesis and conclusion.",
      "The domain of b is not restricted to natural numbers, potentially including zero.",
      "The statement does not account for the case when b equals a, which is crucial for the property being discussed.",
      "The formalization does not use Lean's BigOperators or Mathlib's totalized operations, limiting its correctness.",
      "The statement does not address the case when b is zero, which could lead to undefined behavior in arithmetic operations."
    ]
  }
}
```



```json
{
  "label": "not faithful
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
  "quantifiers": "one each",
  "domains": "ℕ",
  "assumptions": "h : b ≤ a",
  "equivalence": "conclusion a - b + b = a",
  "strength": "same",
  "boundary_cases": "a = 0, a = b",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and Lean theorem are equivalent in meaning. The English statement asserts that for natural numbers a and b where b is less than or equal to a, the operation a - b + b recovers a. This is directly translated into a Lean theorem stating that a - b + b equals a under the assumption h : b ≤ a. There are no boundary cases that invalidate this statement as subtraction and addition of natural numbers are well-defined operations in this context. There is no counterexample that refutes this statement as it is a fundamental property of subtraction in the set of natural numbers. The statement is faithful to the expected Lean statement as they are equivalent in meaning and scope."
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


# arith_004: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural numbers a and b with b at most a, (a minus b) squared plus 2ab equals a squared plus b squared.
```

## Lean type

```lean
theorem sq_sub_nat (a b : ℕ) (h : b ≤ a) : (a - b) ^ 2 + 2 * a * b = a ^ 2 + b ^ 2
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural a,b and b<=a explicitly match; subtraction-square identity retains 2ab, which differs from twice (a-b)b."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "arith_004",
  "theorem": "AuditReference0.sq_sub_nat",
  "source": "data/reference_verification/v0.1.0/references.lean",
  "expected_type": "∀ (a b : ℕ) (h : b ≤ a), (a - b) ^ 2 + 2 * a * b = a ^ 2 + b ^ 2",
  "axioms": [
    "propext",
    "Classical.choice",
    "Quot.sound"
  ],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "arith_004",
  "subject_sha256": "2ad9fe3d356c5287c01d8350c25394df4bb31f15004666e34347b3f2338c04b2",
  "kind": "exact_bounded_probe",
  "checked_assignments": 45,
  "filtered_by_assumptions": 36,
  "failures": [],
  "note": "Truncation under b<=a.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 17 column 1 (char 1008)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "universal quantifier on a and b, existential quantifier on h",
  "domains": "ℕ, h: ℕ → Prop",
  "assumptions": "b ≤ a",
  "equivalence": "the proposition is not equivalent to the expected Lean theorem",
  "strength": "the expected theorem is stronger as it accounts for the case when b = a",
  "boundary_cases": "the case when b = a is not considered in the expected theorem",
  "counterexample_search": "b = a, h is trivially true",
  "explanation": "The expected theorem omits the case when b equals a, which is present in the original statement and affects the equality.",
  "issues": [
    "The expected theorem does not account for the case when b equals a, leading to an incorrect formalization.",
    "The original statement implies b ≤ a, but the expected theorem allows for equality, which changes the equation.",
    "The expected theorem lacks the case when b is greater than a, which is also a valid interpretation of the original statement."
  ]
}
```
````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each on left and right",
  "domains": "ℕ",
  "assumptions": "h : b ≤ a",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "specific endpoint check a = b",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The statement is an application of the square of a difference expanded identity and is true for natural numbers a and b where b is less than or equal to a.",
  "issues": [
    "The English statement uses 'squared' which implies a power of 2, but the Lean statement uses the exponentiation operator ^ which is consistent with the definition of power in Lean.",
    "The English statement uses 'equals' while the Lean statement uses '=', which are equivalent notations in different contexts.",
    "The English statement uses 'two ab' while the Lean statement uses '2 * a * b', which are equivalent notations but use different spacing.",
    "The English statement uses 'at most a' while the Lean statement uses '≤ a', which are equivalent notations but use different spacing.",
    "The English statement uses 'squared' while the Lean statement uses the exponentiation operator ^ which is consistent with the definition of power in Lean.",
    "The English statement uses 'two ab' while the Lean statement uses '2 * a * b', which are equivalent notations but use different spacing.",
    "The English statement uses 'at most a' while the Lean statement uses '≤ a', which are equivalent notations but use different spacing."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "one each on left and right",
  "domains": "ℕ",
  "assumptions": "h : b ≤ a",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "specific endpoint check a = b",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The statement is an application of the square of a difference expanded identity and is true for natural numbers a and b where b is less than or equal to a.",
  "issues": [
    "The English statement uses 'squared' which implies a power of 2, but the Lean statement uses the exponentiation operator ^ which is consistent with the definition of power in Lean.",
    "The English statement uses 'equals' while the Lean statement uses '=', which are equivalent notations in different contexts.",
    "The English statement uses 'two ab' while the Lean statement uses '2 * a * b', which are equivalent notations but use different spacing.",
    "The English statement uses 'at most a' while the Lean statement uses '≤ a', which are equivalent notations but use different spacing.",
    "The English statement uses 'squared' while the Lean statement uses the exponentiation operator ^ which is consistent with the definition of power in Lean.",
    "The English statement uses 'two ab' while the Lean statement uses '2 * a * b', which are equivalent notations but use different spacing.",
    "The English statement uses 'at most a' while the Lean statement uses '≤ a', which are equivalent notations but use different spacing."
  ]
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Phi-4 response quality: Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


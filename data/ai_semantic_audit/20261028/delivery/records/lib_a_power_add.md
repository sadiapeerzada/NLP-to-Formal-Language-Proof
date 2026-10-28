# lib_a_power_add: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural numbers a, m and n, a raised to m+n equals a raised to m times a raised to n.
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_power_add (a m n : ℕ) : a ^ (m + n) = a ^ m * a ^ n
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural base and both natural exponents universally quantified; exponent sum and product order match, including 0^0."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_power_add",
  "theorem": "AuditReference14.study_a_power_add",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a m n : ℕ), a ^ (m + n) = a ^ m * a ^ n",
  "axioms": [
    "propext"
  ],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "lib_a_power_add",
  "subject_sha256": "368ec042e98c1e478e7fca733b61fcff362f5b6bfaa0d66f94a5261e0d89b4d6",
  "kind": "exact_bounded_probe",
  "checked_assignments": 125,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Includes 0^0=1.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 17 column 1 (char 1089)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "uncertain",
  "quantifiers": "universal quantification over ℕ for a, m, n",
  "domains": "natural numbers for a, m, n",
  "assumptions": "no additional assumptions required",
  "equivalence": "not explicitly stated, thus cannot be assumed to be equivalent",
  "strength": "the Lean theorem does not account for zero or negative exponents, which are relevant to the natural number domain",
  "boundary_cases": "excludes cases where m or n is zero, potentially affecting the theorem'才 validity",
  "counterexample_search": "no concrete counterexample provided, but zero exponents could serve as a boundary case",
  "explanation": "the Lean theorem formalizes exponentiation for natural numbers but lacks consideration for zero and negative exponents, which are part of the natural number domain and could affect the theorem's generality",
  "issues": [
    "omission of zero and negative exponents in the domain",
    "lack of clarity on handling zero exponents",
    "possible need for separate theorems or extensions for complete coverage of the natural number domain"
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

```text
{
  "label": "faithful",
  "quantifiers": "m and n",
  "domains": "ℕ",
  "assumptions": "a is a natural number",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "none",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement and Lean theorem are equivalent in meaning and scope. Both assert that a raised to the sum of m and n equals a raised to m times a raised to n for natural numbers a, m and n. There is no difference in the scope of the quantifiers, the variable domains, or the assumptions. The conclusion in both is equivalent. There is no counterexample that refutes either statement."
}
```


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


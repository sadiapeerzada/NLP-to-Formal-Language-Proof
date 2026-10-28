# lib_q_reciprocal: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
If real numbers x and y satisfy 0<x and x≤y, then 1/y≤1/x.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_reciprocal (x y : ℝ) (hx : 0 < x) (hxy : x ≤ y) : 1 / y ≤ 1 / x
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Real 0<x<=y ensures y positive; reciprocal inequality reverses order exactly as stated."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_reciprocal",
  "theorem": "AuditReference14.study_q_reciprocal",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x y : ℝ) (hx : 0 < x) (hxy : x ≤ y), 1 / y ≤ 1 / x",
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
  "candidate_id": "lib_q_reciprocal",
  "subject_sha256": "0bcd24396c036c18d8135298aa8c5df906dc25f0964d43f361085c2d6f906fdb",
  "kind": "exact_bounded_probe",
  "checked_assignments": 21,
  "filtered_by_assumptions": 148,
  "failures": [],
  "note": "0<x<=y ensures both denominators nonzero.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 27 column 1 (char 791)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "uncertain",
  "quantifiers": {
    "subject": "∀x ∈ ℝ, ∃y ∈ ℝ such that 0 < x ∧ x ≤ y and 1/y ≤ ized 1/x",
    "lean": "∀x ∈ ℝ, ∃y ∈ ℝ such that 0 < x ∧ x ≤ y ∧ 1 / y ≤ 1 / x"
  },
  "domains": {
    "subject": "real numbers",
    "lean": "real numbers"
  },
  "assumptions": {
    "subject": "x > 0 and x ≤ y",
    "lean": "0 < x ∧ x ≤ y"
  },
  "equivalence": "not equivalent",
  "strength": "the subject lacks explicit negation handling",
  "boundary_cases": "not addressed",
  "counterexample_search": "consider x = 0.1, y = 1; the subject fails",
  "explanation": "the subject does not account for x = 0 case or division by zero",
  "issues": [
    "implicit negation handling",
    "boundary cases",
    "division by zero",
    "missing assumptions for x > ized x"
  ]
}
```json
{
  "label": "uncertain",
  "quantifiers": {
    "subject": "For all x in the real numbers, there exists a y in the real numbers such that x is greater than 0 and less than or equal to y, and 1/y is less than or equal to 1/x.",
    "lean": "For all x in the real numbers, there exists a y in the real numbers such that 0 < x ∧ x ≤ y ∧ 1 / y ≤ 1 / x"
  },
  "domains": {
    "subject": "real numbers",
    "lean": "real numbers"
  },
  "assumptions": {
    "subject": "x is greater than 0 and less than or equal to y",
    "lean": "0 < x ∧ x ≤ y"
  },
  "equivalence": "the subject is not equivalent to the lean formalization due to handling of edge cases and assumptions",
  "strength": "the subject lacks explicit handling of cases where x is 0, potentially leading to incorrect conclusions",
  "boundary_cases": "the subject does not address what happens when x is 0 or when y is 0",
  "counterexample_search": "the subject fails when x = 0.1, y = 1, as it does not consider division by zero",
  "explanation": "the subject assumes x > 0 without explicitly stating this, which is a limitation when generalizing to all real numbers",
  "issues": [
    "implicit negation handling",
    "boundary cases",
    "division by zero",
    "missing assumptions for x > 0"
  ]
}
}
```
````


## Phi-4-mini actual judgment

```json
{
  "label": "not faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "stronger, than requested",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and Lean theorem are not equivalent due to different handling of division and remainders in Lean versus the expected statement. Lean Nat subtraction is truncated and division and remainders are totalized in Lean, which changes the scope and strength of the theorem.",
  "issues": [
    "Division and remainders handling",
    "Truncated Nat subtraction",
    "Totalization of division and remainders in Lean"
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "not faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "stronger, than requested",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and Lean theorem are not equivalent due to different handling of division and remainders in Lean versus the expected statement. Lean Nat subtraction is truncated and division and remainders are totalized in Lean, which changes the scope and strength of the theorem.",
  "issues": [
    "Division and remainders handling",
    "Truncated Nat subtraction",
    "Totalization of division and remainders in Lean"
  ]
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted.",
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


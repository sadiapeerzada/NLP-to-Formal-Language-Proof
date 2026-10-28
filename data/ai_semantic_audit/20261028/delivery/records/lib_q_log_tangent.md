# lib_q_log_tangent: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every positive real x, log(x) is at most x-1.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_log_tangent (x : ℝ) (hx : 0 < x) : Real.log x ≤ x - 1
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Positive real x premise avoids totalized negative-log interpretation; log(x)<=x-1 matches."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_log_tangent",
  "theorem": "AuditReference14.study_q_log_tangent",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x : ℝ) (hx : 0 < x), Real.log x ≤ x - 1",
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
  "candidate_id": "lib_q_log_tangent",
  "subject_sha256": "665ba75de89367ac0e80db2a97cd025556d90a4f26ebd95ef202d4186b9ca4b0",
  "kind": "approximate_numeric_probe",
  "checked_assignments": 6,
  "filtered_by_assumptions": 7,
  "failures": [],
  "note": "Positive inputs, floating log.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: No completed exploratory judgment: unattempted_reviewer_retired

Raw model response (untrusted, including any unsupported claims):

```text
No completed response. Consult the preserved retirement/journal/stream evidence.
```


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
  "explanation": "The English statement asserts a specific inequality for the logarithm function, while the Lean theorem statement does not explicitly limit the scope of x to positive real numbers. This makes the Lean statement potentially stronger than requested as it does not match the English statement's requirement that x must be greater than zero (x > 0).",
  "issues": [
    "The Lean theorem statement does not include the assumption that x is a positive real number (hx : 0 < x), which is required in the English statement."
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
  "explanation": "The English statement asserts a specific inequality for the logarithm function, while the Lean theorem statement does not explicitly limit the scope of x to positive real numbers. This makes the Lean statement potentially stronger than requested as it does not match the English statement's requirement that x must be greater than zero (x > 0).",
  "issues": [
    "The Lean theorem statement does not include the assumption that x is a positive real number (hx : 0 < x), which is required in the English statement."
  ]
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Exploratory model did not complete a review; no verdict exists.",
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


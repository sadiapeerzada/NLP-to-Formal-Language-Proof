# lib_a_log_product: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For nonzero real x and y, the totalized real logarithm of x*y equals log(x)+log(y), where Mathlib defines the logarithm using absolute values on negative inputs.
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_log_product (x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0) : Real.log (x * y) = Real.log x + Real.log y
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Nonzero real x,y and explicit Mathlib log-absolute convention avoid the usual positive-log restriction; both sign patterns are intentional."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_log_product",
  "theorem": "AuditReference14.study_a_log_product",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0), Real.log (x * y) = Real.log x + Real.log y",
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
  "candidate_id": "lib_a_log_product",
  "subject_sha256": "6984540ec472aa51544ed147d81ea4ab828294889135bb2bbf62be6dfd500085",
  "kind": "approximate_numeric_probe",
  "checked_assignments": 144,
  "filtered_by_assumptions": 25,
  "failures": [],
  "note": "Mathlib totalized log uses absolute value; nonzero inputs; floating.",
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
  "strength": "stronger, with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement assumes the logarithm is defined on negative numbers, while Mathlib uses absolute values on negative numbers, resulting in different behaviors and outcomes.",
  "issues": [
    "The English statement uses Real.log on negative numbers directly, while Mathlib defines Real.log on absolute values.",
    "The totalization of division and remainders in Lean may lead to different results than expected in the English statement."
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
  "strength": "stronger, with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement assumes the logarithm is defined on negative numbers, while Mathlib uses absolute values on negative numbers, resulting in different behaviors and outcomes.",
  "issues": [
    "The English statement uses Real.log on negative numbers directly, while Mathlib defines Real.log on absolute values.",
    "The totalization of division and remainders in Lean may lead to different results than expected in the English statement."
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


# lib_a_exp_add: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For all real x and y, exp(x+y)=exp(x)*exp(y).
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_exp_add (x y : ℝ) : Real.exp (x + y) = Real.exp x * Real.exp y
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal real x,y and real exponential addition identity match exactly."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_exp_add",
  "theorem": "AuditReference14.study_a_exp_add",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x y : ℝ), Real.exp (x + y) = Real.exp x * Real.exp y",
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
  "candidate_id": "lib_a_exp_add",
  "subject_sha256": "34a35427648663388d6cbeda71f96da710c336a3d1ec76d0e33a867928255758",
  "kind": "approximate_numeric_probe",
  "checked_assignments": 169,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Floating approximation only.",
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
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same, stronger, weaker, or ambiguous with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of real numbers and is equivalent to a Lean theorem stating that the exponential function is multiplicative over addition. This is a well-known property of real numbers and is equivalent in strength to the Lean statement provided.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same, stronger, weaker, or ambiguous with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of real numbers and is equivalent to a Lean theorem stating that the exponential function is multiplicative over addition. This is a well-known property of real numbers and is equivalent in strength to the Lean statement provided.",
  "issues": []
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Exploratory model did not complete a review; no verdict exists.",
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into strength. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


# lib_a_trig_unit: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every real x, sin(x)^2+cos(x)^2 equals one.
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_trig_unit (x : ℝ) : (Real.sin x) ^ 2 + (Real.cos x) ^ 2 = 1
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal real x; squared sine plus squared cosine equals one, with exponentiation applied to function values."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_trig_unit",
  "theorem": "AuditReference14.study_a_trig_unit",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x : ℝ), (Real.sin x) ^ 2 + (Real.cos x) ^ 2 = 1",
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
  "candidate_id": "lib_a_trig_unit",
  "subject_sha256": "1350d53a7f3fa950bcb606eb73a357bb8db316138a74f674fc29f585f57eebc9",
  "kind": "approximate_numeric_probe",
  "checked_assignments": 13,
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
  "quantifiers": "one each",
  "domains": "specific Real numbers",
  "assumptions": "specific Real numbers",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a fundamental trigonometric identity that is equivalent to a Lean theorem stating that for every real number x, the sum of the square of the sine of x and the square of the cosine of x equals one. This is a well-known and universally accepted trigonometric identity in mathematics. There is no counterexample that refutes this statement as it is true by definition in the Real numbers. The required import is Mathlib which provides the Real numbers and trigonometric functions. There is an implicit assumption that x is a Real number but it is not explicitly stated in the English statement as it is inherent in the mathematical context. The conclusion in Lean is equivalent to the English statement as it directly restates the trigonometric identity in formal notation.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "one each",
  "domains": "specific Real numbers",
  "assumptions": "specific Real numbers",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a fundamental trigonometric identity that is equivalent to a Lean theorem stating that for every real number x, the sum of the square of the sine of x and the square of the cosine of x equals one. This is a well-known and universally accepted trigonometric identity in mathematics. There is no counterexample that refutes this statement as it is true by definition in the Real numbers. The required import is Mathlib which provides the Real numbers and trigonometric functions. There is an implicit assumption that x is a Real number but it is not explicitly stated in the English statement as it is inherent in the mathematical context. The conclusion in Lean is equivalent to the English statement as it directly restates the trigonometric identity in formal notation.",
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
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


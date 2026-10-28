# lib_a_min_max: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For real x and y, their minimum plus their maximum equals their sum.
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_min_max (x y : ℝ) : min x y + max x y = x + y
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal real x,y; min plus max equals x+y, no strict-order assumption."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_min_max",
  "theorem": "AuditReference14.study_a_min_max",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x y : ℝ), min x y + max x y = x + y",
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
  "candidate_id": "lib_a_min_max",
  "subject_sha256": "341646e4638e20164f48df358e75e571ae0a68c5791e975801aca091f038a6c5",
  "kind": "exact_bounded_probe",
  "checked_assignments": 169,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Exact rational grid.",
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
  "quantifiers": "one each min and max",
  "domains": "specific ℝ",
  "assumptions": "specific x and y real numbers",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific min and max check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement implies a specific case where x and y are distinct and real numbers. However, the Lean theorem does not explicitly limit x and y to distinct values, potentially making it stronger than requested as it could hold for any real numbers x and y, not just distinct real numbers.",
  "issues": [
    "The Lean theorem does not explicitly require x and y to be distinct, which makes it stronger than the English statement implies."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "not faithful",
  "quantifiers": "one each min and max",
  "domains": "specific ℝ",
  "assumptions": "specific x and y real numbers",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific min and max check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement implies a specific case where x and y are distinct and real numbers. However, the Lean theorem does not explicitly limit x and y to distinct values, potentially making it stronger than requested as it could hold for any real numbers x and y, not just distinct real numbers.",
  "issues": [
    "The Lean theorem does not explicitly require x and y to be distinct, which makes it stronger than the English statement implies."
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
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


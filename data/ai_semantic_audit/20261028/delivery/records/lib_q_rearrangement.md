# lib_q_rearrangement: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For real numbers a≤b and c≤d, a*d+b*c is at most a*c+b*d.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_rearrangement (a b c d : ℝ) (hab : a ≤ b) (hcd : c ≤ d) : a * d + b * c ≤ a * c + b * d
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Four reals with a<=b,c<=d; cross products lie on the <= side and aligned products on the >= side, with equality cases allowed."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_rearrangement",
  "theorem": "AuditReference15.study_q_rearrangement",
  "source": "data/curation_batches/v0.2.1/references_expanded.lean",
  "expected_type": "∀ (a b c d : ℝ) (hab : a ≤ b) (hcd : c ≤ d), a * d + b * c ≤ a * c + b * d",
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
  "candidate_id": "lib_q_rearrangement",
  "subject_sha256": "8ee576dffb87e729aa539e765d426d081158fce1b9c08e65538571f5b1402f41",
  "kind": "exact_bounded_probe",
  "checked_assignments": 225,
  "filtered_by_assumptions": 400,
  "failures": [],
  "note": "Ordering hypotheses orient inequality.",
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
  "strength": "stronger, or ambiguous with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement suggests a less restrictive inequality than that implied by the Lean theorem due to the omission of a domain restriction on a and b. This makes the Lean statement stronger than requested.",
  "issues": [
    "The English statement omits the requirement that a and b must be distinct (a strict inequality a < b).",
    "The English statement does not explicitly require a and b to be distinct (a strict inequality a < b).",
    "The English statement does not explicitly require c and d to be distinct (c < d).",
    "The English statement does not explicitly require c and d to be distinct (c < d)."
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
  "strength": "stronger, or ambiguous with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement suggests a less restrictive inequality than that implied by the Lean theorem due to the omission of a domain restriction on a and b. This makes the Lean statement stronger than requested.",
  "issues": [
    "The English statement omits the requirement that a and b must be distinct (a strict inequality a < b).",
    "The English statement does not explicitly require a and b to be distinct (a strict inequality a < b).",
    "The English statement does not explicitly require c and d to be distinct (c < d).",
    "The English statement does not explicitly require c and d to be distinct (c < d)."
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


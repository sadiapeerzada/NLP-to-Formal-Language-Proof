# lib_q_finite_inclusion: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For finite sets s and t of natural numbers, if s is contained in t then the number of elements of s is at most the number of elements of t.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_finite_inclusion (s t : Finset ℕ) (h : s ⊆ t) : s.card ≤ t.card
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Finite natural sets s,t and subset premise; cardinality order matches, including empty sets."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_finite_inclusion",
  "theorem": "AuditReference14.study_q_finite_inclusion",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (s t : Finset ℕ) (h : s ⊆ t), s.card ≤ t.card",
  "axioms": [
    "propext",
    "Quot.sound"
  ],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "lib_q_finite_inclusion",
  "subject_sha256": "ac53373b88b73e44f595703941d28c2111586e85cc8eb2baea89464b78c03490",
  "kind": "exact_bounded_probe",
  "checked_assignments": 81,
  "filtered_by_assumptions": 175,
  "failures": [],
  "note": "All subsets of {0,1,2,3}.",
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
null
```

Schema error: issues must be a string list

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "s.card and t.card",
  "domains": "s and t are elements of Finset ℕ",
  "assumptions": "s is contained in t (s ⊆ t)",
  "equivalence": "s.card ≤ t.card",
  "strength": "same",
  "boundary_cases": "s and t are finite sets",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a containment property between finite sets of natural numbers and compares the cardinalities (sizes) of these sets. The Lean statement expresses this containment property and asserts that the cardinality of a subset is less than or equal to the cardinality of a containing set. This is a direct reflection of the English statement's meaning and is equivalent in strength."
}

```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Exploratory model did not complete a review; no verdict exists.",
    "Phi-4 response quality: Frozen schema parse failed; no accepted judgment.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


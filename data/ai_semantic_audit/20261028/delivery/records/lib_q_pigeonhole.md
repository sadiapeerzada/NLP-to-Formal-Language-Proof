# lib_q_pigeonhole: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
If a function maps a finite set s of natural numbers into a smaller finite set t, two distinct elements of s have the same image.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_pigeonhole (s t : Finset ℕ) (f : ℕ → ℕ) (h : t.card < s.card) (hm : ∀ x ∈ s, f x ∈ t) : ∃ x ∈ s, ∃ y ∈ s, x ≠ y ∧ f x = f y
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Finite natural sets and total natural function; smaller target cardinality plus maps-into hypothesis implies two distinct source members sharing an image; all existential membership clauses are present."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_pigeonhole",
  "theorem": "AuditReference15.study_q_pigeonhole",
  "source": "data/curation_batches/v0.2.1/references_expanded.lean",
  "expected_type": "∀ (s t : Finset ℕ) (f : ℕ → ℕ) (h : t.card < s.card) (hm : ∀ x ∈ s, f x ∈ t), ∃ x ∈ s, ∃ y ∈ s, x ≠ y ∧ f x = f y",
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
  "candidate_id": "lib_q_pigeonhole",
  "subject_sha256": "47c417d17c8895dd6583221c7eb278b568fb5c46455980c494381756be989094",
  "kind": "exact_bounded_probe",
  "checked_assignments": 1640,
  "filtered_by_assumptions": 63896,
  "failures": [],
  "note": "All maps on {0,1,2,3} and all subsets; finite complete universe only.",
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
  "quantifiers": "Universal and Existential",
  "domains": "Natural numbers and finite sets",
  "assumptions": "Function properties and cardinality inequality",
  "equivalence": "Conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "Endpoint check",
  "counterexample_search": "Specific candidate example",
  "explanation": "The English statement asserts a well-known combinatorial principle that is equivalent to a Lean theorem stating that a function mapping a larger set into a smaller one must map elements to the same value.",
  "issues": [
    "Lean Nat subtraction truncation",
    "Division and remainders totalization",
    "Mathlib conventions",
    "Omitted English domain restriction",
    "Different but equivalent algebraic encoding",
    "Proof-method requests separate from equivalence",
    "Specific candidate example needed"
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "Universal and Existential",
  "domains": "Natural numbers and finite sets",
  "assumptions": "Function properties and cardinality inequality",
  "equivalence": "Conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "Endpoint check",
  "counterexample_search": "Specific candidate example",
  "explanation": "The English statement asserts a well-known combinatorial principle that is equivalent to a Lean theorem stating that a function mapping a larger set into a smaller one must map elements to the same value.",
  "issues": [
    "Lean Nat subtraction truncation",
    "Division and remainders totalization",
    "Mathlib conventions",
    "Omitted English domain restriction",
    "Different but equivalent algebraic encoding",
    "Proof-method requests separate from equivalence",
    "Specific candidate example needed"
  ]
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Exploratory model did not complete a review; no verdict exists.",
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


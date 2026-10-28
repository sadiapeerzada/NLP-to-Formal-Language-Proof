# lib_m_canonical: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
If natural a and b are both less than m and congruent modulo m, then they are equal.
```

## Lean type

```lean
open scoped BigOperators
theorem study_m_canonical (m a b : ℕ) (ha : a < m) (hb : b < m) (h : Nat.ModEq m a b) : a = b
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural representatives a,b strictly less than m, congruent modulo m; equality conclusion matches and m=0 is vacuous under these bounds."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_m_canonical",
  "theorem": "AuditReference14.study_m_canonical",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (m a b : ℕ) (ha : a < m) (hb : b < m) (h : Nat.ModEq m a b), a = b",
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
  "candidate_id": "lib_m_canonical",
  "subject_sha256": "2dbe90f940a3dbece825aaa67c2db65d1a12c1f2a040da9b5c95a7b8e24604bf",
  "kind": "exact_bounded_probe",
  "checked_assignments": 36,
  "filtered_by_assumptions": 693,
  "failures": [],
  "note": "m=0 has no accepted a,b; strict representative bounds.",
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
  "quantifiers": "one each a and b",
  "domains": "ℕ",
  "assumptions": "a and b less than m, a and b congruent modulo m",
  "equivalence": "conclusion a = b",
  "strength": "stronger",
  "boundary_cases": "a and b are less than m and congruent modulo m",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of natural numbers that is equivalent to a Lean theorem in Mathlib. The Lean statement is an open scoped theorem that assumes a and b are less than m and congruent modulo m, and concludes they are equal. This is a stronger statement than requested because Mathlib does not require a and b to be distinct (hence not less than m in this case). There is no counterexample as the statement is true in the given domain and assumptions.",
  "issues": [
    "The Lean statement is an open scoped theorem and not a user-defined one.",
    "The required import is Mathlib, which is not specified in the expected Lean statement.",
    "The required definitions field is null, implying that no specific definitions are needed before this statement."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "one each a and b",
  "domains": "ℕ",
  "assumptions": "a and b less than m, a and b congruent modulo m",
  "equivalence": "conclusion a = b",
  "strength": "stronger",
  "boundary_cases": "a and b are less than m and congruent modulo m",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of natural numbers that is equivalent to a Lean theorem in Mathlib. The Lean statement is an open scoped theorem that assumes a and b are less than m and congruent modulo m, and concludes they are equal. This is a stronger statement than requested because Mathlib does not require a and b to be distinct (hence not less than m in this case). There is no counterexample as the statement is true in the given domain and assumptions.",
  "issues": [
    "The Lean statement is an open scoped theorem and not a user-defined one.",
    "The required import is Mathlib, which is not specified in the expected Lean statement.",
    "The required definitions field is null, implying that no specific definitions are needed before this statement."
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
    "Phi-4 response quality: Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


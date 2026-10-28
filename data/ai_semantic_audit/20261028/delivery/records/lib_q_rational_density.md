# lib_q_rational_density: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
Between any two distinct real numbers x<y there is a rational number q with x<q<y.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_rational_density (x y : ℝ) (h : x < y) : ∃ q : ℚ, x < q ∧ (q : ℝ) < y
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal ordered real x<y followed by existential rational q; explicit coercions compare q inside the real inequalities, preserving quantifier order."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_rational_density",
  "theorem": "AuditReference15.study_q_rational_density",
  "source": "data/curation_batches/v0.2.1/references_expanded.lean",
  "expected_type": "∀ (x y : ℝ) (h : x < y), ∃ q : ℚ, x < q ∧ (q : ℝ) < y",
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
  "candidate_id": "lib_q_rational_density",
  "subject_sha256": "ffdde8c335e75946212354f77335ff100750c637bb8c77a23601b25d78f24a41",
  "kind": "exact_bounded_probe",
  "checked_assignments": 78,
  "filtered_by_assumptions": 91,
  "failures": [],
  "note": "Construct rational midpoint for rational real-input subset; not density proof for all reals.",
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
  "quantifiers": "Universal (∀) versus Existential (∃)",
  "domains": "Real numbers (ℝ) versus Rational numbers (ℚ)",
  "assumptions": "x < y versus x < y and y is real",
  "equivalence": "The statement is equivalent in meaning as both assert the density of rationals in reals.",
  "strength": "same",
  "boundary_cases": "x and y are distinct real numbers",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement and Lean theorem assert the density of rational numbers between any two distinct real numbers. Both are equivalent in strength and scope.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "Universal (∀) versus Existential (∃)",
  "domains": "Real numbers (ℝ) versus Rational numbers (ℚ)",
  "assumptions": "x < y versus x < y and y is real",
  "equivalence": "The statement is equivalent in meaning as both assert the density of rationals in reals.",
  "strength": "same",
  "boundary_cases": "x and y are distinct real numbers",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement and Lean theorem assert the density of rational numbers between any two distinct real numbers. Both are equivalent in strength and scope.",
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
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "tentatively_retain_subject_to_resolving_all_disagreements"
}
```


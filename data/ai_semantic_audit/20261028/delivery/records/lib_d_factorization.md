# lib_d_factorization: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For nonzero natural a and b, the prime-exponent factorization function of a*b is the pointwise sum of their prime-exponent factorization functions.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_factorization (a b : ℕ) (ha : a ≠ 0) (hb : b ≠ 0) : (a * b).factorization = a.factorization + b.factorization
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural nonzero a,b; equality of prime-exponent functions means pointwise addition, with both nonzero hypotheses present."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_factorization",
  "theorem": "AuditReference14.study_d_factorization",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b : ℕ) (ha : a ≠ 0) (hb : b ≠ 0), (a * b).factorization = a.factorization + b.factorization",
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
  "candidate_id": "lib_d_factorization",
  "subject_sha256": "8308e14ec10e34a58c6e5a66e1938346f82252389bc3c2c2aad824923ed37814",
  "kind": "exact_bounded_probe",
  "checked_assignments": 256,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Nonzero naturals; compare complete prime-exponent dictionaries.",
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
  "quantifiers": "pointwise",
  "domains": "nonzero natural numbers",
  "assumptions": "a and b are nonzero natural numbers",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific endpoint check",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement implies a pointwise addition of factorization functions, while Lean's theorem expresses a multiplicative property directly. This makes the English statement stronger as it implies a more specific case (pointwise addition) than the general case covered by the Lean theorem.",
  "issues": [
    "The English statement assumes a multiplicative relationship that is not explicitly stated in Lean's theorem.",
    "The English statement does not account for the uniqueness of prime factorization in different numbers."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "pointwise",
  "domains": "nonzero natural numbers",
  "assumptions": "a and b are nonzero natural numbers",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific endpoint check",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement implies a pointwise addition of factorization functions, while Lean's theorem expresses a multiplicative property directly. This makes the English statement stronger as it implies a more specific case (pointwise addition) than the general case covered by the Lean theorem.",
  "issues": [
    "The English statement assumes a multiplicative relationship that is not explicitly stated in Lean's theorem.",
    "The English statement does not account for the uniqueness of prime factorization in different numbers."
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
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


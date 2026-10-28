# lib_d_totient_sum: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every natural n, the sum of Euler totient(d) over the positive divisors d of n equals n; Mathlib assigns the empty divisor set to zero.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_totient_sum (n : ℕ) : (∑ d ∈ n.divisors, Nat.totient d) = n
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal natural n; English explicitly defines zero's divisor set as empty, so the zero instance matches the totalized Mathlib statement."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_totient_sum",
  "theorem": "AuditReference14.study_d_totient_sum",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (n : ℕ), (∑ d ∈ n.divisors, Nat.totient d) = n",
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
  "candidate_id": "lib_d_totient_sum",
  "subject_sha256": "f9cfa717974f59c79254002713c2ba68a6047a1286bc74f3b134e6efe4e0010e",
  "kind": "exact_bounded_probe",
  "checked_assignments": 9,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Zero uses empty positive divisor set explicitly.",
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
  "quantifiers": "∀ n, ∑ d",
  "domains": "ℕ, Nat",
  "assumptions": "totient is a multiplicative function",
  "equivalence": "conclusion is equivalent to expected statement",
  "strength": "same",
  "boundary_cases": "n = 0",
  "counterexample_search": "no counterexample found",
  "explanation": "The statement accurately reflects the definition of the Euler totient function and its multiplicative property over divisors.",
  "issues": [
    "The expected Lean statement does not explicitly handle the case where n is zero, which is an exceptional case in divisor sums."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "∀ n, ∑ d",
  "domains": "ℕ, Nat",
  "assumptions": "totient is a multiplicative function",
  "equivalence": "conclusion is equivalent to expected statement",
  "strength": "same",
  "boundary_cases": "n = 0",
  "counterexample_search": "no counterexample found",
  "explanation": "The statement accurately reflects the definition of the Euler totient function and its multiplicative property over divisors.",
  "issues": [
    "The expected Lean statement does not explicitly handle the case where n is zero, which is an exceptional case in divisor sums."
  ]
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Exploratory model did not complete a review; no verdict exists.",
    "Phi-4 response quality: Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


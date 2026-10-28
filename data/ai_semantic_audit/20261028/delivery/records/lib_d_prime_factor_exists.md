# lib_d_prime_factor_exists: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
Every natural number n at least two has a prime divisor.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_prime_factor_exists (n : ℕ) (hn : 2 ≤ n) : ∃ p : ℕ, p.Prime ∧ p ∣ n
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural n>=2; existential natural prime divisor includes both primality and divisibility as conjuncts."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_prime_factor_exists",
  "theorem": "AuditReference15.study_d_prime_factor_exists",
  "source": "data/curation_batches/v0.2.1/references_expanded.lean",
  "expected_type": "∀ (n : ℕ) (hn : 2 ≤ n), ∃ p : ℕ, p.Prime ∧ p ∣ n",
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
  "candidate_id": "lib_d_prime_factor_exists",
  "subject_sha256": "077984448923ac74a8ed6da6b76c61996c7947f2980d4365c34a7737d05de0d6",
  "kind": "exact_bounded_probe",
  "checked_assignments": 127,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Exhaustive possible prime divisor witnesses for each n.",
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
  "quantifiers": "∀ n > 0, ∃ p : ℕ, p.Prime ∧ p ∣ n",
  "domains": "ℕ",
  "assumptions": "n > 0",
  "equivalence": "conclusion is equivalent",
  "strength": "stronger",
  "boundary_cases": "n = 0 and n = 1 are not considered",
  "counterexample_search": "no counterexample found",
  "explanation": "The statement is true as per the definition of a prime number and is consistent with the expected Lean statement.",
  "issues": [
    "The expected Lean statement incorrectly excludes n = 0 and n = 1 from the domain of natural numbers."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "∀ n > 0, ∃ p : ℕ, p.Prime ∧ p ∣ n",
  "domains": "ℕ",
  "assumptions": "n > 0",
  "equivalence": "conclusion is equivalent",
  "strength": "stronger",
  "boundary_cases": "n = 0 and n = 1 are not considered",
  "counterexample_search": "no counterexample found",
  "explanation": "The statement is true as per the definition of a prime number and is consistent with the expected Lean statement.",
  "issues": [
    "The expected Lean statement incorrectly excludes n = 0 and n = 1 from the domain of natural numbers."
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
    "Phi-4 response quality: Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


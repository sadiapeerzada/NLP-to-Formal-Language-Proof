# lib_i_alternating_binomial: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every positive natural n, the alternating sum of the binomial coefficients in row n is zero, interpreted in the integers.
```

## Lean type

```lean
open scoped BigOperators
theorem study_i_alternating_binomial (n : ℕ) (hn : n ≠ 0) : (∑ k ∈ Finset.range (n + 1), ((-1 : ℤ) ^ k * (n.choose k : ℤ))) = 0
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Positive natural n via n!=0; integer negative-one power and integer-coerced binomial coefficients preserve alternating signs."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_i_alternating_binomial",
  "theorem": "AuditReference14.study_i_alternating_binomial",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (n : ℕ) (hn : n ≠ 0), (∑ k ∈ Finset.range (n + 1), ((-1 : ℤ) ^ k * (n.choose k : ℤ))) = 0",
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
  "candidate_id": "lib_i_alternating_binomial",
  "subject_sha256": "57b5fe5f621bb1442aa63e899ca519c8349740ee83cee234b0bc962be943ed2e",
  "kind": "exact_bounded_probe",
  "checked_assignments": 16,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Positive n only; n=0 would fail.",
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
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of binomial coefficients that is equivalent to a Lean theorem stating that the alternating sum of binomial coefficients in row n is zero. This is a well-known result in combinatorics and is equivalent to the Lean theorem provided. There is no counterexample that refutes this statement, and it is consistent with the expected Lean statement provided.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of binomial coefficients that is equivalent to a Lean theorem stating that the alternating sum of binomial coefficients in row n is zero. This is a well-known result in combinatorics and is equivalent to the Lean theorem provided. There is no counterexample that refutes this statement, and it is consistent with the expected Lean statement provided.",
  "issues": []
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Exploratory model did not complete a review; no verdict exists.",
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


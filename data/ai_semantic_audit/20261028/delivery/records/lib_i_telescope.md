# lib_i_telescope: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every integer-valued function f on natural numbers and natural n, the sum of f(i+1)-f(i) for i from zero through n-1 equals f(n)-f(0).
```

## Lean type

```lean
open scoped BigOperators
theorem study_i_telescope (f : ℕ → ℤ) (n : ℕ) : (∑ i ∈ Finset.range n, (f (i + 1) - f i)) = f n - f 0
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal function from naturals to integers and natural n; range n gives exactly i=0..n-1 and integer subtraction telescopes to f(n)-f(0)."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_i_telescope",
  "theorem": "AuditReference14.study_i_telescope",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (f : ℕ → ℤ) (n : ℕ), (∑ i ∈ Finset.range n, (f (i + 1) - f i)) = f n - f 0",
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
  "candidate_id": "lib_i_telescope",
  "subject_sha256": "e998a2a0c987b611097fc7c14cc58587efb0f48982a981db4cec4c3b85cb3785",
  "kind": "exact_bounded_probe",
  "checked_assignments": 1215,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "All 3^5 sampled function vectors and prefixes, integer subtraction.",
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
  "quantifiers": "one variable n, one variable i",
  "domains": "ℕ f : ℕ → ℤ",
  "assumptions": "one variable f : ℕ → ℤ",
  "equivalence": "conclusion direct",
  "strength": "same",
  "boundary_cases": "specific zero endpoint check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement describes a telescoping sum series where the sum of differences f(i+1) - f(i) from i=0 to i=n-1 equals f(n) - f(0). This is equivalent to the expected Lean statement which expresses this property as a summation over a finite range ending at n, resulting in the final expression f(n) - f(0). There is a direct equivalence in terms of mathematical meaning and formal expression in Lean.",
  "issues": [
    "The expected Lean statement uses a different notation but conveys the same concept as the English statement."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "one variable n, one variable i",
  "domains": "ℕ f : ℕ → ℤ",
  "assumptions": "one variable f : ℕ → ℤ",
  "equivalence": "conclusion direct",
  "strength": "same",
  "boundary_cases": "specific zero endpoint check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement describes a telescoping sum series where the sum of differences f(i+1) - f(i) from i=0 to i=n-1 equals f(n) - f(0). This is equivalent to the expected Lean statement which expresses this property as a summation over a finite range ending at n, resulting in the final expression f(n) - f(0). There is a direct equivalence in terms of mathematical meaning and formal expression in Lean.",
  "issues": [
    "The expected Lean statement uses a different notation but conveys the same concept as the English statement."
  ]
}
```


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


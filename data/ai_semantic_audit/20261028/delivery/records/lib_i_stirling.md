# lib_i_stirling: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
The Stirling numbers of the second kind satisfy S(n+1,k+1)=(k+1)*S(n,k+1)+S(n,k) for natural n and k.
```

## Lean type

```lean
open scoped BigOperators
theorem study_i_stirling (n k : ℕ) : Nat.stirlingSecond (n + 1) (k + 1) = (k + 1) * Nat.stirlingSecond n (k + 1) + Nat.stirlingSecond n k
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal natural n,k; second-kind Stirling recurrence with coefficient k+1 and indices n+1,k+1 matches, including zero boundaries."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_i_stirling",
  "theorem": "AuditReference15.study_i_stirling",
  "source": "data/curation_batches/v0.2.1/references_expanded.lean",
  "expected_type": "∀ (n k : ℕ), Nat.stirlingSecond (n + 1) (k + 1) = (k + 1) * Nat.stirlingSecond n (k + 1) + Nat.stirlingSecond n k",
  "axioms": [],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "lib_i_stirling",
  "subject_sha256": "d54323c53ec31cd66442608400cdc616fd4ef11232c5e6d6f5784bd926e6b018",
  "kind": "exact_bounded_probe",
  "checked_assignments": 81,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Exact recursive Stirling computation; may mirror definition.",
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
  "explanation": "The English statement outlines a recursive formula for Stirling numbers of the second kind, while the Lean theorem expresses this relationship using Nat.stirlingSecond. Both correctly assert that S(n+1,k+1) equals (k+1)*S(n,k+1)+S(n,k) for natural numbers n and k. There is an equivalence in terms of mathematical conclusion and theorem strength.",
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
  "explanation": "The English statement outlines a recursive formula for Stirling numbers of the second kind, while the Lean theorem expresses this relationship using Nat.stirlingSecond. Both correctly assert that S(n+1,k+1) equals (k+1)*S(n,k+1)+S(n,k) for natural numbers n and k. There is an equivalence in terms of mathematical conclusion and theorem strength.",
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


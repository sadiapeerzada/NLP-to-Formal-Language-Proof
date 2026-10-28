# lib_q_integer_sqrt: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every natural n, the square of its natural-number square root is less than n+1.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_integer_sqrt (n : ℕ) : Nat.sqrt n ^ 2 < n + 1
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal natural n; natural floor square root squared < n+1 is non-strict <=n equivalently on naturals."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_integer_sqrt",
  "theorem": "AuditReference14.study_q_integer_sqrt",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (n : ℕ), Nat.sqrt n ^ 2 < n + 1",
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
  "candidate_id": "lib_q_integer_sqrt",
  "subject_sha256": "30f18d1d6c21ee3fc49c9b642ab004077732875fa3371fe5b8ce813385cbc51a",
  "kind": "exact_bounded_probe",
  "checked_assignments": 129,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Exact integer square root.",
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
  "quantifiers": "∀ n : ℕ",
  "domains": "ℕ",
  "assumptions": "none",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of natural numbers regarding the square root and its square. The Lean theorem expresses this property formally. There is an inherent complexity in formalizing the square root operation in Lean due to the truncation of subtraction and the totalization of division and remainders, which may lead to a statement that is technically stronger than the original English statement due to Mathlib conventions not being explicitly stated in English. Without delving into Mathlib's specific definitions and operations on rationals, one cannot directly compare the equivalence of the statement in English versus Lean.",
  "issues": [
    "The English statement implicitly assumes a real-number square root operation while Lean operates on rationals.",
    "The English statement does not account for the truncation of subtraction and totalization of division and remainders in Lean.",
    "The English statement does not explicitly limit the square root operation to natural numbers."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "∀ n : ℕ",
  "domains": "ℕ",
  "assumptions": "none",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of natural numbers regarding the square root and its square. The Lean theorem expresses this property formally. There is an inherent complexity in formalizing the square root operation in Lean due to the truncation of subtraction and the totalization of division and remainders, which may lead to a statement that is technically stronger than the original English statement due to Mathlib conventions not being explicitly stated in English. Without delving into Mathlib's specific definitions and operations on rationals, one cannot directly compare the equivalence of the statement in English versus Lean.",
  "issues": [
    "The English statement implicitly assumes a real-number square root operation while Lean operates on rationals.",
    "The English statement does not account for the truncation of subtraction and totalization of division and remainders in Lean.",
    "The English statement does not explicitly limit the square root operation to natural numbers."
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
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


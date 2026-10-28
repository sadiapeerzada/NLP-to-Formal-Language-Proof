# lib_m_cancel: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For positive natural m, if c*a and c*b are congruent modulo m, then a and b are congruent modulo m/gcd(m,c).
```

## Lean type

```lean
open scoped BigOperators
theorem study_m_cancel (m c a b : ℕ) (hm : 0 < m) (h : Nat.ModEq m (c * a) (c * b)) : Nat.ModEq (m / Nat.gcd m c) a b
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Positive natural modulus m and arbitrary natural multiplier c; cancellation reduces modulus to m/gcd(m,c), not to m."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_m_cancel",
  "theorem": "AuditReference14.study_m_cancel",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (m c a b : ℕ) (hm : 0 < m) (h : Nat.ModEq m (c * a) (c * b)), Nat.ModEq (m / Nat.gcd m c) a b",
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
  "candidate_id": "lib_m_cancel",
  "subject_sha256": "a3eeba36e5a313f57824edf5b62378696a8ccb267bdb615ebfcf9dff1536d840",
  "kind": "exact_bounded_probe",
  "checked_assignments": 2975,
  "filtered_by_assumptions": 2128,
  "failures": [],
  "note": "m positive makes gcd nonzero.",
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
  "strength": "same, stronger, weaker, or ambiguous with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement outlines a theorem from number theory concerning congruence and greatest common divisors (gcd) in the context of modular arithmetic. It states that if a and b are positive natural numbers and c is a positive natural number such that c multiplied by a and c multiplied by b are congruent modulo m, then a and b are congruent modulo the quotient of m divided by the gcd of m and c. This is a statement of cancellation law in modular arithmetic and is consistent with the expected Lean statement provided in the subject data. There is no counterexample provided in the data, so it is not possible to evaluate the counterexample search field directly. However, the statement is true as per number theory and should be faithfully translated into a Lean theorem provided that the import statement and definitions required are met in the actual Lean code.",
  "issues": [
    "The actual import statement and definitions required field is missing in the subject data.",
    "The expected Lean statement references a library (lib_m_cancel) that is not standard in Mathlib and may not be directly translated without modification."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same, stronger, weaker, or ambiguous with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement outlines a theorem from number theory concerning congruence and greatest common divisors (gcd) in the context of modular arithmetic. It states that if a and b are positive natural numbers and c is a positive natural number such that c multiplied by a and c multiplied by b are congruent modulo m, then a and b are congruent modulo the quotient of m divided by the gcd of m and c. This is a statement of cancellation law in modular arithmetic and is consistent with the expected Lean statement provided in the subject data. There is no counterexample provided in the data, so it is not possible to evaluate the counterexample search field directly. However, the statement is true as per number theory and should be faithfully translated into a Lean theorem provided that the import statement and definitions required are met in the actual Lean code.",
  "issues": [
    "The actual import statement and definitions required field is missing in the subject data.",
    "The expected Lean statement references a library (lib_m_cancel) that is not standard in Mathlib and may not be directly translated without modification."
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
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into strength. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


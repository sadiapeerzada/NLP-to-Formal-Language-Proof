# lib_d_prime_parity: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
Every natural prime is either two or odd.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_prime_parity (p : ℕ) (hp : p.Prime) : p = 2 ∨ Odd p
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal natural p with primality premise; p=2 OR Odd p, no accidental conjunction."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_prime_parity",
  "theorem": "AuditReference14.study_d_prime_parity",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (p : ℕ) (hp : p.Prime), p = 2 ∨ Odd p",
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
  "candidate_id": "lib_d_prime_parity",
  "subject_sha256": "1bf5272a6eaf86c297ec7beceaa86267f1c860818877692d868b731fdd7380f9",
  "kind": "exact_bounded_probe",
  "checked_assignments": 6,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Odd primality conclusion only for actual primes.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
{
  "label": "not faithful",
  "quantifiers": "∀p ∈ ℕ, p.Prime",
  "domains": "ℕ, Prime",
  "assumptions": "None specified",
  "equivalence": "The English proposition implies that all primes are either 2 or odd, which aligns with the expected Lean theorem structurized as a disjunction.",
  "strength": "The English proposition is a specific case of the Lean theorem, lacking generality.",
  "boundary_cases": "The proposition does not address the case of the prime number 2, which is both prime and even.",
  "counterexample_search": "The English proposition is challenged by the prime number 2, which is a counterexample to its claim.",
  "explanation": "The English proposition is not entirely faithful to the Lean theorem because it omits the prime number 2, which is an exception to the rule stated. The Lean theorem accounts for all natural prime numbers, including the number 2, which is even.",
  "issues": [
    "Omission of the prime number 2 as a counterexample",
    "Lack of generality in the English proposition",
    "Potential misunderstanding of the theorem's inclusivity of the number 2",
    "Implicit assumption that all primes are odd excluding the prime number 2"
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "not faithful",
  "quantifiers": "∀p ∈ ℕ, p.Prime",
  "domains": "ℕ, Prime",
  "assumptions": "None specified",
  "equivalence": "The English proposition implies that all primes are either 2 or odd, which aligns with the expected Lean theorem structurized as a disjunction.",
  "strength": "The English proposition is a specific case of the Lean theorem, lacking generality.",
  "boundary_cases": "The proposition does not address the case of the prime number 2, which is both prime and even.",
  "counterexample_search": "The English proposition is challenged by the prime number 2, which is a counterexample to its claim.",
  "explanation": "The English proposition is not entirely faithful to the Lean theorem because it omits the prime number 2, which is an exception to the rule stated. The Lean theorem accounts for all natural prime numbers, including the number 2, which is even.",
  "issues": [
    "Omission of the prime number 2 as a counterexample",
    "Lack of generality in the English proposition",
    "Potential misunderstanding of the theorem's inclusivity of the number 2",
    "Implicit assumption that all primes are odd excluding the prime number 2"
  ]
}

```


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each",
  "domains": "ℕ and Prime",
  "assumptions": "p.Prime and p = 2 or p = Odd p",
  "equivalence": "conclusion p = 2 or p is odd",
  "strength": "same",
  "boundary_cases": "p = 2 and p = odd numbers",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of natural primes being odd or equal to two. The Lean theorem expresses this property formally in Mathlib. There is no counterexample that refutes the statement as it is universally accepted in mathematics that primes greater than two are odd. The equivalence is direct as the conclusion directly follows from the assumptions.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "one each",
  "domains": "ℕ and Prime",
  "assumptions": "p.Prime and p = 2 or p = Odd p",
  "equivalence": "conclusion p = 2 or p is odd",
  "strength": "same",
  "boundary_cases": "p = 2 and p = odd numbers",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of natural primes being odd or equal to two. The Lean theorem expresses this property formally in Mathlib. There is no counterexample that refutes the statement as it is universally accepted in mathematics that primes greater than two are odd. The equivalence is direct as the conclusion directly follows from the assumptions.",
  "issues": []
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-4 response quality: Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


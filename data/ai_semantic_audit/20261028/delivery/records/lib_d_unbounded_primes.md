# lib_d_unbounded_primes: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every natural number n, there is a natural prime p at least n.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_unbounded_primes (n : ℕ) : ∃ p : ℕ, n ≤ p ∧ p.Prime
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "For each natural lower bound n, existential natural p>=n and p.Prime; at least is non-strict."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_unbounded_primes",
  "theorem": "AuditReference14.study_d_unbounded_primes",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (n : ℕ), ∃ p : ℕ, n ≤ p ∧ p.Prime",
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
  "candidate_id": "lib_d_unbounded_primes",
  "subject_sha256": "35c4b66f16f67fcf1d2467b4e067ad305ff51fff30bb4310a09a6231200c6ee8",
  "kind": "exact_bounded_probe",
  "checked_assignments": 9,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Complete witness search in stated finite interval for each n; not infinitude proof.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 20 column 1 (char 1800)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "∀n ∈ ℕ, ∃p ∈ ℕ, n ≤ p ∧ Prime(p)",
  "domains": "ℕ for n and p, but Lean's BigOperators do not directly support this",
  "assumptions": "No additional assumptions required",
  "equivalence": "The English proposition suggests a stronger statement than the Lean theorem",
  "strength": "The English proposition implies the existence of a prime greater than any given natural number, while the Lean theorem only asserts the existence of a prime with a property that n is less than or equal to it, which is a weaker claim.",
  "boundary_cases": "Consider the case when n is a large natural number; the English proposition would still imply the existence of a prime greater than n, while the Lean theorem does not guarantee this.",
  "counterexample_search": "The English proposition cannot be equivalent to the Lean theorem because it implies the existence of a prime greater than any given natural number, which is not asserted by the Lean theorem.",
  "explanised": "The English proposition suggests a stronger claim than the Lean theorem, which only asserts the existence of a prime with a specific property related to the given natural number.",
  "issues": [
    "The Lean theorem does not capture the implication that there is a prime greater than any given natural number.",
    "The Lean theorem's scope is limited to the property n ≤ p ∧ Prime(p), not the existence of a prime greater than n.",
    "The English proposition extends beyond the Lean theorem's formalization by implying the existence of a prime greater than any given natural number.",
    "The Lean theorem's formalization does not match the strength of the English proposition.",
    "The English proposition's claim is stronger than what is formalized in the Lean theorem."
  ]
}

```json
{
  "label": "not faithful",
  "quantifiers": "∀n ∈ ℕ, ∃p ∈ ℕ, n ≤ p ∧ Prime(p)",
  "domains": "ℕ for n and p, but Lean's BigOperators do not directly support this",
  "assumptions": "No additional assumptions required",
  "equivalence": "The English proposition suggests a stronger statement than the Lean theorem",
  "strength": "The English proposition implies the existence of a prime greater than any given natural number, while the Lean theorem only asserts the existence of a prime with a property that n is less than or equal to it, which is a weaker claim.",
  "boundary_cases": "Consider the case when n is a large natural number; the English proposition would still imply the existence of a prime greater than n, while the Lean theorem does not guarantee this.",
  "counterexample_search": "The English proposition cannot be equivalent to the Lean theorem because it implies the existence of a prime greater than any given natural number, which is not asserted by the Lean theorem.",
  "explanation": "The English proposition extends beyond the Lean theorem's formalization by implying the existence of a prime greater than any given natural number, which is not asserted by the Lean theorem.",
  "issues": [
    "The Lean theorem does not capture the implication that there is a prime greater than any given natural number.",
    "The Lean theorem's scope is limited to the property n ≤ p ∧ Prime(p), not the existence of a prime greater than n.",
    "The English proposition's claim is stronger than what is formalized in the Lean theorem.",
    "The English proposition extends beyond the Lean theorem's formalization by implying the existence of a prime greater than any given natural number, which is not asserted by the Lean theorem."
  ]
}
}
```
````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "∀ n. ∃ p : ℕ, n ≤ p ∧ p.Prime",
  "domains": "ℕ",
  "assumptions": "none",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts that for every natural number n, there is a prime p greater than or equal to n. This is equivalent to stating that there is an unbounded number of primes in the natural numbers, which is a well-known result in number theory (the infinitude of primes). The Lean statement expresses this as an existential quantifier stating that for every natural number n, there is a prime p such that p is greater than or equal to n and p is a prime number. This is a stronger statement than requested because it directly asserts the infinitude of primes rather than just stating that such primes exist.",
  "issues": [
    "The Lean statement is equivalent to the English statement but is stronger than requested because it directly asserts the infinitude of primes rather than just stating that such primes exist."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "∀ n. ∃ p : ℕ, n ≤ p ∧ p.Prime",
  "domains": "ℕ",
  "assumptions": "none",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts that for every natural number n, there is a prime p greater than or equal to n. This is equivalent to stating that there is an unbounded number of primes in the natural numbers, which is a well-known result in number theory (the infinitude of primes). The Lean statement expresses this as an existential quantifier stating that for every natural number n, there is a prime p such that p is greater than or equal to n and p is a prime number. This is a stronger statement than requested because it directly asserts the infinitude of primes rather than just stating that such primes exist.",
  "issues": [
    "The Lean statement is equivalent to the English statement but is stronger than requested because it directly asserts the infinitude of primes rather than just stating that such primes exist."
  ]
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


# arith_005: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
Explain why the binomial coefficient “n choose 0” equals 1 and the binomial coefficient “n choose n” equals 1.
```

## Lean type

```lean
theorem choose_zero_and_self (n : ℕ) : Nat.choose n 0 = 1 ∧ Nat.choose n n = 1
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural n is implicit in choosing objects; the two binomial boundary equalities form a conjunction, including n=0."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "arith_005",
  "theorem": "AuditReference8.choose_zero_and_self",
  "source": "data/curation_batches/v0.1.4/arith_005_binomial_boundary_values.lean",
  "expected_type": "∀ (n : ℕ), Nat.choose n 0 = 1 ∧ Nat.choose n n = 1",
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
  "candidate_id": "arith_005",
  "subject_sha256": "222617564336d12fc12c2eeeabbcb91de6383dd4dc38a757d35f73d27bcd0cd3",
  "kind": "exact_bounded_probe",
  "checked_assignments": 9,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Both conjuncts at n=0 included.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: issues must be a string list

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "universal quantification over n in ℕ",
  "domains": "ℕ, as implied by the binomial coefficient context",
  "assumptions": "n is a natural number",
  "equivalence": "the English proposition is equivalent to the Lean theorem TYPE",
  "strength": "the Lean theorem fully captures the English proposition' extraneous details",
  "boundary_cases": "consider the case when n = 0, which aligns with the proposition",
  "counterexample_search": "no counterexample exists as the proposition is true for all natural numbers",
  "explanation": "the binomial coefficient 'n choose k' is defined as n!/(k!(n-k)!). For k=0, the formula simplifies to 1, and for k=n, the (n-k) term becomes n!/0! which is also 1. This aligns with the proposition that 'n choose 0' and 'n choose n' both equal 1.",
  "issues": "none"
}






































































































































































































































































































































































































































































































































































































































































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
  "explanation": "The binomial coefficient n choose k is defined as the number of ways to choose k elements from a set of n distinct elements. By definition, choosing none elements (0 elements) from a set is exactly one way (the empty set), hence n choose 0 equals 1. Similarly, choosing all elements (n elements) from a set is exactly one way (the set itself), hence n choose n equals 1.",
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
  "explanation": "The binomial coefficient n choose k is defined as the number of ways to choose k elements from a set of n distinct elements. By definition, choosing none elements (0 elements) from a set is exactly one way (the empty set), hence n choose 0 equals 1. Similarly, choosing all elements (n elements) from a set is exactly one way (the set itself), hence n choose n equals 1.",
  "issues": []
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


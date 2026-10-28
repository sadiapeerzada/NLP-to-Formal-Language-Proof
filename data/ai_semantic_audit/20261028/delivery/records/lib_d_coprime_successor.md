# lib_d_coprime_successor: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
Every natural number n is coprime to n+1.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_coprime_successor (n : ℕ) : Nat.Coprime n (n + 1)
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal natural n; coprimality of n,n+1 includes n=0 as intended."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_coprime_successor",
  "theorem": "AuditReference14.study_d_coprime_successor",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (n : ℕ), Nat.Coprime n (n + 1)",
  "axioms": [
    "propext",
    "Quot.sound"
  ],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "lib_d_coprime_successor",
  "subject_sha256": "4d14191b349536d69b116a89bd36a946080c69aaaf9be96e4644b1b9d8079e75",
  "kind": "exact_bounded_probe",
  "checked_assignments": 9,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Zero included.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 22 column 1 (char 1775)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "uncertain",
  "quantifiers": "universal quantifier over ℕ",
  "domains": "ℕ, as intended by the English proposition",
  "assumptions": "no additional assumptions required",
  "equivalence": "not equivalent to the expected Lean theorem",
  "strength": "the English proposition suggests a stronger statement than the Lean theorem",
  "boundary_cases": "consider the case when n is 1, which is not explicitly handled by the Lean theorem",
  "counterexample_search": "no concrete counterexample provided, but the English proposition implies a stronger statement",
  "explanised": "the English proposition suggests that all natural numbers are coprime to their successors, which is not captured by the Lean theorem",
  "issues": [
    "The Lean theorem does not account for the base case where n is 1.",
    "The Lean theorem lacks the universal quantifier for the natural numbers, making it weaker than the English proposition.",
    "The Lean theorem's domain is implicitly limited, whereas the English proposition encompasse all natural numbers.",
    "The English proposition does not specify any coercions or hypotheses, implying a broader generalization.",
    "The English proposition does not contain any conjunctions, disjunctions, or 'iff' statements, suggesting a single, straightforward claim.",
    "The English proposition does not mention strictness, endpoint conventions, or specific cases like zero and negative numbers, which are not addressed in the Lean theorem.",
    "The Lean theorem does not handle Nat truncated subtraction and division, which may be relevant to the claim.",
    "The English proposition suggests a stronger claim than the Lean theorem, which only asserts coprimality for a specific, not universally quantified case."
  ]
}
```
````


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
  "explanation": "The English statement asserts that every natural number n is coprime to n+1, which implies that gcd(n, n+1) = 1 for all n in ℕ. This is true because n and n+1 are consecutive integers and consecutive integers are always coprime. There is no counterexample that refutes this statement as n cannot be 0 (as ℕ excludes 0) and n+1 is always greater than n, avoiding division by zero.",
  "issues": [
    "The Lean statement is equivalent to the English statement but is written as an open scoped theorem rather than a closed one. This does not change the mathematical truth but reflects a difference in how the statement is formalized in Lean versus Mathlib.",
    "The Lean statement uses a different notation (Nat.Coprime) than one might expect from Mathlib's usual notation but is still equivalent in meaning."
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
  "explanation": "The English statement asserts that every natural number n is coprime to n+1, which implies that gcd(n, n+1) = 1 for all n in ℕ. This is true because n and n+1 are consecutive integers and consecutive integers are always coprime. There is no counterexample that refutes this statement as n cannot be 0 (as ℕ excludes 0) and n+1 is always greater than n, avoiding division by zero.",
  "issues": [
    "The Lean statement is equivalent to the English statement but is written as an open scoped theorem rather than a closed one. This does not change the mathematical truth but reflects a difference in how the statement is formalized in Lean versus Mathlib.",
    "The Lean statement uses a different notation (Nat.Coprime) than one might expect from Mathlib's usual notation but is still equivalent in meaning."
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


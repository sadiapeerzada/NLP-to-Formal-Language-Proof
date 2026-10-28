# lib_i_fibonacci: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every natural number n, the Fibonacci number at n+2 equals the sum of the Fibonacci numbers at n and n+1, using F(0)=0 and F(1)=1.
```

## Lean type

```lean
open scoped BigOperators
theorem study_i_fibonacci (n : ℕ) : Nat.fib (n + 2) = Nat.fib n + Nat.fib (n + 1)
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural n and specified F0=0,F1=1 align with Nat.fib; recurrence at n+2 is exact."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_i_fibonacci",
  "theorem": "AuditReference14.study_i_fibonacci",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (n : ℕ), Nat.fib (n + 2) = Nat.fib n + Nat.fib (n + 1)",
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
  "candidate_id": "lib_i_fibonacci",
  "subject_sha256": "5d1ad6449c1f9ece34dbddebd1ad442a32b5811bb32df41d7cf5a67c185c760a",
  "kind": "exact_bounded_probe",
  "checked_assignments": 9,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "F0=0,F1=1 exact recursive computation.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
{
  "label": "not faithful",
  "quantifiers": "universal quantifier on n, existential quantifier on F(n+2)",
  "domains": "ℕ, BigOperators",
  "assumptions": "definitions of F(0)=0, F(1)=1, and Nat.fib function",
  "equivalence": "proposition does not directly correspond to expected Lean theorem",
  "strength": "the proposition is a weaker statement than the expected Lean theorem",
  "boundary_cases": "undefined for n=0 and n=1",
  "counterexample_search": "n=0 or n=1",
  "explanation": "the English proposition lacks the explicit definition of the Fibonacci sequence and assumes knowledge of its properties",
  "issues": [
    "The proposition does not specify the definition of the Fibonacci sequence, which is necessary for a formal proof.",
    "The proposition assumes properties of the Fibonacci sequence without proof, which is insufficient for a formal theorem.",
    "The proposition does not align with the expected Lean theorem, which includes the definitions of F(0) and F(1).",
    "The proposition does not account for the base cases in the Fibonacci sequence, which are necessary for a complete formalization.",
    "The proposition is not a formal statement that can be directly translated into a Lean theorem without additional assumptions."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "not faithful",
  "quantifiers": "universal quantifier on n, existential quantifier on F(n+2)",
  "domains": "ℕ, BigOperators",
  "assumptions": "definitions of F(0)=0, F(1)=1, and Nat.fib function",
  "equivalence": "proposition does not directly correspond to expected Lean theorem",
  "strength": "the proposition is a weaker statement than the expected Lean theorem",
  "boundary_cases": "undefined for n=0 and n=1",
  "counterexample_search": "n=0 or n=1",
  "explanation": "the English proposition lacks the explicit definition of the Fibonacci sequence and assumes knowledge of its properties",
  "issues": [
    "The proposition does not specify the definition of the Fibonacci sequence, which is necessary for a formal proof.",
    "The proposition assumes properties of the Fibonacci sequence without proof, which is insufficient for a formal theorem.",
    "The proposition does not align with the expected Lean theorem, which includes the definitions of F(0) and F(1).",
    "The proposition does not account for the base cases in the Fibonacci sequence, which are necessary for a complete formalization.",
    "The proposition is not a formal statement that can be directly translated into a Lean theorem without additional assumptions."
  ]
}

```


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each n, n+1, n+2",
  "domains": "Nat",
  "assumptions": "F(0)=0 and F(1)=1",
  "equivalence": "conclusion direct equality",
  "strength": "same",
  "boundary_cases": "n=0",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement directly translates into a Lean theorem that is equivalent in strength and scope to the expected statement.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "one each n, n+1, n+2",
  "domains": "Nat",
  "assumptions": "F(0)=0 and F(1)=1",
  "equivalence": "conclusion direct equality",
  "strength": "same",
  "boundary_cases": "n=0",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement directly translates into a Lean theorem that is equivalent in strength and scope to the expected statement.",
  "issues": []
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Coding-AI/model labels or parse status differ.",
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "tentatively_retain_subject_to_resolving_all_disagreements"
}
```


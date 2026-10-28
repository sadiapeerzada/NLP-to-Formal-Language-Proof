# lib_d_frobenius: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
If natural numbers m and n are coprime and a and b are nonzero natural numbers, m*a+n*b cannot equal m*n.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_frobenius (m n a b : ℕ) (h : Nat.Coprime m n) (ha : a ≠ 0) (hb : b ≠ 0) : m * a + n * b ≠ m * n
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural m,n coprime and nonzero natural a,b; inequality m*a+n*b!=m*n matches all hypotheses including allowed zero m,n."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_frobenius",
  "theorem": "AuditReference14.study_d_frobenius",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (m n a b : ℕ) (h : Nat.Coprime m n) (ha : a ≠ 0) (hb : b ≠ 0), m * a + n * b ≠ m * n",
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
  "candidate_id": "lib_d_frobenius",
  "subject_sha256": "b3df14107ff7d555b53b365f7a260edd59c3c0f2c1430ef6e4a82784b07ceb62",
  "kind": "exact_bounded_probe",
  "checked_assignments": 1125,
  "filtered_by_assumptions": 900,
  "failures": [],
  "note": "Nonzero a,b and coprimality; m or n may be zero.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Missing substantive field: explanation

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "uncertain",
  "quantifiers": "universal quantifiers for m, n, a, b with specified constraints",
  "domains": "ℕ for m, n, a, b with nonzero constraints and coprimality condition",
  "assumptions": "coprimality of m and n, a and b being nonzero",
  "equivalence": "the English proposition is not explicitly stated as equivalent to the Lean theorem",
  "strength": "the English proposition suggests a specific case of the Frobenius theorem, while the Lean theorem generalizes it",
  "boundary_cases": "not specified, but zero and negative cases are not addressed in the Lean theorem",
  "counterexample_search": "no counterexample provided, but the English proposition lacks generality",
  "explanised": "the English proposition is more restrictive than the Lean theorem, implying a subset rather than the full generality of the Lean theorem",
  "issues": [
    "The English proposition does not mention the Frobenius theorem explicitly, which encompassees a broader range of cases.",
    "The Lean theorem allows for the general case, including zero and negative values, which the English proposition does not.",
    "The English proposition does not account for the totalization aspect of operations, which is present in the Lean theorem.",
    "The English proposition does not specify the use of 'BigOperators' or the 'theorems' library, which are necessary for the formalization.",
    "The English proposition does not mention the 'Nat.Coprime' predicate, which is essential for the Lean theorem.",
    "The English proposition does not address the potential for coercions between different domains, which are allowed in the Lean theorem."
  ]
}

```


## Phi-4-mini actual judgment

```json
{
  "label": "not faithful",
  "quantifiers": "m and n coprime; a and b nonzero natural numbers",
  "domains": "ℕ (natural numbers)",
  "assumptions": "m and n coprime; a and b nonzero natural numbers",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example",
  "explanation": "The English statement asserts a property of coprime numbers and nonzero natural numbers that is not equivalent to the Lean theorem due to different handling of division and remainders in Lean's implementation versus the expected behavior in general mathematics.",
  "issues": [
    "Lean Nat subtraction is truncated; division and remainders are totalized.",
    "The expected Lean theorem does not account for the totalization of division and remainders."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "not faithful",
  "quantifiers": "m and n coprime; a and b nonzero natural numbers",
  "domains": "ℕ (natural numbers)",
  "assumptions": "m and n coprime; a and b nonzero natural numbers",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example",
  "explanation": "The English statement asserts a property of coprime numbers and nonzero natural numbers that is not equivalent to the Lean theorem due to different handling of division and remainders in Lean's implementation versus the expected behavior in general mathematics.",
  "issues": [
    "Lean Nat subtraction is truncated; division and remainders are totalized.",
    "The expected Lean theorem does not account for the totalization of division and remainders."
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
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted.",
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


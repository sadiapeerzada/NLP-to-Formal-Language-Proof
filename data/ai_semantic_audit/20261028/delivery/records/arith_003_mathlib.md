# arith_003_mathlib: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For any natural numbers a, b, and c, a times (b plus c) equals a times b plus a times c.
```

## Lean type

```lean
theorem distributive_nat (a b c : ℕ) : a * (b + c) = a * b + a * c
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Same English and same alpha-equivalent proposition as arith_003; faithful proposition but must not count as an independent additional item."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "arith_003_mathlib",
  "theorem": "AuditReference0.distributive_nat",
  "source": "data/reference_verification/v0.1.0/references.lean",
  "expected_type": "∀ (a b c : ℕ), a * (b + c) = a * b + a * c",
  "axioms": [],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "arith_003_mathlib",
  "subject_sha256": "70f725901da6b47a112879c0ab360b2ea528a750f6a782a103b8d1570a3eaf26",
  "kind": "exact_bounded_probe",
  "checked_assignments": 729,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Same distributivity predicate exposes duplicate semantics.",
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
  "label": "faithful",
  "quantifiers": "universal quantification over ℕ for a, b, and c",
  "domains": "natural numbers (ℕ)",
  "assumptions": "no additional assumptions",
  "equivalence": "the expected Lean theorem formalizes the English proposition",
  "strength": "the theorem captures the distributive property of multiplication over addition for natural numbers",
  "boundary_cases": "considering the case when any of a, b, or c is zero, the theorem holds true as both sides of the equation equal zero",
  "counterexample_search": "no counterexample exists as the distributive property is universally valid for natural numbers",
  "explanised": "the distributive property is a fundamental property of multiplication and addition in arithmetic, and the Lean theorem correctly formalizes this property",
  "issues": []
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
  "explanation": "The English statement and the Lean theorem both assert the commutative property of multiplication over addition for natural numbers. The statement assumes a and b are natural numbers and concludes that a multiplied by the sum of b and c equals the sum of a multiplied by b and a multiplied by c. This is equivalent to the distributive property of multiplication over addition in Lean's Nat type. There is no counterexample as this is a fundamental property of arithmetic. The statement is faithful as it is equivalent in meaning and implications to the Lean theorem.",
  "issues": []
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
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and the Lean theorem both assert the commutative property of multiplication over addition for natural numbers. The statement assumes a and b are natural numbers and concludes that a multiplied by the sum of b and c equals the sum of a multiplied by b and a multiplied by c. This is equivalent to the distributive property of multiplication over addition in Lean's Nat type. There is no counterexample as this is a fundamental property of arithmetic. The statement is faithful as it is equivalent in meaning and implications to the Lean theorem.",
  "issues": []
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted.",
    "Exact duplicate of arith_003."
  ],
  "action": "propose_exclude_duplicate"
}
```


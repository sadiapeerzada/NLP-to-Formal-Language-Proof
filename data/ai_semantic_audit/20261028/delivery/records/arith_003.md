# arith_003: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For any natural numbers a, b, and c, a times (b plus c) equals a times b plus a times c.
```

## Lean type

```lean
theorem mul_distrib_left (a b c : ℕ) : a * (b + c) = a * b + a * c
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal three-natural distributivity; exact semantic duplicate of arith_003_mathlib despite a different theorem name."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "arith_003",
  "theorem": "AuditReference0.mul_distrib_left",
  "source": "data/reference_verification/v0.1.0/references.lean",
  "expected_type": "∀ (a b c : ℕ), a * (b + c) = a * b + a * c",
  "axioms": [],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "arith_003",
  "subject_sha256": "9d67ee341acbb83a8ee3ac483b3a0d79befb98d76dc05353bbd7f22960d46ff3",
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
  "quantifiers": "universal quantification over a, b, c in ℕ",
  "domains": "natural numbers (ℕ)",
  "assumptions": "no additional assumptions",
  "equivalence": "the expected Lean theorem formalizes the English proposition",
  "strength": "the theorem captures the distributive property of multiplication over addition for natural numbers",
  "boundary_cases": "consider the case when a, b, or c is zero",
  "counterexample_search": "no counterexample needed as the proposition is generally true",
  "explanised": "the proposition and the Lean theorem both state the distributive property, which is a fundamental property of multiplication in arithmetic",
  "issues": [
    "the Lean theorem assumes the existence of multiplication and addition operations for natural numbers",
    "the theorem is implicitly using the zero and identity properties of addition and multiplication",
    "the theorem does not address negative cases as natural numbers do not include negative values",
    "the theorem assumes that the operations are well-defined and totalized within Mathlib",
    "the theorem does not explicitly handle the case when b or c is negative, which is outside the scope of natural numbers",
    "the theorem's formalization assumes that all numbers are natural and does not account for the extended arithmetic that includes negative numbers"
  ]
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
  "explanation": "This statement outlines the distributive property of multiplication over addition for natural numbers. It is an elementary arithmetic property that is consistent across different mathematical contexts and is equivalent in Lean and Mathlib.",
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
  "explanation": "This statement outlines the distributive property of multiplication over addition for natural numbers. It is an elementary arithmetic property that is consistent across different mathematical contexts and is equivalent in Lean and Mathlib.",
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
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


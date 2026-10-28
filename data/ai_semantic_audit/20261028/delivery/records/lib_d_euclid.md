# lib_d_euclid: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For a natural prime p and natural numbers a and b, p divides their product if and only if it divides at least one factor.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_euclid (p a b : ℕ) (hp : p.Prime) : p ∣ a * b ↔ p ∣ a ∨ p ∣ b
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural prime p and natural a,b; divisibility of product iff divisibility of at least one factor preserves disjunction and both directions."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_euclid",
  "theorem": "AuditReference14.study_d_euclid",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (p a b : ℕ) (hp : p.Prime), p ∣ a * b ↔ p ∣ a ∨ p ∣ b",
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
  "candidate_id": "lib_d_euclid",
  "subject_sha256": "ceb12a172d8178298ed82c862446e182d16be9cdbaee638a71dd7b42cb7feacf",
  "kind": "exact_bounded_probe",
  "checked_assignments": 486,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Prime-domain sample, iff and disjunction.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
{
  "label": "uncertain",
  "quantifiers": "∀p ∈ ℕ, ∃a, ∃b, (p.Prime ∧ a ≠ 0 ∧ b ≠ ゼロ ∧ (p∣a * b ↔ p∣a ∨ p∣b))",
  "domains": "ℕ, Prime",
  "assumptions": "p is a natural prime, a and b are natural numbers",
  "equivalence": "not equivalent",
  "strength": "the expected Lean theorem is a generalization, not accounting for the zero case",
  "boundary_cases": "p=0, a=0, b=0",
  "counterexample_search": "consider p=0, a=0, b=0; p divides both sides trivially, but the expected theorem fails due to the zero case",
  "explanation": "The provided expected Lean theorem does not account for the case when p is zero, which is a natural restriction in number theory.",
  "issues": [
    "Zero case not addressed",
    "Implicit assumption that p is not zero",
    "Lack of clarity on handling zero",
    "Theorem does not fully capture the natural restriction"
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "uncertain",
  "quantifiers": "∀p ∈ ℕ, ∃a, ∃b, (p.Prime ∧ a ≠ 0 ∧ b ≠ ゼロ ∧ (p∣a * b ↔ p∣a ∨ p∣b))",
  "domains": "ℕ, Prime",
  "assumptions": "p is a natural prime, a and b are natural numbers",
  "equivalence": "not equivalent",
  "strength": "the expected Lean theorem is a generalization, not accounting for the zero case",
  "boundary_cases": "p=0, a=0, b=0",
  "counterexample_search": "consider p=0, a=0, b=0; p divides both sides trivially, but the expected theorem fails due to the zero case",
  "explanation": "The provided expected Lean theorem does not account for the case when p is zero, which is a natural restriction in number theory.",
  "issues": [
    "Zero case not addressed",
    "Implicit assumption that p is not zero",
    "Lack of clarity on handling zero",
    "Theorem does not fully capture the natural restriction"
  ]
}

```


## Phi-4-mini actual judgment

```json
null
```

Schema error: issues must be a string list

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "both sides",
  "domains": "ℕ and p.Prime",
  "assumptions": "p divides a * b iff p divides a or p divides b",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "p = 1, a = 0, b = 0",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and Lean theorem are equivalent in terms of mathematical meaning. Both assert that a natural prime p divides the product of two natural numbers a and b if and only if p divides at least one of a or b. There is no counterexample that refutes this equivalence in the specified domain and assumptions."
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-4 response quality: Frozen schema parse failed; no accepted judgment.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted.",
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


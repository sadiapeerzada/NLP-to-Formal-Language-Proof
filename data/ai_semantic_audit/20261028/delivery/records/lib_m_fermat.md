# lib_m_fermat: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For a natural prime p and integer a, a^p is congruent to a modulo p.
```

## Lean type

```lean
open scoped BigOperators
theorem study_m_fermat (p : ℕ) (hp : p.Prime) (a : ℤ) : Int.ModEq (p : ℤ) (a ^ p) a
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural prime p and integer a; integer exponentiation a^p congruent to a modulo coerced p matches, unlike the p-1 coprime form."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_m_fermat",
  "theorem": "AuditReference14.study_m_fermat",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (p : ℕ) (hp : p.Prime) (a : ℤ), Int.ModEq (p : ℤ) (a ^ p) a",
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
  "candidate_id": "lib_m_fermat",
  "subject_sha256": "2cac61538fee36f8647725eb2c83384e085661cc1f1d3309c01d47e6573640e5",
  "kind": "exact_bounded_probe",
  "checked_assignments": 78,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Integer negative bases, prime modulus.",
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
  "quantifiers": "one each",
  "domains": "ℕ and ℤ",
  "assumptions": "p.Prime and Int.ModEq",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "none",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement accurately describes Fermat's Little Theorem as a statement of number theory. It states that a raised to the power of a prime p is congruent to a modulo p, which is equivalent to a mod p being true in Lean. There is an equivalence in terms of conclusion and mathematical expression. There is no counterexample that refutes the statement as it is a well-known theorem in number theory. There is an equivalence in terms of conclusion and mathematical expression in Lean. There is no counterexample that refutes the statement as it is a well-known theorem in number theory.",
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
  "domains": "ℕ and ℤ",
  "assumptions": "p.Prime and Int.ModEq",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "none",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement accurately describes Fermat's Little Theorem as a statement of number theory. It states that a raised to the power of a prime p is congruent to a modulo p, which is equivalent to a mod p being true in Lean. There is an equivalence in terms of conclusion and mathematical expression. There is no counterexample that refutes the statement as it is a well-known theorem in number theory. There is an equivalence in terms of conclusion and mathematical expression in Lean. There is no counterexample that refutes the statement as it is a well-known theorem in number theory.",
  "issues": []
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Exploratory model did not complete a review; no verdict exists.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "tentatively_retain_subject_to_resolving_all_disagreements"
}
```


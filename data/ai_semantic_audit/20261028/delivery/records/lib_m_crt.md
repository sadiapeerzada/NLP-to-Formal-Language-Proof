# lib_m_crt: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
If natural numbers a and b are congruent modulo gcd(n,m), there exists a natural number congruent to a modulo n and to b modulo m.
```

## Lean type

```lean
open scoped BigOperators
theorem study_m_crt (a b n m : ℕ) (h : Nat.ModEq (Nat.gcd n m) a b) : ∃ k : ℕ, Nat.ModEq n k a ∧ Nat.ModEq m k b
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural a,b,n,m; congruence modulo gcd(n,m) implies one existential natural k satisfying both requested congruences, including zero-modulus equality constraints."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_m_crt",
  "theorem": "AuditReference14.study_m_crt",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b n m : ℕ) (h : Nat.ModEq (Nat.gcd n m) a b), ∃ k : ℕ, Nat.ModEq n k a ∧ Nat.ModEq m k b",
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
  "candidate_id": "lib_m_crt",
  "subject_sha256": "28f331598fecca5ac7728392694d20c625188d560a9eefbbc7b2b6cd80b8d7f6",
  "kind": "exact_bounded_probe",
  "checked_assignments": 443,
  "filtered_by_assumptions": 182,
  "failures": [],
  "note": "Enumerated witnesses include equality constraints for modulus zero; covers finite input grid.",
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
  "quantifiers": "one each a and b, one k",
  "domains": "ℕ",
  "assumptions": "a and b congruent modulo gcd(n,m)",
  "equivalence": "conclusion a congruent modulo n and b congruent modulo m",
  "strength": "same",
  "boundary_cases": "n and m are natural numbers",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement asserts a property of natural numbers and a conclusion about a third number k. The Lean theorem expresses this property formally. Both are equivalent in meaning and strength.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "one each a and b, one k",
  "domains": "ℕ",
  "assumptions": "a and b congruent modulo gcd(n,m)",
  "equivalence": "conclusion a congruent modulo n and b congruent modulo m",
  "strength": "same",
  "boundary_cases": "n and m are natural numbers",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement asserts a property of natural numbers and a conclusion about a third number k. The Lean theorem expresses this property formally. Both are equivalent in meaning and strength.",
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


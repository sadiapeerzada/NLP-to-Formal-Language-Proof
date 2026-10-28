# lib_m_euler: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For coprime natural a and m, a raised to Euler totient(m) is congruent to one modulo m.
```

## Lean type

```lean
open scoped BigOperators
theorem study_m_euler (a m : ℕ) (h : Nat.Coprime a m) : Nat.ModEq m (a ^ Nat.totient m) 1
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural a,m and coprimality; exponent totient(m), residue one and totalized modulus all match the stated version."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_m_euler",
  "theorem": "AuditReference14.study_m_euler",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a m : ℕ) (h : Nat.Coprime a m), Nat.ModEq m (a ^ Nat.totient m) 1",
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
  "candidate_id": "lib_m_euler",
  "subject_sha256": "4ea6fd01be74a6b415839d55b9b8f4e5e459895eb4663f9d00f92fb76a92b15c",
  "kind": "exact_bounded_probe",
  "checked_assignments": 45,
  "filtered_by_assumptions": 36,
  "failures": [],
  "note": "Coprime restriction and totalized modulus zero.",
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
  "domains": "ℕ and Nat.Coprime",
  "assumptions": "h : Nat.Coprime a m",
  "equivalence": "conclusion is equivalent to statement",
  "strength": "same",
  "boundary_cases": "none",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement accurately describes the MÃ©thode d'Euler (also known as Euler's theorem) which states that if a and m are coprime natural numbers, then a raised to the power of the Euler totient of m is congruent to one modulo m. This is equivalent to the expected Lean statement provided that the library import and definition required are met in Mathlib. There is no counterexample that refutes this statement as it is a well-known theorem in number theory.",
  "issues": [
    "The expected Lean statement uses a different notation (^) and mod (mod) than Mathlib's current implementation (under BigOperators and Nat.ModEq). This is a difference in notation but does not reflect an issue with faithfulness as long as equivalent mathematical statements are provable in Mathlib."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "one each",
  "domains": "ℕ and Nat.Coprime",
  "assumptions": "h : Nat.Coprime a m",
  "equivalence": "conclusion is equivalent to statement",
  "strength": "same",
  "boundary_cases": "none",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement accurately describes the MÃ©thode d'Euler (also known as Euler's theorem) which states that if a and m are coprime natural numbers, then a raised to the power of the Euler totient of m is congruent to one modulo m. This is equivalent to the expected Lean statement provided that the library import and definition required are met in Mathlib. There is no counterexample that refutes this statement as it is a well-known theorem in number theory.",
  "issues": [
    "The expected Lean statement uses a different notation (^) and mod (mod) than Mathlib's current implementation (under BigOperators and Nat.ModEq). This is a difference in notation but does not reflect an issue with faithfulness as long as equivalent mathematical statements are provable in Mathlib."
  ]
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Exploratory model did not complete a review; no verdict exists.",
    "Phi-4 response quality: Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


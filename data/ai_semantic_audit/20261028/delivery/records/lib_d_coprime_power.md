# lib_d_coprime_power: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural numbers a and b and a positive natural exponent n, a^n is coprime to b if and only if a is coprime to b.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_coprime_power (a b n : ℕ) (hn : 0 < n) : Nat.Coprime (a ^ n) b ↔ Nat.Coprime a b
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural a,b and positive natural exponent n; iff coprimality matches, with exponent-zero exception excluded."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_coprime_power",
  "theorem": "AuditReference14.study_d_coprime_power",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b n : ℕ) (hn : 0 < n), Nat.Coprime (a ^ n) b ↔ Nat.Coprime a b",
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
  "candidate_id": "lib_d_coprime_power",
  "subject_sha256": "1e8e9e6fea29f58beb2e3400571e0e871aef283fcaacd3504a8e05edf17f42b1",
  "kind": "exact_bounded_probe",
  "checked_assignments": 125,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Positive exponent; n=0 excluded.",
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
  "quantifiers": "∀a, b ∈ ℕ, ∃n ∈ ℕ, 0 < n, (Nat.Coprime a b → Nat.Coprime a ^ n b) → Nat.Coprime a ^ n b",
  "domains": "ℕ, ℕ, ℕ",
  "assumptions": "0 < n",
  "equivalence": "not equivalent",
  "strength": "the Lean theorem does not account for the case when n = 0, which is implicitly excluded in the English statement",
  "boundary_cases": "n = 0, n = 1, and large n",
  "counterexample_search": "consider a = 2, b = 4, n = 0",
  "explanised": "the English statement excludes the case where n = 0, which the Lean theorem does not, potentially leading to a discrepency",
  "issues": [
    "implicit assumption that n > 0 in the English statement",
    "Lean theorem does not explicitly exclude n = 0, which could lead to a different conclusion for this case",
    "English statement lacks clarity on the treatment of n = 0",
    "Lean theorem's strength is not fully aligned with the English proposition due to the handling of n = 0"
  ]
}



























































































































































































































































































































































































































































































































































































```


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "both sides",
  "domains": "both sides",
  "assumptions": "both sides",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and Lean theorem are equivalent in terms of mathematical meaning. Both assert that a^n is coprime to b if and only if a is coprime to b, under the assumption that n is a positive natural number. There is no difference in the scope of quantifiers, variable domains, or assumptions on either side. The conclusion on both sides is equivalent. There is a specific boundary case check on n being positive. There is no counterexample that refutes the equivalence.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "both sides",
  "domains": "both sides",
  "assumptions": "both sides",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and Lean theorem are equivalent in terms of mathematical meaning. Both assert that a^n is coprime to b if and only if a is coprime to b, under the assumption that n is a positive natural number. There is no difference in the scope of quantifiers, variable domains, or assumptions on either side. The conclusion on both sides is equivalent. There is a specific boundary case check on n being positive. There is no counterexample that refutes the equivalence.",
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
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


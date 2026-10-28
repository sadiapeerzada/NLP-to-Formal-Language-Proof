# lib_d_dvd_antisymmetry: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
If two natural numbers divide each other, they are equal.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_dvd_antisymmetry (a b : ℕ) (hab : a ∣ b) (hba : b ∣ a) : a = b
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal natural a,b and mutual divisibility premises; equality conclusion needs the natural domain, unlike signed integers."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_dvd_antisymmetry",
  "theorem": "AuditReference14.study_d_dvd_antisymmetry",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b : ℕ) (hab : a ∣ b) (hba : b ∣ a), a = b",
  "axioms": [
    "propext"
  ],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "lib_d_dvd_antisymmetry",
  "subject_sha256": "3c62ea19654d90d5c19782d53f88d916a4ce9d9f4dcf7e903775bbf9db3ed2a7",
  "kind": "exact_bounded_probe",
  "checked_assignments": 9,
  "filtered_by_assumptions": 72,
  "failures": [],
  "note": "Two divisibility assumptions.",
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
  "label": "not faithful",
  "quantifiers": "universal quantification over ℕ",
  "domains": "natural numbers, real numbers, and BigOperators",
  "assumptions": "divisibility in ℕ",
  "equivalence": "none, as the proposition is incorrect",
  "strength": "the proposition is stronger than the general mathematical principle of antisymmetry in divisibility",
  "boundary_cases": "considering the case when a and b are powers of the same number",
  "counterexample_search": "a = 2^3, b = 2^2",
  "counterexample": "a = 8, b = 4, where a divides b and b divides a, but a ≠ b",
  "issues": [
    "The proposition incorrectly generalizes the antisymmetry property of divisibility.",
    "The English statement lacks the necessary exclusivity for the case when a equals b.",
    "The proposition does not account for the scenario where a and b are powers of the same number.",
    "The Lean theorem formulation incorrectly assumes a = b from the given divisibility.",
    "The proposition ignores the possibility of zero or negative values, which are not defined in the context of natural numbers."
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
  "label": "not faithful",
  "quantifiers": "one each",
  "domains": "ℕ",
  "assumptions": "hab and hba",
  "equivalence": "conclusion a = b",
  "strength": "stronger",
  "boundary_cases": "endpoints",
  "counterexample_search": "specific candidate example",
  "explanation": "The English statement asserts a property of natural numbers that is not true in general. However, the Lean theorem is true under the assumption that a and b are natural numbers and a divides b and b divides a. This is a stricter condition than just being divisors (hab and hba), which implies a = b."
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Phi-4 response quality: Frozen schema parse failed; no accepted judgment.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


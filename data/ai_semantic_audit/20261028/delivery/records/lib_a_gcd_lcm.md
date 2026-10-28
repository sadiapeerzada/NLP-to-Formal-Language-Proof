# lib_a_gcd_lcm: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural numbers a and b, their greatest common divisor times their least common multiple equals their product.
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_gcd_lcm (a b : ℕ) : Nat.gcd a b * Nat.lcm a b = a * b
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural a,b including zeros; gcd*lcm=a*b, with no positivity premise in either text."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_gcd_lcm",
  "theorem": "AuditReference14.study_a_gcd_lcm",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b : ℕ), Nat.gcd a b * Nat.lcm a b = a * b",
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
  "candidate_id": "lib_a_gcd_lcm",
  "subject_sha256": "b67b16fb3450615b06611791b0a0e30f3e9643080753e8be005a542afc18184b",
  "kind": "exact_bounded_probe",
  "checked_assignments": 81,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Includes (0,0).",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 18 column 1 (char 945)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "universal quantification over ℕ for a and b",
  "domains": "ℕ for a and b",
  "assumptions": "no additional assumptions",
  "equivalence": "the English proposition does not account for zero and negative cases",
  "strength": "the English proposition is a weaker statement than the Lean theorem",
  "boundary_cases": "the English proposition does not address the case when one or both numbers are zero",
  "counterexample_search": "consider a = 0, b = ∞ (undefined in ℕ)",
  "explanised": "the English proposition implicitly assumes that both a and b are positive, while the Lean theorem is totalized to handle all natural numbers, including zero",
  "issues": [
    "omission of zero and negative cases",
    "implicit assumption of positive integers",
    "lack of clarity on handling undefined or infinite values",
    "misalignment with the Lean theorem's handling of all natural numbers"
  ]
}
```
````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each",
  "domains": "ℕ",
  "assumptions": "a and b are natural numbers",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "checked endpoints and zero",
  "counterexample_search": "no found counterexample",
  "explanation": "The statement is an established theorem in number theory and is equivalent in both English and Lean. It assumes a and b are natural numbers and directly follows from the definitions of gcd and lcm in Mathlib. There is no difference in scope, variable domains, or assumptions between the English statement and the expected Lean statement. The conclusion directly equates the product of a and b to the gcd of a and b times the lcm of a and b, which is consistent with the expected result in Mathlib.",
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
  "domains": "ℕ",
  "assumptions": "a and b are natural numbers",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "checked endpoints and zero",
  "counterexample_search": "no found counterexample",
  "explanation": "The statement is an established theorem in number theory and is equivalent in both English and Lean. It assumes a and b are natural numbers and directly follows from the definitions of gcd and lcm in Mathlib. There is no difference in scope, variable domains, or assumptions between the English statement and the expected Lean statement. The conclusion directly equates the product of a and b to the gcd of a and b times the lcm of a and b, which is consistent with the expected result in Mathlib.",
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
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "tentatively_retain_subject_to_resolving_all_disagreements"
}
```


# lib_m_residue_product: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural a,b,m, the remainder of a*b modulo m equals the remainder of the product of their separate remainders modulo m, including when m is zero.
```

## Lean type

```lean
open scoped BigOperators
theorem study_m_residue_product (a b m : ℕ) : (a * b) % m = ((a % m) * (b % m)) % m
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural a,b,m; both sides have outer remainder modulo m, including m=0 as explicitly requested."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_m_residue_product",
  "theorem": "AuditReference14.study_m_residue_product",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b m : ℕ), (a * b) % m = ((a % m) * (b % m)) % m",
  "axioms": [
    "propext"
  ],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "lib_m_residue_product",
  "subject_sha256": "bb9717c53bc34f2c4c21424ae0aa061167e2308976726299ce92319678e1b49b",
  "kind": "exact_bounded_probe",
  "checked_assignments": 729,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Modulus zero remainder identity.",
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
  "quantifiers": "one each a, b, m",
  "domains": "ℕ",
  "assumptions": "modulo definition and multiplicative property",
  "equivalence": "conclusion is equivalent to expected statement",
  "strength": "same",
  "boundary_cases": "m is zero",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The statement is true under the definition of modulo and multiplicative property, including case when m is zero.",
  "issues": [
    "Lean Nat subtraction is truncated; division and remainders are totalized."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "one each a, b, m",
  "domains": "ℕ",
  "assumptions": "modulo definition and multiplicative property",
  "equivalence": "conclusion is equivalent to expected statement",
  "strength": "same",
  "boundary_cases": "m is zero",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The statement is true under the definition of modulo and multiplicative property, including case when m is zero.",
  "issues": [
    "Lean Nat subtraction is truncated; division and remainders are totalized."
  ]
}
```
````


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


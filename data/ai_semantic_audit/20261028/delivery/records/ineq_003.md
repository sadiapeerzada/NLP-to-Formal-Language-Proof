# ineq_003: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For any natural number n at least 1, n plus 1 is at most 2 to the power n.
```

## Lean type

```lean
theorem succ_le_two_pow (n : ℕ) (h : 1 ≤ n) : n + 1 ≤ 2 ^ n
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural n and 1<=n are both present; n+1<=2^n is non-strict as requested."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "ineq_003",
  "theorem": "AuditReference0.succ_le_two_pow",
  "source": "data/reference_verification/v0.1.0/references.lean",
  "expected_type": "∀ (n : ℕ) (h : 1 ≤ n), n + 1 ≤ 2 ^ n",
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
  "candidate_id": "ineq_003",
  "subject_sha256": "0bd0c727f029a86fecae68ae7e4d787433627ded41f7beef0e82f43647bbf83e",
  "kind": "exact_bounded_probe",
  "checked_assignments": 8,
  "filtered_by_assumptions": 1,
  "failures": [],
  "note": "Only n>=1 accepted by theorem.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Missing substantive field: quantifiers

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "not faithful",
  "quantifiers": {
    "SUBJECT_JSON": "For any natural number n at least 1",
    "expected_lean_statement": "n + ized with '∀ n ≥ 1' and 'n + 1 ≤ 2^n'"
  },
  "domains": {
    "SUBJECT_JSON": "natural number",
    "expected_lean_statement": "ℕ",
    "issues": [
      "Natural number domain should specify 'n ≥ 1' in the hypothesis to match the English statement."
    ]
  },
  "assumptions": {
    "SUBJECT_JSON": null,
    "expected_lean_statement": "h : 1 ≤ n",
    "issues": [
      "Explicit hypothesis required for the domain of 'n'."
    ]
  },
  "equivalence": "uncertain",
  "strength": "the subject proposition is weaker than the Lean theorem",
  "boundary_cases": "n = 1",
  "counterexample_search": "n = 1",
  "explanation": "The subject proposition fails for n = 1, as 1 + 1 is not ≤ 2^1.",
  "issues": [
    "SUBJECT_JSON proposition does not account for the base case n = 1.",
    "SUBJECT_JSON lacks a clear hypothesis.",
    "SUBJECT_JSON's domain is too broad without specifying 'n ≥ 1'."
  ]
}

```


## Phi-4-mini actual judgment

```json
{
  "label": "not faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts an inequality that is not true for all natural numbers n. It suggests that n+1 is less than or equal to 2 raised to the power of n, which is not true as n increases. This inequality is not universally valid in natural numbers and is therefore not faithfully equivalent to a statement that would be true in Lean's Nat subtraction and division operations.",
  "issues": [
    "The inequality n+1 ≤ 2^n is not true for all natural numbers n. It is true for n=1 but fails for n>1 (e.g., n=2 gives n+1=3 and 2^n=4, which does not satisfy the inequality).",
    "The expected Lean statement is not a theorem in Lean's Natural numbers library as written but would be true if written as n+1 ≤ 2^n for n ≥ 1."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "not faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts an inequality that is not true for all natural numbers n. It suggests that n+1 is less than or equal to 2 raised to the power of n, which is not true as n increases. This inequality is not universally valid in natural numbers and is therefore not faithfully equivalent to a statement that would be true in Lean's Nat subtraction and division operations.",
  "issues": [
    "The inequality n+1 ≤ 2^n is not true for all natural numbers n. It is true for n=1 but fails for n>1 (e.g., n=2 gives n+1=3 and 2^n=4, which does not satisfy the inequality).",
    "The expected Lean statement is not a theorem in Lean's Natural numbers library as written but would be true if written as n+1 ≤ 2^n for n ≥ 1."
  ]
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
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


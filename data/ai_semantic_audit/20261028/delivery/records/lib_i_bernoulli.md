# lib_i_bernoulli: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For any real x at least -1 and natural number n, 1+n*x is at most (1+x)^n.
```

## Lean type

```lean
open scoped BigOperators
theorem study_i_bernoulli (x : ℝ) (n : ℕ) (h : -1 ≤ x) : 1 + (n : ℝ) * x ≤ (1 + x) ^ n
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Real x>=-1 and natural n; coercion of n to real is explicit and preserves 1+n*x <= (1+x)^n."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_i_bernoulli",
  "theorem": "AuditReference14.study_i_bernoulli",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x : ℝ) (n : ℕ) (h : -1 ≤ x), 1 + (n : ℝ) * x ≤ (1 + x) ^ n",
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
  "candidate_id": "lib_i_bernoulli",
  "subject_sha256": "752ce7e171b20bdfc06ead1df7345497af13efd25eeaa10c3d3b6d4c53f72486",
  "kind": "exact_bounded_probe",
  "checked_assignments": 81,
  "filtered_by_assumptions": 36,
  "failures": [],
  "note": "Exact rational real subset; x>=-1.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 32 column 1 (char 1503)

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "uncertain",
  "quantifiers": {
    "subject": "forall x ≥ -1 and n ∈ ℕ, 1 + n*x ≤ (1 + x)^n",
    "expected": "forall x ≥ -1 and n ∈ ℕ, 1 + (n : 才能 * x) ≤ (1 + x)^n"
  },
  "domains": {
    "subject": "ℝ for x, ℕ for n",
    "expected": "ℝ for x, ℕ for n"
  },
  "assumptions": {
    "subject": "h : -1 ≤ x",
    "expected": "h : -1 ≤ x"
  },
  "equivalence": "not equivalent",
  "strength": "the subject lacks clarity on the domain of n, potentially limiting its generality",
  "boundary_cases": "not specified, could affect the theorem's application",
  "counterexample_search": "no concrete counterexample provided, but the subject may fail for n = 0",
  "explanency": "the subject assumes multiplication and exponentiation are defined for the domains, which is true, but lacks rigorous formalization",
  "issues": [
    "ambiguous definition of multiplication and exponentiation for n*x and (1 + x)^n",
    "scope of quantifiers is not clear, especially for n",
    "implicit assumption that n*x and (1 + x)^n are well-defined for all n and x in the domains",
    "missing formalization of zero and negative cases for n",
    "absence of a formal proof or method, only a statement is provided",
    "subject does not match the expected formal Lean theorem structure",
    "potential issue with the interpretation of 'at most'",
    "missing explicit handling of the case when x = 0",
    "no mention of Mathlib's totalization, which could be relevant for rigorous formalization"
  ]
}
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
  "quantifiers": "one each on left and right",
  "domains": "ℝ and ℕ",
  "assumptions": "x is real and n is natural",
  "equivalence": "conclusion is equivalent",
  "strength": "stronger",
  "boundary_cases": "x=-1 and n=0",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement is equivalent to the Lean theorem but is stronger due to an omitted domain restriction on x."
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


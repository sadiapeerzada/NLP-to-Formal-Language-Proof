# ineq_001: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For any natural number n, n is at most n squared.
```

## Lean type

```lean
theorem sq_ge_self (n : ℕ) : n ≤ n ^ 2
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal natural n and non-strict n<=n^2, including equality at n=0 and n=1."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "ineq_001",
  "theorem": "AuditReference0.sq_ge_self",
  "source": "data/reference_verification/v0.1.0/references.lean",
  "expected_type": "∀ (n : ℕ), n ≤ n ^ 2",
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
  "candidate_id": "ineq_001",
  "subject_sha256": "bdee887e37866d3fa67f3c81e745898d2251c88287cec8cb9c0f8536596b679a",
  "kind": "exact_bounded_probe",
  "checked_assignments": 9,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Zero and one equality endpoints.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 20 column 1 (char 1358)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "universal quantifier on n",
  "domains": "natural numbers (ℕ)",
  "assumptions": "none specified",
  "equivalence": "the English proposition is not equivalent to the formalized Lean theorem",
  "strength": "the English proposition is weaker than the Lean theorem",
  "boundary_cases": "consider the case when n is 1, the proposition holds but the Lean theorem asserts n ≤ n^2 for all n",
  "counterexample_search": "no counterexample; the English proposition is a subset of the Lean theorem",
  "explanised": "the English proposition lacks consideration of the base case (n=1), which is trivially true, but the Lean theorem includes it as part of its general case",
  "issues": [
    "The English proposition implicitly assumes a domain of natural numbers without explicitly stating it.",
    "The English proposition does not account for the base case n=1, which is trivially true but not addressed in the Lean theorem.",
    "The Lean theorem is more general and includes the base case, making it stronger in the sense of mathematical formalization.",
    "The English proposition could be considered faithful to the Lean theorem if it were to explicitly include the base case.",
    "The Lean theorem's strength lies in its universality and inclusion of all natural numbers, including the base case."
  ]
}

```json
{
  "label": "not faithful",
  "quantifiers": "∀n ∈ ℕ",
  "domains": "ℕ",
  "assumptions": "none, implicit assumption that n is a natural number",
  "equivalence": "the English proposition is not equivalent to the formalized Lean theorem",
  "strength": "the English proposition is weaker than the Lean theorem",
  "boundary_cases": "n=1",
  "counterexample_search": "no counterexample, the English proposition is a subset of the Lean theorem",
  "explanation": "the English proposition is incomplete as it does not address the base case n=1, which is trivially true and included in the Lean theorem.",
  "issues": [
    "Lack of explicit domain specification in the English proposition.",
    "English proposition does not explicitly include the base case n=1.",
    "Lean theorem is more comprehensive and universally applicable.",
    "English proposition could be considered faithful with explicit inclusion of the base case.",
    "Strength of the Lean theorem lies in its complete formalization."
  ]
}
}
```
````


## Phi-4-mini actual judgment

```json
{
  "label": "not faithful",
  "quantifiers": "one each",
  "domains": "ℕ",
  "assumptions": "none",
  "equivalence": "weaker",
  "strength": "weaker",
  "boundary_cases": "none",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property that is not universally true for all natural numbers n. It is equivalent to stating n is less than or equal to n squared (n ≤ n^2), which is true but not a meaningful inequality as n is always less than or equal to n squared (n ≤ n^2 is an obvious inequality). The Lean theorem is equivalent to stating n is less than or equal to n squared (n ≤ n^2), which is true but trivial and not meaningful in this context.",
  "issues": [
    "The inequality is trivial and not meaningful in this context.",
    "The English statement is equivalent to stating n is less than or equal to n squared (n ≤ n^2), which is true but trivial."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "not faithful",
  "quantifiers": "one each",
  "domains": "ℕ",
  "assumptions": "none",
  "equivalence": "weaker",
  "strength": "weaker",
  "boundary_cases": "none",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property that is not universally true for all natural numbers n. It is equivalent to stating n is less than or equal to n squared (n ≤ n^2), which is true but not a meaningful inequality as n is always less than or equal to n squared (n ≤ n^2 is an obvious inequality). The Lean theorem is equivalent to stating n is less than or equal to n squared (n ≤ n^2), which is true but trivial and not meaningful in this context.",
  "issues": [
    "The inequality is trivial and not meaningful in this context.",
    "The English statement is equivalent to stating n is less than or equal to n squared (n ≤ n^2), which is true but trivial."
  ]
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Phi-4 response quality: Prompt placeholder copied into counterexample_search.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted.",
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


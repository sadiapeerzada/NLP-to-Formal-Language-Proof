# lib_i_catalan: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every natural n, the (n+1)st Catalan number is the sum of C(i)*C(n-i) over natural i from zero through n.
```

## Lean type

```lean
open scoped BigOperators
theorem study_i_catalan (n : ℕ) : catalan (n + 1) = ∑ i : Fin n.succ, catalan i * catalan (n - i)
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal natural n; Fin(n+1) enumerates exactly i=0..n and coerces to Nat in C(i), C(n-i), matching convolution endpoints."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_i_catalan",
  "theorem": "AuditReference15.study_i_catalan",
  "source": "data/curation_batches/v0.2.1/references_expanded.lean",
  "expected_type": "∀ (n : ℕ), catalan (n + 1) = ∑ i : Fin n.succ, catalan i * catalan (n - i)",
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
  "candidate_id": "lib_i_catalan",
  "subject_sha256": "2992db4e1798e41d084eba7bd2985753139e7b9b1cc8481839657392efdb2f10",
  "kind": "exact_bounded_probe",
  "checked_assignments": 9,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Closed-form Catalan implementation vs convolution.",
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
  "quantifiers": "C(i) summing over i in Fin n.succ",
  "domains": "C(i) and catalan (n - i) are Catalan numbers",
  "assumptions": "n is a natural number",
  "equivalence": "conclusion is equivalent to expected Lean statement",
  "strength": "stronger",
  "boundary_cases": "n is a natural number",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement accurately describes the recursive formula for Catalan numbers in terms of binomial coefficients, which is equivalent to the expected Lean statement that defines the (n+1)th Catalan number as a sum of products of consecutive Catalan numbers.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "C(i) summing over i in Fin n.succ",
  "domains": "C(i) and catalan (n - i) are Catalan numbers",
  "assumptions": "n is a natural number",
  "equivalence": "conclusion is equivalent to expected Lean statement",
  "strength": "stronger",
  "boundary_cases": "n is a natural number",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement accurately describes the recursive formula for Catalan numbers in terms of binomial coefficients, which is equivalent to the expected Lean statement that defines the (n+1)th Catalan number as a sum of products of consecutive Catalan numbers.",
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


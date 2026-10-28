# lib_a_sqrt_square: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For a nonnegative real number x, the square of its principal square root is x.
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_sqrt_square (x : ℝ) (h : 0 ≤ x) : (Real.sqrt x) ^ 2 = x
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Real x with nonnegativity premise; principal sqrt squared equals x, not sqrt(x^2)=x."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_sqrt_square",
  "theorem": "AuditReference14.study_a_sqrt_square",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x : ℝ) (h : 0 ≤ x), (Real.sqrt x) ^ 2 = x",
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
  "candidate_id": "lib_a_sqrt_square",
  "subject_sha256": "aabfab7dd32fd6d1d6a04578dac4734220646066eed56149dfcfc3a9cc497a34",
  "kind": "approximate_numeric_probe",
  "checked_assignments": 7,
  "filtered_by_assumptions": 6,
  "failures": [],
  "note": "Floating approximation, x>=0 only; not exact real verification.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 19 column 1 (char 1146)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "universal quantifier on x with existential quantifier on h",
  "domains": "x in ℝ, h in {0 ≤ x}",
  "assumptions": "x is nonnegative",
  "equivalence": "the provided Lean theorem does not account for all necessary cases and assumptions",
  "strength": "the theorem is weaker than expected as it does not address negative values of x",
  "boundary_cases": "the theorem does not handle the case when x is zero",
  "counterexample_search": "consider x = 0, where the principal square root is not defined in the same way",
  "explanised": "the Lean theorem assumes x is nonnegative and h is trivially true, but it does not cover the case when x is negative or zero, which is a necessary consideration for a complete formalization",
  "issues": [
    "omission of handling negative values of x",
    "lack of definition for the principal square root at x = 0",
    "missing consideration for the zero case",
    "the theorem does not fully capture the original proposition's intent due to restricted domain",
    "the theorem's scope is insufficient without addressing the zero and negative cases"
  ]
}
```

The provided JSON indicates that the Lean theorem is "not faithful" to the English proposition because it does not account for all necessary cases, particularly the case when x is negative or zero. The theorem assumes x is nonnegative and h (the existence of the principal square root) is trivially true within the nonnegative domain, but it fails to address the proposition's requirements for all real numbers, including negative values and the zero case. The Lean theorem's domain is implicitly restricted to nonnegative reals, which is a strength mismatch with the more general proposition that expects the behavior for all real numbers. The theorem lacks a definition for the principal square root at x = 0 and does not address the behavior when x is negative, which are essential considerations for a complete formalization. The omission of these cases is a significant limitation, making the theorem weaker than expected.

```json
{
  "label": "not faithful",
  "quantifiers": "∀x ∈ ℝ, ∃h (0 ≤ x → (Real.sqrt x)^2 = x)",
  "domains": "x ∈ ℝ, h : {0 ≤ x}",
  "assumptions": "missing consideration for x < 0 and x = 0",
  "equivalence": "the theorem does not fully capture the original proposition's intent",
  "strength": "the theorem is weaker due to its restricted domain and lack of handling negative and zero cases",
  "boundary_cases": "undefined behavior for x < 0 and x = 0",
  "counterexample_search": "x < 0 or x = 0",
  "explanation": "the Lean theorem's domain and treatment of boundary cases do not align with the proposition's requirements for all real numbers",
  "issues": [
    "omission of handling negative values of x",
    "lack of definition for the principal square root at x = 0",
    "missing consideration for the zero case",
    "the theorem does not fully capture the original proposition's intent due to restricted domain",
    "the theorem's scope is insufficient without addressing the zero and negative cases"
  ]
}
```
````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each",
  "domains": "Real numbers",
  "assumptions": "x is a nonnegative real number",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "x is zero",
  "counterexample_search": "no found counterexample",
  "explanation": "The statement is true as per Mathlib conventions and is equivalent to the expected Lean statement.",
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
  "domains": "Real numbers",
  "assumptions": "x is a nonnegative real number",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "x is zero",
  "counterexample_search": "no found counterexample",
  "explanation": "The statement is true as per Mathlib conventions and is equivalent to the expected Lean statement.",
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


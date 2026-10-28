# lib_q_triangle: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For real x and y, the absolute value of x+y is at most the sum of their absolute values.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_triangle (x y : ℝ) : |x + y| ≤ |x| + |y|
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Two universal reals; non-strict triangle inequality with each separate absolute value."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_triangle",
  "theorem": "AuditReference14.study_q_triangle",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x y : ℝ), |x + y| ≤ |x| + |y|",
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
  "candidate_id": "lib_q_triangle",
  "subject_sha256": "fef2725294fb4f49201fa4ac730bbd709d6afaba10467c9c9bd0fe8466fe28bf",
  "kind": "exact_bounded_probe",
  "checked_assignments": 169,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Absolute values, no sign assumptions.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Missing substantive field: domains

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "uncertain",
  "quantifiers": "∀x ∈ ℝ, ∀y ∈ ℝ",
  "domains": {
    "x": "ℝ",
    "y": "ℝ"
  },
  "assumptions": "None specified",
  "equivalence": "The English proposition suggests a general case, while the Lean theorem specifies real numbers, potentially excluding complex numbers.",
  "strength": "The Lean theorem is more specific but assumes real numbers, potentially excluding the general case.",
  "boundary_cases": "The proposition does not account for zero or negative values, while the Lean theorem includes them.",
  "counterexample_search": "The proposition holds for all real numbers, including zero and negatives, but the Lean theorem is more restrictive.",
  "explanised": "The English proposition implies a general case, while the Lean theorem is more specific, assuming real numbers.",
  "issues": [
    "The Lean theorem restricts the domain to real numbers, potentially excluding complex numbers.",
    "The proposition does not explicitly handle zero or negative values, while the Lean theorem does.",
    "The Lean theorem's strictness may exclude cases not covered by the general proposition."
  ]
}

```


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a well-known inequality in real numbers, which is equivalent to a Lean theorem stating that the absolute value of the sum of two real numbers is less than or equal to the sum of their absolute values. This is a standard inequality covered in real analysis and is consistent with the expected Lean statement.",
  "issues": [
    "The English statement assumes the variables x and y are real numbers, which is not explicitly stated in the Lean theorem but can be inferred from the context.",
    "The Lean theorem uses the notation 'open scoped BigOperators' which indicates that it is a statement within a specific scope in Mathlib, but this does not impact the mathematical equivalence.",
    "The Lean statement does not explicitly import Mathlib or define required terms, which may be an oversight but does not affect the mathematical equivalence."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a well-known inequality in real numbers, which is equivalent to a Lean theorem stating that the absolute value of the sum of two real numbers is less than or equal to the sum of their absolute values. This is a standard inequality covered in real analysis and is consistent with the expected Lean statement.",
  "issues": [
    "The English statement assumes the variables x and y are real numbers, which is not explicitly stated in the Lean theorem but can be inferred from the context.",
    "The Lean theorem uses the notation 'open scoped BigOperators' which indicates that it is a statement within a specific scope in Mathlib, but this does not impact the mathematical equivalence.",
    "The Lean statement does not explicitly import Mathlib or define required terms, which may be an oversight but does not affect the mathematical equivalence."
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
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


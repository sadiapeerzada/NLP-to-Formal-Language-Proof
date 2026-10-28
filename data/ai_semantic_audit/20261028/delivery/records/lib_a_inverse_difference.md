# lib_a_inverse_difference: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For nonzero real numbers x and y, 1/x minus 1/y equals (y-x)/(x*y).
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_inverse_difference (x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0) : 1 / x - 1 / y = (y - x) / (x * y)
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Real nonzero x and y explicitly assumed; reciprocal difference numerator is y-x and denominator is x*y."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_inverse_difference",
  "theorem": "AuditReference14.study_a_inverse_difference",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0), 1 / x - 1 / y = (y - x) / (x * y)",
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
  "candidate_id": "lib_a_inverse_difference",
  "subject_sha256": "19c18317038216910471e54b1e7a68e31b71663314490257c817bc8264cc7e2c",
  "kind": "exact_bounded_probe",
  "checked_assignments": 144,
  "filtered_by_assumptions": 25,
  "failures": [],
  "note": "Exact rational reciprocal; zeros excluded.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Expecting ',' delimiter: line 13 column 5 (char 365)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": {
    "SUBJECT_JSON": "For nonzero real numbers x and y",
    "expected_lean_statement": "x ≠ 0 and y ≠ 0"
  },
  "domains": {
    "SUBJECT_JSON": "nonzero real numbers",
    "expected_lean_statement": "ℝ \u2200 x:e ≠ 0 \u2227 y:e ≠ 0"
  },
  "assumptions": {
    "SUBJECT_JSON": "1/x minus 1/y equals (y-x)/(x*y)"
    "expected_lean_statement": "1 / x - 1 / y \u2260 (y - x) / (x * y)"
  },
  "equivalence": "not equivalent",
  "strength": "SUBJECT_JSON proposes a stronger statement than expected",
  "boundary_cases": "SUBJECT_JSON does not account for x or y approaching zero",
  "counterexample_search": "Consider x = ε, y = 1/ε where ε is a small positive real number; the left side approaches infinity while the right side approaches 0, disproving the equivalence.",
  "explanation": "The SUBJECT_JSON proposition lacks the necessary exclusions for x and y being zero, which is critical for the correctness of the operation.",
  "issues": [
    "Implicit quantifier scope",
    "Incorrect equivalence",
    "Missing exclusions for zero values",
    "Lack of boundary case consideration",
    "Incorrect handling of division by zero"
  ]
}
```
````


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
  "explanation": "The English statement and the Lean theorem are equivalent in terms of mathematical meaning. Both assert that for nonzero real numbers x and y, the expression 1/x minus 1/y is equivalent to (y-x)/(x*y). There is no difference in the scope of quantifiers, variable domains, assumptions, or conclusion between the English statement and the Lean theorem. The required imports are consistent, and there is an expectation of equivalence in conclusion. There is a specific boundary case check on nonzero values since division by zero is undefined in ℝ. There is no counterexample that refutes the equivalence in this case.",
  "issues": [
    "The English statement uses a less conventional notation (1/x minus 1/y versus (y-x)/(x*y) which may lead to confusion but does not change the mathematical equivalence."
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
  "explanation": "The English statement and the Lean theorem are equivalent in terms of mathematical meaning. Both assert that for nonzero real numbers x and y, the expression 1/x minus 1/y is equivalent to (y-x)/(x*y). There is no difference in the scope of quantifiers, variable domains, assumptions, or conclusion between the English statement and the Lean theorem. The required imports are consistent, and there is an expectation of equivalence in conclusion. There is a specific boundary case check on nonzero values since division by zero is undefined in ℝ. There is no counterexample that refutes the equivalence in this case.",
  "issues": [
    "The English statement uses a less conventional notation (1/x minus 1/y versus (y-x)/(x*y) which may lead to confusion but does not change the mathematical equivalence."
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


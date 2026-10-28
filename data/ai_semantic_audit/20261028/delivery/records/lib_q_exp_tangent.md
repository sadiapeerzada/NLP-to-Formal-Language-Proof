# lib_q_exp_tangent: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every real x, x+1 is at most exp(x).
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_exp_tangent (x : ℝ) : x + 1 ≤ Real.exp x
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal real x; non-strict x+1<=exp(x) with no positivity restriction matches."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_exp_tangent",
  "theorem": "AuditReference14.study_q_exp_tangent",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x : ℝ), x + 1 ≤ Real.exp x",
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
  "candidate_id": "lib_q_exp_tangent",
  "subject_sha256": "46f342469c745c362afdf0c9361cfde77e356cca7a613bf1b9cbcc88cb253dfe",
  "kind": "approximate_numeric_probe",
  "checked_assignments": 13,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Floating exponential grid only.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Invalid \escape: line 5 column 39 (char 126)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": {
    "SUBJECT_JSON": "For every real x",
    "expected_lean_statement": "x : ℝ \vdash x + ized ≤ Real.exp x"
  },
  "domains": {
    "SUBJECT_JSON": "real",
    "expected_lean_statement": "(x : ℝ) - Real.scope"
  },
  "assumptions": {
    "SUBJECT_JSON": "None specified",
    "expected_lean_statement": "(x : ℝ) - Prop"
  },
  "equivalence": "The domains and quantifiers suggest a comparison, but the equivalence is unclear due to potential misinterpretation of the Lean syntax.",
  "strength": "The subject proposition lacks clarity in quantifier scope and domain specification.",
  "boundary_cases": "The subject proposition does not address the behavior at infinity or negative infinity.",
  "counterexample_search": "Consider x = -∞, where the subject proposition implies x + 1 ≤ 0, which is false.",
  "explanised": "The subject proposition implicitly assumes properties of real numbers that are not specified, such as the behavior of the exponential function at extreme values.",
  "issues": [
    "Ambiguity in quantifier scope",
    "Implicit domain specification without explicit definition",
    "Lack of clarity in equivalence",
    "No consideration of boundary cases",
    "Potential misinterpretation of Lean syntax",
    "Absence of assumptions definition",
    "No provided counterexample to test the proposition's validity"
  ]
}
```

The subject proposition is not faithfully represented by the expected Lean theorem due to several reasons:

1. **Quantifiers and Domains**: The subject proposition uses "every real x," suggesting a universal quantifier, but the expected Lean statement uses "x : ℝ," which is correct. However, the Lean syntax for the inequality suggests a potential misinterpretation, as "x + ized" is not standard and may be a typo.

2. **Equivalence**: The equivalence between the subject and expected Lean statements is unclear due to potential syntactical errors in the Lean statement.

3. **Strength**: The subject proposition is weaker because it does not specify the domain of the variable x, leaving it ambiguous.

4. **Boundary Cases**: The subject proposition does not consider the behavior of the function at extreme values of x, such as negative infinity, which is crucial for statements involving exponential functions.

5. **Counterexample Search**: A concrete counterexample is provided with x = -∞, demonstrating that the subject proposition is false.

6. **Explanation**: The subject proposition implicitly assumes properties of real numbers that are not specified, such as the behavior of the exponential function at extreme values.

7. **Issues**:
   - Ambiguity in quantifier scope
   - Implicit domain specification without explicit definition
   - Lack of clarity in equivalence
   - No consideration of boundary cases
   - Potential misinterpretation of Lean syntax
   - Absence of assumptions definition
   - No provided counterexample to test the proposition's validity

The subject proposition is not a faithful formalization of the English proposition, as it lacks clarity and precision in several key areas. The subject proposition would need to be corrected to include explicit domain specification, clarify the meaning of the inequality, and address boundary cases to be considered a faithful formalization.
````


## Phi-4-mini actual judgment

```json
{
  "label": "not faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "stronger, than requested",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a specific inequality between x+1 and Real.exp x for every real number x. However, the Lean theorem provided does not explicitly assert this inequality but rather defines a property of the Real.exp function in a general setting without a direct inequality comparison. This makes the statement not faithful in terms of direct equivalence.",
  "issues": [
    "The Lean theorem does not directly assert the inequality x+1 ≤ Real.exp x as requested in the English statement.",
    "The inequality is not explicitly stated in the Lean theorem provided."
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
  "strength": "stronger, than requested",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a specific inequality between x+1 and Real.exp x for every real number x. However, the Lean theorem provided does not explicitly assert this inequality but rather defines a property of the Real.exp function in a general setting without a direct inequality comparison. This makes the statement not faithful in terms of direct equivalence.",
  "issues": [
    "The Lean theorem does not directly assert the inequality x+1 ≤ Real.exp x as requested in the English statement.",
    "The inequality is not explicitly stated in the Lean theorem provided."
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


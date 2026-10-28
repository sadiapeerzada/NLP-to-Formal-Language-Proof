# lib_q_sqrt_monotone: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For real x and y with x≤y, the principal square root of x is at most that of y, using the totalized real square root which is zero on negative inputs.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_sqrt_monotone (x y : ℝ) (h : x ≤ y) : Real.sqrt x ≤ Real.sqrt y
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Real x<=y; English explicitly says sqrt is zero on negative inputs, so absence of nonnegativity hypotheses is intentional."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_sqrt_monotone",
  "theorem": "AuditReference14.study_q_sqrt_monotone",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x y : ℝ) (h : x ≤ y), Real.sqrt x ≤ Real.sqrt y",
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
  "candidate_id": "lib_q_sqrt_monotone",
  "subject_sha256": "4a8a33d4e9743c9ec4df06cd28308d48f18605ba7e768ae8d719479cf6f2e8f4",
  "kind": "approximate_numeric_probe",
  "checked_assignments": 91,
  "filtered_by_assumptions": 78,
  "failures": [],
  "note": "Totalized sqrt negative input ->zero; floating approximation.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 20 column 1 (char 1319)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "uncertain",
  "quantifiers": "universal quantification on x and y, existential quantification on h",
  "domains": "real numbers, with zero on negative inputs",
  "assumptions": "x ≤ y, zero on negative inputs",
  "equivalence": "not explicitly stated",
  "strength": "the Lean theorem does not fully capture the English proposition' extraneous assumption about zero on negative inputs.",
  "boundary_cases": "not specified",
  "counterexample_search": "consider x = -1, y = 0; the principal square root is not defined for x, breaking the assumption.",
  "explanation": "The Lean theorem formalizes the comparison of square roots for non-negative real numbers but does not address the case where x is negative, as assumed in the English proposition.",
  "issues": [
    "Implicit assumption about the principal square root being defined for all real numbers, which is incorrect.",
    "Lack of handling for negative inputs.",
    "No explicit mention of zero on negative inputs in the Lean theorem.",
    "The English proposition contains an implicit restriction not present in the Lean theorem.",
    "No counterexample provided for the case where x is negative.",
    "The Lean theorem does not fully match the English proposition's scope, particularly regarding the treatment of negative inputs."
  ]
}
```

The label is "uncertain" because the Lean theorem does not fully encapsulate the English proposition's assumptions, especially concerning the treatment of negative inputs. The English proposition implies a comparison of square roots that is implicitly limited to non-negative real numbers, while the Lean theorem does not include this restriction.

The quantifiers in the English proposition are universal for x and y, with an existential quantification on the condition h (x ≤ y). The Lean theorem uses universal quantification on x and y, with an existential quantification on h, which is functionally equivalent but lacks the implicit restriction on the domains of x and y.

The domains in the English proposition suggest non-negative real numbers with a special case for zero, while the Lean theorem specifies the domain as real numbers with a totalized operation that is zero on negative inputs. This introduces a potential mismatch in treatment of negative numbers.

The assumptions in the English proposition include the condition that x is less than or equal to y and an implicit handling of zero on negative inputs, which is not present in the Lean theorem.

The strength of the Lean theorem in this context is limited because it does not fully match the English proposition's scope, particularly regarding the treatment of negative inputs.

Boundary cases are not specified in the Lean theorem, which is a limitation when considering the full implications of the proposition.

A concrete counterexample to the equivalence between the English proposition and the Lean theorem is x = -1, y = 0. In this case, the principal square root is not defined for x, which breaks the assumption in the English proposition and is not accounted for in the Lean theorem.

The explanation for the mismatch is that the Lean theorem formalizes the comparison of square roots for non-negative real numbers but does not address the case where x is negative, as assumed in the English proposition.

The issues highlighted include the implicit assumption about the principal square root being defined for all real numbers, which is incorrect, the lack of handling for negative inputs, the absence of an explicit mention of zero on negative inputs in the Lean theorem, the omission of this restriction in the Lean theorem, the mismatch in the proposition's scope, and the lack of a counterexample for the case where x is negative.

```json
{
  "label": "uncertain",
  "quantifiers": "universal quantification on x and y, existential quantification on h",
  "domains": "real numbers, with zero on negative inputs",
  "assumptions": "x ≤ y, zero on negative inputs",
  "equivalence": "not explicitly stated",
  "str
````


## Phi-4-mini actual judgment

```json
null
```

Schema error: Unclosed JSON fence

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same, stronger, weaker, or ambiguous with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of the real square root function which is consistent with the expected Lean theorem statement. The Lean theorem statement uses the totalized real square root function which returns zero for negative numbers, ensuring monotonicity as required by the English statement. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is a requirement for a specific import but none are required in this case. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less than or equal to the square root of another non-negative real number when x is less than or equal to y. There is an equivalence in terms of conclusion as both assert that the square root of a non-negative real number is less
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


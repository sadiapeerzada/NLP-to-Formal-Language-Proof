# lib_a_euclidean: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For any integers a and b, the remainder of a upon division by b plus b times the integer quotient equals a, including when b is zero.
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_euclidean (a b : ℤ) : a % b + b * (a / b) = a
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Both variables integers; remainder plus divisor times quotient equals dividend. English explicitly includes zero divisor and aligns with totalized Lean division."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_euclidean",
  "theorem": "AuditReference14.study_a_euclidean",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b : ℤ), a % b + b * (a / b) = a",
  "axioms": [
    "propext"
  ],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "lib_a_euclidean",
  "subject_sha256": "58b2b19c678c9b89f5747d7e97411b9db3aae521b6de5f16a29dc16d76a4d2bc",
  "kind": "exact_bounded_probe",
  "checked_assignments": 169,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Lean Euclidean remainder nonnegative for nonzero negative divisors; /0=0,%0=a.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 18 column 1 (char 1136)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "universal quantification over integers a and b",
  "domains": "ℤ, excluding division by zero",
  "assumptions": "division and multiplication operations, remainder operation",
  "equivalence": "the provided English statement does not account for the case when b is zero",
  "strength": "the English statement is a weaker form of the general theorem, as it lacks clarity on the treatment of b=0",
  "boundary_cases": "not defined for b=0, potentially leading to incorrect formalization",
  "counterexample_search": "b=0 case to demonstrate the English statement's incompletenency",
  "explanation": "the English statement fails to capture the full generality of the Euclidean division, particularly for b=0, which requires defining a as a multiple of b plus the remainder a",
  "issues": [
    "omission of treatment for b=0",
    "lack of clarity on the remainder operation when b is zero",
    "insufficient to match the generality of the Euclidean division theorem as stated in Mathlib",
    "potential misunderstanding of the theorem's application due to incomplete specification"
  ]
}
```



The provided JSON object indicates that the English proposition is "not faithful" to the Lean theorem it is supposed to formalize. The English statement does not address the case when the divisor b is zero, which is a critical aspect of the Euclidean division theorem. The theorem in mathematics requires a definition for the case when the divisor is zero, as division by zero is undefined. The English statement, as given, does not specify this and thus lacks completeness. The Lean theorem, on the other hand, would typically be formalized with additional cases or conditions to handle the scenario where b is zero, ensuring that the theorem is total and applicable in all situations, including the edge case.

The English statement also does not explicitly mention the use of the `BigOperators` or the `remainder` operation, which are necessary for a correct formalization in Lean. The `remainder` operation is essential for stating the theorem correctly, as it captures the essence of the Euclidean division, which is to express a as a multiple of b plus some remainder.

The "strength" is weak because the English statement does not encompass the full generality of the mathematical concept, and the "boundary_cases" section highlights the specific issue with the treatment of b=0. The "counterexample_search" suggests looking at the case where b=0 to find a counterexample to the English statement, demonstrating its incompleteness.

The "issues" list points out the key areas where the English statement falls short of a faithful formalization, emphasizing the need for clarity on the treatment of the zero divisor and the remainder operation. The "explanation" clarifies why the English statement is insufficient and what is required for a complete formalization.

In summary, the English proposition does not fully capture the mathematical theorem due to its omission of the treatment for the case when the divisor is zero, which is a necessary component of the Euclidean division theorem. The Lean theorem would be more general and complete, accounting for all possible values of a and b, including the edge case of b being zero.
````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each a and b",
  "domains": "integers",
  "assumptions": "none",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "when b is zero",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement implies a property of division and subtraction that is not universally true in Lean due to the truncation of division and handling of remainders differently than expected in typical arithmetic sense.",
  "issues": [
    "Division and subtraction operations in Lean may not directly correspond to their usual meanings in mathematics due to handling of remainders and division by zero.",
    "The expected Lean statement assumes division and subtraction operations that lead to a stronger conclusion than the one provided in the English statement."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "one each a and b",
  "domains": "integers",
  "assumptions": "none",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "when b is zero",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement implies a property of division and subtraction that is not universally true in Lean due to the truncation of division and handling of remainders differently than expected in typical arithmetic sense.",
  "issues": [
    "Division and subtraction operations in Lean may not directly correspond to their usual meanings in mathematics due to handling of remainders and division by zero.",
    "The expected Lean statement assumes division and subtraction operations that lead to a stronger conclusion than the one provided in the English statement."
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
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


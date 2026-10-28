# lib_q_cauchy: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For real numbers a,b,c,d, (a*c+b*d)^2 is at most (a^2+b^2)*(c^2+d^2).
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_cauchy (a b c d : ℝ) : (a * c + b * d) ^ 2 ≤ (a ^ 2 + b ^ 2) * (c ^ 2 + d ^ 2)
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Four universal reals; squared dot product and two squared norms are paired as in the English."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_cauchy",
  "theorem": "AuditReference14.study_q_cauchy",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b c d : ℝ), (a * c + b * d) ^ 2 ≤ (a ^ 2 + b ^ 2) * (c ^ 2 + d ^ 2)",
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
  "candidate_id": "lib_q_cauchy",
  "subject_sha256": "842015321110bf2a0ca934429b18aa6c2c0fb2cf5ac11f51f79fbaca78ced8c4",
  "kind": "exact_bounded_probe",
  "checked_assignments": 625,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Exact rational vectors, including zero.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 19 column 1 (char 1149)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "uncertain",
  "quantifiers": "universal quantification over ℝ for a, b, c, d",
  "domains": "ℝ for a, b, c, d",
  "assumptions": "no additional assumptions",
  "equivalence": "not explicitly stated",
  "strength": "the English proposition suggests a stronger claim than the Lean theorem",
  "boundary_cases": "not provided",
  "counterexample_search": "no specific counterexample given, but the claim may not hold universally",
  "explanation": "The English proposition implies that the equality holds, while the Lean theorem only provides an inequality. Without equality, the English proposition is stronger and not equivalent to the Lean theorem.",
  "issues": [
    "The Lean theorem provides an inequality, not an equality.",
    "The English proposition suggests a stronger claim than the Lean theorem.",
    "No counterexample is provided to show the difference between the claims.",
    "The English proposition lacks a quantifier for the strictness of the inequality.",
    "The English proposition does not specify the domain of the variables, which could imply additional restrictions not present in the Lean theorem."
  ]
}
```

The English proposition suggests a stronger claim (equality) than the Lean theorem, which provides an inequality. Without equality, the English proposition cannot be said to be equivalent to the Lean theorem. The Lean theorem's domain is specified as ℝ, but the English proposition does not clarify if it restricts the domain to positive real numbers, non-negative real numbers, or all real numbers, which could imply additional restrictions. The lack of a counterexample or boundary case analysis leaves the equivalence uncertain.

```json
{
  "label": "not faithful",
  "quantifiers": "universal quantification over ℝ for a, b, c, d",
  "domains": "ℝ for a, b, c, d",
  "assumptions": "no additional assumptions",
  "equivalence": "the English proposition suggests a stronger claim (equality) than the Lean theorem",
  "strength": "the English proposition is stronger but not equivalent to the Lean theorem",
  "boundary_cases": "not provided, which may affect the claim's validity",
  "counterexample_search": "the claim may not hold universally, as demonstrated by the Lean theorem's inequality",
  "explanation": "The English proposition implies equality, while the Lean theorem provides an inequality, indicating the English proposition is stronger but not equivalent to the formalized theorem.",
  "issues": [
    "The Lean theorem only provides an inequality.",
    "The English proposition lacks a quantifier for the strictness of the inequality.",
    "No counterexample is provided to show the difference between the claims.",
    "The English proposition lacks domain specification, potentially implying additional restrictions.",
    "The equivalence between the English proposition and the Lean theorem is not established.",
    "No boundary case analysis is provided to support the claim in the English proposition."
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
  "explanation": "The English statement and Lean theorem are equivalent in terms of mathematical meaning. Both assert that the square of the sum of the products of pairs of real numbers is less than or equal to the product of the sums of their squares. This is a statement of the Cauchy-Schwarz inequality in the context of real numbers. There is no counterexample that refutes this inequality, and it is a well-known result in mathematics. The inequality is strict unless a and c, or b and d, are both zero. The inequality is maintained under the usual operations on real numbers and respects the domains and scopes of the variables involved.",
  "issues": [
    "The English statement uses a less formal notation than Lean's formal type theory notation.",
    "The inequality is not explicitly stated as a theorem in Mathlib, but it is equivalent to a theorem that is part of the library."
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
  "explanation": "The English statement and Lean theorem are equivalent in terms of mathematical meaning. Both assert that the square of the sum of the products of pairs of real numbers is less than or equal to the product of the sums of their squares. This is a statement of the Cauchy-Schwarz inequality in the context of real numbers. There is no counterexample that refutes this inequality, and it is a well-known result in mathematics. The inequality is strict unless a and c, or b and d, are both zero. The inequality is maintained under the usual operations on real numbers and respects the domains and scopes of the variables involved.",
  "issues": [
    "The English statement uses a less formal notation than Lean's formal type theory notation.",
    "The inequality is not explicitly stated as a theorem in Mathlib, but it is equivalent to a theorem that is part of the library."
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


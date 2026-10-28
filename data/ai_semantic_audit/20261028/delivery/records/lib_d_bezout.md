# lib_d_bezout: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For integers a and b, their nonnegative greatest common divisor is an integer linear combination of a and b.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_bezout (a b : ℤ) : ∃ x y : ℤ, (Int.gcd a b : ℤ) = a * x + b * y
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Integer a,b and existential integer coefficients; Int.gcd is nonnegative natural and explicitly coerced to integer in the linear combination."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_bezout",
  "theorem": "AuditReference14.study_d_bezout",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b : ℤ), ∃ x y : ℤ, (Int.gcd a b : ℤ) = a * x + b * y",
  "axioms": [
    "propext",
    "Quot.sound"
  ],
  "strict_verified": true
}
```


## Bounded mathematical probe

```json
{
  "candidate_id": "lib_d_bezout",
  "subject_sha256": "96818dfa45be77cb1166b68bd4212cd5998383c55332994ca990b6d615a64b94",
  "kind": "exact_bounded_probe",
  "checked_assignments": 169,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Witness search bounded -12..12; absent witness would be inconclusive, not a mathematical counterexample.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 21 column 1 (char 1622)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "uncertain",
  "quantifiers": "∃ a b : ℤ, ∃ x y : ℤ",
  "domains": "a, b ∈ ℤ",
  "assumptions": "none",
  "equivalence": "uncertain due to potential ambiguity in the statement",
  "strength": "the Lean theorem may generalize the English proposition, but lacks explicit detail on the nonnegative aspect and the exact form of the greatest common divisor",
  "boundary_cases": "not explicitly addressed",
  "counterexample_search": "no concrete counterexample provided, as the English proposition is generally accepted",
  "explanency": "the English proposition aligns with the Bézout's lemma, but the Lean theorem lacks explicit detail on the nonnegative constraint and the exact representation of the greatest common divisor",
  "issues": [
    "The Lean theorem does not explicitly state that the greatest common divisor is nonnegative.",
    "The Lean theorem assumes the existence of a representation without detailing the method to ensure it is nonnegative.",
    "The Lean theorem does not address the case where one or both of the integers a and b are zero, which is a boundary case.",
    "The Lean theorem does not mention the zero and negative cases, which are important for a complete formalization.",
    "The Lean theorem'ized representation lacks clarity on the handling of integer division and truncation, which could lead to different interpretations.",
    "The Lean theorem does not explicitly state the domain of the integers, which could lead to ambiguity.",
    "The Lean theorem's formalization may not fully capture the English proposition's implicit restrictions and assumptions."
  ]
}
```

The English proposition is generally faithful to the Lean theorem, as it is a formalization of Bézout's lemma, which states that the greatest common divisor (gcd) of two integers can be expressed as a linear combination of those integers. However, the Lean theorem provided lacks explicit detail on several critical aspects of the English proposition, leading to uncertainty about its completeness and faithfulness.

The quantifiers in both the English proposition and the Lean theorem are similar, with existential quantifiers for the integers `a` and `b` and the integers `x` and `y`. The domains are correctly identified as integers for `a`, `b`, and `x`, `y`, but the Lean theorem does not explicitly state that `a` and `b` are nonnegative, which is an important aspect of the English proposition.

The assumptions section is empty, but the English proposition implicitly assumes that the gcd is nonnegative, which is not stated in the Lean theorem. The Lean theorem also does not address the boundary case where one or both of `a` and `b` are zero, which could affect the gcd and its representation.

The equivalence between the English proposition and the Lean theorem is uncertain due to potential ambiguity in the statement and the lack of explicit detail on the nonnegative constraint and the exact representation of the gcd.

The strength of the Lean theorem in capturing the English proposition is questionable because it may generalize the proposition without fully capturing all its essential details, such as the nonnegativity of the gcd and the handling of zero and negative cases.

Boundary cases and zero and negative cases are not explicitly addressed in the Lean theorem, which are important for a complete formalization. The Lean theorem's formalization may not fully capture the English proposition's implicit restrictions and assumptions, leading to potential ambiguity.

A concrete counterexample to equivalence is not provided, as the English proposition is generally accepted, but the Lean theorem lacks explicit detail. The Lean theorem may require additional formalization to fully align with the English proposition.

In summary, the alignment between the English proposition and the Lean theorem is uncertain due to potential ambiguity and lack of explicit detail on critical aspects of the proposition. The Lean theorem may need to be adjusted to include the nonnegative constraint, handle boundary cases, and
````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "∀ a, b : ℤ; ∃ x, y : ℤ",
  "domains": "ℤ",
  "assumptions": "a and b are integers",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero check",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement asserts that the nonnegative greatest common divisor (gcd) of any two integers a and b is an integer combination of a and b. This is equivalent to stating that an integer x and y exist such that the gcd equals a multiplied by x plus b multiplied by y. This is a stronger statement in Lean because it implies uniqueness (up to sign), while the expected statement does not explicitly assert uniqueness but implies it through the existence quantifier and the definition of gcd as a combination of a and b.",
  "issues": [
    "The English statement does not explicitly assert uniqueness (up to sign), while the Lean statement implies uniqueness through the existence quantifier and the definition of gcd as a combination of a and b."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "∀ a, b : ℤ; ∃ x, y : ℤ",
  "domains": "ℤ",
  "assumptions": "a and b are integers",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero check",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement asserts that the nonnegative greatest common divisor (gcd) of any two integers a and b is an integer combination of a and b. This is equivalent to stating that an integer x and y exist such that the gcd equals a multiplied by x plus b multiplied by y. This is a stronger statement in Lean because it implies uniqueness (up to sign), while the expected statement does not explicitly assert uniqueness but implies it through the existence quantifier and the definition of gcd as a combination of a and b.",
  "issues": [
    "The English statement does not explicitly assert uniqueness (up to sign), while the Lean statement implies uniqueness through the existence quantifier and the definition of gcd as a combination of a and b."
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
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


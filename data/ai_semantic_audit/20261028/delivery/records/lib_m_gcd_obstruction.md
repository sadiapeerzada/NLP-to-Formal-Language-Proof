# lib_m_gcd_obstruction: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For integers a,b,m, if the greatest common divisor of a and m does not divide b, no integer x solves a*x congruent to b modulo m.
```

## Lean type

```lean
open scoped BigOperators
theorem study_m_gcd_obstruction (a b m : ℤ) (h : ¬ (Int.gcd a m : ℤ) ∣ b) : ¬ ∃ x : ℤ, Int.ModEq m (a * x) b
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Integer a,b,m; nondivisibility by coerced nonnegative gcd implies negated existential integer solution. Negation scope and witness domain match."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_m_gcd_obstruction",
  "theorem": "AuditReference14.study_m_gcd_obstruction",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b m : ℤ) (h : ¬ (Int.gcd a m : ℤ) ∣ b), ¬ ∃ x : ℤ, Int.ModEq m (a * x) b",
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
  "candidate_id": "lib_m_gcd_obstruction",
  "subject_sha256": "8548bf3721481a5cb8c77a220f89790d5bcd807f4937cc0ce20422f20ec6f74d",
  "kind": "exact_bounded_probe",
  "checked_assignments": 572,
  "filtered_by_assumptions": 1625,
  "failures": [],
  "note": "Bounded x counterexample search, not proof of universal nonexistence.",
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
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement outlines a condition where an integer solution does not exist due to a constraint on divisibility by the greatest common divisor (gcd) of a and m. This is directly translated into a Lean theorem stating that no such integer x exists that satisfies the congruence a*x ≡ b (mod m) given the gcd(a,m) does not divide b. This is a stronger statement than requested as it directly asserts non-existence rather than existence, and it respects the convention that an omitted English domain restriction (e.g., a and m being integers) makes a true Lean theorem stronger than requested.",
  "issues": [
    "The English statement assumes a and m are integers and a is not divisible by m, which directly translates into the Lean theorem's assumptions and conclusion.",
    "The Lean theorem is equivalent to the English statement but is stronger due to the explicit mention of the gcd condition not dividing b.",
    "No counterexample is provided in the English statement, but one could construct a counterexample where a and m are coprime and b is a multiple of m, which would not satisfy the condition.",
    "The English statement and Lean theorem are equivalent in terms of their mathematical meaning."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement outlines a condition where an integer solution does not exist due to a constraint on divisibility by the greatest common divisor (gcd) of a and m. This is directly translated into a Lean theorem stating that no such integer x exists that satisfies the congruence a*x ≡ b (mod m) given the gcd(a,m) does not divide b. This is a stronger statement than requested as it directly asserts non-existence rather than existence, and it respects the convention that an omitted English domain restriction (e.g., a and m being integers) makes a true Lean theorem stronger than requested.",
  "issues": [
    "The English statement assumes a and m are integers and a is not divisible by m, which directly translates into the Lean theorem's assumptions and conclusion.",
    "The Lean theorem is equivalent to the English statement but is stronger due to the explicit mention of the gcd condition not dividing b.",
    "No counterexample is provided in the English statement, but one could construct a counterexample where a and m are coprime and b is a multiple of m, which would not satisfy the condition.",
    "The English statement and Lean theorem are equivalent in terms of their mathematical meaning."
  ]
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Exploratory model did not complete a review; no verdict exists.",
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


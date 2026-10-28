# lib_m_power: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For integers a,b,m and a natural exponent n, congruence of a and b modulo m implies congruence of their nth powers modulo m.
```

## Lean type

```lean
open scoped BigOperators
theorem study_m_power (a b m : ℤ) (n : ℕ) (h : Int.ModEq m a b) : Int.ModEq m (a ^ n) (b ^ n)
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "All bases and modulus integer, exponent natural; congruence premise precedes nth-power congruence and includes modulus zero."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_m_power",
  "theorem": "AuditReference14.study_m_power",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b m : ℤ) (n : ℕ) (h : Int.ModEq m a b), Int.ModEq m (a ^ n) (b ^ n)",
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
  "candidate_id": "lib_m_power",
  "subject_sha256": "39a9cf9beab1e365a63eba519b66d2ca159282b43dddc6fd04cd972e666afb12",
  "kind": "exact_bounded_probe",
  "checked_assignments": 4245,
  "filtered_by_assumptions": 6740,
  "failures": [],
  "note": "All integer moduli including zero; natural exponent.",
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
  "strength": "same, stronger, weaker, or ambiguous with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of integer powers under modular equivalence, which is equivalent to a statement in Lean's library on power operations modulo a given number. The Lean statement is an instance of a general theorem on power operations modulo a number. There is an equivalence between the English statement and the Lean statement in terms of mathematical meaning, but the strength of the conclusion may depend on the specific cases considered (e.g., boundary cases such as n=0 or n being a negative integer). There is no explicit counterexample provided in the English statement that would lead to an inequality in Lean.",
  "issues": [
    "The English statement assumes a specific scope of the power operator and a specific domain of integers. It assumes that a and b are integers and n is a natural exponent. It assumes that a and b are congruent modulo m and concludes that a^n and b^n are congruent modulo m.",
    "The Lean statement directly references a theorem in the Mathlib library on power operations modulo a number. It does not introduce any additional assumptions beyond those required by the English statement.",
    "The English statement does not specify the behavior of the power operator when n is negative, while Lean's statement implicitly assumes n is a natural number (non-negative integers). This difference does not lead to inequality as negative exponents are equivalent to taking roots (which is not directly covered in the statement but is consistent with the definition of power operations).",
    "The English statement does not explicitly mention the case when m is 0, which would lead to division by zero in Lean. However, this case is not meaningful in the context of modular arithmetic as modulo 0 is undefined.",
    "The English statement assumes that a and b are elements of a commutative ring (integers), while Lean's statement does not explicitly mention this, but it is implied by the use of the Int.ModEq type constructor."
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
  "strength": "same, stronger, weaker, or ambiguous with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a property of integer powers under modular equivalence, which is equivalent to a statement in Lean's library on power operations modulo a given number. The Lean statement is an instance of a general theorem on power operations modulo a number. There is an equivalence between the English statement and the Lean statement in terms of mathematical meaning, but the strength of the conclusion may depend on the specific cases considered (e.g., boundary cases such as n=0 or n being a negative integer). There is no explicit counterexample provided in the English statement that would lead to an inequality in Lean.",
  "issues": [
    "The English statement assumes a specific scope of the power operator and a specific domain of integers. It assumes that a and b are integers and n is a natural exponent. It assumes that a and b are congruent modulo m and concludes that a^n and b^n are congruent modulo m.",
    "The Lean statement directly references a theorem in the Mathlib library on power operations modulo a number. It does not introduce any additional assumptions beyond those required by the English statement.",
    "The English statement does not specify the behavior of the power operator when n is negative, while Lean's statement implicitly assumes n is a natural number (non-negative integers). This difference does not lead to inequality as negative exponents are equivalent to taking roots (which is not directly covered in the statement but is consistent with the definition of power operations).",
    "The English statement does not explicitly mention the case when m is 0, which would lead to division by zero in Lean. However, this case is not meaningful in the context of modular arithmetic as modulo 0 is undefined.",
    "The English statement assumes that a and b are elements of a commutative ring (integers), while Lean's statement does not explicitly mention this, but it is implied by the use of the Int.ModEq type constructor."
  ]
}
```
````


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Exploratory model did not complete a review; no verdict exists.",
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into strength. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


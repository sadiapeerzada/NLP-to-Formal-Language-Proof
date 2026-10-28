# lib_q_amgm: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For real numbers x and y, twice their product is at most the sum of their squares.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_amgm (x y : ℝ) : 2 * x * y ≤ x ^ 2 + y ^ 2
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Real x,y without nonnegativity assumptions; exactly 2*x*y <= x^2+y^2, so the AM-GM-like name adds no missing hypothesis."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_amgm",
  "theorem": "AuditReference14.study_q_amgm",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (x y : ℝ), 2 * x * y ≤ x ^ 2 + y ^ 2",
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
  "candidate_id": "lib_q_amgm",
  "subject_sha256": "5aa87f56a177bb6993225b741d08e32bbc3b073cbd5a2a2c119d29043ff3486e",
  "kind": "exact_bounded_probe",
  "checked_assignments": 169,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "No nonnegativity assumption required.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Missing substantive field: quantifiers

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "not faithful",
  "quantifiers": {
    "SUBJECT_JSON": "For real numbers x and y",
    "expected_lean_statement": "2 * x * y ≤ x ^ 2 + y ^ 2"
  },
  "domains": {
    "SUBJECT_JSON": "ℝ",
    "expected_lean_statement": "ℝ",
    "issues": "Nat truncated subtraction and division are not explicitly addressed in the Lean theorem."
  },
  "assumptions": {
    "SUBJECT_JSON": null,
    "expected_lean_statement": "open scoped BigOperators",
    "issues": "Implicit assumptions about the domains of operation are not stated, potentially limiting the theorem'ized expression."
  },
  "equivalence": "uncertain",
  "boundary_cases": "not addressed",
  "counterexample_search": "not provided",
  "explanation": "The Lean theorem formalization lacks explicit handling of edge cases and domain restrictions, particularly for operations like division and subtraction.",
  "issues": [
    "Implicit domain assumptions in Lean theorem",
    "Lack of explicit handling of boundary cases",
    "No provided counterexample to test equivalence",
    "Incomplete formalization of assumptions",
    "Potential issues with Nat truncated subtraction and division"
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
  "strength": "same, stronger, weaker, or ambiguous with reason",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a specific inequality involving real numbers x and y. The Lean theorem expresses this inequality formally within the Mathlib library conventions. There is an equivalence between the English statement and the Lean statement provided it respects the scope of quantifiers, variable domains, assumptions, and conclusion as specified in Mathlib. Without an explicit counterexample provided, one assumes the statement is true unless a counterexample is presented. There is an inherent strength in the Lean statement equivalent to or stronger than requested due to the totalization of division and remainders in Lean Nat subtraction.",
  "issues": [
    "The English statement assumes a specific inequality without mentioning boundary cases such as x and y being zero or one.",
    "The Lean statement does not explicitly check endpoint cases such as division by zero."
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
  "explanation": "The English statement asserts a specific inequality involving real numbers x and y. The Lean theorem expresses this inequality formally within the Mathlib library conventions. There is an equivalence between the English statement and the Lean statement provided it respects the scope of quantifiers, variable domains, assumptions, and conclusion as specified in Mathlib. Without an explicit counterexample provided, one assumes the statement is true unless a counterexample is presented. There is an inherent strength in the Lean statement equivalent to or stronger than requested due to the totalization of division and remainders in Lean Nat subtraction.",
  "issues": [
    "The English statement assumes a specific inequality without mentioning boundary cases such as x and y being zero or one.",
    "The Lean statement does not explicitly check endpoint cases such as division by zero."
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
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into strength. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


# ineq_002: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For any natural numbers a and b, a times b plus 1 is at most (a+1) times (b+1).
```

## Lean type

```lean
theorem prod_succ_ge (a b : ℕ) : a * b + 1 ≤ (a + 1) * (b + 1)
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural a,b universally quantified; +1 on the left and both successor factors on the right match."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "ineq_002",
  "theorem": "AuditReference0.prod_succ_ge",
  "source": "data/reference_verification/v0.1.0/references.lean",
  "expected_type": "∀ (a b : ℕ), a * b + 1 ≤ (a + 1) * (b + 1)",
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
  "candidate_id": "ineq_002",
  "subject_sha256": "001142eb421b8d3a06f725207733f8917ae1bf17b833e21ba90db7684b42d082",
  "kind": "exact_bounded_probe",
  "checked_assignments": 81,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Both zero endpoints.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
{
  "label": "not faithful",
  "quantifiers": "universal quantification over ℕ for a and b",
  "domains": "ℕ for a and b",
  "assumptions": "none specified",
  "equivalence": "the English proposition is not equivalent to the Lean theorem",
  "strength": "the English proposition is a weaker statement than the Lean theorem",
  "boundary_cases": "consider the case when a = 0 and b = 0",
  "counterexample_search": "a = 0, b = 0",
  "explanation": "In the English proposition, the term 'at most' is ambiguous and could imply a strict inequality. The Lean theorem, however, uses '≤', which includes equality. When a = 0 and b = 0, the left side of the inequality becomes 1, and the right side becomes 1 as well, making the inequality true. The English proposition does not account for this equality case, thus it is weaker.",
  "issues": [
    "vague language in the English proposition",
    "the English proposition does not specify the strictness of the inequality",
    "the English proposition lacks clarity on handling the boundary case where both a and b are zero",
    "the English proposition does not match the formalism of the Lean theorem",
    "the English proposition is a weaker statement than the Lean theorem"
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "not faithful",
  "quantifiers": "universal quantification over ℕ for a and b",
  "domains": "ℕ for a and b",
  "assumptions": "none specified",
  "equivalence": "the English proposition is not equivalent to the Lean theorem",
  "strength": "the English proposition is a weaker statement than the Lean theorem",
  "boundary_cases": "consider the case when a = 0 and b = 0",
  "counterexample_search": "a = 0, b = 0",
  "explanation": "In the English proposition, the term 'at most' is ambiguous and could imply a strict inequality. The Lean theorem, however, uses '≤', which includes equality. When a = 0 and b = 0, the left side of the inequality becomes 1, and the right side becomes 1 as well, making the inequality true. The English proposition does not account for this equality case, thus it is weaker.",
  "issues": [
    "vague language in the English proposition",
    "the English proposition does not specify the strictness of the inequality",
    "the English proposition lacks clarity on handling the boundary case where both a and b are zero",
    "the English proposition does not match the formalism of the Lean theorem",
    "the English proposition is a weaker statement than the Lean theorem"
  ]
}

```


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each of a and b",
  "domains": "ℕ",
  "assumptions": "none",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific endpoint check a=0 and a=ℕ. b=0 and b=ℕ",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts an inequality that is not true in general and therefore not equivalent to the expected Lean theorem which is always true.",
  "issues": [
    "The inequality a * b + 1 ≤ (a + 1) * (b + 1) does not hold for all natural numbers a and b.",
    "The counterexample a=1, b=1 leads to a * b + 1 = 2 which is not less than or equal to (a + 1) * (b + 1) = 4."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "one each of a and b",
  "domains": "ℕ",
  "assumptions": "none",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific endpoint check a=0 and a=ℕ. b=0 and b=ℕ",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts an inequality that is not true in general and therefore not equivalent to the expected Lean theorem which is always true.",
  "issues": [
    "The inequality a * b + 1 ≤ (a + 1) * (b + 1) does not hold for all natural numbers a and b.",
    "The counterexample a=1, b=1 leads to a * b + 1 = 2 which is not less than or equal to (a + 1) * (b + 1) = 4."
  ]
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-4 response quality: Prompt placeholder copied into equivalence. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


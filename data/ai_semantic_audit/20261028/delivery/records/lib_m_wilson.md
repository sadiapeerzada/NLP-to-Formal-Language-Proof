# lib_m_wilson: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For a natural prime p, the factorial of p-1 equals minus one in the ring of integers modulo p.
```

## Lean type

```lean
open scoped BigOperators
theorem study_m_wilson (p : ℕ) [Fact p.Prime] : ((p - 1).factorial : ZMod p) = -1
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural prime p provided by Fact typeclass; factorial p-1 coerced into ZMod p equals additive inverse one, matching ring wording."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_m_wilson",
  "theorem": "AuditReference14.study_m_wilson",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (p : ℕ) [Fact p.Prime], ((p - 1).factorial : ZMod p) = -1",
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
  "candidate_id": "lib_m_wilson",
  "subject_sha256": "5ce54c56287a347cc7df0cd7742ad564aeae19141d71a1caddeb78f101e7d3fd",
  "kind": "exact_bounded_probe",
  "checked_assignments": 6,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "ZMod equality interpreted as integer congruence.",
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
  "quantifiers": "one each",
  "domains": "Z, ℕ",
  "assumptions": "p.Prime, (ZMod p).one",
  "equivalence": "conclusion exact",
  "strength": "same",
  "boundary_cases": "p prime",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a specific case of Wilson's theorem in modular arithmetic, while the Lean statement expresses a general theorem in Mathlib. Both are equivalent in strength but different in scope and presentation.",
  "issues": [
    "The English statement implicitly assumes p > 1, while Mathlib explicitly states p > 0 in p.Prime.",
    "The English statement uses a negation directly in the expression (p - 1).factorial = -1, while Mathlib uses the zero element (ZMod p).one) in modular subtraction (ZMod p) (p - 1).factorial + (ZMod p).one).",
    "The English statement does not explicitly mention the multiplicative group (Z/pZ)*, while Mathlib does.",
    "The English statement uses a less conventional notation (ZMod p) instead of (Z/(p))Z."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "one each",
  "domains": "Z, ℕ",
  "assumptions": "p.Prime, (ZMod p).one",
  "equivalence": "conclusion exact",
  "strength": "same",
  "boundary_cases": "p prime",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement asserts a specific case of Wilson's theorem in modular arithmetic, while the Lean statement expresses a general theorem in Mathlib. Both are equivalent in strength but different in scope and presentation.",
  "issues": [
    "The English statement implicitly assumes p > 1, while Mathlib explicitly states p > 0 in p.Prime.",
    "The English statement uses a negation directly in the expression (p - 1).factorial = -1, while Mathlib uses the zero element (ZMod p).one) in modular subtraction (ZMod p) (p - 1).factorial + (ZMod p).one).",
    "The English statement does not explicitly mention the multiplicative group (Z/pZ)*, while Mathlib does.",
    "The English statement uses a less conventional notation (ZMod p) instead of (Z/(p))Z."
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
    "Phi-4 response quality: Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


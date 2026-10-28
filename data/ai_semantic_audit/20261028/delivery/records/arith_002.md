# arith_002: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For any natural numbers a and b, a squared minus b squared equals (a + b) times (a - b), assuming a is at least b.
```

## Lean type

```lean
theorem sq_sub_sq_nat (a b : ℕ) (h : b ≤ a) : a ^ 2 - b ^ 2 = (a + b) * (a - b)
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Universal natural a,b with b<=a in both texts; truncated subtraction agrees with ordinary nonnegative difference under this premise."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "arith_002",
  "theorem": "AuditReference0.sq_sub_sq_nat",
  "source": "data/reference_verification/v0.1.0/references.lean",
  "expected_type": "∀ (a b : ℕ) (h : b ≤ a), a ^ 2 - b ^ 2 = (a + b) * (a - b)",
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
  "candidate_id": "arith_002",
  "subject_sha256": "501a999c3cc55a27df39dad131b5a9b5eb9995255bc58c4eb4f673ed2b28c22d",
  "kind": "exact_bounded_probe",
  "checked_assignments": 45,
  "filtered_by_assumptions": 36,
  "failures": [],
  "note": "Natural subtraction; b<=a only.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 22 column 1 (char 1397)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "universal quantifiers for a and b, existential quantifier for h",
  "domains": "natural numbers, with b ≤ a restriction",
  "assumptions": "h: b ≤ a",
  "equivalence": "the provided English statement is not equivalent to the formalized Lean theorem",
  "strength": "the Lean theorem is stronger due to additional assumptions",
  "boundary_cases": "zero and negative cases not addressed",
  "counterexample_search": "no concrete counterexample, but the English statement lacks the necessary assumption",
  "explanised": "the English statement omits the assumption that a ≥ b, which is essential for the Lean theorem's validity",
  "issues": [
    "The English proposition incorrectly generalizes the algebraic identity.",
    "The assumption b ≤ a is necessary for the Lean theorem but is omitted in the English statement.",
    "Without the assumption, the English statement can be false (e.g., if a = 2 and b = -1).",
    "The English statement does not account for the case when a < b, which would make the identity invalid.",
    "The Lean theorem's additional assumption is a strength, not a weakness, as it precisely defines the identity's applicability.",
    "The English proposition lacks the necessary restriction to match the formalized theorem.",
    "The English statement does not reflect the conditional nature of the identity."
  ]
}

```json
{
  "label": "not faithful",
  "quantifiers": "forall a, b in ℕ, (h : b ≤ a)",
  "domains": "ℕ with b ≤ a restriction",
  "assumptions": "b ≤ a",
  "equivalence": "The English proposition is not equivalent to the formalized Lean theorem.",
  "strength": "The Lean theorem is stronger due to the additional assumption b ≤ a.",
  "boundary_cases": "The English proposition does not address the case when a < b.",
  "counterexample_search": "The English proposition is false when a < b, as it lacks the necessary assumption.",
  "explanation": "The English proposition omits the assumption b ≤ a, which is essential for the identity a^2 - b^2 = (a + b)(a - b).",
  "issues": [
    "Incorrect generalization of the algebraic identity.",
    "Omission of the assumption b ≤ a.",
    "Lacks addressing the case when a < b.",
    "Does not reflect the conditional nature of the identity.",
    "Does not specify the necessary restriction for the identity.",
    "Lacks clarity on the applicability of the identity."
  ]
}
}
}
```
````


## Phi-4-mini actual judgment

```json
null
```

Schema error: Unterminated string starting at: line 4 column 14 (char 95)

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "Universal (∀) versus Existential (∃)",
  "domains": "Natural numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real numbers (ℕ) versus Real
```


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


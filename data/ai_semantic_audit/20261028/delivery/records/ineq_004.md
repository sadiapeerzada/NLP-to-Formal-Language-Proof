# ineq_004: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
Prove that n + 3 < n + 7 for all values of n ∈ ℕ. You can do this proof with algebra (without induction), but the goal of this exercise is to write out a valid induction proof.
```

## Lean type

```lean
theorem add_three_lt_add_seven (n : ℕ) : n + 3 < n + 7
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural n and strict n+3<n+7 match. Proposition-level faithfulness does not certify a requested induction proof method."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "ineq_004",
  "theorem": "AuditReference6.add_three_lt_add_seven",
  "source": "data/curation_batches/v0.1.2/ineq_004_linear_inequality.lean",
  "expected_type": "∀ (n : ℕ), n + 3 < n + 7",
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
  "candidate_id": "ineq_004",
  "subject_sha256": "ed94f52c16bf0971faf6c1f1ba8fd1f4c44be47603f602683ca2006dbbc0eb51",
  "kind": "exact_bounded_probe",
  "checked_assignments": 9,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Proposition only; proof-method request is not checked.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Missing substantive field: explanation

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "not faithful",
  "quantifiers": "universal for n in ℕ",
  "domains": "ℕ, algebraic operations",
  "assumptions": "n is an element of ℕ",
  "equivalence": "algebraic manipulation is not equivalent to induction",
  "strength": "algebraic manipulation does not prove the statement for all n in ℕ",
  "boundary_cases": "considering n = 0 and n = ∞",
  "counterexample_search": "n = 0 yields 3 < 7, which is true, but n = ∞ is not defined in ℕ",
  "explanised": "algebraic manipulation can confirm the inequality for specific values but does not constitute a proof for all natural numbers",
  "issues": [
    "The provided English proposition suggests a proof by algebra, which is insufficient for establishing the statement for all n in ℕ.",
    "Induction is typically used to prove statements about all elements of a set like ℕ, and without it, the proof is incomplete.",
    "The statement n + 3 < n + 7 is trivially true for all n in ℕ, but the exercise implies a need for a more complex proof method.",
    "No algebraic manipulation is provided, hence no equivalence to the expected Lean theorem is established.",
    "The exercise's requirement for an induction proof is ignored, leading to a non-fulfilling formalization."
  ]
}

```


## Phi-4-mini actual judgment

```json
{
  "label": "not faithful",
  "quantifiers": "universal (∀) versus inductive (induction)",
  "domains": "specific (ℕ) versus implied (nat numbers)",
  "assumptions": "none specified versus inductive step (n + 1) versus base case (n = 0)",
  "equivalence": "conclusion not equivalent versus final conclusion (true) versus final conclusion (true)",
  "strength": "ambiguous versus final conclusion (true versus true)",
  "boundary_cases": "specific (n = 0) versus final conclusion (true versus true)",
  "counterexample_search": "specific candidate (n = 0) versus final conclusion (true versus true)",
  "explanation": "The English statement requests an induction proof of an inequality that is true by simple algebraic manipulation, while the Lean theorem asks for an inductive proof without specifying the inductive step or base case.",
  "issues": [
    "Confusion between universal and inductive quantifiers",
    "Different expectations on how induction should be applied",
    "The final conclusion in Lean is true, but the requested proof method is different from induction."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "not faithful",
  "quantifiers": "universal (∀) versus inductive (induction)",
  "domains": "specific (ℕ) versus implied (nat numbers)",
  "assumptions": "none specified versus inductive step (n + 1) versus base case (n = 0)",
  "equivalence": "conclusion not equivalent versus final conclusion (true) versus final conclusion (true)",
  "strength": "ambiguous versus final conclusion (true versus true)",
  "boundary_cases": "specific (n = 0) versus final conclusion (true versus true)",
  "counterexample_search": "specific candidate (n = 0) versus final conclusion (true versus true)",
  "explanation": "The English statement requests an induction proof of an inequality that is true by simple algebraic manipulation, while the Lean theorem asks for an inductive proof without specifying the inductive step or base case.",
  "issues": [
    "Confusion between universal and inductive quantifiers",
    "Different expectations on how induction should be applied",
    "The final conclusion in Lean is true, but the requested proof method is different from induction."
  ]
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted.",
    "At least one model raises a semantic concern; raw explanation requires adjudication."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


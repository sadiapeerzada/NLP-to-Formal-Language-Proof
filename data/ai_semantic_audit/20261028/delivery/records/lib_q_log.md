# lib_q_log: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural base b and positive natural n, b raised to the natural logarithm floor log base b of n is at most n, using Mathlib's totalized natural logarithm.
```

## Lean type

```lean
open scoped BigOperators
theorem study_q_log (b n : ℕ) (hn : n ≠ 0) : b ^ Nat.log b n ≤ n
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural base b, nonzero natural n; English explicitly adopts totalized Nat.log, including bases zero and one."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_q_log",
  "theorem": "AuditReference14.study_q_log",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (b n : ℕ) (hn : n ≠ 0), b ^ Nat.log b n ≤ n",
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
  "candidate_id": "lib_q_log",
  "subject_sha256": "31797af04e63d53b2eab6613df08b8279b8dee3051cc854fdbc0c9cad55628a7",
  "kind": "exact_bounded_probe",
  "checked_assignments": 144,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Totalized Nat.log bases zero/one yield zero, including 0^0.",
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
  "label": "uncertain",
  "quantifiers": "universal quantifier on b and n, existential quantifier on hn",
  "domains": "natural numbers, positive natural numbers, BigOperators, and logarithm functions",
  "assumptions": "b is a natural base, n is a positive natural number, and logarithm functions are totalized",
  "equivalence": "the English proposition is not clearly equivalent to the Lean theorem",
  "strength": "the English proposition suggests a stronger claim than the Lean theorem",
  "boundary_cases": "the English proposition does not address the case when n is 1",
  "counterexample_search": "the English proposition implies n must be greater than 1, which is not required by the Lean theorem",
  "explanised": "the English proposition is ambiguous and suggests a stronger claim than the Lean theorem, which only addresses the case where n is not equal to 1",
  "issues": [
    "the English proposition omits the case when n is 1, potentially leading to a stronger claim",
    "the English proposition implies a restriction on the base b that is not present in the Lean theorem",
    "the Lean theorem does not contain a comparison with n, only a statement about the logarithm function",
    "the English proposition lacks a clear formalization of the logarithm function and its properties",
    "the Lean theorem's scope is limited to the case where n is not zero, while the English proposition seems to generalize to all natural numbers"
  ]
}

```


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each",
  "domains": "ℕ and Nat",
  "assumptions": "n ≠ 0",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement implies a less restrictive inequality than the one required by Mathlib conventions. The English statement does not explicitly exclude the case where n is 0, which would make the inequality true but not required by Mathlib conventions.",
  "issues": [
    "The English statement assumes the inequality is strict (b ^ Nat.log b n < n) rather than non-strict (b ^ Nat.log b n ≤ n) as required by Mathlib.",
    "The English statement does not account for the totalization of division and remainders in Lean's Nat subtraction."
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
  "domains": "ℕ and Nat",
  "assumptions": "n ≠ 0",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement implies a less restrictive inequality than the one required by Mathlib conventions. The English statement does not explicitly exclude the case where n is 0, which would make the inequality true but not required by Mathlib conventions.",
  "issues": [
    "The English statement assumes the inequality is strict (b ^ Nat.log b n < n) rather than non-strict (b ^ Nat.log b n ≤ n) as required by Mathlib.",
    "The English statement does not account for the totalization of division and remainders in Lean's Nat subtraction."
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


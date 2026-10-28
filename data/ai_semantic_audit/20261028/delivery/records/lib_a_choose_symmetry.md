# lib_a_choose_symmetry: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural numbers n and k with k at most n, choosing k objects from n gives the same binomial coefficient as choosing n-k objects.
```

## Lean type

```lean
open scoped BigOperators
theorem study_a_choose_symmetry (n k : ℕ) (h : k ≤ n) : n.choose k = n.choose (n - k)
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural n,k with k<=n; natural n-k is ordinary nonnegative difference under the explicit bound."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_a_choose_symmetry",
  "theorem": "AuditReference14.study_a_choose_symmetry",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (n k : ℕ) (h : k ≤ n), n.choose k = n.choose (n - k)",
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
  "candidate_id": "lib_a_choose_symmetry",
  "subject_sha256": "2a929c6bf9b93aac06d13b705479c1e8b1802fdf6d7846627150444ccfc3eb9b",
  "kind": "exact_bounded_probe",
  "checked_assignments": 45,
  "filtered_by_assumptions": 36,
  "failures": [],
  "note": "k<=n; truncated subtraction then ordinary.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 20 column 1 (char 1237)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "uncertain",
  "quantifiers": "universal quantifiers on n and k, existential quantifier on h",
  "domains": "natural numbers, existential quantifier on h",
  "assumptions": "k ≤ n, h: k ≤ n",
  "equivalence": "not explicitly stated",
  "strength": "the theorem generalizes the binomial coefficient symmetry property, but lacks specificity",
  "boundary_cases": "not provided",
  "counterexample_search": "not specified",
  "explanised": "The English proposition suggests a general principle that may not account for all edge cases, such as when k is exactly n.",
  "issues": [
    "The English statement lacks clarity on the handling of the case when k equals n.",
    "The Lean theorem does not explicitly address the case when k equals n, which could be a significant boundary case.",
    "The Lean theorem assumes h: k ≤ n without further justification, which may not be universally accepted.",
    "The Lean theorem does not address the potential for zero or negative values of k, which could lead to undefined behavior in binomial coefficient calculations.",
    "The Lean theorem does not mention the handling of the case when n is zero or negative, which is mathematically relevant for binomial coefficients."
  ]
}

```json
{
  "label": "uncertain",
  "quantifiers": "universal quantifiers on n and k, existential quantifier on h, and implicit assumption that n and k are natural numbers",
  "domains": "natural numbers, with implicit assumption that n, k ≥ 0, and h: k ≤ n",
  "assumptions": "k ≤ n, h: k ≤ n",
    "strength": "The theorem suggests a general principle of binomial coefficient symmetry, but lacks explicit handling of edge cases and potential issues with zero or negative inputs.",
    "boundary_cases": "not provided",
    "counterexample_search": "not specified",
    "explanation": "The English proposition suggests a general principle that may not account for all edge cases, such as when k equals n, and lacks clarity on handling zero or negative inputs.",
    "issues": [
      "Lack of clarity on handling k equals n case.",
      "No explicit handling of zero or negative values for n or k.",
      "No mention of potential issues with zero or negative inputs.",
      "No boundary case analysis provided.",
      "No counterexample search specified to challenge the equivalence or generality of the proposition."
    ]
  ]
}
```
}

````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each on n and k",
  "domains": "both ℕ",
  "assumptions": "one n > 0 and one h : k ≤ n",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "none",
  "counterexample_search": "no found counterexample",
  "explanation": "The statement is true as choosing k items from n is equivalent to choosing n-k items from n, reflecting the symmetry property of binomial coefficients.",
  "issues": []
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "one each on n and k",
  "domains": "both ℕ",
  "assumptions": "one n > 0 and one h : k ≤ n",
  "equivalence": "conclusion is equivalent",
  "strength": "same",
  "boundary_cases": "none",
  "counterexample_search": "no found counterexample",
  "explanation": "The statement is true as choosing k items from n is equivalent to choosing n-k items from n, reflecting the symmetry property of binomial coefficients.",
  "issues": []
}

```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "tentatively_retain_subject_to_resolving_all_disagreements"
}
```


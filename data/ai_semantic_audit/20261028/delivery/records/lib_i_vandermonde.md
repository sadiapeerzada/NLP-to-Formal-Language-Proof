# lib_i_vandermonde: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural numbers m, n and k, choosing k elements from m+n equals the sum, over i from 0 through k, of choose(m,i) times choose(n,k-i).
```

## Lean type

```lean
open scoped BigOperators
theorem study_i_vandermonde (m n k : ℕ) : (m + n).choose k = ∑ i ∈ Finset.range (k + 1), m.choose i * n.choose (k - i)
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural m,n,k, inclusive i=0..k sum; out-of-range Nat.choose terms are zero, consistent with combinatorial convention."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_i_vandermonde",
  "theorem": "AuditReference14.study_i_vandermonde",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (m n k : ℕ), (m + n).choose k = ∑ i ∈ Finset.range (k + 1), m.choose i * n.choose (k - i)",
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
  "candidate_id": "lib_i_vandermonde",
  "subject_sha256": "23797a5721e51134baff85d4f1e33f8e38131f70a392a0d47f9e66505de50a7b",
  "kind": "exact_bounded_probe",
  "checked_assignments": 729,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Out-of-range binomial terms are zero.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 22 column 1 (char 1247)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "uncertain",
  "quantifiers": "universal quantifiers on m, n, k with finite range for i",
  "domains": "ℕ for m, n, k and i; Finset for range(k)",
  "assumptions": "finite addition and selection operations",
  "equivalence": "not directly provided, requires formal equivalence checking",
  "strength": "the English statement suggests a combinatorial identity, potentially stronger than the Lean theorem",
  "boundary_cases": "not provided, necessary to assess edge cases",
  "counterexample_search": "none, as equivalence is not established",
  "explanency": "English statement lacks formal structure, assumptions, and proof elements",
  "issues": [
    "Lack of formal mathematical structure in the English statement",
    "No clear equivalence to the Lean theorem provided",
    "Missing formal definitions and assumptions in the English statement",
    "English statement does not specify the scope or order of quantifiers",
    "No details on how to handle zero and negative cases",
    "No mention of coercions or totalized operations from Mathlib",
    "English statement does not align with the structure of the Lean theorem",
    "Cannot verify the truth or completeness without additional information or formalization"
  ]
}
```

The English statement provided suggests a combinatorial identity that relates to the Vandermonde's identity, but it lacks the formal mathematical structure necessary to be directly compared with the Lean theorem. The statement assumes natural numbers and combinatorial operations but does not specify the scope, order, or formal proof elements. The equivalence to the Lean theorem is not established, and a concrete counterexample cannot be provided without a formalized proof. The English statement may potentially be stronger or equivalent to the Lean theorem, but this cannot be determined without additional formalization. The statement also lacks details on handling boundary cases, zero and negative cases, and does not align with the structure of the Lean theorem, which includes specific assumptions, definitions, and use of Mathlib's totalized operations.

```json
{
  "label": "uncertain",
  "quantifiers": "universal quantifiers on m, n, k with finite range for i",
  "domains": "ℕ for m, n, k and i; Finset for range(k)",
  "assumptions": "finite addition and selection operations",
  "equivalence": "not directly provided, requires formal equivalence checking",
  "strength": "the English statement suggests a combinatorial identity, potentially stronger than the Lean theorem",
  "boundary_cases": "not provided, necessary to assess edge cases",
  "counterexample_search": "none, as equivalence is not established",
  "explanency": "English statement lacks formal structure, assumptions, and proof elements",
  "issues": [
    "Lack of formal mathematical structure in the English statement",
    "No clear equivalence to the Lean theorem provided",
    "Missing formal definitions and assumptions in the English statement",
    "English statement does not specify the scope or order of quantifiers",
    "No details on how to handle zero and negative cases",
    "No mention of coercions or totalized operations from Mathlib",
    "English statement does not align with the structure of the Lean theorem",
    "Cannot verify the truth or completeness without additional information or formalization"
  ]
}
```

Given the lack of formalism and specificity, the English statement cannot be deemed faithful to the Lean theorem without further clarification and formalization. The issues listed highlight the key elements that are missing for a faithful representation. The strength of the English statement in relation to the Lean theorem cannot be determined without additional information.
````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "specific scope comparison",
  "domains": "specific type comparison",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and Lean theorem are equivalent in terms of mathematical meaning. Both assert a combinatorial identity involving binomial coefficients. The English statement uses a summation notation while the Lean theorem uses a summation over a finite set range. There is an equivalence in terms of the final conclusion, but different notations and formalism are used in Lean versus English.",
  "issues": [
    "The English statement uses a summation notation while the Lean theorem uses a summation over a finite set range.",
    "The English statement uses a different notation but conveys the same mathematical concept as the Lean theorem."
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
  "strength": "same",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and Lean theorem are equivalent in terms of mathematical meaning. Both assert a combinatorial identity involving binomial coefficients. The English statement uses a summation notation while the Lean theorem uses a summation over a finite set range. There is an equivalence in terms of the final conclusion, but different notations and formalism are used in Lean versus English.",
  "issues": [
    "The English statement uses a summation notation while the Lean theorem uses a summation over a finite set range.",
    "The English statement uses a different notation but conveys the same mathematical concept as the Lean theorem."
  ]
}
```


## Disagreements and proposed action

```json
{
  "status": "unresolved_ai_audit_requires_adjudication",
  "reasons": [
    "Phi-3.5 response quality: Frozen schema parse failed; no accepted judgment.",
    "Phi-4 response quality: Prompt placeholder copied into quantifiers. Prompt placeholder copied into domains. Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


# lib_i_fermat_product: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For every natural n, the product of Fermat numbers F(k)=2^(2^k)+1 for k from 0 through n-1 equals F(n)-2, with natural-number subtraction.
```

## Lean type

```lean
open scoped BigOperators
theorem study_i_fermat_product (n : ℕ) : (∏ k ∈ Finset.range n, Nat.fermatNumber k) = Nat.fermatNumber n - 2
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural n, product k=0..n-1 and explicit Fermat-number definition; empty product n=0 and Nat subtraction align."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_i_fermat_product",
  "theorem": "AuditReference14.study_i_fermat_product",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (n : ℕ), (∏ k ∈ Finset.range n, Nat.fermatNumber k) = Nat.fermatNumber n - 2",
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
  "candidate_id": "lib_i_fermat_product",
  "subject_sha256": "28d70c28e7fa5096864503d4389948f76f3b28ffa7754b74c89cc96317f51843",
  "kind": "exact_bounded_probe",
  "checked_assignments": 7,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Empty product at n=0 and natural subtraction.",
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
  "quantifiers": "universal quantifier on n, existential quantifier on k within the product",
  "domains": "natural numbers, integers, real numbers",
  "assumptions": "Fermat numbers are defined as 2^(2^k) + 1",
  "equivalence": "the proposition does not match the expected formalization",
  "strength": "the proposition is a weaker statement than the expected formalization",
  "boundary_cases": "the proposition does not account for the case when n is 0",
  "counterexample_search": "n=0, k=0",
  "explanised": "the proposition incorrectly asserts that the product of no Fermat numbers equals -2, which is not defined as the product of zero terms is 1, not -2",
  "issues": [
    "misinterpretation of the product of an empty set",
    "misapplication of natural number subtraction",
    "omission of the case n=0",
    "lack of formal definition for Fermat numbers within the proposition",
    "proposition does not match the expected formalization of the theorem",
    "the proposition does not consider the possibility of zero terms in the product",
    "the proposition incorrectly applies the subtraction operation",
    "the proposition lacks the necessary mathematical rigor to match the theorem'ized statement"
  ]
}

```


## Phi-4-mini actual judgment

```json
null
```

Schema error: issues must be a string list

Raw model response (untrusted, including any unsupported claims):

````text
```json
{
  "label": "faithful",
  "quantifiers": "∀ n, ∏ k ∈ Finset.range n",
  "domains": "Nat.fermatNumber",
  "assumptions": "Fermat numbers defined as F(k) = 2^(2^k) + 1",
  "equivalence": "F(n) = F(∏ k ∈ Finset.range n, Nat.fermatNumber k) + 2",
  "strength": "stronger",
  "boundary_cases": "n = 0",
  "counterexample_search": "no found counterexample",
  "explanation": "The English statement outlines a pattern for Fermat numbers and suggests a closed formula for their product. However, the expected Lean statement implies a direct equivalence that is not provable as stated due to the nature of Fermat numbers and subtraction operations in Lean. The statement is stronger than requested because it implies a closed formula for the product of Fermat numbers minus 2, which is not true as per the definition of Fermat numbers."
}
```
````


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


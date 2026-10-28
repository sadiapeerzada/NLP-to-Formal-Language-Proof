# lib_d_euclidean_gcd: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural m and n, gcd(m,n) equals gcd(n modulo m,m), including m=0 under totalized natural remainder.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_euclidean_gcd (m n : ℕ) : Nat.gcd m n = Nat.gcd (n % m) m
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural m,n including m=0; remainder is n modulo m, and gcd arguments are remainder then m, exactly as stated."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_euclidean_gcd",
  "theorem": "AuditReference15.study_d_euclidean_gcd",
  "source": "data/curation_batches/v0.2.1/references_expanded.lean",
  "expected_type": "∀ (m n : ℕ), Nat.gcd m n = Nat.gcd (n % m) m",
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
  "candidate_id": "lib_d_euclidean_gcd",
  "subject_sha256": "cf7108509717b5955383e831f61a84d4fcbc7e3c4a45ed303f9412724eb74de0",
  "kind": "exact_bounded_probe",
  "checked_assignments": 81,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "Zero modulus totalization.",
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
  "domains": "specific",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and Lean theorem are equivalent in meaning but different in expression due to different handling of division and remainders in Mathlib versus Lean's Nat subtraction and division. The English statement uses 'modulo' while Lean uses 'mod', and division is totalized in Mathlib while division returns a quotient and a remainder in Lean.",
  "issues": [
    "Division and remainder handling",
    "mod versus mod",
    "totalization versus truncation"
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
  "domains": "specific",
  "assumptions": "specific hypothesis comparison",
  "equivalence": "conclusion comparison",
  "strength": "stronger",
  "boundary_cases": "specific zero/endpoint/sign check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement and Lean theorem are equivalent in meaning but different in expression due to different handling of division and remainders in Mathlib versus Lean's Nat subtraction and division. The English statement uses 'modulo' while Lean uses 'mod', and division is totalized in Mathlib while division returns a quotient and a remainder in Lean.",
  "issues": [
    "Division and remainder handling",
    "mod versus mod",
    "totalization versus truncation"
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
    "Phi-4 response quality: Prompt placeholder copied into assumptions. Prompt placeholder copied into equivalence. Prompt placeholder copied into boundary_cases. Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


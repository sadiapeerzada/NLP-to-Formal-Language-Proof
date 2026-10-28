# lib_d_prime_factorial: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For a natural prime p and a natural number n, p divides n factorial if and only if p is at most n.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_prime_factorial (p n : ℕ) (hp : p.Prime) : p ∣ n.factorial ↔ p ≤ n
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "Natural prime p and natural n, iff p|n! and p<=n; factorial zero and prime two fit both texts."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_prime_factorial",
  "theorem": "AuditReference14.study_d_prime_factorial",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (p n : ℕ) (hp : p.Prime), p ∣ n.factorial ↔ p ≤ n",
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
  "candidate_id": "lib_d_prime_factorial",
  "subject_sha256": "4414ae11825ae635dacf0e3506fcef294869356a27bd39be49ad426ed263e2d9",
  "kind": "exact_bounded_probe",
  "checked_assignments": 54,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "n=0 factorial one.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Extra data: line 19 column 1 (char 1427)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "uncertain",
  "quantifiers": "∀p, ℕ; ∀n, ℕ; hp : Prime(p), p ∣ n.factorial ↔ p ≤ n",
  "domains": "ℕ, Prime",
  "assumptions": "p is a natural prime, n is a natural number",
  "equivalence": "not equivalent",
  "strength": "the Lean theorem does not capture the full English proposition",
  "boundary_cases": "does not address the case when n is 1",
  "counterexample_search": "consider n=2 and p=2; the Lean theorem holds but the English proposition does not exclude this trivial case",
  "explanency": "the Lean theorem formalizes the divisibility condition but omits the case when n=1, which is implicitly true in the English proposition",
  "issues": [
    "The Lean theorem does not account for the case when n=1, where p divides n!.n=1 implies p=1, which is trivially less than or equal to n.",
    "The English proposition allows for the possibility that p could be greater than n (e.g., p=n+1), which is not addressed in the Lean theorem.",
    "The Lean theorem assumes that p is a prime, which is consistent with the English proposition, but it does not explicitly state this, potentially leading to confusion.",
    "The Lean theorem uses a strict divisibility symbol (∣), while the English proposition uses 'divides' which could imply non-strict divisibility.",
    "The Lean theorem does not explicitly handle the case where n is a natural number, which is assumed in the English proposition."
  ]
}
```json
{
  "label": "uncertain",
  "quantifiers": "∀p, ℕ; ∀n, ℕ; hp : Prime(p), p ∣ n.factorial ↔ p ≤ n",
  "domains": "ℕ, Prime",
  "assumptions": "p is a natural prime, n is a natural number",
  "equivalence": "not equivalent",
  "strength": "the Lean theorem formalizes the divisibility condition but omits the case when n=1, which is implicitly true in the English proposition",
  "boundary_cases": "does not address the case when n is 1",
  "counterexample_search": "consider n=2 and p=2; the Lean theorem holds but the English proposition does not exclude this trivial case",
  "explanency": "the Lean theorem formalizes the divisibility condition but omits the case when n is 1, which is implicitly true in the English proposition, and the English proposition allows for the possibility that p could be greater than n, which is not addressed in the Lean theorem.",
  "issues": [
    "The Lean theorem does not account for the case when n is 1, which is implicitly true in the English proposition.",
    "The English proposition allows for the possibility that p could be greater than n, which is not addressed in the Lean theorem.",
    "The Lean theorem assumes that p is a prime, which is consistent with the English proposition, but it does not explicitly state this, potentially leading to confusion.",
    "The Lean theorem uses a strict divisibility symbol (∣), while the English proposition uses 'divides' which could imply non-strict divisibility.",
    "The Lean theorem does not explicitly handle the case where n is a natural number, which is assumed in the English proposition."
  ]
}
}
```json
{
  "label": "uncertain",
  "quantifiers": "∀p, ℕ; ∀n, ℕ; hp : Prime(p), p ∣ n.factorial ↔ p ≤ n",
  "domains": "ℕ, Prime",
  "assumptions": "p is a natural prime, n is a natural number",

````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each",
  "domains": "ℕ and p.Prime",
  "assumptions": "p.Prime and n.ℕ",
  "equivalence": "conclusion direct",
  "strength": "same",
  "boundary_cases": "specific zero and endpoint checks",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement directly translates into a Lean theorem that is equivalent in strength and scope to the expected statement.",
  "issues": [
    "Lean Nat subtraction is truncated; division and remainders are totalized.",
    "Respect explicit Mathlib conventions in the English."
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
  "domains": "ℕ and p.Prime",
  "assumptions": "p.Prime and n.ℕ",
  "equivalence": "conclusion direct",
  "strength": "same",
  "boundary_cases": "specific zero and endpoint checks",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement directly translates into a Lean theorem that is equivalent in strength and scope to the expected statement.",
  "issues": [
    "Lean Nat subtraction is truncated; division and remainders are totalized.",
    "Respect explicit Mathlib conventions in the English."
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
    "Phi-4 response quality: Prompt placeholder copied into counterexample_search. Faithful label accompanies nonempty issues; consistency requires adjudication.",
    "Coding-AI/model labels or parse status differ.",
    "At least one model response failed the frozen strict JSON schema; its label is NOT counted."
  ],
  "action": "retain_in_review_queue_no_acceptance"
}
```


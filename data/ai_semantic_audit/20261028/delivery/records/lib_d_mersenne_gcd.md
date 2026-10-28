# lib_d_mersenne_gcd: AI-only audit

No human review or approval. Existing curation and eligibility are unchanged.

## English

```text
For natural numbers a, b and c, the greatest common divisor of a^b-1 and a^c-1 equals a raised to gcd(b,c), minus one; subtraction is natural-number subtraction.
```

## Lean type

```lean
open scoped BigOperators
theorem study_d_mersenne_gcd (a b c : ℕ) : Nat.gcd (a ^ b - 1) (a ^ c - 1) = a ^ Nat.gcd b c - 1
```

## Coding-assistant static assessment

```json
{
  "label": "faithful",
  "note": "All three variables natural; the English explicitly declares truncated subtraction, essential for base zero and zero exponents."
}
```


## Fresh Lean check

```json
{
  "candidate_id": "lib_d_mersenne_gcd",
  "theorem": "AuditReference14.study_d_mersenne_gcd",
  "source": "data/curation_batches/v0.2.0/references_expanded.lean",
  "expected_type": "∀ (a b c : ℕ), Nat.gcd (a ^ b - 1) (a ^ c - 1) = a ^ Nat.gcd b c - 1",
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
  "candidate_id": "lib_d_mersenne_gcd",
  "subject_sha256": "535af04535e01b802324c17c88a11b41843fd8b558516b09cd048a701cb5b0d9",
  "kind": "exact_bounded_probe",
  "checked_assignments": 125,
  "filtered_by_assumptions": 0,
  "failures": [],
  "note": "a=0 and zero exponents use Nat truncation, not integer -1.",
  "status": "no_counterexample_in_stated_grid",
  "scope": "Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification."
}
```


## Phi-3.5 actual judgment

```json
null
```

Schema error: Expecting ',' delimiter: line 19 column 21 (char 1569)

Raw model response (untrusted, including any unsupported claims):

````text
{
  "label": "not faithful",
  "quantifiers": "universal quantifiers on a, b, c with Nat truncation for subtraction",
  "domains": "natural numbers with truncation for subtraction",
  "assumptions": "Nat.gcd and exponentiation are defined with truncation",
  "equivalence": "proposition does not directly translate to Lean's expected theorem",
  "strength": "general Lean theorem is stronger due to unspecified assumptions",
  "boundary_cases": "zero and negative cases not addressed",
  "counterexample_search": "counterexample in natural numbers with b=c to show incorrect subtraction",
  "explanency": "English statement lacks clarity on exponentiation and subtraction rules",
  "issues": [
    "SUBTRACTION: The English statement implies natural number subtraction, but Lean requires explicit handling of truncation.",
    "EXPONENTIATION: The statement does not account for the potential issues with exponentiation in natural numbers, such as zero exponentiation.",
    "SCOPE: The English statement does not specify the scope of quantifiers, which is crucial for formalization.",
    "HYPOTHESIS: The statement assumes properties of exponentiation and GCD that are not trivially provable.",
    "STRENGTH: The general Lean theorem assumes the totality of operations, which is not specified in the English statement.",
    "CONTRACT: The English statement does not match the expected Lean theorem, which includes the totality of operations.",
    "COERCION: The handling of exponentiation and subtraction in Lean requires explicit coercions.",
    "COUNTEREXAMPLE": "Choose a=2, b=c=1; the English statement suggests GCD(2^1-1, 2^1-1) equals 2^(GCD(1,1))-1, which is 1, but in Lean, this needs to account for operation truncation.",
    "IMPLICATIONS": "The English statement lacks precision, making it difficult to formalize.",
    "RECOMMENDATION": "Specify assumptions about exponentiation and subtraction in Lean, and clarify the scope of quantifiers."
}
```

Note: The provided JSON object is a structured summary of the issues with the faithfulness of the English proposition to the expected Lean theorem, based on the analysis of the given information and common mathematical formalization practices. It does not contain actual Lean code or proofs, as the task specifies not to claim to have run Lean or any proof-related tools.
````


## Phi-4-mini actual judgment

```json
{
  "label": "faithful",
  "quantifiers": "one each a, b, c",
  "domains": "ℕ",
  "assumptions": "one each a, b, c",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific endpoint check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement accurately describes a theorem in number theory concerning Mersenne numbers and greatest common divisors (gcd). It equates the gcd of a^b-1 and a^c-1 to a raised to the power of gcd(b,c)-1. This is consistent with the expected Lean statement provided.",
  "issues": [
    "The English statement assumes subtraction is natural-number subtraction, which is true in this context but not explicitly stated in the expected Lean statement."
  ]
}
```

Schema error: None

Raw model response (untrusted, including any unsupported claims):

```text
{
  "label": "faithful",
  "quantifiers": "one each a, b, c",
  "domains": "ℕ",
  "assumptions": "one each a, b, c",
  "equivalence": "conclusion comparison",
  "strength": "same",
  "boundary_cases": "specific endpoint check",
  "counterexample_search": "specific candidate example or no found counterexample",
  "explanation": "The English statement accurately describes a theorem in number theory concerning Mersenne numbers and greatest common divisors (gcd). It equates the gcd of a^b-1 and a^c-1 to a raised to the power of gcd(b,c)-1. This is consistent with the expected Lean statement provided.",
  "issues": [
    "The English statement assumes subtraction is natural-number subtraction, which is true in this context but not explicitly stated in the expected Lean statement."
  ]
}
```


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


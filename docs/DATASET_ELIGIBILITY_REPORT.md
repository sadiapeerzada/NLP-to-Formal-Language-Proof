# Dataset eligibility — 27 October 2026

Status: BLOCKED. Machine evidence: `data/analysis/verified_readiness_20261027/readiness.json`.

| Quantity | Confirmed count |
|---|---:|
| Candidates | 37 |
| Proposed development / test | 29 / 8 |
| Eligible development / test | 0 / 0 |
| Completed independent semantic reviews | 0 |
| Frozen eligible records | 0 |
| Categories | 5 |
| Structural errors | 0 |
| Review warnings | 95 |
| Freeze validation errors | 14 |
| Strict-proof evidence | 12 |
| Existing statement-only checks | 4 |
| New strict-proof-verified reference theorems | 2 |

Two new sourced candidates in `data/curation_batches/v0.1.8/` concern greatest-modulus optimization and an integer Diophantine parameterization, rather than coefficient variants of existing records. Exact citations, adaptation scope, source-byte hashes, assumptions and imports are provided. Initial checks timed out; both subsequently passed strict verification with narrower imports. Neither is eligible without independent reviews. They are authored reference preparation, not model generations.

Exact publisher pages and textbook PDF were captured under `data/source_archives/20261027_curl/`; attribution/license notice accompanies them. New retrieval does not retroactively authenticate historical bytes. Source compatibility, redistribution obligations and third-party API-input use still require genuine review. Groq HTML bytes have no established redistribution clearance and remain local/ignored; their public URLs and hashes are committed.

The prepared review queue has one hash-bound packet per candidate, all human decisions pending, with faithful / not faithful / uncertain labels available. A known exact-English duplicate (`arith_003`, `arith_003_mathlib`) and other family/similarity warnings remain unresolved. Proposed labels do not establish family independence.

No freeze was created. The minimum target remains 60 eligible test examples plus 15–20 eligible development examples. Expanding from 35 to 37 does not satisfy it; acquisition and proof engineering are PARTIALLY COMPLETE. At least 38 additional distinct candidates are needed even before exclusions, duplicate removal and review. The 29 proposed development assignments must be reconsidered as whole families, without examining held-out model outcomes.

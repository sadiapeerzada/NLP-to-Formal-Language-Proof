# Compiler-Guided Repair for Natural-Language-to-Lean Formalization

The reviewed empirical study is available in the [publication bundle](publication/README.md), including the [anonymized manuscript](publication/paper/publication_review.pdf), [research-integrity review](publication/RESEARCH_INTEGRITY_REVIEW.md), and [exact payload manifest](publication/PUBLIC_PAYLOAD_MANIFEST.json).

The frozen dataset has 15 eligible development statements and 60 held-out statements. There are 58 complete A/B/C comparisons. One-shot generation succeeds on 0/60; blind and compiler-guided repair each succeed on 1/60 under missing-as-failure sensitivity. C has 58 observed outcomes and two unavailable outcomes; among complete pairs B and C each succeed once (1/58). The experiment establishes neither a compiler-feedback advantage nor equivalence.

The bundle contains the approved privacy-redacted final-study evidence, original candidate hashes, scientific source snapshot, attribution, analysis, and offline verifiers. Exact original prompts and private evidence remain local; redacted views do not claim exact-byte inference replay. See the bundle's reproducibility and licensing disclosures.

Verify the public bundle without inference or paid services:

```sh
python3 publication/verify_payload.py
python3 publication/reanalyze.py
```

The existing project directories outside `publication/` are retained as historical preparation and implementation artifacts. Their earlier readiness reports, proposed datasets, protocols, and pre-results paper describe earlier stages; use `publication/` for the reviewed empirical results and publication-safety assessment. No historical smoke-test or manually authored proof is promoted into a final model success.

The publication branch was deliberately created without private research ancestry. Its merge preserves the existing project and places the unchanged approved payload under `publication/`; the private research and audit branches are not included.

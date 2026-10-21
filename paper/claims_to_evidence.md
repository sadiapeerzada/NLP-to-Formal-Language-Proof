# Paper claims-to-evidence audit

This audit records what can be supported from the repository at the Phase 6
draft. `Unavailable` means the evidence needed to make the claim does not
exist; it is not a zero-valued experimental result.

| Manuscript statement or required claim | Evidence inspected | Status / allowed wording |
|---|---|---|
| Dataset size and composition | `data/research_dataset_inventory_v0.2.0.json`, baseline draft, six `candidate_records.json` batch files | 31 candidates; 23 proposed development / 8 proposed test; 5 categories; 0 eligible. Do not call these benchmark or frozen-split counts. |
| Lean verification coverage | Research inventory and candidate verification metadata | Inventory records 10 strict Lean-verified candidates. This does not imply 10 eligible records or semantic faithfulness. |
| Source provenance and rights | Source ledger; candidate records; DMOI3 source/license statement | 10 item citations point to DMOI3; 21 baseline records lack item-level citations. Rights review and source-byte archival are incomplete. No record is declared cleared for redistribution. |
| A/B/C design | Protocol v0.2.0 and `src/repair_experiment.py` | A/B/C design is implemented/proposed. Protocol is not approved or preregistered. No measured condition outcome. |
| Primary model | Protocol v0.2.0 and historical run manifests | Proposed mutable alias `openai/gpt-oss-120b`; generation access and immutable revision unverified. Historical model strings do not establish API execution. |
| Dataset freeze / held-out test | `data/research_dataset_manifest_v0.1.0.json`; validator inventory | Manifest status is draft; eligible count is 0; no frozen test set exists. No held-out evaluation claim. |
| First-attempt or repair success | `data/analysis/analysis_readiness_v0.1.0.json`; `data/experiments/` inventory | No paired API run manifests; metrics unavailable. Legacy pipeline/pilot outcomes are excluded. |
| Pass@1 from historical demonstrations | `RUN_REPORT.md`, `data/results/run1_core_lean.jsonl`, legacy attempts | Candidate proofs were manually authored and compiler-checked. They are not autonomous model pass@1. |
| Compiler taxonomy effect | Paired experiment manifests and raw matched outcomes | No qualifying A/B/C traces. Taxonomy effect unavailable. |
| Semantic faithfulness | Candidate review fields and review records | All 31 candidates are pending/unreviewed for semantic fidelity; there is no test-set faithfulness estimate. |
| Qualitative examples | Five selected attempt 1/2 pairs from `data/results/attempts/*.jsonl` | Manual compiler-checking examples only. Saved attempt outcomes are failures; legacy records do not preserve exit codes. They are not API or A/B/C examples. |
| Cost, tokens, and latency | Cost guard, run manifests, protocol and raw artifacts | No paired-run aggregates. Pricing remains unverified; no cost estimate or model-run resource total is reported. |
| Statistical evidence | No frozen denominator or matched pairs | Confidence intervals, McNemar tests, Holm-adjusted p-values, and power statements unavailable. |
| Reproduction | Toolchain and Mathlib lock, prompt hashes, scripts, run schemas | Configuration is recorded, but the paper cannot be empirically reproduced until frozen data and raw paired API runs exist. LNCS PDF build also requires Springer class files not present in this repository. |

## Claims excluded from the draft

- No A/B/C success rate, effect size, significance, category effect, or
  semantic accuracy.
- No claim that Lean compilation proves the English translation is correct.
- No claim that requested model metadata proves provider generation occurred.
- No claim that public access to a source establishes redistribution rights.
- No autonomous LLM pass@1 claim from historical manual demonstrations.
- No assertion that the protocol, dataset, pricing, or submission gate is
  approved, frozen, or complete.

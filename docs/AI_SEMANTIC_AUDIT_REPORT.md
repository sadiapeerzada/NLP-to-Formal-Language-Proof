# AI-only semantic audit — 28 October 2026

All **96 candidates** now have an AI audit record, a fresh exact-type Lean reference check, a bounded mathematical probe and a proposed disposition. **None is certified for acceptance.** All 96 remain in the adjudication queue because model disagreements, invalid outputs or response-quality problems remain unresolved. This does not mean all 96 propositions are wrong.

The proposed dataset adds AI evidence outside the original curation fields. It does not impersonate a human reviewer, approve a source license, establish family independence, change a split, freeze data or authorize an experiment. Independent human reviews and eligible development/test counts remain zero.

## Deliverables

- [Per-item index](../data/ai_semantic_audit/20261028/delivery/README.md), linking 96 detailed Markdown and JSON records.
- [Proposed AI-audited dataset](../data/ai_semantic_audit/20261028/delivery/proposed_ai_audited_dataset.json), containing all 96 original prepared records plus explicitly AI-only evidence. The assembler verifies that every existing field is unchanged.
- [Disagreement ledger](../data/ai_semantic_audit/20261028/delivery/disagreements.json), [proposed actions](../data/ai_semantic_audit/20261028/delivery/proposed_actions.json) and [machine summary](../data/ai_semantic_audit/20261028/delivery/summary.json).
- [95-ID proposal after exact duplicate exclusion](../data/ai_semantic_audit/20261028/delivery/proposed_unique_candidate_ids.json). This is a candidate list, not a frozen dataset or a claim of family independence.
- [Specific revision proposals](../data/ai_semantic_audit/20261028/proposed_revisions.json), [supervisor policy request](AI_SEMANTIC_REVIEW_SUPERVISOR_REQUEST.md) and [reproduction instructions](AI_AUDIT_REPRODUCIBILITY.md).

## Review workflow and actual execution

The primary experimental model remains Qwen2.5-7B-Instruct-4bit. This audit used free local MLX inference with separately downloaded Phi-family weights. Prompts expose English, the exact theorem type, imports and explicit custom definitions; they withhold reference proofs, prior judgments, source difficulty and split assignments. Each candidate gets a fresh conversation. Exact subjects, prompts, seeds, token counts, runtime metadata, model inventories, raw responses and per-token traces are preserved.

| Reviewer stage | Actual execution | Important limits |
|---|---|---|
| Coding-assistant static assessment | All 96; 94 provisionally faithful, one mismatch, one uncertain | These are coding-AI judgments, not ground truth. The assistant helped prepare the dataset and is not author-independent. Notes were sealed before inspecting Phi outputs. |
| Phi-3.5-mini-instruct, 4-bit | 68 completed; one interrupted; 27 unattempted after retirement | 60 schema failures, seven `not faithful`, one `uncertain`. Persistent invalid responses and unsupported objections led to explicit retirement, preserving all evidence. No missing verdict is invented. |
| Phi-4-mini-instruct, 4-bit | All 96 completed | 72 schema-valid `faithful`, 11 schema-valid `not faithful`, 13 invalid-format outputs. Only 10 responses escaped the implemented basic quality flags; this is not a claim that those 10 judgments are correct. |

Phi-4 and a shorter balanced prompt were introduced after observing Phi-3.5 failures. The change is disclosed in the second manifest, and no first-model result was erased. Both Phi models share a family, so their errors are not assumed independent. Model and prompt changed together; this is not a controlled comparison of reviewer models. No experimental repair prompt/model was tuned on these audit outcomes.

There were **165 review generation attempts: 164 completions and one interruption**. The interrupted context was not replayed. The separate synthetic calibration added 12 completed diagnostic generations. Total audit/control attempts were 177, with 176 completions; no paid inference was used. These are curation/judge diagnostics, not A/B/C proof-repair trajectories or a qualifying mathematical pilot.

Phi-3.5 snapshot: `7b2052fd882fe017300d4d42a4eb06a27b816af4`; Phi-4 snapshot: `ac1c269cb4222a4e136a3d09edad301056c1f36a`. Model inventories bind the actual 4-bit weight, tokenizer, configuration and chat-template bytes. Cards and upstream MIT license evidence are archived in `model/` and `model_phi4/`. Original sources: [Microsoft Phi-3.5 card](https://huggingface.co/microsoft/Phi-3.5-mini-instruct/tree/2fe192450127e6a83f7441aef6e3ca586c338b77) and [Microsoft Phi-4-mini card](https://huggingface.co/microsoft/Phi-4-mini-instruct/tree/cfbefacb99257ffa30c83adab238a50856ac3083).

## Concrete findings and proposed changes

1. **`mod_001`: omitted positive-modulus hypothesis.** English requires a positive integer modulus; Lean quantifies over all integer moduli without that premise. The stronger Lean theorem is true, but it does not preserve the requested restriction. A separately compiled proposed revision adds `0 < m`, preserving the existing English. The historical candidate remains untouched.
2. **`ind_001`: clarify the summation endpoints.** “First n natural numbers” can mean 0 through n−1 or 1 through n. The stated formula suggests the latter; Lean sums 0 through n. Proposed English explicitly says 1 through n, with the empty sum at zero. This is a conservative clarification request, not proof that the intended conventional reading is false.
3. **`arith_003_mathlib`: exact duplicate.** It duplicates `arith_003` in both English and theorem proposition, ignoring theorem names. The automated comparison and static assessment agree. Exclude the alias from any future independent benchmark, while preserving both historical records.
4. **Proof methods and equivalent encodings need separate treatment.** The theorem type cannot enforce “use induction” in `ind_005`, `ineq_004` or `ind_009`. The geometric-sum `+1` encoding is equivalent to subtraction under the relevant natural-number bounds; binary Finset witnesses include singleton powers and enforce distinct exponents. These distinctions are documented per item rather than automatically rejected.
5. **Model judgments contain demonstrable errors.** Phi-4 claims n=1 makes n(n+1) odd, although the product is two. The exact arithmetic check and bound response hash are in [refuted model claims](../data/ai_semantic_audit/20261028/refuted_model_claims.json). Other responses invent omissions, confuse induction with quantification, contradict their own labels, or copy prompt placeholders. Schema-valid JSON alone is not a substantive semantic review.

There is no automatic majority vote. Nine items have a tentative retain proposal subject to resolving all disagreements; 84 remain in the review queue without acceptance, one needs a proposed revision, one clarification and one duplicate exclusion. Every record remains unresolved for policy/acceptance purposes. Source provenance, rights, category/difficulty and cross-family independence still require separate decisions; the original 21 source-provenance gaps remain.

## Lean and mathematical evidence

The fresh batch in `lean_reference_check/` compiled all **96 reference proofs and exact theorem-type comparisons**, without placeholder proofs. Each target's dependencies were inspected against the existing allowed axiom policy. This establishes reference proposition truth and exact type binding, not English equivalence.

The handwritten mathematical probes cover all 96 items across **26,467 accepted finite assignments**: 88 exact integer/rational predicates and eight approximate numerical probes. No bounded probe failed. Their domains, hypothesis filters, totalized arithmetic conventions, witness-search bounds and tolerances are recorded in the source and results. These are coding-AI-authored translations, not an automatic English parser or independent formal specification. Finite agreement cannot prove universal equivalence; bounded witness-search failure would be inconclusive, and floating-point checks are not real-number proofs.

Additional successful Lean checks in `semantic_bridges/` cover the geometric-sum encoding, endpoint and missing-premise counterexamples, singleton binary witnesses, positive-sum nonemptiness, totalized logarithm, the proposed positive-modulus correction and the formal references for synthetic controls. Earlier evidence remains unchanged.

## Development-only experiments and engineering

Twelve synthetic semantic-judge controls were authored outside the research pool, with expected labels hidden from the reviewer. The actual diagnostic result was **four usable responses: three matched the authored expectation, one did not; eight were unusable** under the implemented checks. These controls are not independently human-adjudicated gold and provide no generalization accuracy estimate. Their formal sides compiled in Lean. The poor response quality further argues against blanket AI certification.

The workflow includes strict parse rejection, explicit template-echo/consistency flags, prompt/subject/model/source bindings, durable attempt and token journals, replay rejection, primary-pass completeness checks, stale-input rejection, exact duplicate detection and curation-invariance tests. Raw parser outcomes were not rewritten after adding post-hoc quality checks. The final suite passed **287 tests and 28 subtests in 52.44 seconds**; actual output is in `verification/pytest_final.log`. Both model inventories, raw evidence and unchanged gate-file hashes are bound in the package manifest.

The actual human-review importer, dataset validator, local protocol, study runner and approval/freeze manifests match their before-audit hashes. `gates_before.json`, `gates_after.json` and `verification/unchanged_local_plan.json` document zero eligibility and the still-disabled local study. No mathematical A/B/C pilot or held-out repair experiment was run. Those tasks remain gated; the unblocked development work performed here was the synthetic judge experiment, Lean/mathematical checks and workflow engineering.

## Supervisor decision needed

The [request](AI_SEMANTIC_REVIEW_SUPERVISOR_REQUEST.md) proposes an explicitly AI-assisted alternative first-pass policy with adjudication, expert spot checks, source/family review and exact artifact approvals. **The present results do not support unconditional substitution for independent expert review.** No request has been sent and no approval has been fabricated. Even approval of an amended semantic policy would not itself satisfy source, split/freeze, local-substitution, protocol, pilot or held-out gates.

# Supervisor decision requested: local model substitution

Status: PROPOSED — not approved. Do not mark this document signed on a reviewer's behalf.

The professor requested API-generated experiments. The user now forbids paid inference and requests local MLX, so explicit supervisor acceptance of local inference is required. The research question remains C versus B for the same reviewed theorem and shared initial candidate; A is the one-shot secondary baseline.

Review package: `configs/repair_experiment_local_v0.3.0.json`, `data/local_model/20261027/model_inventory.json`, the pinned model card/license evidence, `src/local_llm_client.py`, the shared `src/repair_experiment.py` lifecycle, `src/local_protocol.py`, and the dataset/review reports. The original Groq protocol is retained unchanged.

Proposed model: cached `mlx-community/Qwen2.5-7B-Instruct-4bit`, revision `c26a38f6a37d0a51b4e9a1eb3026530fa35d9fed`, 4-bit/group-size 64. MLX-LM 0.32.2 / MLX 0.32.4; Apple M4, 16 GiB RAM. Exact weights, tokenizer, config and chat-template hashes are recorded. No new weights downloaded. Model card identifies Apache-2.0; independent compatibility review remains pending.

Proposed controls: temperature 0.2; top-p 1; 2000 output tokens; 8192 combined context tokens; three repairs each for B/C; one shared initial output; at most seven local generations per problem; no automatic retries or paid fallback. A single primary base seed 2027 uses independently bound problem/condition/attempt/prompt streams. This preserves one binary trajectory per problem and the existing exact McNemar plan. Three-seed replication is not implemented or claimed; any extension needs a preregistered problem-clustered analysis amendment before test access.

Decisions needed: accept/reject the local substitution; approve the library-derived candidate extension and its contamination/family review plan; assess B-before-C order effects, context-limit failures and fairness of feedback-bearing prompt budgets; approve independent reviewer identities and evidence; approve exact development IDs, theorem/dataset/model/protocol hashes and a fresh output directory. Approved primary outcomes concern fixed-theorem proof repair, not automatic NL semantic correctness.

A legitimate approval record must provide actual reviewer identity/kind/date, a verifiable evidence artifact/hash, local-substitution decision, exact protocol and dataset SHA-256, phase, approved IDs, maximum seven generations per problem and `paid_inference_allowed: false`. The approved protocol must enable local execution and carry genuine approved status. Held-out approval additionally requires frozen eligible splits, preregistration and an authenticated audited genuine pilot artifact. The program checks these bindings before loading/calling the model through the experiment runner.

Current blocker: zero eligible examples and no approval. Neutral READY smoke tests verify backend operation only; they cannot satisfy the requested genuine mathematical pilot. No study generation is authorized by this proposal.

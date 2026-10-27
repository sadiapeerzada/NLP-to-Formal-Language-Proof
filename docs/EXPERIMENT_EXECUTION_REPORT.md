# Experiment execution — 27 October 2026

Status: BLOCKED. Genuine paired pilot runs: 0. Genuine held-out paired runs: 0. API generation requests made this session: 0. No study statistics or significance claims computed.

The proposed primary provider/model remains Groq / `openai/gpt-oss-120b`, temperature 0.2, completion cap 2000, reasoning effort low, at most three repairs per B/C. Public [model documentation](https://console.groq.com/docs/model/openai/gpt-oss-120b) and [reasoning documentation](https://console.groq.com/docs/reasoning) were inspected and exact bytes hashed. Public documentation supports the selected token limit and reasoning option. These observations do not prove account access or authorize execution.

The captured model page lists USD 0.15 per million uncached input tokens and USD 0.60 per million output tokens. These are public page observations, not approved cost-guard settings or confirmation of account billing. The [rate-limit documentation](https://console.groq.com/docs/rate-limits) directs users to account-specific organization limits; public tables cannot establish this account's quota or free-tier status. Archive hashes/URLs: `data/source_archives/20261027_curl/manifest.json`. Credential presence was checked as a boolean only; its value was neither printed nor saved.

Required before pilot: an eligible development example; reviewed protocol; account-specific generation access and quota evidence; reviewed pricing and input bounds; explicit exact request/HTTP-attempt/spend approval; persisted reservations; pinned environment. Current gate remains closed in code and protocol.

Worst-case proposed per-problem bound: 7 logical completions, 3 wrapper attempts each, up to 3 SDK HTTP transmissions per wrapper, hence 63 potentially billable transmissions. Reservations retain ambiguous/unused SDK attempts conservatively. This is a bound, not observed usage, a free-tier guarantee or an approved budget. An ambiguous provider retry can cause an additional generation server-side; exact SDK transmissions are unavailable. Do not treat retries as independent samples.

Offline mocked lifecycle tests cover paired identity, B diagnostic exclusion, C latest-diagnostic binding, stopping, budget limits, pre-transmission persistence and interrupted-run preservation. They do not constitute a genuine pilot or certify recovery/resumption of live paid requests. Historical pilot files remain excluded as paired evidence. The two new authored reference proofs are dataset preparation only.

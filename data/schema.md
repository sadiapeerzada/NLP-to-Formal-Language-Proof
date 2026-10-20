# Dataset schema

## `seed_problems.json` (input)

```json
{
  "id": "arith_001",
  "nl_statement": "For any natural numbers a and b, (a + b) squared equals a squared plus 2ab plus b squared.",
  "category": "arithmetic_identity",
  "difficulty": 1,
  "expected_lean_statement": "theorem add_sq_nat (a b : \u2115) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2"
}
```

Fields:
- `id`: stable string id, `<category_prefix>_<3digit>`
- `nl_statement`: the plain-English problem as it would be given to the pipeline
- `category`: one of `arithmetic_identity`, `divisibility`, `modular_arithmetic`, `induction` (add more as the set grows)
- `difficulty`: 1 (trivial, one `ring`/`norm_num` call) to 5 (genuine multi-step induction or case split)
- `expected_lean_statement`: human reference, used ONLY to sanity-check Stage A output during development, never fed to the model

The five fields above are required. `category` is a non-empty string so new
categories can be introduced without changing the validator. `difficulty`
must be an integer from 1 through 5.

## Optional research-dataset provenance

The following top-level fields document source, licensing, split membership,
and the reference statement. They are optional for backward compatibility;
the validator never fills them in or assigns a split:

- `split`: `development` or `test`. Omission means the problem has no recorded
  split; it must not be treated as a test example by inference.
- `source_citation`: a human-readable citation, such as author/title/edition
  or an internal hand-authored source description.
- `source_url`: a URL identifying the source, when applicable. A citation or
  URL is required for a fully documented research record.
- `license`: the applicable license or an explicit, verified rights status.
- `reference_lean_statement_provenance`: who authored or reviewed
  `expected_lean_statement`, and how it was checked. This describes provenance;
  it is not a replacement for the reference statement itself.

A research record is fully documented only when it has a non-empty citation
or a valid absolute HTTP(S) URL, a non-empty license, and non-empty
reference-statement provenance. Partially populated records are classified as
incomplete; records with no supplied provenance fields are classified as
legacy; records with any invalid supplied provenance field are classified as
invalid. Run `python src/dataset_validation.py <dataset.json>` to validate
structural requirements while reporting legacy, incomplete, and invalid
records. Add
`--require-provenance` to fail validation when any required provenance item is
missing; invalid supplied provenance fields are errors in either mode. Error
messages distinguish missing required provenance from invalid supplied values.
A supplied `split` is always checked against the allowed values.
Validation does not establish that a citation, license, or authorship claim is
truthful; those details require human verification.

## `results/<run>.jsonl` (output, one line per problem)

```json
{
  "id": "arith_001",
  "category": "arithmetic_identity",
  "difficulty": 1,
  "model": {"formalize_sketch": "llama-3.3-70b-versatile", "synthesize": "llama-3.1-8b-instant"},
  "prompt_version": "v1",
  "solved": true,
  "repair_attempts": 2,
  "wall_clock_seconds": 14.3,
  "final_lean_statement": "theorem add_sq_nat (a b : \u2115) : ...",
  "final_proof": "theorem add_sq_nat (a b : \u2115) : ... := by ring",
  "lean_file_path": "lean_project/generated/arith_001.lean"
}
```

## `results/attempts/<id>.jsonl` (full attempt history, for failure analysis)

One line per attempt (including the ones that failed), each with:
`attempt_number`, `proof_text`, `success`, `compiler_errors` (list of strings,
empty if success), `timestamp`.

## Schema version 2 (new API runs)

Historical JSONL artifacts remain in their original format. New runs from
`src/pipeline.py` write `schema_version: 2` records and a neighboring
`<results-stem>.run.json` metadata file. The metadata includes the run ID and
UTC start time, Git state, input/prompt SHA-256 hashes, Lean and Mathlib
versions when available, per-stage models, and run configuration.

Each v2 result records `models` for `formalize`, `sketch`, `synthesize`, and
`repair`; `initial_synthesis_success`; `success_within_repair_budget`; and
`total_synthesis_attempts`. The latter success field is intentionally not
labelled `pass@1`: it may include compiler-guided repairs.
For successful records, `lean_file_path` identifies the promoted proof in the
run-specific `lean_project/generated/runs/<run-id>/` directory.

Each v2 attempt record includes `stage`, `repair_number`,
`is_initial_synthesis`, `verification` (success, Lean exit code, elapsed
time, parsed diagnostics, and axiom dependencies), and `run_id`. Final proofs
are subject to the policy in `docs/verification.md`.
An attempt with `failure_stage: "llm_output"` has empty or whitespace-only
model output; its `verification` is `null`, its `compiler_errors` list is
empty, and `output_error` explains that Lean was not invoked.

Schema-v2 outputs are immutable: the selected `--out` path and its neighboring
run manifest must not already exist. A manifest has a `running`, `failed`, or
`completed` status so a partial result file is never presented as a complete
run. New attempt files are isolated in `results/attempts/<run-id>/`.
Promoted proofs are likewise isolated in `lean_project/generated/runs/<run-id>/`;
the pipeline never writes successful experiment proofs over historical files in
`lean_project/generated/`.

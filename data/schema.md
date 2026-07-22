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

## `results/<run>.jsonl` (output, one line per problem)

```json
{
  "id": "arith_001",
  "category": "arithmetic_identity",
  "difficulty": 1,
  "model": "llama-3.3-70b-versatile",
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

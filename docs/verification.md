# Verification policy

New pipeline runs verify final proof candidates with `lake env lean --json`.
A successful process exit code is required. Timeouts, unavailable executables,
dependency/compiler failures, malformed diagnostics, and compiler error
diagnostics all fail verification.

Lean's JSON diagnostics are read from stdout. On a successful exit, empty
stderr and conventionally prefixed `warning:` or `info:` stderr lines are
accepted; errors and any other stderr text are ambiguous and fail verification.

Final proof candidates may not contain `sorry`, `sorryAx`, or `admit`, and may
not introduce `axiom`, `constant`, or `opaque` declarations. This is a
deliberately explicit source policy for generated candidates; it does not ban
legitimate Lean tactics such as `native_decide` or commands such as
`set_option`. The policy is configurable through `VerificationPolicy`.

For a named final theorem, the verifier appends `#print axioms <theorem>` and
accepts only Lean's standard classical axioms (`propext`, `Classical.choice`,
and `Quot.sound`). This is stronger than token scanning, but it is not a
semantic check that the formal theorem faithfully represents the original
natural-language statement. It also cannot eliminate every unsoundness route
available through malicious Lean metaprogramming or trusted imported code.
Stage A is different: it may use `sorry` solely to establish that a generated
statement elaborates, and it does not claim a proof has been verified.

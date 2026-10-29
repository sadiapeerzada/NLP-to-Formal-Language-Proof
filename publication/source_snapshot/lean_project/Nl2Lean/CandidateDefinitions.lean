import Mathlib.Data.Nat.Basic

/-- Candidate-pool definition, pending independent semantic review.
`geomSum n` sums powers `2^0` through `2^(n-1)`. This explicit module
repairs the previously missing context without approving any dataset record. -/
def geomSum : Nat → Nat
  | 0 => 0
  | n + 1 => geomSum n + 2 ^ n

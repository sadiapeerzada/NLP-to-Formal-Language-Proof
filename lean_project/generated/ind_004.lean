def geomSum : Nat → Nat
  | 0 => 0
  | n + 1 => geomSum n + 2 ^ n

theorem geom_sum_eq (n : Nat) : geomSum n + 1 = 2 ^ n := by
  induction n with
  | zero => decide
  | succ k ih =>
    have step : geomSum (k + 1) = geomSum k + 2 ^ k := rfl
    rw [step, Nat.pow_succ]
    omega

theorem sq_ge_self (n : Nat) : n ≤ n ^ 2 := by
  rw [Nat.pow_two]
  induction n with
  | zero => decide
  | succ k ih => simp [Nat.succ_mul, Nat.mul_succ]

theorem two_pow_gt_self (n : Nat) : n < 2 ^ n := by
  induction n with
  | zero => decide
  | succ k ih => rw [Nat.pow_succ]; omega

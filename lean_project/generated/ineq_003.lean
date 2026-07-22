theorem succ_le_two_pow (n : Nat) (h : 1 ≤ n) : n + 1 ≤ 2 ^ n := by
  induction n with
  | zero => omega
  | succ k ih =>
    rw [Nat.pow_succ]
    rcases Nat.eq_zero_or_pos k with hk0 | hkpos
    · subst hk0; decide
    · have := ih hkpos
      omega

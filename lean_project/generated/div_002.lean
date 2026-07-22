theorem n_mul_succ_even (n : Nat) : ∃ j, n * (n + 1) = 2 * j := by
  induction n with
  | zero => exact ⟨0, by decide⟩
  | succ k ih =>
    obtain ⟨j, hj⟩ := ih
    exact ⟨j + k + 1, by rw [Nat.succ_mul, Nat.mul_succ]; omega⟩

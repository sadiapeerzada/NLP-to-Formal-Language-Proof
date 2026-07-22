def oddSum : Nat → Nat
  | 0 => 0
  | n + 1 => oddSum n + (2 * n + 1)

theorem sum_odd_sq (n : Nat) : oddSum n = n ^ 2 := by
  induction n with
  | zero => decide
  | succ k ih =>
    have step : oddSum (k + 1) = oddSum k + (2 * k + 1) := rfl
    rw [step, ih]
    rw [Nat.pow_two, Nat.pow_two]
    rw [Nat.mul_add, Nat.add_mul, Nat.add_mul]
    simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
    omega

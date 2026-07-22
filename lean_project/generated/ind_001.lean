def natSum : Nat → Nat
  | 0 => 0
  | n + 1 => natSum n + n

theorem gauss_sum (n : Nat) : 2 * natSum (n + 1) = n * (n + 1) := by
  induction n with
  | zero => decide
  | succ k ih =>
    have step : natSum (k + 1 + 1) = natSum (k + 1) + (k + 1) := rfl
    rw [step, Nat.mul_add, ih]
    simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
    omega

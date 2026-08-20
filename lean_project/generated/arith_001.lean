theorem add_sq_nat (a b : Nat) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  rw [Nat.pow_two, Nat.mul_add, Nat.add_mul, Nat.add_mul]
  rw [← Nat.pow_two, ← Nat.pow_two]
  rw [Nat.mul_comm b a]
  rw [show 2 * a * b = a * b + a * b from by rw [Nat.mul_assoc]; omega]
  omega

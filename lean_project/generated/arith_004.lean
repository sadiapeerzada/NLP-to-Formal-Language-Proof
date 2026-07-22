theorem add_sq_nat' (a b : Nat) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  rw [Nat.pow_two, Nat.mul_add, Nat.add_mul, Nat.add_mul]
  rw [← Nat.pow_two, ← Nat.pow_two]
  rw [Nat.mul_comm b a]
  rw [show 2 * a * b = a * b + a * b from by rw [Nat.mul_assoc]; omega]
  omega

theorem sq_sub_nat (a b : Nat) (h : b ≤ a) : (a - b) ^ 2 + 2 * a * b = a ^ 2 + b ^ 2 := by
  obtain ⟨d, hd⟩ := Nat.le.dest h
  subst hd
  rw [Nat.add_sub_cancel_left]
  rw [add_sq_nat' b d]
  rw [Nat.mul_assoc 2 b d]
  have expand2 : 2 * (b + d) * b = 2 * (b * b) + 2 * (d * b) := by
    rw [Nat.mul_assoc, Nat.add_mul, Nat.mul_add]
  rw [expand2, Nat.mul_comm d b]
  simp only [Nat.pow_two]
  omega

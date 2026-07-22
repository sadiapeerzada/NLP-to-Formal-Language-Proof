theorem sq_sub_sq_nat (a b : Nat) (h : b ≤ a) : a ^ 2 - b ^ 2 = (a + b) * (a - b) := by
  obtain ⟨d, hd⟩ := Nat.le.dest h
  subst hd
  simp only [Nat.pow_two, Nat.add_sub_cancel_left]
  rw [Nat.mul_add, Nat.add_mul, Nat.add_mul]
  simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
  omega

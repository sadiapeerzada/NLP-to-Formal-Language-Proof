theorem odd_sq_of_odd (n : Nat) (h : ∃ k, n = 2 * k + 1) : ∃ j, n ^ 2 = 2 * j + 1 := by
  obtain ⟨k, hk⟩ := h
  refine ⟨2 * k ^ 2 + 2 * k, ?_⟩
  rw [hk, Nat.pow_two]
  simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm, Nat.pow_two]
  omega

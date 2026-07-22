theorem even_sq_of_even (n : Nat) (h : ∃ k, n = 2 * k) : ∃ j, n ^ 2 = 2 * j := by
  obtain ⟨k, hk⟩ := h
  refine ⟨2 * k ^ 2, ?_⟩
  rw [hk, Nat.pow_two]
  simp [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm, Nat.pow_two]

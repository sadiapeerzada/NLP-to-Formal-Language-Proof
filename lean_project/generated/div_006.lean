theorem sq_even_iff_even (n : Nat) : (∃ j, n ^ 2 = 2 * j) ↔ (∃ k, n = 2 * k) := by
  rw [Nat.pow_two]
  constructor
  · intro ⟨j, hj⟩
    have hmod : n % 2 = 0 ∨ n % 2 = 1 := by omega
    rcases hmod with h0 | h1
    · exact ⟨n / 2, by omega⟩
    · exfalso
      obtain ⟨k, hk⟩ : ∃ k, n = 2 * k + 1 := ⟨n / 2, by omega⟩
      have hsq : n * n = 2 * (2 * (k * k) + 2 * k) + 1 := by
        rw [hk]
        simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
        omega
      omega
  · intro ⟨k, hk⟩
    refine ⟨2 * (k * k), ?_⟩
    rw [hk]
    simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]

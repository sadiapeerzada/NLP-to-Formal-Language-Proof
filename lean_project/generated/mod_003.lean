theorem sq_mod_three (n : Nat) : n ^ 2 % 3 = 0 ∨ n ^ 2 % 3 = 1 := by
  rw [Nat.pow_two]
  have hmod3 : n % 3 = 0 ∨ n % 3 = 1 ∨ n % 3 = 2 := by omega
  rcases hmod3 with h0 | h1 | h2
  · left
    obtain ⟨k, hk⟩ : ∃ k, n = 3 * k := ⟨n / 3, by omega⟩
    have expand : n * n = 3 * (3 * k * k) := by
      rw [hk]; simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
    omega
  · right
    obtain ⟨k, hk⟩ : ∃ k, n = 3 * k + 1 := ⟨n / 3, by omega⟩
    have expand : n * n = 3 * (3 * k * k + 2 * k) + 1 := by
      rw [hk]; simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]; omega
    omega
  · right
    obtain ⟨k, hk⟩ : ∃ k, n = 3 * k + 2 := ⟨n / 3, by omega⟩
    have expand : n * n = 3 * (3 * k * k + 4 * k + 1) + 1 := by
      rw [hk]; simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]; omega
    omega

theorem int_sq (a : Int) : a ^ 2 = a * a := by
  have h1 : a ^ 2 = a ^ 1 * a := rfl
  have h2 : a ^ 1 = a ^ 0 * a := rfl
  have h3 : a ^ 0 = (1:Int) := rfl
  rw [h1, h2, h3, Int.one_mul]

theorem sq_mod_four (a : Int) : a ^ 2 % 4 = 0 ∨ a ^ 2 % 4 = 1 := by
  rw [int_sq]
  have hmod2 : a % 2 = 0 ∨ a % 2 = 1 := by omega
  rcases hmod2 with h0 | h1
  · left
    obtain ⟨k, hk⟩ : ∃ k, a = 2 * k := ⟨a / 2, by omega⟩
    have expand : a * a = 4 * (k * k) := by
      rw [hk]
      simp [Int.mul_add, Int.add_mul, Int.mul_comm, Int.mul_assoc, Int.mul_left_comm]
    rw [expand]
    omega
  · right
    obtain ⟨k, hk⟩ : ∃ k, a = 2 * k + 1 := ⟨a / 2, by omega⟩
    have expand : a * a = 4 * (k * k + k) + 1 := by
      rw [hk]
      simp [Int.mul_add, Int.add_mul, Int.mul_comm, Int.mul_assoc, Int.mul_left_comm]
      omega
    rw [expand]
    omega

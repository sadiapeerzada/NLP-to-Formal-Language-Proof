theorem prod_succ_ge (a b : Nat) : a * b + 1 ≤ (a + 1) * (b + 1) := by
  have expand : (a + 1) * (b + 1) = a * b + a + b + 1 := by
    rw [Nat.add_mul, Nat.mul_add, Nat.mul_add]
    omega
  omega

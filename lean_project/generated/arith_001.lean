import Mathlib

theorem add_sq_nat (a b : ℕ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  -- Start with the left-hand side of the equation
  simp only [pow_two, Nat.add_mul]
  -- Expand the square using the binomial identity
  ring
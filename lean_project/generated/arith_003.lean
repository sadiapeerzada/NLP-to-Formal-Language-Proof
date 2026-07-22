import Mathlib

-- The distributive property of multiplication over addition for natural numbers
theorem distributive_nat (a b c : ℕ) : a * (b + c) = a * b + a * c := by
  rw [mul_add]
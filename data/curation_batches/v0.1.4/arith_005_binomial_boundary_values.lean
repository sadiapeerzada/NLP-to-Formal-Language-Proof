import Mathlib

theorem choose_zero_and_self (n : ℕ) : Nat.choose n 0 = 1 ∧ Nat.choose n n = 1 := by
  simp

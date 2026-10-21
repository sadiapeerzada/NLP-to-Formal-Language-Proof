import Mathlib

theorem pascal_row_sum (n : ℕ) : ∑ k ∈ Finset.range (n + 1), Nat.choose n k = 2 ^ n := by
  simpa using Nat.sum_range_choose n

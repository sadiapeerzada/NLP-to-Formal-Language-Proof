import Mathlib

theorem even_iff_even_three_mul (n : ℤ) : Even n ↔ Even (3 * n) := by
  constructor
  · intro h
    rcases h with ⟨k, hk⟩
    refine ⟨3 * k, ?_⟩
    nlinarith
  · intro h
    rcases h with ⟨k, hk⟩
    have hn : n % 2 = 0 := by omega
    refine ⟨n / 2, ?_⟩
    omega

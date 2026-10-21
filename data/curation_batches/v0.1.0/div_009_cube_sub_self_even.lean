import Mathlib

theorem even_cube_sub_self (n : ℤ) : Even (n ^ 3 - n) := by
  rcases Int.even_or_odd n with ⟨k, hk⟩ | ⟨k, hk⟩
  · refine ⟨4 * k ^ 3 - k, ?_⟩
    rw [hk]
    ring
  · refine ⟨4 * k ^ 3 + 6 * k ^ 2 + 2 * k, ?_⟩
    rw [hk]
    ring

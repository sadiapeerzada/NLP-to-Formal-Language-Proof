import Mathlib

theorem dvd_mul_right_int (a b c : ℤ) (hab : a ∣ b) : a ∣ b * c := by
  obtain ⟨k, hk⟩ := hab
  refine ⟨k * c, ?_⟩
  rw [hk]
  ring

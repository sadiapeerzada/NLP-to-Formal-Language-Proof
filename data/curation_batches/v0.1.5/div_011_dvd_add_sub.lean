import Mathlib

theorem dvd_add_sub_int (a b c : ℤ) (hab : a ∣ b) (hac : a ∣ c) :
    a ∣ b + c ∧ a ∣ b - c := by
  obtain ⟨x, hx⟩ := hab
  obtain ⟨y, hy⟩ := hac
  constructor
  · refine ⟨x + y, ?_⟩
    rw [hx, hy]
    ring
  · refine ⟨x - y, ?_⟩
    rw [hx, hy]
    ring

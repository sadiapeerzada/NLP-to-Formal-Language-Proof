import Mathlib.Data.Nat.ModEq

theorem largest_modulus_sixteen_twentyfive :
    Nat.ModEq 9 16 25 ∧ ∀ n : ℕ, 0 < n → Nat.ModEq n 16 25 → n ≤ 9 := by
  constructor
  · decide
  · intro n hn h
    have hd : n ∣ 9 := by
      simpa using (Nat.modEq_iff_dvd' (by decide : 16 ≤ 25)).mp h
    exact Nat.le_of_dvd (by decide) hd

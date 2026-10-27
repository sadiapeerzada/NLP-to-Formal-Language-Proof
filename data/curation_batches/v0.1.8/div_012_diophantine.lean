import Mathlib.Data.Int.Basic
import Lean.Elab.Tactic.Omega

theorem diophantine_six_ten (x y : ℤ) :
    6 * x + 10 * y = 32 ↔ ∃ k : ℤ, x = 2 - 5 * k ∧ y = 2 + 3 * k := by
  constructor
  · intro h
    refine ⟨(y - 2) / 3, ?_, ?_⟩ <;> omega
  · rintro ⟨k, rfl, rfl⟩
    omega

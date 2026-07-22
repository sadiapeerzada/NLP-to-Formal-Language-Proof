import Mathlib

theorem sq_mod_four (a : Int) : a ^ 2 % 4 = 0 ∨ a ^ 2 % 4 = 1 := by
  have h : a % 2 = 0 ∨ a % 2 = 1 := by omega
  rcases h with h0 | h1
  · left
    obtain ⟨k, hk⟩ : ∃ k, a = 2 * k := ⟨a / 2, by omega⟩
    subst hk
    ring_nf
    omega
  · right
    obtain ⟨k, hk⟩ : ∃ k, a = 2 * k + 1 := ⟨a / 2, by omega⟩
    subst hk
    ring_nf
    omega

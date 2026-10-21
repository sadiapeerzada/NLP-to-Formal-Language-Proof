import Mathlib

theorem postage_representable_large (n : ℕ) (hn : 28 ≤ n) :
    ∃ five eight : ℕ, 5 * five + 8 * eight = n := by
  have step : ∀ k : ℕ, 28 ≤ k →
      (∃ five eight : ℕ, 5 * five + 8 * eight = k) →
      ∃ five eight : ℕ, 5 * five + 8 * eight = k + 1 := by
    intro k hk hrepr
    obtain ⟨five, eight, hsum⟩ := hrepr
    by_cases hfive : 3 ≤ five
    · refine ⟨five - 3, eight + 2, ?_⟩
      omega
    · have height : 3 ≤ eight := by omega
      refine ⟨five + 5, eight - 3, ?_⟩
      omega
  induction n, hn using Nat.le_induction with
  | base => exact ⟨4, 1, by norm_num⟩
  | succ k hk ih => exact step k hk ih

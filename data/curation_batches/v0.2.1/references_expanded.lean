import Mathlib
open scoped BigOperators

theorem study_q_rational_density (x y : ℝ) (h : x < y) : ∃ q : ℚ, x < q ∧ (q : ℝ) < y := by
  exact exists_rat_btwn h
#print axioms study_q_rational_density

theorem study_i_stirling (n k : ℕ) : Nat.stirlingSecond (n + 1) (k + 1) = (k + 1) * Nat.stirlingSecond n (k + 1) + Nat.stirlingSecond n k := by
  exact Nat.stirlingSecond_succ_succ n k
#print axioms study_i_stirling

theorem study_i_catalan (n : ℕ) : catalan (n + 1) = ∑ i : Fin n.succ, catalan i * catalan (n - i) := by
  exact catalan_succ n
#print axioms study_i_catalan

theorem study_q_rearrangement (a b c d : ℝ) (hab : a ≤ b) (hcd : c ≤ d) : a * d + b * c ≤ a * c + b * d := by
  nlinarith [mul_nonneg (sub_nonneg.mpr hab) (sub_nonneg.mpr hcd)]
#print axioms study_q_rearrangement

theorem study_q_pigeonhole (s t : Finset ℕ) (f : ℕ → ℕ) (h : t.card < s.card) (hm : ∀ x ∈ s, f x ∈ t) : ∃ x ∈ s, ∃ y ∈ s, x ≠ y ∧ f x = f y := by
  exact Finset.exists_ne_map_eq_of_card_lt_of_maps_to h hm
#print axioms study_q_pigeonhole

theorem study_d_prime_factor_exists (n : ℕ) (hn : 2 ≤ n) : ∃ p : ℕ, p.Prime ∧ p ∣ n := by
  exact Nat.exists_prime_and_dvd (by omega)
#print axioms study_d_prime_factor_exists

theorem study_d_euclidean_gcd (m n : ℕ) : Nat.gcd m n = Nat.gcd (n % m) m := by
  exact Nat.gcd_rec m n
#print axioms study_d_euclidean_gcd

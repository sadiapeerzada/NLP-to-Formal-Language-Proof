import Mathlib
open scoped BigOperators

namespace AISemanticBridges

-- Equivalence of the current geometric-sum encoding with English subtraction.
theorem geom_encoding (n s : ℕ) : (s + 1 = 2 ^ n) ↔ (s = 2 ^ n - 1) := by
  have h : 0 < 2 ^ n := by positivity
  omega

-- Positive modulus is a genuine missing specification restriction in mod_001.
theorem extra_modulus_zero_instance : Int.ModEq (0 : ℤ) 0 0 := by rfl
theorem zero_is_not_positive : ¬ (0 < (0 : ℤ)) := by decide

theorem range_endpoint_counterexample :
    (∑ k ∈ Finset.range 1, k) ≠ 1 * (1 + 1) / 2 := by decide

theorem odd_sum_empty : (∑ k ∈ Finset.range 0, (2 * k + 1)) = 0 := by decide

theorem singleton_power_witness (k : ℕ) :
    (2 ^ k : ℕ) = ∑ i ∈ ({k} : Finset ℕ), 2 ^ i := by simp

theorem positive_sum_nonempty (n : ℕ) (hn : 0 < n) (s : Finset ℕ)
    (hs : n = ∑ k ∈ s, 2 ^ k) : s.Nonempty := by
  by_contra h
  have he : s = ∅ := Finset.not_nonempty_iff_eq_empty.mp h
  simp only [he, Finset.sum_empty] at hs
  omega

-- n=0 is a concrete counterexample if the premise in natural subtraction is dropped.
theorem missing_subtraction_premise : ¬ ((0 : ℕ) - 1 + 1 = 0) := by decide

theorem negative_log_totalization : Real.log (-1) = 0 := by simp

-- Fresh reference checks for all synthetic calibration controls. These verify
-- the formal side, not the deliberately false English on mismatch controls.
theorem syn_01 (n : ℕ) : n + 0 = n := by omega
theorem syn_02 (n : ℕ) : n + 1 = n + 1 := rfl
theorem syn_03 (n : ℕ) : 0 ≤ n := by omega
theorem syn_04 (n : ℕ) (h : 1 ≤ n) : n - 1 + 1 = n := by omega
theorem syn_05 (n : ℕ) (h : 1 ≤ n) : n - 1 + 1 = n := by omega
theorem syn_06 (x : ℤ) : ∃ y : ℤ, x < y := ⟨x + 1, by omega⟩
theorem syn_07 : ∀ n : ℕ, ∃ m : ℕ, n < m := by
  intro n
  exact ⟨n + 1, by omega⟩
theorem syn_08 (x : ℤ) : 0 ≤ x ^ 2 := sq_nonneg x
theorem syn_09 (a b : ℕ) (h : a ∣ b) (g : b ∣ a) : a = b := Nat.dvd_antisymm h g
theorem syn_10 (n : ℕ) : 2 * (∑ i ∈ Finset.range (n + 1), i) = n * (n + 1) := by
  simpa [Nat.mul_comm] using Finset.sum_range_id_mul_two (n + 1)
theorem syn_11 (n : ℕ) : 4 ∣ n → 2 ∣ n := fun h => dvd_trans (by decide) h
theorem syn_12 (m : ℤ) : Int.ModEq m 0 0 := by rfl

#print axioms geom_encoding
#print axioms extra_modulus_zero_instance
#print axioms zero_is_not_positive
#print axioms range_endpoint_counterexample
#print axioms odd_sum_empty
#print axioms singleton_power_witness
#print axioms positive_sum_nonempty
#print axioms missing_subtraction_premise
#print axioms negative_log_totalization
#print axioms syn_01
#print axioms syn_02
#print axioms syn_03
#print axioms syn_04
#print axioms syn_05
#print axioms syn_06
#print axioms syn_07
#print axioms syn_08
#print axioms syn_09
#print axioms syn_10
#print axioms syn_11
#print axioms syn_12

end AISemanticBridges

import Mathlib
open scoped BigOperators

def geomSum : ℕ → ℕ
  | 0 => 0
  | n + 1 => geomSum n + 2 ^ n

theorem geom_sum_eq (n : ℕ) : geomSum n + 1 = 2 ^ n := by
  induction n with
  | zero => decide
  | succ n ih =>
    simp only [geomSum, pow_succ]
    omega
#print axioms geom_sum_eq

theorem pow_seven_sub_one_dvd_six (n : ℕ) : 6 ∣ 7 ^ n - 1 := by
  induction n with
  | zero => simp
  | succ n ih =>
    have hp : 1 ≤ 7 ^ n := by positivity
    have heq : 7 ^ (n + 1) - 1 = 7 * (7 ^ n - 1) + 6 := by
      rw [pow_succ]
      omega
    rw [heq]
    exact dvd_add (dvd_mul_of_dvd_right ih 7) (dvd_refl 6)
#print axioms pow_seven_sub_one_dvd_six

theorem sum_squares_closed_form (n : ℕ) : (∑ k ∈ Finset.range (n + 1), k ^ 2) = n * (n + 1) * (2 * n + 1) / 6 := by
  have scaled : ∀ n : ℕ, 6 * (∑ k ∈ Finset.range (n + 1), k ^ 2) = n * (n + 1) * (2 * n + 1) := by
    intro m
    induction m with
    | zero => simp
    | succ m ih =>
      rw [Finset.sum_range_succ]
      nlinarith
  have h := scaled n
  omega
#print axioms sum_squares_closed_form

theorem positive_nat_sum_distinct_powers_two (n : ℕ) (hn : 1 ≤ n) : ∃ s : Finset ℕ, n = ∑ k ∈ s, 2 ^ k := by
  have all : ∀ m : ℕ, ∃ s : Finset ℕ, m = ∑ k ∈ s, 2 ^ k := by
    intro m
    induction m using Nat.strong_induction_on with
    | h m ih =>
      by_cases hm : m = 0
      · subst m
        exact ⟨∅, by simp⟩
      have half : m / 2 < m := Nat.div_lt_self (by omega) (by decide)
      obtain ⟨s, hs⟩ := ih (m / 2) half
      let t := s.image Nat.succ
      have hzero : 0 ∉ t := by simp [t]
      have hsum : (∑ k ∈ t, 2 ^ k) = 2 * (∑ k ∈ s, 2 ^ k) := by
        dsimp only [t]
        rw [Finset.sum_image]
        · simp_rw [Nat.pow_succ, mul_comm _ 2]
          exact (Finset.mul_sum s (fun k => 2 ^ k) 2).symm
        · exact Nat.succ_injective.injOn
      by_cases he : m % 2 = 0
      · refine ⟨t, ?_⟩
        rw [hsum, ← hs]
        omega
      · refine ⟨insert 0 t, ?_⟩
        rw [Finset.sum_insert hzero, pow_zero, hsum, ← hs]
        omega
  exact all n
#print axioms positive_nat_sum_distinct_powers_two

theorem hockey_stick_binomial_identity (n : ℕ) : (∑ k ∈ Finset.range (n + 1), Nat.choose (4 + k) k) = Nat.choose (5 + n) n := by
  calc
    (∑ k ∈ Finset.range (n + 1), Nat.choose (4 + k) k) =
        (∑ k ∈ Finset.range (n + 1), Nat.choose (k + 4) 4) := by
      apply Finset.sum_congr rfl
      intro k hk
      simpa [Nat.add_comm] using (Nat.choose_symm (n := k + 4) (k := 4) (by omega))
    _ = Nat.choose (n + 4 + 1) 5 := Nat.sum_range_add_choose n 4
    _ = Nat.choose (5 + n) n := by
      simpa [Nat.add_comm, Nat.add_assoc] using (Nat.choose_symm (n := 5 + n) (k := 5) (by omega)).symm
#print axioms hockey_stick_binomial_identity

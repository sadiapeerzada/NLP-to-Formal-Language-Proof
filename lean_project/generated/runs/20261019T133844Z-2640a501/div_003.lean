import Mathlib

theorem dvd_two_and_three_of_dvd_six (n : ℕ) (h : (6 : ℕ) ∣ n) :
    (2 : ℕ) ∣ n ∧ (3 : ℕ) ∣ n := by
  rcases h with ⟨k, hk⟩
  refine ⟨?h2, ?h3⟩
  · refine ⟨3 * k, ?_⟩
    calc
      n = 6 * k := hk
      _ = (2 * 3) * k := by norm_num
      _ = 2 * (3 * k) := by
        simp [mul_comm, mul_left_comm, mul_assoc]
  · refine ⟨2 * k, ?_⟩
    calc
      n = 6 * k := hk
      _ = (3 * 2) * k := by norm_num
      _ = 3 * (2 * k) := by
        simp [mul_comm, mul_left_comm, mul_assoc]

#print axioms dvd_two_and_three_of_dvd_six

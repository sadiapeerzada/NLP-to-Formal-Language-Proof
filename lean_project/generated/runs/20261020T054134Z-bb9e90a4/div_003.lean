import Mathlib

theorem dvd_two_and_three_of_dvd_six (n : ℕ) (h : 6 ∣ n) : 2 ∣ n ∧ 3 ∣ n := by
  rcases h with ⟨k, hk⟩
  refine ⟨?h2, ?h3⟩
  · refine ⟨3 * k, ?_⟩
    simpa [hk, mul_comm, mul_left_comm, mul_assoc]
  · refine ⟨2 * k, ?_⟩
    simpa [hk, mul_comm, mul_left_comm, mul_assoc]

#print axioms dvd_two_and_three_of_dvd_six

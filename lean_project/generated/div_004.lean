theorem sum_two_odd_even (a b : Nat) (ha : ∃ i, a = 2 * i + 1) (hb : ∃ j, b = 2 * j + 1) :
    ∃ k, a + b = 2 * k := by
  obtain ⟨i, hi⟩ := ha
  obtain ⟨j, hj⟩ := hb
  exact ⟨i + j + 1, by omega⟩

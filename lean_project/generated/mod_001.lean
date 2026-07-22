theorem cong_add_one (a b m : Int) (h : m ∣ (a - b)) : m ∣ ((a + 1) - (b + 1)) := by
  have heq : (a + 1) - (b + 1) = a - b := by omega
  rw [heq]; exact h

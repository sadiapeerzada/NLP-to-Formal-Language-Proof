import Mathlib

-- Proposal only: explicit missing English restriction for mod_001.
-- Historical candidate and proof remain unchanged; no approval is implied.
theorem proposed_cong_add_one_positive (a b m : ℤ) (_hm : 0 < m)
    (h : a ≡ b [ZMOD m]) : a + 1 ≡ b + 1 [ZMOD m] := by
  exact h.add (Int.ModEq.refl 1)
#print axioms proposed_cong_add_one_positive

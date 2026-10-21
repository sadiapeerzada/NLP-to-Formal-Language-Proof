import Mathlib

theorem modEq_add_two (a b c d n : ℤ) (_hn : 0 < n)
    (hab : a ≡ b [ZMOD n]) (hcd : c ≡ d [ZMOD n]) :
    a + c ≡ b + d [ZMOD n] := by
  exact hab.add hcd

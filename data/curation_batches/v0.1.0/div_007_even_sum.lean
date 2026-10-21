import Mathlib

theorem even_add_of_even (a b : ℤ) (ha : Even a) (hb : Even b) : Even (a + b) := by
  rcases ha with ⟨x, hx⟩
  rcases hb with ⟨y, hy⟩
  refine ⟨x + y, ?_⟩
  nlinarith

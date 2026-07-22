import Mathlib

-- The original attempt was close, but the error messages indicate a type mismatch issue.
-- The `match` tactic was used correctly, but the `have` statements were not properly utilized to prove the goal.
theorem nat_le_sq (n : ℕ) : n ≤ n ^ 2 :=
  match n with
  | 0 => le_refl 0
  | n + 1 =>
    have h1 : (n + 1) ^ 2 = (n + 1) * (n + 1) := by simp [pow_two];
    have h2 : n + 1 ≤ (n + 1) * (n + 1) := by nlinarith;
    have h3 : n + 1 ≤ (n + 1) ^ 2 := by rw [h1]; exact h2;
    h3
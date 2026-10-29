import Mathlib

-- Sanity check: if this file compiles after `lake exe cache get`, the
-- environment is set up correctly. Do not proceed to the pipeline until
-- this compiles with zero errors.
example : (1 : Nat) + 1 = 2 := by norm_num

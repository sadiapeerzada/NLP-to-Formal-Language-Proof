theorem mul_distrib_left (a b c : Nat) : a * (b + c) = a * b + a * c := by
  exact Nat.mul_add a b c

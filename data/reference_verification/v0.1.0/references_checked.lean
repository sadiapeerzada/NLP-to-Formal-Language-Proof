import Mathlib

theorem add_sq_nat (a b : ℕ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring

#print axioms add_sq_nat

theorem sq_sub_sq_nat (a b : ℕ) (h : b ≤ a) : a ^ 2 - b ^ 2 = (a + b) * (a - b) := by
  have hab : b ^ 2 ≤ a ^ 2 := Nat.pow_le_pow_left h 2
  have h1 := Nat.sub_add_cancel h
  have h2 := Nat.sub_add_cancel hab
  nlinarith

#print axioms sq_sub_sq_nat

theorem even_sq_of_even (n : ℕ) (h : Even n) : Even (n ^ 2) := by
  rcases h with ⟨k, hk⟩
  exact ⟨k * n, by nlinarith⟩

#print axioms even_sq_of_even

theorem n_mul_succ_even (n : ℕ) : Even (n * (n + 1)) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rcases ih with ⟨k, hk⟩
    exact ⟨k + n + 1, by nlinarith⟩

#print axioms n_mul_succ_even

theorem div6_imp_div2_div3 (n : ℕ) (h : 6 ∣ n) : 2 ∣ n ∧ 3 ∣ n := by
  exact ⟨dvd_trans (by decide : 2 ∣ 6) h, dvd_trans (by decide : 3 ∣ 6) h⟩

#print axioms div6_imp_div2_div3

theorem cong_add_one (a b m : ℤ) (h : a ≡ b [ZMOD m]) : a + 1 ≡ b + 1 [ZMOD m] := by
  exact h.add (Int.ModEq.refl 1)

#print axioms cong_add_one

theorem int_sq (a : Int) : a ^ 2 = a * a := by
  rw [Int.pow_succ, Int.pow_succ, Int.pow_zero, Int.one_mul]

theorem sq_mod_four (a : Int) : a ^ 2 % 4 = 0 ∨ a ^ 2 % 4 = 1 := by
  rw [int_sq]
  have hmod2 : a % 2 = 0 ∨ a % 2 = 1 := by omega
  rcases hmod2 with h0 | h1
  · left
    obtain ⟨k, hk⟩ : ∃ k, a = 2 * k := ⟨a / 2, by omega⟩
    have expand : a * a = 4 * (k * k) := by
      rw [hk]
      simp [Int.mul_add, Int.add_mul, Int.mul_comm, Int.mul_assoc, Int.mul_left_comm]
    rw [expand]
    omega
  · right
    obtain ⟨k, hk⟩ : ∃ k, a = 2 * k + 1 := ⟨a / 2, by omega⟩
    have expand : a * a = 4 * (k * k + k) + 1 := by
      rw [hk]
      simp [Int.mul_add, Int.add_mul, Int.mul_comm, Int.mul_assoc, Int.mul_left_comm]
      omega
    rw [expand]
    omega

#print axioms sq_mod_four

theorem gauss_sum (n : ℕ) : 2 * (Finset.range (n + 1)).sum id = n * (n + 1) := by
  simpa [Nat.mul_comm] using Finset.sum_range_id_mul_two (n + 1)

#print axioms gauss_sum

theorem sum_odd_sq (n : ℕ) : (Finset.range n).sum (fun i => 2 * i + 1) = n ^ 2 := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ, ih]
    ring

#print axioms sum_odd_sq

theorem two_pow_gt_self (n : Nat) : n < 2 ^ n := by
  induction n with
  | zero => decide
  | succ k ih => rw [Nat.pow_succ]; omega

#print axioms two_pow_gt_self

theorem sum_two_odd_even (a b : Nat) (ha : ∃ i, a = 2 * i + 1) (hb : ∃ j, b = 2 * j + 1) :
    ∃ k, a + b = 2 * k := by
  obtain ⟨i, hi⟩ := ha
  obtain ⟨j, hj⟩ := hb
  exact ⟨i + j + 1, by omega⟩

#print axioms sum_two_odd_even

theorem sq_ge_self (n : ℕ) : n ≤ n ^ 2 := by
  nlinarith [sq_nonneg (n : ℤ)]

#print axioms sq_ge_self

theorem mul_distrib_left (a b c : ℕ) : a * (b + c) = a * b + a * c := by
  exact Nat.mul_add a b c

#print axioms mul_distrib_left

theorem distributive_nat (a b c : ℕ) : a * (b + c) = a * b + a * c := by
  exact Nat.mul_add a b c

#print axioms distributive_nat

theorem sq_sub_nat (a b : ℕ) (h : b ≤ a) : (a - b) ^ 2 + 2 * a * b = a ^ 2 + b ^ 2 := by
  have h1 := Nat.sub_add_cancel h
  nlinarith

#print axioms sq_sub_nat

theorem odd_sq_of_odd (n : Nat) (h : ∃ k, n = 2 * k + 1) : ∃ j, n ^ 2 = 2 * j + 1 := by
  obtain ⟨k, hk⟩ := h
  refine ⟨2 * k ^ 2 + 2 * k, ?_⟩
  rw [hk, Nat.pow_two]
  simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm, Nat.pow_two]
  omega

#print axioms odd_sq_of_odd

theorem sq_even_iff_even (n : Nat) : (∃ j, n ^ 2 = 2 * j) ↔ (∃ k, n = 2 * k) := by
  rw [Nat.pow_two]
  constructor
  · intro ⟨j, hj⟩
    have hmod : n % 2 = 0 ∨ n % 2 = 1 := by omega
    rcases hmod with h0 | h1
    · exact ⟨n / 2, by omega⟩
    · exfalso
      obtain ⟨k, hk⟩ : ∃ k, n = 2 * k + 1 := ⟨n / 2, by omega⟩
      have hsq : n * n = 2 * (2 * (k * k) + 2 * k) + 1 := by
        rw [hk]
        simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
        omega
      omega
  · intro ⟨k, hk⟩
    refine ⟨2 * (k * k), ?_⟩
    rw [hk]
    simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]

#print axioms sq_even_iff_even

theorem prod_succ_ge (a b : ℕ) : a * b + 1 ≤ (a + 1) * (b + 1) := by
  nlinarith

#print axioms prod_succ_ge

theorem succ_le_two_pow (n : Nat) (h : 1 ≤ n) : n + 1 ≤ 2 ^ n := by
  induction n with
  | zero => omega
  | succ k ih =>
    rw [Nat.pow_succ]
    rcases Nat.eq_zero_or_pos k with hk0 | hkpos
    · subst hk0; decide
    · have := ih hkpos
      omega

#print axioms succ_le_two_pow

theorem sq_mod_three (n : Nat) : n ^ 2 % 3 = 0 ∨ n ^ 2 % 3 = 1 := by
  rw [Nat.pow_two]
  have hmod3 : n % 3 = 0 ∨ n % 3 = 1 ∨ n % 3 = 2 := by omega
  rcases hmod3 with h0 | h1 | h2
  · left
    obtain ⟨k, hk⟩ : ∃ k, n = 3 * k := ⟨n / 3, by omega⟩
    have expand : n * n = 3 * (3 * k * k) := by
      rw [hk]; simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]
    omega
  · right
    obtain ⟨k, hk⟩ : ∃ k, n = 3 * k + 1 := ⟨n / 3, by omega⟩
    have expand : n * n = 3 * (3 * k * k + 2 * k) + 1 := by
      rw [hk]; simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]; omega
    omega
  · right
    obtain ⟨k, hk⟩ : ∃ k, n = 3 * k + 2 := ⟨n / 3, by omega⟩
    have expand : n * n = 3 * (3 * k * k + 4 * k + 1) + 1 := by
      rw [hk]; simp [Nat.mul_add, Nat.add_mul, Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]; omega
    omega

#print axioms sq_mod_three


namespace ReferenceExpected
theorem add_sq_nat (a b : ℕ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by sorry
theorem sq_sub_sq_nat (a b : ℕ) (h : b ≤ a) : a ^ 2 - b ^ 2 = (a + b) * (a - b) := by sorry
theorem even_sq_of_even (n : ℕ) (h : Even n) : Even (n ^ 2) := by sorry
theorem n_mul_succ_even (n : ℕ) : Even (n * (n + 1)) := by sorry
theorem div6_imp_div2_div3 (n : ℕ) (h : 6 ∣ n) : 2 ∣ n ∧ 3 ∣ n := by sorry
theorem cong_add_one (a b m : ℤ) (h : a ≡ b [ZMOD m]) : a + 1 ≡ b + 1 [ZMOD m] := by sorry
theorem sq_mod_four (a : ℤ) : a ^ 2 % 4 = 0 ∨ a ^ 2 % 4 = 1 := by sorry
theorem gauss_sum (n : ℕ) : 2 * (Finset.range (n + 1)).sum id = n * (n + 1) := by sorry
theorem sum_odd_sq (n : ℕ) : (Finset.range n).sum (fun i => 2 * i + 1) = n ^ 2 := by sorry
theorem two_pow_gt_self (n : ℕ) : n < 2 ^ n := by sorry
theorem sum_two_odd_even (a b : ℕ) (ha : ∃ i, a = 2*i+1) (hb : ∃ j, b = 2*j+1) : ∃ k, a + b = 2 * k := by sorry
theorem sq_ge_self (n : ℕ) : n ≤ n ^ 2 := by sorry
theorem mul_distrib_left (a b c : ℕ) : a * (b + c) = a * b + a * c := by sorry
theorem distributive_nat (a b c : ℕ) : a * (b + c) = a * b + a * c := by sorry
theorem sq_sub_nat (a b : ℕ) (h : b ≤ a) : (a - b) ^ 2 + 2 * a * b = a ^ 2 + b ^ 2 := by sorry
theorem odd_sq_of_odd (n : ℕ) (h : ∃ k, n = 2*k+1) : ∃ j, n ^ 2 = 2*j+1 := by sorry
theorem sq_even_iff_even (n : ℕ) : (∃ j, n ^ 2 = 2 * j) ↔ (∃ k, n = 2 * k) := by sorry
theorem prod_succ_ge (a b : ℕ) : a * b + 1 ≤ (a + 1) * (b + 1) := by sorry
theorem succ_le_two_pow (n : ℕ) (h : 1 ≤ n) : n + 1 ≤ 2 ^ n := by sorry
theorem sq_mod_three (n : ℕ) : n ^ 2 % 3 = 0 ∨ n ^ 2 % 3 = 1 := by sorry
end ReferenceExpected
example : ReferenceExpected.add_sq_nat = add_sq_nat := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.sq_sub_sq_nat = sq_sub_sq_nat := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.even_sq_of_even = even_sq_of_even := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.n_mul_succ_even = n_mul_succ_even := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.div6_imp_div2_div3 = div6_imp_div2_div3 := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.cong_add_one = cong_add_one := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.sq_mod_four = sq_mod_four := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.gauss_sum = gauss_sum := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.sum_odd_sq = sum_odd_sq := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.two_pow_gt_self = two_pow_gt_self := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.sum_two_odd_even = sum_two_odd_even := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.sq_ge_self = sq_ge_self := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.mul_distrib_left = mul_distrib_left := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.distributive_nat = distributive_nat := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.sq_sub_nat = sq_sub_nat := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.odd_sq_of_odd = odd_sq_of_odd := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.sq_even_iff_even = sq_even_iff_even := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.prod_succ_ge = prod_succ_ge := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.succ_le_two_pow = succ_le_two_pow := by
  exact Subsingleton.elim _ _
example : ReferenceExpected.sq_mod_three = sq_mod_three := by
  exact Subsingleton.elim _ _

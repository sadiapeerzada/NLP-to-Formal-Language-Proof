import Mathlib
import Nl2Lean.CandidateDefinitions
open scoped BigOperators

namespace AuditReference0

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


end AuditReference0

namespace AuditReference1
open scoped BigOperators
namespace AdditionalReferences

theorem geom_sum_eq (n : ℕ) : geomSum n + 1 = 2 ^ n := by
  induction n with
  | zero => decide
  | succ n ih =>
    simp only [geomSum, pow_succ]
    omega
#print axioms geom_sum_eq

theorem pow_seven_sub_one_dvd_six (n : ℕ) : 6 ∣ 7 ^ n - 1 := by
  induction n with
  | zero => simp
  | succ n ih =>
    have hp : 1 ≤ 7 ^ n := Nat.succ_le_of_lt (by positivity)
    have heq : 7 ^ (n + 1) - 1 = 7 * (7 ^ n - 1) + 6 := by
      rw [pow_succ]
      omega
    rw [heq]
    exact dvd_add (dvd_mul_of_dvd_right ih 7) (dvd_refl 6)
#print axioms pow_seven_sub_one_dvd_six

theorem sum_squares_closed_form (n : ℕ) : (∑ k ∈ Finset.range (n + 1), k ^ 2) = n * (n + 1) * (2 * n + 1) / 6 := by
  have scaled : ∀ n : ℕ, 6 * (∑ k ∈ Finset.range (n + 1), k ^ 2) = n * (n + 1) * (2 * n + 1) := by
    intro m
    induction m with
    | zero => simp
    | succ m ih =>
      rw [Finset.sum_range_succ]
      nlinarith
  have h := scaled n
  omega
#print axioms sum_squares_closed_form

theorem positive_nat_sum_distinct_powers_two (n : ℕ) (hn : 1 ≤ n) : ∃ s : Finset ℕ, n = ∑ k ∈ s, 2 ^ k := by
  have all : ∀ m : ℕ, ∃ s : Finset ℕ, m = ∑ k ∈ s, 2 ^ k := by
    intro m
    induction m using Nat.strong_induction_on with
    | h m ih =>
      by_cases hm : m = 0
      · subst m
        exact ⟨∅, by simp⟩
      have half : m / 2 < m := Nat.div_lt_self (by omega) (by decide)
      obtain ⟨s, hs⟩ := ih (m / 2) half
      let t := s.image Nat.succ
      have hzero : 0 ∉ t := by simp [t]
      have hsum : (∑ k ∈ t, 2 ^ k) = 2 * (∑ k ∈ s, 2 ^ k) := by
        dsimp only [t]
        rw [Finset.sum_image]
        · simp_rw [Nat.pow_succ, mul_comm _ 2]
          exact (Finset.mul_sum s (fun k => 2 ^ k) 2).symm
        · exact Nat.succ_injective.injOn
      by_cases he : m % 2 = 0
      · refine ⟨t, ?_⟩
        rw [hsum, ← hs]
        omega
      · refine ⟨insert 0 t, ?_⟩
        rw [Finset.sum_insert hzero, pow_zero, hsum, ← hs]
        omega
  exact all n
#print axioms positive_nat_sum_distinct_powers_two

theorem hockey_stick_binomial_identity (n : ℕ) : (∑ k ∈ Finset.range (n + 1), Nat.choose (4 + k) k) = Nat.choose (5 + n) n := by
  calc
    (∑ k ∈ Finset.range (n + 1), Nat.choose (4 + k) k) =
        (∑ k ∈ Finset.range (n + 1), Nat.choose (k + 4) 4) := by
      apply Finset.sum_congr rfl
      intro k hk
      simpa [Nat.add_comm] using (Nat.choose_symm (n := k + 4) (k := 4) (by omega))
    _ = Nat.choose (n + 4 + 1) 5 := Nat.sum_range_add_choose n 4
    _ = Nat.choose (5 + n) n := by
      have he : n + 4 + 1 = 5 + n := by omega
      rw [he]
      have hs : (5 + n) - 5 = n := by omega
      simpa only [hs] using (Nat.choose_symm (n := 5 + n) (k := 5) (by omega)).symm
#print axioms hockey_stick_binomial_identity

end AdditionalReferences

end AuditReference1

namespace AuditReference2

theorem even_add_of_even (a b : ℤ) (ha : Even a) (hb : Even b) : Even (a + b) := by
  rcases ha with ⟨x, hx⟩
  rcases hb with ⟨y, hy⟩
  refine ⟨x + y, ?_⟩
  nlinarith

end AuditReference2

namespace AuditReference3

theorem even_iff_even_three_mul (n : ℤ) : Even n ↔ Even (3 * n) := by
  constructor
  · intro h
    rcases h with ⟨k, hk⟩
    refine ⟨3 * k, ?_⟩
    nlinarith
  · intro h
    rcases h with ⟨k, hk⟩
    have hn : n % 2 = 0 := by omega
    refine ⟨n / 2, ?_⟩
    omega

end AuditReference3

namespace AuditReference4

theorem even_cube_sub_self (n : ℤ) : Even (n ^ 3 - n) := by
  rcases Int.even_or_odd n with ⟨k, hk⟩ | ⟨k, hk⟩
  · refine ⟨4 * k ^ 3 - k, ?_⟩
    rw [hk]
    ring
  · refine ⟨4 * k ^ 3 + 6 * k ^ 2 + 2 * k, ?_⟩
    rw [hk]
    ring

end AuditReference4

namespace AuditReference5

theorem pascal_row_sum (n : ℕ) : ∑ k ∈ Finset.range (n + 1), Nat.choose n k = 2 ^ n := by
  simpa using Nat.sum_range_choose n

end AuditReference5

namespace AuditReference6

theorem add_three_lt_add_seven (n : ℕ) : n + 3 < n + 7 := by
  omega

end AuditReference6

namespace AuditReference7

theorem modEq_add_two (a b c d n : ℤ) (_hn : 0 < n)
    (hab : a ≡ b [ZMOD n]) (hcd : c ≡ d [ZMOD n]) :
    a + c ≡ b + d [ZMOD n] := by
  exact hab.add hcd

end AuditReference7

namespace AuditReference8

theorem choose_zero_and_self (n : ℕ) : Nat.choose n 0 = 1 ∧ Nat.choose n n = 1 := by
  simp

end AuditReference8

namespace AuditReference9

theorem dvd_mul_right_int (a b c : ℤ) (hab : a ∣ b) : a ∣ b * c := by
  obtain ⟨k, hk⟩ := hab
  refine ⟨k * c, ?_⟩
  rw [hk]
  ring

end AuditReference9

namespace AuditReference10

theorem dvd_add_sub_int (a b c : ℤ) (hab : a ∣ b) (hac : a ∣ c) :
    a ∣ b + c ∧ a ∣ b - c := by
  obtain ⟨x, hx⟩ := hab
  obtain ⟨y, hy⟩ := hac
  constructor
  · refine ⟨x + y, ?_⟩
    rw [hx, hy]
    ring
  · refine ⟨x - y, ?_⟩
    rw [hx, hy]
    ring

end AuditReference10

namespace AuditReference11

theorem postage_representable_large (n : ℕ) (hn : 28 ≤ n) :
    ∃ five eight : ℕ, 5 * five + 8 * eight = n := by
  have step : ∀ k : ℕ, 28 ≤ k →
      (∃ five eight : ℕ, 5 * five + 8 * eight = k) →
      ∃ five eight : ℕ, 5 * five + 8 * eight = k + 1 := by
    intro k hk hrepr
    obtain ⟨five, eight, hsum⟩ := hrepr
    by_cases hfive : 3 ≤ five
    · refine ⟨five - 3, eight + 2, ?_⟩
      omega
    · have height : 3 ≤ eight := by omega
      refine ⟨five + 5, eight - 3, ?_⟩
      omega
  induction n, hn using Nat.le_induction with
  | base => exact ⟨4, 1, by norm_num⟩
  | succ k hk ih => exact step k hk ih

end AuditReference11

namespace AuditReference12

theorem diophantine_six_ten (x y : ℤ) :
    6 * x + 10 * y = 32 ↔ ∃ k : ℤ, x = 2 - 5 * k ∧ y = 2 + 3 * k := by
  constructor
  · intro h
    refine ⟨(y - 2) / 3, ?_, ?_⟩ <;> omega
  · rintro ⟨k, rfl, rfl⟩
    omega

end AuditReference12

namespace AuditReference13

theorem largest_modulus_sixteen_twentyfive :
    Nat.ModEq 9 16 25 ∧ ∀ n : ℕ, 0 < n → Nat.ModEq n 16 25 → n ≤ 9 := by
  constructor
  · decide
  · intro n hn h
    have hd : n ∣ 9 := by
      simpa using (Nat.modEq_iff_dvd' (by decide : 16 ≤ 25)).mp h
    exact Nat.le_of_dvd (by decide) hd

end AuditReference13

namespace AuditReference14
open scoped BigOperators

theorem study_a_power_add (a m n : ℕ) : a ^ (m + n) = a ^ m * a ^ n := by
  exact pow_add a m n
#print axioms study_a_power_add

theorem study_a_euclidean (a b : ℤ) : a % b + b * (a / b) = a := by
  exact Int.emod_add_mul_ediv a b
#print axioms study_a_euclidean

theorem study_a_choose_symmetry (n k : ℕ) (h : k ≤ n) : n.choose k = n.choose (n - k) := by
  exact (Nat.choose_symm h).symm
#print axioms study_a_choose_symmetry

theorem study_a_abs_product (x y : ℝ) : |x * y| = |x| * |y| := by
  exact abs_mul x y
#print axioms study_a_abs_product

theorem study_a_sqrt_square (x : ℝ) (h : 0 ≤ x) : (Real.sqrt x) ^ 2 = x := by
  exact Real.sq_sqrt h
#print axioms study_a_sqrt_square

theorem study_a_truncated_sub (a b : ℕ) (h : b ≤ a) : a - b + b = a := by
  exact Nat.sub_add_cancel h
#print axioms study_a_truncated_sub

theorem study_a_inverse_difference (x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0) : 1 / x - 1 / y = (y - x) / (x * y) := by
  field_simp <;> ring
#print axioms study_a_inverse_difference

theorem study_a_gcd_lcm (a b : ℕ) : Nat.gcd a b * Nat.lcm a b = a * b := by
  exact Nat.gcd_mul_lcm a b
#print axioms study_a_gcd_lcm

theorem study_d_euclid (p a b : ℕ) (hp : p.Prime) : p ∣ a * b ↔ p ∣ a ∨ p ∣ b := by
  exact hp.dvd_mul
#print axioms study_d_euclid

theorem study_d_unbounded_primes (n : ℕ) : ∃ p : ℕ, n ≤ p ∧ p.Prime := by
  exact Nat.exists_infinite_primes n
#print axioms study_d_unbounded_primes

theorem study_d_bezout (a b : ℤ) : ∃ x y : ℤ, (Int.gcd a b : ℤ) = a * x + b * y := by
  exact ⟨Int.gcdA a b, Int.gcdB a b, Int.gcd_eq_gcd_ab a b⟩
#print axioms study_d_bezout

theorem study_d_coprime_successor (n : ℕ) : Nat.Coprime n (n + 1) := by
  exact (Nat.coprime_self_add_right (m := n) (n := 1)).2 (Nat.coprime_one_right n)
#print axioms study_d_coprime_successor

theorem study_d_prime_factorial (p n : ℕ) (hp : p.Prime) : p ∣ n.factorial ↔ p ≤ n := by
  exact hp.dvd_factorial
#print axioms study_d_prime_factorial

theorem study_d_mersenne_gcd (a b c : ℕ) : Nat.gcd (a ^ b - 1) (a ^ c - 1) = a ^ Nat.gcd b c - 1 := by
  exact Nat.pow_sub_one_gcd_pow_sub_one a b c
#print axioms study_d_mersenne_gcd

theorem study_d_prime_parity (p : ℕ) (hp : p.Prime) : p = 2 ∨ Odd p := by
  simpa only [Nat.odd_iff] using hp.eq_two_or_odd
#print axioms study_d_prime_parity

theorem study_d_dvd_antisymmetry (a b : ℕ) (hab : a ∣ b) (hba : b ∣ a) : a = b := by
  exact Nat.dvd_antisymm hab hba
#print axioms study_d_dvd_antisymmetry

theorem study_d_coprime_power (a b n : ℕ) (hn : 0 < n) : Nat.Coprime (a ^ n) b ↔ Nat.Coprime a b := by
  exact Nat.coprime_pow_left_iff hn a b
#print axioms study_d_coprime_power

theorem study_d_frobenius (m n a b : ℕ) (h : Nat.Coprime m n) (ha : a ≠ 0) (hb : b ≠ 0) : m * a + n * b ≠ m * n := by
  simpa only [mul_comm m a, mul_comm n b] using h.mul_add_mul_ne_mul ha hb
#print axioms study_d_frobenius

theorem study_i_factorial (n : ℕ) : (n + 1).factorial = (n + 1) * n.factorial := by
  exact Nat.factorial_succ n
#print axioms study_i_factorial

theorem study_i_fibonacci (n : ℕ) : Nat.fib (n + 2) = Nat.fib n + Nat.fib (n + 1) := by
  exact Nat.fib_add_two
#print axioms study_i_fibonacci

theorem study_i_bernoulli (x : ℝ) (n : ℕ) (h : -1 ≤ x) : 1 + (n : ℝ) * x ≤ (1 + x) ^ n := by
  exact one_add_mul_le_pow (by linarith) n
#print axioms study_i_bernoulli

theorem study_i_vandermonde (m n k : ℕ) : (m + n).choose k = ∑ i ∈ Finset.range (k + 1), m.choose i * n.choose (k - i) := by
  simpa only [Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk] using Nat.add_choose_eq m n k
#print axioms study_i_vandermonde

theorem study_i_fermat_product (n : ℕ) : (∏ k ∈ Finset.range n, Nat.fermatNumber k) = Nat.fermatNumber n - 2 := by
  exact Nat.prod_fermatNumber n
#print axioms study_i_fermat_product

theorem study_q_amgm (x y : ℝ) : 2 * x * y ≤ x ^ 2 + y ^ 2 := by
  nlinarith [sq_nonneg (x - y)]
#print axioms study_q_amgm

theorem study_q_cauchy (a b c d : ℝ) : (a * c + b * d) ^ 2 ≤ (a ^ 2 + b ^ 2) * (c ^ 2 + d ^ 2) := by
  nlinarith [sq_nonneg (a * d - b * c)]
#print axioms study_q_cauchy

theorem study_q_triangle (x y : ℝ) : |x + y| ≤ |x| + |y| := by
  exact abs_add_le x y
#print axioms study_q_triangle

theorem study_q_reciprocal (x y : ℝ) (hx : 0 < x) (hxy : x ≤ y) : 1 / y ≤ 1 / x := by
  exact one_div_le_one_div_of_le hx hxy
#print axioms study_q_reciprocal

theorem study_q_log (b n : ℕ) (hn : n ≠ 0) : b ^ Nat.log b n ≤ n := by
  exact Nat.pow_log_le_self b hn
#print axioms study_q_log

theorem study_q_sqrt_monotone (x y : ℝ) (h : x ≤ y) : Real.sqrt x ≤ Real.sqrt y := by
  exact Real.sqrt_le_sqrt h
#print axioms study_q_sqrt_monotone

theorem study_q_exp_tangent (x : ℝ) : x + 1 ≤ Real.exp x := by
  exact Real.add_one_le_exp x
#print axioms study_q_exp_tangent

theorem study_q_sine (x : ℝ) (hx : 0 ≤ x) : Real.sin x ≤ x := by
  exact Real.sin_le hx
#print axioms study_q_sine

theorem study_q_quotient (m n : ℕ) : m / n ≤ m := by
  exact Nat.div_le_self m n
#print axioms study_q_quotient

theorem study_m_crt (a b n m : ℕ) (h : Nat.ModEq (Nat.gcd n m) a b) : ∃ k : ℕ, Nat.ModEq n k a ∧ Nat.ModEq m k b := by
  exact ⟨Nat.chineseRemainder' h, (Nat.chineseRemainder' h).property⟩
#print axioms study_m_crt

theorem study_m_cancel (m c a b : ℕ) (hm : 0 < m) (h : Nat.ModEq m (c * a) (c * b)) : Nat.ModEq (m / Nat.gcd m c) a b := by
  exact h.cancel_left_div_gcd hm
#print axioms study_m_cancel

theorem study_m_canonical (m a b : ℕ) (ha : a < m) (hb : b < m) (h : Nat.ModEq m a b) : a = b := by
  exact h.eq_of_lt_of_lt ha hb
#print axioms study_m_canonical

theorem study_m_fermat (p : ℕ) (hp : p.Prime) (a : ℤ) : Int.ModEq (p : ℤ) (a ^ p) a := by
  exact Int.ModEq.pow_prime_eq_self hp a
#print axioms study_m_fermat

theorem study_m_wilson (p : ℕ) [Fact p.Prime] : ((p - 1).factorial : ZMod p) = -1 := by
  exact ZMod.wilsons_lemma p
#print axioms study_m_wilson

theorem study_m_power (a b m : ℤ) (n : ℕ) (h : Int.ModEq m a b) : Int.ModEq m (a ^ n) (b ^ n) := by
  exact h.pow n
#print axioms study_m_power

theorem study_m_gcd_obstruction (a b m : ℤ) (h : ¬ (Int.gcd a m : ℤ) ∣ b) : ¬ ∃ x : ℤ, Int.ModEq m (a * x) b := by
  intro ⟨x, hx⟩; apply h; have hd := hx.dvd; have ha : (Int.gcd a m : ℤ) ∣ a := Int.gcd_dvd_left a m; have hm : (Int.gcd a m : ℤ) ∣ m := Int.gcd_dvd_right a m; have ht := hm.trans hd; have hp := ha.mul_right x; have hs := dvd_add ht hp; simpa using hs
#print axioms study_m_gcd_obstruction

theorem study_m_residue_product (a b m : ℕ) : (a * b) % m = ((a % m) * (b % m)) % m := by
  exact Nat.mul_mod a b m
#print axioms study_m_residue_product

theorem study_a_trig_unit (x : ℝ) : (Real.sin x) ^ 2 + (Real.cos x) ^ 2 = 1 := by
  exact Real.sin_sq_add_cos_sq x
#print axioms study_a_trig_unit

theorem study_a_log_product (x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0) : Real.log (x * y) = Real.log x + Real.log y := by
  exact Real.log_mul hx hy
#print axioms study_a_log_product

theorem study_a_exp_add (x y : ℝ) : Real.exp (x + y) = Real.exp x * Real.exp y := by
  exact Real.exp_add x y
#print axioms study_a_exp_add

theorem study_a_min_max (x y : ℝ) : min x y + max x y = x + y := by
  exact min_add_max x y
#print axioms study_a_min_max

theorem study_d_factorization (a b : ℕ) (ha : a ≠ 0) (hb : b ≠ 0) : (a * b).factorization = a.factorization + b.factorization := by
  exact Nat.factorization_mul ha hb
#print axioms study_d_factorization

theorem study_d_totient_sum (n : ℕ) : (∑ d ∈ n.divisors, Nat.totient d) = n := by
  exact Nat.sum_totient n
#print axioms study_d_totient_sum

theorem study_i_telescope (f : ℕ → ℤ) (n : ℕ) : (∑ i ∈ Finset.range n, (f (i + 1) - f i)) = f n - f 0 := by
  induction n with | zero => simp | succ n ih => rw [Finset.sum_range_succ, ih]; ring
#print axioms study_i_telescope

theorem study_i_alternating_binomial (n : ℕ) (hn : n ≠ 0) : (∑ k ∈ Finset.range (n + 1), ((-1 : ℤ) ^ k * (n.choose k : ℤ))) = 0 := by
  exact Int.alternating_sum_range_choose_of_ne hn
#print axioms study_i_alternating_binomial

theorem study_q_integer_sqrt (n : ℕ) : Nat.sqrt n ^ 2 < n + 1 := by
  exact Nat.sqrt_mul_sqrt_lt_succ' n
#print axioms study_q_integer_sqrt

theorem study_q_finite_inclusion (s t : Finset ℕ) (h : s ⊆ t) : s.card ≤ t.card := by
  exact Finset.card_le_card h
#print axioms study_q_finite_inclusion

theorem study_q_log_tangent (x : ℝ) (hx : 0 < x) : Real.log x ≤ x - 1 := by
  exact Real.log_le_sub_one_of_pos hx
#print axioms study_q_log_tangent

theorem study_m_euler (a m : ℕ) (h : Nat.Coprime a m) : Nat.ModEq m (a ^ Nat.totient m) 1 := by
  exact Nat.ModEq.pow_totient h
#print axioms study_m_euler


end AuditReference14

namespace AuditReference15
open scoped BigOperators

theorem study_q_rational_density (x y : ℝ) (h : x < y) : ∃ q : ℚ, x < q ∧ (q : ℝ) < y := by
  exact exists_rat_btwn h
#print axioms study_q_rational_density

theorem study_i_stirling (n k : ℕ) : Nat.stirlingSecond (n + 1) (k + 1) = (k + 1) * Nat.stirlingSecond n (k + 1) + Nat.stirlingSecond n k := by
  exact Nat.stirlingSecond_succ_succ n k
#print axioms study_i_stirling

theorem study_i_catalan (n : ℕ) : catalan (n + 1) = ∑ i : Fin n.succ, catalan i * catalan (n - i) := by
  exact catalan_succ n
#print axioms study_i_catalan

theorem study_q_rearrangement (a b c d : ℝ) (hab : a ≤ b) (hcd : c ≤ d) : a * d + b * c ≤ a * c + b * d := by
  nlinarith [mul_nonneg (sub_nonneg.mpr hab) (sub_nonneg.mpr hcd)]
#print axioms study_q_rearrangement

theorem study_q_pigeonhole (s t : Finset ℕ) (f : ℕ → ℕ) (h : t.card < s.card) (hm : ∀ x ∈ s, f x ∈ t) : ∃ x ∈ s, ∃ y ∈ s, x ≠ y ∧ f x = f y := by
  exact Finset.exists_ne_map_eq_of_card_lt_of_maps_to h hm
#print axioms study_q_pigeonhole

theorem study_d_prime_factor_exists (n : ℕ) (hn : 2 ≤ n) : ∃ p : ℕ, p.Prime ∧ p ∣ n := by
  exact Nat.exists_prime_and_dvd (by omega)
#print axioms study_d_prime_factor_exists

theorem study_d_euclidean_gcd (m n : ℕ) : Nat.gcd m n = Nat.gcd (n % m) m := by
  exact Nat.gcd_rec m n
#print axioms study_d_euclidean_gcd

end AuditReference15

-- Exact type comparison: arith_001
example : ∀ (a b : ℕ), (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := @AuditReference0.add_sq_nat
#print axioms AuditReference0.add_sq_nat

-- Exact type comparison: arith_002
example : ∀ (a b : ℕ) (h : b ≤ a), a ^ 2 - b ^ 2 = (a + b) * (a - b) := @AuditReference0.sq_sub_sq_nat
#print axioms AuditReference0.sq_sub_sq_nat

-- Exact type comparison: div_001
example : ∀ (n : ℕ) (h : Even n), Even (n ^ 2) := @AuditReference0.even_sq_of_even
#print axioms AuditReference0.even_sq_of_even

-- Exact type comparison: div_002
example : ∀ (n : ℕ), Even (n * (n + 1)) := @AuditReference0.n_mul_succ_even
#print axioms AuditReference0.n_mul_succ_even

-- Exact type comparison: div_003
example : ∀ (n : ℕ) (h : 6 ∣ n), 2 ∣ n ∧ 3 ∣ n := @AuditReference0.div6_imp_div2_div3
#print axioms AuditReference0.div6_imp_div2_div3

-- Exact type comparison: mod_001
example : ∀ (a b m : ℤ) (h : a ≡ b [ZMOD m]), a + 1 ≡ b + 1 [ZMOD m] := @AuditReference0.cong_add_one
#print axioms AuditReference0.cong_add_one

-- Exact type comparison: mod_002
example : ∀ (a : ℤ), a ^ 2 % 4 = 0 ∨ a ^ 2 % 4 = 1 := @AuditReference0.sq_mod_four
#print axioms AuditReference0.sq_mod_four

-- Exact type comparison: ind_001
example : ∀ (n : ℕ), 2 * (Finset.range (n + 1)).sum id = n * (n + 1) := @AuditReference0.gauss_sum
#print axioms AuditReference0.gauss_sum

-- Exact type comparison: ind_002
example : ∀ (n : ℕ), (Finset.range n).sum (fun i => 2 * i + 1) = n ^ 2 := @AuditReference0.sum_odd_sq
#print axioms AuditReference0.sum_odd_sq

-- Exact type comparison: ind_003
example : ∀ (n : ℕ), n < 2 ^ n := @AuditReference0.two_pow_gt_self
#print axioms AuditReference0.two_pow_gt_self

-- Exact type comparison: div_004
example : ∀ (a b : ℕ) (ha : ∃ i, a = 2*i+1) (hb : ∃ j, b = 2*j+1), ∃ k, a + b = 2 * k := @AuditReference0.sum_two_odd_even
#print axioms AuditReference0.sum_two_odd_even

-- Exact type comparison: ineq_001
example : ∀ (n : ℕ), n ≤ n ^ 2 := @AuditReference0.sq_ge_self
#print axioms AuditReference0.sq_ge_self

-- Exact type comparison: arith_003
example : ∀ (a b c : ℕ), a * (b + c) = a * b + a * c := @AuditReference0.mul_distrib_left
#print axioms AuditReference0.mul_distrib_left

-- Exact type comparison: arith_003_mathlib
example : ∀ (a b c : ℕ), a * (b + c) = a * b + a * c := @AuditReference0.distributive_nat
#print axioms AuditReference0.distributive_nat

-- Exact type comparison: arith_004
example : ∀ (a b : ℕ) (h : b ≤ a), (a - b) ^ 2 + 2 * a * b = a ^ 2 + b ^ 2 := @AuditReference0.sq_sub_nat
#print axioms AuditReference0.sq_sub_nat

-- Exact type comparison: div_005
example : ∀ (n : ℕ) (h : ∃ k, n = 2*k+1), ∃ j, n ^ 2 = 2*j+1 := @AuditReference0.odd_sq_of_odd
#print axioms AuditReference0.odd_sq_of_odd

-- Exact type comparison: div_006
example : ∀ (n : ℕ), (∃ j, n ^ 2 = 2 * j) ↔ (∃ k, n = 2 * k) := @AuditReference0.sq_even_iff_even
#print axioms AuditReference0.sq_even_iff_even

-- Exact type comparison: ineq_002
example : ∀ (a b : ℕ), a * b + 1 ≤ (a + 1) * (b + 1) := @AuditReference0.prod_succ_ge
#print axioms AuditReference0.prod_succ_ge

-- Exact type comparison: ineq_003
example : ∀ (n : ℕ) (h : 1 ≤ n), n + 1 ≤ 2 ^ n := @AuditReference0.succ_le_two_pow
#print axioms AuditReference0.succ_le_two_pow

-- Exact type comparison: ind_004
example : ∀ (n : ℕ), geomSum n + 1 = 2 ^ n := @AuditReference1.AdditionalReferences.geom_sum_eq
#print axioms AuditReference1.AdditionalReferences.geom_sum_eq

-- Exact type comparison: mod_003
example : ∀ (n : ℕ), n ^ 2 % 3 = 0 ∨ n ^ 2 % 3 = 1 := @AuditReference0.sq_mod_three
#print axioms AuditReference0.sq_mod_three

-- Exact type comparison: div_007
example : ∀ (a b : ℤ) (ha : Even a) (hb : Even b), Even (a + b) := @AuditReference2.even_add_of_even
#print axioms AuditReference2.even_add_of_even

-- Exact type comparison: div_008
example : ∀ (n : ℤ), Even n ↔ Even (3 * n) := @AuditReference3.even_iff_even_three_mul
#print axioms AuditReference3.even_iff_even_three_mul

-- Exact type comparison: div_009
example : ∀ (n : ℤ), Even (n ^ 3 - n) := @AuditReference4.even_cube_sub_self
#print axioms AuditReference4.even_cube_sub_self

-- Exact type comparison: ind_005
example : ∀ (n : ℕ), ∑ k ∈ Finset.range (n + 1), Nat.choose n k = 2 ^ n := @AuditReference5.pascal_row_sum
#print axioms AuditReference5.pascal_row_sum

-- Exact type comparison: ineq_004
example : ∀ (n : ℕ), n + 3 < n + 7 := @AuditReference6.add_three_lt_add_seven
#print axioms AuditReference6.add_three_lt_add_seven

-- Exact type comparison: mod_004
example : ∀ (a b c d n : ℤ) (_hn : 0 < n) (hab : a ≡ b [ZMOD n]) (hcd : c ≡ d [ZMOD n]), a + c ≡ b + d [ZMOD n] := @AuditReference7.modEq_add_two
#print axioms AuditReference7.modEq_add_two

-- Exact type comparison: arith_005
example : ∀ (n : ℕ), Nat.choose n 0 = 1 ∧ Nat.choose n n = 1 := @AuditReference8.choose_zero_and_self
#print axioms AuditReference8.choose_zero_and_self

-- Exact type comparison: ind_006
example : ∀ (n : ℕ) (hn : 28 ≤ n), ∃ five eight : ℕ, 5 * five + 8 * eight = n := @AuditReference11.postage_representable_large
#print axioms AuditReference11.postage_representable_large

-- Exact type comparison: div_010
example : ∀ (a b c : ℤ) (hab : a ∣ b), a ∣ b * c := @AuditReference9.dvd_mul_right_int
#print axioms AuditReference9.dvd_mul_right_int

-- Exact type comparison: div_011
example : ∀ (a b c : ℤ) (hab : a ∣ b) (hac : a ∣ c), a ∣ b + c ∧ a ∣ b - c := @AuditReference10.dvd_add_sub_int
#print axioms AuditReference10.dvd_add_sub_int

-- Exact type comparison: mod_005
example : ∀ (n : ℕ), 6 ∣ 7 ^ n - 1 := @AuditReference1.AdditionalReferences.pow_seven_sub_one_dvd_six
#print axioms AuditReference1.AdditionalReferences.pow_seven_sub_one_dvd_six

-- Exact type comparison: ind_007
example : ∀ (n : ℕ), (∑ k ∈ Finset.range (n + 1), k ^ 2) = n * (n + 1) * (2 * n + 1) / 6 := @AuditReference1.AdditionalReferences.sum_squares_closed_form
#print axioms AuditReference1.AdditionalReferences.sum_squares_closed_form

-- Exact type comparison: ind_008
example : ∀ (n : ℕ) (hn : 1 ≤ n), ∃ s : Finset ℕ, n = ∑ k ∈ s, 2 ^ k := @AuditReference1.AdditionalReferences.positive_nat_sum_distinct_powers_two
#print axioms AuditReference1.AdditionalReferences.positive_nat_sum_distinct_powers_two

-- Exact type comparison: ind_009
example : ∀ (n : ℕ), (∑ k ∈ Finset.range (n + 1), Nat.choose (4 + k) k) = Nat.choose (5 + n) n := @AuditReference1.AdditionalReferences.hockey_stick_binomial_identity
#print axioms AuditReference1.AdditionalReferences.hockey_stick_binomial_identity

-- Exact type comparison: mod_006
example : Nat.ModEq 9 16 25 ∧ ∀ n : ℕ, 0 < n → Nat.ModEq n 16 25 → n ≤ 9 := @AuditReference13.largest_modulus_sixteen_twentyfive
#print axioms AuditReference13.largest_modulus_sixteen_twentyfive

-- Exact type comparison: div_012
example : ∀ (x y : ℤ), 6 * x + 10 * y = 32 ↔ ∃ k : ℤ, x = 2 - 5 * k ∧ y = 2 + 3 * k := @AuditReference12.diophantine_six_ten
#print axioms AuditReference12.diophantine_six_ten

-- Exact type comparison: lib_a_power_add
example : ∀ (a m n : ℕ), a ^ (m + n) = a ^ m * a ^ n := @AuditReference14.study_a_power_add
#print axioms AuditReference14.study_a_power_add

-- Exact type comparison: lib_a_euclidean
example : ∀ (a b : ℤ), a % b + b * (a / b) = a := @AuditReference14.study_a_euclidean
#print axioms AuditReference14.study_a_euclidean

-- Exact type comparison: lib_a_choose_symmetry
example : ∀ (n k : ℕ) (h : k ≤ n), n.choose k = n.choose (n - k) := @AuditReference14.study_a_choose_symmetry
#print axioms AuditReference14.study_a_choose_symmetry

-- Exact type comparison: lib_a_abs_product
example : ∀ (x y : ℝ), |x * y| = |x| * |y| := @AuditReference14.study_a_abs_product
#print axioms AuditReference14.study_a_abs_product

-- Exact type comparison: lib_a_sqrt_square
example : ∀ (x : ℝ) (h : 0 ≤ x), (Real.sqrt x) ^ 2 = x := @AuditReference14.study_a_sqrt_square
#print axioms AuditReference14.study_a_sqrt_square

-- Exact type comparison: lib_a_truncated_sub
example : ∀ (a b : ℕ) (h : b ≤ a), a - b + b = a := @AuditReference14.study_a_truncated_sub
#print axioms AuditReference14.study_a_truncated_sub

-- Exact type comparison: lib_a_inverse_difference
example : ∀ (x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0), 1 / x - 1 / y = (y - x) / (x * y) := @AuditReference14.study_a_inverse_difference
#print axioms AuditReference14.study_a_inverse_difference

-- Exact type comparison: lib_a_gcd_lcm
example : ∀ (a b : ℕ), Nat.gcd a b * Nat.lcm a b = a * b := @AuditReference14.study_a_gcd_lcm
#print axioms AuditReference14.study_a_gcd_lcm

-- Exact type comparison: lib_d_euclid
example : ∀ (p a b : ℕ) (hp : p.Prime), p ∣ a * b ↔ p ∣ a ∨ p ∣ b := @AuditReference14.study_d_euclid
#print axioms AuditReference14.study_d_euclid

-- Exact type comparison: lib_d_unbounded_primes
example : ∀ (n : ℕ), ∃ p : ℕ, n ≤ p ∧ p.Prime := @AuditReference14.study_d_unbounded_primes
#print axioms AuditReference14.study_d_unbounded_primes

-- Exact type comparison: lib_d_bezout
example : ∀ (a b : ℤ), ∃ x y : ℤ, (Int.gcd a b : ℤ) = a * x + b * y := @AuditReference14.study_d_bezout
#print axioms AuditReference14.study_d_bezout

-- Exact type comparison: lib_d_coprime_successor
example : ∀ (n : ℕ), Nat.Coprime n (n + 1) := @AuditReference14.study_d_coprime_successor
#print axioms AuditReference14.study_d_coprime_successor

-- Exact type comparison: lib_d_prime_factorial
example : ∀ (p n : ℕ) (hp : p.Prime), p ∣ n.factorial ↔ p ≤ n := @AuditReference14.study_d_prime_factorial
#print axioms AuditReference14.study_d_prime_factorial

-- Exact type comparison: lib_d_mersenne_gcd
example : ∀ (a b c : ℕ), Nat.gcd (a ^ b - 1) (a ^ c - 1) = a ^ Nat.gcd b c - 1 := @AuditReference14.study_d_mersenne_gcd
#print axioms AuditReference14.study_d_mersenne_gcd

-- Exact type comparison: lib_d_prime_parity
example : ∀ (p : ℕ) (hp : p.Prime), p = 2 ∨ Odd p := @AuditReference14.study_d_prime_parity
#print axioms AuditReference14.study_d_prime_parity

-- Exact type comparison: lib_d_dvd_antisymmetry
example : ∀ (a b : ℕ) (hab : a ∣ b) (hba : b ∣ a), a = b := @AuditReference14.study_d_dvd_antisymmetry
#print axioms AuditReference14.study_d_dvd_antisymmetry

-- Exact type comparison: lib_d_coprime_power
example : ∀ (a b n : ℕ) (hn : 0 < n), Nat.Coprime (a ^ n) b ↔ Nat.Coprime a b := @AuditReference14.study_d_coprime_power
#print axioms AuditReference14.study_d_coprime_power

-- Exact type comparison: lib_d_frobenius
example : ∀ (m n a b : ℕ) (h : Nat.Coprime m n) (ha : a ≠ 0) (hb : b ≠ 0), m * a + n * b ≠ m * n := @AuditReference14.study_d_frobenius
#print axioms AuditReference14.study_d_frobenius

-- Exact type comparison: lib_i_factorial
example : ∀ (n : ℕ), (n + 1).factorial = (n + 1) * n.factorial := @AuditReference14.study_i_factorial
#print axioms AuditReference14.study_i_factorial

-- Exact type comparison: lib_i_fibonacci
example : ∀ (n : ℕ), Nat.fib (n + 2) = Nat.fib n + Nat.fib (n + 1) := @AuditReference14.study_i_fibonacci
#print axioms AuditReference14.study_i_fibonacci

-- Exact type comparison: lib_i_bernoulli
example : ∀ (x : ℝ) (n : ℕ) (h : -1 ≤ x), 1 + (n : ℝ) * x ≤ (1 + x) ^ n := @AuditReference14.study_i_bernoulli
#print axioms AuditReference14.study_i_bernoulli

-- Exact type comparison: lib_i_vandermonde
example : ∀ (m n k : ℕ), (m + n).choose k = ∑ i ∈ Finset.range (k + 1), m.choose i * n.choose (k - i) := @AuditReference14.study_i_vandermonde
#print axioms AuditReference14.study_i_vandermonde

-- Exact type comparison: lib_i_fermat_product
example : ∀ (n : ℕ), (∏ k ∈ Finset.range n, Nat.fermatNumber k) = Nat.fermatNumber n - 2 := @AuditReference14.study_i_fermat_product
#print axioms AuditReference14.study_i_fermat_product

-- Exact type comparison: lib_q_amgm
example : ∀ (x y : ℝ), 2 * x * y ≤ x ^ 2 + y ^ 2 := @AuditReference14.study_q_amgm
#print axioms AuditReference14.study_q_amgm

-- Exact type comparison: lib_q_cauchy
example : ∀ (a b c d : ℝ), (a * c + b * d) ^ 2 ≤ (a ^ 2 + b ^ 2) * (c ^ 2 + d ^ 2) := @AuditReference14.study_q_cauchy
#print axioms AuditReference14.study_q_cauchy

-- Exact type comparison: lib_q_triangle
example : ∀ (x y : ℝ), |x + y| ≤ |x| + |y| := @AuditReference14.study_q_triangle
#print axioms AuditReference14.study_q_triangle

-- Exact type comparison: lib_q_reciprocal
example : ∀ (x y : ℝ) (hx : 0 < x) (hxy : x ≤ y), 1 / y ≤ 1 / x := @AuditReference14.study_q_reciprocal
#print axioms AuditReference14.study_q_reciprocal

-- Exact type comparison: lib_q_log
example : ∀ (b n : ℕ) (hn : n ≠ 0), b ^ Nat.log b n ≤ n := @AuditReference14.study_q_log
#print axioms AuditReference14.study_q_log

-- Exact type comparison: lib_q_sqrt_monotone
example : ∀ (x y : ℝ) (h : x ≤ y), Real.sqrt x ≤ Real.sqrt y := @AuditReference14.study_q_sqrt_monotone
#print axioms AuditReference14.study_q_sqrt_monotone

-- Exact type comparison: lib_q_exp_tangent
example : ∀ (x : ℝ), x + 1 ≤ Real.exp x := @AuditReference14.study_q_exp_tangent
#print axioms AuditReference14.study_q_exp_tangent

-- Exact type comparison: lib_q_sine
example : ∀ (x : ℝ) (hx : 0 ≤ x), Real.sin x ≤ x := @AuditReference14.study_q_sine
#print axioms AuditReference14.study_q_sine

-- Exact type comparison: lib_q_quotient
example : ∀ (m n : ℕ), m / n ≤ m := @AuditReference14.study_q_quotient
#print axioms AuditReference14.study_q_quotient

-- Exact type comparison: lib_m_crt
example : ∀ (a b n m : ℕ) (h : Nat.ModEq (Nat.gcd n m) a b), ∃ k : ℕ, Nat.ModEq n k a ∧ Nat.ModEq m k b := @AuditReference14.study_m_crt
#print axioms AuditReference14.study_m_crt

-- Exact type comparison: lib_m_cancel
example : ∀ (m c a b : ℕ) (hm : 0 < m) (h : Nat.ModEq m (c * a) (c * b)), Nat.ModEq (m / Nat.gcd m c) a b := @AuditReference14.study_m_cancel
#print axioms AuditReference14.study_m_cancel

-- Exact type comparison: lib_m_canonical
example : ∀ (m a b : ℕ) (ha : a < m) (hb : b < m) (h : Nat.ModEq m a b), a = b := @AuditReference14.study_m_canonical
#print axioms AuditReference14.study_m_canonical

-- Exact type comparison: lib_m_fermat
example : ∀ (p : ℕ) (hp : p.Prime) (a : ℤ), Int.ModEq (p : ℤ) (a ^ p) a := @AuditReference14.study_m_fermat
#print axioms AuditReference14.study_m_fermat

-- Exact type comparison: lib_m_wilson
example : ∀ (p : ℕ) [Fact p.Prime], ((p - 1).factorial : ZMod p) = -1 := @AuditReference14.study_m_wilson
#print axioms AuditReference14.study_m_wilson

-- Exact type comparison: lib_m_power
example : ∀ (a b m : ℤ) (n : ℕ) (h : Int.ModEq m a b), Int.ModEq m (a ^ n) (b ^ n) := @AuditReference14.study_m_power
#print axioms AuditReference14.study_m_power

-- Exact type comparison: lib_m_gcd_obstruction
example : ∀ (a b m : ℤ) (h : ¬ (Int.gcd a m : ℤ) ∣ b), ¬ ∃ x : ℤ, Int.ModEq m (a * x) b := @AuditReference14.study_m_gcd_obstruction
#print axioms AuditReference14.study_m_gcd_obstruction

-- Exact type comparison: lib_m_residue_product
example : ∀ (a b m : ℕ), (a * b) % m = ((a % m) * (b % m)) % m := @AuditReference14.study_m_residue_product
#print axioms AuditReference14.study_m_residue_product

-- Exact type comparison: lib_a_trig_unit
example : ∀ (x : ℝ), (Real.sin x) ^ 2 + (Real.cos x) ^ 2 = 1 := @AuditReference14.study_a_trig_unit
#print axioms AuditReference14.study_a_trig_unit

-- Exact type comparison: lib_a_log_product
example : ∀ (x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0), Real.log (x * y) = Real.log x + Real.log y := @AuditReference14.study_a_log_product
#print axioms AuditReference14.study_a_log_product

-- Exact type comparison: lib_a_exp_add
example : ∀ (x y : ℝ), Real.exp (x + y) = Real.exp x * Real.exp y := @AuditReference14.study_a_exp_add
#print axioms AuditReference14.study_a_exp_add

-- Exact type comparison: lib_a_min_max
example : ∀ (x y : ℝ), min x y + max x y = x + y := @AuditReference14.study_a_min_max
#print axioms AuditReference14.study_a_min_max

-- Exact type comparison: lib_d_factorization
example : ∀ (a b : ℕ) (ha : a ≠ 0) (hb : b ≠ 0), (a * b).factorization = a.factorization + b.factorization := @AuditReference14.study_d_factorization
#print axioms AuditReference14.study_d_factorization

-- Exact type comparison: lib_d_totient_sum
example : ∀ (n : ℕ), (∑ d ∈ n.divisors, Nat.totient d) = n := @AuditReference14.study_d_totient_sum
#print axioms AuditReference14.study_d_totient_sum

-- Exact type comparison: lib_i_telescope
example : ∀ (f : ℕ → ℤ) (n : ℕ), (∑ i ∈ Finset.range n, (f (i + 1) - f i)) = f n - f 0 := @AuditReference14.study_i_telescope
#print axioms AuditReference14.study_i_telescope

-- Exact type comparison: lib_i_alternating_binomial
example : ∀ (n : ℕ) (hn : n ≠ 0), (∑ k ∈ Finset.range (n + 1), ((-1 : ℤ) ^ k * (n.choose k : ℤ))) = 0 := @AuditReference14.study_i_alternating_binomial
#print axioms AuditReference14.study_i_alternating_binomial

-- Exact type comparison: lib_q_integer_sqrt
example : ∀ (n : ℕ), Nat.sqrt n ^ 2 < n + 1 := @AuditReference14.study_q_integer_sqrt
#print axioms AuditReference14.study_q_integer_sqrt

-- Exact type comparison: lib_q_finite_inclusion
example : ∀ (s t : Finset ℕ) (h : s ⊆ t), s.card ≤ t.card := @AuditReference14.study_q_finite_inclusion
#print axioms AuditReference14.study_q_finite_inclusion

-- Exact type comparison: lib_q_log_tangent
example : ∀ (x : ℝ) (hx : 0 < x), Real.log x ≤ x - 1 := @AuditReference14.study_q_log_tangent
#print axioms AuditReference14.study_q_log_tangent

-- Exact type comparison: lib_m_euler
example : ∀ (a m : ℕ) (h : Nat.Coprime a m), Nat.ModEq m (a ^ Nat.totient m) 1 := @AuditReference14.study_m_euler
#print axioms AuditReference14.study_m_euler

-- Exact type comparison: lib_q_rational_density
example : ∀ (x y : ℝ) (h : x < y), ∃ q : ℚ, x < q ∧ (q : ℝ) < y := @AuditReference15.study_q_rational_density
#print axioms AuditReference15.study_q_rational_density

-- Exact type comparison: lib_i_stirling
example : ∀ (n k : ℕ), Nat.stirlingSecond (n + 1) (k + 1) = (k + 1) * Nat.stirlingSecond n (k + 1) + Nat.stirlingSecond n k := @AuditReference15.study_i_stirling
#print axioms AuditReference15.study_i_stirling

-- Exact type comparison: lib_i_catalan
example : ∀ (n : ℕ), catalan (n + 1) = ∑ i : Fin n.succ, catalan i * catalan (n - i) := @AuditReference15.study_i_catalan
#print axioms AuditReference15.study_i_catalan

-- Exact type comparison: lib_q_rearrangement
example : ∀ (a b c d : ℝ) (hab : a ≤ b) (hcd : c ≤ d), a * d + b * c ≤ a * c + b * d := @AuditReference15.study_q_rearrangement
#print axioms AuditReference15.study_q_rearrangement

-- Exact type comparison: lib_q_pigeonhole
example : ∀ (s t : Finset ℕ) (f : ℕ → ℕ) (h : t.card < s.card) (hm : ∀ x ∈ s, f x ∈ t), ∃ x ∈ s, ∃ y ∈ s, x ≠ y ∧ f x = f y := @AuditReference15.study_q_pigeonhole
#print axioms AuditReference15.study_q_pigeonhole

-- Exact type comparison: lib_d_prime_factor_exists
example : ∀ (n : ℕ) (hn : 2 ≤ n), ∃ p : ℕ, p.Prime ∧ p ∣ n := @AuditReference15.study_d_prime_factor_exists
#print axioms AuditReference15.study_d_prime_factor_exists

-- Exact type comparison: lib_d_euclidean_gcd
example : ∀ (m n : ℕ), Nat.gcd m n = Nat.gcd (n % m) m := @AuditReference15.study_d_euclidean_gcd
#print axioms AuditReference15.study_d_euclidean_gcd

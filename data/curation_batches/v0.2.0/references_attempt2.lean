import Mathlib
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
  simpa only [Finset.sum_antidiagonal_eq_sum_range_succ_mk] using Nat.add_choose_eq m n k
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


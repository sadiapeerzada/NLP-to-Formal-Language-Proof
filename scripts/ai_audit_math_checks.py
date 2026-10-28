"""Bounded, manually translated mathematical probes; NOT an NL/Lean interpreter.

Every predicate below was authored by the coding AI, independently of the Phi
responses. Exact integer/rational checks and approximate transcendental checks
are distinguished. Passing a finite search is never a semantic proof.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from candidate_inventory import load_candidates
from ai_semantic_audit import digest, subject

N = tuple(range(9))
Z = tuple(range(-6, 7))
R = tuple(F(x, 2) for x in range(-6, 7))
SMALL = tuple(range(5))
P = (2, 3, 5, 7, 11, 13)


def dvd(a, b): return b == 0 if a == 0 else b % abs(a) == 0
def mod(a, m): return a if m == 0 else a % abs(m)
def eqmod(a, b, m): return mod(a, m) == mod(b, m)
def tsub(a, b): return max(0, a-b)
def ndiv(a, b): return a // b if b else 0
def choose(n, k): return math.comb(n, k) if 0 <= k <= n else 0
def prime(n): return n >= 2 and all(n % d for d in range(2, math.isqrt(n)+1))
def phi(n): return sum(math.gcd(k, n) == 1 for k in range(n))
def fib(n):
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a
@lru_cache(None)
def stirling(n,k):
    if n == 0: return int(k == 0)
    if k == 0: return 0
    return k*stirling(n-1,k)+stirling(n-1,k-1)
def catalan(n): return choose(2*n,n)//(n+1)
def factorization(n):
    out={};p=2
    while p*p <= n:
        while n%p == 0: out[p]=out.get(p,0)+1;n//=p
        p+=1
    if n>1:out[n]=out.get(n,0)+1
    return out


def specifications():
    specs={}
    def add(ids, variables, predicate, note, *, assumptions=lambda *x:True, approximate=False):
        for ident in ids.split():
            if ident in specs: raise ValueError('Duplicate probe')
            specs[ident]=(variables,predicate,assumptions,note,approximate)
    add('arith_001', [N,N], lambda a,b:(a+b)**2==a*a+2*a*b+b*b, 'Polynomial identity on all pairs 0..8.')
    add('arith_002', [N,N], lambda a,b:tsub(a*a,b*b)==(a+b)*tsub(a,b), 'Natural subtraction; b<=a only.', assumptions=lambda a,b:b<=a)
    add('arith_003 arith_003_mathlib', [N,N,N], lambda a,b,c:a*(b+c)==a*b+a*c, 'Same distributivity predicate exposes duplicate semantics.')
    add('arith_004', [N,N], lambda a,b:tsub(a,b)**2+2*a*b==a*a+b*b, 'Truncation under b<=a.', assumptions=lambda a,b:b<=a)
    add('arith_005', [N], lambda n:choose(n,0)==1 and choose(n,n)==1, 'Both conjuncts at n=0 included.')
    add('div_001',[N],lambda n:(n*n)%2==0,'Conditional even square.',assumptions=lambda n:n%2==0)
    add('div_002',[N],lambda n:n*(n+1)%2==0,'Consecutive product.')
    add('div_003',[N],lambda n:dvd(2,n) and dvd(3,n),'Both divisors; zero included.',assumptions=lambda n:dvd(6,n))
    add('div_004',[N,N],lambda a,b:(a+b)%2==0,'Odd inputs existential witnesses reduce to parity.',assumptions=lambda a,b:a%2==b%2==1)
    add('div_005',[N],lambda n:n*n%2==1,'Odd-square witnesses exist.',assumptions=lambda n:n%2==1)
    add('div_006',[N],lambda n:(n*n%2==0)==(n%2==0),'Biconditional, both directions.')
    add('div_007',[Z,Z],lambda a,b:(a+b)%2==0,'Negative even integers included.',assumptions=lambda a,b:a%2==b%2==0)
    add('div_008',[Z],lambda n:(n%2==0)==(3*n%2==0),'Biconditional over negative and positive integers.')
    add('div_009',[Z],lambda n:(n**3-n)%2==0,'Integer subtraction.')
    add('div_010',[Z,Z,Z],lambda a,b,c:dvd(a,b*c),'Divisor zero included.',assumptions=lambda a,b,c:dvd(a,b))
    add('div_011',[Z,Z,Z],lambda a,b,c:dvd(a,b+c) and dvd(a,b-c),'Integer sum and difference.',assumptions=lambda a,b,c:dvd(a,b) and dvd(a,c))
    def dioph(x,y):
        k=(y-2)//3
        return (6*x+10*y==32)==((y-2)%3==0 and x==2-5*k and y==2+3*k)
    add('div_012',[Z,Z],dioph,'Eliminate integer existential with exact forced witness (y-2)/3; no bounded existential approximation.')
    add('ineq_001',[N],lambda n:n<=n*n,'Zero and one equality endpoints.')
    add('ineq_002',[N,N],lambda a,b:a*b+1<=(a+1)*(b+1),'Both zero endpoints.')
    add('ineq_003',[N],lambda n:n+1<=2**n,'Only n>=1 accepted by theorem.',assumptions=lambda n:n>=1)
    add('ineq_004',[N],lambda n:n+3<n+7,'Proposition only; proof-method request is not checked.')
    add('mod_001',[Z,Z,tuple(range(1,7))],lambda a,b,m:eqmod(a+1,b+1,m),'NL-positive moduli only; omitted restriction separately flagged.',assumptions=lambda a,b,m:eqmod(a,b,m))
    add('mod_002',[Z],lambda a:mod(a*a,4) in (0,1),'Negative integers included.')
    add('mod_003',[N],lambda n:mod(n*n,3) in (0,1),'Natural remainder.')
    add('mod_004',[tuple(range(-3,4))]*4+[tuple(range(1,5))],lambda a,b,c,d,n:eqmod(a+c,b+d,n),'Positive modulus; both input congruences.',assumptions=lambda a,b,c,d,n:eqmod(a,b,n) and eqmod(c,d,n))
    add('mod_005',[N],lambda n:dvd(6,tsub(7**n,1)),'n=0 yields zero; 7^n>=1 makes Nat/Int subtraction agree.')
    add('mod_006',[tuple(range(1,65))],lambda n:(not eqmod(16,25,n) or n<=9) and eqmod(16,25,9),'Check all positive moduli 1..64 and explicit witness nine; finite, not maximality proof.')
    add('ind_001',[N],lambda n:2*sum(range(n+1))==n*(n+1),'Chosen interpretation is 1 through n, NOT proof that ambiguous English has this meaning.')
    add('ind_002',[N],lambda n:sum(2*i+1 for i in range(n))==n*n,'Exactly n odd summands; empty sum n=0.')
    add('ind_003',[N],lambda n:n<2**n,'Strict inequality n=0.')
    add('ind_004',[N],lambda n:sum(2**k for k in range(n))+1==2**n and sum(2**k for k in range(n))==tsub(2**n,1),'Recursive geomSum interpreted as finite sum, compare +1 and truncated-subtraction forms.')
    add('ind_005',[N],lambda n:sum(choose(n,k) for k in range(n+1))==2**n,'Inclusive upper endpoint.')
    add('ind_006',[tuple(range(28,201))],lambda n:any((n-5*x)>=0 and (n-5*x)%8==0 for x in range(n//5+1)),'Complete nonnegative witness search for each n from 28 through 200.')
    add('ind_007',[N],lambda n:sum(k*k for k in range(n+1))==n*(n+1)*(2*n+1)//6,'Zero adds nothing; integer numerator divisible by six.')
    add('ind_008',[tuple(range(1,129))],lambda n:sum(2**k for k in range(n.bit_length()) if (n>>k)&1)==n,'Construct actual distinct-power Finset witness from binary digits; singleton covers first disjunct.')
    add('ind_009',[N],lambda n:sum(choose(4+k,k) for k in range(n+1))==choose(5+n,n),'Hockey-stick orientation with both endpoints.')
    add('lib_a_power_add',[SMALL]*3,lambda a,m,n:a**(m+n)==a**m*a**n,'Includes 0^0=1.')
    def euclidean(a,b):
        rem=mod(a,b);quot=(a-rem)//b if b else 0
        return rem+b*quot==a
    add('lib_a_euclidean',[Z,Z],euclidean,'Lean Euclidean remainder nonnegative for nonzero negative divisors; /0=0,%0=a.')
    add('lib_a_choose_symmetry',[N,N],lambda n,k:choose(n,k)==choose(n,n-k),'k<=n; truncated subtraction then ordinary.',assumptions=lambda n,k:k<=n)
    add('lib_a_abs_product',[R,R],lambda x,y:abs(x*y)==abs(x)*abs(y),'Exact rational grid as a subset of reals.')
    add('lib_a_sqrt_square',[R],lambda x:abs(math.sqrt(float(x))**2-float(x))<1e-12,'Floating approximation, x>=0 only; not exact real verification.',assumptions=lambda x:x>=0,approximate=True)
    add('lib_a_truncated_sub',[N,N],lambda a,b:tsub(a,b)+b==a,'b<=a required.',assumptions=lambda a,b:b<=a)
    add('lib_a_inverse_difference',[R,R],lambda x,y:1/x-1/y==(y-x)/(x*y),'Exact rational reciprocal; zeros excluded.',assumptions=lambda x,y:x!=0 and y!=0)
    add('lib_a_gcd_lcm',[N,N],lambda a,b:math.gcd(a,b)*math.lcm(a,b)==a*b,'Includes (0,0).')
    add('lib_d_euclid',[P,N,N],lambda p,a,b:dvd(p,a*b)==(dvd(p,a) or dvd(p,b)),'Prime-domain sample, iff and disjunction.')
    add('lib_d_unbounded_primes',[N],lambda n:any(prime(p) for p in range(n,max(3,2*n+2))),'Complete witness search in stated finite interval for each n; not infinitude proof.')
    add('lib_d_bezout',[Z,Z],lambda a,b:any(a*x+b*y==math.gcd(a,b) for x in range(-12,13) for y in range(-12,13)),'Witness search bounded -12..12; absent witness would be inconclusive, not a mathematical counterexample.')
    add('lib_d_coprime_successor',[N],lambda n:math.gcd(n,n+1)==1,'Zero included.')
    add('lib_d_prime_factorial',[P,N],lambda p,n:dvd(p,math.factorial(n))==(p<=n),'n=0 factorial one.')
    add('lib_d_mersenne_gcd',[SMALL]*3,lambda a,b,c:math.gcd(tsub(a**b,1),tsub(a**c,1))==tsub(a**math.gcd(b,c),1),'a=0 and zero exponents use Nat truncation, not integer -1.')
    add('lib_d_prime_parity',[P],lambda p:p==2 or p%2==1,'Odd primality conclusion only for actual primes.')
    add('lib_d_dvd_antisymmetry',[N,N],lambda a,b:a==b,'Two divisibility assumptions.',assumptions=lambda a,b:dvd(a,b) and dvd(b,a))
    add('lib_d_coprime_power',[SMALL,SMALL,tuple(range(1,6))],lambda a,b,n:(math.gcd(a**n,b)==1)==(math.gcd(a,b)==1),'Positive exponent; n=0 excluded.')
    add('lib_d_frobenius',[N,N,tuple(range(1,6)),tuple(range(1,6))],lambda m,n,a,b:m*a+n*b!=m*n,'Nonzero a,b and coprimality; m or n may be zero.',assumptions=lambda m,n,a,b:math.gcd(m,n)==1)
    add('lib_i_factorial',[N],lambda n:math.factorial(n+1)==(n+1)*math.factorial(n),'Zero endpoint.')
    add('lib_i_fibonacci',[N],lambda n:fib(n+2)==fib(n)+fib(n+1),'F0=0,F1=1 exact recursive computation.')
    add('lib_i_bernoulli',[R,N],lambda x,n:1+n*x<=(1+x)**n,'Exact rational real subset; x>=-1.',assumptions=lambda x,n:x>=-1)
    add('lib_i_vandermonde',[N]*3,lambda m,n,k:choose(m+n,k)==sum(choose(m,i)*choose(n,k-i) for i in range(k+1)),'Out-of-range binomial terms are zero.')
    add('lib_i_fermat_product',[tuple(range(7))],lambda n:math.prod(2**(2**k)+1 for k in range(n))==tsub(2**(2**n)+1,2),'Empty product at n=0 and natural subtraction.')
    add('lib_q_amgm',[R,R],lambda x,y:2*x*y<=x*x+y*y,'No nonnegativity assumption required.')
    add('lib_q_cauchy',[tuple(F(x) for x in range(-2,3))]*4,lambda a,b,c,d:(a*c+b*d)**2<=(a*a+b*b)*(c*c+d*d),'Exact rational vectors, including zero.')
    add('lib_q_triangle',[R,R],lambda x,y:abs(x+y)<=abs(x)+abs(y),'Absolute values, no sign assumptions.')
    add('lib_q_reciprocal',[R,R],lambda x,y:1/y<=1/x,'0<x<=y ensures both denominators nonzero.',assumptions=lambda x,y:0<x<=y)
    def nat_log(b,n):
        if b<=1:return 0
        k=0
        while b**(k+1)<=n:k+=1
        return k
    add('lib_q_log',[N,tuple(range(1,17))],lambda b,n:b**nat_log(b,n)<=n,'Totalized Nat.log bases zero/one yield zero, including 0^0.')
    add('lib_q_sqrt_monotone',[R,R],lambda x,y:math.sqrt(max(0,float(x)))<=math.sqrt(max(0,float(y)))+1e-12,'Totalized sqrt negative input ->zero; floating approximation.',assumptions=lambda x,y:x<=y,approximate=True)
    add('lib_q_exp_tangent',[R],lambda x:float(x)+1<=math.exp(float(x))+1e-12,'Floating exponential grid only.',approximate=True)
    add('lib_q_sine',[R],lambda x:math.sin(float(x))<=float(x)+1e-12,'Nonnegative x, floating sine grid.',assumptions=lambda x:x>=0,approximate=True)
    add('lib_q_quotient',[N,N],lambda m,n:ndiv(m,n)<=m,'Nat /0=0 included.')
    def crt(a,b,n,m):
        bound=max(a,b,math.lcm(n,m),1)
        return any(eqmod(k,a,n) and eqmod(k,b,m) for k in range(bound+1))
    add('lib_m_crt',[SMALL]*4,crt,'Enumerated witnesses include equality constraints for modulus zero; covers finite input grid.',assumptions=lambda a,b,n,m:eqmod(a,b,math.gcd(n,m)))
    add('lib_m_cancel',[tuple(range(1,8)),N,N,N],lambda m,c,a,b:eqmod(a,b,m//math.gcd(m,c)),'m positive makes gcd nonzero.',assumptions=lambda m,c,a,b:eqmod(c*a,c*b,m))
    add('lib_m_canonical',[N,N,N],lambda m,a,b:a==b,'m=0 has no accepted a,b; strict representative bounds.',assumptions=lambda m,a,b:a<m and b<m and eqmod(a,b,m))
    add('lib_m_fermat',[P,Z],lambda p,a:eqmod(a**p,a,p),'Integer negative bases, prime modulus.')
    add('lib_m_wilson',[P],lambda p:eqmod(math.factorial(p-1),-1,p),'ZMod equality interpreted as integer congruence.')
    add('lib_m_power',[Z,Z,Z,SMALL],lambda a,b,m,n:eqmod(a**n,b**n,m),'All integer moduli including zero; natural exponent.',assumptions=lambda a,b,m,n:eqmod(a,b,m))
    add('lib_m_gcd_obstruction',[Z,Z,Z],lambda a,b,m:all(not eqmod(a*x,b,m) for x in range(-20,21)),'Bounded x counterexample search, not proof of universal nonexistence.',assumptions=lambda a,b,m:not dvd(math.gcd(a,m),b))
    add('lib_m_residue_product',[N,N,N],lambda a,b,m:mod(a*b,m)==mod(mod(a,m)*mod(b,m),m),'Modulus zero remainder identity.')
    add('lib_a_trig_unit',[R],lambda x:abs(math.sin(float(x))**2+math.cos(float(x))**2-1)<1e-12,'Floating approximation only.',approximate=True)
    add('lib_a_log_product',[R,R],lambda x,y:abs(math.log(abs(float(x*y)))-math.log(abs(float(x)))-math.log(abs(float(y))))<1e-12,'Mathlib totalized log uses absolute value; nonzero inputs; floating.',assumptions=lambda x,y:x!=0 and y!=0,approximate=True)
    add('lib_a_exp_add',[R,R],lambda x,y:abs(math.exp(float(x+y))-math.exp(float(x))*math.exp(float(y)))<=1e-10,'Floating approximation only.',approximate=True)
    add('lib_a_min_max',[R,R],lambda x,y:min(x,y)+max(x,y)==x+y,'Exact rational grid.')
    def fac(a,b):
        fa,fb=factorization(a),factorization(b)
        return factorization(a*b)=={p:fa.get(p,0)+fb.get(p,0) for p in fa.keys()|fb.keys()}
    add('lib_d_factorization',[tuple(range(1,17))]*2,fac,'Nonzero naturals; compare complete prime-exponent dictionaries.')
    add('lib_d_totient_sum',[N],lambda n:sum(phi(d) for d in range(1,n+1) if dvd(d,n))==n,'Zero uses empty positive divisor set explicitly.')
    add('lib_i_telescope',[tuple(product((-1,0,1),repeat=5)),tuple(range(5))],lambda f,n:sum(f[i+1]-f[i] for i in range(n))==f[n]-f[0],'All 3^5 sampled function vectors and prefixes, integer subtraction.')
    add('lib_i_alternating_binomial',[tuple(range(1,17))],lambda n:sum((-1)**k*choose(n,k) for k in range(n+1))==0,'Positive n only; n=0 would fail.')
    add('lib_q_integer_sqrt',[tuple(range(129))],lambda n:math.isqrt(n)**2<n+1,'Exact integer square root.')
    subsets=tuple(frozenset(s) for k in range(5) for s in combinations(range(4),k))
    add('lib_q_finite_inclusion',[subsets,subsets],lambda s,t:len(s)<=len(t),'All subsets of {0,1,2,3}.',assumptions=lambda s,t:s<=t)
    add('lib_q_log_tangent',[R],lambda x:math.log(float(x))<=float(x)-1+1e-12,'Positive inputs, floating log.',assumptions=lambda x:x>0,approximate=True)
    add('lib_m_euler',[N,N],lambda a,m:eqmod(a**phi(m),1,m),'Coprime restriction and totalized modulus zero.',assumptions=lambda a,m:math.gcd(a,m)==1)
    add('lib_q_rational_density',[R,R],lambda x,y:x<(x+y)/2<y,'Construct rational midpoint for rational real-input subset; not density proof for all reals.',assumptions=lambda x,y:x<y)
    add('lib_i_stirling',[N,N],lambda n,k:stirling(n+1,k+1)==(k+1)*stirling(n,k+1)+stirling(n,k),'Exact recursive Stirling computation; may mirror definition.')
    add('lib_i_catalan',[N],lambda n:catalan(n+1)==sum(catalan(i)*catalan(n-i) for i in range(n+1)),'Closed-form Catalan implementation vs convolution.')
    add('lib_q_rearrangement',[tuple(F(x) for x in range(-2,3))]*4,lambda a,b,c,d:a*d+b*c<=a*c+b*d,'Ordering hypotheses orient inequality.',assumptions=lambda a,b,c,d:a<=b and c<=d)
    def pigeon(s,t,f):return any(x!=y and f[x]==f[y] for x in s for y in s)
    add('lib_q_pigeonhole',[subsets,subsets,tuple(product(range(4),repeat=4))],pigeon,'All maps on {0,1,2,3} and all subsets; finite complete universe only.',assumptions=lambda s,t,f:len(t)<len(s) and all(f[x] in t for x in s))
    add('lib_d_prime_factor_exists',[tuple(range(2,129))],lambda n:any(prime(p) and dvd(p,n) for p in range(2,n+1)),'Exhaustive possible prime divisor witnesses for each n.')
    add('lib_d_euclidean_gcd',[N,N],lambda m,n:math.gcd(m,n)==math.gcd(mod(n,m),m),'Zero modulus totalization.')
    return specs


def run(output):
    rows=load_candidates(ROOT);specs=specifications()
    if set(specs)!={r['id'] for r in rows}:raise ValueError('Probe coverage does not match candidate IDs')
    output.mkdir(parents=True,exist_ok=False);results=[]
    for r in rows:
        domains,predicate,assumptions,note,approx=specs[r['id']]
        checked=skipped=0;failures=[]
        for args in product(*domains):
            if not assumptions(*args):skipped+=1;continue
            checked+=1
            if not predicate(*args):failures.append([str(a) for a in args])
        if not checked:raise ValueError('Vacuous grid: '+r['id'])
        results.append({'candidate_id':r['id'],'subject_sha256':digest(subject(r)),
            'kind':'approximate_numeric_probe' if approx else 'exact_bounded_probe',
            'checked_assignments':checked,'filtered_by_assumptions':skipped,
            'failures':failures,'note':note,
            'status':'bounded_counterexample_or_missing_witness' if failures else 'no_counterexample_in_stated_grid',
            'scope':'Manually AI-translated proposition checks, not automatic English parsing or Lean evaluation; no unbounded semantic certification.'})
    result={'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'python_version':sys.version,'candidate_count':len(rows),
            'checked_assignments':sum(r['checked_assignments'] for r in results),'results':results}
    (output/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Checked',len(rows),'candidate predicates;',result['checked_assignments'],'assignments;',sum(bool(r['failures']) for r in results),'with failures.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    run(p.parse_args().output)

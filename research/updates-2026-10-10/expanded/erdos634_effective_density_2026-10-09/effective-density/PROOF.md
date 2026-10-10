# Effective density in every square class, and a positive-density obstruction

**Research directed by Denis Paliy, with ChatGPT assistance. 9 October 2026.**

Status: a new written deduction from the specified existing classification and
constructive-tail inputs. Exact arithmetic regression tests accompany the proof.
No external referee, independently staffed proof review, formal verification, or
priority claim is asserted. This note does not decide every individual tile count.
It does not attack F3/14430, beta-92, or the small W/beta scales.

## 0. Main result

Let S be the positive integers N for which some nondegenerate triangle is a
union of N congruent nondegenerate triangular tiles with disjoint interiors.
Reflections and arbitrary T-junctions are allowed. For a positive squarefree d,
put

\[
 M_d=\{m\geq1:dm^2\in S\}.
\]

**Theorem.** Using the classification and constructive results specified below:

1. The natural density
   \[
   \rho_d=\lim_{X\to\infty}\frac{\#(M_d\cap[1,X])}{X}
   \]
   exists for every d. It is a computable real, uniformly in the input d: a
   terminating finite algorithm gives a rational interval of any prescribed
   positive rational width containing rho_d. The algorithm does not require
   an elliptic-curve rank, a Mordell–Weil basis, or decisions of the unresolved
   small geometric scales. No useful complexity bound is claimed.
2. If d is odd then rho_d=1. If d is even, then
   \[
   \rho_d=(1+\delta_d)/2\geq1/2,
   \]
   where delta_d is the natural density of the admissible odd multipliers,
   relative to all odd positive integers.
3. The following are equivalent:
   \[
   \boxed{\rho_d=1
     \quad\Longleftrightarrow\quad M_d\text{ is cofinite}
     \quad\Longleftrightarrow\quad \mathsf T(d).}
   \]
   Here T(d) is the existing finite cofinal-class arithmetic test recalled
   below. In particular, if it fails, the impossible multipliers have
   **positive natural density**, not merely infinitely many examples.
4. The full arithmetic divisibility envelope and the known constructive
   tails disagree on an effectively density-zero set of multipliers.
   This is an almost-all statement within each fixed square class, not
   an exact membership criterion for every multiplier.

The cofinal test T(d) itself is an earlier repository result. The additions
here are the all-branch effective density, a rank-free explicit tail bound,
and the positive-density strengthening of non-cofiniteness.

A square class is sparse in the integers N. Densities in this note concern
multipliers m, or equivalently counts in that one class normalized by
sqrt(Z/d) for N<=Z. They are not densities among all positive integers N.

## 1. Exact prior inputs and provenance

The repository was read at main tree/commit
`3a0ad269f645850ed9fd01bbd76a08c9b456032e`.
All the following paths refer to `DenisUkranian/erdos-634-tilings` at that
snapshot; historical statements about individual counts retain their dated
scope and are not used to override later results.

**G1. Exhaustive classification and integral residual scales.** The classical
families are squares, sums of two squares, twice a square, three times a
square, and six times a square. After them, the thirteen necessary rows are
those in `docs/global-gap-2026-10-07.md` and
`research/uniform-reduction/PROOF.md`, with a primitive coefficient D and
an integer residual scale t, so N=D t^2. Their published angular/rationality
inputs are recorded in those sources. The classifications are used, not
reproved in this note.

**G2. Fixed-tile constructive tails.** Every one of the nine product rows in
Section 3 has a computable every-integer tail in its residual scale. Use
`docs/square-class-tails.md`, Appendix A, for the norm-family transfers,
`research/general-spectra/PROOF.md` for the equilateral cores, and
`docs/universal-rational-scales.md` with `docs/explicit-theta-seeds.md`
for alpha. The QP row is positive at every scale by
`docs/two-piece-construction.md`. Harries, Zhang, Laczkovich, and Beeson
retain the construction attributions given in those notes.

Only eventual existence is required here, not the sharp threshold or a
converse to a particular macro dissection. For each finite witness list we
can select any one of its certified computable sufficient thresholds.

**G3. Easy cofinal classes.** Define

\[
 C_0(d): d\in\{1,2,3,6\}\text{ or every odd prime dividing }d
                    \text{ is }1\pmod4,
\]
\[
 C_W(d): \text{every odd prime dividing }d\text{ is }1\text{ or }7\pmod8,
\]

and C_B(d) by: every prime p>3 dividing d is 1 or 11 modulo 12, and

\[
 d\equiv2\pmod3\quad(3\nmid d),\qquad
 d/3\equiv1\pmod3\quad(3\mid d).
\]

The W/beta square-class saturation result in
`research/square-class-saturation/PROOF.md`, as recorded in
`docs/square-class-tails.md`, supplies a computable all-multiplier tail
whenever C_W or C_B holds, with its stated classical exceptions already
covered by C_0. This is not the unaccepted candidate all-primes proof.

Every fixed odd d has a theta tail: for d>1 take u=(d-1)/2, v=(d+1)/2,
so v^2-u^2=d. For even d, take u=d-1, v=d+1, giving the primitive theta
coefficient 4d and hence every sufficiently large **even** multiplier in
M_d. Kernel 1 is classical. These are G2 and
`docs/universal-rational-scales.md`, Section 7.

**Comparison with the earlier result.**
`research/final-synthesis-oct7/F3_FIXED_CLASS_DENSITY.md` established a
stronger rate for F3 in a fixed class using elliptic heights, but did not
compute its height/lattice constants. It did not establish the all-branch,
rank-free effective theorem proved here. We do not improve its F3 exponent
1/3; our elementary coefficient bound is weaker but explicitly effective
and simultaneously applicable to every product row.

**External algebraic input.** We use unique factorization of ideals in
quadratic number fields, prime splitting and ideal norms. A primary
reference inspected for this note is J. S. Milne, *Algebraic Number Theory*,
v3.08 (2020), Sections 3 and 4, especially the ideal-factorization theorem
and Propositions 4.1–4.2; the real-quadratic unit discussion is in Section 5.
https://www.jmilne.org/math/CourseNotes/ANT.pdf
The small unit-gap inequalities used below are proved directly.

## 2. Why nine product rows suffice in the non-cofinal odd sector

It remains to treat even squarefree d for which C_0,C_W,C_B all fail.
Consider an odd multiplier m and an actual tiling of d m^2.

A representation N=D t^2 with t integer forces

\[
 t\mid m,\qquad D=d s^2,\qquad s=m/t\in\mathbb Z_{>0}.
\tag{2.1}
\]

For example, this follows prime by prime from v_p(D)+2v_p(t)=v_p(d)+2v_p(m)
and v_p(d) in {0,1}: v_p(t)<=v_p(m). Both s and t are odd.

The classical rows are impossible when C_0 fails. A primitive W
coefficient 2v^2-u^2 containing a prime p|d would imply (2/p)=1 for each
odd p|d, so C_W is necessary. A primitive beta coefficient 3v^2-u^2
similarly implies (3/p)=1 for p>3 dividing d. Its 3-adic valuation, if
positive, is exactly one. Reducing the remaining part modulo 3 gives
precisely the displayed additional C_B condition. Thus neither W nor
beta can occur in this case.

Both difference-of-squares rows have D=v^2-u^2 with gcd(u,v)=1. This D is
odd when u,v have opposite parity, and is divisible by 8 when both are
odd. It never has 2-adic valuation one. But d s^2 has that valuation
because d is even squarefree and s is odd. These two rows cannot occur.

The remaining possibilities are exactly the nine product rows below.
This reduction does not require any new small-scale geometric theorem.

## 3. The complete arithmetic coefficient list

For Group 1 write

\[
 b_0=v^2-u^2,\quad Q=2v^2-u^2,\quad P=3v^2-u^2,
 \qquad 0<u<v,\quad\gcd(u,v)=1.
\]

The norm rows have positive a,b,c with gcd(a,b)=1 and the indicated norm.
Both orders of a,b are included. The classical equilateral (1,1,1) in the
minus norm is harmless; it cannot contribute an even kernel.

| Row | D | Norm/parameter condition |
|---|---:|---|
| alpha | b_0 Q | Group 1 |
| QP | QP | Group 1 |
| E60 | ab | c^2=a^2-ab+b^2 |
| E120 | ab | c^2=a^2+ab+b^2 |
| F1 | b(a+b) | plus norm |
| I120 | b(a+2b) | plus norm |
| F2 | (a+2b)(2a+b) | plus norm |
| F3 | 3(a+b)(a+2b) | plus norm |
| F4 | (a+b)(2a+b) | plus norm |

Let B_d be the set of odd positive integers s for which at least one row
has an exact primitive coefficient D=d s^2. Put

\[
 A_d=\{m\ge1:m\text{ odd and }s\mid m\text{ for some }s\in B_d\}.
\]

For each s, its witness list is finite and computable by factoring d s^2.
For completeness, the inverse formula for alpha from D=b_0 Q is
v^2=Q-b_0, u^2=Q-2b_0; for QP it is v^2=P-Q, u^2=2P-3Q. For the
norm rows test divisors and recover a,b from the linear factors. For F3
factor D/3 rather than D. The executable `inverse_witnesses` gives all
nine exact inverse tests, not a bounded search over arbitrary tile sizes.

For each s in B_d, select a sufficient every-integer tail threshold t_s
from one of its witnesses using G2. Define

\[
 C_d=\{m\text{ odd}: s\mid m,\ m/s\ge t_s
                          \text{ for some }s\in B_d\}.
\]

Writing F_d for the actual admissible odd multipliers, Sections 1–2 give

\[
 C_d\subseteq F_d\subseteq A_d.                         \tag{3.1}
\]

The only new task is to control the infinite coefficient list. In
particular, passing the coefficient test at residual scale one has NOT
been identified with existence of a tiling.

## 4. A small-factor counting lemma with explicit constants

Write tau(n) for the number of positive divisors of n.

### Lemma 4.1: ideals and a compact Pell sector

In a quadratic number field, the number of integral ideals of norm n is
at most tau(n). Indeed, for each p^e exactly e+1 choices are possible if p
splits, at most one if it is inert, and one if it ramifies. Multiply these
bounds, using unique ideal factorization. This does not assume class number
one or unique factorization of elements.

For integers 0<u<v, the number of solutions of 2v^2-u^2=L, with L fixed,
is at most tau(L). Associate u+v sqrt(2), which has norm -L, to its
principal ideal of norm L. Its positive real value, divided by sqrt(L),
lies in (1,1+sqrt(2)). Two elements generating the same ideal and having
this same norm differ by a positive unit of norm one. The smallest such
unit greater than one in Z[sqrt(2)] is 3+2sqrt(2). To see the needed gap
directly, a unit x+y sqrt(2)>1 of norm one has x,y positive integers;
y=1 is impossible in x^2-2y^2=1, and y>=2 gives x+y sqrt(2)>=3+2sqrt(2).
The interval ratio is smaller, so it contains at most one such generator.

Likewise, the number of 3v^2-u^2=L in 0<u<v is at most tau(L): now
(u+v sqrt(3))/sqrt(L) lies in
(1,(1+sqrt(3))/sqrt(2)), whose ratio is less than 2+sqrt(3), the smallest
positive norm-one unit greater than one in Z[sqrt(3)]. These are the full
rings of integers of the two fields. This last gap follows already from
y>=1 in x^2-3y^2=1.

### Lemma 4.2: fixing one factor of any row

After removing the displayed factor 3 from F3, each row's two factors
L_1,L_2 are coprime. For F2 a possible common divisor divides 3; but
3|a+2b and 3|2a+b would imply a=b nonzero modulo 3, and then the norm is
3 modulo 9, not a square. This excludes that exception.

For **either** of the two factors of **any** row, fixing its value L
leaves at most

\[
                  2\tau(3L^2)                           \tag{4.1}
\]

positive ordered primitive parameter witnesses. Here are all the cases,
with bounds that even allow nonprimitive parameters.

* Fixing b_0=v^2-u^2 leaves at most tau(L) possibilities by
  (v-u)(v+u)=L. Fixing Q or P has the same bound by Lemma 4.1.
* Fix a short side B of a plus or minus norm, and write A for the other.
  The identities
  \[
  (2c-2A-B)(2c+2A+B)=3B^2\quad(+),
  \]
  \[
  (2c-2A+B)(2c+2A-B)=3B^2\quad(-)
  \]
  have positive integral factors; each factor pair determines A,c
  uniquely. Thus at most tau(3B^2) possibilities occur, even when A is
  much larger than B. This covers both equilateral rows and the b factor
  in F1 and I120.
* Fix L=a+b in the plus norm. Set z=a-b. Then
  \[
     4c^2-z^2=3L^2,\qquad |z|<L,
  \]
  and hence
  \[
     (2c-z)(2c+z)=3L^2.
  \]
  Both factors are positive integers. Each ordered divisor pair recovers
  c and z, and then a=(L+z)/2 and b=(L-z)/2, uniquely. There are thus
  at most tau(3L^2) ordered pairs. This factorization also covers z<0;
  it does not discard the opposite short-side ordering.
* Fix L=a+2b. Then 4c^2-3a^2=L^2 and 0<a<L. The corresponding interval
  for (2c+a sqrt(3))/L is (1,2+sqrt(3)), containing at most one generator
  per ideal. The bound is tau(L^2). Fixing 2a+b is the same argument
  with a and b exchanged.

These exhaust every linear or quadratic factor in the table. Each bound
is at most (4.1). No unproved uniform bound for integral elliptic points
or non-elementary estimate for Pell solutions has been substituted.

### Lemma 4.3: the coefficient-counting estimate

For positive squarefree d put

\[
 h=\frac{3d}{\gcd(3,d)^2},\qquad
 \mathfrak c_d=32\tau(d)\tau(3d^2)+4\tau(h)\tau(3h^2).
\tag{4.2}
\]

Then for every real K>=1,

\[
 \boxed{\#\{s\in B_d:s\le K\}
 \le\mathfrak c_d\sqrt K\left(1+\tfrac12\log K\right)^4.}
\tag{4.3}
\]

The same bound holds for the number of ordered primitive witnesses,
counting the row as part of the witness. It in fact bounds even as well
as odd s; oddness is simply discarded for the estimate.

**Proof.** First take one of the eight rows without the factor 3. Its
coprime factors satisfy L_1 L_2=d s^2. Squarefreeness and coprimality give
uniquely

\[
 L_1=d_1 x^2,\quad L_2=d_2 y^2,\quad d_1d_2=d,\quad xy=s.
\]

There are tau(d) ordered squarefree allocations. If s<=K, either x or y
is at most sqrt(K). Fix that smaller variable z and which side it came
from. Lemma 4.2 bounds the witnesses by

\[
 2\tau(3(d_i z^2)^2)
 \le 2\tau(3d^2)\tau(z^4).
\]

Counting both choices of the smaller side, including any overcount,
gives at most

\[
 4\tau(d)\tau(3d^2)\sum_{z\le\sqrt K}\tau(z^4)
\]

witnesses for that row. The inequality tau(AB)<=tau(A)tau(B) does not
require coprimality of A,B.

For F3, when 3|d remove the factor 3 to get L_1 L_2=(d/3)s^2. When
3 does not divide d, the equality 3L_1 L_2=d s^2 forces 3|s; writing
s=3k gives L_1 L_2=3d k^2. Thus the corresponding squarefree kernel
is always h in (4.2), and the new multiplier k is at most s<=K.
The same bound with h therefore handles F3, including all cases
where 3 divides d or s.

Finally tau(z^4)<=d_5(z), the five-fold divisor function. On a prime
power this is 4e+1<=binomial(e+4,4). Counting ordered products of five
positive integers shows, for Z>=1,

\[
 \sum_{z\le Z}d_5(z)
 \le Z\left(\sum_{n\le Z}\frac1n\right)^4
 \le Z(1+\log Z)^4.
\]

Sum the eight row bounds and the F3 bound, and set Z=sqrt(K).
This proves (4.3). QED.

## 5. Explicit reciprocal tail and a density algorithm

Define L_K=1+(log K)/2 and

\[
 P_4(L)=L^4+4L^3+12L^2+24L+24.
\]

Partial summation of (4.3), dropping its nonpositive endpoint term,
gives the fully explicit bound

\[
 \boxed{\sum_{\substack{s\in B_d\\s>K}}\frac1s
 \le E_d(K):=\frac{2\mathfrak c_d}{\sqrt K}P_4(L_K).}
\tag{5.1}
\]

Indeed the integral to bound is
mathfrak_c_d times the integral from K to infinity of
`t^(-3/2)(1+log(t)/2)^4`. Substituting u=sqrt(t) and integrating four
times gives exactly (5.1). Its right side tends to zero effectively.

Let B_d(K) contain the odd coefficient multipliers at most K. The finite
union of odd multiples of these generators is periodic. Its relative
odd density is the rational number

\[
 \delta_d(K)=\sum_{\varnothing\ne J\subseteq B_d(K)}
             \frac{(-1)^{|J|+1}}{\operatorname{lcm}(J)},
\tag{5.2}
\]

with value zero for an empty set. Generators divisible by a smaller
retained generator can be removed before inclusion–exclusion.

**Existence and explicit error.** The natural odd-relative density of
A_d exists and obeys

\[
              0\le\delta_d-\delta_d(K)\le E_d(K).
\tag{5.3}
\]

For clarity about normalization, a uniform counting bound through X
for multiples of generators beyond K is X times their reciprocal sum.
To get the sharper constant one, rather than two, for odd-relative
*limiting density*, first truncate that tail at a finite J. Its density
is at most sum_{K<s<=J}1/s. The remaining upper odd-relative density
is at most 2 sum_{s>J}1/s by the uniform bound. Let J tend to infinity
and use (5.1). The bound tends to sum_{s>K}1/s. Then let K grow to
obtain existence and (5.3).

**Equality with the geometric density.** Fix K. For each s<=K, the
multiples not yet covered by its selected tail t_s form a finite set.
Consequently A_d\C_d has upper odd-relative density at most E_d(K).
Letting K tend to infinity and applying (3.1) proves that A_d,C_d,F_d
all have density delta_d. The actual geometric density, not just the
necessary arithmetic density, therefore obeys (5.3).

**A terminating algorithm with rational error bounds.** First test the
odd kernel and the three easy conditions. If one holds, rho_d=1.
Otherwise factor d and compute mathfrak_c_d. Choose an integer j>=0
with

\[
 \frac{2\mathfrak c_d}{2^j}P_4(1+j)<\epsilon.
\tag{5.4}
\]

This is an exact rational test and eventually succeeds. Take K=2^(2j).
Because log(2)<1, (5.4) bounds E_d(K). Enumerate the finite coefficient
list B_d(K), compute (5.2), and use the interval

\[
 [\delta_d(K),\ \min(1,\delta_d(K)+E)]
\]

for the odd density. Convert to the interval with endpoints
(1+lower)/2 and (1+upper)/2 for rho_d. Both endpoints are rational if
the rational bound in (5.4) is used as E. Testing B_d(1) first is a
useful shortcut: its nonemptiness also gives rho_d=1.

This algorithm can be astronomically slow. The theorem proves
computability, not a practically sharp numerical error bar. The script
reports finite lower approximations honestly; an empty finite list is
not an infinite exclusion. No accurate numerical value of delta_38 is
claimed in this package.

**Effective sparse geometric disagreement.** This can also be made into
a uniform finite-X statement after specifying a finite list of tail
thresholds. Let

\[
 A_0(K)=\sum_{s\in B_d(K)}\max(0,t_s-1).
\]

For all X>=1,

\[
 \#((A_d\setminus C_d)\cap[1,X])
 \le A_0(K)+X E_d(K).                                  \tag{5.5}
\]

Choose K with E_d(K)<=epsilon/2 and then X>=2 A_0(K)/epsilon.
The right side is at most epsilon X. All choices are computable from
the prior explicit constructive tails. For an odd-relative bound divide
by ceil(X/2), or replace epsilon by half the desired tolerance.
The fixed initial exceptions in the easy classes and in the even sector
are handled by their fixed constructive thresholds. This proves part 4
of the theorem without solving those exceptions individually.

## 6. Failure of the cofinal test leaves positive-density impossible counts

The earlier cofinal test is

\[
 \mathsf T(d):\quad d\text{ odd},\quad\text{or}\quad
 C_0(d)\lor C_W(d)\lor C_B(d)\lor\mathcal P(d),
\tag{6.1}
\]

where P(d) means that one of the nine product rows has exact coefficient
d. In the non-easy even case this is exactly 1 in B_d. It is a finite
factor-and-square test, not a test of geometric existence at scale one.

When T(d) holds, the already specified constructive inputs give a fixed
all-multiplier tail. Thus M_d is cofinite and rho_d=1.

Suppose T(d) fails. Then d is even, none of the easy conditions holds,
and every generator in B_d is odd and at least 3. We prove that the
complement of A_d has positive odd-relative density.

For any finite set B of odd integers at least 3, CRT gives

\[
 \operatorname{dens}_{\rm odd}(\{m:b\nmid m\text{ for every }b\in B\})
 \ge\prod_{b\in B}(1-1/b).                            \tag{6.2}
\]

Here is a proof, including the correlation issue. Under the limiting
CRT distribution, the finitely many relevant prime valuations are
independent geometric variables; cap each valuation at the largest
exponent needed by B. The indicator of b not dividing m is decreasing
in each valuation. For two decreasing functions of one variable,
nonnegative covariance follows from
`2 Cov(f(Z),g(Z)) = E[(f(Z)-f(Z'))(g(Z)-g(Z'))] >= 0`,
where Z' is an independent copy. Induction over independent coordinates
gives the same positive-correlation inequality for functions decreasing
in every coordinate. A product of such nonnegative indicators is again
decreasing, so induction over B proves (6.2). Thus independence of the
different divisibility events is NOT falsely assumed.

Apply (6.2) to B_d(K) and let K tend to infinity. By (5.1) and (5.3),

\[
 1-\delta_d\ge\prod_{s\in B_d}(1-1/s)>0.               \tag{6.3}
\]

The product is positive because sum 1/s converges and s>=3. More
explicitly, `-log(1-1/s) <= 3/(2s)` gives

\[
 1-\delta_d\ge\exp\left(-\tfrac32\sum_{s\in B_d}1/s\right).
\tag{6.4}
\]

Even the very coarse explicit constant from (5.1) at K=1 is enough:
P_4(1)=65 and 1 is absent, so the reciprocal sum is at most
130 mathfrak_c_d. Therefore

\[
 1-\delta_d\ge e^{-195\mathfrak c_d},\qquad
 1-\rho_d\ge\tfrac12 e^{-195\mathfrak c_d}>0.           \tag{6.5}
\]

The tiny bound is not intended for numerical estimation. It proves an
explicit positive gap from density one. In particular rho_d=1 cannot
occur without T(d), establishing the equivalence in part 3.

The outside-of-envelope multipliers are already impossible by the
exhaustive necessity result G1; the positive-density obstruction is not
an inference that the unresolved inside-of-envelope multipliers fail.

## 7. What this closes, and what it leaves open

This settles the following independent all-class questions within the
stated input framework:

* Does the density within every square class exist? **Yes.**
* Is it effectively approximable without a complete elliptic basis or
  a solution of every small-scale tiling question? **Yes**, with (5.1).
* Can a square class have density one but infinitely many impossible
  multipliers? **No.** Density one is exactly the existing finite
  cofinal criterion; every other class has a positive-density obstruction.

These are global-in-the-branches statements for every fixed d. The
nine-row counting lemma includes alpha, both equilateral rows, F1,
I120, F2, F3, F4, and QP, rather than treating F3 in isolation. The
four other nonclassical rows are eliminated or supplied with a full
cofinal tail in Section 2. No extrapolation from 38 or from finite
computer tests is used.

It does not follow that every arithmetic coefficient is positive at
scale one, that all small scales are classified, or that a finite fixed
list of congruences gives exact membership. The repository already
contains examples that prohibit such conclusions. In particular,
cofinality and density one for class 154 do not overturn the later
negative result for N=154 itself. The occupied F3/14430 and W/beta
geometric problems remain separate.

## 8. Reproduction and limits of verification

Run, without Python optimization:

```sh
python check_density.py --limit 3000 --output verification.json
```

The standard-library checker:

1. independently compares forward coefficient formulas with the finite
   divisor inverses for all nine rows on the stated parameter boxes;
2. checks coprimality and both versions of the F3 factor-3 normalization;
3. completely enumerates all witnesses for each fixed factor L<=300
   for the seven cases in Lemma 4.2, including the unbalanced fixed-side
   cases via their divisor identities rather than a box cutoff;
4. checks the divisor majorant and exact CRT densities/correlation
   lower bounds on finite samples;
5. lists all primitive odd coefficient multipliers up to the specified K
   in the chosen classes, with exact witnesses and finite rational density.

These computations check arithmetic implementation and identities. They
are not a proof of infinite ideal factorization, do not verify all the
external geometric constructions afresh, and do not certify any new
small-count tiling or negative geometric decision. The universal result
is the written argument above with its explicitly identified inputs.

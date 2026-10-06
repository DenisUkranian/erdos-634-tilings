# Independent internal audit of the global fixed-split-part reduction

6 October 2026. This is a separate mathematical review within the project,
not external refereeing, formal verification, or a priority claim.

**Conclusion:** [`GLOBAL_FIXED_SPLIT_PART.md`](GLOBAL_FIXED_SPLIT_PART.md)
is sound under its stated prior exhaustive classification, rationality,
integral-scale, and constructive-tail inputs. The assumptions that d is
even squarefree and m is odd are essential to the branch reduction.

## Classification and the prime support

The prime classes greater than 3 which split for 2 are 1,7,17,23 modulo
24; those which split for 3 are 1,11,13,23. Their union omits exactly
5 and 19. Thus the unrestricted complementary support is precisely
the prime 3 together with these two classes.

Squarefreeness of d in `dm²=Dt²` gives `t|m` and `D=ds²`, where
`s=m/t` is odd and divides m. In particular `v_2(D)=1`.

The classification has thirteen nonclassical rows. Exactly the five
rows removed in Section 2 are incompatible with that valuation:

* For either difference-of-squares coefficient `v²-u²`, opposite
  parities give an odd number; two odd primitive parameters give a
  multiple of 8.
* For either norm `c²=a²±ab+b²`, if a is even and b odd, then c is
  odd and `c²-b²=a(a±b)` is divisible by 8. Its second factor is odd,
  so `8|a`. The argument is symmetric. Hence an even equilateral
  coefficient ab is divisible by 8.
* In the plus norm, two odd sides satisfy `ab=7 mod 8`, hence
  `a+b=0 mod 8`. Together with the preceding even-side observation,
  this makes `b(a+b)` odd or divisible by 8. Thus F1 also cannot
  have valuation one.

The eight remaining rows in the theorem are therefore exhaustive,
including both orders of the norm-tile parameters.

## Bounds for the primitive list

For `Q=2v²-u²`, an odd prime divisor forces 2 to be a quadratic
residue because gcd(u,v)=1. In particular 3 cannot divide Q.
If Q is even, u is even and v odd, so its 2-adic valuation is one.
Since Q divides each coefficient in W, alpha, and QP, its prime powers
are bounded by those in `dH²`. Also `v²<Q`, giving the claimed finite
parameter bound.

For `P=3v²-u²`, every prime divisor greater than 3 splits for 3.
If 3 divides P, write u=3z; then v is prime to 3 and
`P=3(v²-3z²)` has 3-adic valuation exactly one. In the beta row
`P=ds²` and s is odd, so 3 does not divide s; every other prime of s
belongs to H's support. Thus `P|dH²` and `2v²<P`. The factor 3
which may occur in P is supplied by the squarefree kernel, not an
unbounded power from m/H.

For the norm factors `U=a+2b` and `V=2a+b`, divisibility by 3
would give a=b modulo 3 and a primitive norm equal to 3 modulo 9,
which is impossible. At primes greater than 3, their norm reductions
are respectively `c²=3b²` and `c²=3a²`, with nonzero denominator.
Only primes splitting for 3 can therefore divide U or V. Their
2-parts are bounded by `v_2(D)=1`. Since the relevant factor divides
D, the asserted divisibility by `dH²` follows directly. No assignment
of every prime to a coprime factor is needed in this argument.

Consequently the coarse parameter boxes in Section 4 contain every
possible nonclassical witness. Filtering by an odd integral square
`D/d=s²` and `H(s)|H` preserves every s which could divide a
multiplier in the chosen sector. Keeping extra witnesses does not
invalidate either necessity or the positive tail test.

## Classical cases, thresholds, and empty lists

For a fixed squarefree even d, a square multiplier cannot change
whether a prime 3 modulo 4 has odd exponent. Thus the sum-of-two-
squares condition depends only on d. The exceptional classical
twice-square and six-times-square forms add precisely d=2 and d=6.
Perfect-square and three-times-square forms have odd squarefree
kernels and cannot occur here. This verifies the stated classical
flag and its independence from m.

Every remaining branch has an explicitly computable positive threshold:

* W and beta have the universal rational-scale threshold, and the
  subsequent cap construction can also give a smaller safe value.
* Alpha uses `ceil(C_theta/v)`. The theta seed is explicitly
  computable in both signs of its parameter Delta by
  `docs/explicit-theta-seeds.md`; Delta=0 is excluded there. This
  dependency is therefore effective, not an unspecified existence
  constant. The two annulus thresholds can both be used safely;
  the displayed H_u is at least H_v.
* QP has threshold 1 by its full positive construction.
* The four norm thresholds are exactly those in Appendix A of
  `docs/square-class-tails.md`: `3(floor(R)+2)` for isosceles and
  F4, and its half rounded up for F2 and F3. These positive transfers
  retain their stated Harries/Zhang attribution.

Taking `C=max({1} union {sT})` over the finite list is computable.
If m>=C and a listed s divides m, its integer residual multiplier
m/s is at least its sufficient threshold T. Conversely, every actual
nonclassical tiling has a listed divisor. This proves the eventual
equivalence. If the nonclassical list is empty and the classical flag
fails, necessity excludes every multiplier in the sector; C=1 is
well defined and introduces no exceptional case.

For each fixed d,H there are finitely many positive integers below C,
hence finitely many geometric decisions not answered by the tail
criterion. The previously proved exact fixed-count procedure makes
these decisions computable in principle. This audit does not claim
they were executed.

There is no bound uniform over growing H, no full classification of
all multipliers, and no conclusion for even m from this theorem.
An eventual finite divisor list with an ordinary size cutoff also
does not imply a finite exact basis under divisibility.

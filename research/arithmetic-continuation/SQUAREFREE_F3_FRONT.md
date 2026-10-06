# Infinitely many squarefree candidates confined to primitive F3 geometry

6 October 2026. This is an arithmetic family of necessary coefficient
candidates, **not a family of asserted tilings or non-tilings**. Its
purpose is to identify precisely what coefficient replacement and
existing large-scale constructions cannot settle by themselves.

The only geometric classification input is the prior F3 isolation
theorem in `docs/f3-global-overlap.md`, Theorem 1.1. The newly certified
positive 990-tiling shows that primitive F3 tilings can exist. No
universal scale-one impossibility statement is made here.

## 1. The family

For a positive integer h satisfying `h=5 mod 24`, put

    a=h²−1, b=2h+1, c=h²+h+1,
    q=h²+4h+1,
    D(h)=3h(h+2)q.                                   (1)

**Theorem.** Infinitely many h in this progression have squarefree
D(h). Every such D(h) has a positive primitive F3 coefficient witness.
If D(h) is an actual tiling count, then every classified realization
must belong to F3 and must have residual multiplier exactly one.

More precisely, the number of these squarefree candidates at most Y is

    ~ delta/(24*3^(1/4)) * Y^(1/4),                  (2)

where the positive convergent product is

    delta = product_{p>=5 prime} (1−(3+(3/p))/p²).    (3)

The Legendre symbol `(3/p)` appears in (3). Formula (2) counts
arithmetic candidates, not realizable tiling counts.

## 2. Primitive norm, branch isolation and the forced scale

Direct expansion gives `c²=a²+ab+b²`. All three sides are positive,
and a>b because h>=5. The identity

    4a=(2h−1)b−3

shows that gcd(a,b) divides 3. But h=2 mod 3 implies b=2 mod 3, so
the tile is primitive. Its F3 coefficient is

    3(a+2b)(a+b)=3q*h(h+2)=D(h).

The integers h,h+2,q are pairwise coprime. Indeed their possible
common divisors divide 2, 1 and 3 respectively; h,h+2 are odd and
h+2=1 mod 3. None of these three factors is divisible by 3, while
q=14 mod 16 when h=5 mod 8. Hence v_2(q)=1 and v_3(D)=1.

Reducing (1) modulo 16 gives

    D(h)=14 mod 16.

Also h=5 mod 8 gives the Jacobi symbol `(2/h)=-1`. Therefore at
least one prime p dividing h has odd valuation and `(2/p)=-1`.
This prime is not 3, since h=2 mod 3, and it divides neither h+2
nor q. Its valuation in D remains odd. The prior isolation theorem
therefore forces every realization of D into F3.

When D is squarefree, the integral necessary spectrum `D=D_0 t²`
forces t=1. This remains true if one replaces the original tile by
a different primitive tile: the conclusion uses squarefreeness of
the count itself. Thus no same-count change of tile can move this
family to a constructive residual scale greater than one.

## 3. Positive density of squarefree parameters

The factors h,h+2,q are pairwise coprime; 2 and 3 have already been
controlled. Consequently D is squarefree exactly when no prime p>=5
has its square dividing any of the three factors.

For p>=5, the two linear factors each give one forbidden residue
modulo p². The quadratic q has discriminant 12, so its number of
roots modulo p² is `1+(3/p)`: distinct roots modulo p lift uniquely,
and p does not divide the discriminant. The roots of the three
factors are disjoint modulo p, by the gcd computations in Section 2.
Their total forbidden-residue count is therefore

    rho(p)=3+(3/p), in {2,4}.                        (4)

Fix z>=5. The Chinese remainder theorem shows that the number of
h<=X, h=5 mod 24, avoiding all such squares at p<=z is

    X/24 * product_{5<=p<=z}(1−rho(p)/p²) + O_z(1). (5)

The factors in this product are positive. Since
`sum_p rho(p)/p²` converges, their infinite product delta exists and
is strictly positive.

It remains to control primes beyond z uniformly. For
`z<p<=sqrt(X+2)`, the root count gives at most

    O(X sum_{p>z} 1/p² + sqrt X)
      = O(X/z+sqrt X)                               (6)

bad parameters. Using all h rather than just the progression is a
valid upper bound.

For `p>sqrt(X+2)`, neither h nor h+2 can be divisible by p².
Only q can contribute. Since

    0<q(h)<(h+2)²<=(X+2)²,

such a prime is at most X+2. For each p there are at most two roots
modulo p²; and X<p², so the entire interval 1<=h<=X contains at
most two of them. The elementary Chebyshev prime-counting bound
therefore gives a total of

    O(pi(X+2))=O(X/log X)=o(X).                      (7)

Combining (5)–(7), first letting X tend to infinity with z fixed
and then letting z tend to infinity, proves

    #{h<=X: h=5 mod24, D(h) squarefree} ~ delta X/24. (8)

This is a written squarefree-sieve proof, not a density inferred
from a finite sample. Finally D(h) is strictly increasing for h>0
and `D(h)~3h⁴`, so (8) gives (2).

## 4. Examples and the fixed-H distinction

The first two examples are

| h | Tile (a,b,c) | Squarefree coefficient D |
| --- | --- | --- |
| 5 | (24,11,31) | 4830=2·3·5·7·23 |
| 29 | (840,59,871) | 2583726=2·3·29·31·479 |

The theorem does not declare either coefficient realizable or
unrealizable. In particular, the previously unresolved 4830 is the
first member of this arithmetic family, rather than an isolated
numerical accident.

For every squarefree D in this family, write the full count in the
global square-class notation as `N=d m²` with d=D, m=1. Then the
split part H(m) in `GLOBAL_FIXED_SPLIT_PART.md` is already 1.
Thus eliminating growth of H alone would not close the complete
problem: an infinite primitive geometric front remains through
growth of d, even when H is fixed at its smallest possible value.

The finite regression `check_squarefree_f3_front.py` checks the
displayed algebra, prime allocation, factorization and sample
squarefreeness. It is supplementary to the proof of infinitude,
not a substitute for it. External novelty and referee acceptance
are not asserted.

# Global reduction with a fixed split part and unrestricted nonsplit support

6 October 2026. This theorem reduces infinitely many tile counts to a
finite primitive list and a finite small remainder. It does not determine
that remainder, or give a finite list valid for all split parts. It uses
the existing exhaustive angular classification, primitive integer
normalization and integral residual scales, and the established
every-integer fixed-tile construction tails. No new geometric
construction or all-integer solution is claimed.

## 1. Statement

Let d be a positive **even squarefree** integer. For odd m define

    H(m) = product_{p | m, p>3, p not =5,19 mod 24} p^{v_p(m)}.

These are exactly the primes which split in at least one of
`Q(sqrt(2))` and `Q(sqrt(3))`. The complementary part m/H(m) is supported
on

    P_0 = {3} union {p prime: p=5 or 19 mod 24}.       (1)

It may contain arbitrarily many distinct primes and arbitrary exponents.

**Theorem.** Given d and a positive odd integer H whose prime divisors
belong to the defining support of H(m), one can compute a finite list
of primitive tile/branch witnesses L(d,H). Associate to each witness
its exact coefficient `D=d s²` and a computable sufficient multiplier
threshold T. Set

    C(d,H)=max({1} union {sT: witnesses in L(d,H)}).  (2)

Unless the classical condition below holds, every odd m with H(m)=H
has the following properties:

1. If `dm²` is realizable, then some listed s divides m.
2. If a listed s divides m and `m/s>=T` for its witness, then `dm²`
   is realizable.
3. Consequently, for `m>=C(d,H)`,

       dm² is realizable iff some listed s divides m. (3)

If the list is empty, no such multiplier is realizable at any size.
Below C(d,H) only finitely many positive integers remain; their
geometric decisions are not supplied by the theorem. Thus an exact
classification of this entire fixed-H sector requires only finitely
many additional fixed-count geometric decisions.

The classical condition is

    d in {2,6}, or every odd prime divisor of d is 1 mod 4. (4)

When (4) holds, every multiplier is already realizable by the classical
twice-square, six-times-square, or sum-of-two-squares constructions,
so no list or remainder is needed. If (4) fails, no odd multiplier can
occur in a classical branch: multiplying by a square changes none of
the odd valuations of the squarefree kernel.

The difference from the fixed-prime-support theorem in
`docs/fixed-prime-support.md` is that (1) permits **unbounded and
unrestricted support inside two prime residue classes**. Neither an
S-unit equation solver nor an elliptic-rank computation is used.

## 2. Integral spectra and the eight surviving rows

Use the exhaustive classification and rationality/normalization inputs
recorded in `research/uniform-reduction/PROOF.md` and
`research/uniform-sectors/PROOF.md`. Beyond the classical cases, every
actual count has a primitive integer coefficient and a positive
integer residual multiplier:

    dm²=D t².

Squarefreeness of d gives `t|m`, so

    D=d s², s=m/t, s|m.                              (5)

Because m and t are odd, `v_2(D)=1`.

For coprime `0<u<v`, set

    b=v²−u², Q=2v²−u², P=3v²−u².

Both difference-of-squares rows are absent: a primitive difference
`v²−u²` is odd if u,v have opposite parity, and is divisible by 8
if both are odd. It never has 2-adic valuation one.

For a primitive norm tile `c²=a²±ab+b²`, an even short side is
divisible by 8. If both sides are odd, the plus norm forces
`a+b=0 mod 8`, while the minus norm has ab odd. Therefore neither
equilateral coefficient ab has valuation one. Neither does the
plus-norm F1 coefficient `b(a+b)`: when one side is even the product
is odd or divisible by 8; when both are odd their sum is divisible
by 8. No assumption about the magnitude of the residual scale is
used in these exclusions.

Exactly eight nonclassical rows remain as possible rows (not assertions
that all eight occur for a given d):

| Row | Exact coefficient D | Bounded factor or parameter |
| --- | --- | --- |
| W | Q | Q |
| Beta-isosceles | P | P |
| Group-1 alpha | bQ | Q |
| Group-1 QP | QP | Q |
| 120-degree isosceles | b(a+2b) | U=a+2b |
| F2 | (a+2b)(2a+b) | U=a+2b |
| F3 | 3(a+2b)(a+b) | U=a+2b |
| F4 | (2a+b)(a+b) | V=2a+b |

All norm rows in this table have `c²=a²+ab+b²`, `a,b>0` and
`gcd(a,b)=1`. Both orders of a,b are retained.

## 3. Bounds depending only on d and H

Put B=dH². Every primitive witness to (5) in a surviving row obeys
the following bounds, independent of m/H and its prime support.

### Group 1

An odd prime p dividing Q has `(2/p)=1`: otherwise reduction of
`2v²−u²=0 mod p` forces p to divide both u and v. In particular
3 does not divide Q. The exponent at 2 is at most one: if Q is
even, u is even and v is odd, giving Q=2 mod 4.

In each of the W, alpha and QP rows, Q divides D. By (5), every
prime-power factor of Q divides dH²: all its odd primes occur in
H's allowed support, and its exponent is bounded by
`v_p(d)+2v_p(m)=v_p(d)+2v_p(H)`. Thus

    Q | B,  v²<Q<=B.                                (6)

For the beta row, an odd p>3 dividing P has `(3/p)=1`, by the same
primitive reduction argument. Moreover `v_3(P)<=1`: if 3 divides P,
then u=3z, 3 does not divide v, and

    P/3=v²−3z²=1 mod 3.

Since d is squarefree, (5) forces 3 not to divide its coefficient
multiplier s. All other prime factors of s belong to H's support.
Consequently

    P=d s² | B,  2v²<P<=B.                          (7)

One may therefore enumerate every potentially relevant Group-1 tile
using just coprime `0<u<v` and `v²<=B`. This is a finite safe bound;
the sharper strict inequalities in (6)–(7) are not needed by the
enumerator.

### The four norm rows

For a primitive plus-norm triple put U=a+2b and V=2a+b. Neither U
nor V is divisible by 3: such divisibility gives a=b mod 3, and
primitivity then makes the norm 3 mod 9, impossible for c².

If p>3 divides U, the norm equation becomes `c²=3b² mod p`, with
b,c units, so `(3/p)=1`. Similarly p dividing V forces `(3/p)=1`
using `c²=3a² mod p`. Thus neither factor contains any prime from
P_0. In each row the displayed factor U or V divides D. Its full
prime-power valuations are bounded by those of dH² from (5),
including the exponent at 2, since `v_2(D)=1`.

It follows that

    U | B in the isosceles, F2 and F3 rows;
    V | B in the F4 row.                             (8)

In particular `1<=a,b<=B` is a safe simultaneous bound on every
primitive norm witness. The coefficient may still contain primes
from P_0 in its other factor. This does not affect finiteness:
both tile parameters have already been bounded by (8).

The allocation arguments only use divisibility of the indicated
factor into D. They do not require an unproved assignment of every
prime to one coprime factor. Primitivity is used in the local norm
exclusions, and the integer residual scale is used in (5).

## 4. The finite list and constructive threshold

An explicit, deliberately coarse algorithm is as follows.

1. Handle the classical condition (4).
2. Set B=dH². Enumerate coprime `0<u<v`, `v²<=B`, and compute the
   four Group-1 coefficients in the table.
3. Enumerate `1<=a,b<=B`, `gcd(a,b)=1`; retain the pairs for which
   `a²+ab+b²` is a square. Compute the four norm coefficients.
4. Retain a row exactly when `D/d` is an odd positive integer
   square s² and `H(s)|H`. Keep the row, tile and s. Duplicates
   may be removed or retained.
5. Assign each retained witness its already proved every-integer
   sufficient threshold T. Compute C by (2).

Step 4 removes coefficient multipliers that can divide no m in
the sector; it does not assume realization at coefficient scale
one. The finite list is an overlist of actual primitive witnesses,
which is sufficient for necessity and the tail criterion.

The existing thresholds are explicit or effectively computable:

* W and beta use the universal rational-scale construction;
  alpha uses its theta-to-alpha transfer and the computable theta
  seed. Both are recorded in `docs/universal-rational-scales.md`
  and `docs/explicit-theta-seeds.md`.
* QP is constructive at every positive integer scale, so T=1.
* Isosceles and F4 use `3(floor(R)+2)`, with
  `R=max(a,b)/min(a,b)`; F2 and F3 use half this bound rounded up.
  These old positive transfers are recorded, with their
  Harries/Zhang attribution, in `docs/square-class-tails.md`,
  Appendix A.

Any actual tiling has a witness on the list by Sections 2–3, and
its s divides m by (5). Conversely, a listed s dividing m gives
an integer residual scale m/s; if that scale is at least T, the
existing construction realizes exactly `d s²(m/s)²=dm²` tiles.
For m>=C, every listed divisor has this property, proving (3).

## 5. Scope of the remaining finite decisions

For fixed d,H, only the finitely many odd m<C with H(m)=H remain
outside the arithmetic equivalence. If one invokes the prior
fixed-count decision procedure (or the separately proved exact
disk-certificate enumeration), their truth values can in principle
be computed. No such general campaign is implemented or claimed
here. The important reduction is the bound **uniform over all
prime supports in P_0**, not a search that stops after observing
no further examples.

There is no uniform bound over H in this theorem. The class-38
infinite-antichain result is compatible with it: positive multipliers
can have different split parts. A finite eventual list with a size
cutoff also does not imply a finite exact divisibility-minimal seed
list when the support is infinite.

The statement concerns positive even squarefree kernels and odd
multipliers only. Even multipliers allow the two difference-of-squares
rows and require a separate argument. No claim for that sector is
made here.

## 6. Read-only scoped classifier

The companion CLI prints its finite witness list and cutoff C:

```sh
python research/arithmetic-continuation/classify_global_sector.py 38 3
python research/arithmetic-continuation/classify_global_sector.py 110 3
python research/arithmetic-continuation/classify_global_sector.py 110 15
```

The respective results are `NO`, `UNRESOLVED_SMALL_SCALE`, and `YES`.
It accepts only positive even squarefree d and positive odd m. It uses
the already established sufficient thresholds in
`research/square-class-tails/classify.py`; it does not write a tiling
certificate or modify files.

`NO` means that every necessary primitive witness has been excluded,
not merely that the input falls below C. `YES` supplies a classical or
constructive-tail witness. `UNRESOLVED_SMALL_SCALE` means this particular
classifier's sufficient constructions do not decide a surviving
coefficient witness. A sharper construction elsewhere can still decide
such an input; this status is not a claim of an open problem in the
literature.

The bounds are deliberately coarse, and enumeration can become
expensive as dH² grows. The tool is a reproducible implementation of
this scoped reduction, not an efficient general solver for all counts.

`check_global_sector_cli.py` checks these three outputs, the classical
case, and rejection of odd kernels, even multipliers, nonsquarefree
kernels and nonpositive inputs. Its saved report is
`global-sector-cli-verification.json`.

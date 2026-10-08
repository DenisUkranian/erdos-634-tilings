# Square class 15 cannot be replaced by W or F3

8 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
This is an exact obstruction to one proposed global overlap reduction. It
neither decides the remaining count 135 nor solves Erdős problem 634.

**Theorem.** For every positive integer m, no tiling with count `15m²`
belongs to the W branch or to the 120-degree F3 branch. Nevertheless, every
`15m²` with `m >= 4` is realizable, by the previously verified 240-tile
construction and trapezoid extension.

Consequently, W and F3 together, even supplemented by finitely many individual
counts, cannot cover the entire set of realizable counts. This does not rule
out a classification retaining other already-classified infinite sectors
alongside W and F3. In particular, it does not refute a proposed reduction of
only the *remaining uncertainty* to those branches.

## W is excluded by the prime 5

The necessary W spectrum is

    N = (2v²-u²)t²,     gcd(u,v)=1.

For `N=15m²`, the 5-adic valuation of N is odd. Hence 5 divides `2v²-u²`.
Primitivity makes v nonzero modulo 5, so 2 would be a quadratic residue
modulo 5, a contradiction. This uses only the necessary spectrum, not a
scale-one W exclusion.

## An F3 coefficient would produce a forbidden rational point

Suppose an F3 realization exists. Its necessary count has the form

    3(a+2b)(a+b)t² = 15m²,     c²=a²+ab+b²,     a,b,c,t>0.

Put `A=a+2b`, `B=a+b`, and `s=m/t`. Thus `AB=5s²`. The rational point

    x = 5b/B,       y = 5Ac/(sB)

satisfies

    y² = x³+125,       0<x<5.

Indeed `c²=B²-Bb+b²` and
`(B+b)(B²-Bb+b²)=B³+b³`. This is also the specialization at square class
15 of the [general F3 elliptic correspondence](../../../docs/elliptic-square-classes.md).
We show directly that this elliptic curve has only its identity and the
rational point `(-5,0)`.

## A complete two-isogeny descent

Replace x by `X-5`. The curve becomes

    E:  Y²=X³-15X²+75X.

Its 2-isogenous curve is

    E': Y²=X³+30X²-75X.

For a curve `y²=x³+A x²+B x`, the standard two-isogeny descent map sends a
nonexceptional point to the square class of x, the identity to 1, and `(0,0)`
to the square class of B. Its image is represented by signed squarefree
divisors d of B. Each nonexceptional class must have a solution

    w² = d u⁴ + A u²v² + (B/d)v⁴,       gcd(u,v)=1.       (1)

The two images obey

    2^rank(E) = |image(alpha_E)| |image(alpha_E')| / 4.   (2)

These are standard descent results, for example Cremona, *Algorithms for
Modular Elliptic Curves*, Chapter III, §3.6, pp.84–85, equation (3.6.2)
([author's text](https://johncremona.github.io/book/fulltext/chapter3.pdf)).
The equivalent Selmer upper bound suffices here; see Aguirre,
Lozano-Robledo and Peral, *Elliptic curves of maximal rank*, §2
([author PDF](https://alozano.clas.uconn.edu/wp-content/uploads/sites/490/2014/01/ALP-2-23-07.pdf)).
The following local calculations determine the images exactly, so no rank
oracle, unproved analytic conjecture, or search bound is used.

### The image for E is exactly {1,3}

The quadratic `X²-15X+75` is everywhere positive, so every rational point
of E has `X>=0`. The possible classes are therefore `1,3,5,15`. Both 1 and
3 occur, from the identity and `(0,0)`.

Class 5 would require

    w²=5u⁴-15u²v²+15v⁴.

Modulo 5 this forces `5|w`. After dividing by 5 and reducing modulo 5,

    u⁴-3u²v²+3v⁴ = 0 (mod 5).

If `5|v`, this also forces `5|u`, contrary to coprimality. Otherwise put
`t=(u/v)²` modulo 5. Its possibilities are `0,1,4`; none is a zero of
`t²-3t+3`. Class 5 is impossible. Since the image is a group and contains
3, class 15 is impossible as well. Hence `image(alpha_E)={1,3}`.

### The image for E' is exactly {1,-3}

The possible classes are `±1,±3,±5,±15`; the identity and `(0,0)` supply
`1,-3`. It suffices to eliminate representatives `3,5,-5` of the other
three cosets under multiplication by -3.

For d=3, equation (1) becomes

    w²=3u⁴+30u²v²-25v⁴.

Modulo 3, this forces `3|v,w`. Modulo 9 it then forces `3|u`, a
contradiction.

For d=5, equation (1) becomes

    w²=5u⁴+30u²v²-15v⁴.

As above, reduction modulo 25 reduces the question to a zero of
`t²+t+2` modulo 5 for `t in {0,1,4}`. There is none.

For d=-5, the equation is

    w²=-5u⁴+30u²v²+15v⁴.

The analogous polynomial is `-t²+t+3`, which again has no zero for
`t in {0,1,4}`. Thus `image(alpha_E')={1,-3}`.

Equation (2) gives `rank(E)=0`.

### The rational torsion is exactly of order two

For the original model `y²=x³+125`, the good reductions at 7 and 17 have
respectively 4 and 18 points. Their explicit point counts are included in
the finite checker. Prime-to-p torsion injects under good reduction at p;
using these two primes also excludes torsion at either exceptional prime.
Consequently the rational torsion order divides `gcd(4,18)=2`. The point
`(-5,0)` has order two. The complete rational group is therefore

    {O, (-5,0)}.

There is no rational point with `0<x<5`, contradicting the point obtained
from the F3 coefficient. This excludes every multiplier in square class 15.

## Constructive and overlap consequences

The earlier [class-15 construction and reduction](../../final-closure-oct8/class15/REDUCTION.md)
proves `15m²` realizable for every `m>=4`. These give infinitely many actual
counts outside both W and F3, starting with 240 and 375. They also lie
outside the classical families: their squarefree part is 15, and the
3-adic valuation is odd, preventing a sum of two squares.

Thus at least one additional nonclassical branch remains necessary in any
coverage of these actual counts. The theorem does not assert that one
particular additional branch is individually indispensable: the counts can
have alternative realizations within the remaining families.

The known rank zero of this classical elliptic curve is not claimed as a
new elliptic-curve result. The point is the explicit all-multiplier overlap
obstruction, with a short exact proof tied to the new class-15 construction.
As an external check only, the LMFDB record for Cremona 900b1 / LMFDB 900.g4
lists `[0,0,0,0,125]`, rank zero, and torsion order two
([data](https://www.lmfdb.org/EllipticCurve/Q/data/900.g)).

## Reproduction and review

Run, from the repository root:

    python3 research/universal-closure-oct8/overlap-literature/check_class15_overlap.py

The standard-library checker exhausts the four primitive local obstructions
modulo 25 or 9, verifies the descent cosets, checks the two good-reduction
point counts, and checks the W obstruction modulo 5. The mathematical argument
above supplies the passage from those finite computations to the rank and
nonexistence statements.

A separate internal mathematical review independently checked both descent
images and all four local contradictions. This is not external refereeing.

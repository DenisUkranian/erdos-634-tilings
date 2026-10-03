# Orientation reduction: proved cases and failed reductions

4 October 2026, Kyiv. Research directed by Denis Paliy, with ChatGPT assistance.
This records a continuation of the [finite-scheme investigation](finite-schemes-attack.md).
Neither the finite-scheme conjecture nor Erdős problem 634 is solved here.
The elementary arguments below were reviewed separately within this investigation;
no external acceptance or priority is asserted.

## The quantifier that must be preserved

The proposed bound concerns **some alternative tiling of the same triangular
target by the same congruent tile**, with the same tile count. A complicated
chosen tiling does not refute it. A replacement for an arbitrary polygonal
patch is a stronger auxiliary statement; refuting that statement does not
refute the triangular-target conjecture.

Two particularly tempting implications are invalid:

* A terminating collection of local rewrites need not have uniformly bounded
  irreducible configurations.
* An integer solution of boundary, area, or orientation-inventory equations
  need not describe a positive geometric tiling.

The archive already distinguishes both gaps. No termination argument or
finite computation in this continuation removes them.

## Similar pairs: at most six orientations

Use the fixed-pair statement of Beeson, *Triangle Tiling I*, Theorem 2,
printed page 25 [B1]. If the tile and target are similar, a tileable pair has
one of these alternative constructions:

| Case | Explicit alternative | Maximum rigid orientations |
|---|---|---|
| Square count | One ordinary triangular grid | 2 |
| Right tile, N=e²+f² with the specified leg ratio e/f | Two triangular grids | 4 |
| 30–60–90 tile, N=3m² | Three triangular grids | 6 |

The area fixes the scale of the target, so these are alternatives for the
same tile and target. This is a consequence of the cited classification,
not a new classification of similar tilings.

In particular, large orientation sets in pinwheel-type substitutions cannot
by themselves refute the conjecture. For the tile with legs 1 and 2 and a
similar target with N=5^k, even k has a one-grid alternative and odd k has
a two-grid alternative.

## Rational-angle tiles: at most 24 orientations

Assume the congruent-tile shape classification reproduced in Table 2 of
Beeson's *No triangle can be cut into seven congruent triangles*, printed
page 8 [B2]. It leaves similar pairs, a right tile doubled along a leg to
form an isosceles target, and an equilateral target with a 30–30–120 tile.
The similar case was just handled. Here is an independent argument for
the orientation bound in the other cases; it does not use that paper's
count table.

For the doubled right-triangle shape normalize its hypotenuse to 1, put
a=sin(alpha), b=cos(alpha), and lambda=sqrt(N/2). Choose the doubled leg
so that the target has equal sides lambda and base 2 lambda a. Boundary
edge decompositions give nonnegative integers p,q,r,s,t,u with

    lambda = p a + q b + r,
    2 lambda a = s a + t b + u.

If lambda is rational, it is an integer: lambda=h/k in lowest terms and
N=2h²/k² imply k² divides 2, hence k=1. Two ordinary grids suffice.

Suppose lambda is irrational. The determinant of these two equations for
a,b is D=pt-qs+2q lambda. If D is nonzero, both a and b belong to the real
quadratic field Q(lambda). Since alpha/pi is rational, b+i a is a root of
unity in the biquadratic field Q(lambda,i). Its order n has phi(n)<=4 and
its Galois group has exponent at most two. Orders 5 and 10 are therefore
excluded; the possible orders are 1,2,3,4,6,8,12. For an acute alpha this
leaves pi/6, pi/4, or pi/3.

If D=0, irrationality gives q=0 and pt=0. The first boundary equation
forces p>0, so t=0. Substitution gives

    -N + (s+2r)lambda - sr = -pu.

Thus s+2r=0, and nonnegativity gives s=r=0. Consequently a=lambda/p and
sin²(alpha) is rational. The rational algebraic integer 2cos(2alpha),
strictly between -2 and 2, is -1, 0, or 1. The same three angles result.

For a triangle with angles in (pi/6)Z, its three edge directions are in
one coset of (pi/6)Z. Across a positive-length edge contact, the next
tile's rotation changes by an integer multiple of pi/6, whether or not
it is reflected. The positive-length contact graph of a finite tiling of
a triangle is connected: a generic path between interior tile points
avoids the finitely many tiling vertices. Hence the entire tiling has at
most 12 rotations and 12 reflected rotations. The pi/4 case has at most
16, and the 30–30–120 tile is covered by the bound 24 as well.

Therefore every rational-angle tileable pair has an alternative with at
most 24 rigid orientations, conditional on the stated shape classification.
This does not establish a bound on the number of grid blocks.

## Irrational right tiles: at most eight orientations

The separate [right-tile argument](right-tile-orientation-bound.md) supplies
the remaining classical case. It uses the rationality and boundary statement
of [B3], Lemma 7.5, and an independent parity proof based on a directed graph
of whole hypotenuses. It does not use Theorems 7.8 or 7.10.

After normalizing the legs to coprime integers r,s, boundary arithmetic
leaves either a double-grid construction or a scale k sqrt(r²+s²)/2.
Even k gives four triangular grids. Odd k would force r,s odd and hence
N odd. Independently of rational leg ratios, the directed-edge argument
gives sqrt(N/2)=U+V exp(i alpha), with U,V Gaussian integers. Taking
norms proves that N must be even, excluding the odd-k case.

Thus every nonsimilar irrational right-tile pair has an alternative with
at most eight rigid orientations. Together with the preceding sections,
all classical branches have a bound of 24, with the listed published
dependencies. This removes the classical cases from the necessary
orientation-bound conjecture; the nonclassical cases remain.

## A restriction on orientation cuts

Partition the orientations used in a triangular tiling into two nonempty
groups A and B. Let D_A and D_B be the unions of their unoriented edge
directions. Then

    |D_A intersect D_B| >= 2.

If their intersection is empty, the connected contact graph already gives
a contradiction. If the only common direction is d, every A/B interface
is parallel to d. Every target side not parallel to d belongs wholly to
one group, since the other group has no edge in that direction.

Sum the oriented boundary vectors of the union of A tiles and project
perpendicular to d. Internal contacts cancel after subdivision, including
T-junctions. The sum of the full target-side vectors assigned to A must
therefore be parallel to d. Exactly one such side cannot have this
property. Zero such sides would leave a positive-area polygonal union
whose entire boundary is parallel to d, also impossible. Thus A needs
at least two target sides, and the same holds for B. A triangle has only
three sides, which is the contradiction.

The hypothesis concerns the unions of available directions. Merely seeing
parallel interfaces in one drawing is insufficient: an exterior side
could then alternate between the groups.

In particular, if a triangular tiling uses at most two grid classes modulo
half-turn and those classes share at most one edge direction, only one
class can occur. With just one grid class the target
has the tile's three directions; its boundary edges are integer multiples
of the corresponding tile edges. It has a one-grid alternative. Larger
orientation systems with two or more shared directions across every cut
are not excluded by this argument.

## An exact failure of arbitrary patch switching

Let a,b,c be positive integers with a!=b and c²=a²+ab+b², and put
rho=exp(i pi/3). The parallelogram

    conv{0, a, a+b rho, b rho}

is tiled by two copies of the 120-degree tile along its long diagonal
of length c. This is its only congruent two-triangle dissection. A
two-triangle dissection of a convex quadrilateral must use a diagonal;
the other diagonal has length sqrt(a²-ab+b²)<c and does not give this
tile. A T-junction cannot give a different two-triangle partition.

All boundary directions have class 0 modulo pi/3. The internal diagonal
has class theta=arg(a+b rho). The classes theta and -theta are distinct:
2cos(theta)=(2a+b)/c is rational strictly between 1 and 2, so theta/pi
cannot be rational (the rational trace of a root of unity is an integer).
Thus this patch cannot be retiled in the opposite adjacent class while
retaining its boundary and unit tile.

This refutes an arbitrary two-class polygon-patch switch. It does not
refute a switch restricted to pure inward islands, nor the existence of
bounded-orientation alternatives for triangular targets.

## Why arithmetic height alone did not finish the argument

For a primitive 120-degree norm tile put z=(a+b rho)/c and d=2a+b.
One has gcd(c,d)=1 and the primitive minimal polynomial

    f(X)=cX²-dX+c.

Gauss's lemma implies that every integer polynomial P with P(z)=0 is an
integer-polynomial multiple of f. Its first and last nonzero coefficients
are therefore divisible by c. But the relations

    f(X)(1+X+...+X^(L-2)) = 0 at X=z

have arbitrarily large span L and coefficients bounded independently of
L. Accordingly, denominator cancellation in a signed boundary relation
does not establish exponential geometric cost for high orientation levels.
A proof of such a cost would need an additional positive geometric argument.

## Remaining obligation and source caution

There is no uniform orientation bound here for the remaining nonright,
irrational-angle nonsimilar pairs, and no proof converting a finite orientation bound
into a bounded number of positive construction blocks. Exact searches of
restricted patches do not decide those universal statements.

This continuation also examined [B3], Section 7. Its printed proof of
Theorem 7.8 replaces the sine given by its preceding length equation by
a tangent and uses that replacement in a rationality argument. The
fixed-pair claim in Theorem 7.10 is therefore not used as a shortcut.
This observation is not a disproof of that theorem. The separate
right-tile proof supplies the needed parity and integrality argument,
retaining Lemma 7.5 as an explicit dependency. The inputs used are [B1],
the shape classifications identified in [B2] and [B3], and that lemma.

Sources:

* [B1] M. Beeson, [Triangle Tiling I](https://www.michaelbeeson.com/research/papers/TriangleTiling1.pdf), Theorem 2, printed p.25.
* [B2] M. Beeson, [No triangle can be cut into seven congruent triangles](https://michaelbeeson.com/research/papers/NoSevenTiling.pdf), Table 2, printed p.8, reporting Laczkovich's congruent-tile shape classification.
* [B3] M. Beeson, [Tilings of an Isosceles Triangle, v7](https://arxiv.org/html/1206.1974v7), Section 7. Accessed 3 October 2026 UTC.

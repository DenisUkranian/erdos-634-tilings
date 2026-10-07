# A reflected-corner quadrilateral needs at least five similar triangles

7 October 2026. A geometric limitation of small dissection recipes, not a
nonexistence theorem for a full F3 tiling.

Let `(a,b,c)` be a primitive positive integral triple with
`c²=a²+ab+b²`, `a>b`, and a even. Let R be its 120-degree triangle. In
Eisenstein coordinates set

```
n=a-b,
Q=[(an,0),(c²,0),(a²,ab),(an,bn)].
```

**Theorem.** Q has no dissection into at most four triangles similar to
R, even allowing different positive real scales, reflections, and
T-junctions.

The key uniform arithmetic statement is completely elementary. The
extension from rational to real scales uses the rationalization lemma
proved below.

## 1. Geometry and parity

The quadrilateral Q is the c-fold R triangle with its reflected n-fold
corner removed. Its tile area and four successive side lengths are

```
area(Q)/area(R)=c²-n²=3ab,
b(2a+b), bc, bc, bn.
```

Primitivity implies b,c odd. Since c²=b²=1 modulo 8, the norm identity
gives `a(a+b)=0 (mod 8)`. The factor a+b is odd, hence `8|a`. Thus
`8|3ab`, and all four side lengths of Q are odd integers.

## 2. No integer grid dissection at any integer multiplier

Suppose mQ, for a positive integer m, is tiled by r integer-scaled R
triangles with positive scales `k_i`, where `r<=4`. Area yields

```
k_1²+...+k_r²=3ab m².                       (1)
```

A sum of at most four integer squares divisible by 8 has all the bases
even. Indeed an odd base contributes 1 modulo 8, while an even base
contributes 0 or4; with between one and four odd bases the total cannot
be 0 modulo 8.

Write `m=2^s m_0` with m_0 odd. The right side of (1) is divisible by
`2^(2s+3)`. Apply the preceding observation s+1 times, dividing the
square identity by 4 after each of the first s applications. It follows
that every k_i is divisible by `2^(s+1)`.

Every side of each macrotriangle is consequently an integer multiple of
`2^(s+1)`. Each exterior side of convex mQ is a concatenation of whole
macrotriangle sides, also in the presence of T-junctions: a side lying
on a supporting boundary line cannot extend outside that boundary
segment. Hence its length is divisible by `2^(s+1)`. But all exterior
side lengths of mQ are m times odd integers, so their 2-adic valuation
is exactly s. This is a contradiction.

In particular Q has no dissection into at most four rationally scaled
R triangles: clear a common denominator of their scales and apply the
statement just proved to an integer multiplier of Q.

## 3. Rationalization for this setting

We prove the following lemma.

**Lemma.** If Q has a finite dissection into triangles similar to R at
positive real scales, then Q has a dissection with the same number of
triangles, the same relative orientations and incidences, and positive
rational scales.

All reference vertices of R and Q have rational Eisenstein coordinates,
and all their side lengths are rational. The reference unit vectors
along their sides therefore have rational Eisenstein coordinates.
Reflection acts rationally in this basis:
`conjugate(x+y*rho)=(x+y)-y*rho`.

The adjacency graph obtained by joining two tiles sharing a segment of
positive length is connected. To see this, join two interior points by
a polygonal path inside Q that avoids the finitely many tile vertices;
it crosses from one tile to the next through positive-length edge
contacts. Start with a tile having a boundary side. Its orientation
matrix has rational entries in the Eisenstein basis, because its side
unit direction is aligned with a rational boundary unit direction.
Across an adjacency contact, alignment of the two side directions
expresses the second orientation as the first followed by a rotation
or reflection with rational matrix entries. Induction through this
connected graph proves that every orientation matrix is rational.

Fix these orientation matrices and the complete incidence structure of
the given dissection, subdividing sides at all T-junctions and any other
vertices. Introduce two translation variables and one scale variable
for every tile, together with coordinates for every incidence vertex.
The conditions that a corner vertex is the appropriate translated,
scaled reference corner are linear equations with rational coefficients.
The condition that an incidence vertex lies on a fixed-direction tile
side is also linear with rational coefficients. Its distance along that
side may be introduced as a separate variable, avoiding products of
unknowns. Impose the ordered strict inequalities between successive
incidence vertices on every side, and impose positive tile scales.
On the outer boundary, impose the analogous linear incidences with the
fixed sides and corners of Q, in their prescribed order.

This is a finite rational linear system with strict rational linear
inequalities. It has the original real solution. Gaussian elimination
parametrizes its affine solution space over Q, and rational values of
the free variables are dense in the real values. Thus it has a rational
solution satisfying all the strict inequalities. All new scales are
positive and rational.

For completeness, these data really give a dissection. They realize the
same abstract subdivided disk. Each underlying triangular face remains
a similar triangle with its positive boundary orientation; its moving
T-junction vertices retain their order. A parameterization of the
subdivided face may be piecewise linear rather than one similarity.
The outer boundary maps once, in order, onto the simple boundary of Q.
Subdivision order prevents collapsed atomic edges. For a point away
from all developed edges, the
winding number of the developed boundary equals the sum of the winding
numbers of the individual face boundaries: internal edges cancel in
opposite pairs. Each positively oriented face contributes either 0 or1.
The outer boundary contributes 1 inside Q and 0 outside. Thus every such
interior point is covered exactly once, and every such exterior point
is covered zero times. Closure gives the entire dissection, with no
interior overlap. This proves the lemma.

Apply the lemma to a hypothetical at-most-four-piece real dissection,
then clear denominators and contradict Section 2. The theorem follows.

## 4. Scope

For `(a,b,c)=(24,11,31)`, this applies to the 792-tile quadrilateral with
side lengths `(649,341,341,143)`. It rules out a small direct dissection,
not a tiling by 792 unit triangles or any other dissection with at least
five similar pieces. In particular 4830 remains unresolved.

The argument applies to all primitive norm triples with a>b and a even,
including `(8,7,13)`, whose reflected-corner quadrilateral is already
known to have a 168-unit tiling by a different construction. Thus the
obstruction is deliberately restricted to the number of similar pieces.

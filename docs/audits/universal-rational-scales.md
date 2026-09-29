# Independent internal audit of the universal rational-scale theorem

29 September 2026. **Verdict: the two annular constructions and their
stated eventual-existence consequences pass this audit.** This is an
internal mathematical review, not external refereeing or proof-assistant
verification. No priority claim is made.

The reviewed statement is [the universal rational-scale note](../universal-rational-scales.md).
The scope is the five non-similar target shapes in the rational
`3alpha+2beta=pi` classification, for each fixed primitive tile. The
similar target and the other groups in Erdős 634 are separate. In
particular, this result does not classify the exceptional small scales
or solve the entire problem.

## 1. The two annuli are actual partitions

Use the note's parameters `a=uv`, `b=v²−u²`, `c=v²`, and physical metric
`dx²+(4v²−u²)dy²`. Both constructions were derived again from the nested
theta triangles, without assuming a lattice or any internal structure
of a pre-existing tiling.

For the apex-centered addition of `u`, the three triangles have side
triples

    ABD: (ab,a²,ac),  ADR: (ac,c²,bc),  SEC: (b²,ab,bc).

Thus their integer similarity scales are `a,c,b`. The remaining
parallelogram has sides `bc` and `L=ubT−a²−b²`. The identity
`c²−a²−b²=bu²` makes its horizontal width equal to `C_x−R_x`.
The inequality `L>=F0` puts the top points `B,D,S,E` and bottom points
`A,R,C` in their claimed order. Consequently the diagonals divide the
trapezoid with disjoint interiors. The common apex is

    (ub(T+u)/2, b(T+u)/2),

and homothety of ratio `T/(T+u)` produces exactly the indicated inner
triangle. This verifies the shell interpretation as well as the
four-piece partition.

For the base-centered addition of `v`, the particularly useful
independent containment check is

    E=C+lambda(D−C),  lambda=u²v/(bT).

The condition `L'=bvT−a²>=F0>0` implies `0<lambda<1`. Hence E is on CD.
The point G is on the outer equal side AB under the same inequality:
its height is `cv/2`, while the height of A is `b(T+v)/2`.
The segments BE and EG divide off the two indicated triangles;
the remaining quadrilateral is exactly ADEG. The side triples are

    BCE: (ab,a²,ac),  BEG: (ac,bc,c²).

At A, the parallelogram's two side vectors are

    AD=(-ubv/2, -bv/2),
    AG=(u(bT−u²v)/2, -(bT−u²v)/2).

They have lengths `bc,L'`. Their metric scalar product, divided by
these lengths, is `(b+c)/(2c)=cos(alpha)`. Thus the claimed acute angle
is alpha for every `0<u<v`, including the complementary Delta-negative
range. No ordering assumption between a and b is required.

## 2. Mixed strips and tile counts

Since `gcd(b,c)=1`, every integer `L>=(b−1)(c−1)` is a nonnegative
integer combination of b and c. A parallelogram with sides `L,bc` and
acute angle alpha therefore splits into b-wide and c-wide strips.
The respective other-direction step lengths are c and b. Each cell
has sides b,c and difference diagonal a, so it consists of two original
tiles. A strip of width b contributes `2b` tiles, and one of width c
contributes `2c`; the entire parallelogram contributes `2L`.

The count identities independently simplify to

    a²+b²+c²+2(ubT−a²−b²) = b((T+u)²−T²),
    a²+c²+2(bvT−a²)       = b((T+v)²−T²).

The stated ceiling bounds are precisely sufficient for the two widths
to reach the Frobenius bound. They need not be optimal. Grid boundaries
on adjacent strips need not align; this is permitted in a tiling with
T-junctions.

## 3. Extension of arbitrary W and beta tilings

The existing geometric transfers partition W into theta plus one
tile-shaped triangle, and beta into theta plus two such triangles.
Their apex is common, and each added block has angle alpha there and
integer scale `vT`.

Apply homothety about this common apex. Each component of the outer
fan contains its corresponding inner component. Therefore the
difference of the whole targets is exactly the disjoint union of
their component annuli. The theta annulus is the first construction.
Each other annulus lies between two similarly oriented tile triangles
at integer scales `vT` and `v(T+u)`, sharing a vertex. The standard
triangular grid based at that vertex contains the smaller triangle as
a subcomplex, so the difference is tiled by the remaining grid cells.

This is a forward construction outside the old target. It does not
require the old W or beta tiling to contain a theta cut, or to agree
with any auxiliary fan or grid inside the old target. Arbitrary old
T-junctions therefore cause no difficulty.

## 4. Seed, arithmetic, and conductor dependencies

The scale-v seed is a direct valid specialization of Beeson's version 4,
Theorem 11:

    M=a, K=c, N=cQ,
    a²+cQ=2c², a²<cQ, c|a².

It supplies exactly the fixed tile `(a,b,c)` and W at scale v. The
already verified transfer supplies beta at the same scale. The
[pure-grid bridge](../scale-spectra.md) then adds v to any realized
scale, using this actual seed. It does not assume that v can be added
without a tiled second triangle.

Quadratic enlargement gives the starting scale
`T0=v ceil(Hu/v)`. From T0, both +u and +v remain available. Frobenius
then supplies every integer scale at least

    C_W,beta=T0+(u−1)(v−1).

For theta, Beeson v4 Corollary 5 explicitly supplies at least one seed
for every rational tile; its cited constructions cover complementary
parameter ranges. The core annulus proof retains this external theorem
dependency. The later [explicit seed appendix](../explicit-theta-seeds.md)
supplies numerical seeds in both ranges; its construction is outside
this audit's scope and has its own [separate audit](explicit-theta-seeds.md).
Given a seed s, quadratic enlargement to
`S=s ceil(max(Hu,Hv)/s)` and the two shells give every scale at least
`S+(u−1)(v−1)`. The theta-to-alpha transfer at theta scale vK gives
the claimed alpha bound. The Frobenius statements include u=1, when
the offset bound is zero.

The necessary integer-scale statements were also checked independently.
For W and beta they follow from the primitive integer side triples.
For theta and alpha the
[two-character argument](../eventual-rational-families.md) uses genuine
characters of the directed-edge group. Its two signed tile counts
both have parity N, even with reflections and T-junctions. For theta,
their half-sum and half-difference force `b|uL` and `b|vL`, hence b|L.
For alpha the half-difference is `LQ/b`, and `gcd(b,Q)=1` gives b|L.
Thus `bT²` and `bQK²` cover all arithmetically admissible scales, even
when b is not squarefree. The false divisibility assertion of Beeson
v4 Lemma 55 is not used here, by the seeds, or by either annulus.

The other-scalene row retains its separate
[two-piece construction and primitive-side necessity proof](../two-piece-construction.md).
Exhaustiveness of the five non-similar target shapes remains the cited
classification input; the new theorem proves their eventual sufficiency.

## 5. The added consequence across tile shapes

The main note's later Section 7 also passes this review. If an odd
integer d is at least 3, then `u=(d−1)/2`, `v=(d+1)/2` are positive
consecutive integers with `v²−u²=d`. The theta theorem therefore
constructs every sufficiently large `dT²` for this fixed d.

If d is even and at least 2, then `u=d−1`, `v=d+1` are positive odd
integers whose common divisor divides 2, so they are coprime. Now
`v²−u²=4d`, giving every sufficiently large `d(2T)²`. This argument
does not cover the odd multipliers in an even square class. Neither
corollary claims a threshold uniform in d or removes the finite
exceptions within a class.

## 6. Exact finite checks and frozen snapshot

The public checker was read and replayed. Its deterministic output
agrees with the [frozen report](../../verification/universal-annuli.json):
773 primitive parameter pairs, both annuli at their own threshold,
and 6,957 macroregion-pair checks all pass.

A separate implementation, importing no project code, reconstructed
the inner triangles by homothety and used exact Fraction polygon
clipping instead of separating-axis tests. For every coprime
`0<u<v<=40`, it checked both shells at their threshold, threshold+1,
and threshold+v. All 2,934 shell instances and 13,203 macroregion-pair
intersections passed, including containment, avoidance of the inner
triangle, area, side congruence, cell geometry, and integer strip
decompositions. These finite checks supplement the symbolic proof;
they do not establish the universal quantifier by themselves.

Reviewed SHA-256 values, after reviewing the main note's added
non-similar wording, explicit-seed references, and Section 7 corollary:

| Artifact | SHA-256 |
|---|---|
| `docs/universal-rational-scales.md` | `65bebdc6617c5af8e6e9d03b3eabe4ad1e9e612aef4ad7aa2b49081464308e9c` |
| `scripts/check_universal_annuli.py` | `27dd28f482e2d74f642a521837eee14a4b23d3bd2f87f34cb3d8a82e938d96c4` |
| `verification/universal-annuli.json` | `0a0d7449721d43ad69a15c6d5237b954f081b2db8ece6f3cf4a5a531746f7500` |

The accepted conclusion is cofinite scale existence for each fixed
rational tile, with the stated explicit W/beta conductor and the
theta/alpha conductor formula in terms of a seed. The later appendix's
explicit seed formulas are covered by their separate audit, not by
the present one. The theorem neither
bounds exceptional counts uniformly over all primitive tiles nor
settles the other angle groups in Erdős 634.

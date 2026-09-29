# Constructive scale structure for the rational base-beta family

29 September 2026. This note gives a new construction derived during the
current session and an eventual-periodicity consequence. Its novelty relative
to the full literature is not established. It does not solve Erdős 634.

**Later refinements.** The [scale-spectrum note](scale-spectra.md) proves
nonemptiness for every primitive pair and treats both W and beta.
The [universal two-annulus theorem](universal-rational-scales.md) further
gives eventual divisor $d=1$ for every primitive pair, with an explicit
bound and no sign restriction. The constructions below remain valid.

## Parameters

Fix coprime integers `0<e<f` and the tile

    a=ef, b=f²-e², c=f², N0=3f²-e².

Let beta be the angle between sides a and c. Let Delta_m be the isosceles
base-beta target with legs `mX`, base `mY`, where

    X=f³, Y=eN0.

Its tile count, if tiled, is `N0*m²`. Let S(e,f) be the positive integer scales
m for which it admits a tiling. All constructions allow reflected tiles and
T-junctions.

Use affine coordinates `(x,y)` for the physical point
`x(1,0)+y(cos(beta),sin(beta))`. The parallelogram P(p,q) is the box
`[0,pY] × [0,qX]` in these coordinates.

## 1. A wider construction than the previously stated pure-grid rule

**Bridge theorem.** P(p,q) can be tiled by `2pqN0` copies of the tile whenever

    e divides q, and p >= ceil(e/2).

First prove the elementary case `e|q` and `q<=2p`. Put

    H=qf, J=2pf, s=peb.

The identities

    pY=Ja+s, qX=Hc

split the box into three regions along the parallel lines

    x/a+y/c=H,       x/a+y/c=H+s/a.

The first region is a triangle of side vectors `(Ha,0)` and `(0,Hc)`.
The usual triangular subdivision into a-by-c cells gives exactly H² tile
copies. The final region, after translating x by s, is the trapezoid

    0<=x<=Ja, 0<=y<=Hc, x/a+y/c>=H.

Since `J>=H`, all its cells are full a-by-c parallelograms or half-cells cut
on their b-diagonal. It contains exactly `2JH-H²` tile copies.

The middle region is the parallelogram with edge vectors

    (s,0), (-Ha,Hc).

Define two brick vectors

    U=(b,0), V=(-a²/b,ac/b).

In the physical metric,

    |U|=b, |V|=a, |U+V|=c.

For example the latter two identities follow directly from
`cos(beta)=(a²+c²-b²)/(2ac)`. Hence the parallelogram spanned by U,V is
two copies of the original tile, split on its U+V diagonal. Moreover

    (pe)U=(s,0),       (qb/e)V=(-Ha,Hc).

Both multipliers are integers. Thus the middle region is an actual grid of
`pq b` two-tile bricks. The three regions have disjoint interiors, full
straight interfaces, and union P(p,q). Their count is

    H²+(2JH-H²)+2pqb = 4pqf²+2pqb = 2pqN0.

For the theorem as stated, apply the elementary construction to P(p,e),
which is permitted by `e<=2p`, and stack `q/e` translated copies along
the leg direction. This proves the result for arbitrarily large q.

This is different from the pure a-by-c grid construction, which requires
`f|p`. For example `(e,f,p,q)=(2,3,1,2)` gives a 92-tile bridge although
`f` does not divide `p`. It does not assert that the corresponding unit
parallelogram P(1,1) tiles.

## 2. The resulting addition rule

**Addition corollary.** If p,q belong to S(e,f), `e|q`, and
`p>=ceil(e/2)`, then p+q belongs to S(e,f).

This is an exact affine dissection. In coordinates let

    Delta_m = {(x,y): x,y>=0, x/Y+y/X<=m}.

The triangle Delta_(p+q) is the disjoint-interior union of

* P(p,q), at the lower-left;
* Delta_p translated by `(0,qX)`;
* Delta_q translated by `(pY,0)`.

The connecting parallelogram is supplied by the theorem, and the two
triangles by hypothesis. The count is
`N0(p+q)² = N0 p²+2pqN0+N0 q²`.

Also retain the simpler existing addition rule: if `f|q` and p,q are
realizable then p+q is realizable. To see this directly, orient the same
decomposition with width qY and height pX; it is an ordinary a-by-c grid
because `(qY)/a=qN0/f` and `(pX)/c=pf` are integers. No lower bound on p
is needed for this rule.

## 3. Eventual classification of the scale set

**Theorem.** For each fixed primitive rational base-beta tile, the set
S(e,f) is either empty or eventually consists of exactly the multiples of
one positive integer d. In the nonempty case `d=gcd S(e,f)`.

Proof. Choose a finite set of realizable scales `m1,...,mk` with gcd d;
every gcd of a nonempty set of positive integers is achieved by a finite
subset. The subdivision ladder makes every positive integer multiple of
each mi realizable. Choose a realizable M with `M>=ceil(e/2)`.

Starting at M, we may repeatedly add any `e mi` by the new bridge theorem,
or any `f mi` by the ordinary grid rule. The current scale only grows, so
the width condition stays true. Thus

    M + <e m1, f m1, ..., e mk, f mk>  is a subset of S(e,f),

where angle brackets denote nonnegative integer sums. The displayed
generators have gcd d, because gcd(e,f)=1.

A finitely generated additive semigroup of positive integers with gcd d
contains every sufficiently large multiple of d. For completeness, divide
the generators by d and fix one generator g. Their residues generate the
whole finite group Z/gZ. Each residue therefore has a representative that
is a nonnegative sum of the generators (negative coefficients can be
replaced modulo g). Choose one such representative per residue and take
their maximum B. Any integer at least B can be obtained from its chosen
representative by adding a nonnegative multiple of g.

Since M is a multiple of d, the inclusion above gives every sufficiently
large multiple of d in S(e,f). Conversely every element of S(e,f) is
divisible by d by definition. This proves the theorem.

**Effective seed version.** Given any finite verified seed list, its gcd
d guarantees all sufficiently large multiples of d are realized, with an
explicit bound obtained from the finite residue construction. This does
not establish that d is the gcd of the complete unknown set S.

For two seeds r,s with `s>=ceil(e/2)`, an especially simple guarantee is

    s+k r belongs to S for every k >= (e-1)(f-1),

because every such k is `A e+B f` with A,B nonnegative. This is a useful
constructive propagation rule, not a statement that all smaller scales
are impossible.

## 4. Complete member (2,3,4), and what is already in the literature

For `(e,f)=(1,2)`, the parallelogram theorem permits all p,q. The exact
44- and 99-tile constructions of Bonfioli give scales 2 and 3. Additive
closure then gives every scale `m>=2`, since each is a sum of 2s and 3s.
Scale one is excluded by the restored adjacent-parameter boundary theorem
at v=2 (its allowed base-count range is empty). Consequently this pair's
scale spectrum is exactly

    S(1,2)={2,3,4,...},      N=11m².

This complete-member result is already present in Bonfioli's companion
source, section 'Realizability', and is not new here. The main source also
retains an older paragraph claiming the gcd(m,6)=1 cases, starting at275,
are undetermined. That paragraph conflicts with the later constructive
theorem; it must not be repeated as the current consequence of those
explicit seeds and bridges.

The complete-member construction does not make every integer count
realizable. It gives only `11m²` in this pair. For instance, absence of a
tiling of a fixed (target,tile) pair at a given count says nothing by
itself about the same count in another pair. In particular a statement
that `(3,8,9)` does not tile its beta target at scale2 is not an exclusion
of104 from the global Erdős spectrum: `104=10²+2²` is realized by the
classical sum-of-two-squares construction.

For e=1 and arbitrary f the unit bridge exists and S(1,f) is additively
closed, but no triangle seed follows just from that bridge. An m-fold
triangle has `m(m+1)/2` upright cells and `m(m-1)/2` inverted cells, while
each two-cell parallelogram consumes one of each. At least m unmatched
cells remain. This is the exact limitation of a proof that tries to make
triangle seeds solely out of these unit parallelograms.

## 5. Verification and audit

`scripts/check_bridges.py` explicitly generates rational affine
coordinates. For each test it checks every squared tile side exactly,
target containment, the exact total area, and pairwise nonoverlap by exact
triangle separating-axis checks; a bounding-box test omits trivial pairs.
`verification/replay.json` records the six cases:

| e | f | p | q | Tiles | Result |
|---|---|---|---|---:|---|
|1|2|1|1|22|PASS|
|1|3|1|1|52|PASS|
|2|3|1|2|92|PASS|
|2|5|1|2|284|PASS|
|3|4|2|3|468|PASS|
|2|3|1|6|276|PASS|

The supplied 44- and 99-tile coordinate files were also independently
replayed over rational coordinates `(x,y/sqrt(15))`: correct sides,
containment, total area and all 946/4851 tile-pair separations passed.
Results are in `triangle_seed_replay.json`.

A separate internal review checked the symbolic three-region
partition, the physical metric of U,V, the cell counts and the additive
gluing, and found no gap. Sample checks support the implementation; the
uniform proof is the explicit construction above. No formal proof or
external novelty/peer-review claim is made.

## 6. Exact barrier to a full solution

The subsequent results cited above establish that S is nonempty and
its gcd is $d=1$ for every primitive pair. Its exact finite exceptional
scales below the explicit universal bound remain undetermined in general.
It also covers only rational base-beta pairs. A solution of all of
Erdős634 must combine every target/tile family and eliminate or realize
all remaining counts, including composites. Prime nonexistence alone
would not supply this classification. The constructive theorem here is
new progress in the scale direction, not that missing full classification.

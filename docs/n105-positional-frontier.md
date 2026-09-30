# N = 105: exact boundary collars and the remaining positional gap

> **Historical stage — 29 September 2026.** Its limited claims remain as written. The later [global N=105 proof](n105-global.md) supersedes statements here that the count is unresolved. These old partial certificates are retained as regression evidence, not as the new proof.

29 September 2026. Research result checked by exact arithmetic; no priority or external review claim.

**No complete 105-tiling or proof excluding every 105-tiling was obtained.**
Both surviving rational 60-degree equilateral candidates admit the explicit
positive-width boundary collars described below. These partial configurations
satisfy outer-boundary coverage, congruence, nonoverlap, and all outer junctions.
Further analysis shows that **neither of these two fixed collars can extend**:
in each, one convex corner on the inner rim has no possible first tile.
See the [four-placement proof and independent replay](n105-fixed-collar-obstructions.md).

The precise lesson is that the outer-boundary checks alone are insufficient;
inner-rim extendability is an additional necessary condition. This is not a
barrier to all arguments based on a first boundary layer, and it does not
exclude other collars or settle N=105.

## 1. The boundary-junction lemma

Let the tile angles be `(alpha,beta,gamma)`, where `gamma=pi/3` and
`alpha/pi` is irrational. Since `alpha+beta=2pi/3`, the only nonnegative
integer angle decompositions of a straight angle are

    pi = alpha + beta + gamma = 3 gamma.

At each equilateral target corner there is exactly one tile, with its gamma
angle there. Along an outer side, consecutive boundary tiles contribute two
angles at their common boundary vertex. Two alpha angles or two beta angles
cannot occur together. Each allowed pair has exactly one missing tile angle:

| Boundary pair | Missing angle |
|---|---|
| alpha, beta | gamma |
| alpha, gamma | beta |
| beta, gamma | alpha |
| gamma, gamma | gamma |

The order of the first three pairs may be reversed. The missing angle cannot
split into several tile angles: compare the coefficients of alpha and pi/3.
Consequently **exactly one further tile fills each boundary gap**, with at
most two possible placements, obtained by interchanging its two incident
side lengths. This argument allows T-junctions: an edge passing through the
gap vertex would contribute pi, larger than the gap.

For a prescribed boundary row on all three target sides, compatibility of
these missing tiles is a finite 2-SAT problem. Each gap has at most two
placements; two choices whose interiors overlap, unless they describe the
same tile, cannot both be selected. Containment and compatibility with the
boundary tiles are unary constraints. Thus testing one complete boundary
collar does not require a full interior tiling search.

## 2. Two exact partial tilings

Applying this to the two 60-degree candidates left by the arithmetic for
N=105 gives the following **partial** tilings of an equilateral triangle of
side 105:

| Tile sides | Placed tiles | Remaining connected area | Residual boundary vertices |
|---|---:|---:|---:|
| (5,21,19) | 45 | 60 tile areas | 38 |
| (7,15,13) | 57 | 48 tile areas | 44 |

All three boundary side words are the same, read counterclockwise. Writing
`a,b,c` for the corresponding edge lengths, the words are

    a a a a a c c b b             for (5,21,19),
    a a a a a a a c c b b         for (7,15,13).

Their lengths are respectively `5*5+2*19+2*21=105` and
`7*7+2*13+2*15=105`. The coordinate certificates specify the orientations and
the selected gap tiles; the edge words alone are not certificates.

Use oblique coordinates with basis `(1,0)` and `(1/2,sqrt(3)/2)`.
Each certificate stores integer coordinates divided by its integer `scale`.
Its Euclidean squared-length form is therefore

    (dx^2 + dx*dy + dy^2) / scale^2.

The residual polygon stays strictly inside the target. The minimum of its
three oblique barycentric coordinates is `25/19` in the first case and
`49/13` in the second. In particular these are genuine positive-width
boundary collars, not merely nonoverlapping tiles that touch the sides.
The remaining interior has positive area. For these two fixed collars, a
subsequent exact four-placement check proves that it **cannot** be tiled
without changing the collar.

An independent verifier, without importing the construction script, checked:

* every tile's three exact squared lengths and orientation;
* containment in the equilateral target;
* all 990 and 1,596 pair intersections, using rational convex clipping;
* oriented-edge cancellation after atomizing at all T-junctions;
* the unique residual polygon, its exact area, and its positive distance
  from every outer side.

Run the fast verification with:

    python scripts/verify_n105_collars.py

The coordinate certificates are [the 45-tile collar](../data/n105-collar-5-21-19.json)
and [the 57-tile collar](../data/n105-collar-7-15-13.json). The saved exact report is
[verification/n105-collars.json](../verification/n105-collars.json).
The verifier uses only the Python standard library, resolves these paths from
its own location, writes no files, and prints deterministic JSON to standard
output. It rejects optimized Python modes that disable assertions.

The exploratory search used the same boundary word on each of the three
sides, then solved the gap-placement constraints by 2-SAT. The chosen full
collars need not have rotational symmetry. The search was stopped after
finding a collar; it gave an existence certificate for a partial configuration,
not an exhaustive verdict about all N=105 tilings. The exact certificate
replay above is sufficient to verify the published claim and does not depend
on that search.

## 3. The F1 candidate: a clean reduction, with an unproved forcing step

For a primitive 120-degree tile `(a,b,c)`, where `c^2=a^2+ab+b^2`, the minimal
F1 target has sides `b(a+b),ab,bc` and area count `b(a+b)`.

There is an elementary two-region dissection of that target. In the oblique
coordinates above put

    O=(0,0), A=(b(a+b),0), C=(0,ab), B=(ab,0).

Then `OBC` is equilateral of side `ab`, and `ABC` is the tile enlarged by
factor b. Subdivide the latter quadratically into `b^2` copies of the tile.
The former would require `ab` further tiles, giving `b^2+ab=b(a+b)` in total.

For `(a,b,c)=(8,7,13)`, this is a 49-tile corner block plus an equilateral
region requiring 56 tiles, inside the target `(105,56,91)`.

Bonfioli's [manuscript at repository snapshot `2f9af59`](https://github.com/ElVec1o/erdos_634_proof/blob/2f9af59/paper/erdos-634.tex)
reports a complete search excluding that 56-tile equilateral instance
(156,646 nodes). That external certificate was not replayed
in this round. **Even accepting its verdict does not exclude the F1
105-tiling**: a general tiling need not respect the segment BC. A theorem
forcing that entire 49-tile corner block would be the missing geometric
step. No such forcing theorem was established here.

## 4. What not to infer from invariant computations

The round-3 formal boundary identity proves that every additive invariant
depending only on edge direction and length passes the minimal F1 candidate.
It does not prove that every positional or noncommutative tiling invariant
passes. In particular, testing finitely many finite-group quotients and a
finite number of nilpotent quotients cannot by itself prove that the full
tiling-group obstruction is trivial. A broader claim in the local external
source should not be imported without a separate general argument.

## 5. Scope

The arithmetic exclusion of the irrational 120-degree equilateral branch at
105 from the earlier arithmetic analysis remains valid. The two 60-degree
targets and the F1 candidate remain unsettled by our own work.

The coordinate certificates establish valid partial boundary collars. A
subsequent exact local argument proves that these **two fixed placements**
cannot extend: at the oblique point `(a,b)`, the remaining angle is
`alpha+gamma`, and all four possible first-tile placements overlap an existing
collar tile. Each refutation has a complete one-node certificate independently
checked without the search's polygon subtraction or boundary stitching.

Thus outer-boundary coverage, congruence and nonoverlap alone do not guarantee
extendability. The result does not show that an arbitrary first-layer forcing
argument must fail, and it is not an exclusion of all N=105 tilings or a
solution of Erdős problem 634.

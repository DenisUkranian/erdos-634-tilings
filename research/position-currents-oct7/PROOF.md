# Positioned boundary currents and a three-height obstruction for the 154 candidate

**7 October 2026. Prepared for Denis Paliy, with ChatGPT assistance.**

## Status

The missing universal theorem for Erdős problem 634 has **not** been proved.
Neither 154 nor 4830 is decided by this note. The new result is a restricted,
computer-assisted obstruction, together with the lattice and current arguments
that make its placement enumeration complete.

For the triangle with sides `(91,91,154)` and tile `(8,7,13)`, no tiling can
use at most two classes of short-edge directions modulo 60 degrees. In
particular, the complete two-adjacent-height placement problem has an exact
integer refutation. This does not assert that a tiling using three or more
classes is impossible.

The source baseline is repository commit
`d460b3d23a90953e9524fba5e7616be71b779efd`. The arguments below do not assume
a universal pure-switch, gamma extraction, bounded-treewidth normal form,
or that a fractional solution is a genuine tiling. No first-priority claim,
external referee approval, or proof-assistant verification is asserted.

## 1. Directions and a sharper lattice for a prescribed height band

Use Eisenstein coordinates `(x,y) <-> x+y*rho`, where
`rho=exp(i*pi/3)` and the squared Euclidean norm is `x²+xy+y²`.
For positive primitive integer sides satisfying

    c²=a²+ab+b²,

put `Z=a+b*rho` and `z=Z/c`. The angle of z is an irrational multiple of pi:
`2 cos(arg z)=(2a+b)/c` is rational and strictly between 1 and 2. If the
angle were a rational multiple of pi, this quantity would be a rational
algebraic integer, hence an integer, a contradiction.

After fixing the boundary normalization, every edge direction is uniquely
`rho^j z^h`, modulo `j in Z/6Z`. Propagation across positive-length contacts
gives this representation. Both short edges of one tile have one height h;
its long edge has height h-1 or h+1. Both handedness choices are permitted.
These are the height conventions of the existing project [2].

### Lemma 1 (finite-band vertex lattice)

Suppose a convex polygon has an actual tiling by this integer-sided tile,
and all its short-edge heights lie between integers L and U. Choose one
actual vertex as origin. Then all actual vertices lie in the discrete module

    Lambda_[L,U] = sum_{h=L}^U z^h Z[rho].                 (1)

**Proof.** Split tile edges at all genuine tile vertices on them. Each atom
has positive integer length, by the whole-edge partition argument in [1].
For direction heights L through U, its displacement therefore belongs to
one of the displayed summands.

At an extreme edge height L-1 or U+1, an edge can only be a c-edge. On a
maximal interior collinear component both banks are partitions into whole
edges of the same length c, with common initial and final endpoints. They
therefore match whole-to-whole. The supporting-boundary case also consists
of whole c-edges. An extreme-direction atom consequently has length c, not
an arbitrary integer length. Its displacement is in (1), since

    c z^(L-1) = z^L conjugate(Z),
    c z^(U+1) = z^U Z.

The connected atomic-edge graph propagates membership from the chosen
origin to every vertex. After rotation by z^(-L), the module is contained
in `c^(-(U-L)) Z[rho]`, so it is discrete. ∎

This lemma assumes a height band; it does not prove an absolute band bound.
Its lattice can be much sharper than the general rational denominator bound
obtained by developing a spanning tree of all faces in [3].

### The lattice for heights 0 and 1 of the 154 candidate

Here `a=8,b=7,c=13`. Let

    eta=(3+rho)/13.

The exact equality is

    Z[rho]+z Z[rho] = Z + eta Z,                        (2)

because `eta=2z-1-rho`, `rho=13eta-3`, `z=7eta-1`, and
`rho*z=15eta-4`.

Thus, in coordinates multiplied by 13, every vertex is an integer pair
`(p,q)` with

    p-3q = 0 (mod 13).                                  (3)

This includes the gamma vertex of every candidate tile. It is not a guessed
mesh or a restriction to integer Cartesian positions.

## 2. A positioned-current criterion

Let `T_1,...,T_J` be a finite list of actual closed triangular placements
contained in a fixed polygon P. Orient each triangle and P counterclockwise.
Split collinear sides into common elementary directed segments. Let B have
one column for the signed boundary of each T_j, and let b be the signed
boundary of P. Positions of the segments are retained: parallel segments
on different lines, or at different positions on a line, are different rows.

### Lemma 2 (integer current criterion)

    P has a tiling using the listed placements
    iff there is x in Z_{>=0}^J with Bx=b.               (4)

Moreover, a real nonnegative solution gives weighted coverage exactly one
almost everywhere, and necessarily `0<=x_j<=1` for each j.

**Proof.** Necessity is cancellation of internal boundaries. For the
converse, the compactly supported function

    f = sum_j x_j 1_{T_j} - 1_P

has zero jump across every open edge atom when `Bx=b`. Split the finite
arrangement further at intersections when necessary. Across any edge away
from its finitely many endpoints, the two constant values of f coincide.
A generic path from the exterior to any arrangement cell crosses only such
edge interiors. It follows that f is zero on every cell, and hence almost
everywhere. This is equivalently the vanishing of its distributional
boundary current.

For any one T_j, take an interior point off all edges. Nonnegativity and
weighted coverage one imply `x_j<=1`. If all weights are integers, each is
0 or 1; two selected triangles cannot overlap in their interiors, since an
open overlap would contain a point off all edges. The selected closed
triangles cover the target by closure. This is a tiling. ∎

A fractional positive solution of (4) is **not** thereby an ordinary tiling.
The implication used for negative certificates is safe:

    no real solution in [0,1]^J => no tiling.

Lemmas 1 and 2 combine into a complete finite integer placement formulation
for any *prescribed* height band. They do not constitute a new theorem of
unrestricted fixed-N decidability, which is already recorded in [1]. Their
use here is a position-sensitive negative test without prescribing a disk
or a contact ordering in advance.

## 3. Exhaustive dictionary for the adjacent-height 154 problem

The target is

    P = conv{(0,0),(154,0),(49,56)}

in Eisenstein coordinates. Its side lengths are `(154,91,91)` and its area
is 154 times the `(8,7,13)` tile area. In coordinates multiplied by 13,

    P13 = conv{(0,0),(2002,0),(637,728)}.

The complete set of possible gamma anchors satisfying (3) is specified by

    q >= 0,
    8p >= 7q,
    8p+15q <= 16016,
    p-3q = 0 (mod 13).                                 (5)

It has 56,183 points. The generator uses exact integer row bounds; a separate
audit scans the enclosing integer Cartesian rectangle using (5).

For each `(x,y)=(8,7)` or `(7,8)`, the two reference edge vectors from the
gamma corner are, in these multiplied coordinates:

| Short height | First edge | Second edge |
| --- | --- | --- |
| 0 | `(13x,0)` | `(-13y,13y)` |
| 1 | `(8x,7x)` | `(-15y,8y)` |

Apply all six rotations `(p,q)->(-q,p+q)`. This gives all 24 variants,
including both handedness choices. At every anchor retain a variant exactly
when all three vertices satisfy the target half-plane inequalities. Convexity
then gives full containment. Completeness follows from Lemma 1, the unique
gamma corner, and the two choices of ordering the short sides.

The resulting dictionary contains exactly **873,496** contained triangles.
All squared side lengths and positive oriented areas were checked again by
an independent integer half-plane enumeration.

### Matrix construction and separate audit

Along each side, split at consecutive points of the lattice (2). The matrix
has

    550,333 rows,
    873,496 columns,
    19,222,288 nonzero entries, each +1 or -1.            (6)

The builder obtains the shortest lattice step using a gcd in ambient
coordinates. The separate matrix audit transforms endpoints to lattice
coordinates `((p-3q)/13,q)`, divides their difference by its integer gcd, and
reconstructs every positioned atom. It checks all entries in (6), their
signs, absence of repeated rows within a column, and the target RHS.

Neither enumeration nor either audit uses a geometric floating tolerance.
NumPy integer arrays and SciPy's sparse storage do not supply a numerical
feasibility verdict; they store the exact integer instance.

## 4. Integer refutation of the complete adjacent-height matrix

Initially every possible placement has an unknown weight in `[0,1]`.
Consider any signed row after some weights have been fixed. If it contains
p positive and n negative unknown coefficients, its remaining value lies
in `[-n,p]`. If its required RHS is -n, all positive unknowns must be zero
and all negative unknowns one. If it is p, the reverse assignments are
forced. A required value outside this interval is a contradiction.

This rule is valid for real weights, not just for binary choices. Applying
it repeatedly gave 869,546 forced assignments and a contradictory row.
The retained proof removes unused dependencies and contains **678,493**
assignments. Each record names a variable, its forced value, and the row
which forces it. The independent C++ verifier recomputes the row bounds
from scratch at each record, rather than reusing the producer's queue or
incremental interval calculations.

After the retained transcript, row **70104** requires residual value **1**,
whereas its possible interval is **[-1,0]**. This row is the positioned atom

    (637,533) -> (644,518)

in the coordinates multiplied by 13. Thus the complete matrix has no
nonnegative real solution, and the target has no tiling with short heights
in `{0,1}`.

The isosceles target is invariant under the reflection
`w -> 154-conjugate(w)`. This sends h to -h. It therefore also excludes
short heights in `{-1,0}`.

A mutation reversing the first recorded forced assignment is rejected by
the independent verifier. As a positive control, a known 88-tiling by
`(3,5,7)` was reconstructed from the four-region construction [4], then
reflected into the same two-height convention. It passes exact positional
current cancellation and all 3,828 tile-pair tests. Removing or duplicating
a tile fails the current test. The 88 construction is credited to the prior
project/Harries source, not claimed as a new result of this note.

## 5. Excluding every two-height possibility for this candidate

The preceding computation excludes adjacent heights containing zero. Two
short further arguments account for all sets with at most two heights.

### The zero height is compulsory

The existing I120 level theorem [2] gives

    13 | n_h for h != 0,
    n_0 = 154 = 11 (mod 13).                            (7)

Thus height zero must occur. Its proof uses whole-edge cut currents and
lattices `z^k(c Z[rho]+Z Z[rho])` of area index c. It permits arbitrary
T-junctions and does not assume that every vertex lies in one short lattice.
We use (7) exactly as established there, not the unsupported stronger
assertion `c² | n_h`.

### The two heights cannot be far apart

A tile of short height h has edge heights h and h-1 or h+1. Two tiles in
positive-length contact must have a common edge direction. Accordingly,
if only heights 0 and h occur, connectivity of the positive-contact graph
forces `|h|<=2`. Larger gaps could not connect the two populations.

### Heights 0 and 2 already require too many tiles

Suppose only heights 0 and 2 occur, with height 2 present. Consider a
positive-contact component of height-2 tiles. Its short-height-2 edges
cannot lie on the target boundary, whose heights are -1, 0 and 1, or touch
a height-0 tile. They therefore cancel within the component. Its long
height-3 edges likewise cannot be external or touch height zero, and
cancel internally.

All remaining component boundary edges have height 1 and length c. On
any height-1 line every tile side is a c-edge, because neither height-1
short tiles nor any other short height is present. Convex ambient
whole-edge partitioning makes these contacts whole-to-whole. Thus the
component boundary is a balanced signed sum of **whole** c-edges at one
height, even when the component is nonconvex or has holes.

Decompose that boundary into closed directed walks. After translating a
walk's initial vertex, its steps lie in `c z Z[rho]`. Its signed area is
an integer multiple of `c² sqrt(3)/4`. Summing the walk areas and comparing
with the tile area `ab sqrt(3)/4` yields

    ab * (component tile count) = c² * integer.

Since `gcd(ab,c²)=1`, the component has at least `c²=169` tiles. The entire
target has only 154, a contradiction. Reflection handles heights 0 and -2.
Notice why this argument cannot just be applied when height 1 is also
present: long height-1 edges may then meet short edges, and the crucial
whole-c-edge boundary conclusion is lost.

### Theorem 3 (three-height lower bound)

Every hypothetical tiling of the triangle `(91,91,154)` by congruent
`(8,7,13)` triangles has **at least three distinct short-edge direction
classes modulo pi/3**.

**Proof.** Height zero occurs by (7). A second height, if it is the only
other height, must be ±1 or ±2. Adjacent cases are excluded by the exact
certificate and reflection; the distance-two cases are excluded by the
169-tile component bound. A single height is included in the adjacent-band
exclusion. ∎

This theorem does not decide N=154. It leaves every configuration with
three or more heights to be treated. It is stated for the specified tile
and target; using any all-branch uniqueness reduction is a separate input.

## 6. What remains of the missing theorem

The positioned-current formulation retains the geometry omitted by a
translation-invariant directional signature. On this example it proves
an actual restricted impossibility, rather than merely verifying a supplied
configuration. It is nevertheless still a finite-band placement problem,
not an all-integer arithmetic classification.

A general extension must justify complete control of all relevant height
bands and must keep the distinction between real and integer feasibility.
No bounded-height normal form, LP integrality theorem, or universal positive
replacement is assumed or proved here. Existing counterexamples to other
normal-form routes must remain respected [3].

Two exploratory integer-macro searches for the 792-tile beta quadrilateral
for 4830 (including a version allowing tileable parallelograms) were stopped
at their explicit resource budgets. They returned INCOMPLETE, not a proof
of impossibility. No new 4830 construction or exclusion was obtained.
No W small-scale classification was obtained. The full Erdős problem remains
unresolved in this work.

## 7. Sources and reproducibility

All repository references below are pinned at
`d460b3d23a90953e9524fba5e7616be71b779efd`:

1. `docs/exact-seam-certificates.md`, Section 1 (integer atoms), and the
   existing fixed-N decidability scope.
2. `research/i120-global-oct7/HEIGHT_LEVELS.md`, I120 height representation
   and divisibility of the nonzero populations.
3. `docs/audits/seam-automata-global-width-2026-10-07.md`, genuine limitations
   of bounded-width arguments and the earlier rational-development bounds.
4. `research/group2-f4/PROOF.md`, reconstruction of the known 88 positive
   control, with its attribution to Harries's example.
5. `research/final-synthesis-oct7/LITERATURE.md`, previous project source and
   dependency audit. Reading it does not certify all external literature.

Canonical source root:
https://github.com/DenisUkranian/erdos-634-tilings/tree/d460b3d23a90953e9524fba5e7616be71b779efd

The package README gives a complete local replay without network access.
The numerical proof object is the retained propagation transcript, not a
solver log. The finite dictionary, exact matrix audit, independent replay,
and positive/adversarial controls have distinct scopes. Independence here
means different implementations within this investigation, not separate
human referees.

# Exact seam-tree certificates for a fixed candidate

For a fixed integer-sided triangle and a fixed triangular target, the metric
part of a proposed tiling certificate can be checked by integer arithmetic
on trees of side contacts. The theorem below permits arbitrary T-junctions
and reflections. It does not solve Erdős 634 or give a uniformly bounded
construction grammar.

## Existing finite reduction and scope

[The uniform reduction](../research/uniform-reduction/PROOF.md), Sections 6–7, already proves, conditional
on the stated published angular/rationality classification inputs:

* a finite exhaustive overlist of at most `13(N+1)^2` primitive tile/target
  candidates, with primitive tile sides at most `(N+1)^2`;
* a complete exact rational six-choice convex-sector search of depth N;
* hence fixed-N decidability in principle. The retained N=154 run is
  INCOMPLETE, not a negative decision.

[The finite-schemes discussion](finite-schemes-attack.md) and its audit correctly distinguish that from
a bounded description of all positive constructions. A universal bound on
ordinary grid blocks was already refuted. The more general finite repetition
grammar is unresolved. Pure-island chirality switching is also unavailable:
the same-target local switching assertion has an
[explicit counterexample](nonconvex-chirality-counterexample.md).

The useful additional observation below is that **continuous seam offsets
can be removed entirely** for these primitive integer-sided candidates.
What remains is the unbounded global combinatorial disk, not real algebraic
feasibility for a fixed disk.

## 1. Integer atoms in a convex ambient polygon

**Lemma.** If a convex polygon is tiled by finitely many triangles having
integer side lengths, every atomic edge obtained by splitting all tile edges
at all tile vertices on them has positive integer length.

**Proof.** Fix a line containing some tile edge and let J be a maximal
connected interval in the union of the tile edges on that line. If the line
supports the target, J lies in one straight boundary side; the boundary is
partitioned by whole tile edges. A tile side cannot lie partly on the
boundary and partly in the interior, because the target is convex.

Otherwise every relative interior point of J lies in the interior of the
target. On each side of its line, J is partitioned into whole tile edges.
Indeed, at a generic point of a tile edge the opposite incident region must
also have a tile edge on the line: an opposite tile containing that point
in its interior would overlap the first tile. A partition edge cannot
continue beyond an endpoint of J, by maximality. Nor can an endpoint of J
lie in the interior of a same-line tile edge, for the same reason. Thus both
partitions start and end at the endpoints of J. All their breakpoints are
integer distances from the initial endpoint, being cumulative sums of whole
integer side lengths. Every atomic length is the difference of two such
integers. The boundary case has the same cumulative-sum proof. QED.

This does not imply that Cartesian coordinates are integral, or that atoms
are multiples of any one distinguished side c. The geometry of a nonconvex
region alone does not give the common endpoints used in the proof: partly
exposed sides can have different phases. If such a region is already known
to be a union of tiles in a full convex integer-sided tiling, its contact
atoms inherit integrality from that full tiling, but still need not have
lengths divisible by c. These distinctions prevent applying the lemma as
the unsupported long-edge matching or chirality-switching assertion.

The underlying whole-edge partition observation appears in Michael Beeson,
[*Triangle Tiling I*](https://www.michaelbeeson.com/research/papers/TriangleTiling1.pdf),
Definition 1 and the paragraph immediately following it, printed page 8.
The integer-atom statement above is a short consequence of that elementary
observation; no priority claim is made here.

The additive cancellation argument in
[the uniform-sectors proof](../research/uniform-sectors/PROOF.md) does not
require integer atomic lengths. For the full convex integer-sided tiling,
however, the stronger conclusion proved here does apply.

## 2. A stronger, purely combinatorial seam obstruction

Make one vertex for each **original full tile side occurrence**, so there
are 3N vertices. Join two such vertices when their corresponding sides
overlap in a positive-length atomic contact. Call this the side-contact
graph; it is not the ordinary tile-adjacency graph.

**Lemma.** Every nontrivial connected component of the side-contact graph
of a tiling of a convex polygon is a tree. Boundary side occurrences are
isolated. In particular, the side-contact graph is a forest.

**Proof.** All sides in a component are on the same line. On a maximal
collinear interval J, the two sides of the line supply two interval
partitions, with disjoint interiors within each partition. Let them have
p and q intervals. Let h be the number of common internal breakpoints.
Their overlap graph has p+q vertices, p+q-1-h edges (one per elementary
overlap interval), and h+1 connected components, cut at precisely the common
breakpoints. Each component is connected and has one fewer edge than
vertices, hence is a tree. Convexity supplies complete partitions with
common outer endpoints as in Section 1. QED.

For a fixed tree H, assign to each vertex v its full side length l(v), one
of a,b,c. For an edge e let x(e) be the unknown contact length. Its equations
are simply

    sum_{e incident with v} x(e) = l(v).

There is **at most one** solution. Recover it by repeatedly deleting a leaf:
the leaf's residual length is the value on its sole remaining edge; subtract
it from its neighbor's residual length. At the end the final residual must
be zero. Every recovered edge value must be strictly positive. Thus the
only arithmetic checks on a specified seam tree are an alternating balance
and positivity of its signed cut sums. All recovered lengths are integers.

Equivalently, bipartition H with signs epsilon(v)=+/-1. The final balance is
`sum epsilon(v) l(v)=0`; removing any one edge gives a component S and that
edge's length is the appropriate signed value of
`sum_{v in S} epsilon(v) l(v)`.

This is a universal exact obstruction to a *proposed side-contact pattern*:
a cycle, a failed alternating balance, or a nonpositive cut length is
impossible. It is not a universal impossibility result for any tile count,
since a different disk/contact pattern may exist.

The stronger [caterpillar theorem](seam-caterpillars.md) shows that every
nontrivial component is a tree whose nonleaf vertices form a path. Together
with positive length balances this characterizes an isolated seam when its
contact ordering may be chosen. It does not by itself characterize a disk.

## 3. Linear-size combinatorial bound

Discard artificially inserted vertices which are not vertices of any tile.
Let I be the number of interior vertices at which every incident tile
has a genuine corner, T the number of interior T-junction vertices, and B
the number of boundary vertices, including the three target corners. At a
T-junction exactly one incident tile has a flat
angle pi; all other incident tiles have genuine corners. A boundary vertex
cannot lie in the interior of a boundary tile side in a convex target.

Summing the original N triangle angle sums gives

    N = 2 I + T + B - 2.

Here I and T are disjoint counts. The three target corners together
contribute π, while the other B−3 boundary vertices each contribute π.
This is also Beeson's angle-counting identity in Lemma 2 of the source
cited above, with the three target corners included in B here.

There are V=I+T+B vertices, E atomic edges, N faces, so Euler gives

    T <= N-1,
    V = N+2-I <= N+2,
    E = V+N-1 <= 2N+1.

Every T-junction inserts precisely one extra atom incidence into the side
of its straight-through tile. Thus the total number of face-edge incidences
(darts) is `3N+T <= 4N-1`. These are useful sharp-order bounds for complete
enumeration; they are **not** N-independent complexity bounds.

## 4. Exact sufficiency of a disk certificate

Fix a nondegenerate integer-sided tile R and a triangular target with side
lengths A,B,C. A certificate consists of an oriented finite regular cell disk
with N faces, each face being a triangle with finitely many flat marked
points inserted on its three sides. Here regularity means that each closed
face is embedded and face intersections are unions of atomic cells; it does
not require every pair of original triangles to meet along a whole original
side. Cross-points at genuine tile corners and T-junctions are allowed. Record:

1. the cyclic order of each face's three true corners, matching R or its
   mirror, and the grouping of its darts into its three side chains;
2. reversed-orientation pairings of interior darts and the resulting vertex
   identifications; unpaired darts form one boundary cycle;
3. three distinct marked target corners on that boundary cycle.

Require the following finite checks.

* The quotient is connected and is genuinely an oriented topological disk:
  vertex links are circles internally and intervals on the boundary; one boundary cycle;
  Euler characteristic 1; all atomic vertices around each closed face are
  distinct, not merely its three original corners.
  Every vertex must be a true corner of at least one incident face, not
  merely an artificial flat subdivision mark. Otherwise a redundant mark
  can slide along an edge, and neither atom integrality nor uniqueness is
  valid for that enlarged set of marks.
* The relative interior of each original side is either wholly inside the
  target or wholly on its boundary; boundary sides have one dart. The
  original-side contact graph is a forest.
  Use one graph edge per glued atomic pair; parallel edges count as a cycle.
* The preceding leaf elimination assigns strictly positive lengths to every
  interior atom and zero final residual to every tree. Boundary atoms have
  the specified original full side lengths. Equivalently, all face side
  sums equal a,b,c. The three exterior chain sums equal A,B,C.
* Interior vertex angle sums are exactly 2pi. Boundary vertex sums are pi
  except at the three designated target corners, where they equal the
  target's three positive angles. A flat point of a face contributes pi,
  not zero. The corner-type counts are not a substitute for their specified
  cyclic gluing and disk topology.

**Theorem.** Such a certificate exists if and only if the target admits an
N-tiling by R.

Necessity is Sections 1–3 and the evident geometric cell decomposition.

For sufficiency, give each face the metric of the specified triangle R,
placing the flat side points at the recovered cumulative distances. Glue
equal-length paired atoms by the indicated reversed boundary isometries.
This produces a flat metric disk: all interior cone angles are 2pi, and all
interior seam points have ordinary flat neighborhoods. Its orientation
gives an orientation-preserving development into the Euclidean plane.
Interior holonomy is trivial because the disk is simply connected and
the small loops around its vertices have total angle 2pi. The development
therefore extends consistently over the whole disk, face by face.

The developed boundary has three positive turns adding to 2pi; every other
boundary point has angle pi. Its three side lengths are A,B,C. It is exactly
one simple positively oriented convex target triangle, up to a rigid motion.
For a point not on a developed edge, the number of its preimages is the
oriented degree, hence 1 inside this triangle and 0 outside. Each face
contributes positively. Consequently face interiors are disjoint, lie
inside the target, and cover it. Closure supplies the seams and boundary.
This is the required tiling.

One can equivalently begin with positive real unknown atom lengths and
linear face-side sum equations. The same sufficiency argument applies;
Section 1 then forces every solution integral. In fact there can be at most
one positive solution per gluing: interpolating two distinct solutions
would give a nonintegral one. The seam-tree method proves this uniqueness
constructively, without linear programming or quantifier elimination.

The exact local angle equalities are decidable from the known classified
angle relations, or by exact algebraic rotations together with winding
counts. Merely testing a rotation product equal to 1 is insufficient: a
cone angle 4pi has the same product as 2pi and must be excluded.

## 5. What this accomplishes, and the exact missing theorem

Together with the 13-row overlist, one may enumerate all oriented disks with
at most 4N-1 darts, all face side/corner labels, and all allowed pairings.
Every true tiling appears. The forest and leaf checks have no real unknowns;
the angle and boundary tests complete the decision. This is an alternative
exact finite certificate system, not a new proof that membership is
decidable, and not an improved asymptotic search bound over the existing
six-choice search.

The essential remaining object is the **global disk gluing**: three separate
side-contact trees meet through each triangle and must coexist with the
local angle fans and the single outer boundary. Tree balances, all angle
inventories, the boundary word, and integer atoms separately do not provide
this compatibility. The number and shapes of these disks are unbounded as
N varies. Nothing here proves a fixed finite repetition grammar, a uniform
small-scale classification, or a general arithmetic membership criterion.

## 6. Finite replay

The standalone standard-library verifier
[`verify_seams.py`](../research/seam-certificates/verify_seams.py) reads the
retained [`N=322` certificate](../data/tiling-322.json) without importing
construction code. It extracts every atom using all genuine tile vertices,
checks the forest property, and reconstructs every interior atom length
solely from whole side lengths by leaf elimination. The retained
[verification report](../research/seam-certificates/verification.json) gives:

* 966 original side occurrences;
* 450 interior contact trees: 444 of size 2, five of size 5, one of size 11;
* 474 interior atoms and 42 boundary atoms;
* 195 vertices: 129 ordinary interior vertices, 24 T-junctions, and 42
  boundary vertices including the three target corners;
* 516 atomic edges and 990 face-edge incidences;
* integer atom lengths in `{1,2,3,4,5,6,9}`;
* every recovered length agrees with the exact coordinates.

## 7. Implemented abstract-disk verifier

The subsequent [disk-certificate package](../research/disk-certificates/)
implements the full check from coordinate-free incidence data. Its input
contains neither coordinates nor atomic lengths. It reconstructs integer
atoms, checks the disk topology and caterpillar contacts, develops every face
using exact rational arithmetic, and checks that all vertex images agree and
the boundary traverses one triangle strictly forward. The
[independent proof audit](audits/disk-realization-2026-10-06.md) explains why
degree one then certifies nonoverlap without evaluating angles. The local
angle criterion above remains valid; direct development is an alternative.

The retained 322-face disk and adversarial examples, including a 4-pi cone
with trivial holonomy, are checked by that package. A failure rejects only
the supplied scheme. No search for a new N is performed.

This finite replay does not implement the general abstract-disk certificate
checker described in Section 4. It also does not independently reprove the
retained construction's global containment or nonoverlap; the separate
existing [`verify_322.py`](../scripts/verify_322.py) performs those geometric
checks. Boundary incidence and opposite-bank contacts are checked here as
local consistency conditions. See the
[replay instructions](../research/seam-certificates/README.md).

The example illustrates why integer atoms need not be multiples of a
particular tile side: some atoms have length 1, whereas the tile sides are
5, 6, and 9. The unbounded global disk-gluing problem from Section 5 remains
unresolved.

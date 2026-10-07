# What a finite seam automaton does not imply globally

7 October 2026. This is a precise limitation of a proposed bounded-width
proof, not a counterexample to the finite parametric construction conjecture.

## Fixed directions and trivial seams do not bound disk width

**Proposition.** Fix any nondegenerate triangle R, including any fixed
primitive integer-sided tile in the classification. For every positive k
there is a tiling of a triangular target by congruent copies of R such that:

* only R and its half-turn occur as orientations;
* the tiling is edge-to-edge, with no T-junctions;
* every nontrivial original-side contact component is one matched pair;
* its tile-adjacency graph contains a k-by-k square-grid minor.

**Proof.** Subdivide the homothetic triangle 2k R by its ordinary triangular
grid. If p,q are the two side vectors of R from one corner, its tiles are

    D(i,j) = conv(ip+jq, (i+1)p+jq, ip+(j+1)q),
    U(i,j) = conv((i+1)p+jq, ip+(j+1)q, (i+1)p+(j+1)q),

for i,j nonnegative and i+j at most 2k-1 for D, or 2k-2 for U.
The U tile is a translated half-turn of D. Every contact is a full side
matched to a full side, so its side-contact component is a single edge.

For 0<=i,j<k, both D(i,j) and U(i,j) exist. Contract their shared diagonal
in the tile-adjacency graph. The resulting k² parallelogram cells have the
horizontal and vertical adjacencies of a k-by-k grid. Delete all other
vertices and edges. This proves the minor assertion. QED.

For completeness, that grid requires tree-decomposition bags of size at
least k. Consider all connected crosses consisting of one grid row and
one grid column. Any two crosses intersect. In a tree decomposition, the
bags meeting one connected cross form a subtree; these subtrees pairwise
intersect and therefore share a bag, by the elementary Helly property for
subtrees of a tree. This bag meets every cross. Fewer than k grid vertices
miss some row and some column, hence miss their cross. Thus the common
bag has at least k vertices. Contracting graph edges never increases
treewidth: replace both endpoint labels by the contracted label in each
bag. Consequently the original tile graph has treewidth at least k-1.

This rules out deriving a uniform bound on the width of **every actual
certificate** from caterpillar seams, finite seam states, integer atoms,
or a bounded number of orientations. All those local properties already
hold in this family, in their simplest form.

The width obstruction also persists within any fixed nonsimilar tile/target
pair already having a tiling. Scale that whole tiling by 2k and subdivide
each enlarged tile into its ordinary unit grid. The target remains
nonsimilar to the fixed unit tile; the number of orientations stays bounded
by twice the original number, independently of k. A single enlarged tile
already contains the preceding grid minor. The seams between enlarged
tiles need not be matched pairs, but they still obey the same fixed-tile
finite seam automaton and caterpillar theorem.

## The minimum width over alternative tilings also grows

The preceding explicit example can be strengthened to a geometric bound
that applies to **every** tiling of the same target, regardless of its
orientations or seam pattern.

**Theorem.** Suppose a triangular target contains a square of side L,
and every congruent tile has diameter C. Put `k=floor(L/(2C))`. For
`k>=1`, the positive-length tile-contact graph of every tiling has
treewidth at least k-1.

**Proof.** Inside the square choose k horizontal and k vertical segments
spanning it, with spacing greater than C within each parallel family.
For example, start at spacings 2C and perturb slightly. Choose the
perturbations generically so that the segments miss all tile vertices,
no segment is collinear with a tile edge, and each horizontal/vertical
crossing is in a tile interior. Only finitely many forbidden positions
must be avoided.

Let H_i and V_j be the sets of tiles whose interiors meet the corresponding
segments. Each is connected in the contact graph: a segment passes from
one tile to the next through the relative interior of a common atom.
The H_i are pairwise disjoint, as are the V_j, because the diameter of
one tile is at most C. Each H_i meets each V_j in the tile containing
their crossing.

The connected sets `H_i union V_j` therefore pairwise intersect. Fewer
than k tiles miss some H_i and some V_j and hence miss their union.
The same subtree-Helly argument used above implies that some bag in any
tree decomposition meets all these sets, and thus has at least k
vertices. This proves the bound. QED.

A target of inradius r contains a square of side `sqrt(2)r`, so the bound
is `floor(r/(sqrt(2)C))-1`. Under homothety of any fixed tileable target
while retaining the same unit tile, this grows linearly with the scale.
It holds for all alternative tilings as well as the original certificate.

Consequently a uniform bounded-treewidth normal form is impossible even
when alternatives are allowed. This still does not refute a finite
parametric grammar: a single grid recipe already describes the explicit
family above, despite the necessary large width of its expansions.
An adequate grammar must allow grid macros or comparably powerful
operations with interfaces whose lengths can grow. A finite set of
one-dimensional seam states alone does not supply those operations.

## Why pumping one seam does not pump a triangular disk

A repeated signed-offset state in the seam automaton permits insertion
of a further matched interval into that isolated seam. It supplies neither
the other two sides of its incident triangles nor a filling of the added
area.

There is also a simple boundary obstruction to interpreting this as a
translation of one complete crosscut strip. Suppose two crosscuts join
the same two nonparallel sides of a triangle, and a translation v maps
the first crosscut and its designated endpoints to the second. If both
endpoints must remain on their respective original supporting lines,
then v is parallel to both lines. Hence v=0. A nontrivial translated
crosscut pump cannot preserve these triangular boundary incidences.

This leaves coupled multi-strip constructions, changes to the target
scale, and more general retilings open. The existing cyclic trapezoid
constructions are examples of coordinated operations of this kind.

## Exact certificates nevertheless have polynomial verification

For a fixed integer-sided tile with largest side C, a genuine triangular
N-tiling has `V<=N+2`, `E<=2N+1`, and at most `4N-1` face-edge incidences,
after omitting artificial subdivision points, by the
[seam-certificate count](../exact-seam-certificates.md). Vertex IDs and
dart pairings therefore use O(N log N) bits. Encoding repeated whole-side
lengths gives total input size `O(N(log N+log(C+1)))`; using labels a,b,c
instead requires only one global copy of the side data.

There is a compatible bound for the exact rational development. Put

    H=(a+b+c)(-a+b+c)(a-b+c)(a+b-c),
    D=2abc,

and represent the Euclidean point `x+i sqrt(H)y` by `(x,y)`. Reference
triangle corners, their unit edge vectors, and integer atom offsets have
rational coordinates with denominators dividing D. Across an adjacent
pair of faces, the relative rotation is the product of one such unit
edge direction and the conjugate of another, so its two rational
coefficients have denominators dividing D².

Along a spanning-tree path with at most N-1 adjacency steps, the resulting
vertex coordinates consequently have denominators dividing `D^(2N-1)`.
Their Euclidean magnitudes are O(NC), because a path of at most N faces
connects them to the root face. As H is a positive integer, the rational
coordinate magnitudes are bounded by the same order. Their bit lengths
are therefore `O(N log(C+1)+log N)`; H itself has O(log(C+1)) bits.

Topology, seam reconstruction, consistency across all paired atoms and
vertices, and the triangular developed-boundary test all use polynomially
many exact rational operations on numbers of these bit lengths. The
[development theorem](disk-realization-2026-10-06.md) then proves
non-overlap. Thus this is a polynomial verification procedure in N and
log(C+1), despite the unavoidable large graph width.

Under the separately stated classified bound `C<=(N+1)^2`, the compact
certificate has O(N log N) bits and verification is polynomial in N.
Here N is its numerical value, not its binary input length; this is not
an assertion of NP membership with an O(log N)-bit instance encoding.
It is also not a new fixed-N decidability theorem or an arithmetic
classification of all counts.

## Outstanding requirement

An actual positive normalization theorem must therefore produce a tiled
macroregion with a proved boundary interface and a proved replacement;
neither repetition of a one-dimensional seam state nor a fixed list of
tile directions supplies it. No such universal replacement is proved here.

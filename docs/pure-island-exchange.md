# Pure inward islands: chirality duality and the deformation obstruction

4 October 2026. Denis Paliy, research with ChatGPT assistance.
No chirality-switch theorem or positive counterexample is claimed in this
note. The formal-cochain argument below received a separate internal
mathematical audit; external acceptance is not asserted.

## Question

Let a scalene integral 120-degree triangle have short sides a,b and long
side c, with D=c²=a²+ab+b². A pure inward island is tiled by rotations
of one handed state: all short edges have one direction class modulo
π/3, every long edge has the adjacent lower class, and the whole polygon
boundary has only that long-edge class.

The open replacement question is whether the same polygon always admits
the reflected pure state with the same unit triangle. A replacement may
change all internal incidences and must allow arbitrary T-junctions.

The existing positive regular-hexagon example, thin-strip exclusions,
boundary inventories, and failed annulus are taken as established prior
work; none is a resolution of this question.

## An exact obstruction to continuous shape deformation

**Proposition.** A nonempty fixed polygon cannot admit a continuous family
of finite tilings by congruent 120-degree triangles with fixed long-side
length c while the ratio of the two short sides varies continuously.
For a convex all-c polygon the boundary condition itself forces c to
remain fixed. The same conclusion holds after an overall similarity
normalization that keeps the polygon and c fixed.

Here continuity means that the side lengths are positive continuous
functions. The statement does not require edge-to-edge tilings or fixed
internal incidence data.

**Proof.** Area gives A=N(t)(√3/4)a(t)b(t). Since a(t)b(t) is positive and continuous,
N(t) is integer-valued and continuous, so it too is constant. Consequently
both a(t)b(t) and a(t)²+a(t)b(t)+b(t)²=c² are fixed. Thus a(t)+b(t) is fixed,
and the unordered pair {a(t),b(t)} is fixed. A continuous exchange of two
distinct positive values is impossible.

For the convex-boundary assertion, pick a genuine boundary side of
length S. It is partitioned into whole c-edges, so S=m(t)c(t) with a
positive integer m(t). Continuity makes m(t), hence c(t), constant.
At a convex corner a tile edge cannot extend past that corner along
the same line. Arbitrary internal T-junctions do not affect the argument. ∎

For a nonconvex polygon, an edge can pass through a reflex boundary
corner and continue into the interior. Its boundary portion need not
be a whole c-edge. The proposition therefore assumes c fixed in that
generality; it does not infer this from an arbitrary nonconvex boundary.

In particular, continuously varying a/b to b/a, normalizing c to keep
the c-boundary polygon fixed, cannot prove the desired chirality switch.
The intermediate triangle at a=b has the wrong area. This remains an
obstruction even if one permits internal combinatorial changes during
the deformation. Regularity of the angle counts at vertices cannot
remove it.

## The explicit defect in the natural short-frame transpose

Let ρ=exp(iπ/3). Use the short-direction frame with reference triangle

    0, a, w=a+b−bρ.

Its c-edge is w and its area is γab, where γ=√3/4. Swapping a and b
produces the opposite handed state after rotating its c-edge back to
the original direction.

The natural linear transpose keeps each tile's rotation index in this
short frame and sets

    a_t=(1−t)a+tb,
    b_t=(1−t)b+ta,
    w_t=a_t+b_t−b_tρ.

Put q=t(1−t) and Δ=a−b. Then

    a_t b_t = ab+qΔ²,
    |w_t|² = D−qΔ².

If an interpolated boundary keeps the same oriented c-edge indices,
it is a similarity of the initial boundary by w_t/w. Its signed area
is therefore

    A_boundary(t)=A_boundary(0)(D−qΔ²)/D.

But N interpolated positive tiles have total area

    A_tiles(t)=Nγ(ab+qΔ²).

Using A_boundary(0)=Nγab, the discrepancy is exactly

    A_tiles(t)−A_boundary(t)
      = Nγ qΔ²(a+b)²/D > 0       (0<t<1, a≠b).

Thus these data cannot define a tiling, or even a consistent oriented
planar cell decomposition with cancellation of its internal edges.
At t=1/2, both short sides are s=(a+b)/2: the boundary area factor is
3s²/D, whereas the tile-area factor is s²/(ab).

This also rules out a proposed endpoint a↔b correspondence whenever its
incidence data really are linearly interpolatable in this way. For
example, in a convex island the established whole-c-edge matching lemma
removes c-edge phase issues. If corresponding tiles keep their rotation
indices, corresponding short-edge chains retain the same ordered
T-junction incidences, and the boundary is tracked with its oriented
c-edge indices fixed, linear interpolation preserves the incidences.
Signed-area cancellation then yields the contradiction above.

The qualifications matter. A global reflection of a reflection-symmetric
polygon reverses direction and boundary indices, so is not excluded.
Nor does this calculation rule out a genuinely new tiling with different
incidences. For nonconvex islands, partially overlapping c-edge chains
can have changing subdivision phases; no unrestricted interpolation
claim about those chains is being made.

## Why the ordinary edge-to-edge setting cannot suffice

**Lemma.** A nonempty pure all-c island for a scalene triangle cannot have
an edge-to-edge tiling in the usual whole-edge sense.

**Proof.** The permitted triangles are the six rotations of a fixed
triangle by multiples of π/3. Along a shared complete edge, its length
identifies its side type. Two copies sharing that edge and lying on
opposite sides must consequently differ by a half-turn. Positive-length
adjacency is connected in a connected polygonal region, so all triangles
have just one orientation or its half-turn. Their c-edges are therefore
all parallel. If the whole boundary consists of c-edges, its edges are
all parallel, which is impossible for a positive-area bounded region. ∎

Thus T-junction arithmetic is essential in every pure island, including
the known positive examples. Along a maximal short-edge chain one can
have

    ma+nb=m'a+n'b

without separate equality of the a- and b-counts. Swapping a and b
generally destroys this equality. When a≠b, requiring both the original
and swapped equalities forces m=m' and n=n'. A weighted-lozenge argument
must therefore reconstruct these chains, rather than simply relabel
their edge lengths.

## A forced arithmetic exchange inside every convex island

The preceding obstruction gives a stronger structural statement than
the mere existence of a T-junction.

**Theorem.** In every nonempty convex pure all-c island, there is an
internal straight short-edge interval whose two partitions into complete
a- and b-edges have different separate counts of a-edges and b-edges.
Consequently a/b must be rational. If a and b are positive integers,
the island contains such an interval of length at least

    lcm(a,b)=ab/gcd(a,b).

In particular the lower bound is ab for a primitive integral norm
triple. The statement permits arbitrary short-edge T-junctions.

**Proof.** First, every interior c-edge is shared in full. A maximal connected
collinear component of c-edges has, on each side, a partition into whole
c-edges of the same length. Both partitions start at the same component
endpoint and therefore coincide. No short edge can overlap this line:
the c-direction class is distinct from the short-direction class. If
the line is an exterior supporting line, convexity instead gives one
partition into whole c-edges on the boundary. Thus every interior
c-edge is fully matched and every boundary side has whole c-edges.

Take a maximal connected collinear union J of short edges. Since the
target boundary has no short directions, the two sides of J are
partitions of the same interval into complete a- and b-edges. Cut J at
every common endpoint of its two partitions. Call the resulting
intervals overlap blocks. Each block has two complete-edge partitions,
with common initial and final endpoints.

Suppose every overlap block has equal separate a- and b-counts in its
two partitions. Introduce formal real variables A and B. In a directed
block, give a partition endpoint the formal distance mA+nB from the
initial endpoint, where the corresponding prefix has m a-edges and n
b-edges. This assignment agrees whenever a vertex is an endpoint in
both partitions: those are precisely the cuts, and the separate counts
agree on each intervening block. Therefore each subsegment in the
combined subdivision of the block has a well-defined formal vector,
its formal scalar distance times the fixed short-direction unit vector.

On a c-edge of rotation index j assign the formal vector

    ρ^j(A+B−Bρ),

with the appropriate sign. Whole-c-edge matching makes this assignment
consistent across its two incident tiles. Subdivide the planar tiling
at all its T-junctions. Around each tile the formal vectors sum to zero:
its short sides telescope to their prescribed A- and B-vectors, and
its c-side is their sum. Thus this vector-valued cochain is closed on
every face of a cell decomposition of a disk. Integrating along paths
gives formal coordinates for every vertex; independence of path follows
by summing the tile-face identities inside a closed path.

In those formal coordinates each tile has signed area γAB, where
γ=√3/4. Every boundary edge has its original vector multiplied by

    (A+B−Bρ)/(a+b−bρ).

Consequently formal signed-area cancellation over the cell decomposition
would give the polynomial identity

    NγAB = (Area(P)/D)(A²+AB+B²).

No positive-area polygon can satisfy this identity: the right-hand
coefficient of A² is Area(P)/D>0, while the left-hand coefficient is
zero. This contradiction proves the existence of an unbalanced block.
This is a formal area argument; it does not assume that the resulting
formal coordinates embed without crossings for arbitrary A,B.

For that block write its two partition counts as (m,n) and (m',n').
Their common actual length gives

    (m−m')a+(n−n')b=0,

with a nonzero integer pair of differences. This already forces a/b
to be rational. For integer a,b, put g=gcd(a,b), and reverse the two
partitions if necessary. Then

    m−m'=(b/g)k,    n−n'=−(a/g)k,    k≥1.

The first partition has m≥b/g a-edges, so the interval has length at
least ma≥ab/g. ∎

This theorem does not contradict the existing islands: their large
grid blocks contain precisely such arithmetic exchanges. It also does
not furnish chirality switching. It identifies a place where any
combinatorial duality has to change the short-edge partition data.

## Consequence for the current reduction

The [positive nested-patch cut identity](height-cut-area.md) supplies
actual geometric islands;
it removes an earlier signed-cycle ambiguity. It does not supply their
chirality duality. The all-c boundary condition is strong enough to
obstruct the proposed continuous regular deformation, while still
leaving open a discrete retiling with changed internal combinatorics.

A useful next lemma must directly construct such a discrete replacement,
or give an actual positive one-state island together with an invariant
excluding the other state. A construction only after dilation does not
settle same-polygon replacement. No such replacement or counterexample
has been obtained here.

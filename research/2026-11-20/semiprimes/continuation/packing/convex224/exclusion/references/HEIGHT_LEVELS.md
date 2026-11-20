# Orientation-level divisibility for I120

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
This is a necessary condition; 154 remains unresolved.

Let `(a,b,c)` be primitive, with `c²=a²+ab+b²`, and put

    rho = exp(i*pi/3),  z = (a+b*rho)/c.

Normalize an I120 target so its base is horizontal. Its count and side
lengths are `N=b(a+2b)m²` and `(bcm,bcm,b(a+2b)m)`. Every edge direction
of any tiling has a unique integer height h modulo rotations by pi/3:
its direction is `rho^j z^h`. This follows by propagating directions
through positive-length tile contacts; irrationality of arg(z)/pi gives
uniqueness. The two short edges of a tile have a common height h, and
its c-edge has height h+1 or h-1. Write n_h for the number of tiles
whose short edges have height h.

**Theorem.** In any actual I120 tiling, allowing arbitrary T-junctions,

    c divides n_h for every h != 0,
    n_0 = N (mod c).

There are at most `floor(N/c)+1` occupied heights. The same divisibility
holds for equilateral targets with horizontal side and for the F1
normalization whose two unrotated exterior directions have height 0.

## Whole-edge chain identity

Use the median-cut identity in [the existing cut theorem](../../docs/height-cut-area.md).
For an integer k, let H_k be the union of actual tiles with short-edge
height greater than k, and B_>k the part of the counterclockwise target
boundary whose edge heights exceed k. Then

    C_k = boundary(H_k) - B_>k

is a signed sum of whole c-edges. Specifically, a tile of short-edge
height k with c-height k+1 contributes its negative c-edge, and a tile
of short-edge height k+1 with c-height k contributes its positive c-edge.
All other tiles contribute zero. Cancellation on atomic contacts proves
the identity even when a c-edge on one side meets several short edges
on the other. No assertion that H_k's own boundary consists of its own
c-edges is used.

All selected displacement vectors lie in the lattice

    M_k = z^k [c Z[rho] + (a+b*rho) Z[rho]].

Its index in the rotated Eisenstein lattice is c. In the basis 1,rho
the four generators are

    (c,0), (0,c), (a,b), (-b,a+b).

Their two-by-two determinants have greatest common divisor
`gcd(c²,ca,cb,c(a+b))=c`, using primitivity and the norm equation.
Thus M_k has fundamental area `c*sqrt(3)/2`.

Any closed directed walk with steps in M_k has signed area in
`(c*sqrt(3)/4) Z`, by translating its first vertex to zero and applying
the shoelace formula in a lattice basis. A balanced signed sum of whole
edges decomposes into such walks. Coincident edges, self-intersections,
and different translations of different components cause no difficulty.
The area of one tile is `ab*sqrt(3)/4`, and `gcd(ab,c)=1`. Consequently,
whenever the chain is the boundary of an actual union of tiles, its
tile count is divisible by c.

## Closing the I120 cuts

The target boundary signature is

    mb(a+2b) + mbc*rho²*z - mbc*rho*z^(-1).

Its exterior heights are 0,1,-1. For k>=1, B_>k is empty, so C_k is
the boundary of H_k and c divides its tile count. For k<=-2, B_>k is
the entire target boundary; -C_k bounds its complementary tile union,
whose count is therefore divisible by c.

For k=0, B_>0 is the single exterior side of height 1. Its whole
displacement is `mbc*rho²*z`, which belongs to M_0. Adding this one
whole segment to C_0 gives the closed chain boundary(H_0), so c divides
the number of tiles of positive height.

For k=-1, let B_<=-1 be the single exterior side of height -1. Its
displacement `-mbc*rho*z^(-1)` belongs to M_-1. The chain

    -C_-1 + B_<=-1 = boundary(target minus H_-1)

therefore gives divisibility for the total number of negative-height
tiles. Differences of consecutive cumulative counts give `c | n_h`
for each h != 0. Subtract from N to obtain the congruence for n_0.

The height-count bound follows because each occupied nonzero height
contains at least c tiles. For an equilateral target all exterior
heights are zero, so the outside-cut argument alone applies. For F1,
the exterior heights are 0,0,-1 and the height -1 side has length bcm;
the same single-side closure applies.

## F2 and F3: the exceptional level is 2

The same chain argument gives a uniform result for the two remaining
norm targets.
Put `U=a+2b`, `V=2a+b`, `W=a+b`, and use the canonical horizontal
side `OB=mc²` in both cases. Their third vertices are

    F2: C = maU z²,       C-B = mbV rho z²;
    F3: C = mcU z³,       C-B = 3mbW rho z².

These vector identities follow from
`aU-conj(a+b*rho)²=bV*rho` and
`U(a+b*rho)-conj(a+b*rho)²=3bW*rho`.

Thus F2 has exterior heights 0,2,2 and F3 has exterior heights 0,2,3.
For k=0 or k=1, B_>k consists of both nonhorizontal exterior sides.
Subtract the horizontal whole segment OB from C_k; the resulting
closed chain is `boundary(H_k)-boundary(target)`. The displacement
`mc²` lies in both M_0 and M_1, since

    c² / z = c conj(a+b*rho) in c Z[rho].

Consequently `|H_0|=|H_1|=N (mod c)`. For F2, B_>2 is empty. For F3,
B_>2 is the side CO, with displacement `-mcU z³` in M_2; adding that
one segment gives `c | |H_2|`. All more distant cuts have empty or
complete exterior chains. Taking differences proves:

**F2/F3 theorem.** Every short-height population other than n_2 is
divisible by c, and `n_2=N (mod c)`, with arbitrary T-junctions.

The existing actual certificates give:

| Target | Tile | Nonzero short-height populations |
|---|---|---|
| F3, N=990 | (8,7,13) | n_1=455, n_2=535 |
| F3, N=19320 | (24,11,31) | n_1=11532, n_2=7788 |

In particular, the first row also rules out replacing c by c² in this
uniform F2/F3 conclusion: `455` is divisible by 13 and not by 169.
This does not decide the I120-specific possibility of a stronger bound.

## Consequence and limitation for 154

For `(8,7,13)` this proves

    n_h = 0 (mod 13) for h != 0,
    n_0 = 11 (mod 13),
    number of occupied heights <= 12.

It does not prove `N>=c²`. In particular, the positive but unplaced
inventory already recorded for 154 can be padded entirely at height 0
to give `(n_0,n_1)=(141,13)`, which passes this theorem. Neither that
inventory nor this congruence settles its geometric realizability.

## Why this cut argument cannot give c-squared divisibility

There is a direct positive-region counterexample to such an upgrade.
Consider the parallelogram with side vectors `c` and `ac z`. Divide its
second side into c pieces of vector `a z`, and split each resulting
parallelogram into two triangles. Since

    c - a z = b z rho^(-1),

the resulting `2c` triangles are copies of the original tile, all with
short-edge height 1 and c-edge height 0. The boundary is a closed walk
of whole c-steps: its two lengths are c and ac, with direction heights
0 and 1. Its tile count is 2c, which is not divisible by c² for c>2.

On the long sides these artificial c-steps need not be edges of the
displayed tiles. Thus this example does not refute a stronger assertion
requiring every boundary step to be a whole edge of an incident tile;
it isolates the limitation of the lattice-step and positive-area data.

For `(5,3,7)` the parallelogram vertices are
`(0,0),(7,0),(32,15),(25,15)` and it contains exactly 14 tiles. Thus a
positive union and a closed whole-c-step boundary alone cannot imply
c² divisibility. This parallelogram is not asserted to occur as an
orientation component in an I120 tiling; a theorem using additional
global restrictions would require an independent argument.

The attached checker verifies the lattice determinants on all primitive
plus-norm triples with `2<=b<a<=500` and tests the level counts on
an actual equilateral tiling and an actual I120 tiling obtained by the
existing equilateral construction and two standard triangle attachments.
It also checks the 14-tile parallelogram and all of its 91 tile pairs.
It does not replace the whole-edge-chain proof above with finite testing.

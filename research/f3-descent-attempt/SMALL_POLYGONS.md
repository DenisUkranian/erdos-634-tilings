# A small-count rigidity theorem for balanced three-direction polygons

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026.**

This theorem excludes one natural auxiliary construction for the F3
frontier. It does not exclude the full 54-tile parallelogram associated
with 990, nor any F3 scale-one target. In particular, a different positive
corner construction is compatible with this obstruction.

Let `a,b,c` be a primitive positive integer triple with

    c²=a²+ab+b².

Write `ρ=exp(iπ/3)`, `Z=a+bρ`, `z=Z/c`, and `δ=a−b`. The reference tile
is `R=conv(0,a,Z)`. Its two short-edge directions have height zero, and
its c-edge direction has height one, where a direction `z^h ρ^j` has
height `h`.

**Theorem.** Let P be a positive-area convex polygon all of whose side
directions are `ρ^j`, and suppose that its alternating directed boundary
length is zero:

    Σ (directed side length) (-1)^j = 0.                 (1)

If P is tiled by `N≤2c` copies of R, allowing reflections and T-junctions,
then every tile has short-edge height zero. All its c-edges pair
whole-to-whole, and P consequently has a tiling by `N/2` parallelograms
with adjacent sides a,b and angles 60 and 120 degrees.

Every centrally symmetric polygon with these three side axes satisfies
(1). This includes the parallelograms to which the corollary below applies.
The zero-boundary-character assumption must not be omitted: an equilateral
triangle generally fails (1).

**Corollary.** The 60-degree parallelogram with adjacent side lengths
`ab,c` has no tiling by the primitive `(a,b,c)` triangle. Its area would
require exactly `2c` copies.

For `(a,b,c)=(8,7,13)`, this rules out the 26-tile parallelogram with sides
56 and 13. Thus decomposing the 56-by-27 F3 auxiliary parallelogram into
widths `13+7+7` cannot provide a positive construction by three such
strips. It says nothing against tiling the full 54-tile region by another
partition.

## 1. Direction propagation and primitive arithmetic

The number `θ=arg Z` is an irrational multiple of π. Indeed,
`2cos θ=(2a+b)/c` is rational and strictly between 1 and 2; if θ were a
rational multiple of π it would be a rational algebraic integer.
Therefore the representation of a direction as `hθ+jπ/3` has unique
integer h and unique j modulo 6.

Starting with a tile on a boundary side, and propagating through
positive-length edge contacts, shows that every directed tile edge has
this form. A path through the target can avoid the finite vertex set, so
positive-length contact connectivity does not require whole-edge matching.
Every tile is a translate of either `z^h ρ^j R` or `z^h ρ^j conjugate(R)`.
Call these the positive and reflected chirality at short height h.

Primitivity implies `gcd(a,b)=gcd(a,c)=gcd(b,c)=1`. Also c is odd. Finally,

    gcd(δ,c)=1.                                         (2)

If a prime divided δ and c, it would divide `3ab`, so it could only be 3.
But `3|c` would imply `a≡b≠0 (mod 3)` and
`a²+ab+b²≡3 (mod 9)`, contradicting `9|c²`.
The equality δ=0 is impossible, since it would give `c²=3a²`.

## 2. Exact chirality-sign factorization

For a directed edge of height h and rotation j assign the formal value
`length·(-1)^j X^h`. Reversing its direction reverses this value.
Internal edge segments cancel after splitting all T-junctions. The
counterclockwise boundary values of the two reference chiralities are

    Φ(R)=δ−cX,
    Φ(conjugate(R))=−δ+cX⁻¹.

For each h, let U_h be the even-minus-odd rotation count of positive
chirality tiles, and let V_h be the **odd-minus-even** rotation count of
reflected tiles. Set `U=ΣU_h X^h` and `V=ΣV_h X^h`.
The sign convention for V incorporates the reversed boundary traversal.
Condition (1) gives the Laurent identity

    (δ−cX)U+(δ−cX⁻¹)V=0.                               (3)

The two linear factors `δ−cX` and `δX−c` are coprime over Q, since
`δ²≠c²`. They are primitive integer polynomials by (2). Euclid's lemma
over Q and Gauss's lemma over Z therefore give an integer Laurent
polynomial W such that

    U=(δX−c)W,
    V=−X(δ−cX)W.                                       (4)

This is an exact necessary identity for an actual tiling, not a geometric
construction from a formal orientation inventory.

If W is nonzero, its lowest and highest nonzero coefficients are
nonzero integers. The extreme coefficients of `(δX−c)W` have absolute
values at least c and `|δ|`, respectively; its support has distinct
endpoints. The same argument applies to `−X(δ−cX)W`, in reverse order.
Consequently

    N ≥ ||U||₁+||V||₁ ≥ 2(c+|δ|).                      (5)

No estimate of intermediate coefficients is needed; their cancellations
cannot remove the two extreme terms of either product. Since δ is
nonzero, `N≤2c` forces `W=U=V=0`. At each short height, the number of
tiles of either chirality is therefore even, and hence the total
height population is even.

## 3. Every nonzero short height has population divisible by c

Here is the lattice-cut argument, stated to keep the dependencies explicit.
It is the 120-degree specialization of the positive median-cut identity
in [the height-cut note](../../docs/height-cut-area.md).

For an integer k, let H_k be the actual union of tiles whose short height
exceeds k. Subtract from its oriented boundary the target boundary edges
whose heights exceed k. The result C_k is a sum of selected **whole
c-edges**. Their heights are k or `k+1`: a tile has two short edges at
h and its long edge at `h+1` or `h−1`, and the median-height cut selects
exactly the minority edge.

The permitted selected edge vectors generate, up to the rotation `z^k`,
the integer lattice

    M = c Z[ρ] + Z Z[ρ].

In coordinates `(1,ρ)` its generator columns are

    (c,0), (0,c), (a,b), (−b,a+b).

Their 2-by-2 minors have greatest common divisor c: all are divisible
by c, while the minors include `c²,ca,cb`, and `gcd(a,b,c)=1`.
Thus M has index c in the unit Eisenstein lattice and fundamental
Euclidean area `c√3/2`.

All target sides have height zero. For `k≥0`, C_k is the boundary of
H_k; for `k<0`, it is the boundary of H_k minus the full target boundary.
In either case it is a balanced whole-edge chain. Decompose it into
closed whole-edge walks. Each walk, after translating its starting
point, lies in the stated lattice; its signed area is a multiple of
`c√3/4`. Summing areas measures respectively the positive tile union
H_k or its complement with a sign. Each tile has area `ab√3/4`.
Since `gcd(ab,c)=1`, the corresponding tile count is divisible by c.

Taking differences of successive cuts proves

    c divides n_h for every h≠0,                       (6)

where n_h is the total number of tiles of short height h.
Neither simple connectivity nor convexity of the cut unions is needed.
The argument uses their actual positive area; it does not replace them
by arbitrary signed formal polygons.

## 4. Small counts force only the boundary height

By Sections 2 and 3, every positive n_h with `h≠0` is an even positive
multiple of the odd number c, and is at least `2c`. If such a height
occurs when `N≤2c`, then `N=2c` and `n_0=0`.

In that event every tile edge on the target boundary is a c-edge: short
edges have nonzero height, whereas every boundary side has height zero.
Because the target is convex, each boundary tile edge is whole, so each
target side has length an integer multiple of c. All target vertices
belong to one translate of `c Z[ρ]`. Its area is consequently a multiple
of `c²√3/4` by the shoelace formula. Comparing with the actual tile area
gives

    c² divides N ab = 2c ab,

and thus `c|2ab`, impossible because `gcd(c,2ab)=1` and `c>1`.
This contradiction proves that every tile has short height zero.

The c-edge directions of the two chiralities have heights +1 and −1,
which are distinct. No short edge can overlap a c-edge, and no c-edge
lies on the target boundary. On every maximal collinear c-edge interval,
both sides partition the same interval into whole edges of the equal
length c, starting at its common endpoint. The partitions agree.
Thus every c-edge matches one whole c-edge of the same chirality. The
two incident tiles are half-turn copies, and their union is the claimed
a-by-b parallelogram. This proves the theorem.

## 5. The strip contradiction

The parallelogram with sides ab,c has zero alternating boundary character
and area requiring `N=2c`. If tiled, the theorem would make every external
edge a short tile edge. In particular, its side of length c would be a
nonnegative integer combination of a and b.

But `max(a,b)<c<a+b`. Such a combination cannot use both generators, and
a pure multiple of either is ruled out by the coprimality with c and
`min(a,b)>1`. This proves the corollary.

The mathematical argument was independently reviewed internally. No
external priority, referee acceptance, or full F3 classification is
claimed. The crucial cutoff is `N≤2c`; it cannot be applied to the
54-tile `(8,7,13)` auxiliary region, since `54>26`.

# Exact enumeration of prescribed F2 notch quadrilaterals

Let `rho = exp(i*pi/3)`, `z=(a+b*rho)/c` and let the angle at the
origin have rays 1 and z. Remove the closed-interior corner triangle
with radial intercepts (kc,ka) from the triangle with intercepts
(ta,tc), taking the closure of the difference. The quadrilateral in
Eisenstein coordinates has counterclockwise vertices
`(ta,0), (ta,tb), (k*a*a/c,k*a*b/c), (kc,0)`.
A tiling would have t²−k² tiles. The following exclusions apply to these
specified quadrilaterals. A full original triangle could avoid the notch.

The exhaustive replays exclude the 105, 147, 117, and 195 quadrilaterals,
as well as the 206 and 250 pentagons formed by one-step extensions.
The 250 certificate exhausts 31 disjoint parts of its complete palette
in 5,331,660 search visits, with no initial placement prescribed. The positive construction later in the note
gives an independently checkable 171-tile quadrilateral and covers
an infinite sufficient range.

## Why only the listed heights need be tested

Write R = Z[rho]. Height h denotes an edge direction rho^j z^h.
Each tile has short sides at a height h and long side at h+1 or h−1.
The exterior provides the normalization, and propagation through
positive-length contacts gives all tile orientations, allowing reflected
tiles and full or partial contacts. The direction exponent is unique
since z is not a root of unity for these primitive triples.
Let n_h count tiles at short height h. Then

    n_0 = t² (mod c),   n_1 = −k² (mod c),
    n_h = 0 (mod c) at all other heights.

To prove this, compare the purported tiling with the formal difference
between the aligned quadratic subdivision of the first triangle (t²
tiles at short height 0) and the aligned subdivision of the removed one
(k² tiles at short height 1). Both 2-chains have the same oriented
boundary, even at T-junctions. Cut each tile population by short height
above H and compare the boundaries. The exterior high-direction chain
cancels. The difference is a closed signed sum of whole long edges at
H and H+1. Indeed the discrepancy between projecting a tile boundary onto
edge heights above H and retaining its whole boundary according to short
height is only its long edge when its short and long heights straddle H.
An equality of subdivided 1-chains suffices: the remaining whole-edge
chain has zero endpoint boundary and can be arranged in closed walks.

The steps of each walk belong to the rotated lattice
z^H(cR + (a+b*rho)R). The latter before rotation has index c in R:
its determinant divisors, from the basis generators c, c*rho,
a+b*rho, (a+b*rho)*rho, have gcd c (use gcd(a,b)=1 and
norm(a+b*rho)=c²). Shoelace, translated separately in each walk,
makes the doubled signed area in Eisenstein coordinates a multiple of c.
A tile has doubled area ab, coprime to c. This proves the congruence
on every cumulative population difference and hence on each height.

The existing single-height line-count theorem `LINE_COUNTS.md` applies
at every exterior-free height: n_h=0 or n_h>=2c. Indeed every exterior
edge has height 0 or 1. In addition, if a height separates a nonempty
outside group from {0,1} but is vacant, the same cut applied to the
outside alone has no exterior contribution and only whole long edges on
that one vacant height. Its step lattice is z^h*cR, of index c² up to
rotation. Hence its nonzero tile count is a multiple of c². The boards
tested below have fewer than c² tiles. Thus the occupied heights outside
{0,1} have no intermediate gaps. Neither argument assumes a face-to-face
tiling, a vertex lattice, or a corner subdivision in the quadrilateral.

|a,b,c|t,k|area|least residues at 0,1|remaining|height palettes sufficient|
|---|---|---:|---|---:|---|
|33,7,37|13,8|105|21,10|74|[-1,1] or [0,2]|
|33,7,37|26,23|147|10,26|111|[-1,1] or [0,2]|
|35,13,43|11,2|117|35,39|43|[0,1]|
|35,13,43|22,17|195|11,12|172|[-2,1], [-1,2], or [0,3]|

In the first and third rows, respectively, the palettes can also be
derived without the vacant-height argument. For 105, at most one outside
height is occupied and adjacent tiles have short heights differing by
at most two, so it lies between −2 and 3. The replay for 105 uses the
larger palettes [-2,1] and [0,3].

## Signed inventories for the quadrilateral and the extended pentagon

For a tile at short height h, read the orientation of its a-edge
counterclockwise and write it as rho^e*z^h. Its sign is (−1)^e. Let
G_h be the signed tile population. Write d=a−b. The oriented side
weights (−1)^e*L and (−1)^(e+h)*L, where L is Euclidean length,
are additive at T-junctions and reverse sign on edge reversal. On one
tile their sums are respectively (d−c)*sign and (d+c)*(−1)^h*sign.
This follows from the reference tile and its rotations and reflections.

In the quadrilateral the formal t-triangle has total signed count t at
height zero (its n² grid of scale n has signed excess n); the k-triangle
being subtracted has signed excess −k at height one. Adding a strip of j
steps increases the height-zero wall weight by −jc, and the height-one
weight by j(a−b), with every other height unchanged. Thus for the entire
pentagon, including j=0 for the quadrilateral,

    sum_{h even} G_h=t,   sum_{h odd}G_h=k+j.

At each height all long edges have signed weight divisible by c, so
dG_h agrees with the exterior weight modulo c. Since gcd(d,c)=1,

    G_0 ≡ t,   G_1 ≡ k+j,   all other G_h ≡ 0   (mod c).

The search also checks G_h=n_h (mod 2) and |G_h|≤n_h. The base replay
disables this optional signed refinement to provide a weaker independent
pruning path.

The signed refinement can separate tiles by whether their long edge is
one height up or down. Denote the two signed sums at short height h by
U_h,V_h. Writing E_h for the exterior weight at height h gives
d*G_h−c*(U_(h−1)+V_(h+1))=E_h and U_h+V_h=G_h. Here E_0=d*t−c*(k+j)
and E_1=d*(k+j)−c*t, and all others vanish. Starting below the occupied
heights, the two recurrences uniquely determine U_h,V_h once the G_h are
known. A partial placement with m_h tiles and used signed sums u_h,v_h
therefore requires m_h+|U_h−u_h|+|V_h−v_h|≤n_h at each height.
This extra filter is disabled by IGNORE_CHIRALITY in the base replay.

### Complete palette reductions for the 195 and 206 boards

For the 195 quadrilateral (35,13,43,t=22,k=17,j=0), n_0 ≡ 11 and
G_0 ≡ 22 modulo 43. An integer congruent to 22 has absolute value at
least 21; hence n_0≥54. Similarly n_1≡12 while G_1≡17, so n_1≥55.
At most 86 tiles remain for exterior-free heights. A single occupied
outside height needs at least 86, and a missed intermediate height would
create a group of at least 43² tiles. Therefore [−1,2] is a complete
palette. Its negative replay suffices for unrestricted nonexistence.

For the 206 pentagon (33,7,37,t=26,k=23,j=1), n_0 ≡ 10 and G_0 ≡ 26
modulo 37; the latter needs |G_0|≥11, so n_0≥47. Also n_1≡11 and
G_1≡24 needs |G_1|≥13, hence n_1≥48. The 111 remaining tiles cannot
support two new heights, each of which costs at least 74. Again [−1,2]
is a complete palette. Its negative replay excludes this prescribed
pentagon with reflections, T-junctions, and no initial restriction
on allowable tiles.

### A side-count bound removes the remote heights on the 250 pentagon

Here (a,b,c,t,k,j)=(35,13,43,22,17,1). The signed and unsigned residues
give n_0≥54 and n_1≥24. Two further occupied heights would each require
at least 86 tiles, forcing equality throughout: n_0=54, n_1=24 and two
populations of 86. Then G_1≡k+j=18 mod 43 and G_1 has the same parity
as n_1, so G_1=18. Only (24−18)/2=3 short-height-one tiles of negative
sign would exist.

Inspect the three consecutive genuine height-one sides, in their
counterclockwise directions. They have lengths 28b along −z, a along
rho^4*z, and 17b along rho^5*z. For either displayed length nb with
n=28 or 17, write nb=Xa+Yb+Zc by the whole tile edges on that wall.
Since nb<ab, both X and Z are less than b; reduction modulo b, using
a+c=6b and gcd(a,b)=1, gives X=Z and Y=n−6Z. On both walls an a-edge
has negative direction character, hence uses a negative height-one tile.
Distinct such edges belong to distinct tiles. Thus the two Z values
sum to at most 3. The middle side has only the single a-edge because
c>a and b does not divide a. At least 28+17+1−5*3=31 short edges of
height one consequently occur on these walls. A tile contributing two
such edges must put its obtuse vertex at one of the two adjacent wall
corners. At most one tile can do so at each corner, and nonadjacent
walls are disjoint. Therefore at least 29 distinct height-one tiles are
required, contradicting n_1=24. Only one additional height is possible,
so [−1,2] is a complete palette here as well. The unseeded corner-fan replay exhausts this palette, so the 250 pentagon is excluded.

Before the geometric search, combining the palette reduction with the two signed edge recurrences leaves
five possible populations, ordered by heights −1,0,1,2. They are
(0,54,110,86), (0,54,196,0), (0,140,110,0), (86,54,110,0), and
(129,54,67,0). The sums G at the two central heights are 22 and 18
except in the last case, where they are 22 and −25 and G_(−1)=43.
These lists follow by enumerating the arithmetic congruences through
total count 250, and do not assert the existence of a configuration.

In general, the same count applies to extended notches with
a+c=u*b, H=(tc−ka)/b integral, n=H+j and k both below a, and a
middle side ja that has only the pure a decomposition. The two b-banks
then require n+k−(u−1)(Z_1+Z_2) short edges. Since Z_1+Z_2≤
(n_1−G_1)/2 and at most two of the j middle edges can meet another
bank in the same short-height-one tile, a necessary inequality is

    (u+1)n_1 − (u−1)G_1 ≥ 2(H+k+2j−2).

This argument uses complete edges on genuine supporting sides and is
unaffected by T-junctions elsewhere in the polygon.

## Exhaustive corner enumeration

For a finite palette the code generates all six rotations at each
height, both choices of a b-edge forming 120 degrees with the a-edge,
and all three choices of anchored corner. The coordinates of these
vectors have denominator dividing c^max(1,abs(h_min),abs(h_max)).
This is not a global lattice assumption on putative tilings. Each
proposed placement is anchored at a vertex exposed by earlier placements,
where at least one tile must meet in a genuine corner.

At a regular strict convex vertex of the remaining region, every
completion contains a full ordered fan of tiles with this apex. The code
enumerates it from the outgoing boundary ray through successive CCW tile
corner sectors to the reverse incoming ray. Interiors of tiles of the
same fan are already separated by their disjoint angular sectors. Each
new tile is contained in the board and its interior is disjoint from
previously placed tiles, by elementary polygon separating-axis tests.
Subtracting its three oriented edges and combining collinear signed
intervals maintains the actual boundary as a 1-chain. The code skips
singular contacts as pivot candidates and reports an inconclusive error
if no regular pivot exists. No completed negative replay encounters that
condition. Choosing any pivot is complete; comparing numbers of compatible
fans only changes traversal order.

A clamped exposed interval, with both endpoints regular convex vertices
or on a supporting line of the genuine board, must be a concatenation of
whole tile edges. An incident tile cannot overhang a strictly convex
endpoint, or overlap the tiles that terminate the exposed interval on a
genuine exterior wall. Its length is therefore an integer sum of the
possible directed side lengths. An optional extra necessary test checks
that each pair of successive exposed tiles can be joined by a complete
angular fan at its common vertex, with analogous tests at clamped ends.
The search respects all feasible populations from the congruence and
line-count bounds. The node budget ends with exit status 2, not a NO.
All geometric decisions, squared lengths, collinear interval operations,
and the length check use integer arithmetic.

Independently check a positive control generated by the same engine with
`python verify_control.py`. Its explicit 171 congruent triangles tile the
(5,3,7), t=14,k=5 quadrilateral. The verifier independently checks
all metric data, every pair's separation, containment, and total area.

## A uniform positive construction for prescribed notches

For every admissible tile with a<c and every positive integer k, the
quadrilateral is tiled whenever

    t ≥ a + c*ceil(k/a).

Use radial coordinates on (1,z). An ac-by-ac grid cell is a union of
complete rectangular cells in both unit grids: one has spacings a,c,
the other c,a. Use the second grid on the union of coarse cells meeting
the interior of kT_o, with that triangle removed. The indices of these
cells are exactly i,j≥0 with ia+jc<k. Their top-right vertices are
inside tT_i when (i+1)c+(j+1)a≤t. To maximize ic+ja subject to ia+jc<k
replace each unit of j by one unit of i: the constraint weakens and
the objective grows. The maximum is therefore c*floor((k−1)/a).
The claimed inequality places every coarse cell inside tT_i. Outside
their union use the first grid. Both original slant sides lie on unit
tile diagonals in their respective grids, and both tilings meet along
coarse-cell boundaries. The construction accounts for the positive
control (a,b,c,t,k)=(5,3,7,14,5), while the smaller unit controls lie
outside this sufficient range.

## Reproduction

Build the base replay with `g++ -O3 -std=c++20 -DIGNORE_CHIRALITY -DIGNORE_SIGNS -DIGNORE_CONTACTS -DREVERSE_TIES dfs.cpp -o notch`.
Run `./notch a b c t k h_min h_max 5000000` for each palette.
The optional final argument j adds a strip of 2j*(tc−ka)/b+j² tiles when the division is exact. Each added strip has formal short height 1, being the difference of two aligned trapezoids with spanning edge vectors c*rho and b*z. For these extended pentagons add the strip size to the short-height-1 residue and to the total count.

The default contact test, disabled in the base replay above, also verifies integral offsets at every vertex touching another tile edge, and possible whole-side sums from both extremities of a true board wall. This follows by considering the maximal connected collinear segment of tile edges, both banks of which are composed of complete tile edges starting at the common initial endpoint.

Macros IGNORE_SIDE_FANS (disable the optional stronger test), REVERSE_TIES
and WALL_FIRST change traversal or pruning. The output NO(in palette)
is an exhaustive conclusion for that one palette. See REPLAY.md for
exact completed runs.

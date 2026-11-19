# Proof development for the 329-tiling exclusion

The final proof and exact reproduction commands are in [RESULT.md](RESULT.md). The sections below retain the intermediate reductions, followed by the completed four-height computations.

Work dated 19 November 2026. This is an independent adaptation and extension of the positioned-current methods recorded in Denis Paliy's repository, commit 0f7935b71fd958bd764bccf079e1e70bc68ce351. It is a research calculation with reproducible code. No referee or proof assistant has certified it.

The target is the polygon with Eisenstein vertices 0, 329, 49+231ρ, where ρ=exp(πi/3). Its sides are 329,259,259, and the primitive tile sides are a=33,b=7,c=37. The determinant ratio is exactly 329. This note concerns this tile and target only.

## Why finite-band enumeration includes arbitrary T-junctions

Write Z=33+7ρ, z=Z/37, η=7−3ρ and η'=4+3ρ. Then ηη'=37 and z=ρη/η'. A short-edge height h means that its direction is z^h times a sixth root of unity. The two short sides of a tile have the same height and its long side has height h+1 or h−1. Positive-length contacts propagate this description to the whole tiling. Height indices are distinct because 2cos(arg z)=73/37 is a rational noninteger, and cannot be a rational algebraic integer.

For a maximal continuous collinear component of tile sides in the interior, each bank partitions the same segment into whole integer tile sides. From the common initial endpoint, every breakpoint therefore lies at an integer distance. The outside boundary similarly partitions into whole tile sides. If h is a direction height outside the short-height band [L,U], every side there has length 37, so on such a component the two banks agree step-for-step. Thus a split atom at an extreme height has full length 37. In a short height each split atom has integer length. The extreme displacements 37z^(L−1) and 37z^(U+1) are respectively z^L conjugate(Z) and z^U Z. The connected graph of split edges then puts every actual vertex in the module ∑_(h=L)^U z^h Z[ρ] after choosing the outer corner 0 as origin. This is the finite-band vertex lemma of the repository, research/position-currents-oct7/PROOF.md, §1.

Multiplication by D=η^(−L)(η')^U sends that entire module into Z[ρ], since D z^h=ρ^h η^(h−L)(η')^(U−h). Inclusion suffices. All orientations of both chiralities are obtained by using the two vectors from the 120-degree corner, k u and (40−k)ρ²u, for k∈{7,33}, u=ρ^rη^(h−L)(η')^(U−h), and r=0,...,5 in these multiplied coordinates. The algorithms examine every possible integer translation with all three vertices in the target. This argument permits an edge to touch any number of other edges.

## Why support has at most four heights

Use the existing I120 height-population divisibility result from research/i120-global-oct7/HEIGHT_LEVELS.md in Paliy's repository. It gives 37|n_h at h≠0 and n_0 ≡ 329 ≡ 33 mod 37. In particular zero occurs. A gap between 0 and an occupied height is impossible. Tiles on the far side of a vacant height k have exposed component edges only of height k, all whole edges of length 37 by the same collinear-component argument. The outer border has heights −1,0,1; for k=±1 the far side can meet it at height k only. On closed walks of this boundary all steps lie in 37z^k Z[ρ]. The signed area is therefore an integer multiple of 37²√3/4. The area of one tile is 231√3/4, coprime in coefficient to 37², forcing at least 1369 tiles in any nonempty such component. Thus short heights form an interval containing zero.

To see that any nonzero height has at least 74 tiles, assign to a directed side of length l and direction z^hρ^j the current l(−1)^j. For any one tile, its two short edges contribute 26ε to the total current at its short height, where ε=±1. The other contributions in that height, including **any outer legs** of length 259, are multiples of 37, so ∑ε ≡ 0 mod 37. If n_h=37 then the sum is odd and must be ±37. Thus all 37 tiles have the same ε. Along each individual supporting line carrying short edges at that height, all 33-edges have one current sign and all 7-edges the other. The lengths of all incident 37-edges and any entire exterior side on this line are multiples of 37. Thus its counts m,n satisfy 33m−7n ≡ 0 mod 37, equivalently 4m+7n ≡ 0 mod 37. A nonempty line requires at least seven short edges. There are 74 short edges across the 37 tiles and hence at most ten such lines. For any fixed first line and distinct second line, prescribing which carries length 33 and the common ε gives at most one tile at their intersection. The two possible 120-degree ray pairs are opposite and have opposite ε. Therefore m,n≤9 on each line. The only nonzero solutions of 4m+7n ≡0 mod 37 in this box are (4,3) and (8,6), inconsistent with ∑m=∑n=37.

For parity, write g_h as the signed sum of ε for tiles at height h. In the orientation with short vectors (33u,7ρ²u), the long-side direction is −z^(h−1)ρ^j for u=z^hρ^j; in the ordering (7u,33ρ²u) its direction is z^(h+1)ρ^(j+2). In both cases the total ordinary current over the three edges is −11ε. The total with each height also weighted by (−1)^h is 63(−1)^h ε. The exterior has positive currents 329,259,259 at heights 0,+1,−1, respectively. Consequently ∑g_h = −847/11 = −77, and ∑(−1)^h g_h = −189/63 = −3. Thus the aggregate signed count on odd heights equals (−77+3)/2=−37. At least one odd height has an odd population, so at least 111 tiles there. Five heights need at least 33+111+3·74=366>329.

## Computer-assisted elimination of up to three heights

For every point and unoriented line direction, the number of oriented counterclockwise tile edges starting there minus the number ending there must equal the corresponding count for the outer polygon. This follows by taking the one-dimensional derivative of the signed edge currents restricted to that line (an oriented edge contributes + at its initial point and − at the final point in either geometric direction). A T-junction cancels correctly. At a zero boundary row, a placement having no surviving opposite sign at one of its endpoints can be removed. At a nonzero boundary row, absence of its required sign is a contradiction. No positivity inferences stronger than this rule are required.

The stand-alone C++17 program strip_replay.cpp represents the possible horizontal integer translations as disjoint intervals on each scanline. It starts by imposing all three target halfplanes on all tile vertices, then intersects each possible endpoint with the union of opposite endpoint positions during each sweep. At exterior corners it explicitly tests the required sign. For [0,2] the initial 1,337,387,033 placements produce an exterior-corner contradiction on sweep 109. An independently implemented adapted bitmap sweep, using different template/direction order and update scheduling, reported sweep 65 from exactly the same initial population. Reflection about the vertical symmetry axis sends h to −h.

For [−1,1] both sweeps produce a stable set of 952,400 placements. A second necessary test requires full coverage of every positive-length part of every candidate edge by the union of opposite oriented edges on exactly the same affine line. The outer border is inserted with reversed orientation. Positions are integer coordinates and projections, and touching closed intervals are merged. Run with the phase flag **0**, so that arbitrary collinear matches are permitted. On sweep 37 opposite candidates no longer cover the right exterior side. The output shows the affine line and its primitive direction. Discarding these center and one-sided bands proves every possible tiling of this target uses exactly four consecutive short heights. At this stage of the argument the remaining ranges up to reflection are [0,3] and [−1,2]. The next computation below excludes [0,3]. Height zero has 33 or 70 tiles; each nonzero height has 74 or 111. Indeed 107 at zero, or 148 at a nonzero height, would force all nonzero populations even, violating odd-height parity.

## Reproduce

Run the following in an empty working directory containing the two source files. Only a standard C++17 compiler is required. The intermediate listing of 952,400 placements occupies approximately 12 MB. The generic interval replay briefly uses hundreds of MB.

```sh
c++ -O3 -std=c++17 strip_replay.cpp -o strip_replay
c++ -O3 -std=c++17 segments.cpp -o segments
./strip_replay 0 2
./strip_replay 0 1 2
./strip_replay -1 1 0 1000 centered.txt
./segments centered.txt 0
```

The positive control uses a two-fold dilation of the tile with its known four-tile tiling. Running the segment checker on these four placements with control scale 2 preserves them, and removing one yields a contradiction at the exterior side. It stabilizes at exactly four placements. This restricted exclusion is insufficient to decide 329 or Erdős's classification question.

The bitmap replay is optional. Its source is adapted from the named repository implementation for 154, with the tile, target and prime factors substituted; the standalone interval replay was written separately. The two membership checks use different scanline calculations.

```sh
c++ -O3 -std=c++17 bitmap.cpp -o bitmap
./bitmap 0 2 bitmap-02 600
./bitmap -1 1 bitmap-11 600
```

## Four-height frontier investigation

The file peel.cpp contains a depth-first exact geometry search. The current is stored by location after subtracting previously placed triangles. It considers all exposed convex sectors, uses containment and the separating-axis theorem in integer coordinates, and evaluates admissible whole-side words on surviving exterior intervals and on free intervals with two convex ends. Any isolated direction outside [L,U] consists entirely of long 37-edges, so an internal tile edge there forces a unique mate by a half-turn through its midpoint. In the band [0,3] the exterior leg at height −1 similarly forces seven tiles, which are inserted before search. An equality check on the full residual boundary and the used-height counts guards cached failures. Three-fold dilation gives a nine-tile positive control. Time-limited runs of the four-height frontier have explored branches but have not certified either exclusion or existence. This exploratory code is independent of the restricted proof above.

```sh
c++ -O3 -std=c++17 peel.cpp -o peel
./peel 0 3 60 3
./peel 0 3 300
./peel -1 2 300
```

## Refinement by position cosets

Write R=Z[ρ]. For any short height h with 74 or 111 tiles at the outer end of a band, all vertices of those tiles belong to **one translate of the coarse lattice z^h R**. To prove it, assign each tile of height h to its vertex coset C modulo z^hR. All of its vertices agree in this coset. On any height-h line the endpoints of each contributory edge agree modulo z^hR, including the nearby long 37-edges and any exterior side at h having length 259. Restrict the endpoint-incidence identity on that line to C; the resulting signed compactly supported chain has zero derivative, so vanishes as a line current. On outward directions of the extreme layer the only tile contributions are whole 37-edges of that layer, which cancel within their coset. For nonzero extrema of size at least two there is no exterior there; the same applies at h=−1 in [−1,2], whose outward height is −2. The boundary of the union of the chosen-coset tiles at h is thus a sum of whole edges from the inward-facing 37-edges and the length-37 neighbor edges at height h, plus any 259=7·37 side of height h. Their steps lie in z^h times the ideal generated by 37 and either Z or its conjugate. Since Z=ρη² and 37=ηη', the ideal is ηR or η'R up to a unit, of area index 37. Balance at vertices decomposes the multiset of oriented edges into closed walks. Every signed area is a multiple of 37√3/4, hence 37 divides n_(h,C). The short-line argument that excluded 37 applies in this coset separately. Consequently every occupied coset has at least 74 tiles, and there is only one since the entire layer has at most 111.

For [0,3] the base layer is pinned to R itself. On every C other than R, the exceptional exterior base of length 329 and the compulsory h=−1 seven-edge exterior leg are absent, so the same proof gives n_(0,C)≥74 whenever positive. The bound n_0≤70 excludes this.

More generally all height-k vertices in [0,3] lie in Λ_k=(η')^(−k)R (k=0,1,2). Here is the inductive step. Assume all lower heights are in Λ_k, which contains z^jR for j=0,...,k. All vertices of a height-k triangle still share a coset C of Λ_k. At height k−1, the inward long edges of height-k tiles in any C other than Λ_k cancel as a signed line chain. Indeed all other possible contributions (from lower layers and any exterior side) belong to Λ_k. At height k itself, the line-current identity splits into cosets of Λ_k as before, including the lengths 37 of the upper neighbors and any exterior side here. For an off-base C, the remaining boundary steps are multiples of 37 at height k, or inward-facing (toward larger heights) 37-edges at height k+1. The corresponding index-37 area gives 37|n_(k,C). The same divisibility follows for the base coset by subtracting from 37|n_k. Each occupied C must then have 74 or more by the short-line obstruction, hence all height-k triangles are in just one C.

If that one C were off-base, the entire inward long chain at height k−1 of the height-k tiles would vanish. Consider the boundary of the union of all tiles of height ≥k. At heights below k−1 there are no such edges. Their height-(k−1) term is precisely the zero chain just proved; their height-k term, by the whole tiling current, equals the exterior height-k boundary minus the height-k edges of lower tiles, the latter all whole 37-edges of height k−1 tiles. For larger direction heights all tiles contributing are in the tail, so the current there equals the exterior, empty since k≥1. The only possible exterior side in this surviving chain is the height-1 leg when k=1, and it has length 7·37. Thus the entire tail boundary uses steps in 37z^kR, forcing a nonempty tail to have at least 1369 tiles. This contradiction pins C to Λ_k. In full [0,3] integer search coordinates each gamma anchor at h=k must therefore be divisible in R by (η')^(3−k). In particular h=0,1,2 anchor densities fall by factors 50,653, 1,369, and 37 respectively relative to the unconstrained dictionary.

These are direct current-and-area arguments independently cross-checked within this investigation. They are also restrictions on a hypothetical four-height tiling; neither one supplies a positive construction or an exclusion of the whole band.


## The entire one-sided four-height band is excluded

The exact scanline replay *without* the extra lattice/pairing/collar assumptions also excludes all of [0,3]. The implementation in packed_replay.cpp encodes each sorted list of disjoint horizontal runs by its first coordinate and the successive run lengths and gaps as variable-length unsigned integers. The containment bounds, available endpoints and monotone forcing rules are unchanged. Its exhaustive dictionary has 65,681,363,443 contained placements in 48 oriented templates across 82,909 scanlines. Sweep 108 found no positive endpoint at the required exterior apex (−61691,54159) in primitive direction (8813,−7737). The entire log is in packed-0-3.log. As an additional check, removing the nine individually forced left-collar triangles before replay gave a missing positive endpoint at the same apex in primitive direction (252,−181), on sweep 107. This second run is a consistency check and uses additional hypotheses; the main sweep had no preset tile placements. The resulting **only remaining four-height band, modulo reflection, is [−1,2]**. The detailed phase restrictions for that band are in PHASES.md.

```sh
c++ -O3 -std=c++17 packed_replay.cpp -o packed_replay
./packed_replay 0 3
```


## Centered four-height exclusion

Using the necessary positions in PHASES.md, the exact centered dictionary of 465,602,541 placements reaches a corner contradiction on sweep 62 in pinned_center.cpp. Its apex in the sheared coordinates is (−83657,−269360). There was no required positive incidence there in primitive direction (323,1040). The immediately preceding sweep still left 2,888 placements. The raw log is pinned12.log. This last step allows every lower-layer placement in all of M(−1,0), every height-zero placement in R, every height-one placement in M(0,1), and every height-two placement in M(0,2), without selecting a particular phase triple. The independent initial-dictionary audit in ../iso329_review recalculates the exact total by counting in each layer's native lattice.

Thus the two four-height bands, the previously treated shorter bands, and their reflections are excluded. Conditional only on the arithmetic reduction to this candidate and the cited height-population input, there is no 329-tiling. This is an internally checked, computer-assisted result and does not classify all tile counts. The additional independent grouped sparse queue is an audit of the centered calculation.

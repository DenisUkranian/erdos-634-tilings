# Vertex-star certificate for the beta triangle of count 236

Set d=i√21 and z=(−2+d)/5. The target is T with axial coordinates (0,0),(472,0),(236,18), and each copy of the tile has physical side lengths 9,20,25. The argument checks a necessary consequence of an arbitrary tiling, allowing arbitrary real translations and T-junctions. Its core does not assume that any tile vertex falls on the numerical mesh.

## Orientations and exact cells

Give each tile its counterclockwise boundary and anchor it at the tail of its directed 9-side. Relative to the anchor its possible vertex triples are 0,9u,(e+4d)u with e=−8 or 17 and u=±z^h. This follows by solving x²+21y²=400 or 625 and (x−9)²+21y²=625 or 400 with y>0. Since the tile-angle turns are integer multiples of arg(z) modulo π, all tiles of a tiling of T have this form: the base direction is horizontal, and a generic curve between tile interiors gives a chain of positive-length contacts. The direction exponent h is unique because 2cos(arg z)=−4/5 is a nonintegral rational number and a root of unity plus its conjugate is an algebraic integer.

For Q a positive integer, record a point (X,Y) by the **two mathematical floors** (⌊QX⌋,⌊QY⌋). If a known displacement v has mesh-coordinate components (t,s), mapping a cell forward by v can only move its coordinates by one of {⌊t⌋,⌈t⌉}×{⌊s⌋,⌈s⌉}. This follows from ⌊w+t⌋−⌊w⌋=⌊{w}+t⌋ for every real w,t, including negative t. A singleton occurs for an integral displacement. Different choices in the two components are all admitted. For a reverse query use all negatives of these same shifts. A union is required for the possible relative shifts of each single corner. The three different tile corners then impose an intersection of necessary conditions. Reverse and forward rounding therefore cannot reject a real placement.

## Geometric initial conditions

The anchor itself is a contained vertex, so its mesh cell indices range from 0 through 472Q and 0 through 18Q. On each wall of T, every point at which a tile vertex lies is a joint of the boundary tiling or an outer corner. Indeed any tile whose vertex touches a point in the relative interior of an unbroken wall edge of a second tile would enter the interior of that second tile. Along the wall the distances to its ends are sums of the three integral tile lengths. All such arithmetically eligible joint positions, including both corners, are enumerated; realizability of their neighboring words is not assumed.

For a wall A to A+D, with directed integer vector D=(Dₓ,Dᵧ) and physical length L, use the signed axial determinant C=Dₓ(Pᵧ−Aᵧ)−Dᵧ(Pₓ−Aₓ). A tile vertex on the wall must fall exactly at a listed joint J. For a vertex off the wall, the positive clearance inequality is C≥81L/125. If one of the tile sides through it is parallel to that wall, the stronger bound is C≥36L/25. Both statements, including the T-junction case, are established in the first section of [the clearance argument](../../nov19/beta236/RESULTS.md).

For the parallel-side bound, take a generic point on the line: the tile immediately on its wall-facing side has axial altitude at least 36/25 and lies in the target. For the other bound, every off-wall vertex of a tile meeting the wall lies at physical height at least 9 sin β. Indeed the side joining it to a wall vertex makes an acute angle of at least β with the wall. At an interior wall joint the gaps are sums of tile angles. At a target corner use its angle or its supplement, as in the clearance argument. The finite union of all tiles that meet the wall contains a relative neighborhood of that wall. The polygonal frontier between this union and other tiles has ends at vertices of one of the tiles in this union, off the wall. All these ends are at height at least 9 sin β. The whole frontier therefore has that lower bound. The connected strip below it is covered by the first union; any additional tile with a vertex in the open strip would have interior there. This proves the estimate including T-junctions.

In mesh units a candidate anchor cell has lower-left coordinate (i,j). For a fixed relative vertex v use the test
```
Dₓ(j+Qvᵧ−QAᵧ) − Dᵧ(i+Qvₓ−QAₓ) + max(0,Dₓ)+max(0,−Dᵧ) ≥ Q · clearance.
```
The two maxima give an upper bound on the determinant anywhere in the half-open cell. If the inequality fails, still retain the cell whenever it equals floor(Q(J−v)) for one of the listed joints. Apply this union independently for every wall and every corner of the template, taking the intersection over the requirements. Thus every actual placement is present initially. All geometry involving the powers of z, wall inequalities, and ray order uses exact integer or rational arithmetic.

## The sweep

For each tile shape and each currently possible anchor cell, record the following directed angular arcs, always counterclockwise around their incidence point.

1. At each corner, record its sector from the forward side to the reversed preceding side, at every cell allowed by translating its anchor to that corner.
2. Along each open tile edge, record a semicircle on the tile side for every integral physical offset from 1 to its full length minus one. For each offset, allow all floor/ceiling translations as above. These are all through-edge possibilities because the maximal connected straight seam through any contact is partitioned on both banks by whole tile sides of integral lengths; from a common endpoint the two sets of joints differ by integers.
3. At an eligible interior joint on an outer wall add the complementary exterior semicircle at the cell of the exact joint. At each outer corner add the whole reflex exterior arc. The point set here is fixed, independent of the current placements.

At a physical vertex of a genuine tiling all incident arcs, with the exterior arc where needed, partition a sufficiently small circle. Consequently if a particular corner contributes the arc a→b, there must exist a path of remaining arcs, all at the same cell, going from ray b counterclockwise to a through strictly less than a full turn. Different possible paths are united. The masks for consecutive arcs on the same path are intersected. The strictly increasing circular ray order gives a finite exact Boolean dynamic program. Its use of candidate arcs from different placements or different real locations within a cell may add spurious paths; it preserves every actual circular partition.

Using only availability at the start of the sweep, compute this complement for every possible oriented corner and for the three exterior arcs at their target corners. Remove any anchored shape cell whose three corners do not individually admit a complementary path. If the fixed exterior arc at a target corner lacks a complement at its own cell, a true tiling is impossible. Inductively every genuine tile survives every generation, so failure at one target corner proves the claim for the tested orientation range. Node counts and search-time bounds do not enter the implication.

## Reproduction

Two implementations compute the masks independently. `mesh_stars.py` uses rational coordinates and Python big integers. `mesh_replay.cpp` regenerates every shape, directed ray, shift and cell constraint in integer arithmetic and uses GMP for the Boolean bit sets. It has an arbitrary-precision initialization mode for wider orientation ranges.

```sh
python mesh_stars.py 39 25
g++ -std=c++20 -O3 -DWIDE_INIT mesh_replay.cpp -lgmpxx -lgmp -o mesh_replay
./mesh_replay 39 25
```

The [−39,39] result is in `mesh39.json` and `mesh39-replay.log`. Both programs give the identical sequence of 29 populations. Starting with 428,920,544 oriented shape/anchor cells, the 28th sweep loses the complement of the exterior arc at physical apex (236,18), mesh cell (5900,450). On that same generation 10,325 shape/anchor cells still survive elsewhere in the target. The conclusion is inconsistency at the mandatory apex. The earlier orientation bound |h|≤39 for every retained boundary configuration is in [the November 19 height analysis](../../nov19/beta236_independent/HEIGHT_CUTS.md).

## The global range and positive controls

The earlier local classifications of boundary words can be bypassed. The independent [height audit](../cubes/AUDIT_236_HEIGHT.md) gives a global upper bound |h|≤51 for any tiling of this target. Even without its terminal-population refinement, the weaker bound 57 follows: all nonzero heights cost at least five tiles, so there are at most 47 occupied positive heights. A separated vacancy below a nonempty upper tail forces its size to be a distinct positive multiple of 25, so there are at most nine such gap blocks. A block of two vacancies forces a positive multiple of 125, permitting at most one extra vacant height. A block of three is impossible by the one-direction area argument. Reflection supplies the lower bound. These facts hold before any boundary-word search.

The arbitrary-precision replay covers [−57,57] by `./mesh_replay 57 25`. It starts with 624,827,600 cells and loses the apex on sweep 28, with 10,325 remaining cells. The two independently computed full trajectories agree in `mesh57.json` and `mesh57-replay.log`. A separate unrestricted-translation recheck with **both clearance bounds disabled** also eliminates this band. It starts with 762,512,895 cells and loses the apex on sweep 29, with 24,371 left elsewhere. Use `./mesh_replay 57 25 60 2 100 0`; see `mesh57-no-clearance.log`. Thus the specific (9,20,25) beta target has no tiling. Any conclusion about the numerical count 236 for arbitrary triangle shapes also uses the independent reduction to this sole potential target.

In addition to the exact 16- and 1475-tile controls, `python mesh_control.py` restricts the initial masks to the **specific 1475 placements** of the known larger beta tiling and applies the rounded star rule. At meshes Q=7 and Q=11, 1241 of its 1475 anchors are genuinely off grid. Every single real tile survives, and deleting the unique tile at the origin immediately removes the required corner star. Q=25 supplies a third control, with all these anchors on grid. See `mesh-control.json`. These are independently coded numerical and geometric checks, without external refereeing or a Lean proof.

## Unbounded-height exclusion with a frozen outer band

There is a way to validate a finite orientation calculation without assuming any a priori bound on tiling heights. For an interior vertex, inside an outer side or at either target corner, the angles of the filled domain sum, respectively, to 2π, π, β or 3α. A possible through-edge tile contributes a straight angle. Since γ=2α+β and π=3α+2β and α/β is irrational, the coefficients of α and β can be compared as integers. In every case straight angles, corner α's, β's and γ's make nonnegative contributions to total coefficient bounds (6,4). The irrationality follows at once from the irrationality of γ/π and the two displayed angle relations.

The signed changes of ray exponent through the four respective elementary angles α,β,γ,π are 2,−3,1,0. Between any two actual incident rays we can follow the sequence of physical tile angles inside the target. Its positive exponent contribution is at most 12 and its negative contribution has magnitude at most 12: 2 times the number of α's plus the number of γ's is at most 12 by the first coefficient bound, and three times the number of β's is at most 12 by the second. Thus every two rays in this star differ in exponent by at most 12. A tile's short-side exponent differs from the exponent of any one of its edges by at most 2. Any two tiles contributing to the same star therefore have their short-side exponents differ by at most 16, also for a through-edge tile. The three target-corner stars themselves start from exterior exponents 0 or ±3 and hence use |h|≤17.

For any B≥17, keep the orientations |h|≤B. Leave all initial cells of orientations |h|>B−16 permanently available and apply the star test only to |h|≤B−16. Every true tile of a checked height has each of its star witnesses inside the stored band; every true tile from the untested shell remains available by construction. Induction proves that a missing target-corner complement in this test would rule out **all tilings**, without any global height bound. The commands use the optional `--freeze-outside B-16` for Python or a sixth positional argument after target scale for C++. The computation with B=39 and permanently frozen |h|>23 eliminates the mandatory apex on sweep **35**. The other 243,881,947 shape/cell pairs at that point are permitted but do not supply the missing apex star. This establishes the geometric exclusion with no assumption about how large the orientation heights might be in a tiling and no use of the prior 100 boundary orbits. Both independent implementations produce the same 36 populations, recorded in `unbounded-frozen.json` and `unbounded-frozen-replay.log`.

```sh
python mesh_stars.py 39 25 --freeze-outside 23
g++ -std=c++20 -O3 -DWIDE_INIT mesh_replay.cpp -lgmpxx -lgmp -o mesh_replay
./mesh_replay 39 25 60 2 23
```

The 60 in the command is the maximum number of passes requested. The recorded contradiction occurs on the 35th pass, before that limit.


A sharper window of 12 is also valid, although the reported B=39, K=23 certificate keeps the more conservative margin of 16. If the starting ray of a counterclockwise corner has exponent j, then the possible short-side exponents are {j,j+2} at α, {j−1,j−2} at β, and {j,j+1} at γ. This follows by deciding whether the first ray is the 9-, 20- or 25-side and using their exponent differences 0, +ε, −2ε. In every case the short height lies between the two corner-ray heights. Without a through-edge tile the whole star therefore fits in the ray-height span of 12. With a through-edge tile, its straight angle consumes π and all remaining actual corner sectors fill at most π, giving ray-span at most 6 by the same coefficient count. The through-edge tile can be only two heights beyond that interval. The domain at a base corner or apex is smaller than π, with coefficient bounds given above.


## Unbounded heights with containment as the sole initial shape restriction

Choose B=52, freeze all 128 types with 37≤|h|≤52, and turn both exterior-clearance estimates off. This combines unrestricted tile translations and orientations with the simplest initialization. All real tiles with |h|≤36 have their entire local stars inside the stored band. Starting from 696,515,374 admissible shape/cell pairs, the required complement at the physical apex (236,18) is absent on **sweep 29**. At that time 292,784,658 pairs remain elsewhere or in the permanently available outer shell. The integer trace is [unbounded-no-clearance.log](unbounded-no-clearance.log). This proof uses no finite bound on the orientations of an actual tiling, no side-word census, no cut-area divisibility, and no metric strip clearance. It retains the elementary integer-offset condition on complete contact seams and boundary joints.

```sh
g++ -std=c++20 -O3 -DWIDE_INIT mesh_replay.cpp -lgmpxx -lgmp -o replay
./replay 52 25 55 2 36 0
python mesh_stars.py 52 25 --freeze-outside 36 --no-clearance
```


As a corroborating calculation the same containment-only frozen test with B=65, K=49 also loses the apex on sweep 29 (868,656,219 initial cells, 295,632,308 remaining). The run used an optimized copy of the C++ sweep that preaggregates the immutable outer-shell arc masks. The primary B=52 computation above used the unmodified verifier and its recorded command.

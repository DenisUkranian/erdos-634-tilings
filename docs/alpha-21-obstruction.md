# A finite exact obstruction for the 21-tile alpha-isosceles target

29 September 2026. **Status: computer-assisted exclusion with a separately implemented exact replay; internal mathematical review only.** The replay checks all branches without importing the search, trusting its memoization, or using its overlap predicate. This is not external refereeing or a proof-assistant formalization.

## Statement and current certificate

Let T have sides `(2,3,4)` and opposite angles α,β,γ. Then

$$
3\alpha+2\beta=\pi,\qquad
\cos\alpha=\frac78,\quad
\cos\beta=\frac{11}{16},\quad
\cos\gamma=-\frac14.
$$

The exclusion is that the triangle with sides `(12,12,21)` cannot be tiled by 21 congruent copies of T, allowing reflections and arbitrary T-junctions.

The exact search [search_alpha21.py](../scripts/search_alpha21.py) terminates with `UNSAT` on this instance. It stores its entire branching record in [alpha-21-refutation.json](../data/alpha-21-refutation.json):

- 391 distinct states;
- six repeated-state references;
- maximum depth 18;
- maximum branching width four;
- 135 terminal states, of which five have an impossible convex-corner angle and 130 have no feasible tile placement;
- rational coordinates only, with denominators at most 64 in this particular run.

The denominator 64 is an observed outcome, **not a search restriction**. No integer lattice, denominator bound, edge-to-edge condition, bounded list of orientations, or prior “no b-edge” lemma is imposed.

The deterministic public certificate has SHA-256

```text
68c4b0edd0eaeb2c99818d41522d40ef6e7062a2f800c0cc3fd78f7a1bbed74c
```

The public certificate omits elapsed-time metadata from the original research run. Its mathematical branching record is unchanged, and the independent checker was rerun on these exact public bytes. The optional search requires an explicit output path and reproduces the deterministic certificate.

## 1. Coordinate model and exact arithmetic

Write `(x,y)` for the Euclidean point `(x,y√15)`. Squared length is

$$
\|(x,y)\|^2=x^2+15y^2.
$$

Take the target counterclockwise vertices

$$
A=(0,0),\qquad C=(21,0),\qquad B=(21/2,3/2).
$$

Its equal sides have length 12, and its base has length 21. Its area is 21 times the tile area `3√15/4`.

A rotation is represented by `(C,S)` meaning physical cosine C and physical sine `S√15`. Rotation composition is

$$
(C,S)(C',S')=(CC'-15SS',\ CS'+SC'),
$$

and its action on a coordinate vector is

$$
(x,y)\mapsto(Cx-15Sy,\ Sx+Cy).
$$

The three tile-angle rotations are exactly

$$
R_\alpha=(7/8,1/8),\qquad
R_\beta=(11/16,3/16),\qquad
R_\gamma=(-1/4,1/4).
$$

All subsequent calculations use rational numbers, represented by arbitrary-precision fractions. A side direction is normalized using the exact rational square root of its squared metric length; exact-square assertions check that operation. These rational lengths follow inductively because every frontier segment is part of an already constructed tile edge or target side.

## 2. Why every hypothetical tiling is reached without a grid assumption

Suppose some already selected whole tiles are part of a hypothetical complete tiling. Let Ω be the positive-area uncovered region. It is a bounded polygonal region, possibly disconnected and possibly with holes, whose boundary consists of actual segments of target sides and selected tile edges.

**Convex-corner lemma.** If Ω has positive area, it has a boundary sector with angle strictly between 0 and π. One may take an outer boundary of a positive-area component: its total turning is 2π, so at least one of its vertices has a positive exterior turn. Point contacts between boundary components can be separated into their local sectors; they do not remove this conclusion.

Select any such sector, with corner P, outgoing boundary ray d, and the next incoming boundary ray r in counterclockwise order. Its interior sector is the counterclockwise interval from d to r. Let its angle be φ, with `0<φ<π`.

In the hypothetical complete tiling, consider the unselected tile adjacent to a sufficiently short initial segment of d. It must have P as a tile vertex. Otherwise P would be in the relative interior of its side, giving an interior angle π at P, or in its interior, giving angle 2π; neither fits in the uncovered sector of angle less than π. Its edge from P is along d, and the tile lies on d's left side.

There are consequently only six placements to consider:

| Tile corner at P | Side on d | Other incident side |
|---|---:|---:|
| α | 3 | 4 |
| α | 4 | 3 |
| β | 2 | 4 |
| β | 4 | 2 |
| γ | 2 | 3 |
| γ | 3 | 2 |

For a unit vector e along d, the corresponding candidate is

$$
\operatorname{conv}(P,\ P+\ell e,\ P+\ell'R_\delta e).
$$

The two ordered side choices include reflected tiles. They determine the full tile without any continuously variable offset: the convex corner fixes its vertex.

At least one of these six candidates is the actual tile from the hypothetical completion. Removing it preserves a completion with one fewer tile. Induction therefore proves that repeatedly branching in this way reaches every possible tiling, even though the chosen order need not match any original labeling of its tiles.

This also proves, rather than assumes, that all coordinates encountered in this search lie in the rational coordinate model. Each candidate follows from a rational point, a rational normalized edge direction, and one of the three rational rotation matrices. No unrestricted completion is lost by storing those resulting coordinates exactly.

## 3. Necessary angle and geometry filters

### Angle filter

At a convex residual corner, the uncovered sector is a sum of tile angles. The program constructs the finite set of all sums strictly below π by beginning with zero and repeatedly adding one of α,β,γ whenever the resulting sine coefficient is positive.

This test is exact. The current angle lies in `[0,π)`, and each added tile angle lies in `(0,π)`, so the sum lies in `(0,2π)`. In this range its sine is positive exactly when the sum is below π. No wrapping through a full turn is possible. The resulting set has 17 rotation values, including zero. It is closed under every allowed addition, so induction on the number of summands proves that it contains every possible convex tile fan.

If φ is absent from this set, the state cannot be completed. For a candidate using angle δ, the remaining sector `φ−δ` must be zero or another allowed fan. The program tests this by exact rotation division. Since both φ and δ lie in `(0,π)`, their difference lies in `(−π,π)`; an accepted positive-sine rotation therefore cannot represent a negative difference disguised by a full turn.

### Geometry filter

Every candidate must lie in the target. Since the target is convex, this is equivalent to all three candidate vertices lying in all three target half-planes.

Its interior must be disjoint from every selected tile's interior. For two convex triangles, interior disjointness is equivalent to a separating line parallel to an edge of one triangle. The program checks every edge of both triangles using exact signed cross products. Zero cross products permit shared edges, partial shared edges, and isolated vertex contacts.

These are only necessary conditions for an extendible partial tiling. Neither filter assumes anything about the eventual positions of unselected vertices.

## 4. Exact frontier and memoization

The uncovered boundary is oriented with uncovered area on its left. Initially it is the target's counterclockwise boundary. Placing a counterclockwise tile subtracts its three directed edges, equivalently adding their reversals.

Before cancellation, every collinear overlap is split at all segment endpoints lying on it. Opposite directed atoms cancel. Because selected tiles are interior-disjoint and lie inside the target, no true boundary atom has multiplicity greater than one. All intersections relevant to this operation occur at known endpoints: transverse intersections of two edge interiors would force positive-area overlap and have already been rejected.

Straight degree-two subdivision vertices are erased. This does not alter Ω or any possible future tile placement. At a vertex of higher degree, incident rays are sorted cyclically using only half-plane signs and cross products. An outgoing ray followed counterclockwise by an incoming ray bounds an uncovered sector. A positive cross product selects exactly its convex sectors.

The canonical oriented boundary determines the uncovered region, including its holes and components, by winding number. Thus two states with identical canonical boundaries have identical possible completions. The search may reuse a previously examined state even if a different order of already placed tiles produced it. Tile area also determines the depth from the remaining area, so repeated-state references cannot create an increasing-depth cycle.

## 5. What an independent replay must check

Each stored state records its depth, selected convex sector, and every candidate that survives the angle and geometry filters, together with the corresponding successor state.

An independent checker should verify, from the root:

1. The recorded sector is an actual convex uncovered sector of that state.
2. Its listed children are exactly all six angle/side placements surviving the necessary filters; no legal candidate is omitted.
3. Every child's coordinates agree exactly with its angle and side choices.
4. Every successor boundary is the exact subtraction of that tile, and a repeated reference has the same canonical uncovered region and depth.
5. Every leaf has no surviving candidate, and all branches end in such a leaf before 21 tiles.

The completeness theorem in Section 2 converts this finite verified branching record into a nonexistence proof. The separate implementation [verify_alpha21.py](../scripts/verify_alpha21.py) has now completed this replay and returned PASS. It uses exact local tangent cones rather than the search's frontier subtraction, rational polygon clipping rather than its separating-axis test, and an independently bounded integer-triple angle enumeration. Every repeated-state reference is expanded and checked under its own placement history; thus it does not rely on the search's memoization argument. It verifies 437 expanded states and 158 dead ends, reaches all 391 certificate nodes, and confirms maximum depth 18. Its recorded result is [alpha21.json](../verification/alpha21.json).

For the finite certificate, the checker need not even assume a general existence theorem for residual convex corners: it directly verifies the chosen empty convex sector at every recorded state. What remains essential is the local six-placement completeness argument at that verified sector.

## 6. Positive controls

The same convex-sector, angle-filter, candidate-placement, and frontier-update routines were applied to the separately verified 75- and 147-tile theta constructions. At every chosen convex corner, at least one of the enumerated candidates was an actual remaining tile from the known construction. Selecting that tile and repeating removed all 75 and all 147 tiles and left empty boundaries.

These controls exercise arbitrary T-junctions and the geometry of the new constructions. They cannot establish universal completeness by themselves; the convex-corner argument supplies that proof. They do guard against simple implementation mistakes that would reject a known tiling before all its tiles are removed.

## 7. Consequence of the verified obstruction

For the fixed tile `(2,3,4)` and an alpha-isosceles target with equal sides X, the base is `7X/4`. Integer boundary lengths give `X=4r`. The area equation gives `7r²=3N`, so `r=3K` and

$$
N=21K^2,\qquad (X,X,Y)=(12K,12K,21K),\qquad K\in\mathbb Z_{>0}.
$$

For every K≥2 there is a construction: cut the base at distance 9K from its left endpoint. The corner triangle has sides `(6K,9K,12K)`, hence is a `3K`-scaled copy of the tile and has `9K²` tiles. The complement has sides `(6K,12K,12K)`, a theta-isosceles target of scale `t=2K`, and has `12K²` tiles by the already established theta construction. The total is `21K²`.

The validated exclusion of K=1 therefore completes this fixed-tile alpha branch with exact spectrum

$$
\boxed{N=21K^2,\qquad K\ge2.}
$$

This is a statement about one tile and one target shape. It does not by itself solve the full all-integer classification in Erdős problem 634. Beeson's report of a previous external computational exclusion is not used in this proof; his v4 conclusion continues to list 21 as undecided.

## Reproduce the public certificate

From the repository root:

```bash
python3 scripts/verify_alpha21.py
python3 scripts/search_alpha21.py --output /tmp/alpha-21-refutation.json
cmp data/alpha-21-refutation.json /tmp/alpha-21-refutation.json
```

The checker writes only its result to standard output. Both programs reject optimized Python (`-O`), since their checks require assertions. The certificate and both implementations use only the Python standard library. See also the [independent audit](audits/alpha21.md).

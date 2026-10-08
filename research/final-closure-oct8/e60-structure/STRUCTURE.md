# E30: at most four consecutive short-edge heights

8 October 2026. Necessary geometry for the equilateral triangle of side
30 tiled by 60 congruent (3,5,7) triangles. This note does not itself
decide existence. It adapts the earlier affine-line argument for (8,7,13)
and adds a separate argument to rule out a 49-tile tail across an empty
height. The earlier sub-c-squared no-gap theorem alone is insufficient,
because 60>49.

Put rho=exp(i pi/3), z=(3+5 rho)/7. Short-edge height h means directions
rho^j z^h. Every tile's long edge has height h-1 or h+1. All exterior
directions of the equilateral target have height zero.

**Theorem.** In any such tiling, including arbitrary T-junctions:

* n_0>=11 and n_0=4 mod7;
* every occupied nonzero height has n_h>=14 and n_h=0 mod7;
* the occupied heights form a consecutive interval containing zero;
* the interval has at most four members.

The divisibility statements are the equilateral case of
`../../i120-global-oct7/HEIGHT_LEVELS.md`. Their whole-edge median-cut
proof is used here, not a supposition that vertices already lie on one
fixed short lattice.

## 1. A nonzero height cannot have population seven

At a nonzero height, integrate oriented boundary cancellation on each
separate affine line in one of its three short-axis directions. Exterior
edges have another height, and every other tile edge on that line is a
whole long edge of length7. Therefore the signed sum of the height-h
short edges on each such line is divisible by7. Partial contacts and
T-junctions cause no problem: complete edges are integrated over the
whole supporting line.

Use the twelve counterclockwise gamma-anchored orientations

    A_j=(0,3 rho^j,5 rho^(j+2)),
    B_j=(0,5 rho^j,3 rho^(j+2)),       j=0,...,5.

The three short-direction currents are all divisible by7. Their
alternating character J0-J1+J2 equals -2(-1)^j for A_j and
2(-1)^j for B_j. If there are seven tiles, this is twice a sum of
seven signs. Divisibility by7 forces all seven signs to agree.
Consequently the length3 and length5 edges on a line have opposite
signs. A line containing m of the former and n of the latter satisfies

    3m-5n=0 mod7,       0<m+n<=7.

Its complete possibilities and maximum numbers of nonempty supporting
lines in a partition of that pair are:

| Total pair (m,n) | Maximum lines |
| --- | ---: |
| (7,0), (0,7), (1,2), (4,1) | 1 |
| (2,4) | 2 |

Enumeration of the six allowed common-sign orientations gives 36
modularly feasible inventories. Under rotations and reflection these
are three orbits, each of size12:

| Representative inventory | Repeated orientation | Two direction totals | Maximum gamma vertices |
| --- | --- | --- | ---: |
| B5=7 | B5:7 | (0,7), (7,0) | 1 |
| B1=1, B3=2, B5=4 | B5:4 | (2,4), (4,1) | 2 |
| A3=3, A5=1, B0=B2=B4=1 | A3:3 | (4,1), (2,4) | 2 |

For a fixed orientation its gamma vertex lies at an intersection of a
line from each of its two nonparallel short-axis families. Each row has
more copies than possible intersections. Two copies must coincide,
contradicting disjoint interiors. Population seven is impossible.
Together with population divisibility, this gives n_h>=14.

The checker verifies this enumeration in two ways: common-sign weak
compositions, and a join of residue tables for all twelve orientations
without assuming the common-sign conclusion. It verifies all36 actual
pigeonhole inequalities, not only the orbit representatives.

## 2. The central population is at least eleven

Every whole-edge partition of an external side of length30 satisfies

    3A+5B+7C=30.

If A+B<=2, the possible short lengths modulo7 are 0,3,5,6,1,3;
none equals30 mod7=2. Thus every side needs at least three short edges.
There are at least nine short boundary edges overall, all belonging to
height-zero tiles. A tile has at most two short edges, so n_0>=5.
The population congruence n_0=60=4 mod7 strengthens this to n_0>=11.

Already this proves at most four occupied heights, without assuming
that those heights are consecutive: 11+4*14>60.

## 3. A gap would isolate exactly forty-nine tiles

Suppose a positive height k is empty and some higher height is occupied.
For H, the union of all short-height-greater-than-k tiles, the median-cut
identity expresses boundary(H) as a sum of whole long edges at height k.
There are no exterior target directions above k and no height-k tiles;
all selected edges come from height-(k+1) tiles with long height k.

Every displacement belongs to 7 z^k Z[rho]. Decomposing the balanced
whole-edge chain into closed walks and comparing shoelace area with
the area15 sqrt(3)/4 of a tile gives 49 divides |H|, just as in
`../../closure-position-oct7/heights/HEIGHT_GAPS.md`. Since
0<|H|<=60, it follows that |H|=49. A negative gap is reduced to this
case by reflection and relabeling heights.

The previously proved 2c^2 divisibility for *pure* islands cannot be
invoked here: H could contain several short heights. The following
argument is specific to the actual (3,5,7) arithmetic and does not
silently assume purity.

## 4. A forty-nine-tile tail is impossible

Rotate by z^(-k), so the selected boundary long edges have height zero
and all tiles of H have strictly positive short height. Give a directed
edge of direction rho^j z^h the value length*(-1)^j X^h.
The two tile chiralities yield the integer Laurent identity

    (-2-7X)U(X)+(-2-7X^(-1))V(X)=7M.              (1)

In the A_j,B_j convention of section1, A_j contributes
(-1)^j*(-2-7/X), and B_j contributes (-1)^j*(2+7X). Thus explicitly
U_h is the odd-minus-even rotation count for B tiles, while V_h is
the even-minus-odd rotation count for A tiles. Both U and V have only
strictly positive powers. At every height

    n_h >= |U_h|+|V_h|,
    n_h = U_h+V_h mod2.

Each selected whole c-edge contributes +7 or -7. There is at most one
selected edge per tile of H, so |M|<=49. This bound is valid for the
whole-edge chain representation itself; no assumption about a simple
boundary or absence of holes is needed.

Evaluate (1) modulo45 at X=19. This is permitted for Laurent powers
because 19^2=1 mod45. Both factors vanish:

    -2-7*19=-135=0 mod45.

Hence 45 divides7M, and therefore45 divides M. On the other hand,
evaluation at X=1 gives

    -9(U(1)+V(1))=7M.

There are49 tiles, so U(1)+V(1) is odd. Consequently M is odd too.
Together with |M|<=49, these facts force

    M=45 or M=-45.

The constant coefficient in (1) gives V_1=-M. The X=1 identity gives
U(1)+V(1)=-7M/9. Thus the signed sum of **all remaining coefficients**,
after omitting V_1, is 2M/9. The triangle inequality now yields

    49 >= ||U||_1+||V||_1 >= |V_1|+|2M/9|=45+10=55,

a contradiction. This last argument uses no population floor and no
assumption that the tail has only one height. There is no 49-tile tail
and hence no gap in the occupied support.

Sections1--4 prove the theorem. For four occupied heights the population
vectors must be n_0=18 with three populations14, or n_0=11 with one
population21 and two populations14. This is still a necessary inventory
restriction, not a geometric tiling or nonexistence proof.

## Reproduction and attribution

Run

    python research/final-closure-oct8/e60-structure/check_structure.py

The saved output is `structure_verified.json`. It checks all36
inventories, the three orbit decompositions, line partition maxima,
side30 arithmetic, and the finite arithmetic used in the 49-tail proof.
The mathematical argument, rather than this finite calculation alone,
justifies the whole-edge and area steps.

The affine-line pigeonhole method and the height-population/median-cut
lemmas are prior results of this repository. The side30 central bound
was identified in the parallel E60 inventory investigation. The current
note supplies their (3,5,7) specialization and the separate modulus45
argument needed to remove the otherwise admissible 49-tile gap tail.
The direct L1 contradiction and the explicit A/B sign convention were
supplied in an independent internal review of this note.

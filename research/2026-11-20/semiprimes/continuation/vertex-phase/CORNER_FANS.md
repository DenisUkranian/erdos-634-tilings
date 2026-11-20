# Unrestricted local corner circuits for the two F2 boards

20 November 2026. This is an additional globally necessary search constraint,
not a solution of either board. All tiles may be translated, rotated, reflected,
and meet at T-junctions. No fixed corner packing or height interval is imposed.

## Exact local completeness

Let the tile angles be alpha, beta and gamma, with gamma = 120 degrees and
alpha + beta = 60 degrees. Write rho = exp(i*pi/3) and
z = (a+b*rho)/c = exp(i*beta). A ray is rho^j z^h. The three possible
counterclockwise corner increments, recorded as coefficients of (alpha,beta),
are

| Corner | Coefficients | Ray update (h,j) |
|---|---|---|
| alpha | (1,0) | (h-1,j+1) |
| beta | (0,1) | (h+1,j) |
| gamma | (2,2) | (h,j+2) |

Here j is taken modulo six. The angle beta is an irrational multiple of pi:
otherwise z is a root of unity, so z+z^{-1}=(2a+b)/c would be a rational
algebraic integer, hence an integer. It is strictly between one and two.
It follows that a sum of tile angles equals a full turn exactly when its
coefficient pair is (6,6), and a half-turn exactly when it is (3,3).

Fix one selected tile T and one of its physical vertices p. Take a sufficiently
small circle about p, avoiding every other vertex and every side not incident
with p. If p is interior to the board, exactly two cases are possible.

1. Every tile meeting p has p as a vertex. Their sectors give a full fan, with
   total coefficients (6,6).
2. One tile has p in the relative interior of a side and occupies an open
   half-plane near p. There cannot be two such tiles while T also meets p:
   two disjoint open half-planes leave no positive-angle sector for T. The
   other tiles, all having p as a vertex, form the complementary half-fan,
   with total coefficients (3,3).

The through-edge tile in the second case is not inserted as a discrete
placement variable. Instead its full continuum of translations is checked
by exact one-variable intervals, as described below. No lattice restriction
on that tile is introduced.

At a boundary point the sector is prescribed by the board. For the frame
with vertices O=0, X=b(2a+b), Y=a(a+2b)*rho, its sectors are:

| Point | Starting ray (h,j) | Total coefficients |
|---|---|---|
| O | (0,0) | (1,1) |
| X | (2,1) | (2,0) |
| Y | (0,4) | (0,2) |
| Interior of OX | (0,0) | (3,3) |
| Interior of XY | (2,1) | (3,3) |
| Interior of YO | (0,4) | (3,3) |

A tile with a vertex on the boundary cannot meet the relative interior of
another tile side there: the latter would occupy the entire interior
half-plane near that point, leaving no positive sector for the former.

For any prescribed starting ray, each corner type permits exactly two rigid
placements, from the two orders of its adjacent side lengths. The implementation
uses the existing complete 24-placement endpoint enumeration and retains the
six placements whose counterclockwise sector starts on that ray. Whole-tile
containment and the existing necessary boundary arithmetic may reject some.
No other tile with a vertex at p and that sector can occur.

## The finite circuit

For a point p, starting ray r and coefficient budget (A,B), define

    F(p,r,A,B) = OR over admissible outgoing corner tiles U:
                 x_U AND F(p, r+angle(U), A-alpha(U), B-beta(U)),

with F(p,r,0,0)=true and with negative budgets disallowed. Every recursive
call strictly decreases A+B. Thus this is a finite acyclic Boolean circuit;
the full-turn case has at most 49 coefficient states for any fixed start and
budget. Common suffixes across several fans are shared by the search code.

For an interior selected tile T with coefficient pair (a_T,b_T), either the
complementary full fan must hold, or T must occur in a half-fan. In the latter
case enumerate its preceding coefficient pair (u,v), where

    0 <= u <= 3-a_T,     0 <= v <= 3-b_T.

Require a prefix of budget (u,v) ending on T's starting ray and a suffix of
budget (3-a_T-u,3-b_T-v) starting on T's ending ray. The board-boundary case
uses the table's prescribed start and budget. Hence the permanent implication

    x_T => (some complete full/half/boundary fan containing T)

is necessary for every actual tiling. Each variable introduced by the circuit
represents a complete contained physical placement. Any tiling projects to a
satisfying assignment by selecting precisely its generated placements and
setting auxiliary symbols to their actual path-existence values. Missing
placements away from this conditional local neighborhood impose no restriction.
The construction is complete locally even if every other generated catalogue
or endpoint system is finite and incomplete.

## Exact real-translation check for the through-edge tile

A half-fan runs counterclockwise from a ray r to -r and occupies the left
half-plane. A through-edge tile must occupy the right half-plane. There are
exactly six shapes with a side beginning at p along r on that side of the
line: three side lengths and two orders of the remaining adjacent lengths.
For a side length L, translate every vertex of this reference triangle by
-t*r, where 0<t<L. This parameterizes every possible through-edge placement
of that shape containing p in the relative interior of the side.

Every board half-plane inequality on each translated vertex has form
f0+t*f1 >= 0. All coefficients are rational in the axial frame. Intersect
the nine resulting closed intervals and then intersect with the open
interval (0,L). Reject a half-fan if all six intersections are empty.
Endpoints lying on the board remain permitted. A singleton t strictly
between zero and L also remains permitted. Thus this check covers every
real translation, including any that is not a generated endpoint placement.
It does not check overlap farther away from p with the fan's other tiles;
allowing such overlaps only weakens this necessary condition.

## Angular nonoverlap

For any finite set of generated placements that all have p as a vertex, sort
their exact outgoing side rays. In each open angular interval between consecutive
rays, at most one of the placements whose sectors contain that interval may
be selected. These are valid at-most-one constraints without any completeness
requirement on the finite set. Rays are sorted by exact half-plane signs and
integer determinants in axial coordinates. This includes overlapping sectors
with no common side ray, which the original same-ray wedge clauses do not see.

The fan circuits alone do not forbid overlap away from p and do not provide
a complete tiling algorithm. Angular groups likewise are local necessary
conditions. The independent full positive certificate checker remains required.

## Implementation and replay

* `corner_oracle.py` provides the finite local graphs, direct selected-fan
  evaluation, inline SMT terms, and exact angular interval groups.
* `corner_search.py` extends the existing complete-row solver. It installs
  all six outer endpoint corner circuits initially, then chooses a specified
  number of temporary-core rows for fan completion in each round. It adds
  the implications and circuit definitions permanently, preserves every such
  assertion when rebuilding Z3, and writes restartable root keys in
  `corners.json`.
  The optional `few_missing` core policy completes every core row whose full
  incident catalogue is already present before selecting a bounded number of
  rows that require new placements. Among equal expansion costs it prefers
  boundary rows and repeatedly encountered rows. This changes search order
  only. A memory threshold and an optional stop file write an explicit
  inconclusive checkpoint before terminating.
* `verify_corners.py` checks every one of the 429 corners in the known exact
  143-tiling, reconstructs sliding witnesses for every actual through-edge
  incidence, checks the six-placement catalogue on 54 interior rays, fixes
  every generated placement to the known tiling in SMT, repeats after a
  solver-context rebuild, and rejects a deliberately isolated interior tile.

Run the replay with the existing integer search directory as its sole argument.
The search requires the same installed `libz3.so.4` as the base solver. Its
resource limits and temporary-core UNSAT responses retain their original
meaning: inconclusive unless an independently verified positive certificate
or an unconditional negative certificate is obtained.

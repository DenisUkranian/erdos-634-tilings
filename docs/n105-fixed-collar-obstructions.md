# Two boundary collars that cannot extend: a four-placement proof

> **Historical stage — 29 September 2026.** Its limited claims remain as written. The later [global N=105 proof](n105-global.md) supersedes statements here that the count is unresolved. These old partial certificates are retained as regression evidence, not as the new proof.

29 September 2026. Exact scope: the two fixed coordinate certificates from the
boundary-collar calculation. **This does not exclude other collars, either
60-degree target at N=105, or N=105 globally.**

The 45-tile collar for `(5,21,19)` and the 57-tile collar for `(7,15,13)` each
cover a positive-width neighborhood of all three sides of an equilateral
triangle of side 105. Nevertheless, neither collar extends to a tiling of
the interior. In both cases one inner corner already gives a contradiction.
No large search or search cutoff is needed.

## Coordinates and the forced corner

Use the oblique basis `(1,0),(1/2,sqrt(3)/2)`. The target is
`(0,0),(105,0),(0,105)`, and squared lengths are `x^2+xy+y^2`.
The tile sides are `(a,b,c)` with `c^2=a^2-ab+b^2`; its opposite angles are
`alpha,beta,gamma`, with `gamma=pi/3`.

In each named collar the remaining region has a convex corner at

    P=(a,b).

The two boundary rays, in counterclockwise order around the unfilled sector,
are `(1,0)` and `(-a/c,b/c)`. Thus the unfilled angle is

    theta = pi-beta = alpha+gamma.

These are facts about the explicit collars, not assertions about an arbitrary
tiling. The replay checker verifies the exact local sector directly against
all already placed tiles.

For the two tiles, `2 cos(alpha)` is respectively `37/19` and `23/13`.
Therefore `alpha/pi` is irrational: otherwise `2 cos(alpha)` would be a
rational algebraic integer, hence an integer. As `beta=2pi/3-alpha`, a
decomposition of `theta` into tile angles must satisfy

    n_alpha-n_beta=1,     2 n_beta+n_gamma=1.

The only nonnegative solution is `(n_alpha,n_beta,n_gamma)=(1,0,1)`.
Exactly two tiles must therefore meet this corner, one contributing alpha
and the other gamma.

Take the first tile bordering the outgoing horizontal ray from P. Its
corner angle is either alpha or gamma; for either angle there are two
orders of the incident side lengths. These are all four candidates:

| Candidate | Three vertices |
|---|---|
| A1: alpha, horizontal side b | `(a,b), (a+b,b), (b,a+b)` |
| A2: alpha, horizontal side c | `(a,b), (a+c,b), (a+b(b-a)/c, b+ab/c)` |
| G1: gamma, horizontal side a | `(a,b), (2a,b), (a,2b)` |
| G2: gamma, horizontal side b | `(a,b), (a+b,b), (a,a+b)` |

This list does not assume edge-to-edge matching. A tile edge cannot pass
through P in its relative interior while filling an angle smaller than pi.
There is consequently a tile vertex at P and a whole tile edge starts along
the indicated ray. That edge may extend beyond any neighboring frontier
vertex; no restriction to the displayed boundary-segment length is imposed.

## Every candidate overlaps an existing collar tile

For `(a,b,c)=(5,21,19)`, the collar contains

    O1 = [(25,0), (555/19,25/19), (370/19,441/19)],
    O2 = [(0,61), (0,42), (105/19,718/19)].

For `(a,b,c)=(7,15,13)`, it contains

    O1 = [(0,30), (49/13,285/13), (225/13,270/13)],
    O2 = [(0,43), (0,30), (105/13,334/13)].

The following points lie **strictly inside both** the proposed candidate and
the named existing tile. This is checked by the three positive oriented-edge
determinants for each triangle; all coordinates are rational.

| Tile | Candidate(s) | Existing tile | Common interior point |
|---|---|---|---|
| (5,21,19) | A1, A2, G2 | O1 | `(20,22)` |
| (5,21,19) | G1 | O2 | `(16/3,38)` |
| (7,15,13) | A1, A2 | O1 | `(15,21)` |
| (7,15,13) | G1 | O2 | `(15/2,53/2)` |
| (7,15,13) | G2 | O1 | `(22/3,65/3)` |

Every possible first tile is obstructed. Hence neither fixed collar can
extend. This completes the proof for the two configurations.

## Exact replay

The proof records are each a one-node complete refutation:

* [n105-collar-refutation-5-21-19.json](../data/n105-collar-refutation-5-21-19.json)
* [n105-collar-refutation-7-15-13.json](../data/n105-collar-refutation-7-15-13.json)

Run:

    python scripts/verify_n105_collar_refutations.py

The checker does not import the search program and does not use its polygon
subtraction or boundary stitching. It independently checks the initial
congruent, contained, disjoint tiles; reconstructs the local empty angular
sector from incident triangles; enumerates all possible first-corner tile
placements; and rejects each by exact rational polygon clipping. It uses
only the Python standard library, rejects optimized Python modes that disable
assertions, and prints deterministic JSON without creating files.

For completeness, angle-sum enumeration is finite and exact. The checker
represents an angle by `(cos(theta),sin(theta)/sqrt(3))`, both rational here.
Adding any tile angle advances counterclockwise by an amount in `(0,pi)`.
Exact circular ordering detects a crossing of 2pi, so breadth-first
enumeration retains precisely all nonnegative angle sums below 2pi. No
floating-point angle comparison, guessed denominator bound, orientation
cutoff, or node cap is used.

The resulting reports contain `scope: two_fixed_collars_only` and
`global_N105_decided: false`. The saved report is [n105-collar-refutations.json](../verification/n105-collar-refutations.json).
The two replayed proof trees each have one node,
one impossible-placement leaf, and no further tile additions.

The preceding collar result should therefore be read narrowly:
outer-boundary coverage, congruence and nonoverlap do not by themselves
guarantee extendability. These two particular collars already fail the
additional inner-corner condition. They do not establish a barrier to all
arguments based on a first boundary layer.

# No nonzero height can contain exactly thirteen tiles

8 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
This is a necessary geometric condition, not a proof of impossibility for 154.

**Theorem.** In any I120 tiling by the primitive `(8,7,13)` triangle,
every occupied nonzero short-edge height contains at least 26 tiles.
The theorem allows arbitrary T-junctions and does not assume that the
tiles at a height form a connected set. In particular, for the 154
candidate,

    n_h >= 26 for every occupied h != 0.

Together with the existing `n_0=11 (mod 13)` and population divisibility,
there are at most six occupied heights. The proof below excludes the
previously allowed population 13 at *every* nonzero height, including
internal heights of the support.

## 1. Affine-line divisibility

Fix a nonzero short height h. A direction is `rho^j z^h`, where
`rho=exp(i*pi/3)` and `z=(8+7rho)/13`.

There are twelve possible oriented tiles at this height: types A_j and
B_j, j=0,...,5. Their gamma vertices and short edges follow
[the established reference triangles](../dual/DIRECTIONAL_SUPPORT.md):

    A_j: (0, 8rho^j, 7rho^(j+2)),
    B_j: (0, 7rho^j, 8rho^(j+2)),

all multiplied by z^h and then translated. These vertex orders are
counterclockwise. The short boundary edges therefore have data

    A_j: 8 in direction j; 7 in direction j+5,
    B_j: 7 in direction j; 8 in direction j+5.       (1)

Fix one complete affine line in any of the three unoriented directions
of height h. Integrate oriented boundary cancellation along that line.
All other tile edges on it have whole length 13: they are c-edges of
tiles whose short heights are h-1 or h+1. If h=1 or h=-1, a whole
exterior target side on this line has length `13 b m`, also divisible
by 13. For other nonzero heights there is no exterior side on it.
It follows that the signed sum of the height-h short-edge lengths on
*each separate affine line* is divisible by 13.                         (2)

This argument integrates complete edges on their supporting line.
It does not require a c-edge to coincide with a complete short-edge
chain, and remains valid with partial contacts and T-junctions.

## 2. Thirteen tiles force a single alternating sign

Suppose that n_h=13. Summing (2) over parallel lines gives divisibility
by 13 of the three signed direction currents J0,J1,J2, where reversing
a direction changes its sign. Apply the character `J0-J1+J2`.
By (1), each A_j contributes `(-1)^j` and each B_j contributes
`-(-1)^j`. Thus the character is a sum of thirteen numbers in {1,-1},
and is divisible by 13. It is odd and between -13 and 13, so it equals
13 or -13. **Every tile has the same character sign.**

Consequently all 8-edges have one direction parity and all 7-edges the
opposite parity. On any affine line they contribute with opposite signs.
If m 8-edges and n 7-edges lie on that line, (2) becomes

    8m-7n = 0 (mod 13),       m+n <= 13.            (3)

The second bound holds because a triangle has at most one short edge
in any one unoriented direction. The complete nonzero possibilities are

    (13,0), (0,13), (9,1), (5,2), (1,3),
    (6,5), (2,6), (3,9).                           (4)

Let (M,N) count all height-h 8-edges and 7-edges in one unoriented
direction. Its partition into affine supporting lines must be a sum
of the pairs (4). In the cases below the maximum number of such lines is

| Total pair (M,N) | Maximum number of nonempty supporting lines |
|---|---:|
| (13,0), (0,13), (9,1), (5,2), (1,3) | 1 |
| (6,5), (2,6) | 2 |
| (3,9) | 3 |

For example, (6,5) is either a single pair or (5,2)+(1,3), and
(3,9) can split into three copies of (1,3).

## 3. The nine orientation inventories

There are exactly 108 unsigned orientation inventories of total 13
whose three signed short-direction currents are all divisible by 13.
Modulo rotations by 60 degrees and reflection, they form the following
nine orbits, each of size twelve. Omitted orientation counts are zero.
This is a small exhaustive integer statement: restrict to the six
orientations of either common character sign and enumerate the weak
compositions of 13. The accompanying checker also independently obtains
the list by joining the A and B direction-current residue tables.

For each orbit the table picks a repeated orientation, gives the total
edge-count pairs in the directions of its two short edges, and bounds
the number of possible gamma vertices by the product of the two
supporting-line counts. The pairs may be listed in either short-edge
order.

| Nonzero orientation counts | Chosen orientation: count | Two direction totals (M,N) | Maximum gamma vertices |
|---|---|---|---:|
| B5=13 | B5: 13 | (0,13), (13,0) | 1 |
| B1=1, B3=3, B5=9 | B5: 9 | (3,9), (9,1) | 3 |
| B1=2, B3=6, B5=5 | B5: 5 | (6,5), (5,2) | 2 |
| A3=8, A5=2, B0=B2=B4=1 | A3: 8 | (9,1), (3,9) | 3 |
| A1=A3=A5=1, B0=1, B2=5, B4=4 | B4: 4 | (6,5), (5,2) | 2 |
| A3=4, A5=1, B0=1, B2=2, B4=5 | B4: 5 | (2,6), (9,1) | 2 |
| A3=4, A5=1, B0=2, B2=5, B4=1 | B2: 5 | (3,9), (5,2) | 3 |
| A3=4, A5=1, B0=5, B2=1, B4=2 | B0: 5 | (6,5), (6,5) | 4 |
| A3=3, A5=4, B0=B2=B4=2 | A3: 3 | (5,2), (6,5) | 2 |

The two direction families are nonparallel, so two selected supporting
lines intersect at most once. Each gamma vertex is their intersection.
In every row there are more tiles of the chosen orientation than
possible gamma vertices. Two such tiles therefore share their gamma
vertex and their orientation, so coincide. This contradicts disjoint
interiors and excludes n_h=13.

The established population theorem says that a nonzero height has
population divisible by 13. Excluding 13 therefore proves the theorem.

## 4. Check and scope

Run

```sh
python research/closure-position-oct7/oct8-structural/check_no_thirteen_height.py
```

The checker uses exact integers only, verifies all 108 inventories, all
nine symmetry orbits, the supporting-line partitions, and a gamma
pigeonhole contradiction for every inventory. Its companion report is
`no_thirteen_height_verified.json`. The geometric justification is (2)
and the intersection argument; no solver infeasibility status is used.

For 154, six occupied heights are still arithmetically possible because
`11+5*26=141 <=154`. This theorem alone neither supplies a tiling nor
proves that the remaining supports are impossible. It does not prove
that nonzero height populations must be multiples of 26: populations
39, 65, and other larger odd multiples of 13 are not excluded here.

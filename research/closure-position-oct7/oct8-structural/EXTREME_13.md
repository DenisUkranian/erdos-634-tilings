# An extreme height cannot contain exactly 13 tiles

8 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
This is a geometric necessary condition, not an exclusion of 154.

**Theorem.** In a tiling of an I120 target by the primitive tile `(8,7,13)`,
if the maximum occupied short height U is positive, then `n_U != 13`.
By reflection, if the minimum occupied height L is negative, then
`n_L != 13`. Consequently, the established population divisibility gives
`n_U >= 26` and `n_L >= 26` at these respective nonzero extremes.
No assumption about a connected extreme-height component is made.

## 1. Extreme signed inventories

Use the notation and oriented edge table in
[the complete direction-current proof](../dual/DIRECTIONAL_SUPPORT.md).
Write A and B for the signed three-vectors at height U, with antipodal
rotations subtracted. At height U+1 there are no short edges and no
exterior target edge, since U+1 >= 2. The current equation therefore
gives `13 R² B = 0`, hence B=0.

At height U, all contributions except the A and B short edges have
length divisible by 13. This includes the target boundary when U=1:
the relevant whole target side has length `13 b m`. Thus

    (8I - 7R²)A = 0 modulo 13,

or, in coordinates,

    8A0+7A1 = 8A1+7A2 = 8A2-7A0 = 0 modulo 13.       (1)

Assume `n_U=13`. The unsigned population dominates `||A||_1`; since
B=0, every B population and every cancellation in A uses an even number
of tiles. Therefore `||A||_1 <= 13` and `||A||_1` is odd.

The complete list of solutions to (1) satisfying those two conditions
consists of the rotations and negatives of

    (13,0,0), (9,-1,3), (6,-5,2).                    (2)

Here rotation acts as `R(A0,A1,A2)=(-A2,A0,A1)`.
All eighteen vectors in this list have L1 norm 13. A direct finite
check is supplied below; equivalently, substitute
`A1=-3A0 (mod 13)`, `A2=-4A0 (mod 13)` and retain the odd L1 ball.

It follows that there are no B tiles, and no antipodal cancellations
among the A tiles. After rotation by a multiple of 60 degrees, their
actual counts at rotations 0,2,4 are exactly one of

    (13,0,0), (9,3,1), (6,2,5).                    (3)

All other rotations have count zero. Thus the 8-edges run in the three
directions 0,2,4, and the 7-edges run in the opposite three directions.

## 2. Keep each supporting line

Fix a complete affine line of height U in one of these three unoriented
directions. Let m be the number of 8-edges of the height-U tiles on it,
and n the number of their 7-edges on it. The signs of these two kinds
are opposite. Integrating the oriented boundary cancellation along
this particular line, rather than summing all parallel lines, gives

    8m - 7n = 0 modulo 13.                         (4)

Indeed every other tile edge on the line is a whole 13-edge from
height U-1; there is no height U+1 tile and no B tile at height U.
If U=1, an exterior side on this line also has whole length divisible
by 13. Whole-edge integration is valid even with arbitrary partial
contacts and T-junctions. It does not assert that a whole 13-edge is
contained in the extreme-height union's boundary.

Since there are only 13 height-U tiles and each tile has at most one
edge in this fixed unoriented direction, `m+n <= 13`. The complete
nonzero possibilities for (m,n) in (4) are

    (13,0), (0,13), (9,1), (5,2), (1,3),
    (6,5), (2,6), (3,9).                          (5)

We now exclude the three cases (3). Each tile's gamma vertex is the
intersection of the supporting lines of its two short edges.

* **(13,0,0).** All thirteen 8-edges must lie on one line, because their
  total pair is (13,0); all thirteen 7-edges similarly lie on one line.
  All thirteen gamma vertices coincide. Their orientations are equal,
  so the triangles coincide, contrary to disjoint interiors.

* **(9,3,1).** In direction 0, the total pair is (9,1), which cannot
  split as a sum of two nonzero pairs in (5). Thus the nine rotation-0
  tiles have their 8-edges on a single line. In direction 2 the total
  pair is (3,9); its only possible nonzero summands are (1,3), (2,6),
  and (3,9), so there are at most three supporting lines. These carry
  the 7-edges of the same nine rotation-0 tiles. Consequently their
  gamma vertices occupy at most three points. Two tiles coincide.

* **(6,2,5).** In direction 4 the total pair is (5,2), which cannot
  split into two nonzero pairs in (5). Thus the five rotation-4 tiles
  have their 8-edges on a single line. In direction 0 the total pair
  is (6,5); it is either one pair (6,5), or the two pairs (5,2)+(1,3).
  There are at most two lines carrying the 7-edges of those five tiles.
  Their gamma vertices occupy at most two points. Again two tiles
  coincide.

All cases contradict nonoverlap. This proves the theorem.

## 3. Reproducible finite arithmetic

`check_extreme_13.py` exhausts the odd L1 ball for (1), checks that its
solutions are exactly the eighteen vectors in (2), checks (5), and
enumerates every decomposition needed in the three line arguments.
These are small exact integer enumerations. The geometric content is
the line-by-line cancellation and the gamma-vertex intersection argument
above; no floating-point solver status is used.

## 4. Scope

For N=154, the two nonzero endpoints of a two-sided support each cost at
least 26 tiles; for a one-sided support the nonzero endpoint costs at
least 26. This can strengthen the existing finite direction-inventory
search, but it is not by itself an impossibility proof for 154.
No claim that every extreme component has 26 tiles is made: the theorem
concerns the total population at the extreme height. No bound of 169
at that height has been proved.

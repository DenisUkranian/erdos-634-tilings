# Complete base-edge profiles and the additional angle-fan condition

8 October 2026. Necessary conditions for the 154 candidate only.
These computations do not exclude all five-height inventories.

## Exact profiles of the boundary edge tiles

Normalize the target to Eisenstein coordinates `(0,0),(154,0),(49,56)`.
The six tile placements above a horizontal base edge, written by apex
coordinate relative to its left endpoint, are:

| Type | Short height | Orientation | Base length | Apex |
|---|---:|---|---:|---|
| 0 | 0 | A0 | 8 | `(-7,7)` |
| 1 | 0 | B1 | 8 | `(8,7)` |
| 2 | 0 | B0 | 7 | `(-8,8)` |
| 3 | 0 | A1 | 7 | `(7,8)` |
| 4 | 1 | A3 | 13 | `(64/13,56/13)` |
| 5 | -1 | B4 | 13 | `(49/13,56/13)` |

These are all possibilities: a triangle on a fixed side has two
possible positions above that side, according to which remaining edge
meets its left endpoint. The reference A/B conventions are those of
`closure-position-oct7/dual/DIRECTIONAL_SUPPORT.md`.

Every actual exterior base is partitioned into whole edges of these
types. Partial internal contacts and T-junctions do not change this:
a triangle contained in a convex target cannot have an exterior edge
extend past the target boundary. Hence the edge endpoints occur at
integer distances along the base.

Both target base angles equal the tile angle alpha opposite side 8.
In particular, the left corner's unique incident tile is type 3 or 5,
and the right corner's is type 2 or 4. To justify uniqueness without a
numerical angle comparison, alpha+beta=pi/3 and gamma=2pi/3, whereas
alpha/pi is irrational. Indeed `cos(2 alpha)=73/169`. If alpha/pi were rational,
`2 cos(2 alpha)` would be a sum of two roots of unity, hence an
algebraic integer; its rational value `146/169` is not an integer.
The nonnegative angular equation for a corner of angle alpha
therefore has the sole solution one alpha tile.

The file `base_profiles.py` enumerates all words of these six types
whose base lengths add to 154, whose tiles lie in the target, and whose
interiors are pairwise disjoint. The first and last types obey the
corner restriction above. Each state keeps the six counts and the
last two tile types. This is sufficient for the nonoverlap check:
every tile extends horizontally by at most 4 beyond its base interval,
whereas two intervening base intervals have total length at least 14.
Thus a tile can overlap an earlier tile only when zero or one other
base interval lies between them.

All arithmetic uses integer Eisenstein coordinates scaled by 13.
Triangle containment uses oriented half-planes; nonoverlap uses exact
separating axes. A second implementation uses rational polygon
clipping to verify all 874 containment tests, 36 adjacent-type pairs,
and 216 triples with one intervening tile.

The exhaustive result is **2561 six-count profiles**, with 651 distinct
projections onto the four height-zero orientations. They are recorded
in `base_profiles.json`. They are possible boundary-edge packings, not
certificates that the region above them can be tiled.

For an actual complete unsigned orientation inventory, at least one
of the profiles must be coordinatewise bounded by

```
(A0 at h=0, B1 at h=0, B0 at h=0, A1 at h=0,
 A3 at h=1, B4 at h=-1).
```

An absent height contributes a zero count. This makes the condition
sensitive to the boundary positions and to the neighboring heights.

## Additional tiles at the boundary junctions

At an interior base junction every incident tile has a vertex there.
A tile edge containing that point in its relative interior would
otherwise cross below the exterior base, or itself occupy a base
interval already occupied by a boundary-edge tile.

The complete angle fan at such a junction is therefore either

```
one alpha + one beta + one gamma,
```

or

```
three alpha + three beta.
```

This follows from the irrationality just used: the equation
`a alpha+b beta+c gamma=pi` requires `a=b` and `b+2c=3`.
Two of these tiles are the consecutive boundary-edge tiles. The
remaining fan consequently has one or four additional tiles. For a
fixed incoming ray, each corner angle admits two mirrored triangle
placements. Thus the complete numbers of remaining fans are:

| Angles of the two boundary tiles at their common endpoint | Extra fans |
|---|---:|
| gamma, gamma | 0 |
| gamma, alpha or beta | 2 fans of one tile |
| alpha, alpha or beta, beta | 64 fans of four tiles |
| alpha, beta | 2 fans of one tile and 96 fans of four tiles |

`fan_probe.py` constructs these fans from exact rational rays and
reference triangles. `check_fans.py` verifies all 36 ordered base-type
pairs against the independent angle-word counts in this table.
Every produced short height lies in `[-3,3]`; the generator allows
`[-4,4]`. This bounded enumeration is complete because a straight fan
uses at most three alpha and three beta angles, and short-ray height
is the negative coefficient of alpha in its angular expression.

Additional fan tiles at different base junctions are **distinct**:
each such tile has just its fan vertex on the base, and its other two
vertices strictly above it. Thus their orientation counts, along with
those of the edge tiles, must fit inside the total unsigned inventory.
The file `boundary_fan_inventory.py` performs this additional finite
inventory check. It deliberately relaxes overlaps between tiles from
different fans, so a positive result remains only a necessary
condition. Resource exhaustion is reported as `INCOMPLETE`.

## Present outcome and limitation

The complete supplied unsigned five-height witness on `[0,4]` from
`../layers/filtered_0_4.json` fails this boundary-fan inventory test:
42,196 memoized states exhaust all possibilities. The corresponding
report is `boundary_fan_0_4.json`. This excludes **that inventory only**;
it does not exclude its signed-current vectors after other antipodal
pair expansions, much less all inventories on `[0,4]`.

The supplied witnesses on `[-1,3]` and `[-2,2]` pass the relaxed fan
inventory test. Their reports explicitly say
`EXACT_RELAXATION_FEASIBLE`. Neither report asserts a geometric tiling.

Run:

```sh
python research/closure-position-oct8/central/check_base_profiles.py
python research/closure-position-oct8/central/check_fans.py
python research/closure-position-oct8/central/boundary_fan_inventory.py research/closure-position-oct8/layers/filtered_0_4.json 30
```

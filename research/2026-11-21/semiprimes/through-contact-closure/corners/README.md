# Complete three-corner roots for unrestricted tilings

21 November 2026. **3431 and 5063 remain OPEN.** This package supplies a
complete finite list of necessary six-tile starting patterns for an
unrestricted full-board search. It does not assume the minimal odd
population, a height interval, a phase class, or edge-to-edge contact.

Both targets have **128 distinct surviving roots**. All 128 raw patterns
pass the exact tests used here; none is silently discarded. The complete
143 control also has 128 such roots, and its actual tiling uses
`O1-X2-Y2`.

| Board | Tile `(a,b,c)` | Raw roots | Surviving roots | Actual complete control |
|---:|---|---:|---:|---|
| 3431 | `(33,7,37)` | 128 | 128 | No completion asserted |
| 5063 | `(35,13,43)` | 128 | 128 | No completion asserted |
| 143 | `(5,3,7)` | 128 | 128 | Root `O1-X2-Y2` retained |

## 1. Why these corner cases are exhaustive

Use the standard frame

\[
O=0,\qquad X=b(2a+b),\qquad Y=a(a+2b)\rho,
\qquad \rho=e^{i\pi/3},\quad z=(a+b\rho)/c.
\]

The board angles at `O,X,Y` are respectively `alpha+beta`, `2alpha`,
and `2beta`, where the tile angles are `alpha,beta,2alpha+2beta`,
`alpha+beta=pi/3`, and the third angle is 120 degrees.

The [unrestricted corner-fan theorem](../../../../2026-11-20/semiprimes/continuation/vertex-phase/CORNER_FANS.md)
proves the relevant angle independence. In particular
`2*cos(beta)=(2a+b)/c` is rational strictly between one and two. If
`beta/pi` were rational, this rational algebraic integer would have to
be an integer. Thus `beta/pi` is irrational, and `alpha,beta` are
rationally independent.

Every tile meeting a board corner has that point as one of its vertices.
A tile whose side passes through the corner would contribute a half-plane,
which cannot fit inside any of these board angles. The independent angle
coefficients therefore force exactly these sectors:

| Corner | Required counterclockwise angle order | Choices |
|---|---|---:|
| `O` | `alpha,beta` or `beta,alpha` | 2 |
| `X` | `alpha,alpha` | 1 |
| `Y` | `beta,beta` | 1 |

For each angle and each fixed first ray, exactly two whole congruent
triangles are possible. At an alpha corner the incident side lengths
are `b,c` in either order; at a beta corner they are `a,c` in either
order. This includes both reflections. Hence the numbers of two-tile
fans are `2*2*2=8`, `2*2=4`, and `2*2=4`, giving

\[
8\cdot4\cdot4=128.
\]

Every full tiling contains one of these roots. The six tiles are distinct:
the distances between board corners exceed the largest tile side `c`.
The list is a containing list; survival of a root says nothing about
whether it extends to a tiling.

### No accidental height or T-junction restriction

Starting rays are `(h,j)=(0,0),(2,1),(0,4)` at `O,X,Y`, with directions
`z^h*rho^j`. The exact increments for alpha and beta are

\[
(h,j)\longmapsto(h-1,j+1),\qquad
(h,j)\longmapsto(h+1,j).
\]

The incident placements are obtained from the existing complete
24-placement endpoint catalogue, then filtered by the prescribed sector.
These are locally forced orientations, not a truncation of the full
tiling's heights. Some valid root tiles have short height **-1**.

The two sides on a corner seam may have different lengths. Ten of the
sixteen corner variants have this feature and remain in the list. Their
common two-bank portion has length equal to the smaller side, while the
known straight seam itself continues at least to the larger endpoint.
The shorter endpoint is allowed to be a T-junction; its eventual other
neighbors belong to the continuation problem.

## 2. Exact pruning rules and their scope

The enumerator applies the following globally necessary checks to every
raw root and records a reason for any rejected case. All checks happen
to pass on all 128 patterns at each of the three boards.

### Whole-triangle containment

In axial coordinates the board inequalities are

\[
x\ge0,\quad y\ge0,\quad Bx+Ay\le AB,
\qquad A=b(2a+b),\ B=a(a+2b).
\]

They are checked at every vertex of every root triangle, with rational
arithmetic. Convexity makes these vertex checks sufficient for containment.

### Positive-area overlap

All fifteen triangle pairs in each root are tested by exact separating
axes along their edges. Boundary contacts, including partial contacts
and shared vertices, are allowed. Any positive-area intersection would
exclude that root from a full tiling.

### Boundary prefix arithmetic

A tile vertex on an outer side is a genuine partition point of that
side. Another tile cannot pass through it along that same boundary and
occupy the interior half-plane while the selected tile contributes a
positive sector. Both distances from the vertex to the side's endpoints
must therefore be sums of full side lengths `a,b,c`. This is the
necessary arithmetic already used by the unrestricted `Geometry.legal`.

### Remaining-side gap arithmetic

There is a further joint boundary check. Collect the exterior-side
intervals occupied by all six selected triangles and take their union.
Every gap between fixed intervals, or between one fixed interval and a
board endpoint, must have length in

\[
\{ia+jb+kc:i,j,k\in\mathbb Z_{\ge0}\}.
\]

Indeed the other tiles partition the gap by their complete outer sides.
No such side can cross into a fixed selected boundary interval: both
triangles would lie inside the board on the same bank and would overlap
in positive area. Thus neither an overhanging edge nor a T-junction can
invalidate the gap's necessary semigroup condition. This cut uses only
actual fixed exterior intervals. It is not applied to arbitrary internal
segments or unfinished internal banks.

The generator checks this semigroup with the existing unbounded-coin
table. The independent verifier uses a different algorithm: shortest
representable distances modulo `b`. An integer `L` is representable
exactly when it is at least the shortest distance in residue `L mod b`.

## 3. Corner seams give extension constraints, but no root exclusion

The [corner-seam theorem](../../../../2026-11-20/semiprimes/continuation/first-cuts/CORNER_RAYS.md)
proves that, at unit scale, the initial straight seam from `O` cannot
meet the initial straight seam from either `X` or `Y`. Their proposed
intersections would have nonintegral distances from the emitting board
corners, whereas an actual noncollinear seam meeting is a side endpoint
on both straight runs and has integral offsets.

Each JSON file records the four exact intersection thresholds. A
continuation may use the following necessary constraint: the relevant
two initial straight seams cannot both continue at least as far as their
listed meeting distances. Equality counts as a meeting and is forbidden.
These constraints concern uninterrupted initial straight portions, not
arbitrary bent descendants of the corner seams.

The root triangles guarantee only the maximum of their two incident seam
side lengths, at most `c`. The verifier checks that **both** distances in
all four forbidden meetings are greater than `c` for every board here.
Therefore this inherited theorem excludes no six-tile root by itself.
The `X` and `Y` seams have an arithmetically permissible intersection;
they are not declared disjoint.

The placed boards are scalene, so their only Euclidean self-isometry is
the identity. No reflection, corner permutation, or exchange of `a,b`
is used to identify different roots. The verifier checks that all 128
surviving root sets are physically distinct.

## 4. Machine interface

The generated files are
[`ROOTS_3431.json`](ROOTS_3431.json),
[`ROOTS_5063.json`](ROOTS_5063.json), and
[`ROOTS_143.json`](ROOTS_143.json). Their schema is
`three-corner-roots-v1`.

Each `surviving_roots` record contains:

```json
{
  "id": "O0-X0-Y0",
  "corner_variant_ids": [0, 0, 0],
  "tiles": ["six ordinary Geometry tile keys"],
  "corner_tile_indices": [[0, 1], [2, 3], [4, 5]],
  "seams": ["three exact seam records"],
  "remaining_boundary_gaps": ["exact rational lengths and semigroup results"]
}
```

An actual tile key is `[[qx,qy,e],h,j,s]`, directly compatible with
`global_core_sat.Geometry`. Its obtuse vertex is
`(qx+qy*rho)/c^e`; its other vertices are
`q-a*z^h*rho^j` and `q+b*z^h*rho^(j+s)`. There is no new coordinate
convention or conversion step. The corner tiles are ordered
counterclockwise from the specified initial board ray.

`corner_variants` gives the complete 8/4/4 factorization, including side
orders and exact vertices. `raw_roots` retains every raw combination and
its rejection list. `seam_constraints` contains the rational thresholds
described above. The six-tile list is intended to be asserted as one
branch of a complete disjunction; selecting a single root does not
represent the unrestricted problem unless every other root is also
handled or independently excluded.

## 5. Generation and independent verification

From the repository root:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/corners/enumerate_corner_roots.py
python3 research/2026-11-21/semiprimes/through-contact-closure/corners/verify_corner_roots.py
```

Both commands use the Python standard library. The generator imports the
existing unrestricted geometry and corner-sector code. The verifier
imports neither: it directly rotates each board ray through alpha and
beta and constructs both adjacent-side orders. It checks that these
independently obtained physical triangles coincide with every saved tile
key and that all 128 Cartesian products are present.

For the 143 positive control, the verifier reads the existing complete
certificate, reconstructs all 143 triangles, checks all 10,153 pairs for
interior disjointness, checks exact metric and containment, and confirms
that their total area is the board area. It then extracts its actual
two triangles at each board corner and finds the saved root
`O1-X2-Y2`. This is a whole-tiling control, not just six locally valid
triangles.

The result is recorded in [`CORNER_ROOT_REPLAY.json`](CORNER_ROOT_REPLAY.json).
These finite checks establish catalogue completeness under the cited
angle theorem and the stated necessary geometric tests. They do not
assert that either target root list has been exhausted by a completion
search, and they do not decide either tiling question.

# Independent audit of the adjacent-parameter W construction

8 October 2026. Internal independent implementation and mathematical audit;
not a claim of external referee acceptance or priority.

**Result: PASS.** For every integer u>=2, put v=u+1 and m=u+2. The W
triangle with sides

    m(v³, u(2v²-u²), v(v²-u²))

has a tiling by

    (2v²-u²)m² = (u²+4u+2)(u+2)²

congruent triangles with sides (uv,2u+1,v²).

The complete construction is in
[`../group1-adjacent/PROOF.md`](../group1-adjacent/PROOF.md), together with
the outside macrocoordinates in `ADJACENT_MACRO_REDUCTION.md`. The finite
parameter u is unrestricted beyond u>=2. This gives the previously omitted
scale v+1 in each adjacent-parameter W family, not all scales >=v.

For every u>=2 this scale lies outside the older sufficient set
v+<u,v>: its increment over v is one, while both generators exceed one.
Thus the old cap semigroup is strictly smaller than the true scale
spectrum for every member of this infinite adjacent-parameter family.

The existing beta transfer also supplies the isosceles target at this
same scale, with count

    (3v²-u²)(u+2)² = (2u²+6u+3)(u+2)².

This corollary attaches the ordinary tile triangle at scale v(u+2);
it does not need a new negative argument or an additional search.

## 1. Independent formula implementation

`adjacent_formula.py` was written from the displayed geometric formulas,
without importing the search code and without a solver. It generates the
ordinary grid cells of each region, removes exactly one whole corner tile
from the final upper strip grid, and generates the complementary cap
including that same region. There are no negative-weight tiles.

`verify_general_geometry.py` imports neither the construction nor a solver.
For each exported certificate it checks the exact tile metrics, positive
areas, target containment, total area, and every pair of tile interiors.
Its separating-axis calculations use only integers. Results:

| u | Tile count | Pair checks | Result |
|---:|---:|---:|---|
| 2 | 224 | 24,976 | PASS |
| 3 | 575 | 165,025 | PASS |
| 4 | 1224 | 748,476 | PASS |
| 5 | 2303 | 2,650,753 | PASS |

These checks establish exact individual constructions and detect formula
implementation errors. The universal quantifier is justified separately
below, not inferred from this table.

## 2. Universal symbolic geometry

`check_adjacent_symbolic.py` implements elementary polynomial arithmetic
over Z[u], without a computer algebra package. It first collapses the
ordinary central-strip grids into their combined positive convex region,
with the corner triangle removed. Together with the five right-end and
nine left-end regions this gives **15 fixed positive macroregions** for
the residual polygon, independent of u.

For every macroregion, the checker proves positive signed area and
convexity: all necessary determinants, after the exact substitution
u=t+2, have nonnegative integer coefficients. The area polynomials also
have strictly positive constant term. Thus these are proofs for every
real u>=2, not evaluations at sample parameters. The central-strip grids
are disjoint because their column intervals meet only at endpoints; their
upper and lower fringes have the displayed sloping strip boundaries.

The checker then proves **exact positioned-boundary equality**. Each
boundary edge is assigned its direction class, supporting-line offset and
two exact polynomial endpoints. It contributes +1 at its initial endpoint
and -1 at its final endpoint. After subtracting the target boundary every
event cancels identically in Z[u]. This is stronger than checking total
lengths or total area. On any fixed supporting line, the derivative of
the signed interval-coverage function is exactly this endpoint event
list. Zero events and compact support imply zero signed interval
coverage on the whole line.

The checker independently repeats this identity for the **entire W
target**, adding the four outside grid macroregions. Multiplying all
coordinates by b=2u+1 clears denominators. All **19 positive convex
macroregions** have the exact positioned boundary of the target triangle.
Their area and target tile-count identities are also checked symbolically.

Why does this certify a real dissection? The difference between the sum
of the region indicator functions and the target indicator has zero
distributional boundary, hence is constant off the finite edge set. It
has compact support, so the constant is zero. The region multiplicities
are nonnegative integers, therefore each target interior point away from
edges has multiplicity exactly one and points outside have multiplicity
zero. The finite closed union covers the target boundary as well. Thus
there are no overlaps or holes. No separate gluing normal form is assumed.

## 3. Primitive metrics and grid hypotheses

Let E=z^(-2), F=z, z=(-u+sqrt(-D))/(2v), D=4v²-u². The oblique basis
is vE,vF. The physical metric in these coordinates has Gram form

    v²(x²+y²) + [u(3v²-u²)/v]xy.

Consequently the coordinate triangles of legs (u,v) and (v,u) both
have physical side lengths uv,v²,b. Their ordinary rectangles and
triangular grids therefore consist of copies of the same original tile.

The symbolic checker verifies every edge length of the four outside
macros in this metric, and verifies the exact parallel-base homothety
identity for each annulus. The prescribed outer and inner grid scales
are integers with outer>inner>=0 for every u>=2. Hence the outside
regions also contain actual positive unit-grid tilings.

Finally the corner exchange is checked symbolically: in left-cap
coordinates its vertices are

    (k,-u²), (k,-uv), (u²,-uv),   k=u²-u-1.

Their differences are (0,-u) and (v,-u), so this is exactly one B-unit
tile. After translation by V it equals the corner removed from the last
upper strip triangle. This equality is the essential interface that was
missing from the earlier incomplete endcap separations.

## 4. Reproduction and scope

```sh
python research/universal-closure-oct8/group1/check_adjacent_symbolic.py
python research/universal-closure-oct8/group1/adjacent_formula.py --u 5 --output /tmp/W2303.json
python research/universal-closure-oct8/group1/verify_general_geometry.py /tmp/W2303.json
```

The symbolic report is `adjacent_symbolic_verified.json`. The construction
proves a new sufficient parameterized family within this project. Prior
global realizability of an individual count using other shapes or tiles
must still be distinguished from this fixed-family statement. It does not
prove necessity of any scale condition and does not solve the full
classification requested in Erdős problem 634.

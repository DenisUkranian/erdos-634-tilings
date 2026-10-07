# A concrete second-junction escape in the W56 corner

7 October 2026. This package does **not** decide W56, classify the W scale
spectrum, or solve Erdős 634. It records an actual partial patch explaining
why the next natural corner-forcing induction needs a new argument.

## The exact patch

Coordinates `(x,y)` mean physical coordinates `(x,sqrt(2)y)`. The target
is `(0,0),(56,0),(46,20)`, with sides `(56,54,30)` and area 56 times
the area of the tile `(6,5,9)`. Put

    L_i=(23i/3,10i/3),  0<=i<=6.

The six triangles `[L_i,L_i+(6,0),L_(i+1)]` are valid boundary tiles
along the target's side of length 54. At `L_1`, add their usual first
half-turn mate `[L_1,(6,0),L_1+(6,0)]`.

The next junction `V=L_2=(46/3,20/3)` does **not** have to be filled by
the usual single gamma tile on the evidence of these placed tiles alone.
The following three tiles fit instead:

| Tile | Vertices |
|---|---|
| 1 | `V, (41/3,10/3), (55/3,2/3)` |
| 2 | `V, (55/3,2/3), (20,4)` |
| 3 | `V, (173/9,40/9), (73/3,20/3)` |

Their angles at V are respectively alpha, beta, alpha. Thus they fill
exactly `2alpha+beta=gamma`, while no individual tile has gamma at V.
Tiles 1 and 2 share a complete c-edge. Tiles 2 and 3 have a legitimate
T-junction: a length-5 edge occupies the first five units of a length-6
edge. The length-9 horizontal edge of tile 3 also passes through
`V+(6,0)`, with integral pieces 6 and 3.

The normal mate at `L_3` still fits:

    [(64/3,20/3), (29,10), (23,10)].

This produces eleven actual nonoverlapping tiles inside the target.
Every known seam atom is integral. The file `verify_local_patch.py` is
an independent checker: it imports no search or constructor, checks all
three squared side lengths of each tile, all target half-planes, all 55
pairs by exact separating axes, and all known seam atoms. Its certificate
and short report are `W56-local-escape-patch.json` and
`local-patch-verification.json`.

This is an escape from **immediate local forcing**, not a counterexample
to a global corner-extraction theorem: whether the remaining 45 tile areas
can be filled is unknown. If the whole standard six-fold corner could be
forced, its complement would be theta(6,5,9) at scale 2, which is impossible
because `b(T-1)=5<2v=6`; see
[`../../docs/theta-branch.md`](../../docs/theta-branch.md), Section 3.
The displayed three-angle fan is the concrete alternative that such a
global argument must eliminate or transform.

`local_fans.py` enumerates full fans only at this specified junction with
these specified preceding boundary tiles. It finds 26 geometrically
admissible fans before continuation checks. Exact necessary filters and
forced local placements reject 24; the ordinary gamma mate and the
displayed alpha-beta-alpha fan remain unresolved. This does not enumerate
all W56 boundary words or prove either survivor extendible.

## Why simply scaling the existing cap cannot reduce its step

For general coprime `0<u<v`, put `a=uv,b=v^2-u^2,c=v^2`. Scaling the
known +u six-block cap to an integer increment d scales it by `d/u`.
Five of its six blocks retain integral grid dimensions. The remaining
parallelogram has side lengths

    X=cK, Y=bK, K=d(v-u),

and would need cells of sides a,b in either order along its two axes.
Such a cell tiling exists **if and only if u divides d**.

Sufficiency is the original grid, since then `X/a=vK/u` and `Y/b=K`
are integers. For necessity, apply the affine coordinate change taking
the two unit axis vectors to orthogonal unit vectors. A putative filling
becomes a rectangle tiled by a-by-b rectangles in the two orientations.
Integrate `exp(2*pi*i*(x+y)/a)` over the whole rectangle. Every tile has
zero integral because one of its coordinate side lengths is a. The outer
rectangle integral therefore vanishes, so `a|X` or `a|Y`. In the first
case `uv|v^2 K` forces `u|K`; in the second, `gcd(a,b)=1` gives `a|K`
and hence again `u|K`. Since `gcd(u,v-u)=1`, both imply `u|d`.

This is an exact obstruction to filling that unchanged macroregion with
the two-axis cells. It is not an obstruction to changing the macroregion,
using other triangle orientations, or building a different collar.

## Search record, explicitly incomplete

`pruned_search.py` adds three sound necessary tests to the archived exact
convex-corner search: integer known seam segments, exact convex angle-fan
feasibility, and integral areas of separated residual components. It also
maintains the residual boundary incrementally. The angle fan generation
uses only rational rotations and their sine signs; it uses no floating
angle cutoff.

The final W56 run, `W56-pruned-search-v2.json`, stopped after 180 seconds,
13,331 nodes, and depth 44/56. It rejected 2,133 impossible angle fans,
60 nonintegral seam states, and 48 nonintegral component areas, but its
status remains **INCOMPLETE**. Earlier bounded runs and the fixed six-edge
strip run were likewise incomplete. The positive control W28 was found
and is stored separately. None of these resource-limited runs is a negative
certificate. The complete fixed-tile W spectrum for `(6,5,9)` remains
unknown at scales 2 and 4.

Fast reproduction:

    python research/group1-global-scales/verify_local_patch.py
    python research/group1-global-scales/local_fans.py

The known positive scales remain `3+<2,3>={3,5,6,7,...}`. No new positive
or negative W count is claimed by this package.

# A uniform macro ansatz extracted from the 224 certificate

8 October 2026. Uniform construction, extending the fixed-(6,5,9)
theorem in `PROOF.md`.

The 224 certificate has a useful extension to the adjacent primitive
parameters u>=2, v=u+1 at scale m=v+1=u+2. The four outer macroregions
below are explicit ordinary triangular grids or their trapezoidal
annuli. The residual region is now completed for every u>=2 by the
[one-tile-exchange construction](../group1-adjacent/PROOF.md). The
independent [symbolic audit](ADJACENT_UNIVERSAL_AUDIT.md) verifies the
whole parameterized dissection; the result does not rest on the finite
examples below.

Put

    a=uv, b=2u+1=v²-u², c=v², Q=2v²-u², D=4v²-u²,
    z=(-u+sqrt(-D))/(2v), E=z^(-2), F=z.

Physical complex coordinates use the oblique basis vE,vF. In this basis,
the following two coordinate triangles are congruent to the original
(a,b,c) tile:

    (0,0),(u,0),(0,v),
    (0,0),(v,0),(0,u).

Their half-turns are also allowed. Indeed, their two axis edges have
lengths a,c, and aE-cF and cE-aF both have length b. These right-looking
coordinate triangles are not physically right triangles: the basis is
oblique.

## 1. Four ordinary grid macroregions

Along the left side of the W target, from its bottom corner to its apex,
place the following four regions, all with horizontal bottom and top
cuts in physical coordinates:

| Region | Outer grid scale | Inner grid scale | Count |
|---|---:|---:|---:|
| First a/b triangle annulus, c horizontal | u(u+2) | u | u²((u+2)²-1) |
| First a/c triangle annulus, a horizontal | v | 1 | v²-1 |
| Second a/b triangle annulus, c horizontal | 2u | u-1 | 4u²-(u-1)² |
| Upper a/c triangle, a horizontal | u+2 | 0 | (u+2)² |

Here an annulus means an ordinary integral triangular grid with a
smaller homothetic corner grid removed along a grid line. Thus its
tile count is the difference of the two displayed squares; no negative
tile weights are used.

For reproducibility, the complete rational macrocoordinates are returned
by `shape(u)` in `adjacent_macro_search.py`. They use the target

    O=(u m v³/b, -u² m v²/b),
    A=(-u v m, u²m),
    C=(-u v m, v²m).

The function's four macro polygons have disjoint horizontal height
intervals in physical coordinates. Their left endpoints lie in order
on OC. Their right endpoints lie on or to the interior side of AC:
the AC line is x=-uvm in the oblique coordinates. Their horizontal
lengths are positive because all outer scales exceed their inner
scales. The first lower base fits on OA since its physical length is
u m c < u m Q. These observations verify their containment and disjoint
interiors for u>=2.

Their total count is

    u^4+4u^3+8u²+8u+3.

The difference from the target count Qm² is

    R(u)=4u³+14u²+16u+5.

## 2. The remaining integer-coordinate polygon

After the four macros have been removed, the residual polygon has
vertices, in boundary order,

    (0,0),
    (-u v m, u²m),
    (-u v m, v²m),
    (-u²m, u v m),
    (-u²m+v², u v²),
    (-u²v, u v²),
    (u v, u v),
    (u(2u+1),0).

Thus a tiling of this explicit polygon by the two coordinate triangles
above, and their half-turns, gives an actual W tiling at scale v+1. This
is a sufficient reduced construction problem. No assertion is made that
every W tiling has these four macros or this residual form.

Most of the residual is a long strip between

    y=-(u/v)x,   y=-(u/v)x+u(2u+1).

It admits ordinary rectangular grids. The uniform construction joins
these grids to the upper-end polygon by moving one corner B-tile from
the last upper strip triangle into the adjacent cap. Choosing the strip
phase carelessly and isolating a thin parallelogram would fail; the
coupled construction in the linked proof avoids that separation.

## 3. Exact finite completions

`adjacent_macro_search.py` enumerates integer-coordinate positions of
both residual tile types, with both half-turns. It imposes exact
positioned-boundary equality and Boolean selection variables. Positive
solutions are expanded together with all four grid macros into complete
unit-coordinate certificates.

| (u,v) | Scale | Target sides | Tile | Count | Status |
|---|---:|---|---|---:|---|
| (2,3) | 4 | (108,112,60) | (6,5,9) | 224 | Original full certificate in `PROOF.md` |
| (3,4) | 5 | (320,345,140) | (12,7,16) | 575 | Exact full unit certificate PASS |
| (4,5) | 6 | (750,816,270) | (20,9,25) | 1224 | Exact full unit certificate PASS |

The independent `verify_general_geometry.py` imports neither the search
nor a solver. It verifies congruence, containment, total area, and every
pair of tile interiors by exact separating-axis tests. It checks 165,025
pairs for 575 and 748,476 pairs for 1224.

These are fixed-tile, fixed-target results. In particular 575 was already
globally realizable using the other tile (6,5,9) in its beta target at
scale five; no claim of a new global admissible integer is made for that
example. No priority claim is made for either fixed-shape construction.

The new seeds can be extended by the already proved cap: scale five
with (u,v)=(3,4) extends by increments three, and scale six with (4,5)
extends by increments four. This does not determine their complete
fixed-tile scale spectra.

The solver-free `adjacent_formula.py` now generates every member of the
uniform family. Its independent full-coordinate checks passed at u=2,3,4,5,
with counts 224,575,1224,2303. `check_adjacent_symbolic.py` separately proves
the metric, positivity, positioned-boundary and area identities as exact
polynomials for every u>=2. The universal theorem is

    N=(u²+4u+2)(u+2)², tile (u(u+1),2u+1,(u+1)²), u>=2.

The W target sides are

    (u+2)((u+1)³, u(u²+4u+2), (u+1)(2u+1)).

This is a uniform sufficient family. It does not classify every W scale
or every count in Erdős problem 634.

Reproduction, from the repository root:

```sh
ERDOS_ORTOOLS_PATH=/tmp/erdos634-ortools python research/universal-closure-oct8/group1/adjacent_macro_search.py --u 3 --seconds 60 --prefix research/universal-closure-oct8/group1/W575_adjacent
python research/universal-closure-oct8/group1/verify_general_geometry.py research/universal-closure-oct8/group1/W575_adjacent.certificate.json
```

The analogous u=4 certificate uses prefix `W1224_adjacent`. OR-Tools is
needed only to search; the retained positive certificates can be checked
with standard Python alone.

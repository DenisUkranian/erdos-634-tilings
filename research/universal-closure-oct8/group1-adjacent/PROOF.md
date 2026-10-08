# A uniform completion of the adjacent-parameter W remainder

Let `u>=2`, `v=u+1`, `m=u+2`, and `b=2u+1`. Work in the oblique
coordinates of `group1/adjacent_macro_search.py`. An A-tile has coordinate
vertices `(0,0),(u,0),(0,v)`; a B-tile has vertices
`(0,0),(v,0),(0,u)`. Translations and half-turns are allowed. Both correspond
to the same physical `(uv,b,v^2)` tile.

An A-grid triangle of scale n has legs `nu,nv`; a B-grid triangle of scale n
has legs `nv,nu`. It contains n^2 unit tiles. An axis-parallel rectangle with
side lengths integer multiples of the corresponding legs is tiled by the
ordinary rectangular grid, with each small rectangle divided along its
negative-slope diagonal.

The four already specified outside macros leave the eight-vertex polygon

```
X=(0,0), A=(-uvm,u^2m), C=(-uvm,v^2m), V=(-u^2m,uvm),
U=(-u^2m+v^2,uv^2), R=(-u^2v,uv^2), S=(uv,uv), Q=(ub,0).
```

The following finite, parameterized dissection tiles this entire remainder.
The only exchange between its central strip and left cap is one B-tile.

## 1. Central strip

For `j=0,...,u`, put

```
P_j=(-v-j*uv, u+j*u^2).
```

Include the square with lower-left corner P_j and side uv. Each such square
contains 2uv A-tiles (or, alternatively, 2uv B-tiles).

For every `j=0,...,u`, include the B-grid triangle of scale u with vertices

```
P_j+(0,uv), P_j+(0,uv+u^2), P_j+(uv,uv).
```

For `j=u` alone remove its uppermost B-unit tile. Explicitly, if
`F=P_u+(0,uv+u^2)`, remove the triangle

```
F, F+(0,-u), F+(v,-u).
```

Thus the last upper piece is a grid triangle with its corner unit removed,
and it contains u^2-1 tiles. This is a positive trapezoidal grid region.

For `j=1,...,u`, include the B-grid triangle of scale u with vertices

```
P_j, P_j+(uv,0), P_j+(uv,-u^2).
```

These squares and triangles have disjoint interiors. The lower and upper
strip lines are respectively `u*x+v*y=0` and `u*x+v*y=uv*b`.

## 2. Right end, in the original coordinates

Put `x0=v*(u-1)`. The right end is covered by the following five pieces:

1. B-unit triangle `(0,0),(-v,u),(0,u)`.
2. B-grid rectangle `[0,x0] x [0,u]`, containing `2(u-1)` tiles.
3. B-grid rectangle `[x0,uv] x [0,uv]`, containing `2v` tiles.
4. A-grid triangle of scale u with vertices `(uv,0),(ub,0),(uv,uv)`.
5. B-unit triangle `(x0,uv),(uv,uv),(x0,uv+u)`.

The first two pieces fill the trapezoid below the j=0 square. The last three
fill the quadrilateral with vertices `(x0,0),Q,S,(x0,uv+u)`.

## 3. Left end, in coordinates translated by V

Every coordinate in this section is relative to the original point
`V=(-u^2m,uvm)`: add V to obtain coordinates in Sections 1 and 2.
Put `k=u^2-u-1`. Include these nine pieces:

| Piece | Exact vertices or rectangle | Unit count |
|---|---|---:|
| A-grid triangle, scale v | `(-um,vm),(-um,v),(-u,v)` | `v^2` |
| B-grid rectangle | `[-um,-u] x [1,v]` | `2u` |
| A-unit triangle | `(-u,0),(-u,v),(0,0)` | `1` |
| A-grid rectangle | `[-um,-u] x [-um,1]` | `2v^2` |
| B-grid triangle, scale u | `(-um,-um),(-u,-um),(-u,-2uv)` | `u^2` |
| A-grid rectangle | `[-u,0] x [-uv,0]` | `2u` |
| B-grid triangle, scale v | `(0,0),(0,-uv),(v^2,-uv)` | `v^2` |
| B-grid rectangle | `[-u,k] x [-2uv,-uv]` | `2v(u-1)` |
| B-grid triangle, scale u-1 | `(-u,-2uv),(k,-2uv),(k,-3u^2-u)` | `(u-1)^2` |

The rectangle dimensions follow from the exact identities

```
um+1=v^2,   um-u=uv,   k+u=(u-1)v.
```

All dimensions and grid scales are positive for u>=2. The first five pieces
are disjoint by their displayed horizontal and vertical cuts. After those
cuts, the remaining nominal left cap is the seven-vertex polygon

```
(-u,-2uv), (-u,0), (0,0), (v^2,-uv),
(u^2,-uv), (k,-u^2), (k,-3u^2-u).
```

The last four pieces fill precisely that polygon **plus** the B-unit triangle

```
H=(k,-u^2), K=(k,-uv), R=(u^2,-uv).
```

Indeed `R-H=(v,-u)` and `K-H=(0,-u)`. Adding this unit triangle replaces
the notch `R,H,(k,-3u^2-u)` by the straight horizontal/vertical cut through K.
The resulting polygon splits immediately into the last four listed pieces.

Finally this added unit is exactly the corner removed from the j=u upper
strip triangle in Section 1: translating that strip apex by minus V gives
`H=(k,-u^2)`. Hence there is neither a missing region nor an overlap at the
only nontrivial interface.

The remaining interfaces follow the two strip lines and the stated vertical
cuts. All outer edges are exactly the eight boundary edges of the remainder.
Thus these pieces form a dissection, including their shared boundaries.

## 4. Count and scope

The central strip contributes

```
2uv(u+1) + (2u+1)u^2 - 1 = 4u^3+5u^2+2u-1.
```

The right end contributes `u^2+4u+2`, and the left end contributes
`8u^2+10u+4`. Their sum is

```
4u^3+14u^2+16u+5,
```

the exact unit count in the original eight-vertex remainder. Together with
the four outside macros, the W construction therefore uses

```
N=(2v^2-u^2)*(u+2)^2
```

congruent `(uv,2u+1,v^2)` tiles. This proves scale `v+1` for every adjacent
pair `v=u+1`, `u>=2`. Ordinary subdivision gives its positive multiples.
It does not assert that every scale at least v is realizable.

The full W target has sides `m*(v^3,u(2v^2-u^2),vb)`. They are ordered
`mvb < mv^3 < mu(2v^2-u^2)`, since
`u(2v^2-u^2)-v^3=u^2-u-1>0`. The tile sides are ordered
`b<uv<v^2`. Their respective smallest-to-middle ratios are `b/v^2` and
`b/(uv)`, which differ. Thus the target is not similar to the tile.

Equivalently, with `t=u+2`, this gives the simple infinite family

```
N=t^2*(t^2-2),  t>=4,
tile=((t-2)(t-1), 2t-3, (t-1)^2).
```

The first counts are 224, 575, 1224, 2303, and 3968.

## 5. Two-seed scale spectrum and its exact sufficient conductor

The prior [six-block cap theorem](../../w-beta-caps/PROOF.md) supplies the
old W seed at scale `u+1`, and extends any constructed W scale T to `T+u`
when `T>=v-u=1`. Ordinary subdivision of the old and new seeds, followed by
these caps, therefore supplies every scale in

```
S = {p(u+1)+qu : p>=1, q>=0}
    union {p(u+2)+qu : p>=1, q>=0}.
```

For residue `r` modulo u, let w_r be the smallest element of S in that
residue. If u is even, the odd residues have `w_r=r(u+1)`, the nonzero
even residues have `w_r=(r/2)(u+2)`, and `w_0=(u/2)(u+2)`. If u is odd,
the same formulas hold at nonzero residues but `w_0=u(u+1)`: for an odd
residue the competing new-seed value has `p=(r+u)/2`, and exceeds the old
value by `u(u+2-r)/2>0`.

Each residue contains precisely `w_r+u*Z_{>=0}`. Consequently the largest
missing integer is `max_r w_r-u`. This proves the exact conductor of this
particular sufficient set:

```
C_S = 3                if u=2,
      u^2-u            if u>=4 is even,
      u^2+1            if u>=3 is odd.
```

For even u>=4, `max_r w_r=(u-1)(u+1)=u^2-1`; for odd u, the maximum
is `w_0=u(u+1)`. Thus every scale at least C_S is constructed. In the even
case this improves the previous cap threshold `u^2+1` by `u+1` scales.
These conductor values concern S only; an omitted scale is not declared
geometrically impossible.

The same sufficient set and tail apply to the fixed-tile beta-isosceles
family. Section 5 of the cited cap theorem extends W at scale T to beta at
the same scale by adding an ordinary tile triangle of integer scale vT.
Its sides are `T*(v^3,v^3,u(3v^2-u^2))`, and its tile count is
`(3v^2-u^2)T^2`. In particular the new seed also supplies
`N_beta=t^2*(2t^2-2t-1)` for every t>=4, with the same primitive tile.

## 6. Independent checks

The dissection was derived by a one-tile exchange visible in the u=3 exact
certificate. Its proof above is parameterized; no inference from a finite
sample is used.

The independent implementation is
[`adjacent_formula.py`](../group1/adjacent_formula.py). Full metric, area,
containment, and pairwise geometric checks pass for u=2,3,4,5. More strongly,
[`check_adjacent_symbolic.py`](../group1/check_adjacent_symbolic.py) verifies
the full W boundary identity for 19 positive convex macro regions as a
polynomial identity in u. Its sign checks use positive coefficients in
`t=u-2`; the outside-grid metric identities and total tile count are checked
symbolically as well. The report is
[`adjacent_symbolic_verified.json`](../group1/adjacent_symbolic_verified.json).
This supplies a uniform exact verification, rather than a sample-based claim.
The independent mathematical audit is
[`INDEPENDENT_MATH_AUDIT.md`](INDEPENDENT_MATH_AUDIT.md).

# Uniform horizontal-strip completion for every adjacent seed residue

**Theorem.** For every `u>=2`, with `v=u+1`, the primitive tile
`(uv,2u+1,v^2)` tiles its W target at every integer scale `M>=v`.
The target sides are `M*(v^3,u(2v^2-u^2),v(2u+1))`, and the count is
`(2v^2-u^2)M^2`. The same tile realizes the beta target
`M*(v^3,v^3,u(3v^2-u^2))`, with count `(3v^2-u^2)M^2`, at every such scale.
This is a complete positive tail; scales below v are not excluded here.

Let `u>=3`, `v=u+1`, `b=2u+1=u+v`, `2<=t<=u-1`, and `m=v+t`.
The tile types in the established oblique coordinates are

```
A: (0,0),(u,0),(0,v),
B: (0,0),(v,0),(0,u).
```

Both are congruent physical `(uv,b,v^2)` triangles. Half-turns are allowed.
Every region below is an ordinary triangular grid, a triangular grid with
a smaller corner grid removed, or an axis-parallel rectangle tiled by A/B
rectangular grids. There is no search oracle in this construction.

The four outside macros supplied by `group1/adjacent_t_search.py` leave

```
X=(0,0), A=(-uvm,u^2m), C=(-uvm,v^2m), V=(-u^2m,uvm),
U=(-u^2m+t*v^2,uv^2), R=(-u^2v+b(t-1),uv^2),
S=(ub-u^2t,uvt), Q=(ub,0).
```

The remainder is cut by horizontal lines `y=uvt` and `y=uv^2` into a lower
trapezoid, a central strip, and an upper pentagon. Indeed
`u^2m-uv^2=u(ut-v)>0` for the stated parameters. Thus the first two regions
have the lower boundary `ux+vy=0` throughout. The upper strip boundary is
`ux+vy=ub(u+t)`.

## A reusable complete strip cell

Consider the parallelogram with bottom-left `(x,y)`, horizontal width W,
vertical height uv, and horizontal displacement `-v^2` from bottom to top.
For any nonnegative integers p,q with

```
W-v^2=p*u+q*v,
```

it is tiled by:

1. The left B-grid triangle of scale v with vertices
   `(x,y),(x-v^2,y+uv),(x,y+uv)`.
2. The rectangle `[x,x+W-v^2] x [y,y+uv]`. Partition its width into p
   columns of width u and q columns of width v. Width-u columns have u
   A-grid rows; width-v columns have v B-grid rows.
3. The right B-grid triangle of scale v with vertices
   `(x+W-v^2,y),(x+W,y),(x+W-v^2,y+uv)`.

These are visibly disjoint and cover the parallelogram. Each rectangular
column has integer grid dimensions.

## Lower trapezoid

For `j=0,...,t-1`, let

```
L_j=(-v^2*j,uv*j), Q_j=(ub-u^2*j,uv*j).
```

The layer between `y=uvj` and `y=uv(j+1)` consists of:

* Left B-grid triangle of scale v:
  `L_j, L_j+(-v^2,uv), L_j+(0,uv)`.
* Right A-grid triangle of scale u:
  `Q_j, Q_j+(-u^2,0), Q_j+(-u^2,uv)`.
* The intervening rectangle
  `[L_j.x,Q_j.x-u^2] x [uvj,uv(j+1)]`.

Its width is `uv+bj=ju+(u+j)v`, so use j width-u A columns and u+j
width-v B columns. This works independently in every layer. The complete
lower count is

```
sum_(j=0)^(t-1) (v^2+u^2+2uj+2v(u+j)) = b*t*(2u+t).
```

## Central strip

For `j=t,...,v-1`, use the reusable cell with

```
x=-v^2*j, y=uv*j, W=b(u+t), p=t-1, q=u+t-1.
```

The width identity is

```
b(u+t)-v^2=(t-1)u+(u+t-1)v.
```

There are v-t complete cells. Their count is `2b(u+t)(v-t)`.

## Upper pentagon

All coordinates in this section are relative to `V=(-u^2m,uvm)`.
The pentagon has vertices

```
L=(u^2t-vb,-uvt), A=(-um,-um), C=(-um,vm), (0,0), U=(tv^2,-uvt).
```

First tile its part above y=0 by the A-grid triangle of scale m with
vertices `(-um,0),(-um,vm),(0,0)`.

The first negative layer, `-uv<=y<=0`, is the disjoint union of the A-grid
rectangle `[-um,0] x [-uv,0]` and the B-grid triangle of scale v with
vertices `(0,0),(0,-uv),(v^2,-uv)`. The rectangle contains 2um unit tiles.

For every `j=1,...,t-1`, use the reusable cell with

```
x=(j+1)*v^2-bm, y=-(j+1)*uv, W=bm, p=t, q=u+t.
```

Here `bm-v^2=tu+(u+t)v`. All of these are complete cells except j=1:
from its left B-grid triangle remove the corner B-grid triangle of scale t
at the upper-left apex. The big triangle has scale v, and t<v, so its
remainder is a positive ordinary grid annulus containing `v^2-t^2` tiles.

For clarity, that upper-left apex and the removed triangle are

```
F=(v^2-bm,-uv),
F, F+(vt,0), F+(vt,-ut).
```

The last two vertices equal `(-um,-uv)` and `A=(-um,-um)` respectively.
This follows from `v^2-bm+vt=-um` and `uv+ut=um`.
Thus the removal produces exactly the pentagon's left vertical edge down
to A, followed by its sloping edge down to L. No strip or cap overlap is
being ignored: the corner removed here is outside the target pentagon.

The comparison `uv<um<2uv` follows from `0<t<v`. Therefore the left kink
A lies strictly in this second layer, and all later layers are complete
parallelograms. The bottom corner of the last layer is
`tv^2-bm=u^2t-vb`, exactly L.x. The right boundary likewise ends at U.

The upper count is

```
m^2+2um+v^2+(t-1)*2bm-t^2 = 2bmt.
```

## Consequence

The entire remainder is tiled, with total

```
b*t*(2u+t)+2b(u+t)(v-t)+2bmt
  = b*(2uv+4vt+t^2)
```

unit tiles. Together with the four outer macros, this proves every seed
scale `m=v+t` with `2<=t<=u-1`. The previously proved scales v and v+1,
plus these seeds, give every residue modulo u in the interval `[v,v+u-1]`.
The existing `T -> T+u` cap therefore supplies every integer scale `T>=v`
for adjacent parameters `v=u+1`. The old W-to-beta grid bridge supplies
the same sufficient scale tail for the beta target.

The old scale-v seed and both extension steps are proved in the prior
[six-block cap theorem](../../w-beta-caps/PROOF.md). The scale-v+1 seed is
proved in the [one-corner exchange construction](../../universal-closure-oct8/group1-adjacent/PROOF.md).

No impossibility is asserted for scales below v. In particular this theorem
does not claim a necessary scale threshold or a full solution of Erdős634.

## Independent exact checks

The independent implementation is
[`all_adjacent_formula.py`](../group1/all_adjacent_formula.py).
The uniform symbolic verifier
[`check_all_adjacent_symbolic.py`](../group1/check_all_adjacent_symbolic.py)
works over the integer polynomial ring in p,q with

```
u=p+q+3, t=q+2, p>=0, q>=0.
```

This parametrizes the entire domain `u>=3,2<=t<=u-1`. It verifies the full
W boundary identity and positive convexity for its 13 macro regions,
the metric and annulus identities for the outside macros, the generic cell
and lower-layer constructions, and the total count. Thus its PASS is a
symbolic all-parameter result, not an inference from examples.

The separate local generator [`residual_formula.py`](residual_formula.py)
and its [`check_residual_formula.py`](check_residual_formula.py) checker
provide an additional implementation and exact unit/current examples.

# A balanced 16-tile nonoverlapping cylinder packing

21 November 2026. **Neither target is closed.**

An exact search in the neighboring `integer3431` directory found a balanced
16-tile periodic endpoint kernel for `(a,b,c)=(35,13,43)`. The explicit lift
below shows that this kernel also has a finite realization by whole triangles
with pairwise disjoint interiors and exact cylinder endpoint equations. Thus
the proposed restriction

> Every balanced nonoverlapping cylinder kernel of population below `2c`
> has population divisible by six

is false. The examples of sizes six and sixteen do not, by themselves, exclude
any whole-board tiling or establish existence of one.

## Coordinates and the checked equations

Use the oblique lattice basis with unit directions

```
U = ((1,0), (0,1), (-1,1), (-1,0), (0,-1), (1,-1)).
```

A tile with label `(x,y,j,s)`, where `s=+/-1`, has vertices

\[
q=(x,y),\qquad u=q-35U_j,\qquad w=q+13U_{j+s}.
\]

Its signed charge is `epsilon=s*(-1)^j`. The endpoint column has the four
contributions

\[
s(j,q),\quad -s(j,u),\quad s(j+s,w),\quad -s(j+s,q).
\]

Cylinder rows retain the actual transverse coordinate and reduce only the
coordinate along the supporting line modulo 43:

| Axis | Row at `(x,y)` |
|---|---|
| 0 | `(0,y,x mod 43)` |
| 1 | `(1,x,y mod 43)` |
| 2 | `(2,x+y,y mod 43)` |

All 32 rows used by the construction have zero signed endpoint total.

## Construction

The original periodic support is included verbatim in the
[independent verifier](verify_balanced_16_lift.py). Index its tiles from zero.
Partition the sixteen indices into seven groups:

```
(0,1,2), (3,5), (4,8), (6,12), (9,11), (10,13), (7,14,15).
```

Translate group `k` by `(172k,0)`. The resulting labels are:

| Index | x | y | j | s |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 1 | -1 |
| 1 | 0 | 0 | 1 | 1 |
| 2 | 0 | 0 | 3 | -1 |
| 3 | 198 | 0 | 2 | 1 |
| 4 | 379 | 0 | 2 | 1 |
| 5 | 190 | 8 | 5 | 1 |
| 6 | 547 | 8 | 5 | 1 |
| 7 | 1037 | 8 | 5 | 1 |
| 8 | 371 | 8 | 5 | 1 |
| 9 | 702 | 8 | 5 | 1 |
| 10 | 861 | 8 | 5 | 1 |
| 11 | 710 | 0 | 2 | 1 |
| 12 | 555 | 0 | 2 | 1 |
| 13 | 869 | 0 | 2 | 1 |
| 14 | 1037 | 8 | 5 | -1 |
| 15 | 1037 | 8 | 3 | 1 |

The two groups of three are fans of three triangles around a common vertex.
Each middle group has one triangle below `y=0` and another above `y=8`.
The seven groups have disjoint horizontal ranges. These observations explain
the nonoverlap; the verifier separately checks every one of the 120 pairs by
the exact separating-axis criterion. Projection onto a normal to an edge is
computed by an integer determinant, so no floating-point geometry is used.
Using the oblique lattice basis is harmless: invertible linear coordinate
changes preserve intersections, interiors, and separation by a line.

The output [certificate](BALANCED_16_NONOVERLAP.json) contains the full
vertices and an explicit separating direction and projection ranges for each
triangle pair. It also checks that there are eight tiles of each sign.

## Strict containment in the 5063 board

A compact version fits strictly inside the target board, including when all
sixteen triangles are assigned the odd short height one. Starting again from
the original periodic support, translate group `k` by `(129k,0)` and then
translate every normalized anchor by `(40,40)`. Multiply every vertex by

\[
z=(35+13\rho)/43.
\]

This realizes the labels at height one in the standard frame. In physical
axial coordinates, a normalized vertex `(x,y)` becomes

\[
(X,Y)=\left(\frac{35x-13y}{43},
                \frac{13x+48y}{43}\right).
\]

The standard board has vertices `(0,0)`, `(1079,0)`, `(0,2135)`; its area
ratio to the tile is `(35+2*13)(2*35+13)=5063`. For all 48 triangle vertices,
the verifier checks the three strict inequalities

\[
43X>0,\qquad43Y>0,\qquad
43\cdot1079\cdot2135-43\cdot2135X-43\cdot1079Y>0.
\]

Their respective minimum integer margins are `256`, `760`, and `22109611`.
Convexity therefore places every complete triangle strictly inside the
board. The cylinder rows are rechecked after the normalized translation,
and all 120 pairs again have integer separating-axis certificates. Rotation
by `z`, whose norm is one, preserves their disjoint interiors. Full physical
vertex numerators and these checks are included in the certificate.

## Scope and the remaining possible restriction

This is a real nonoverlapping partial packing satisfying the cylinder
equations, with a compact version strictly contained in the prescribed outer
triangle. It does not impose the full long-edge currents, either complete
joint-gate profile, or filling of its complement. Cylinder equations permit
long edges whose missing
neighbors are not supplied by the packing. A theorem using those omitted
conditions is therefore not contradicted.

In this example the three signed `a`-axis inventories and the three signed
`b`-axis inventories are both zero. Consequently it does not decide the weaker
proposal that every balanced kernel of population below `2c` has zero signed
axis inventories. That proposal requires a separate proof or counterexample.

Reproduce the certificate from the repository root:

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/global/verify_balanced_16_lift.py
```

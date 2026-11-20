# A charged terminal polygon with c-squared tiles in its terminal node

20 November 2026. This is an exact local counterexample and a limit on
a proposed proof route. It is not a complete tiling of either F2
target, nor a counterexample to any theorem restricted to complete
F2 tilings.

For both target tiles there is a positively tiled polygon containing
a terminal exterior-free phase node of population `c^2` and signed
population `-c`. The entire polygon can also be placed inside the
corresponding F2 triangle. In that placement its `c^2` tiles belong
to a node which is exterior-free relative to the F2 outer edges.
An unknown completion may add tiles in that node or its descendants;
terminality is not asserted for such a completion.

## 1. Exact polygon and its tiling

Use axial coordinates `x+y*rho`, and put

\[
 W=(a^2,ab),\qquad B=(c^2,0),\qquad z=(a+b\rho)/c.
\]

The triangle `U=(0,B,W)` has side lengths `ac,bc,c^2` and is a
scale-`c` copy of the tile, at short height 1 and long height 0.
Subdivide it by its standard triangular grid into `c^2` unit tiles.
All these tiles have short height 1 and lie in the same translate
`zR`. There are `c(c+1)/2` downward copies of sign `-1` and
`c(c-1)/2` half-turn copies of sign `+1`. Hence

\[
 n_U=c^2,\qquad G_U=-c.                                  \tag{1}
\]

For `0<=i<a`, attach the height-zero tile

\[
 L_i=\operatorname{conv}\{i(a,b),(i+1)(a,b),i(a,b)+(0,b)\}.
\]

Its long edge is the `i`-th length-`c` interval on `0W`; its short
edges have vectors of lengths `a,b` on the axial directions.
For `0<=i<b`, put `p_i=W+i(a+b,-a)` and attach

\[
 R_i=\operatorname{conv}\{p_i,p_{i+1},p_i+(b,0)\}.
\]

Its long edge is the `i`-th length-`c` interval on `WB`. All displayed
triangles are positively oriented and congruent to the unit tile.

The left teeth lie outside `U` across the line `0W`. Different left
teeth have disjoint open axial `x`-intervals `[ia,(i+1)a]`.
The right teeth lie outside `U` across `WB`; their corresponding
intervals are `[a^2+i(a+b),a^2+(i+1)(a+b)]`. Thus different right
teeth have disjoint interiors as well. Every left tooth has `x<=a^2`,
and every right tooth has `x>=a^2`; the two rows meet only at `W`.
This proves disjointness without a numerical tolerance.

Let `P` be their union with `U`. It is a connected polygon tiled by

\[
 |P|=c^2+a+b
\]

unit tiles. The two height-one sides of `U` are completely covered
by the parent teeth. All remaining outer edges of `P` have height
zero: they are the long-height-zero base of `U` and short edges of
the parent teeth. Consequently the height-one node containing `U`
is exterior-free for this polygon. There are no tiles of height
greater than 1, so that node is terminal. Equation (1) shows that
terminality and exterior-freeness do not force zero signed population
for general positively tiled polygons, even with the target tile
shapes.

## 2. Placement inside the F2 triangle

Let the F2 target have vertices

\[
 0,\quad A=b(2a+b),\quad C=a(a+2b)\rho,
\]

and abbreviate `H=a(a+2b)`. Apply the rigid motion

\[
 F(x,y)=(y,c^2-x-y),
 \quad\text{equivalently}\quad
 F(P)=\rho(c^2-P).
\]

Its linear part is rotation by 240 degrees. It preserves physical
heights and the sign `epsilon`, because its direction shift is even.

The convex hull of `P` is contained in the hull of the six points

\[
 (0,0),\ (0,b),\ (a^2-a,ab),\ (a^2+b,ab),\ (c^2-a,a),\ (c^2,0).
\tag{2}
\]

Containment of `F(P)` in the F2 triangle is checked on these points.
In its axial coordinates the target inequalities are

\[
 X\ge0,\quad Y\ge0,\quad HX+AY\le AH.
\]

After applying `F`, these become

\[
 y\ge0,\quad x+y\le c^2,\quad
 -Ax+(H-A)y\le A(H-c^2).
\tag{3}
\]

All six points satisfy the first two inequalities. For the third,
`H-A=(a-b)(a+b)` and `H-c^2=b(a-b)`. Its only potentially largest
positive value among (2) occurs at `(0,b)` and satisfies

\[
 (a-b)(a+b)b\le b^2(2a+b)(a-b),
\]

because `a+b<=b(2a+b)`. At `(a^2-a,ab)` the left side equals
`ab((2a+b)-c^2)`, which is nonpositive for the two target tiles;
at `(a^2+b,ab)` it is smaller. At `(c^2-a,a)` it equals
`aH-Ac^2`, which is -648376 and -1920346 for the two target tiles,
respectively, and is therefore negative. The other points are
immediate. Thus the entire patch fits in the target.

| Tile | Terminal portion | Parent teeth | Total placed tiles | Target tile count |
|---|---:|---:|---:|---:|
| `(33,7,37)` | 1369 | 40 | **1409** | 3431 |
| `(35,13,43)` | 1849 | 48 | **1897** | 5063 |

The transformed height-one portion has phase node `zA_pi`: its
original vertices lie in `zR`, and the translation `c^2 rho` also
belongs to `zA_pi`. In the increasing-height prime tree its subtree
cannot contain an outer height-zero node. The outer height-two node
has ancestor `b(2a+b)+zA_pi`, distinct from `zA_pi`, since
`b(2a+b)` is a unit at the chosen prime. This checks
exterior-freeness relative to the full F2 boundary as well.

## 3. What the example does and does not show

The polygon `P` is completely tiled and has an actual charged
terminal exterior-free node. This refutes a terminal-zero-character
theorem whose hypotheses mention only a tiled polygon and its phase
tree. Containment in the F2 target does not by itself eliminate this
local configuration.

The displayed F2 placement is a partial packing. Neither its
completability nor terminality of the same node in a completion is
claimed. Thus this is not a counterexample to a target-specific
terminal theorem using the entire complement of the patch.

It supplies a local example at `n=c^2, |G|=c`, compatible with the
conjectural inequality `n>=c*|G|`. It neither proves that inequality
nor proves it sharp among nodes of complete F2 tilings. In particular
the possibility of a charged terminal node of population `3c` remains
unresolved for the two targets.

The file `charged_patch_certificate.json` records the exact native
macro triangles: one standard `c`-grid and the parent unit triangles.
Run `python3 verify_charged_patch.py`. The checker verifies the side
norms, all macro-piece interior-disjointness tests, exact area and sign
counts, rigid motion, F2 containment, and the exterior-node residue,
and compares the recorded certificate with these exact pieces.

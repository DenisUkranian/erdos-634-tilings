# No missing short-edge heights for the remaining N=135 equilateral instance

8 October 2026. Exact necessary geometry, not a decision of N=135.
Tile sides are(3,5,7); the target is equilateral of side45.
Write rho=exp(i*pi/3), z=(3+5rho)/7. The short-edge height of a tile is h
when its short sides have directions rho^j z^h.

## 1. Population and connectivity bounds

The established height divisibility gives n0=135=2(mod7) and nh=0(mod7)
for h!=0. The [seven-population exclusion](../e60-structure/STRUCTURE.md)
is local to a nonzero height, and applies unchanged: every occupied nonzero
height contains at least14tiles.

Every external side has length45, not divisible by7, hence supports at least
one short tile edge. One tile cannot have both short edges on the external
boundary: their common120-degree vertex would have to be a60-degree target
corner. Therefore at least three distinct height-zero tiles occur, and the
population congruence strengthens this to **n0>=9**.

Consequently at most ten heights are occupied. Across a positive-length tile
contact the two short-edge heights differ by at most two: their respective
edge-direction sets are contained in {h-1,h,h+1}. The positive-contact graph
of a finite tiling of a triangle is connected, by a generic path avoiding all
vertices. Thus any empty heights between occupied ones are isolated; two
consecutive empty heights would separate that contact graph.

## 2. A gap can only isolate98tiles with zero boundary character

Suppose positive height k is empty and some larger height occurs. Let H be the
union of all tiles with short height greater than k. Its boundary consists
of whole length7edges at height k. Here the word *whole* can be justified
geometrically, not merely by a formal chain identity: since height k is empty,
every edge on a line of that direction is a long edge. Both sides of each
maximal straight seam have equal-length whole-edge partitions with common
endpoints; they therefore match edge for edge. A boundary between the two
height groups consists of whole matched7edges. The same statement follows
from the established whole-edge median-cut argument.

The lattice shoelace argument gives49 dividing the number of tiles of H.
Since the whole target contains135tiles, its size is49 or98. The earlier
[49-tail argument](../e60-structure/STRUCTURE.md), Section4, rules out49
without using the size of the enclosing target.

For98tiles the same integer Laurent identity is

    (-2-7X)U(X)+(-2-7/X)V(X)=7M,

with only strictly positive exponents in U,V after rotating by z^-k, and
|M|<=98. Evaluation at X=19(mod45) gives45|M. Evaluation at X=1 and tile-count
parity show M even. Hence M is0 or±90. The constant coefficient and X=1
identity imply

    ||U||1+||V||1 >= 11|M|/9.

The values±90 would require at least110tiles. Consequently **M=0**.

Any second positive gap would have another98-tile tail strictly contained
in H, impossible because at least one occupied height lies between two
isolated gaps. A negative gap would produce a disjoint98-tile tail, also
impossible. Thus there is at most one gap in the entire occupied support.
The other side of that gap contains37tiles, including the central height.
Since9+3*14>37, its consecutive central block has at most three occupied
heights. Accordingly, after reflection, the only possible positive gap
heights are **k=1,2,3**.

## 3. The98-tile tail is one hole-free lattice polygon

Consider components with connected interior, so that touching at a single
vertex does not identify two components. Each component has a boundary of
whole7edges at height k. The lattice area argument separately makes its
positive tile count a multiple of49. A49-tile component is impossible by
the same Laurent proof as above. Hence the98-tile tail has one component.

It has no holes. Every bounded complementary component is filled with whole
tiles of the original tiling. Its closed boundary consists of whole7edges,
so its area is an integer multiple of49*sqrt(3)/4. Comparing with tile area
15*sqrt(3)/4 makes its tile count divisible by49. But there are only37tiles
outside H in total.

All vertices of the connected outer boundary consequently lie in one affine
copy of7z^k Z[rho]. Dividing by7 and rotating by z^-k represents H as a union
of elementary up- and down-pointing unit lattice triangles. Its area is

    98*15/49 =30

such unit triangles. The character M is three times the difference between
their up and down counts, since their respective oriented characters are+3
and-3. As M=0, H must contain **15 up triangles and15 down triangles**.

## 4. Exact containment bound for every lattice translation

The target, after this normalization, is the equilateral triangle

    Pk = (45/7) z^(-k) conv(0,1,rho).

The affine lattice translation can be restricted to t in[0,1]^2 in the
basis(1,rho). An elementary cell q+t is contained in Pk precisely when
three exact linear inequalities in t hold, one for each target side.
Intersecting these inequalities with the fundamental square gives a convex
polygon of permitted translations for that cell.

`cell_bound.py` enumerates all possible unit cells using an enclosing integer
coordinate rectangle. It discards a cell only if its permitted-translation
polygon is empty. It then constructs the arrangement of all polygon-support
lines and the four sides of the fundamental square. Every possible simultaneous
cell-containment set is attained at an arrangement vertex: the intersection
of the relevant closed convex polygons is nonempty and bounded, hence has
an extreme point on these lines. Therefore counting cells at every such
vertex gives a rigorous maximum over **all real translations**, including
translations on arrangement boundaries.

All calculations use integer line coefficients and rational intersection
points. No rasterization, floating tolerance, random sampling, or prescribed
tilings are involved.

| k | Potential elementary cells | Arrangement vertices | Maximum up count | Maximum down count |
|---:|---:|---:|---:|---:|
|1|47|100|12|14|
|2|45|161|12|14|
|3|46|165|16|13|

Thus k=1,2 cannot contain15 up cells, and k=3 cannot contain15 down cells.
All three possibilities for the98-tile tail are impossible. Reflections
exclude the negative gaps. **The occupied short-edge heights are consecutive.**

The population bounds above give at most ten heights. A separate signed-charge
argument in `../e135-inventory/` sharpens ten to nine. These restrictions do
not assert that all the remaining finite direction-band problems have been
solved, and do not decide135.

## Reproduction and evidence scope

```sh
python3 research/final-closure-oct8/e135-structure/cell_bound.py
```

This standard-library computation regenerates `cell_bound_checked.json` in
well under a second in the recorded environment. The complete proof combines
the geometric reductions above with this finite, exact containment calculation;
the final containment table alone is not a proof for arbitrary tilings.

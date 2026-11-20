# A row obstruction that survives mixing tile directions

Use the coordinates of [the staircase construction](BOUNDARY_WITNESSES.md),
with axes along $CO,CB$ and mesh length $c$. Write $U=ap/c$, $V=bq/c$.
Let $S$ be a nonempty region bounded by tile edges in the unit F2 board,
formed by whole unit rhombi on *one translated grid* using these two axes.
Assume $V<a$, which holds in particular when $a\ge2b$. The results allow
arbitrary tile orientations, including reflected tiles and T-junctions.

**Theorem.** The tiles in $S$ cannot all be paired into parallelograms
along a shared full $b$- or $c$-edge. This includes pairings that use
different directions or choose either shared length from pair to pair.
In particular $S$ cannot be tiled entirely by triangles with their short
edges at the board-side height 2. The result covers the odd mixed
semiprime parameters beyond the unit staircase: the [parameter bounds](../paths/TWO_PATHS.md)
give $u/v\ge6$, hence $a/b=(u^2-v^2)/(v(2u+v))\ge35/13>2$.

## A periodic boundary test

For this argument measure physical lengths in tile units, so one
coarse grid edge has length $c$. In the chosen axial frame all unit
tile directions have the form $\rho^j z^h$, since the frame itself
has a tile direction. Both $z$ and its inverse have axial coordinates
with denominator dividing $c$. For any given finite tiling, take a
large enough power $L$ of $c$ that **every unit tile direction** has
coordinates in $L^{-1}\mathbb Z^2$. Opposite edges of a parallelogram
with an $a$-side are separated either by an $a$-vector belonging to
$(a/L)\mathbb Z^2$, or by the other side. Translations and the locations
of all the tile vertices remain arbitrary.

Retain just edges parallel to the horizontal coarse axis, with their CCW
orientation, then identify coordinates modulo $(a/L)\mathbb Z^2$.
Take the signed endpoints of the resulting horizontal intervals (end
minus start). Every parallelogram with an $a$-side contributes zero.
If its horizontal sides have length $a$, their individual endpoints
coincide modulo the periods. Otherwise its two horizontal sides are
opposite translates by an $a$-vector, so their endpoint measures
cancel. A parallelogram with no horizontal side contributes nothing.
Internal currents cancel on the original tiling after splitting partial
contacts, hence their endpoint measures cancel as well. The same argument
works for either coarse axis. This extends the line-periodization idea
used in [the earlier height-1 argument](../paths/TWO_PATHS.md) to a
finite set of simultaneous rational directions.

Horizontal coarse boundary lines have physical heights $y_0+cj$. Two
of them agree on the torus exactly when their indices are congruent
modulo $a$, since $\gcd(cL,a)=1$. Their span in coarse row units is
at most $V<a$, so no distinct such lines coincide. On one coarse line
write $E_i$ for the signed horizontal boundary indicator on unit interval
$i$. Its endpoints give differences $E_{i-1}-E_i$. Vanishing of the
periodic endpoint measure says
$$
 \sum_{i\equiv t\ (a)} E_i=\sum_{i\equiv t-1\ (a)} E_i
 \quad\text{for every residue }t.
$$
For a union of rhombi, $E_i$ is the difference of the two occupancy
indicators immediately above and below the line. Starting with the
empty row below the polygon and proceeding upward shows that in *every*
row the count of occupied cells is the same in every column residue.
In particular each nonempty row contains a multiple of $a$ cells.

The maximal horizontal width $U$ is less than $2a$ because $p<2c$.
Therefore each nonempty row has exactly $a$ cells. By the single-height
boundary area bound [recalled here](CYCLES.md), a tiled $S$ contains
exactly $ab$ rhombi, so $b$ nonempty rows are needed. The same bound
holds for a region with holes or multiple components by summing its
closed boundary walks. Yet the $a$ cells of a row must fit at its top
edge, requiring $U(1-y/V)\ge a$. All those rows lie in the strip
$$ 0\le y\le V(1-a/U)<b. $$
The strict inequality is equivalent to $N<3c(a+b)$, since $p+q=3(a+b)$.
Indeed $N=2(a+b)^2+ab\le9(a+b)^2/4$ and
$c\ge\sqrt3(a+b)/2$. The strip cannot contain $b$ distinct rows of
height one. On the two controls it can hold at most 2 and 7 such rows,
respectively, whereas 7 and 13 are required. This contradicts the
putative complete pairing.

If all triangles have short height 2, every long edge is interior and
is at height 1 or 3. Along each maximal straight run of such edges both
banks partition the same interval into complete edges of length $c$.
There are no exterior edges of these directions. Edges therefore match
one to one. For fixed short height and fixed long-edge direction only
one hand occurs; the two opposite bank triangles are half-turn mates.
(Reflection in the common edge would change the short height.) The
matching gives a complete pairing along $c$, already excluded.

## A certificate of the number of triangles left outside any pairing

For each of the two board-side axes form the signed endpoint counts of
the complete boundary on the torus, as above, and sum their total
variations. Every allowed pair contributes zero. The endpoints of an
$a$-edge of a remaining tile also cancel. Its $b$- and $c$-edges belong
to different heights, so at most one is parallel to either of the two
selected axes. It contributes at most two in total variation. Therefore
half the summed variation is a lower bound on the number of triangles
outside any such pairing, even when all remaining orientations are free.
For a coarse boundary vertex $(i,j)$ the equivalence classes are exactly
$(i,j)\bmod a$, up to translation and the invertible factor $cL$. The
bound can be checked without knowing $L$ or any tile positions.

For the two explicit [area-correct outlines](BOUNDARY_WITNESSES.md) the
horizontal and vertical variations are $(12,12)$ and $(6,6)$.
Any tiling of these particular regions would leave at least **12** and
**6** triangles, respectively, outside every pairing into parallelograms
along $b$ or $c$. The [integer verifier](check_staircases.py) computes
the variations from the boundary vertices. The argument allows tiles
paired along $a$ to be counted among the unmatched triangles and does
not decide whether the two regions or the complete boards can be tiled.

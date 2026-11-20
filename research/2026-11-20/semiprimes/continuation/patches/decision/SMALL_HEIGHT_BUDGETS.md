# Exact height budgets for the small notch and pentagon tests

Use the uniform line-count lemma and scalar characters in the previous
full-board note. The boundary of every board here has edge heights
0 and 1. Off these heights each population is a multiple of $c$ and
is either zero or at least $2c$, since the exterior current on its lines
vanishes. At a vacant height strictly outside the exterior pair, the
far union has its boundary represented by full $c$ edges from only one
height, so a nonempty far group has at least $2c^2$ tiles. This applies
also to convex polygonal boards. In the examples $N<2c^2$, so the
support cannot skip heights outside 0,1.

At the intermediate cut the chain of exposed low edges is a two-segment
arc. Close this arc by its chord in the lattice
$M_0=cR+(a+b\rho)R$ of index $c$. More precisely its chord displacement
for a notch is $tc z-kc$, in $M_0$. For the pentagon use the two edge
vectors $(0,c+tb),(ta-kc,0)$, whose sum is $tc z-kc+c\rho$, also in
$M_0$. Comparing the low union to the arc triangle gives a closed
whole-edge chain in $M_0$, hence their doubled axial areas agree modulo
$c$ (with the arc oriented as part of the counterclockwise boundary).
Both polygons have the interior on the triangular side of this arc,
so its oriented area has positive sign. The arc triangles have doubled
area $(ta-kc)tb$ and $(ta-kc)(c+tb)$, respectively. Thus the low
population is $t^2\pmod c$, after division by the invertible tile
area factor $ab$. Subtracting the off-level totals gives
$n_0\equiv t^2$ and $n_1\equiv N-t^2\pmod c$.

For the 117 notch $n_0\ge35$ and $n_1\ge39$. This leaves at most 43
tiles elsewhere, so all short heights are 0,1. For the 168 pentagon
the residues are 21,36 with room for 111 further tiles. For 180 they
are 35,16 with room for 129. In both pentagons at most one height
outside 0,1 can occur and, by contiguity, it is -1 or 2.

There is a further parity test for the pentagons. In the physical
orientation $X'\to Y\to W\to D\to D'$, the circuit is clockwise.
Its counterclockwise scalar current polynomial is
$$
 B(X)=(k+1)c-t(a-b)+[tc-(k+1)(a-b)]X .
$$
Indeed the five clockwise directions are $\rho,1,\bar\rho z,-\rho z,-z$
with lengths $c+tb,ta-kc,kb,a,tc-ka+b$. The standard two evaluations
therefore give signed population sums of $-t$ over even heights and
$-(k+1)$ over odd heights. Both are odd in the two controls.
If there are $2c$ tiles in an outside height, its signed population is
even, so $n_0,n_1$ must both be odd. The unique remaining budgets are
$(n_0,n_1,n_{\rm out})=(21,73,74)$ for 168 and $(35,59,86)$ for 180.
If instead there are $3c$ outside, the budget has $n_0$ odd and $n_1$
even, so the outside height must be odd, namely -1. Its budgets are
$(21,36,111)$ and $(35,16,129)$.

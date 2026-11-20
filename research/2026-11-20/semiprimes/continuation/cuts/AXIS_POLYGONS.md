# Convex partitions of the two smallest equilateral targets

Let a primitive tile have positive integer sides $a,b,c$, with angle
$120^\circ$ opposite $c$. Put $L=ab$. Write $E_s$ for the equilateral
triangle with axial coordinates $(0,0),(s,0),(0,s)$ in the basis
$1,\rho=e^{i\pi/3}$. A partition here has finitely many convex
polygons of positive area, each tileable by the given tile. Every
polygon side must be parallel to a side of the outer equilateral
triangle. Inside each polygon the tiles may have any orientations
and T-junctions. A proper partition has at least two polygons.

**Theorem.** $E_L$ admits no proper partition of this kind. A proper
partition of $E_{2L}$ exists if and only if $E_L$ tiles.
Every such proper partition of $E_{2L}$ contains an entire polygon
congruent to $E_L$. No global straight cut or symmetry of the
partition is assumed.

One may even let each polygon choose its own three directions, provided
they differ by multiples of 60 degrees. Two polygons sharing a
positive-length segment then have the same three unoriented directions.
Their positive-contact graph is connected: connect two polygon interior
points by a path in the target avoiding the finitely many vertices.
Since an exterior side supplies one of the directions, all polygons
use the outer axes. Thus the shared-axis condition can equivalently be
checked on each polygon separately.

### An integer for each convex polygon

Traverse a polygon counterclockwise, and let $s_j$ be its total side
length in direction $\rho^j$, for $j$ modulo six. Zero lengths are
permitted. Each length is an integer because a straight boundary of a
tiled convex polygon is a concatenation of whole tile edges. Closure
and $1-\rho+\rho^2=0$ give
$$
s_0-s_3=s_2-s_5=s_4-s_1=w.
$$
Thus the alternating sum of the six lengths is $3w$.
For an equilateral triangle in the displayed orientation, $w$ is its
side. The quantity $w$ is additive under partitions into polygons
with the given three directions because reversed internal edge
segments cancel, also at T-junctions.

For a tileable polygon of this kind, **$L$ divides $w$**.
Use the [two signed direction characters](../../../../general-spectra/PROOF.md),
with the horizontal direction as reference. On the six boundary
directions $\rho^j$ both characters take weight $(-1)^j$. Set
$X=c+a-b$, $Y=c+b-a$. For each tile the two normalized character
sums, obtained by dividing by $X$ and $Y$ in the reference convention,
are independently signs. For a polygon of $M$ tiles it follows that
$U=3w/X$ and $V=3w/Y$ are integers of parity $M$. Therefore
$$
\frac{U+V}{2}=\frac{cw}{ab}\in\mathbb Z,
$$
using $XY=3ab$ and $X+Y=2c$. Primitivity and the norm equation
$c^2=a^2+ab+b^2$ give $\gcd(c,ab)=1$; hence $w=abk$ with $k$
integral. This includes $w=0$ and negative $w$.

### Where an equilateral triangle fits

For $w>0$ the polygon is, up to translation, the Minkowski sum of
$E_w$ and three line segments of lengths
$\min(s_j,s_{j+3})$ in directions $\rho^j$, $j=0,1,2$. Here a
zero length means a point. For $w<0$ use $-E_{|w|}$ in place of
$E_w$; for $w=0$ use a point. Indeed the list of oriented boundary
vectors of a Minkowski sum of convex polygons is the angularly sorted
merge of their lists, with parallel vectors added. Adding a segment
inserts its two opposite vectors, as one sees by translating the
two supporting vertices or faces perpendicular to it. The indicated
sum therefore has exactly the original polygon's six directed side
lengths in cyclic order, determining the polygon up to translation.

Consequently each polygon of imbalance $Lk$ contains a translate of
a triangle of side $L|k|$, and has area at least $k^2$ times that of
$E_L$. If $k\ne0$ and the sum of the line segments is not a point,
it contains a continuum of distinct translates of that triangle.
Its area is then strictly larger than the triangle's, since
translating a full-dimensional triangle over a nontrivial interval
sweeps additional positive area.

For a partition of $E_{mL}$ this gives
$$
\sum_i k_i=m,\qquad \sum_i k_i^2\le m^2.
$$
When $m=1$ the only nonzero $k_i$ is $+1$. Its polygon already
fills the available area. No proper partition exists.

When $m=2$, a $+2$ already fills the available area and a $-2$ is
incompatible with the two sums. In a proper partition either the
nonzero entries are $+1,+1,+1,-1$, or they are $+1,+1$.
In the first case equality in area forces the four polygons to be
equilateral of side $L$, with no room for any others.

### The two positive polygons

It remains to handle $+1,+1$, possibly with other polygons of
imbalance zero. Each positive polygon contains a translate of the
upright triangle $E_L$. A translate $t+E_L$ lies in $E_{2L}$ exactly
when $t\in E_L$. For $t,u\in E_L$, these translates have disjoint
interiors exactly when
$$
\max(|t_x-u_x|,|t_y-u_y|,|(t_x+t_y)-(u_x+u_y)|)\ge L .
$$
To see this, a triangle $t+E_L$ imposes $x\ge t_x$, $y\ge t_y$,
$x+y\le L+t_x+t_y$. The interiors of two such triangles meet exactly
when
$\max(t_x,u_x)+\max(t_y,u_y)<L+\min(t_x+t_y,u_x+u_y)$.
After subtracting the minimum on the right, the left side becomes
the maximum of the three absolute differences above: this follows by
taking the four possible sums of a choice of $x$ and a choice of $y$,
and both choices of the subtracted total.

Each of $x,y,x+y$ ranges from zero to $L$ on the translation triangle
$E_L$. Equality in the displayed maximum thus requires one of the two
translations to be a vertex of $E_L$: the maxima of $x$ and $y$,
and the minimum of $x+y$, are each attained at a unique vertex.
If neither of the two positive polygons were itself an equilateral
triangle, both would contain a continuum of translated $E_L$'s.
In each choose a translation outside the three vertices. The two
chosen triangles then have intersecting interiors, a contradiction.
At least one entire positive polygon equals a translate of $E_L$.

Finally, if $E_L$ tiles, its three upright and one inverted copies
in the midpoint subdivision tile $E_{2L}$ in four convex pieces.
This proves the converse.

### Consequences for the original F2 boards

At $(33,7,37)$ an independent [fixed-tile certificate](../../../../2026-11-19/nov19/equilateral231/cert/README.md)
excludes $E_{231}$. Thus any filling of $E_{462}$ by 924 copies
would admit no proper convex partition using the three outside directions,
including partitions with no straight cut passing through the board.
At $(35,13,43)$ a proper partition of $E_{910}$ into such tileable
polygons is equivalent to a filling of $E_{455}$ by 455 tiles. Both
implications hold for every primitive 120-degree tile at the same scales.
An unrestricted filling of the larger equilateral triangle would suffice
for the corresponding original F2 board by attaching the three grids
in the [cut theorem](README.md). The argument leaves open a filling
of the larger triangle that admits no such partition, and an original
F2 tiling that avoids the equilateral triangle.

[Integer polygon and translation checks](check_axis_polygons.py) · [Rotational symmetry at these scales](EQUILATERAL_SYMMETRY.md).

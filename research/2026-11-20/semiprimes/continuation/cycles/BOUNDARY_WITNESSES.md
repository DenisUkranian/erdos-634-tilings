# A balanced boundary of precisely the required area exists on every odd unit F2 board

In *every* primitive odd F2 triangle there is a simple polygon, strictly
inside the board, made of exactly $ab$ unit grid rhombi of side $c$.
Its boundary has equal opposite-direction totals and it encloses the
area of precisely $2c^2$ tiles. The construction works in a mesh whose
axes follow the two board sides meeting at the $60^\circ$ vertex. An open
interval of rotations also works, so there are admissible geometric
outlines in infinitely many positive and negative orientation heights.
For the $5063$ board **every rotation and every translation** of the
triangular mesh allows an outline of the required area.

These are polygons with exact areas. To be a boundary in a tiling their
edges would have to be supported by actual tile sides and both regions
would have to tile. Thus the area, direction balance and freedom to turn
the grid cannot by themselves exclude all the mixed semiprime boards.

## Construction for every board

Use mesh units, with origin at $C$ and axes along $CO,CB$. The angle is
$60^\circ$. The board is $x,y\ge0$, $x/U+y/V\le1$, where
$$ U=ap/c,\qquad V=bq/c,\qquad U>V. $$
A unit coordinate square is a physical rhombus. It is contained if its
outer corner $(i,j)$ satisfies $i/U+j/V\le1$. The available rhombi
therefore form a left-aligned staircase with nonincreasing row lengths.
For $m=\lfloor V\rfloor$, the number is
$$
 M=\sum_{j=1}^{m}\lfloor U(1-j/V)\rfloor
   > UV/2-U/2-V.
$$
Indeed $m-m(m+1)/(2V)=(V-1)/2+\{V\}(1-\{V\})/(2V)$, and replacing a
real row length with its floor loses less than one. Also
$UV/2=ab+3a^2b^2/(2c^2)$. A sufficient condition for $M\ge ab$ is
$$ 3a^2b^2\ge c(a^2+6ab+2b^2). $$
For $b\ge9$, write $t=a/b>1$. It suffices that
$$
 b\ge\frac{\sqrt{t^2+t+1}(t^2+6t+2)}{3t^2}.
$$
The right-hand side is smaller than
$t/3+7/3+8/(3t)+2/(3t^2)\le t/3+17/3$.
Since $(2c-2a-b)(2c+2a+b)=3b^2$ and its first factor is a positive
integer, $a<3b^2/4$. Hence $t/3<b/4$ and $b\ge9$ suffices. For odd
$b<9$ the same bound on $a$ leaves just two primitive triples, $(5,3,7)$
and $(33,7,37)$, with $M=16,260$ and $ab=15,231$, respectively.

Take complete rows from the bottom and, if needed, a left-aligned part
of the next row, stopping at exactly $ab$ rhombi. This is a simple polygon
with at most $\lfloor V\rfloor-1\le2b-2$ reflex corners because $q<2c$.
Every rhombus contributes one cell of each orientation. Its boundary
balances opposite directions and these totals add after cancellation.
No lattice vertex lies on the sloping board side: the equality would be
$c(bq\,i+ap\,j)=abpq$, impossible since $\gcd(c,abpq)=1$ and $c>1$.
Here $p^2=4c^2-3a^2$, $q^2=4c^2-3b^2$ and $\gcd(c,3ab)=1$.
A small translation increasing both axial coordinates puts the polygon
strictly inside, so all rotations sufficiently near this one still fit.
The angle of $z=(a+b\rho)/c$ is an irrational multiple of $\pi$:
if $z$ were a root of unity, $z+z^{-1}=q/c$ would be an algebraic
integer, whereas it is rational and strictly between 1 and 2. Thus the
positive and the negative powers of $z$ are each dense in the circle.
This density statement concerns geometric placements, not the height
range possible in a particular tiling.

## Smallest possible number of reflex corners on the controls

A bar $(x_i,h_i)$ fills $[x_{i-1},x_i]\times[0,h_i]$, starting at
$x_0=0$. These explicit decreasing bars lie in the boards just described.

| $N$ | Bars $(x_i,h_i)$ | Rhombi | Reflex corners |
|---:|---|---:|---:|
| 3431 | $(5,12),(14,9),(20,7),(26,5),(32,3)$ | $60+81+42+30+18=231$ | 4 |
| 5063 | $(12,19),(23,13),(35,7)$ | $228+143+84=455$ | 2 |

Together with the [one-reflex capacity theorem](ONE_REFLEX.md), this
shows that **two is the exact minimum on the 5063 board** for an
abstract balanced polygon of the required area. The minimum on the
3431 board is between two and four inclusive.

## An estimate valid for all mesh rotations and translations

Keep mesh length equal to one and let $A$ denote the Euclidean board
area. The board perimeter is $N/c$ and $A=Nab\sqrt3/(4c^2)$. Fix any
rotation and phase of the triangular lattice. Any two of its three axes
give a grid by translates of a unit rhombus $P$. The support distance
of its difference body $P-P$ in the unit normal $n$ is
$|n\cdot e_i|+|n\cdot e_j|$ for the selected unit axis vectors. The
mean of these distances over the three pairs is at most $4/3$, since
$\sum_{i=0}^2 |n\cdot e_i|\le2$. For the last inequality maximize the
projection of $\sum\pm e_i$; the lengths of these signed sums are
0 or 2. By averaging the sums over the three board sides, one pair has
$\sum L_i h_i\le(4/3)N/c$, with $L_i$ the side lengths and $h_i$ their
respective support distances.

Move each board side inward by $h_i$. The remaining region $E$ is a
translated homothetic copy of the board with scale
$1-\sum L_i h_i/(2A)$ whenever this quantity is positive. Indeed the
three barycentric lower bounds are $L_i h_i/(2A)$ and their sum is
the fraction removed from the available barycentric sum. Every grid
rhombus whose interior meets the interior of $E$ lies wholly in the
board, since the difference of any two of its points belongs to $P-P$.
These rhombi cover $E$ up to a set of area zero, and their number is
at least the ceiling of
$$
 \frac{Nab}{2c^2}\left(1-\frac{8c}{3\sqrt3\,ab}\right)^2
 \qquad\text{if }\ 8c<3\sqrt3\,ab.
$$
They admit a simple polygon of every smaller positive integer rhombus
count. In axial coordinates the selected rhombi in each row form an
interval, since the intersection of the open triangle with an open
row strip is convex. Between consecutive nonempty rows the triangle
crosses the common line in an open segment, hence their intervals share
a column. Take successive complete rows until only part of the last is
needed. Begin the last interval in a column shared with its predecessor
and extend it within that row to the desired length. A stack of intervals
meeting in positive-length edges has a simple boundary. All the selected
rhombi are strictly inside the board: an interior point of $E$ satisfies
the three offset inequalities strictly and supplies a strictly positive
slack for its entire closed rhombus.

For $(35,13,43)$, replacing $\sqrt3$ by the smaller $433/250$ gives the
exact rational lower bound $258284339720515/567840809718>454$. The
number of available rhombi is integral, so at least **455** fit, for
every phase and orientation. This result allows the rhombus axis pair
to depend on orientation. It places no bound of two on the number of
reflex vertices for an arbitrary prescribed mesh; the two-corner
example above uses a specific orientation.

[Integer and rational verification of the small cases and both outlines](check_staircases.py).

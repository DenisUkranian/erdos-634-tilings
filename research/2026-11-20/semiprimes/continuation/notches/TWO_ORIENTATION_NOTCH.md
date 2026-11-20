# Sharp threshold for the two orientations at the cone apex

Let $a,b,c$ be a primitive integer tile, $a>b>0$ and
$c^2=a^2+ab+b^2$, and let $z=(a+b e^{i\pi/3})/c$. In the (oblique)
coordinates $x+yz$, use two orientations of this tile:
$$ A=\operatorname{conv}\{(0,0),(a,0),(0,c)\},\qquad
 B=\operatorname{conv}\{(0,0),(c,0),(0,a)\}. $$
These are congruent by reflection in the bisector of the cone between
the positive axes. Let $t,k$ be positive integers with $kB\subset tA$;
interiors of the constituent pieces are required disjoint, and any
partial edge contacts are allowed.

**Theorem.** The notch $\overline{tA\setminus kB}$ admits a tiling by translates and half-turns of $A,B$
if and only if
$$ t\ \ge\ a+c\left\lceil k/a\right\rceil. $$
No lattice constraint on the translations or contact vertices is imposed.
The formula covers arbitrarily large and small corners. Every unit
oversized-load quadrilateral arising from $s>0$, $r\le c-b$ has
$t=(ar-bs)/c<a$. Any hypothetical tiling of that quadrilateral must
therefore introduce some tile orientation outside these two classes.

## Equivalent geometric restriction: no new edge directions

For a strict notch (positive remaining segments on both cone rays), the
four unoriented boundary directions are $1,\rho,z,z/\rho$, where
$\rho=e^{i\pi/3}$. The two orientation classes in the theorem are
**exactly** the tiles all of whose sides use those boundary directions.
Indeed $2\cos\beta=(2a+b)/c$ for $z=e^{i\beta}$, a rational strictly
between 1 and 2. If $z$ had finite order this number would be an
algebraic integer, which is impossible. Thus the exponents of $z$ in
these directions are distinct modulo multiplication by powers of
$\rho$. The short sides have directions separated by $60^\circ$ modulo
$180^\circ$, so they must occupy either the pair $1,\rho$ or the pair
$z,z/\rho$. In the first pair the choice $a$ on $1$ produces long
direction $z$; exchanging $a,b$ produces $\rho/z$, absent from the list.
In the second pair $a$ on $z$ gives long direction $1$; exchanging the
lengths gives $z^2/\rho$, also absent. With the short axes and their
lengths fixed, the included angle of $120^\circ$ determines the tile
up to translation and half-turn.

Consequently the same sharp formula is the criterion for a filling with
only boundary directions, even though no alignment of the junctions
is assumed. In every unit oversized-load case each filling, if it exists,
uses a direction absent from the quadrilateral boundary.

## Why a tiling forces the bound

Here $\gcd(a,c)=1$ by primitivity. Complete the notch by the standard
$k^2$-tile $B$ grid in $kB$. Each triangle of either orientation class
has two axis-parallel sides and a third side, called its slant. The
slant directions are distinct because $a\ne c$, and all slants have
the same physical length $b$.

On any interior line carrying one of these slants, each bank of each
maximal segment of collinear tile edges is partitioned entirely by
slants of that same class. To see equality of the two banks, consider
an interior point of a tile edge distinct from every tile vertex.
Its other bank must be a tile edge in the same line. The ends of a
maximal collinear component are therefore common ends of these two
partitions. Since all lengths are $b$, the two lists of endpoints agree.
Each matched pair of triangles is the full axis rectangle, of dimensions
$a\times c$ or $c\times a$. This holds independently of T-junctions
along the axial edges.

Only the outer slant of $tA$ is exceptional. It has exactly $t$ exposed
$A$ slants, at prescribed successive length-$b$ intervals, and thus
exactly $t$ prescribed caps. Their removal leaves the axis staircase
which under the ordinary $A$ grid is made of $a\times c$ rectangles
in rows of $t-1,t-2,\ldots,1$ cells. Hence each generic horizontal
section has length a multiple of $a$, and each generic vertical section
has length a multiple of $c$. In the proposed tiling the same staircase
is tiled by arbitrary translates of the two rectangle types.

At a horizontal section, the number of $B$ rectangles it meets is a
multiple of $a$, since each has width $c$ and all other widths are $a$.
At a vertical section, the analogous number is a multiple of $c$ since
$B$ rectangle heights are $a$. Thus every generic vertical line meeting
the interior of the union of $B$ rectangles contains at least $ac$
of height there. Even inside the original $tA$, the available height is
$c(t-x/a)$. By closure all the $B$ rectangles lie in $x\le a(t-a)$.

At arbitrarily small positive generic $y$, the horizontal section of
the inserted $kB$ triangle has width $kc-(c/a)y$. Its points are covered
by $B$ rectangles. For $y<a$ its length exceeds $(k-1)c$, so there
are at least $k$ such rectangles on that row. Divisibility rounds this up
to $a\lceil k/a\rceil$ rectangles. They are all in
$0\le x\le a(t-a)$ and their widths add without overlap. Consequently
$ac\lceil k/a\rceil\le a(t-a)$, as claimed. In particular even
a single exchanged apex tile requires $t\ge a+c$ in this class.

For example, with $(a,b,c)=(33,7,37)$, $t=37$ and $k=1$, the
two shortened cone sides have lengths $1184=32\cdot37$ and
$1336=36\cdot33+4\cdot37$. Both individually pass the tests using
only $a,c$ lengths. The theorem still excludes the two-class filling
at that scale, and constructs it for the first time at $t=70$.

## A construction at every scale meeting the bound

This uses the positive coarse-grid construction. Mark all closed square
cells (in the oblique coordinates) of side $ac$ whose interiors meet
the interior of $kB$. For nonnegative cell indices $(i,j)$ the precise
marking test is $ia+jc<k$. Such a cell fits wholly in $tA$ if
$(i+1)c+(j+1)a\le t$. Since $c>a$, the marking test gives
$i+j\le\lfloor(k-1)/a\rfloor$ and hence
$$ (i+1)c+(j+1)a\le a+c\lceil k/a\rceil. $$
Consequently the marked cells cover $kB$ and lie inside $tA$ at the
stated bound. Their union is a union of full cells of both fine rectangle
grids. Tile the marked region from the $B$ grid, retaining everything
outside $kB$, and use the $A$ grid outside the marked region. The two
independent dissections meet along complete straight boundaries and may
have different edge partitions there. This proves sufficiency.

## The reflected-corner quadrilateral in the original F2 reduction

At dilation $h$ the original reflected-corner quadrilateral $Q_h$ has
outer cone intercepts $(hc^2,hac)$ and inner intercepts $(ka,kc)$
with $k=h(a-b)$. Exchanging the two coordinate axes puts it exactly
into the above form with $t=hc$. For any positive admissible $k$, since
$0<a<c$, the condition
$$ hc\ge a+c\lceil k/a\rceil $$
is equivalent to $k\le(h-1)a$. Substitution of $k=h(a-b)$ now gives
$$ Q_h\text{ tiles using only its boundary directions}
 \quad\Longleftrightarrow\quad hb\ge a. $$
In particular the first such dilations of 3431 and 5063 are 5 and 3,
respectively. This statement concerns one sufficient cut of the original
board and a restricted choice of directions inside the cut.

This corollary and the arbitrary-notch version with $t=hc$ were already
proved in the project's semiprime checkpoint 07, `PROGRESS.md`, §§1–2.
Its proof supplied a positive construction and recovered the necessity
from the original packet's `f2/AXIAL_Q.md`. Checkpoint 07 also classified
the two-extra-type case. The arbitrary outer scale $t$ treated here need
not be a multiple of $c$; in particular none of the four leading unit
bridge tests has $c\mid t$.

## Which fresh axes a unit repair must actually use

**Every unit bare notch needs at least two fresh directions, one from
each of two explicit pairs. Every extended pentagon and clipped
hexagon needs a direction outside its own boundary axes, at every
permitted row or column extension.** This includes both controls and
all residual parameters. The argument uses only two straight side
lengths and works at arbitrary partial contacts.

In a strict notch with $k>0$, the surviving cone ray along $1$ has
length $ta-kc>0$. If $t<c$, the partition of this exterior segment
into whole tile sides must include a $b$ side. Otherwise
$ta-kc=Xa+Yc$ with $X,Y\ge0$, so $c\mid(t-X)$ while
$0<t-X\le t<c$. This contradicts $\gcd(a,c)=1$.
In every [expanded pentagon](../patches/PENTAGONS.md) and [clipped hexagon](../patches/HEXAGONS.md)
this very same boundary segment survives as $YW$.

For a tile with its $b$ side along $1$, the $a$ side must be on
$\rho$ or $1/\rho$ (unoriented). If it is on $\rho$, the long side is on
$b+a\rho=c\rho/z$. Otherwise the $a$ side itself supplies the axis
$1/\rho$. Consequently every such tiling uses **at least one** of
$$ \{\,1/\rho,\;\rho/z\,\}. $$
Neither of these is among the five axes $1,\rho,z,z/\rho,z/\rho^2$
of the extended pentagon or hexagon. This conclusion applies even at
the largest row extension, where a former straight side has length $ab$.

The bare notch has a second surviving ray along $z$, of length $tc-ka$.
When $t<a$, it too requires a $b$ side: otherwise
$tc-ka=Xa+Yc$ gives $a\mid(t-Y)$ with $0<t-Y<a$.
Reflection in the cone bisector interchanges $1,z$ and takes the first
pair of required axes to
$$ \{\,z\rho,\;z^2/\rho\,\}. $$
The pairs are disjoint as unoriented axes, and disjoint from the four
original directions, by the irrationality of $\arg(z)/\pi$. All unit
oversized loads have $t<a<c$, since $r\le c-b$ and $s>0$. Thus each
unit bare notch filling would have to use at least six direction axes.
The [one- and two-step pentagons](../patches/PENTAGONS.md) and the
[clipped hexagons](../patches/HEXAGONS.md) would also require at least six axes.
The actual pentagon or hexagon may still tile after introducing these
directions. A full-board tiling may bypass the small regions.

## Prior rhombus exchange

Beeson already exhibited the local rhombus flip in the case of
commensurate sides $3a=2b$, with an interior version leaving the
boundary unchanged. See [Triangle Tiling I, Figure 14 and the paragraph
before Section 6](https://www.michaelbeeson.com/research/papers/TriangleTiling1.pdf).
The simple flip itself is prior work. The sharp exclusions and
enumeration above concern what all tilings in the specified orientation
classes can do.

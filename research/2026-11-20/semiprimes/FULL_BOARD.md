# Orientation gaps in the entire unit F2 triangle

Research note, 20 November 2026. Assume that the primitive tile has odd sides
$a>b>0$ and $c^2=a^2+ab+b^2$. Put $p=a+2b$, $q=2a+b$, $d=a-b$.
Primality of $p,q$ is unnecessary. Write $\rho=e^{i\pi/3}$,
$z=(a+b\rho)/c=e^{i\beta}$ and $R=\mathbb Z[\rho]$. Place the board at
$O=0$, $B=c^2$, $C=apz^2$. Then $C-B=bq\rho z^2$. Its angles at $O,B,C$
are $2\beta,2\alpha,60^\circ$, where $\alpha+\beta=60^\circ$.
Its tile count is $N=pq=2c^2+3ab=3c^2-d^2$.

The *height* $h$ of a direction is the exponent in $\rho^j z^h$.
Directions differing by a multiple of $60^\circ$ have the same height.
A tile is counted at the common height of its $a$- and $b$-edges.
Its $c$-edge is one height away. Write $n_h$ for the number at height $h$.
The board has edge heights $0,2,2$. Reflection and arbitrary partial edge
contacts are allowed throughout. No cuts or corner patches are prescribed.

**Theorem.** In any tiling of this board the occupied heights form an integer
interval with at most one interior value missing.

* If the missing height is $k\le0$, exactly $2c^2$ tiles have height below
  $k$. If it is $k\ge3$, exactly $2c^2$ have height above $k$.
  Height 2 is always occupied.
* If $n_1=0$, exactly $c^2$ tiles have height at most 0 and
  $c^2+3ab$ have height at least 2. Both groups have contiguous height
  support. Heights $-1,0,2,3$ all occur. The two groups meet along
  whole $c$-edges. From the $2\beta$ corner a straight interface follows
  the bisector for at least $c\lceil a/b\rceil$.
* In the last case the entire interface has $I=a+b+2s$ unit edges for an
  integer $s\ge0$ (physical length $cI$). At $s=0$ the low group is exactly
  the triangle formed by $OB$ and the two bisectors from $O$ and $B$.
  This triangle can be replaced by its standard grid of $c^2$ tiles at
  height 1 while keeping the rest of the tiling. Consequently an existence
  search can restrict itself to tilings with $n_1>0$ or to tilings with
  $n_1=0$ and $I\ge a+b+2$.

## Counts beyond a missing height

The angles propagate across positive-length contacts. These contacts connect
any two tiles by perturbing a path to avoid the finitely many vertices.
The rational number $2\cos\beta=q/c$ lies strictly between 1 and 2. If
$z$ were a root of unity that number would be an algebraic integer, which
a nonintegral rational cannot be. This proves uniqueness of the height.
Adjacent tiles have short heights differing by at most two.

Here are the earlier ingredients and how they apply. The
[whole-edge cut identity](../../../docs/height-cut-area.md) says that for
$H_k$ the union of the tiles of height greater than $k$,
$\partial H_k-B_{>k}$ is the sum of selected whole $c$-edges.
Here $B_{>k}$ consists of the board edges at heights above $k$.
The selected edges arise only from tiles of height $k,k+1$ with the
long edge on the other side of the cut. This follows by subtracting
the high edges of each tile from its boundary weighted by its high-tile
indicator. Internal contacts then cancel as oriented segments.
The [F2 population calculation](../../i120-global-oct7/HEIGHT_LEVELS.md)
gives $n_h\equiv0\pmod c$ for $h\ne2$ and $n_2\equiv N\pmod c$.
The sides are pairwise coprime. Also $3\nmid c$ (if $a=b\pmod3$,
primitivity gives $c^2=3\pmod9$). Hence $c\nmid3ab$ and $n_2>0$.

When $k\le0$ is vacant apply the cut at $k-1$ to the low tail. There
are no exterior edges of height at most $k-1$. When $k\ge2$ is vacant
apply the cut at $k$ to the high tail. There are no exterior edges of
height greater than $k$. In either case the boundary of the tail is a
chain of whole $c$-edges of height $k$. The
[single-height boundary bound](../../gap-closure-oct8/structure/WHOLE_C_BOUNDARY.md)
gives a multiple of $c^2$ of size at least $2c^2$ for a nonempty tail.
For clarity, the same bound applies to a boundary *represented* by the
whole-edge chain. Closed walks give area divisible by $c^2\sqrt3/4$.
The boundary character and its parity proof only use the sum of those
edges with multiplicities. A short derivation follows.

For any oriented boundary segment of direction $\rho^jz^h$ and length
$L$ use the two weights $(-1)^j L$ and $(-1)^{j+h}L$. They reverse
under orientation reversal and add at T-junctions. On a CCW tile the
two weights summed over the boundary are $(d-c)\epsilon$ and
$(d+c)(-1)^h\epsilon$ with $\epsilon\in\{-1,1\}$. This follows from
the reference tile $(0,a,a+b\rho)$, and persists after rotations,
reflections and translations. On a region of $m$ tiles let $D,D_*$ be
the sums of $\epsilon,(-1)^h\epsilon$. Both have absolute value at most
$m$ and parity $m$. For a height-$k$ whole-$c$ boundary write $cM$ for
the first weight. Then
$(d-c)D=cM$ and $(d+c)D_*=(-1)^k cM$.
The odd integers $c-d$ and $c+d$ are coprime since $\gcd(c,d)=1$,
$d$ is even and $c$ is odd. Their product is $3ab$.
Thus $M=3ab r$ with $r\in\mathbb Z$, $|D|=c(c+d)|r|$ and
$r\equiv m\pmod2$. The area of one tile is $ab\sqrt3/4$, so the lattice
area and coprimality give $c^2\mid m$. The choice $m=c^2$ would force
$|r|\ge1$ and $|D|>m$.

Since $N<3c^2$, every nonempty far tail across such a gap contains
exactly $2c^2$ tiles. Two gaps on opposite sides would require two
disjoint tails of this size. Two gaps on the same side with an occupied
height between them would require strictly nested tails of the same
size. Two consecutive internal heights cannot both be vacant since
adjacent tiles change height by at most two. It remains to account for
the middle height.

## The middle gap fixes both populations

Suppose $n_1=0$. Write $L$ for the region of heights at most 0 and $H$
for the region of heights at least 2. The whole base $OB$ is on the
boundary of $L$ and the two remaining sides belong to $H$, up to
vertices. Both regions have positive area. Interfaces lie on axes of
height 1. Every edge there has length $c$. On each maximal collinear
edge run the two banks partition the same interval into lengths $c$
from its endpoints. This pairs the whole edges, including in the presence
of T-junctions elsewhere. Their oriented union with the base gives
$\partial L$. The long edge of a tile at any board side occurs at least
once on that side. Otherwise each of its $t$ contributing $a,b$ edges
would put a $120^\circ$ angle at one of only $t-1$ internal joins, and
two such corners cannot share a join. All three board angles are less
than $120^\circ$. Consequently heights $-1$ and 3 both occur. Connectivity
forces both 0 and 2 between them.

The interface steps belong to $czR$ and $B/(cz)=c\bar z=a+b-b\rho$
also belongs to $R$. Adding the directed base to the interface gives a
closed integral chain in the sense of the preceding area argument:
each closed walk has its own lattice translation. Thus $|L|=tc^2$ with
$t=1$ or 2, where vertical bars here count tiles. Let $cM$ be the first
weight of the interface directed as part of $\partial L$. The base has
weight $c^2$ for both characters, so
$$
 (d-c) D_L=c^2+cM,\qquad (d+c)D_{*,L}=c^2-cM.
$$
These imply $M=-d+3ab r$ and
$$
 D_L=-c[1+(c+d)r],\qquad D_{*,L}=c[1-(c-d)r],\qquad
 t\equiv1+r\pmod2 .
$$
For the full board the first boundary weight is $c^2-ap-bq=-3ab$,
so $D_{\rm all}=c+d$. If $t=2$, the high group has only $3ab$ tiles,
and $r$ is odd. But
$$
 |D_H|=|2c+d+c(c+d)r|
 \ge c(c+d)-(2c+d)>3ab .
$$
The last difference is $(d-2)c+d(d-1)>0$ because $d\ge2$.
This is impossible. For $t=1$, any nonzero even $r$ would give
$|D_L|>c^2$. Hence $t=1,r=0,M=-d$. The two populations are
$c^2$ and $c^2+3ab$, each smaller than $2c^2$. A further gap on
either side would require a tail of $2c^2$, which finishes the proof
of the one-gap assertion.

## The initial seam and the shortest possible interface

Use the axial coordinates $x+y\rho$ after division by $cz$. Then
$O=(0,0)$, $B=(a+b,-b)$. At $O$ the board is in the wedge
$$
 -bx/(a+b)\le y\le bx/a .
$$
Orient the interface from $O$ to $B$ by reversing its low-side boundary
orientation. Its integer directed flow has one source and one sink. It
therefore contains a simple path from $O$ to $B$, plus possibly closed
walks. The path begins in $R$ and all its steps are unit lattice
directions. At $(i,0)$ a nonhorizontal step into the wedge needs
$i\ge a/b$. Indeed the most favorable positive and negative endpoints
are $(i,1)$ and $(i+1,-1)$, respectively. Both require that same
inequality. The simple path cannot backtrack. Its first $\lceil a/b\rceil$
steps follow the bisector. Both banks there are made of whole tile edges. The [interface theorem](INTERFACE.md) proves that the full interface is a single simple path, including when the path touches the other board boundary.

Compare the directed interface with the reference path $O\to W\to B$,
where $W=(a,0)$. The reference has $a$ edges $E=(1,0)$ and $b$ edges
$S=(1,-1)$. Both chains have net displacement $B$ and first character
$d$ in units of $c$. Displacement and character together determine
the three signed counts on axes $1,\rho,\rho^2$: the vector projection
has kernel generated by $(1,-1,1)$, whose character is 3. The signed
counts therefore agree on each axis. The total edge count is
$I=a+b+2s$ for an integer $s\ge0$.

If $s=0$, only forward $E,S$ edges occur. Their $x$-coordinates increase
so the entire flow is a single path. Among the orders of its steps,
$E^aS^b$ uniquely maximizes the signed area above the base. Each
interchange of $SE$ to $ES$ increases that area by one unit
parallelogram. The maximum is $ab$ half-parallelograms, already required
by the $c^2$ low tiles. The only path is the reference and the low region
is $OBW$. Its two short side lengths are $ac,bc$ and the included angle
is $120^\circ$. Subdividing it in the standard triangular grid supplies
$c^2$ height-1 tiles. This proves the replacement assertion. In particular
the two comparison triangles in this argument are never assumed to be
subregions of an arbitrary input tiling.

## A limitation with an explicit witness for every shape

The next possible edge count already passes the interface tests in this
note. Put $U=(0,1)$ and read the following word from $O$:
$$
 E^{a-2}\, U S\, E\, S\,(-U)E\, S^{b-2}.
$$
It replaces one $E$ of the reference by $US$ and one $S$ by $(-U)E$.
The two elementary triangular changes have opposite signed areas.
The word has the required signed counts and $a+b+2$ edges. It has a
simple trace: $x$ increases except for the two vertical steps on
different columns. The extra vertices are $(a-2,1)$ and $(a+1,-2)$.
Besides the wedge above, the board has the inequality
$(a+b)x+by\le a(a+2b)$. Both vertices strictly satisfy all three
bounds when $a>b\ge3$, $a\ge5$, as holds for the primitive odd
tiles here. For example $(a+1,-2)$ satisfies the lower bound because
$(a-1)b>2a$ for $a\ge5,b\ge3$. Other vertices are on the reference
path. The word therefore cuts the board into the required exact geometric
areas and satisfies the forced initial run. It assigns no tiles to
either side. It shows why the population, total signed directions,
initial seam and area alone cannot force a shortest interface.

A general existence or impossibility proof still needs geometric
information about actual placements. The case in which height 1
is occupied is allowed by all the gap statements.

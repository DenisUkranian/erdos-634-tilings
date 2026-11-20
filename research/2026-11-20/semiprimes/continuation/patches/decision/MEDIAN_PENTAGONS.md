# Shortest median paths for the residual pentagons

Let the polygon be the Eisenstein pentagon $X',Y,W,D,D'$ of the translated
two-step or one-step construction. Write $j$ for the strip extension.
The directed whole-long-edge cut of the union of tiles at short heights
strictly above 0 gives an edge path $W\to X'$: the other exterior arc
$W,D,D',X'$ has height 1, and the clockwise arc $X',Y,W$ has height 0.
In the cut-chain identity the positive bank for a height-0 step is
on its left (short height 1); the bank for a height-1 step is on its
right (short height 0). Removing directed cycles in the abstract finite
graph gives a path with no repeated vertex. This argument uses the original
whole long edges, hence also applies with T-junctions. Geometric simplicity of the chosen path is proved below.

Put $d=a-b$, $z=(a+b\rho)/c$, $\rho=e^{i\pi/3}$.
For $h=0,1$, let $J_h$ sum $(-1)^i$ over path steps
$c\rho^i z^h$. Appending $X'Y,YW$ to the path yields a closed walk
along tile edges. Its winding is integral and constant on each open
tile. Its two directed boundary characters (with weights $(-1)^i L$
and $(-1)^{i+h}L$ at length $L$) are thus integer sums of entire
tile characters. The two contributions of the exterior arc are both
$A=td-(k+j)c$. Consequently
$$
 A+c(J_0+J_1)=0\pmod{c-d},\qquad
 A+c(J_0-J_1)=0\pmod{c+d}.
$$
The second is $J_0-J_1=t+k+j\pmod{c+d}$. Both character quotients have
the parity of the integer signed area in tile units. These conclusions
allow self-contact and arbitrary interior directions.

The displacement further fixes
$$
 (k c-ta,-jc-tb)=c(X,Y)+(a x-b y,bx+(a+b)y).
$$
For each of the two heights, displacement $(x,y)$ and character $J$
determine the signed multiplicities on $1,\rho,\rho^2$ uniquely:
$(x+r,y-r,r)$ where $r=(J-x+y)/3$ is integral. The sum of their
absolute values is the shortest possible word with these signed
multiplicities. Every longer word has opposing pairs added to these
six axis counts. The straight net word with $k+j+t$ steps gives a
universal search ceiling for the arithmetic minimum. Enumeration thus
needs only bounded integer ranges and no lattice ansatz for the other
tiles.

| Polygon in tile units | Pure displacement and both characters | Minimum after testing wall containment, integral signed area and bank triangle disjointness |
|---:|---:|---:|
| 168 | 22 | 22 |
| 180 | 14 | 16 |
| 206 | 15 | 19 |
| 250 | 27 | 29 |

Here the last column is an exact minimum for this necessary path test.
It supplies a lower bound on the median path in a complete tiling.
Every matched endpoint, board containment and bank contact used in a
positive path certificate is consistent with individually placing those
specific path tiles. Covering the two sides of the path is a further
problem.

To reproduce, run `python replay_path_minima.py`. For each bound the
script enumerates all possible signed inventories and ways to add
opposing pairs. For an inventory the state is the counts remaining;
its position is determined by those counts. It stores possible signed
doubled areas and rejects bank triangles outside the convex pentagon.
A final search uses only states of a valid signed area, removes repeated
path vertices, and checks pairwise nonoverlap of all bank triangles.
The sign and area tests use winding-weighted integers, without a
geometric simplicity assumption. For the 180 polygon the sole candidate
inventory at 14 steps gives 264 possible signed areas and none is an
integer in tile units. At 206 and 250 the shortest respective
inventories have no ordering with every bank triangle contained.

## One entire side of a median path has a single short orientation height

**Theorem.** In any filling of either the 168- or 180-tile pentagon, choose
any vertex-simple directed median path as above. Its left/right partition
has one entire side tiled at its designated single short height. The side
adjacent to the low exterior arc designates height 0; the complementary
side designates height 1. More precisely, all tiles that deviate from
their side's designated short height form a single side-and-height
population. If this population is nonempty it has $2c$ or $3c$ tiles.

**Proof.** All path vertices are in a translate of
$M=cR+(a+b\rho)R$, $R=\mathbb Z[\rho]$. Along each of the twelve rays
of the path alphabet the primitive lattice step has length $c$.
For a horizontal vector $(x,0)$ in $M$, the congruence
$a y-b x=0\pmod c$ gives $c\mid x$, as $b$ is a unit modulo $c$.
The rotations by units preserve $M$. The same test after division by $z$
uses $cR+(a+b-b\rho)R$ with the second generator's coefficient of
$\rho$ equal to $-b$. Hence no path vertex is inside a path edge.
Interiors of two nonparallel path edges cannot cross, since each
carries a tiled bank and the two tiles' interiors would overlap near
the crossing. Two collinear path edges can overlap in their interiors
only by coincidence; a vertex-simple path excludes this. Thus the
chosen median arc is geometrically simple. This is the primitive-step
argument of the full-board two-path theorem.

Join its endpoints by an arc just outside the convex polygon on the side
of $X'YW$, disjoint from the original polygon except at its endpoints.
The result is a Jordan curve. Its interior selects the low-side tiles,
and its exterior selects the high-side tiles. One may replace the outside
arc by the actual low boundary arc in the oriented boundary of this
tile union: where the path follows a polygon side in reverse to this
arc, the segments cancel; where the path follows the opposite polygon
side, it is the boundary of the low region there. Equivalently use
the winding number of the closed path plus $X'YW$ on the open polygon.
It is 0 or $-1$ since deforming the exterior arc onto the boundary
does not cross open tile interiors. Every boundary therefore is the sum
of the displayed native exterior arc and signed whole median edges.
There can be several open connected components on a side.

For the low side, every boundary segment of heights above 0 represents
a whole $c$ edge at height 1. For the high cut at 0 these steps close
the chain of the high tile union in $M$. A polygonal cycle on this
index-$c$ lattice has doubled axial area divisible by $c$; hence the
population above 0 on the low side is divisible by $c$ since
$\gcd(ab,c)=1$. At thresholds $k\ge1$ there are no high exterior
edges, and at $k<0$ no low exterior edges. The exterior-free threshold
chain is in a translate of $z^kM$ whose doubled lattice area is again
$c$; compare the corresponding integer tile area. Tail differences
prove that each non-designated height on the low side has population
divisible by $c$. On the high side use the low tail at threshold 0:
its displayed low exterior edges are whole $c$ edges at height 0,
again in $M$. Other exterior-free thresholds give the same conclusion
there. If a tail boundary has multiple components the closed walks may
use different lattice translates, which do not change the area.

On each supporting line of a non-designated height the exterior
signed length of either side is a multiple of $c$: its only terms are
whole median steps. The uniform line-count theorem in
`semiprime-public/LINE_COUNTS.md` therefore excludes a population of
exactly $c$. Every nonzero non-designated side-and-height population
costs at least $2c$.

On the low side the closing displacement of $X'YW$ belongs to $M$.
Closing it by its chord shows that its doubled area differs from
$(ta-kc)(jc+tb)$ by a multiple of $c$. Its tile count modulo $c$ is
therefore $t^2$. The native population has this same residue since all
other populations are multiples of $c$. The native population on the
high side correspondingly has residue $N-t^2$. Their least residues
are $(21,36)$ for 168 and $(35,16)$ for 180. Subtracting their sum from
the board leaves $3c$ in each case. Two nonempty non-designated
populations would require at least $4c$, which is too large. This proves
the theorem, without any initial restriction on directions.

The same proof works for any pentagon for which the least positive
or nonnegative native residues (as warranted by geometric positivity)
leave fewer than $4c$ tiles. It constrains the pentagon filling that
would suffice for the original board. A full-board tiling outside this
dissection need not supply a pentagon filling.

# Two directed paths of whole long edges on every unit F2 board

Use the primitive odd F2 convention of the full-board note, with outer
vertices $O=0$, $B=c^2$, $C=apz^2$, $R=\mathbb Z[\rho]$,
$\rho=e^{i\pi/3}$, $z=(a+b\rho)/c$. There is no restriction on
interior heights, tile orientations, or T-junctions.

**Theorem.** For each $k=0,1$ the tiling contains a directed path from $O$
to $B$ made of whole tile long edges, directed from their $\beta$ to
their $\alpha$ endpoint. A step of long height $k$ has its tile of short
height $k+1$ on the left. A step of long height $k+1$ has its tile of
short height $k$ on the right. The two chosen paths use disjoint tiles, even
if some edges geometrically coincide. All vertices on each path are
respectively in $L_k=cz^k(R+zR)$, with
$L_0\cap L_1=czR$.

Indeed apply the whole-edge median cut to the union of tiles with short
height greater than $k$. The boundary minus the high exterior arc
retains just whole long edges of the two sorts in the theorem. On a
short-height-$k$ tile with the long edge of height $k+1$, its negative
CCW long edge goes from $\beta$ to $\alpha$, by the reference tile
$(0,a,a+b\rho)$. The other hand gives the positive CCW edge with the
same direction on the opposing bank. For either cut the high exterior
arc is $B\to C\to O$, so the boundary of the directed chain is $B-O$.
The integer directed multigraph contains an $O$ to $B$ path and a
collection of cycles. Keeping individual tile edges preserves their
endpoints even at partial contacts. Edges from distinct cuts represent
different tiles, as a long edge crosses exactly one height threshold.
Geometric simplicity is not required for this conclusion.

For the lattice assertion note that $R$ is the Euclidean Eisenstein ring.
Write $z=\lambda/\eta$ in lowest terms. A unit factor in the fraction is
harmless. Equal algebraic norms of numerator and denominator give
$N(\lambda)=N(\eta)=c$: the lattice $R+zR=\eta^{-1}R$ has index $c$
over $R$ since $(a+b\rho)w\in cR$ imposes exactly one independent
congruence modulo $c$ on the two integral coordinates of $w$. In fact
it is $a x-b y=0\pmod c$; the other coordinate vanishes automatically
by $a^2+ab+b^2=c^2$ and $\gcd(a,c)=1$. Thus $L_0=c\eta^{-1}R$ and $L_1=c\lambda\eta^{-2}R$. Their
intersection is $c\lambda\eta^{-1}R=czR$. Their fundamental area
is $c\sqrt3/2$. A closed path formed by adding the reversed base to
one of these paths has oriented area an integral multiple of
$c\sqrt3/4$. Its winding number is constant on each open tile, so
its signed area is also an integral multiple of $ab\sqrt3/4$.
This gives a multiple of $c$ in tile units even with self-contacts.

**Exact displacement bound.** Suppose the primitive parameters $u,v$
lie beyond the odd unit staircase. Each lower path has at least $c$
steps and each upper path has at least
$$
 \mu=a+b-v\left\lfloor {2v-1\over g}\right\rfloor,
 \qquad g=\gcd(3,u-v).
$$
These are sharp only for the respective step alphabets and endpoint
displacements. The stronger genuine-tiling bound in the last section
excludes all mixed shortest words in the residuals. This displacement
result is proved without any assumption that a shortest word extends to
an actual tiling. Primality is unnecessary.

In units $cz$, the end is $(a+b,-b)$. The available upper steps are
units of $R$ and their $z$-rotates. Denote the net middle displacement
by $(X,Y)$ and the net upper displacement before rotation by $(x,y)$.
Write $m=x+y$. The least cost per net vector is
$H(x,y)=\max(|x|,|y|,|x+y|)$. Put $A=(u+2v)/g$, $D=(2u+v)/g$,
$F=(u-v)/g$, so $c-a=vA$, $b=vD$. As the endpoint is integral,
the first coordinate of $z(x+y\rho)$ is integral. Therefore
$t=(-Ax-Dy)/c$ is an integer since $\gcd(c,v)=1$. The coordinate
equations reduce to
$$
 X=a+b-x-vt,\qquad Y=-b+(u+v)t+m .
$$
The second identity follows by substitution, using the primitive
parameter formulas in the full-board note. Set the nonnegative
deficiencies $s_A=H(X,Y)-X$, $s_B=H(x,y)-x$. The improvement over
$a+b$ in the net-vector cost is $G=vt-s_A-s_B$. Since $s_A\ge Y$ and
$s_B\ge-m$, we also have $G\le b-ut$. Thus for every integer $t$,
$$
 G\le\min(vt,b-ut).
$$
Set $t_0=\lfloor(2v-1)/g\rfloor$. For $t\le t_0$ the desired bound
follows. For $t\ge t_0+1\ge2v/g$, $G\le v^2/g$. This is at most
$vt_0$, apart from $v=1,g=3$ where $G$ is integral and $v^2/g<1$.

To attain it if $t_0=0$ take $x=y=0$. Otherwise set
$$
 t=t_0,\quad x=ut+D,\quad m=F-vt,\quad y=m-x .
$$
Then $Fx-Dm=tc$ because $uF+vD=c$. The first coordinate congruence
holds and yields the indicated pair $(X,Y)$. The residual range has
$u>2v^2+v$ for $v\ge3$ (the exceptional staircase starts above
$4v(v-1)$, with odd $v\ge5$ there). For $v=1$ outside the staircase
$u>4$. Thus $m\ge0$, and $m\le x$. Also $Y=-b+ut+F\le0$ since
$gt\le2v-1$. Finally $X+Y=a-vt-A\ge0$, since
$g(a-vt-A)\ge u^2-u-3v^2-v>0$ for $u> (1+\sqrt3)v$ and
$u\ge4$ (or directly from the residual inequalities).
Both deficiencies vanish. The two hexagonal shortest words attaining
each net vector give equality for the displacement-only problem.
For the lower path the straight word along the base attains the
Euclidean distance bound $c$.

The net bound is computed separately from the geometry in
[chain_bounds.py](chain_bounds.py). The finite [control certificates and verification](verify_paths.py) also demand the tiles touching the base in a
two-height search, the bank tile at each step, whole-tile signed area,
containment and disjoint tile interiors. At the first two controls there
are mixed upper paths attaining the bound with all these tests, and the
remaining interiors are unfilled.

| N | Lower displacement bound | Upper displacement-only bound | Placed tiles in partial control | Areas below / above partial path in tile units |
|---:|---:|---:|---:|---:|
| 3431 | 37 | 40 | 77 | 1147 / 2284 |
| 5063 | 43 | 47 | 90 | 1548 / 3515 |

Neither displayed mixed path can separate two tiled regions: the
stronger boundary-character theorem below excludes both. The partial
packings certify only the explicitly listed local tests. The lower
row of base triangles in these controls is a search choice.
It is necessary if only heights 1 and 2 occur, but arbitrary tilings
can use lower heights elsewhere.

## Net vectors of all shortest upper paths

The equality case gives a small finite list. Put $r_0=2v-g t_0$. In the
residual domain $r_0=1$ or 2 (for $g=1$ it is 1).
Every displacement-only shortest upper word uses only $1,1-\rho,z,z(1-\rho)$ in the
$cz$ frame. Its two net vectors have
$$
 x=ut_0+Dj,\quad m=x+y=Fj-vt_0,\quad
 X=a+b-x-vt_0,\quad Y=-b+ut_0+Fj ,
$$
with
$$
 \left\lceil vt_0/F\right\rceil\le j\le
 \left\lfloor(b-ut_0)/F\right\rfloor .
$$
It has $X+Y,-Y,m,x-m$ occurrences of the four directions in the
order displayed. These equations concern any ordering subject to
the geometric constraints. A shortest upper path need not occur in
a given tiling.

Indeed an optimal $t<t_0$ loses at least $v$. For $t>t_0$ the bound
$b-ut\le v^2/g$ is strict relative to $vt_0$ throughout the residuals,
except possibly at $v=1$. For $v=1,g=3$ one has $b-u<0$.
For $v=1,g=1$ a possible tie would require $t=2$, $s_A+s_B=1$
and $Y-m=1$, hence $-1\le m\le0$. But $m=Fj-2$ and $F=u-1\ge5$.
The parameterization by $j$ at any $t$ follows from $Fx-Dm=ct$ and
$c=uF+vD$, $\gcd(F,D)=1$. Thus $t=t_0$ and both deficiencies vanish.
On a shortest path all projection costs on the two alphabets must
also be individually sharp. The only hexagonal unit steps with
unit $x$-projection are $(1,0),(1,-1)$.

For example the 5063 control has just one displacement-only shortest inventory:
26 steps $1$, 2 steps $1-\rho$, 4 steps $z$ and 15 steps
$z(1-\rho)$. The 3431 control has three shortest net inventories,
one supported on the middle directions alone.

## The upper path always cuts off a genuine tiled region

No condition on the occupied heights is needed here. In the $cz$ frame,
the upper path lattice is $R+zR$. In axial coordinates it is exactly
$$
 \{(U,V)/c: U,V\in\mathbb Z,\ aV-bU=0\pmod c\}.
$$
Indeed $(a,b)$ and $(-b,a+b)$ satisfy this relation, and every residue
solution is a multiple of $(a,b)$ since $a$ is a unit modulo $c$. A
horizontal lattice displacement then has $c\mid U$, since $V=0$ and
$b$ is a unit modulo $c$. Rotation by $\rho$ preserves the lattice.
Dividing the lattice by $z$ gives $R+\bar zR$, where the same test uses
the primitive pair $(a+b,-b)$. Consequently along each ray of either
step alphabet the lattice displacements are exactly integer multiples
of the corresponding unit step. No lattice vertex can occur strictly
inside an upper-path edge.

Take a vertex-simple directed graph path from $O$ to $B$. Distinct
edges cannot meet internally in a transverse crossing: each is the
whole side of some tile, and two half-disks of different directions
at a transverse interior crossing overlap in positive area. A geometric
T-contact between two of its edges would place a path vertex strictly
inside a unit lattice step, just ruled out. Collinear overlap of edges
from this path forces their endpoints to agree, which a vertex-simple
path avoids. Thus this particular path is a simple plane arc even if
other tile edges and arcs make T-contacts with it.

Its only base contacts are $O$ and $B$. In this frame the endpoint is
$B=(a+b,-b)$, a primitive axial vector. A lattice point of the line
through $OB$ must therefore have numerator $(U,V)=t(a+b,-b)$ with
$t\in\mathbb Z$. The lattice test becomes $c\mid b(2a+b)t$ and
$\gcd(c,b(2a+b))=1$: $q^2=4c^2-3b^2$, $3\nmid c$, and
$\gcd(b,c)=1$. Hence $c\mid t$. The open base has no lattice point,
and cannot contain a subsegment of any step because its direction is
outside both alphabets. A straight segment in the convex board can
meet the open base only at a segment endpoint or along the base.

The union of path and base is a simple closed polygon bounding a
positive-area lower region. The vertex $C$ is not on the path: in this
frame $OC$ is in the $z$-alphabet, but $|OC|=ap/c$ is not integral,
by $p^2=4c^2-3a^2$ and coprimality. This excludes a path vertex at $C$. As an extreme point of the convex board, $C$ cannot lie in the relative interior of a nontrivial path segment or in the interior of the polygon either. A
relative neighborhood of $C$ in the board belongs to the remainder,
which also has positive area. The path may visit or follow $OC$ or
$BC$ repeatedly. The remainder can have several open components.
The simple closed polygon on the base side exists in all these cases.
No tile interior crosses its boundary, so it and the entire remainder
are unions of whole tiles. The earlier area argument now gives a
positive multiple of $c$ for the actual number below the path.

A stronger conclusion applies on this lower polygon. **Every occupied
short height, including 2, contains at least $2c$ tiles below the cut
and is a multiple of $c$.** In fact every boundary segment in its
displayed decomposition is a whole $c$ step at height 1 or 2, except
the whole base of length $c^2$ at height 0. Thus all exterior signed
line currents at every level are multiples of $c$. To check population
divisibility use the median cut on the lower polygon itself. At threshold
$k=1$ each high exterior edge is one $c$-step of height 2 and belongs
to $L_1$. This closes the high-chain area calculation. At threshold
$k=0$ the low exterior chain is the whole base, whose displacement
$c^2$ belongs to $L_0$. This closes the low-chain calculation. At
$k\ge2$ there are no high exterior edges; at $k<0$ there are no low
exterior edges. Thus the lower and upper tails outside the central
interval, the tail up through 0 and the tail above 1, all have count
divisible by $c$. The whole lower polygon has count divisible by $c$,
so differences give population divisibility at each individual height.
The uniform single-block exclusion from LINE_COUNTS.md now applies.
For $h\ne2$ the same conclusion holds in the entire remainder by
subtraction for divisibility and by its signed exterior line currents
for the exclusion; the line argument works for several components.
Therefore every global height $h\ne2$ with $n_h=2c$ or $3c$ lies
entirely on one side of **each** such upper cut. If the cut contains
a long height-2 edge, its prescribed bank tile has short height 1
and lies below it (the interior of the base-side polygon is to the
right when the path is directed $O\to B$). In particular if
$0<n_1<4c$ all the middle tiles then lie below this cut.

## Five blocks are necessary when only two short heights are used

Suppose the entire board uses short heights 1 and 2. Then
$$
 n_1\ge 5c,\qquad n_1/c\text{ is odd}.
$$
The earlier population and line exclusion gives divisibility and rules
out $c$. The two scalar currents give $G_1=c$ since 1 is the sole odd
height. Here $G_1$ is the number of positive height-1 signs minus the
number of negatives. This proves odd parity of $n_1/c$.

Work in physical coordinates divided by $z$, with basis $(1,\rho)$;
$E=(1,0)$, $S=(1,-1)$. Each of the $c$ consecutive base segments has
length $c$ because only height-1 tiles with long edge at height 0 can
supply the base. Its unique tile has vertices
$$p_i=i(a+b,-b),\quad p_{i+1},\quad p_i+(a,0) \qquad(0\le i<c)$$
in CCW order. Its $a$-edge is directed $-E$ and has negative character.
If $n_1=3c$, its $c$ negative-sign tiles are thereby exhausted.
An interior edge of height 0 is always a long edge; in a maximal
collinear run both banks partition the same interval into $c$-steps.
Each such interior edge is matched in a half-turn pair (only one hand
has short height 1 and long height 0). The pair would use an additional
negative tile. Therefore the remaining $2c$ short-height-1 tiles all
have positive sign and long height 2.

There are three rotations of this hand with positive sign. Their
counts $(A,B',D')$ correspond to the short-axis pairs
$(E,\rho)$, $(\rho,S)$, $(S,E)$ in $(a,b)$ order; the axes in this
list are unoriented. On each affine short-height-1 line, take the
direction character weighted by length. There is no exterior edge of
this height, all other contributors are whole $c$-edges, and the
positive tiles have contributions $+a,-b$. The $c$ negative base
$a$-edges lie on distinct $E$-lines, and the $c$ negative base
$b$-edges lie on distinct $S$-lines. A marked $E$-line without a
type-$A$ tile needs at least $l$ type-$D'$ tiles, where
$bl=-a\bmod c$, $0<l<c$. Likewise a marked $S$-line without a
type-$B'$ tile needs at least $m$ type-$D'$ tiles, where
$am=-b\bmod c$, $0<m<c$. Neither least residue is one, since
$c<a+b<2c$. They cannot both be two, since that would imply
$c\mid 3a$ despite $\gcd(c,3a)=1$. Hence $1/l+1/m<1$.
Counting marked lines yields
$$
 A\ge c-D'/l,\qquad B'\ge c-D'/m.
$$
Their sum and $A+B'+D'=2c$ force $D'=0$ and $A=B'=c$.

Each marked $E$-line therefore has just one positive $a$-interval and
one negative $a$-interval. All other contributions on it are whole
$c$-edges of either sign. Periodize this signed interval identity
on the length-$c$ circle along the line. Each $c$ interval gives
a constant function almost everywhere. The two $a$ indicators have
equal integrals; their difference must be zero. As $0<a<c$, their
endpoints agree modulo $c$, comparing origins in increasing $x$ order.
For the $i$-th line, the positive $A$ tile therefore begins its
$a$-edge at $x=i(a+b)$ modulo $c$ and its ensuing $b$-edge lies on
the $\rho$-line
$$ x=i(a+b)+a\pmod c . $$
These are $c$ distinct line residue classes because $\gcd(a+b,c)=1$
(the norm gives $c^2=(a+b)^2-ab$). On the union of $\rho$-lines with
any one such residue, exactly one $b$ edge now contributes $-b$.
The only short $a$ edges there come from $B'$ tiles. Long edges
contribute multiples of $c$ upon summing line currents, so at least
one $B'$ is required in each residue. Exactly $c$ are available, giving
one in every residue. This would force $c\mid a-b$ and is impossible.

In the original controls this elementary argument gives lower bounds 185 and 215 for the
intermediate-height populations when only two short heights occur.
The argument imposes no staircase, side-to-side matching or restriction
on the positions of the high tiles.

More generally, suppose the smallest short height is at least 1 and allow
all higher heights. Then $n_1\ge3c$ and at least $5c$ tiles have odd
short height in total. For $n_1=2c$ the $c$ fixed base teeth would
leave only $c$ other short-height-1 tiles. Each of the $2c$ distinct
marked base short-edge lines needs a further short edge to cancel
its nonzero current modulo $c$. Thus every remaining tile must use an
$E$-line and an $S$-line, and every marked line receives exactly one
edge. Mismatched labels cannot cancel since neither $a-b$ nor $a+b$
is divisible by $c$. Equal signs with matched labels cannot cancel
either, since $c$ is odd and coprime to both $a,b$. Every remaining
tile must have $a$ on $E$, $b$ on $S$, and positive sign. This is
the down hand, whose interior $c$ edge at height 0 would need a
negative nonbase half-turn mate. All negative tiles were used on the
base. Divisibility and the single-block lemma now yield $n_1\ge3c$.
If the total odd population were less than $5c$ it could only be
$3c$ by odd parity of its quotient by $c$. It would all occur at 1
and have $G_1=c$. The $3c$ proof above depends solely on the base
teeth, the absence of short heights at most zero, and whole-edge
current cancellations on the height-1 lines. Thus that same
contradiction applies, even with extra even heights.

## Stronger upper-path bound and equality for every genuine tiling

With the boundary-character observation from the pentagon path analysis,
one can distinguish locally admissible sequences from genuine upper
cuts. For every primitive odd unit F2 shape with $u>3v$, **every** upper
path bounding the tiled lower region has at least $a+b$ edges. Equality
forces the specific path $E^a S^b$ in the $cz$ frame, $E=1,S=1-\rho$.
It encloses the triangle $OBW$ with $W=acz$, which can be filled by its
canonical grid of $c^2$ short-height-1 tiles. This applies whether or
not the original board has a height gap. In particular the true lower
bounds are 40 for 3431 and 48 for 5063. The initial staircase residuals
and all subsequent ones have $u/v\ge6$ by the inequalities above.

Let $J_1,J_2$ be sums of the signed direction characters on the middle
and upper steps, respectively, normalized by removing their length
$c$. Put $d=a-b$ and $L$ for the number of steps. The lower polygon
has CCW boundary consisting of the base then the reversed path. Its
two scalar currents from the full-board theorem are
$c^2-c(J_1+J_2)$ and $c^2+c(J_1-J_2)$, divisible by $d-c$ and $d+c$,
respectively. Since $c$ is coprime to $d$,
$$
 J_1+J_2\equiv d\pmod{c-d},\qquad J_1-J_2\equiv d\pmod{c+d}.
$$
These conditions use actual tiling of the lower polygon; area alone is
insufficient. Write $B_1,B_2$ for the signed numbers of $\rho$ steps
minus $-\rho$ steps in each of the two rotated hexagonal alphabets.
A displacement $(x_i,y_i)$ has $J_i=x_i+2y_i-3B_i$, by checking the
six basic directions. Use the displacement parameters in the first
section: $x_1=X,y_1=Y,x_2=x,y_2=y$, $X+x=a+b-vt$. Every step
contributes at most 1 to the first coordinate in its own alphabet, and
every vertical step contributes zero. Hence
$$
 |B_1|+|B_2|\le C=L-X-x=L-(a+b)+vt.
$$
It follows that if $L\le a+b$, then $t\ge0$, and
$$
 J_1-J_2=d+(2u+v)t-3(B_1-B_2)\ge d+2(u-v)t.
$$
Since $J_1-J_2\le L\le a+b<c+2d$ (the gap equals
$(2u+v)(u-3v)/g$), its congruence forces $J_1-J_2=d$ and $t=0$.
Then $C=0$, $L=a+b$, and each step is either $E$ or $S$ in its own
alphabet.

Use the equality displacement parametrization $x=Dj$, $m=Fj$,
$Y=-b+Fj$ with $F=(u-v)/g$, $D=(2u+v)/g$. Hence $0\le j\le b/F$.
Now $J_1+J_2=d-6vj/g$ and $c-d=3v(u+v)/g$, forcing $u+v\mid2j$.
The integer $u+v$ is odd and $b/F<u+v$ exactly because
$u^2-2uv-2v^2>0$, equivalent to $a>b$. Therefore $j=0$ and there
are no upper-alphabet steps. The middle steps then consist of $a$
copies of $E$ and $b$ copies of $S$.

The closed polygon is in the single lattice $czR$: $B/(cz)$ is
integral. Its area in units $\sqrt3/4$ is a multiple of $c^2$ by the
lattice determinant, so its positive tile count is a multiple of $c^2$
by $(ab,c)=1$. The word $E^aS^b$ uniquely maximizes the enclosed area
among all words of that inventory, as swapping an adjacent $SE$ to
$ES$ increases it by one fundamental parallelogram. The maximal triangle
has exactly $c^2$ tile areas. A genuine cut must attain that maximum.
This proves the stated equality and replacement claim.

There is a parity window above this minimum. If $e=L-a-b\ge0$, the
general projection deficit gives $t\ge-e/v$ and
$$
 J_1-J_2\ge d+2(u-v)t-3e\ge d-(2u/v+1)e.
$$
If $e<\min(c+a-3b,vF)$ both $-c<J_1-J_2<c+2d$ hold, so $J_1-J_2=d$
and $L$ is even. In particular for the residuals $u\ge6v$ this applies
whenever $0\le e<vF$: $(2u+v)(u-3v)>v(u-v)$. Every noncanonical
upper path is therefore at least $a+b+2$ edges long there, and all odd
excesses strictly below $vF$ are impossible.

For every residual $u\ge6v$, one can also determine all six *net signed*
inventories throughout $0\le e<2v$. They agree exactly with the
canonical word: the mixed upper alphabet has zero net count on each
axis, and middle counts differ only by cancelling pairs. Indeed inside
this range $e<vF$, so $3(B_1-B_2)=(2u+v)t$. From
$|B_1-B_2|\le e+vt$ one obtains $e\ge2(u-v)t/3$ if $t>0$,
and $e\ge(2u+4v)|t|/3$ if $t<0$. Thus $t=0$ and $B_1=B_2=B$.
We again have $x=Dj$, $m=Fj$, and now
$J_1+J_2=d-6vj/g-6B$. The first congruence implies
$v(u+v)\mid2(vj+gB)$. Since $v$ is odd and prime to $g$, $v\mid B$;
also $2|B|\le e<2v$ forces $B=0$. Hence $u+v\mid j$.
The two projection deficiencies imply $-e\le m\le b+e$.
For $u\ge6v$, $F(u+v)-b=(u^2-2uv-2v^2)/g>2v$, so the only such
multiple is $j=0$. Both the upper net displacement and its signed
vertical count vanish, forcing opposite upper step counts equal on
every axis. The middle alphabet has displacement $(a+b,-b)$ and zero
signed vertical count, as claimed. Every allowed word in this range
therefore has the canonical signed inventories with at most $v-1$
additional opposite pairs in total; placement of such pairs can still
change the geometry of the cut.

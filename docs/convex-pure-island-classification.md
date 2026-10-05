# Classification and chirality exchange for convex pure islands

5 October 2026. Denis Paliy, research with ChatGPT assistance.

This note gives a complete criterion for **convex pure all-long-edge
islands** of primitive integral 120-degree tiles. The necessity and
construction were checked separately and then audited together. This is
an auxiliary theorem; no solution of Erdős problem 634, external review,
or literature-priority claim is asserted.

## The theorem and its precise scope

Let positive integers $a,b,c$ satisfy
$$
\gcd(a,b,c)=1,\qquad c^2=a^2+ab+b^2.
$$
Use Eisenstein coordinates $(p,q)\leftrightarrow p+q\rho$, with
$\rho=e^{i\pi/3}$. Put
$$
u=(a+b,-b),\qquad w=(b,a)=\rho u,\qquad v=w-u.
$$
The reference tile is $R=\operatorname{conv}\{0,u,(a,0)\}$.
A *pure* tiling uses translates of the six rotations $\rho^jR$.
Its short edges have one direction class modulo $\pi/3$, and its
long edges have the distinct class of $u$. T-junctions are allowed.

**Theorem.** A positive-area convex polygon with edges parallel to
$u,w,v$ admits this pure tiling if and only if it is centrally
symmetric and each of its genuine side lengths is an integer multiple
of $abc$.

Equivalently, up to translation and a permitted rotation, its vertices are
$$
0, Xu, Xu+Yw, Xu+Yw+Zv, Yw+Zv, Zv,
\tag{1}
$$
where $X,Y,Z\in ab\mathbb Z_{\ge0}$ and at least two are positive.
Repeated vertices are omitted. Thus parallelograms are included.

**Chirality corollary.** Every such polygon has tilings in both pure
states, using the original unit tile and the same polygon. In particular,
every existing convex pure all-long-edge island can be replaced by the
opposite state without dilation.

The number of tiles is necessarily
$$
N=\frac{2c^2(XY+XZ+YZ)}{ab}.
\tag{2}
$$
The theorem does not assume that islands arising in an arbitrary
triangle tiling are convex or pure. Those properties require separate
proofs and are not supplied here.

## 1. Geometric reduction, including T-junctions

First, $\gcd(a,b)=1$. Also $a,b\ge3$: the cases 1 and 2 make
$b^2+b+1$ and $(b+1)^2+3$, respectively, fall strictly between
consecutive squares. The equality $a=b$ is impossible for an integral
norm triple.

Give a directed long edge of direction $\rho^ju$ the formal value
$(-1)^j$ times its length, and a directed short edge of direction
$\rho^j$ the value $(-1)^j z$ times its length. The reference
tile's counterclockwise boundary has value $c+(b-a)z$; rotation by
$\pi/3$ changes the sign. Subdivide all internal overlaps at their
endpoints. Cancellation of these directed pieces shows that the outer
boundary value is $S[c+(b-a)z]$ for an integer $S$. It has no
short-direction term. Since $a\ne b$, $S=0$, and the alternating
long-direction boundary sum is zero.

For a convex polygon write its six possible directed side lengths as
$\ell_0,\ldots,\ell_5$, using zero for an absent direction. Let
$d_j=\ell_j-\ell_{j+3}$, $j=0,1,2$. Vector closure gives
$d_0=d_2$, $d_1=-d_2$; the alternating sum gives
$d_0-d_1+d_2=0$. Hence all three differences vanish. The polygon is
centrally symmetric.

Every boundary side consists of whole long edges. Indeed, a long edge
on a supporting line of a convex polygon is entirely on its boundary;
the short directions cannot occur on that line. Thus the polygon has
form (1), initially with integral side counts $X,Y,Z$.

Every interior long edge matches one whole long edge on the opposite
side. To see this, take a maximal connected collinear union of long
edges on a line through the interior. Convexity ensures that the line
has no positive-length exterior boundary segment. Each side partitions
the same interval into entire edges of the same length $c$. Both
partitions start at its endpoint and therefore coincide. The two tiles
on a matched edge are half-turn copies of each other.

There is also one common translate of the integer short-direction
lattice containing every vertex. On a maximal short-edge chain, the
two sides partition the same interval by complete edges of integral
lengths $a,b$. Every endpoint differs from the first endpoint by an
integer multiple of that short-direction unit vector. Thus adjacency
across a short chain preserves the lattice coset. Adjacency across a
long edge preserves it by whole-edge matching. The positive-length
adjacency graph of the tiling is connected, so one coset propagates
throughout. Translate its origin to a polygon vertex.

The boundary triangle on each long-edge segment is uniquely determined
by the pure state and its inward side. Remove these triangles. Their
interiors cannot overlap in an actual tiling. All remaining tiles pair
along their long edges. The resulting, possibly disconnected or
nonconvex, core is tiled by three types of lattice parallelograms with
short side lengths $a,b$. No convexity of this core is assumed.

## 2. Exact boundary inventories

An upward elementary lattice triangle at $(i,j)$ has vertices
$(i,j),(i+1,j),(i,j+1)$. A downward one has vertices
$(i+1,j+1),(i+1,j),(i,j+1)$. Let $U(x,y),D(x,y)$ be the Laurent
polynomials counting these cells in the core, with weight $x^iy^j$.
Write $S_n(t)=1+t+\cdots+t^{n-1}$, including $S_0=0$.

The three paired-tile inventory vectors $(U,D)$ are
$$
g_0=y^{-1}(x,1)S_a(x)S_b(x/y),\quad
g_1=(1,1)S_b(x)S_a(y),\quad
g_2=x^{-1}(y,1)S_b(y)S_a(y/x).
\tag{3}
$$
A translation multiplies both entries by the same Laurent monomial.
The core inventory is a sum of such translated vectors.

Set
$$
q=x^{a+b}y^{-b},\qquad r=x^by^a,\qquad s=r/q=x^{-a}y^{a+b}.
$$
Boundary cancellation gives the following polynomial identities:
$$
\begin{aligned}
F:=U-D={}&y^{-1}S_b(x/y)S_X(q)(r^Ys^Z-x^a)\\
 &+x^{-a}y^{a-1}S_a(x/y)S_Z(s)(q^Xr^Y-y^b),\\
G:=U-xD={}&S_a(y)S_Y(r)(x^bs^Z-q^X)\\
 &+S_b(y)S_Z(s)(1-x^{-a}y^a q^Xr^Y).
\end{aligned}
\tag{4}
$$

Here is a direct way to verify every boundary term. For $F$, assign
the directed elementary edge $(i+1,j)\to(i,j+1)$ the value
$x^iy^j$, with the opposite sign on reversal, and assign zero to
the other two directions. Cell circulations are $x^iy^j$ and
$-x^iy^j$. For $G$, assign the vertical edge
$(i,j)\to(i,j+1)$ the value $-x^iy^j$, and the other directions
zero. Its cell circulations are $x^iy^j$ and $-x^{i+1}y^j$.

For a removed boundary triangle of rotations $0,\ldots,5$, its
reversed short-edge path contributes, before translating the triangle:
$$
\begin{array}{c|c|c}
j&F&G\\\hline
0&-x^ay^{-1}S_b(x/y)&0\\
1&0&-S_a(y)\\
2&x^{-a}y^{a-1}S_a(x/y)&-x^{-a}y^aS_b(y)\\
3&x^{-a-b}y^{b-1}S_b(x/y)&0\\
4&0&y^{-a}S_a(y)\\
5&-y^{-1}S_a(x/y)&x^ay^{-a-b}S_b(y)
\end{array}
$$
Multiply by the successive side-start characters
$1,q^X,q^Xr^Y,q^Xr^Ys^Z,r^Ys^Z,s^Z$, and sum along each side
using direction characters $q,r,s,q^{-1},r^{-1},s^{-1}$.
Combining opposite sides yields (4). Cancellation is on unit cells,
so no edge-to-edge assumption enters these identities.

## 3. First derivatives force divisibility of every side

Take any distinct nontrivial $a$-th roots $x,y$. Then $x/y$
is also a nontrivial $a$-th root. All three vectors (3) vanish.
With $D_x=x\partial_x$ and $D_y=y\partial_y$, their first
derivative vectors $(D_xU,D_yU,D_xD,D_yD)$ are scalar multiples of
$$
(x,0,1,0),\qquad(0,1,0,1),\qquad(-y,y,-1,1).
$$
Consequently the functional
$$
L=(y-1)(D_xU-xD_xD)+(y-x)(D_yU-D_yD)
$$
annihilates each tile and each translated tile. Translation derivatives
give no extra term because its zero-order inventory vanishes. Thus any
tileable core satisfies $U=D=0$ and
$$
(y-1)D_xG+(y-x)D_yF=0.
\tag{5}
$$

At these roots, $q=(x/y)^b,r=x^b,s=y^b$ are nontrivial since
$\gcd(a,b)=1$. Put $A=q^X,B=r^Y,C=s^Z$. Equation (4) at the
roots reduces to
$$
(1-A)(BC-1)=0,\qquad(1-C)(1-AB)=0.
\tag{6}
$$
Differentiate (4) **before** imposing the root relations. Using (6),
the left side of (5) simplifies to
$$
\begin{aligned}
J={}&bXA(BC-1)+(1-A)BC[aY+(a+b)Z]\\
 &-aZC(1-AB)+(1-C)AB[(a+b)X+bY].
\end{aligned}
\tag{7}
$$
For checking this differentiation, at the root
$D_yS_a(x/y)=a/(1-x/y)$, $D_xs=-as$, and $D_yq=-bq$.
The term $aS_Z(s)(AB-s)$ simplifies to $a(1-C)$ under (6) and
cancels the extra term from differentiating $x^{-a}$.

The four choices in (6) reduce (7) as follows:

| Case | Value of $J$ |
|---|---|
| $A=C=1$ | $(bX+aZ)(B-1)$ |
| $A=B=1$ | $(aX+bY)(1-C)$ |
| $B=C=1$ | $(aY+bZ)(1-A)$ |
| $BC=AB=1$ | $(a+b)(X+Y+Z)(1-A)$ |

Every real prefactor is strictly positive: at least two of $X,Y,Z$
are positive. Hence $J=0$ forces $A=B=C=1$.

For a primitive $a$-th root $\zeta$, choose first
$(x,y)=(\zeta,\zeta^2)$. This is valid since $a\ge3$;
$q=\zeta^{-b}$ and $r=\zeta^b$ are primitive, giving
$a\mid X,Y$. Interchange $x,y$: now $s=\zeta^b$ is
primitive, giving $a\mid Z$. This also handles even $a$;
$\zeta^2$ itself need not be primitive.

To obtain the other divisibility, put $u'=(a+b,-a)$. The affine
isometry
$$
T(p,q)=u'+(-p,p+q)
$$
maps $R$ to the canonical tile for swapped parameters $(b,a)$,
with vertices $u',0,(b,0)$. Its linear part reverses rotation, and
maps the three long-edge axes to those for the swapped tile. Their
side counts are only permuted: explicitly it maps
$u,w,v$ to $-u',w'-u',w'$, where $w'=(a,b)$.
Applying the established first-parameter argument to this actual
reflected tiling gives $b\mid X,Y,Z$. Coprimality proves
$$
\boxed{ab\mid X,\qquad ab\mid Y,\qquad ab\mid Z.}
\tag{8}
$$

## 4. A universal positive rhombus

We now construct a pure tiling of the rhombus with side vectors
$ab,u,ab,w$. This is a general construction, not a search result.

Define
$$
\pi(L_0,L_1,L_2)=(L_2-L_1,L_1-L_0),\qquad
U_0=(0,-b,a),\quad V_0=(-a,0,b).
$$
Then $\pi(U_0)=u,\pi(V_0)=w$, and the kernel of $\pi$ is
spanned by $(1,1,1)$. We build a surface with boundary
$0,U_0,U_0+V_0,V_0$, using coordinate-plane facets.

Write $L_0=-s,L_1=-t$, with $0\le s\le a,0\le t\le b$.
The lifted boundary heights are
$$
\begin{array}{c|c}
s=0&L_2=at/b\\
s=a&L_2=b+at/b\\
t=0&L_2=bs/a\\
t=b&L_2=a+bs/a.
\end{array}
\tag{9}
$$
For $0\le i<a,0\le j<b$, let
$$
H_{ij}=\max\!\left(\left\lceil\frac{b(i+1)}a\right\rceil,
                         \left\lceil\frac{a(j+1)}b\right\rceil\right).
\tag{10}
$$
Place a horizontal unit-square facet at height $H_{ij}$ over each
cell $[i,i+1]\times[j,j+1]$. Include the internal vertical facets
$$
\begin{array}{ll}
s=i:&j\le t\le j+1,\quad H_{i-1,j}\le L_2\le H_{ij},\quad1\le i<a,\\
t=j:&i\le s\le i+1,\quad H_{i,j-1}\le L_2\le H_{ij},\quad1\le j<b.
\end{array}
\tag{11}
$$
Add boundary facets joining the stepped surface to (9):
$$
\begin{array}{ll}
s=0:&at/b\le L_2\le H_{0j},\quad j\le t\le j+1,\\
s=a:&H_{a-1,j}\le L_2\le b+at/b,\quad j\le t\le j+1,\\
t=0:&bs/a\le L_2\le H_{i0},\quad i\le s\le i+1,\\
t=b:&H_{i,b-1}\le L_2\le a+bs/a,\quad i\le s\le i+1.
\end{array}
\tag{12}
$$
Omit zero-area facets.

All these intervals are nonnegative. The heights (10) increase in both
indices, proving this for (11) and the near boundary facets. For the
far ones it suffices that
$$
a<b(b-1),\qquad b<a(a-1).
\tag{13}
$$
Indeed
$\lceil a(j+1)/b\rceil\le\lfloor aj/b\rfloor+\lceil a/b\rceil+1
\le aj/b+b$, and the other term of $H_{a-1,j}$ is $b$.
The other far side follows by interchanging $a,b$.
At the two mixed corners $H_{a-1,0}=b,H_{0,b-1}=a$; at the other
corners the adjacent boundary facets have the same vertical edge.

Every integral norm triple satisfies (13). Write $c=a+k$, so
$0<k<b$ and
$a(2k-b)=b^2-k^2>0$. The integer $r=2k-b$ is positive, giving
$$
a=\frac{3b^2-2br-r^2}{4r}
 \le\frac{3b^2-2b-1}{4}<b(b-1).
$$
Swap $a,b$ for the other inequality.

Orient horizontal facets with normal $+e_2$, the $s$-constant
facets with $+e_0$, and the $t$-constant facets with $+e_1$.
Equations (11)--(12) make all internal oriented edges cancel, after
subdivision if needed. The only remaining boundary is the lifted
parallelogram (9). On every coordinate plane, $\pi$ preserves the
same orientation sign, since
$$
\pi(e_0)=(0,-1),\quad\pi(e_1)=(-1,1),\quad\pi(e_2)=(1,0).
$$
No positive-area facet collapses. Taking winding numbers at any point
off the finitely many projected edges, the sum of the positively
oriented facet indicators equals the indicator of
$\operatorname{conv}\{0,u,u+w,w\}$. Hence exactly one facet covers
each interior point and none covers an exterior point. The finite closed
facets cover their edges as well. This proves a positive partition,
including containment and absence of overlaps; no unproved injectivity
of the surface is being used.

Multiply the lifted coordinates by $M=ab$. Tile each facet using
the following rectangular grids in its free coordinates:

| Fixed coordinate | First grid spacing | Second grid spacing |
|---|---|---|
| $L_0$ | $L_1:b$ | $L_2:a$ |
| $L_1$ | $L_0:a$ | $L_2:b$ |
| $L_2$ | $L_0:b$ | $L_1:a$ |

The integral rectangle boundaries become grid lines. Split each grid
cell along the diagonal whose two free-coordinate increments have
opposite signs. The projected long diagonals, up to sign, are $u,w,v$.
The halves are exactly the six allowed rotations of $R$. For an
explicit check, the lower and upper halves of the cell based at zero
in the two increasing free coordinates are respectively:

| Fixed coordinate | Lower half | Upper half |
|---|---|---|
| $L_0$ | $\rho^3R+(a,0)$ | $R+(-b,b)$ |
| $L_1$ | $\rho R+(0,-a)$ | $\rho^4R+(b,0)$ |
| $L_2$ | $\rho^5R+(-a,a)$ | $\rho^2R+(0,-b)$ |

The boundary facets also tile exactly. On a fixed-$L_0$ facet, use
grid coordinates $p=L_1/b,q=L_2/a$. After multiplication by $ab$,
the oblique line in (9) becomes $p+q=0$ or $p+q=b^2$. The other
boundaries are integral grid lines. Therefore the line cuts a cell
only on its prescribed long diagonal. Keep a whole cell or its required
half. For fixed $L_1$, coordinates $p=L_0/a,q=L_2/b$ give
$p+q=0$ or $p+q=a^2$. Thus all clipped facets are filled by
the same unit tiles, with the same pure state. Different face grids
may form T-junctions; their geometric boundaries already agree.

The result is the required pure rhombus of side counts $(ab,ab)$,
with exactly $2c^2ab$ unit tiles. Reflecting it in a rhombus symmetry
axis yields its opposite-state tiling on the identical rhombus.

## 5. Complete sufficiency and same-polygon exchange

Let $X,Y,Z$ satisfy (8), and set $A=Xu,B=Yw,C=Zv$.
The zonogon (1) partitions into the following three parallelograms:
$$
\begin{aligned}
&\operatorname{conv}\{0,A,A+B,B\},\\
&\operatorname{conv}\{B,A+B,A+B+C,B+C\},\\
&\operatorname{conv}\{0,B,B+C,C\}.
\end{aligned}
$$
Zero-area pieces are omitted. Each side count of each piece is divisible
by $ab$; subdivide it into congruent rhombi with side counts
$(ab,ab)$. Rotations and translations of the construction in section 4
tile every such rhombus in the desired global pure state. Choosing the
reflected version in each gives the opposite global state. These are
fillings of the original polygon, not enlarged polygons. This proves
the theorem and the chirality corollary.

## Verification and remaining gap to problem 634

The [reproducibility folder](../research/pure-convex-islands/README.md)
contains standard-library-only integer checks. Independent cell
enumeration verifies the boundary formulas and both first derivatives;
cyclotomic remainders check the first-derivative identities, all four
phase cases, and an even parameter. A separately implemented facet
generator verifies exact containment, pairwise nonoverlap, area and
grid compatibility for three different norm triples. These checks
supplement the general proof; finite tests are not its logical basis.

The earlier open **convex pure-island exchange question is resolved by
this theorem**. General orientation-cut regions may be nonconvex, have
holes, or contain both inward triangles and outward paired blocks.
Convexity was essential in the whole-long-edge matching step. Neither
a decomposition of every such region into the present convex islands
nor a replacement theorem for those broader regions follows here.
Moreover, the full all-count classification in Erdős 634 contains other
tile/target branches. This note does not close those remaining steps.

More specifically, an extremal contact component can include inward tiles
(short edges at level $H$, long edge at $H-1$) and outward tiles
(short edges at $H-1$, long edge at $H$). Taking only the inward
tiles can leave short-direction boundary contacts; taking all top contacts
can give a mixed component. Even pure all-long-edge unions can be nonconvex
(an L-shaped union of three constructed rhombi is an example). A geometric
cut into convex pieces is insufficient if it cuts existing unit tiles;
one needs an inherited tiling or another independently proved filling.
The principal lattice argument in `height-cut-area.md` also concerns the
separate Group-1 angle family, not just the 120-degree family treated here.

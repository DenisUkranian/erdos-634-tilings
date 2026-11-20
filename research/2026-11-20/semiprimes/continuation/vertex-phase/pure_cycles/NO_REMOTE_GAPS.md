# Ordered boundary words exclude supported pure-mesh cycles

This is the supported-cycle portion of the project's earlier
ordered-boundary argument, restored here with its exact rational checker.
Additional middle-path and all-parameter claims from the working note
are not used in this package. Its new consequence for individual
phase nodes is proved in [No vacant phase ancestor](../NO_PHASE_GAPS.md).

Let the primitive odd F2 tile have short sides $a>b$, long side $c$, and
$c^2=a^2+ab+b^2$. Write $p=a+2b$, $q=2a+b$, $N=pq$, $\rho=e^{i\pi/3}$
and $z=(a+b\rho)/c$. In the standard board frame a side in direction
$z^h\rho^j$ has height $h$. A tile's reported height is the common
height of its two short sides. A supported cycle is a simple polygonal
loop in the tile skeleton, on one translate of a triangular mesh of
step $c$, composed of edges in that mesh.

**Theorem.** Neither the 3431 board $(a,b,c)=(33,7,37)$ nor the
5063 board $(35,13,43)$ has a supported cycle in any tiling.
Consequently no interior height $k\le0$ or $k\ge3$ can be missing
between occupied short heights. The only possible missing interior
height is 1.

The [supported-cycle and gap theorem](../../cycles/CYCLES.md) shows that a remote gap
forces such a cycle. We recall an independent area check. A polygon of
the triangular mesh encloses an integer number of elementary cells of
physical area $c^2\sqrt3/4$. Each tile has area $ab\sqrt3/4$ and
$\gcd(ab,c)=1$. Thus its tile count $m$ is a multiple of $c^2$ and
$m\le N=3c^2-(a-b)^2<3c^2$.

To rule out $m=c^2$, assign the two weights $(-1)^jL$ and
$(-1)^{j+h}L$ to a directed segment of length $L$ in heading $z^h\rho^j$.
The two sums around a counterclockwise tile of short height $h$ are
$(d-c)\epsilon$ and $(d+c)(-1)^h\epsilon$, with $d=a-b$ and
$\epsilon=\pm1$. This follows from the directed side relation below
and its reflection. Summing over the tiles cancels all internal edges.
On the pure mesh boundary of height $k$, the two totals are $cM$ and
$(-1)^k cM$ for an integer $M$. The odd integers $c-d,c+d$ are coprime,
since $d$ is even and $\gcd(c,d)=1$, and both are coprime to $c$.
Their product is $c^2-d^2=3ab$. Thus $M=3ab\,r$ for an integer $r$.
The first tile-sign sum has absolute value $c(c+d)|r|$ and parity
$m$. If $m=c^2$ then $r$ is odd, and this absolute value exceeds $m$,
a contradiction. Therefore $m=2c^2$. In units of mesh rhombi of
physical area $c^2\sqrt3/2$, the cycle must enclose **$ab$**.

## Ordered words

The [earlier tile-group note](../../../../../final-push-oct7/duality/NONCOMMUTATIVE_BOUNDARY.md)
gives the unit-segment presentation and its disk interpretation.
Here we use a free product of three cyclic groups of order $a$, with
generators $X_0,X_1,X_2$, extended by $X_{i+3}=X_i^{-1}$ and
period six. Put $s=bc^{-1}\pmod a$, so $s^2=1\pmod a$.
A directed physical unit segment $z^h\rho^j$ receives
$X_{j+h}^{s^h}$. The side of length $a$ gives the identity.
For the direct hand the other two side words agree in the positive
vector equation

$$
  a z^h\rho^j + b z^h\rho^{j+1}=c z^{h+1}\rho^j
$$

since $b=cs\pmod a$. For the reflected hand use $j-1,h-1$ and
$s^{-1}=s$. Thus every tile has trivial boundary word.

On each maximal connected run of collinear sides, its banks partition
the run into full sides of integer length. Consequently all endpoints
on both banks lie at integer distances from the start of that run.
Insert common unit vertices. The product around the boundary of a tiled
disk is trivial, by the disk diagram of its elementary face loops
with opposite labels on opposite traversals of each shared edge. Nonstraight
corners on a supported simple polygon are actual tile vertices. Intermediate
collinear mesh marks do not affect the word, because the total length
of each straight boundary segment is a multiple of $c$. This argument
permits reflections and T-junctions.

On a pure mesh at height $h$, the power $cs^h$ per mesh step is a
unit modulo $a$. Renumber the generators by the fixed rotation, invert
them as needed and apply the same exponent automorphism in the three
factors. Each mesh step then has its ordinary axis letter or its inverse.
In particular its ordered boundary word is trivial in $C_a*C_a*C_a$.

## A cylinder test for a pure triangular mesh

Let the board have mesh-unit diameter strictly less than $\sqrt3 a$.
Assume at most one of the three unoriented mesh axes admits a length-$a$
chord in the board. Choose that axis as the horizontal $e_0$. If there
is none, choose any axis. A chord here means a displacement of two
points of the board. It need not lie on a tile edge.

Take the ordered unit-step word of a supported cycle. Repeatedly delete
an adjacent inverse pair or a consecutive block of $a$ identical
horizontal letters of either sign. In the cylinder obtained by identifying
points differing by $a e_0$, each inverse deletion retraces one edge,
and each horizontal deletion traverses one entire horizontal circle.
Each deletion has displacement in $a\mathbb Z e_0$ in the original plane.

Suppose a nonempty word remains after these deletions cease. Write it
in maximal same-axis runs. Each run has one sign, since inverse pairs
have been removed. Adjacent runs have different axes, and every horizontal
run has nonzero exponent modulo $a$. By the reduced-word theorem
for free products, triviality in $C_a*C_a*C_a$ requires a nonhorizontal
run of exponent divisible by $a$. Take $a$ of its consecutive letters.
The two endpoints of that subword lift to two vertices of the original
path whose difference is $a(\pm e_i+n e_0)$ for $n\in\mathbb Z$,
where $e_i$ is a nonhorizontal mesh axis. Each intervening deleted
subword has displacement in $a\mathbb Z e_0$.
The squared mesh norm of $\pm e_i+n e_0$ is $n^2\pm n+1$.
It equals 1 or is at least 3. The latter is impossible by the diameter,
and in the former case the chord has length $a$ in a nonhorizontal
mesh direction. This contradicts the unique-axis assumption.
The original word thus deletes to the empty word using only the two
stated operations.

As an oriented edge chain on the cylinder, the projected cycle is
therefore a sum of horizontal circles. All nonhorizontal oriented edges
cancel exactly there. Use axial coordinates $x,y$ in the mesh
basis $e_0,\rho e_0$. For each $y$ strictly between the extreme
$y$-coordinates of the simple polygon and different from every vertex
height, sum the indicators of its interior over all horizontal translates
by $a$. This $a$-periodic function of $x$ has no jump. The crossings
of nonhorizontal edges cancel with their opposite crossings on the
cylinder, and there is no horizontal edge on this level. It is constant
away from finitely many points. Its integral over one period is the
total horizontal length of the polygon's slice. The interior is connected
and projects onto the full open interval between its extreme heights,
so the slice has positive length. It is at most the board diameter,
strictly less than $2a$. Its length must consequently be **exactly $a$**.
This allows a slice with several disjoint intervals.

The area measure in units of mesh rhombi is $dx\,dy$. Integrating proves
that an enclosed area of $ab$ would require a **$y$-span equal to $b$**,
with a horizontal board chord of length at least $a$ on almost every
level in that span.

## Exact board geometry

Rotate the board's 60-degree corner to describe it by axial vertices
$(0,0),(A,0),(0,B)$, where $A=ap/c$, $B=bq/c$. Its third side has
length $c$. Its diameter on both controls is $A<\sqrt3 a$.
In these particular coordinates its difference body is the hexagon

$$
 D=\{(x,y): |x|\le A,\ |y|\le B,\ |Bx+Ay|\le AB\}.
$$

This follows by taking the convex hull of the six directed
side displacements. If two different mesh axes supported length-$a$
chords, then $D\cap\rho^{-1}D$ would contain a vector of length $a$.
Choose the signs and order of the two axes so they differ by $60^\circ$.
The maximum of the squared norm $x^2+xy+y^2$ in this intersection
occurs at a vertex. The [exact checker](check_remote_cycles.py) enumerates
all feasible intersections of the twelve supporting lines, using rational
arithmetic.

| Board | Maximum squared norm in $D\cap\rho^{-1}D$ | $a^2$ |
|---|---:|---:|
| 3431 | $1331780030161/3293267769$ | 1089 |
| 5063 | $9230010672961/8428158025$ | 1225 |

Both maxima are smaller than $a^2$. This proves the one-axis hypothesis
simultaneously at every mesh rotation.

There are also direct bounds without enumerating vertices. Put $t=x+y$.
On both boards $|t|,|y|\le B$, so $x^2+xy+y^2=t^2-ty+y^2\le3B^2$.
This is already below $33^2$ at 3431. At 5063, when $t,y$ have the
same sign the norm is at most $B^2$. Otherwise reverse the vector
if necessary to write $t=r\ge0$, $y=-s\le0$. The rotated-body
inequality $|Ax+(A-B)y|\le AB$ gives $0\le r\le B-(B/A)s$,
with $0\le s\le B$. The norm $r^2+rs+s^2$ increases in $r$
and on the upper edge is a convex quadratic in $s$. Its maximum is
bounded by the larger of its endpoint values at $s=0,B$.
Here $B/A=1079/2135>1/2$, so this maximum is at most $7B^2/4$.
Since $B=1079/43<26$, it is below $1183<35^2$.

Return to the axial frame with the distinguished mesh direction
horizontal. Let $M$ be the maximum horizontal chord length of the
triangle and $H$ its full $y$-span. The cross-sectional lengths
are linear from zero to the maximum and back to zero, allowing the
maximum along a horizontal side at an endpoint. Hence $MH=AB$ by
area. If $M\ge a$, the $y$-span on which chords of length at least
$a$ are available is exactly

$$
  H(1-a/M)=AB(M-a)/M^2 \ \le\ B(1-a/A).
$$

The inequality follows from $M\le A<2a$ and monotonicity on
$[a,2a]$. If $M<a$ there are no such chords. The upper bounds are
$5110/1739<7$ and $19422/2623<13$, respectively. More generally
$B(1-a/A)<b$ follows from $1/p+1/q>1/c$, since $p,q<2c$.
The required span $b$ is unavailable. This excludes the cycle and
therefore excludes every remote gap on the two boards.

# Every whole-board tiling must leave triangles outside parallelogram pairs

Fix an arbitrary tiling of the original odd unit F2 triangle. No cycle,
corner patches, height gap or restriction on tile directions is assumed.
Select any disjoint pairs of tiles that form parallelograms along their
common complete side. The following theorem concerns how many triangles
remain outside the selected pairs.

Define $D_a$ using $\lambda=b/c\bmod a$ by
$$
 D_a=\min\{|x|+|y|:x+\lambda y\equiv b\pmod a\},
$$
and define $D_b$ by interchanging $a,b$. Division denotes modular
inversion. The two quantities have the exact elementary formula below.

* If the shared edge in each pair is $b$ or $c$, at least $2D_a+1$
  triangles remain.
* If it is $a$ or $c$, at least $2D_b+1$ triangles remain.
* In particular for pairs along the long edge $c$, at least
  **$2\max(D_a,D_b)+1$** triangles remain, including when all tile
  orientations and T-junctions are permitted.

| Unit count | $(a,b,c)$ | $D_a$ | $D_b$ | Triangles outside any such long-edge pairing, at least |
|---:|---:|---:|---:|---:|
| 3431 | (33,7,37) | 4 | 2 | 9 |
| 5063 | (35,13,43) | 3 | 4 | 9 |
| 64367 | (161,15,169) | 8 | 4 | 17 |

The [stronger whole-board bound for pairs exclusively along the long edge](LONG_EDGE_PAIRS.md) gives 97, 129 and 385 on these three controls. The modular bounds above also apply to the indicated mixed choices of shared sides. These are lower bounds, without a claim of attainability. They strengthen
the single leftover forced by parity. They apply on boards for which the
existence of any tiling is still unknown.

## Two disjoint orientation cuts on a torus

In the base frame write $R=\mathbb Z[\rho]$, $\rho=e^{i\pi/3}$ and
$z=(a+b\rho)/c$. In a tiling a direction of height $h$ is $\rho^jz^h$;
a tile's $a,b$ edges have the same short height, and its $c$ edge has a
neighboring height. These standard full-board facts and the two thresholds
are reviewed in [TWO_PATHS.md](../paths/TWO_PATHS.md). Choose a power
$L$ of $c$ so all unit directions of this finite tiling belong to $L^{-1}R$.
Project points onto the real torus $\mathbb C/((a/L)R)$. Every actual
$a$-edge now has coincident endpoints, regardless of its direction.

For threshold $k=0$ or $1$, retain the CCW edges of height greater than
$k$ and take their directed endpoint measure on the torus (end minus
start). The measure is additive across partial contacts because endpoints
introduced by splitting an interval cancel. On the full board, the
retained outer edges form the arc $B\to C\to O$, so its measure is
$[O]-[B]$, where $B=c^2$, $O=0$. These torus points are distinct since
$\gcd(c,a)=1$.

Each allowed parallelogram has an $a$-side. Its $a$-sides individually
have zero endpoint measure. Its other two sides have equal height and
are opposite translates by an $a$-vector, hence contribute zero together
for either threshold. On a single remaining triangle the $a$-edge also
contributes zero. The endpoint measures of its $b$- and $c$-edges are
opposites because the full boundary is closed. Unless their heights
straddle the chosen threshold, its contribution is zero. A contributing
tile therefore supplies one directed torus edge, with displacement equal
up to sign to its $b$-edge. Its short height is $k$ or $k+1$.

The finite directed graph of these edges has total endpoint measure
$[O]-[B]$. It contains a path from $B$ to $O$. To lower-bound its length,
scale displacements by $L$ and reduce both axial coordinates modulo $a$.
The scaled displacements are integral and the periods become $aR$;
this argument needs no integrality assumption on intermediate points.
Denominators that are powers of $c$ are invertible modulo $a$. We have
$z\equiv\lambda\rho$ and $\lambda^2=1\pmod a$ by $c^2\equiv b^2$.
After dividing by $Lb$ modulo $a$, every step has first axial coordinate
in $\{0,\pm1,\pm\lambda\}$, since unit Eisenstein directions have first
coordinate $0,1$ or $-1$. The total first coordinate is
$-c^2/b\equiv-b\pmod a$. Thus there are at least $D_a$ distinct tiles
for this cut. No single tile straddles both thresholds; the two ends
of its $b$-to-$c$ height change are consecutive. There are at least
$2D_a$ unpaired triangles, and oddness of $N$ raises the bound to
$2D_a+1$.

For the second bound project instead by $(b/L)R$. Each $b$-edge vanishes,
the other two endpoint measures on a triangle are opposite, and
$z\equiv a/c\pmod b$, with $(a/c)^2=1\pmod b$. The same two outer arcs
and the two consecutive height cuts give the stated $D_b$ result. In an
arbitrary family of parallelogram pairs with shared-side counts $P_a,P_b,P_c$
and $U$ unpaired tiles, the same reasoning gives
$U+2P_a\ge 2D_a+1$ and $U+2P_b\ge 2D_b+1$.

## Exact arithmetic and a growing lower bound

Put $m=a$, $v_0=b$ and $s=\gcd(m,c-v_0)$, $t=\gcd(m,c+v_0)$.
The odd coprime integers $s,t$ have product $m$ since $m\mid c^2-v_0^2$
and $\gcd(m,2c)=1$. The involution $\lambda$ is $+1$ modulo $s$ and
$-1$ modulo $t$. Setting $X=x+y$, $Y=x-y$, the congruence becomes
$X\equiv v_0\pmod s$, $Y\equiv v_0\pmod t$ with $X,Y$ of the same
parity. Also $|x|+|y|=\max(|X|,|Y|)$. For parity $e=0,1$ let $d_e(m')$
be the least absolute integer of that parity congruent to $v_0$ modulo
$m'$. Then $D_a=\min_e\max(d_e(s),d_e(t))$. Interchange $a,b$ to obtain
$D_b$. The [replay](check_pairs.py) compares the formula with shortest
paths on the residue graph for bounded parameters.

For the standard primitive parameters $u,v$ and $g=\gcd(3,u-v)$ write
$ga=u^2-v^2$, $gb=v(2u+v)$, $gc=u^2+uv+v^2$. If $g=3$, then
$t=u+v$ and $s=(u-v)/3$: indeed $c-b=u(u-v)/3$ and
$\gcd(u,u+v)=1$. The required $Y$ satisfies
$3Y\equiv-v^2\pmod{u+v}$. Since $3\nmid v$, the integer
$3Y+v^2$ cannot vanish. Consequently
$$ D_a\ \ge\ \left\lceil\frac{u+v-v^2}{3}\right\rceil . $$
For fixed $v$ this grows linearly with $u$. The statement is conditional
on tiling at the specified parameters; it makes no assertion of infinitely
many prime pairs. For example at $v=1$, $u\equiv4\pmod6$, write
$u=6h+4$ ($h\ge0$). Then $s=2h+1$, $t=6h+5$, $b=4h+3$.
The nearest $Y\equiv b\pmod t$ is $-(2h+2)$. An even $X$ can be
chosen as $-2h$ (it is 1 modulo $2h+1$). Thus $D_a=2h+2=(u+2)/3$,
and at least $(2u+7)/3$ triangles lie outside any pairing along $b$ or
$c$ on these whole boards.

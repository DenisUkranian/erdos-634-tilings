# What one triangular tile can do

Fix the shape and size of a triangular tile. Let the outside triangle have any shape and size. Which numbers of tiles can occur?

**Theorem.** There is a finite list of positive integers $C_1,\ldots,C_q$, depending on the tile, such that the possible counts are exactly

$$
\left(\bigcup_{i=1}^q\{C_i k^2:k=1,2,\ldots\}\right)\setminus F_T
$$

for some finite set $F_T$. For a fixed outside shape there are at most three families. If the side ratios of the tile are rational, there is at most one family for each outside shape. Reflections and T-junctions are allowed.

For example, when both shapes are right isosceles, the counts are exactly $k^2$ and $2k^2$. One copy and two copies give the first examples. Subdivision gives every member of both families. The side-length argument below rules out any others.

The geometric idea is to reuse two tilings as larger building blocks. Fill the middle of each large triangle with blocks of the first size. Adjust the dividing lines so the spaces around the corners can all be filled with blocks of the second size. This works at **every** sufficiently large multiple of the two scales’ greatest common divisor.

## Building any large scale from two tilings

Suppose copies of the same physical tile fill $dmB$ and $dnB$, where $B$ is a triangle, $d>0$, and $m,n$ are coprime positive integers. Relabel the sizes so that $m\le n$. Then the same tile fills $dkB$ for every integer

$$
k\ge 20m^2 n=20mn\min(m,n).
$$

If $m=1$, ordinary subdivision gives every $k\ge1$. The displayed bound is sufficient. In particular it gives no prediction about the first scale at which a tiling exists.

Use affine coordinates along two sides of $dB$. Its model is $D_1$, where $D_h$ has vertices $(0,0),(h,0),(0,h)$. A translate of $D_m$ or $-D_m$ becomes a translate or a half-turn of the actual board $dmB$. Thus substituting the given tilings preserves the physical tile.

**1. Make room for the corners.** Put $M=mn$. Choose the largest integer $H$ with $mH\le k$ and $mH\equiv k\pmod n$. Coprimality gives $0\le k-mH<M$ and $H>20M-n\ge19M$. Subdivide $D_{mH}$ into $m^2$ triangles of side $H$ on the lines $x=iH$, $y=jH$, $x+y=hH$. We will move the diagonal boundary to $x+y=k$. Each edge of the subdivision gets its own shifted supporting line. Its two incident triangles use the same shift.

**2. Choose the lines.** At a coarse vertex $(iH,jH)$ put $w=ki\pmod m$ if $i+j=m$, and $w=0$ elsewhere. Assign a desired level modulo $m$ to each edge as follows.

| Supporting line | Desired level modulo $m$ |
|---|---|
| Vertical, $x=X$ | $w(\mathrm{bottom})-w(\mathrm{top})$ |
| Horizontal, $y=Y$ | $w(\mathrm{right})-w(\mathrm{left})$ |
| Diagonal, $x+y=Z$ | $w(\mathrm{lower\ right})-w(\mathrm{upper\ left})$ |

These differences telescope around either orientation of a coarse triangle, so $X+Y\equiv Z\pmod m$. Given the original level $L_0$, choose the unique integer in $[L_0,L_0+M)$ equal to $L_0$ modulo $n$ and equal to the desired residue modulo $m$. This is the Chinese remainder theorem. Both axis boundaries stay fixed. Along the outer diagonal every desired residue is $k\bmod m$, so its shifted level is exactly $k$.

**3. Fill the middles.** The three new lines of each cell form a triangle on a translated grid of step $m$, since $X+Y\equiv Z\pmod m$. The side is greater than $H-3M$. Cut a corner triangle of side $5M$ off each vertex. The remaining hexagon is a union of elementary $m$-triangles. Because the line shifts and the cut size are multiples of $n$, the exposed edges around each old vertex lie on one common grid of step $n$. Fill each corner region with its elementary $n$-triangles.

<details>
<summary>Why the hexagons and corner fillings cover the board exactly</summary>

Measure distance by $\|(x,y)\|=\max(|x|,|y|,|x+y|)$. The three inward slacks $a,b,c$ of a coarse triangle are signed distances in support levels and sum to $H$. Shifting a line changes its slack by less than $M$. A point is in the central hexagon exactly when the three shifted slacks are nonnegative and each pair sums to at least $5M$.

Within distance $2M$ of a coarse vertex, both slacks through that vertex have old sum of absolute value at most $2M$, so their shifted sum is less than $4M$. No incident hexagon reaches this neighborhood. A nonincident cell has a slack at most $-H$ at the vertex and cannot reach it either.

Away from those neighborhoods at most one coarse grid line is within $M$ in level. Two nonparallel such lines would put their intersection within distance $2M$, and parallel levels differ by $H$. If there is no close line, all half-plane signs stay fixed. If there is one close line, project to it by a displacement of norm at most $M$. No other coarse line is crossed. The two possible cells are the ones sharing the projected edge, and they use opposite sides of the same shifted line. On the outer boundary the inward side is exactly the corresponding half-plane of $D_k$. Equivalently this sign test can be applied in the full planar coarse grid, retaining only the cells of the board. An exterior coarse vertex violates an old board inequality by at least $H$, so lies farther than $9M$ from the new board. This proves containment and disjoint interiors for the hexagons.

Outside distance $9M$ from every coarse vertex the hexagons already cover $D_k$. Indeed the sign test gives a triangle containing the point before clipping. If a corner cut fails, two old slacks satisfy $a,b\ge-M$ and $a+b<7M$. The distance to their old vertex is $\max(|a|,|b|,|a+b|)<8M$.

The closed neighborhoods of radius $9M$ are disjoint since $H>18M$. In a neighborhood about $v$, only incident cells can contribute. In each, the far support and the other two cuts are at level distance at least $H-5M-2M>9M$ from $v$. The remaining two supports, the nearby cut, the relevant outer boundaries and the six walls of the neighborhood all lie on the grid translated by $v$ with step $n$. The complement there is therefore tiled by whole elementary $n$-triangles. Taking their closures also covers every boundary point. This proves the construction for arbitrary $k$ in the stated range.

</details>

To see a direct example, take $m=2$, $n=3$, $k=241$. The construction gives 11,827 blocks of size 2 and 1,197 of size 3. Two programs starting from the three sizes check the same dissection. One tests area, containment and disjointness. The other reconstructs the corner fillings from their oriented boundaries. [Area check](verify_two_scale.py) · [Boundary check](verify_gluing_boundaries.py) · [Exact counts for 13 examples](gluing_boundaries.json).

~~~sh
python3 research/2026-11-19/structural/verify_two_scale.py 2 3 --target 241
python3 research/2026-11-19/structural/verify_gluing_boundaries.py 2 3 241
~~~

## Why the counts are square families

**Integer scales.** For fixed physical $B,T$, let $S$ consist of the positive integers $s$ for which $sB$ is tiled by copies of $T$. If $S$ is nonempty, it contains all sufficiently large multiples of $g=\gcd(S)$, and every member is divisible by $g$.

Choose finitely many attained scales with gcd $g$, adjoining one scale whenever it decreases the current gcd. For the first scale, subdividing gives every positive multiple. Suppose all sufficiently large multiples of $h$ are attained and $u$ is the next scale. Choose $t$ large with $t\equiv1\pmod u$. Then $ht,u$ are attained and $\gcd(ht,u)=\gcd(h,u)$. The two-size construction supplies every large multiple of this new gcd. This proves the claim by induction.

Write $A,a$ for the areas of $B,T$. The counts at integer dilates are all $Ck^2$ with just finitely many omissions, where $C=g^2 A/a$ is a positive integer. Indeed finitely many attained scales $gk_i$ have $\gcd_i k_i=1$. All $Ck_i^2$ are integers and $\gcd_i k_i^2=1$, so Bézout's identity gives $C\in\mathbb Z$.

**All real scales for a fixed outside shape.** Choose a side of $B$ of length $L$. It is tiled along its full length by whole tile edges. Two such edges cannot overlap on an open interval, since both tile interiors would lie on its inward side. Let $\ell_1,\ell_2,\ell_3$ be the tile side lengths. For a count $N$, comparison of areas fixes the outside scale at $\sqrt{Na/A}$. For some nonnegative integers $n_i$ this gives

$$
\sqrt N=\frac{\sqrt{A/a}}{L}(n_1\ell_1+n_2\ell_2+n_3\ell_3).
$$

Thus for every occurring squarefree part $d$ of $N$, the number $\sqrt d$ lies in a single rational vector space of dimension $r=\dim_{\mathbb Q}\operatorname{span}_{\mathbb Q}(\ell_1,\ell_2,\ell_3)\le3$. The square roots of distinct positive squarefree integers, including $1$, are rationally linearly independent. Hence at most $r$ different $d$ occur. For one such $d$, take $\sqrt{da/A}\,B$ as reference board. Counts $dt^2$ now correspond exactly to its attainable integer scales $t$. The preceding argument shows that these counts form a family $d\,g_d^2 k^2$ with finitely many omissions. [Independence of squarefree radicals](https://kam.mff.cuni.cz/~klazar/tomek_pr.pdf).

**Allowing the outside shape to vary.** At any outside corner, all incident tiles have a vertex there, since a tile edge meeting the corner in its relative interior would occupy an angle of at least $\pi$. Therefore each outside angle is a sum of tile angles. If the smallest tile angle is $\delta$ and $J=\lceil\pi/\delta\rceil-1$, there are at most $\binom{J+3}{3}$ such sums, counting nonnegative triples of total at most $J$. Two angles determine the shape. Applying the fixed-shape result to this finite list proves the theorem with $q\le r\binom{J+3}{3}^2$. A finite union of finite sets of omissions stays finite.

**Counting consequence.** The number of admissible counts up to $X$ for this one tile is $\kappa_T\sqrt X+O_T(1)$. Group the coefficients as $C_i=d g_i^2$ by squarefree $d$. Within each group the allowed multipliers, apart from finitely many omissions, are the integers divisible by one of the $g_i$. They are periodic modulo their least common multiple and have rational density $\rho_d$. Summing up to $\sqrt{X/d}$ gives $\kappa_T=\sum_d\rho_d/\sqrt d$. Every square occurs by subdivision of the tile itself, so $\kappa_T\ge1$.

The coefficients and early exceptions may change with the tile. Determining the union over all tiles remains the open part of Erdős 634. The project supplies a mathematical proof and exact checks of sample constructions. Independent scholarly review is pending.

# Which regular-grid patches can change their directions?

Let the primitive scalene tile have positive integer sides $a>b$, $c^2=a^2+ab+b^2$, and $\gcd(a,b)=1$. Put $p=a+2b$, $q=2a+b$, $N=pq$. In the axial basis $1,\rho=e^{i\pi/3}$ the F2 board has vertices $0,H,V\rho$ with $H=bq$, $V=ap$. A regular grid is the full triangular tessellation obtained by translating the two triangles of a parallelogram cut along its tile diagonal. Each of its three families of parallel sides has a fixed unit segment length, one of $a,b,c$. A patch can have holes or a nonconvex boundary. The tiles outside a patch can have any directions or T-junctions.

## The elementary switch is complete for two regular grids

Choose two tile sides $x,y$ and use their two supporting directions. A rhombus with sides $\ell=\operatorname{lcm}(x,y)=xy$ in those directions has two grid fillings related by reflection in a rhombus diagonal. One assigns lengths $x,y$ to the two directions; the other assigns $y,x$. Each filling has $2xy$ tiles. The suitable diagonal in each cell follows from the third side length. Pairwise coprimality follows from the norm and primitivity.

Conversely, suppose two complete regular grids have a common finite region of positive area made of whole tiles of each. Every boundary edge lies on a common grid direction. A bounded positive-area polygon needs at least two directions. Three shared directions determine the same tile-side assignment: the three acute angles between unoriented lines are $\alpha,\beta,60^\circ$, where $\alpha+\beta=60^\circ$ and $\alpha\ne\beta$. A line can be recognized by the two angles it makes with the others. At a boundary turn both grids have a vertex, so aligning this vertex aligns the two tessellations. This also rules out a translated equal-heading trade. If exactly two directions are shared, their angle identifies the same unordered side pair $x,y$ in both grids. Identical assignments to the two lines would give the same vertex lattice and diagonal, since the two diagonals have different lengths. Hence the lengths are exchanged.

Choose any common boundary turn as origin. In unit vectors $e,f$ of the two shared lines the two vertex lattices are $x\mathbb Ze+y\mathbb Zf$ and $y\mathbb Ze+x\mathbb Zf$. Any two distinct edge steps of a triangular grid form a basis of its vertex lattice. The common lattice is exactly $\ell\mathbb Ze+\ell\mathbb Zf$. Every turn on every boundary component lies in this one lattice, including turns on holes. Thus the common region is a union of its elementary rhombi. Each constituent rhombus can be switched separately. A scaled triangular seed grid of order $n$ admits such a switch involving sides $x,y$ if and only if $n\ge x+y$: in coordinates of these original sides the seed is $i,j\ge0$, $i+j\le n$, and one switch occupies a $y$-by-$x$ rectangle. Therefore none of the three seed grids of orders $a,b,c$ in the incenter construction admits an internal switch to one other regular tessellation, since $a+b>c$.

## Every F2 board excludes double thickness

No rhombus of twice the elementary side length $2xy$ fits in the original board, under any rigid motion. Thus an exchange region between regular grids can never contain a $2$-by-$2$ block of elementary rhombi.

Here is a short justification for minimizing over every rotation. In normalized board coordinates $(X,Y)=(x/H,y/V)$ the triangle is $X,Y\ge0$, $X+Y\le1$. For a centrally symmetric parallelogram centered at 0, the least scale of this board containing a translate is
$$
h(X)+h(Y)+h(X+Y),
$$
where $h(L)$ is the maximum of the linear functional $L$ on the parallelogram. Indeed translate its two coordinate minima to zero. For half-edge vectors $u,v$, $h(L)=|L(u)|+|L(v)|$. As both vectors rotate together in the physical Euclidean plane, the displayed sum is positive and satisfies $f''=-f$ between zeros of the six linear functionals evaluated on the rotated half-edges. Its minimum is attained at a zero. There an edge of the parallelogram is parallel to a side of the board. This argument covers all real rotations and both reflected orientations.

Write $s$ for the aligned board side. The board altitude is $abN\sin(60^\circ)/s$. The altitude of the proposed rhombus relative to either of its edges is $2xy\sin\angle(x,y)=2ab\sin(60^\circ)$. Cross-sections parallel to $s$ shrink linearly, so a necessary inequality at this orientation is
$$
\frac{2xy}{s}+\frac{2s}{N}\le1 .
$$
Since $xy\ge ab$, for $s=ap$ and $s=bq$ the left hand side is at least $2b/p+2a/q>1$. The last inequality follows from $2q>p$. For $s=c^2$ it is at least $2ab/c^2+2c^2/N>1$, because $N-2c^2=3ab$ and $2N-3c^2=a^2+7ab+b^2>0$. This proves the exclusion.

For $a\ge2b$ even a **single** switch exchanging the sides $a,c$ is too large. Its area is $2ac$ tile units and $4ac>N$: use $c>a+b/2$ and $(2a+b)(a-2b)\ge0$. Every parallelogram inside a triangle occupies at most half its area. Indeed, for a fixed parallelogram shape its largest inscribed copy can be chosen at an alignment as above. For the aligned side, if the parallelogram has height fraction $t$ of the triangle altitude, its base is at most $s(1-t)$, giving area fraction $2t(1-t)\le1/2$.

## A coherent switch across grid interfaces at unit scale

Let $w=a+b$, $z=(a+b\rho)/c$ and $d=(b+a\rho)/c=\rho\bar z$. Form a parallelogram from $k$ consecutive $bc$-rhombi, with span vectors $kbc\,d$ and $bc$. Initially cell edge vectors are $cd$ and $b$; their difference is $a\rho$. Flip all $k$ rhombi. The new rectangle in cell coordinates has $kc$ columns along $e=bd$ and $b$ rows along $f=c$. Its third unit vector is $g=f-e=a\bar z$. An $ab$ elementary rhombus with edges $ae$ and $bg$ occupies the cell-coordinate vertices
$$
(b,0),\quad(a+b,0),\quad(a,b),\quad(0,b).
$$
Translate it by $jae$ for $j=0,\ldots,m-1$, with $m=\lfloor(kc-b)/a\rfloor$. These rhombi have disjoint interiors: their constant-$i+j$ bands have disjoint interiors. Any subset can be switched independently. In each selected rhombus the two new short vectors are $ad$ and $b\bar z$, giving a long edge $ad+b\bar z=c\rho\bar z^2$. The three long-edge directions encountered have heights $-1,0,-2$ in the local frame. Initial short edges have height zero; tiles with a side two levels away now fill a positive-area patch. Each choice is an ordinary filling of the *same* region, preserves its entire external boundary, and can coexist with T-junctions outside. The number of tiles in the strip is $2kbc$.

To place the construction in the unit F2 board, reflect and rotate by $v\mapsto\rho^2\bar z\bar v$. Its new spans are $(-ab,bw)$ and $(0,kbc)$. For $a/b\ge5/2$ the minimum board scale for this orientation is
$$
 F=\max\left(\frac{a}{q},\frac{bw}{ap}\right)+\frac{kbc}{ap}
  =\frac{a}{q}+\frac{kbc}{ap}.
$$
The maximum formula follows by translating the four vertices to have both coordinate minima zero. For the equality put $r=a/b$ and use $r^3-3r-1>0$ for $r\ge2$. One may place the lower vertex at $(ab,\delta)$ with $0<\delta<V(1-F)$ whenever $F<1$. This avoids forcing the triangular cap at the board corner produced by $\delta=0$.

For $k=2$ one has $F<1$ throughout $a/b\ge5/2$. Indeed $c<a+3b/4$ there, and $apw-2b(a+3b/4)q=b^3(r^3-r^2-3r-3/2)>0$ at $r=5/2$ and thereafter. The residual mixed prime-product family meets this hypothesis: at $v=1$ its even parameter $u$ is at least six; at $v\ge3$ the staircase bound requires $u/v>4(v-1)\ge8$. The side ratio is $((u/v)^2-1)/(2u/v+1)$, an increasing function, and at $u/v=6$ it is $35/13>5/2$. These parameter facts are from the [sharp staircase theorem](../../staircase/SHARP_STAIRCASE.md).

At $k=2$ there are precisely two independent second-stage rhombi: $2a<2c-b<3a$ follows from $a+b/2<c<a+b$ and $b<a$. Thus the common intermediate grid yields four second-stage fillings of the same patch. At 3431 the two-stage patch uses 1036 tiles. At 5063 it uses 2236. The patch is deliberately shared by both fillings. Tileability of the rest of the board is a separate condition. In particular the switch preserves the exact boundary of its patch and cannot by itself close a hole outside it. A [standard-library integer checker](check_rhombus_switches.py) reconstructs the initial, intermediate and final fillings and compares their full boundary chains.

## Installing the switch inside an existing packing

In the unrotated frame the strip and its initial tiles belong to the ordinary axial $b$-by-$a$ grid of [the single-strip packing](../packing/GRID_STRIP.md). Its bounding rectangle at $O$ has dimensions $b(c+kb)$ and $kab$, both aligned to full cells. Hence the switch is already installed in the $N-p-q+1$ packing of a residual prime board whenever
$$
(c+kb)/q+kb/p\le1 .
$$
At $k=1$ this holds for every residual pair: $c<a+b$ and $p/q+b/p<1$ for $r=a/b\ge5/2$, since $r^2-r-3>0$.

At $k=2$ it holds for every residual mixed prime pair **except 5063**. For $a\ge5b$ use $c<a+3b/4$ and
$$
(a+2b)(a-7b/4)-2bq=a^2-15ab/4-11b^2/2>0.
$$
For $v\ge5$ the failed staircase requires $u/v>4(v-1)\ge16$. For $v=3$ the exceptional staircase threshold does not apply, so failure requires $u>36$. Thus $v>1$ always has $a/b>5$. If $v=1$, only the even integers $u=6,8,10$ outside the staircase can give $a/b<5$. They give $(35,13,43)$, $(63,17,73)$, and $(33,7,37)$ respectively. The middle case has composite $q=143$. At 3431 the bounding rectangle fits with ratio $3419/3431$. At 5063 it fails with ratio $6367/5063$; in the original orientation its far corner actually belongs to the strip, so translating it inside this board is impossible.

At 5063 there is still a concrete larger packing in which to perform both stages. Use the rotated strip above and take the **entire regular tessellation of its first stage**. Its basis vectors in physical axial coordinates are $(0,c)$ and $(-ab/c,bw/c)$, and its cell diagonal is their difference. Anchor its vertex lattice at $(ab,1)$. Keep every whole triangle contained in the board. This gives **4846** full tiles, including the entire **2236**-tile switch. The other 2610 placements remain fixed through the stages. The same rotated construction has 3248 full tiles at 3431. Its original axial packing of 3312 already admits the two stages. The checker enumerates the contained triangles directly using the three board inequalities; the bounding box in integer cell coordinates is calculated from the inverse images of all three board vertices.

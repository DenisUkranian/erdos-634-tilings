# A gluing theorem for every fixed triangle and tile

Let $B$ be any nondegenerate Euclidean triangle and $T$ any fixed physical triangle. Put
$$
 S=\{s\in\mathbb Z_{\ge1}:sB\text{ can be tiled by congruent copies of }T\}.
$$
The boards $sB$ are homothetic. Both orientations of a tile are allowed and side subdivisions on adjoining pieces may differ.

**Theorem.** Every nonempty $S$ contains all sufficiently large multiples of $\gcd(S)$. Thus for a fixed physical tile and board the gcd decides the entire tail. Two attained scales give the explicit bound proved in the last section.

## A strip that propagates tilings

Write $D_k$ for the reference triangle with vertices $(0,0),(k,0),(0,k)$. Work in coordinates along the two sides of $dB$. Translations and half-turns in these coordinates are Euclidean translations and half-turns in the original plane.

If $dm,dn,dk\in S$ with $k=am+bn$ for nonnegative integers $a,b$, then $d(k+mn)\in S$. Put $L=mn$ and partition $D_{k+L}$ into $D_k+(0,L)$, $D_L+(k,0)$ and $[0,k]\times[0,L]$. The first region uses its given tiling. Subdivision tiles $D_L$ with copies of $D_m$. Partition the box into $a$ strips of width $m$ and $b$ strips of width $n$. A strip of width $s$ consists of $L/s$ coordinate squares of side $s$. Each square splits into two copies of $D_s$ related by a half-turn. Filling these with the original physical tile gives the assertion.

## Coprime sizes construct a scale coprime to both

Write $D_s=\{x,y\ge0,\ x+y\le s\}$. A size-$s$ grid triangle is a translate of $D_s$ or of $-D_s$. We give an explicit positive dissection, allowing T-junctions.

**Lemma.** If $m,n\ge2$ are coprime, set $M=mn$, $H=100M+m$, $r=m$, $K=rH+n$. Then $D_K$ is tiled by grid triangles of sizes $m$ and $n$, and $\gcd(K,mn)=1$.

**Compatible lines.** Take the usual triangulation of $D_{rH}$ into $r^2$ grid triangles of size $H$. Its edges have supporting lines $x=iH$, $y=jH$, or $x+y=kH$. To each *edge segment* assign a residue $a_e$ modulo $m$. On the two coordinate sides assign zero, and on the diagonal boundary assign one. Across each cell require $a_x+a_y-a_{x+y}=0\bmod m$ for its three edge segments. These conditions can be solved: multiply the equations of the downward triangles by $-1$. The two incidences of each internal edge now have opposite signs. This is a flow problem on the connected graph dual to the triangulation. Its only compatibility condition is that the sum of all prescribed boundary contributions vanish. That sum is $-r=0\bmod m$. Concretely put zero on non-tree internal edges of the dual graph and solve successively from leaves of a spanning tree. The final equation holds by the sum condition.

Choose representatives $0\le a_e<m$ and shift the corresponding support level by $na_e$. In particular the new boundary supports are $x=0,y=0,x+y=K$. Use each common shifted support for both adjacent cells. Inside each cell the three shifted lines belong to a translate of the $m$-grid: the residues of the $x$- and $y$-levels sum to that of the diagonal level, since $m\mid H$ and the face equation holds. The inward half-planes of one cell cut out a triangle of side between $H-3M$ and $H+3M$. At each of its three new vertices remove a corner triangle of side $\tau=10M$ using the parallel to the opposite edge. The remaining hexagon lies on the same translated $m$-grid, as $m\mid\tau$. Fill it with its elementary size-$m$ triangles.

**Disjointness and coverage.** Use the norm $\|(x,y)\|=\max(|x|,|y|,|x+y|)$. On a coarse cell let $a,b,c$ be its inward slack variables (the signed differences from its three support levels). They sum to $H$. After the shifts write $a',b',c'$, each differing from its old value by less than $M$. The hexagon has all three shifted slacks nonnegative and each pair sum at least $\tau$.

Within norm distance $2M$ of a coarse vertex $v$ no incident hexagon is present: for the two slacks zero at $v$, their original sum has absolute value at most $2M$, and the shifted sum is less than $4M$. A nonincident cell has some old slack at most $-H$ at $v$ and cannot reach that neighborhood. Elsewhere at most one supporting line of the entire coarse grid can be within $M$ in level difference. Indeed two nonparallel close levels would locate their intersection, a grid vertex, within $2M$, and distinct parallel levels differ by at least $H$. This argument can equally be made in the full planar coarse grid before restricting to the board. A coarse lattice vertex outside the original board cannot be within $R$ of $D_K$, since its violation of an old board inequality is at least $H$ and the exterior diagonal moved only by $n$.

If there is no close line, no inward sign can change. If there is one, projection to it can be made with norm displacement at most $M$. No other level is crossed. Thus the only two potential coarse cells are the two incident to the single edge where the projection lands. Both use the *same* shifted line on opposite sides. On the board boundary the incident inside half-plane is precisely the half-plane of the new board. These observations establish that the hexagons have disjoint interiors and stay inside $D_K$. Near a coarse vertex they were removed entirely within distance $2M$; away from all such neighborhoods this argument also covers points near the three outer sides and permits equality on a supporting line.

Outside the radius-$R$ neighborhoods of the coarse vertices, $R=20M$, every point of $D_K$ is covered by those hexagons. The preceding sign argument first chooses a cell satisfying its three shifted half-plane conditions. If, for example, its $a'+b'$ cut fails, then $a,b\ge-M$ and $a+b<\tau+2M$. Relative to the old intersection of these two lines the three norm coordinates have absolute values $|a|,|b|,|a+b|$, each at most $\tau+3M<R$. This contradicts the choice of point.

**Filling the remaining regions.** The closed radius-$R$ hexagons about distinct coarse vertices are disjoint since $2R<H$. Fix the neighborhood of a coarse vertex $v$. Only incident coarse cells can reach it. Only their two shifted supports through the vicinity of $v$ and their cut opposite $v$ can affect the local boundary. Indeed the old far support is at level distance $H$, and the cuts at the two other vertices remain at level distance at least $H-\tau-2M>R$. Each relevant line belongs to the translated $n$-grid $v+n\mathbb Z^2$: its level measured relative to $v$ is a sum of the shifts $na_e$ and possibly $\tau$, all divisible by $n$. The sides of the radius-$R$ hexagon are on that grid as well, since $n\mid R$. Every outer board boundary meeting this neighborhood also has the required level. Thus every remaining open region in this neighborhood is a union of elementary size-$n$ triangle interiors and their intervening edges. Take their closures. Together with the previously filled hexagons these cover the entire closed board; all tile interiors are disjoint. Finally $K\equiv n\bmod m$ and $K\equiv m^2\bmod n$, proving coprimality.

## Consequence for arbitrary physical triangles

**Theorem.** If $d mB$ and $d nB$ both have tilings by the same fixed tile $T$, where $\gcd(m,n)=1$, then $d kB$ has such a tiling for every sufficiently large $k$. For $m,n\ge2$ one sufficient bound is
$$
 k\ \ge\ (m-1)(n-1)+mn\big(100m^2n+m^2+n\big).
$$
If one normalized size equals one, every positive $k$ works.

In the affine side coordinates of $dB$, the lemma supplies a third attained scale $dK$ by substituting the original two tilings into its macrotriangles. All positive multiples of $K$ are attained in normalized units. All integers from $F=(m-1)(n-1)$ onward are nonnegative combinations of $m,n$ (use the least representative $b\in[0,m-1]$ with $bn\equiv k\bmod m$). In this range the strip construction above propagates any attained scale by $mn$. Given $k\ge F+Kmn$, there is a multiple $jK\in[F,F+Kmn]$ congruent to $k$ modulo $mn$, since $\gcd(K,mn)=1$. It propagates to $k$.

Consequently, for **every** nonempty fixed-pair spectrum $S$, its eventual members are exactly the multiples of $\gcd(S)$. Choose finitely many attained scales generating the gcd: begin with any attained scale and adjoin one reducing the current positive gcd whenever it still exceeds $\gcd(S)$. If all sufficiently large multiples of $g$ have already been obtained and another seed is $u$, choose a large $gk\in S$ with $k\equiv1\bmod u$. Applying the two-seed theorem to $gk,u$ yields all sufficiently large multiples of $\gcd(g,u)$. Induction gives the claim. This is a theorem on a fixed board and a fixed physical tile. For the unrestricted spectrum the shapes, the integer scales that occur first, and their gcd can all vary. This proof has been checked inside the project; external mathematical review is pending.

There is a direct interpretation in tile counts. For a fixed pair with nonempty $S$, put $d=\gcd(S)$ and $C=d^2\operatorname{area}(B)/\operatorname{area}(T)$. Then $C$ is a positive integer. Indeed, for finitely many attained $dk_i$ with $\gcd_i k_i=1$, all $Ck_i^2$ are tile counts and $\gcd_i k_i^2=1$. An integer linear combination gives $C$. Consequently the exact set of counts from the integer dilates of this board with this tile is $\{Ck^2:k\ge1\}$ with at most finitely many counts removed. The coefficient $C$ need not be squarefree.

The sample with $(m,n)=(2,3)$ has $K=1207$, with 353419 triangles of size 2 and 4797 of size 3. Two standalone implementations check example constructions. One checks containment, area and separation of convex blocks. The other reconstructs the complementary cells by winding numbers and cancels their oriented boundaries exactly. [Area and disjointness test](verify_two_scale.py) · [Independent boundary check](verify_gluing_boundaries.py) · [Eight test pairs](gluing_boundaries.json).

# Charge variation across the physical gates of a lifted cell

A later [disjoint branch reserve](OFF_HULL.md) improves the bounds below to 45 and 63, respectively.

For the 3431 and 5063 F2 boards, let $V$ be the sum of the absolute signed populations of all odd **lifted** cells, divided by the long side $c$. Any complete tiling satisfies
$$
V\le 51\quad (3431),\qquad V\le 71\quad (5063).
$$
These bounds also apply after projecting to Euclidean cells. At 5063 every ordinary 86-tile cell has exactly 43 tiles of each sign, at either parity and at arbitrary heights. At 3431 there are at most three ordinary monochromatic lifts of size 74 or 111 combined across the entire board. Both original counts remain **OPEN**.

## Disjoint components at one physical lift

Use the reflected path frame of the [complete gate equation](../joint-cell-tree/FIVE_BLOCKS.md). The axial marker $C$ has path height two, the slant marker $T$ has path height zero and $d=a-b$. The total even and odd signed populations are $d,c$, respectively. Rotating or reflecting the entire coordinate frame is performed once. Within this frame the labels on every cut below have the same signs.

Take an ordinary lift $v\ne C$. For each incident edge let $i$ index the component on its far side. Use $E_i,O_i$ for its actual even and odd signed tile populations and $I_C,I_T$ for its exterior inclusion indicators. The far components partition the short populations outside $v$. The [tree and physical cut theorem](../joint-cell-tree/TREE.md) gives $c\mid O_i$ and $E_i\equiv d I_C\pmod c$. Let $Q_i$ count the signed tiles at $v$ going through gate $i$ and $P_i$ the signed owners reaching $v$ from the far side. The two cut characters give
$$
\begin{aligned}
v\text{ odd}:\quad &Q_i=d(E_i-d I_C)/c-O_i+2c I_C-c I_T, &P_i&=E_i-dO_i/c,\\
v\text{ even}:\quad &Q_i=d O_i/c-E_i .
\end{aligned}
$$
Indeed with the far root even, adding the two character equations cancels the exterior term to give $P_i$. Subtracting gives $Q_i$ with exterior term $-(2c^2-d^2)I_C+c^2I_T$. With the far root odd the exterior term cancels in the equation for $Q_i$. These signs cover $v=T$ as well. The gates partition whole short-to-long steps even when a geometric side meets several tiles.

Choose a sign $\sigma$ and set $q_i=\sigma Q_i$. The following integer coordinates incorporate all exterior terms.

| Parity of $v$ | $s_i/\sigma$ | $t_i/\sigma$ |
|---|---|---|
| Odd | $O_i/c-2I_C+I_T$ | $(E_i-dI_C)/c$ |
| Even | $(E_i-dI_C)/c$ | $O_i/c-I_C$ |

In both rows $q_i=d t_i-c s_i$. At an ordinary lift with charge $G_v$, one has $\sum t_i=0$ and $\sum s_i=-\sigma G_v/c$. The disjoint far-side populations give, with $S=\sum|s_i|, U=\sum|t_i|$,
$$
\begin{array}{c|cc}
 &n_{\rm odd}\text{ at least}&n_{\rm even}\text{ at least}\\ \hline
v\text{ odd}&n_v+c(S-3)&cU-d\\
v\text{ even}&c(U-1)&n_v+cS-d .
\end{array}
$$
For instance at odd $v$, the total correction to the odd counts has absolute variation at most $3c$ (one occurrence of each marker), and the correction to the even counts costs at most $d$. The triangle inequality on each component proves the table.

## Balance at 86 tiles

If $v$ is monochromatic, take $\sigma$ to be its sign and write $n_v=kc$. Then $q_i$ is the unsigned gate population, with $0\le q_i\le\lfloor\alpha kc\rfloor$. The [verified endpoint capacities](../../../2026-11-20/semiprimes/continuation/global-closure/median/NATIVE_GATE_CAPACITY.md) give $\alpha=43/222$ or $8/43$. Their lift localization uses equality of the two bank markers at every positive-length contact. The only possible exterior contribution at an ordinary lift is from the full slant. Its endpoints coincide modulo the normalized period $c$. See the [localization proof](../joint-cell-tree/BRANCHING.md). These facts allow positive or negative tiles of either hand.

At 5063 take $k=2$, so $q_i\le16$ and $\sum q_i=86$. As $-43\equiv1\pmod{22}$, write $s_i=q_i-22l_i$. Then $\sum l_i=4$. For every integral $l$ and $0\le q\le16$,
$$
|q-22l|\ge q-10l.
$$
For $l\le0$ this follows immediately, and for $l\ge1$ it reduces to $32l\ge2q$. Thus $S\ge46$. From $22t_i=q_i+43s_i$ it follows that $22U\ge43S-86$, hence $U\ge86$. Even the weaker parity row in the table now requires $N\ge86+43(46+86-3)-22=5611$. This contradicts the board budget. The argument has no hypothesis on the number of odd tiles.

The separate sign counts are multiples of 43 and every nonempty ordinary lift costs at least 86. Consequently any ordinary Euclidean cell of size 86 consists of one occupied lift and has inventory $(43,43)$. Every charged ordinary lift costs at least 129. If $R$ counts occupied ordinary lifts of both parities and $r$ counts charged ones, the core reserve gives $2R+r\le117$ at 5063.

An independent integer recurrence checks this contradiction. Give a gate option $(q,s,t)$ cost $|s|$, $|t|$ or $|s|+|t|$. At increasing cumulative cost store all reachable pairs $(\sum q,\sum s)$ and stop at $(kc,-k)$. The equation then gives $\sum t=0$. Nonzero options have positive cost in all three runs because the caps in the table are below both $c$ and $d$. The cost bound limits the charged coordinate and the other follows from the gate equation. Repetitions and unlimited gates give a relaxation of the tiling.

| $c,k$ | Gate cap | Minimum $S$ | Minimum $U$ | Minimum $S+U$ |
|---|---:|---:|---:|---:|
| 37, 2 | 14 | 10 | 12 | 22 |
| 37, 3 | 21 | 9 | 12 | 21 |
| 43, 2 | 16 | 46 | 88 | 134 |

## Two parity trees at 3431

Mark $C,T$ and all charged lifts of one chosen parity in the existing lifted tree, then take their minimal spanning subtree. Do this separately for each parity. At any monochromatic ordinary lift of size $2c$ or $3c$, the caps 14 and 21 require at least six nonempty gates. A gate leading away from the exterior has $q=d t-c s$ with $0<q<\min(c,d)$. Neither $s$ nor $t$ can vanish. Its far component contains a charged lift of **each** parity. A gate toward an exterior marker already leads to a marked vertex for each tree. Thus all six directions occur in *both* subtrees, wherever the monochromatic lift is situated.

Let $m_2,m_3$ count these lifts across both parities. Each subtree has at least $2+4(m_2+m_3)$ leaves, by the degree sum of a finite tree. At most two leaves are exterior markers. Every remaining leaf is charged in the parity used to define that subtree. The two sets of remaining leaves are disjoint and none is among the counted monochromatic lifts. Each costs at least $3c$, since an ordinary charged lift of size $2c$ would itself be counted. Reserving the axial core separately yields
$$
26m_2+27m_3\le (3431-(3431\bmod 37))/37=92 .
$$
In particular $m_2+m_3\le3$. This strengthens the [one-parity branching estimate](../joint-cell-tree/BRANCHING.md).

## A whole-board bound on odd charge variation

Use only the minimal subtree $H$ spanning $C,T$ and the charged odd lifts. Write $G_v=\sigma ck$ with $k>0$ at a charged odd vertex, let $m=cx$ be its minority population, and let $l$ be its degree in $H$. Then $n_v=ck+2m$. On each of its $l$ gates inside $H$, the signed current aligned with $\sigma$ is at most its population of that sign. The same endpoint certificate bounds that population by
$$
p=\lfloor\alpha(ck+m)+(1-\alpha)m\rfloor=\lfloor\alpha ck\rfloor+m.
$$
Every other gate has $O_i=I_C=I_T=0$. Its two banks obey $dP_i=cQ_i$, with $d\mid Q_i$. These statements allow nonempty balanced branches. The aligned sum of the $Q_i$ on these gates is therefore $d j$ for an integer
$$
j\ge J=\left\lceil (ck-lp)/d\right\rceil .
$$
The corresponding even bank has aligned signed population $cj$. All even owners reaching $v$, summed across *all* its gates, have aligned signed population $dk$ by the formula for $P_i$ and the two whole-board totals. Consequently the actual number of such even tiles is at least
$$
dk+2\max(0,cJ-dk).
$$
Indeed the complementary bank must have at least $cj-dk$ oppositely signed tiles if this is positive. Each even tile has only one odd long-side marker. Hence adding these bounds over charged odd vertices counts disjoint physical even owners. The odd short populations at the same vertices are disjoint as well. Writing $V=\sum k$ gives the simultaneous necessary conditions
$$
\frac{N-(c+d)V}{2}\ \ge\ \sum_v [m+\max(0,cJ-dk)],\qquad
\sum_v (2-l_v)\ge0 .
$$
The second inequality follows because every unmarked vertex of $H$ has degree at least two. The two exterior markers together contribute at most two to the degree sum $\sum_H(2-\deg)=2$. Every charged odd vertex is distinct from both markers. In particular the surplus condition is valid when there is just one charged odd lift on the exterior path.

For a finite replay, $V$ is positive and odd with $(c+d)V\le N$. Its two sign totals in units of $c$ are $(V+1)/2$ and $(V-1)/2$. At each charged lift enumerate $k$, $1\le l\le 2c$ and $m=cx$ below the available half-excess budget. A unit charge requires $x\ge1$. At 5063 a charge of magnitude two also requires $x\ge1$ by the 86-tile exclusion. Maximize the sum of $2-l$ over multisets with these sign totals and budget. In particular discarding any placement or tree-embedding constraints at this step enlarges the candidate set. The largest possible surpluses in this relaxation are as follows.

| Board | $V$ | Maximum surplus |
|---|---:|---:|
| 3431 | 53 | −1 |
| 3431 | 51 | 0 |
| 5063 | 77 | −4 |
| 5063 | 75 | −2 |
| 5063 | 73 | −1 |
| 5063 | 71 | 1 |

Larger odd values already exceed the area budget $(c+d)V\le N$. Negative surplus violates the tree identity. This excludes the previous extremal odd-variation profile $V=77$ even when many heights and exterior-free branches are available. The endpoint values 51 and 71 pass only the displayed relaxation. Their geometric feasibility remains unknown, as does the native one-cell regime at small variation.

## Verification

Run from this directory:

```sh
python3 verify.py | diff - STATUS.json
```

[verify.py](verify.py) recovers the lifted owners from exact coordinates of two complete 143 tilings. It measures both banks independently of the charge formula, verifies both parity equations and tests the hull estimate with the positive-control gate constant $1/2$. The proof for arbitrary tilings uses the cut and endpoint theorems above. [hull.py](hull.py) checks the last table twice. Its second recursion scans the integer outward current and recovers the least possible degree, instead of constructing the first recursion's degree profiles. Negative outward current cannot improve the minimum required degree or save tiles compared with zero in this relaxation. [Machine-readable replay](STATUS.json).

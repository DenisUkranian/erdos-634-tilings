# How much area can cross a physical gate?

Both original triangle counts are open. We work in the standard vertex-phase frame on the positioned tree. Let a complete F2 tiling have an exterior-free tree edge, and let its far union contain `n` tiles. Its gate has `m` unmatched whole long-side owners. The argument uses the physical gate even when the far union has several short lifts. There is no two-height hypothesis.

A [gate carrying one unit of alternating charge with the minimum number of owners](SATURATION.md) encloses at most **2849** tiles at 3431 and **2107** at 5063, at any total unmatched population. The geometry of the original triangle enters the former bound. Simultaneous projected word constraints give the latter.

The [charged equality theorem](../remote-sections/CHARGED_EQUALITY.md) puts the entire odd charge at the native middle lift if the whole board has at most 149 unmatched tiles at 3431, or 171 at 5063. In these windows we obtain the following bounds on distinct tiles whose short lifts lie outside the exterior path.

| Board | Number of occupied off-path lifts | Maximum distinct off-path population |
|---|---:|---:|
| 3431 | one | 1776 |
| 3431 | two, on separate branches | 814 |
| 3431 | two, nested | 592 |
| 5063 | one | 172 |

In particular, at 5063 in this window at least **4891** tiles have one of the three native short lifts. If the off-path lift has 172 tiles, its gate costs at least 20 unmatched owners. The limits use the earlier disjoint exterior charge payment of 107 and 149. This leaves a total of 42 or 22 owners for neutral branches. Each occupied branch costs at least 16, so there cannot be more off-path lifts in these windows. For the nested case the outer gate costs at most 26. The table concerns actual arbitrary tilings under its stated budget hypothesis.

## A determinant inequality for any charge

Write the directed long-edge vectors supplied by the two banks as $v_i$. At a remote gate they form the boundary of the far union and decompose into edge-disjoint Jordan circuits, even at pinches. The embedding and the treatment of T-junctions are proved in the [physical circuit theorem](../../../2026-11-26/semiprimes/charged-contour/README.md). In axial coordinates a unit parallelogram has Euclidean area $\sqrt3/2$. Then

$$
2abn\ \le\ \sum_{i<j}|\det_{\rm axial}(v_i,v_j)|.
$$

For one circuit take the convex hull $K$ of its vertices and the centered zonotope $Z=\sum_i[-v_i/2,v_i/2]$. In any projection direction the closed walk travels from its minimum to its maximum and back. Its total projected variation is at least twice the width. Thus every support value of $K-K$ is bounded by that of $Z$. Planar Brunn–Minkowski gives $4|K|\le|K-K|\le|Z|$. Adding a generator segment to a zonotope sweeps out its length times the previous perpendicular width. Induction gives $|Z|=\sum_{i<j}|\det(v_i,v_j)|$ in Euclidean area. A reference for the convex-body inequality and its equality case is [the Brunn–Minkowski monograph](https://users.renyi.hu/~carlos/Brunn-Minkowski-Book-2024-02-05.pdf). The tile has area $ab\sqrt3/4$. For several circuits, the signed sum of the enclosed areas is the physical area. Bounding the positive terms separately and then adding every nonnegative cross term gives the assertion.

In the local chart, conjugated if necessary and always oriented positively, the low vector is $D\rho^j$, the high vector $c\rho^j$, with $D=a+b\bar\rho$ and $\rho=e^{i\pi/3}$. If their respective counts are $u,v$, averaging the zonotope over the six unit rotations by Minkowski addition and division by six does not decrease its area by Brunn–Minkowski. This spreads the unsigned multiplicities evenly over the three axes of each bank. Within each triple the axial determinant has absolute value $c^2$, and each row of mixed absolute determinants sums to $2c(a+b)$. Hence
$$
6abn\ \le\ c^2(u+v)^2+2c(a+b-c)uv.
$$
This inequality uses both banks at the same physical cut. Its validity includes charged branches. For neutral branches the exact determinant sum can replace the circular area estimate in the [global reserve](../remote-sections/README.md). Its floor for an individual edge and the signed exterior payment count disjoint owners under the hypotheses of that reserve.

For a neutral cut both bank heading characters vanish. On axes $0,1,2$ each signed triple therefore has the form $(x,x+z,z)$. The vector sums of the two banks cancel. Every unsigned axis count equals the absolute signed count plus a nonnegative even number. [reserve.py](reserve.py) exhausts these possibilities and computes the determinant sum for each vector of six counts. Both banks occur by the supported-cycle theorem. The 16-owner terminal result is applied separately.

Equality in the determinant inequality for a positive-area region forces a single positively oriented convex circuit. Two distinct circuits have a strictly positive cross term, since each spans the plane. Equality forces the Jordan region to fill its convex hull. The equality case of Brunn–Minkowski makes $K$ centrally symmetric, and $K-K=Z$ follows from containment and equal areas. Thus the contour is a translate of $Z/2$. On each axis its opposite sides have half the total unsigned length, hence half the owner count on each side is integral. The sorted positive word must be an identity in both projected boundary groups. At 3431 the putative 592 tiles at length 24 attain equality. At 5063 so do 344 tiles at length 22. In the order-$a$ group combine each high run at $j$ with the next low run at $j+1$. The six resulting cyclic syllables remain nonzero, on successively different factors. [check.py](check.py) independently constructs all integral half-side polygons by shoelace area. It finds one extremal inventory at 3431 and six at 5063. [CHECK.json](CHECK.json) gives their nonzero residues. The word argument below is stronger at 5063.

## Area from the order of the sides

The [supported-word theorem](../../../2026-11-26/semiprimes/terminal-contact/REMOTE_BOUNDARY.md) assigns each closed Jordan circuit the identity in each of two free products of three cyclic factors of order $q$, for $q=a,b$. A high step at heading $j$ projects to $c$ copies of heading $j$. A low step projects to $b$ copies of heading $j-1$ at order $a$, and $a$ copies of heading $j$ at order $b$. Opposite headings give inverse generators. The planar displacement of the letter modulo $q$ equals its projected generator displacement.

For a separate order, tabulate the greatest shoelace sum for a path of length $h$, displacement $p$, and product in the factor $k$. Also tabulate the identity states. Within one factor the product is determined by $p$ modulo $q$: each of the three primitive axes embeds its cyclic factor into the axial lattice modulo $q$. Appending paths with endpoint displacements $p,r$ and scores $s,t$ gives $s+t+\det(p,r)$. Thus retaining a maximum is safe at fixed state.

A word whose product belongs to factor $k$ can end with a $k$ letter and a prefix in $k$, or with a nonempty identity suffix and a prefix in $k$. To see completeness, read from the right in reduced syllables. If the last letter is outside $k$, the first disappearance of that last syllable gives an identity suffix. If the entire word is its first such suffix, the whole product is identity and the word can instead be generated using the factor of its last letter. After processing a length, copy the identity states into all three factors. Record a spatial return before dropping it from all tables for higher lengths. A proper contiguous subword of a Jordan circuit cannot return to its starting vertex. The resulting maxima upper-bound all Jordan circuits, though the relaxation can retain intersecting walks.

Below $c+d$, every circuit has zero alternating charge. Its positive enclosed count is divisible by $2c$, and its length is even. In the cut's Jordan decomposition holes can only reduce signed area. Maximize the sum of the rounded individual capacities over all allowed length partitions. The minimum circuit lengths are 10 and 12 from the circuit theorem. At 5063 the largest doubled axial areas allowed by the order-35 test at lengths 18, 20, 22 are 63210, 87290, 114380. Even the largest is less than $258ab=117390$. Multiple circuits obey the bound by the same partition calculation. At 3431 length 26 gives 151404, below $666ab=153846$. [WORDS.json](WORDS.json) lists every even cost in the two windows.

[words.py](words.py) also uses literal reduced stacks and meets two walks in the middle for all even lengths through eight in both orders on both boards. This independent computation gives the same extrema. On both complete 143 tilings [check.py](check.py) rebuilds the short lifts and actual unmatched owners. Including the exterior slant, the determinant bound passes on all four native cuts, in particular the positive populations 105 and 91. Their directed supported words reduce to identity in both orders, using their physical segment displacements. The 143 examples have no occupied exterior-free cut, so the target-specific concentration and saturated-charge tests have empty hypotheses there.

## Reproduction

Use Python 3.9 or later, a C++17 compiler and enabled Python assertions. Run from this directory.

```sh
python3 reserve.py | diff - RESERVE.json
python3 check.py | diff - CHECK.json
python3 words.py | diff - WORDS.json
```

For the independent charged-gate calculation see [SATURATION.md](SATURATION.md). The classification reduction and the unrestricted existence questions remain at their previous status. None of the capacities supplies an upper bound on the total number of unmatched tiles in an arbitrary board.

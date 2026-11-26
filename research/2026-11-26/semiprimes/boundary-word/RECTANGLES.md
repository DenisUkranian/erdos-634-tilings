# Rectangular remainder at the smallest unmatched population

Suppose $M=107$ or $149$, respectively. The nested bounds force the three native cells. Every unmatched owner is on one of the two distinguished cuts. Fix the increasing tree. All height-two tiles therefore form the slant component $S_2$. Its even charge is $-c$, and its odd charge is zero. The crossing classes are saturated with $p_2=-c$, $q_2=c-d$ and $m_2=2c-d$. No bank contains both signs.

After rotation by $z^{-1}$, list the multiplicities of effective directions $0,2,4$ first in $cR$ and then in $(a+b\rho)R$. The checker solves the exact displacement and the two characters by the signed-axis formula in the main theorem.

| Board | Low triple | High triple |
|---|---|---|
| 3431 | $(0,0,37)$ | $(7,0,4)$ |
| 5063 | $(0,0,43)$ | $(13,0,8)$ |
| 5063 | $(6,1,36)$ | $(6,1,14)$ |

The following argument applies to the first inventory for each target. Translate $Y$ to the origin and normalize by $z^{-2}$ (no reflection). In axial coordinates the effective word from $Y$ to $X$ uses

| Token | Step | Count | Owner |
|---|---|---:|---|
| 0 | $(-b,-a)$ | $c$ | short height two, hand minus, $j=4$ |
| 1 | $(c,0)$ | $b$ | short height one, hand plus, $j=0$ |
| 2 | $(0,-c)$ | $c-a$ | short height one, hand plus, $j=4$ |

All steps strictly increase the linear form $x-Ky$ for any $K>b/a$. Thus the crossing graph has no directed cycle. Its divergences are a single unit source at $Y$ and sink at $X$. Decomposing the integer flow into a path and cycles leaves exactly one physical path; none of its edges may be independently translated. Its positions follow from the prefix counts. The long edge, directed bank, height and hand determine its whole triangle uniquely. Consecutive owners must be contained in the board and have disjoint interiors.

**Removing the specified triangles.** The $c$ owners of token 0 are precisely the unmatched height-two tiles. Remove them from $S_2$ without moving anything. All remaining height-two tiles already have their actual half-turn mates in that same cell and region, so their union is tiled by parallelograms. Subtracting the counterclockwise triangle boundary replaces each token 0 on the contour by a vertical step of length $a$ down and a horizontal step of length $b$ left, in that order. This follows from the third vertex being $(x,y-a)$ when the long edge starts at $(x,y)$. All sides of the residual boundary are now horizontal or vertical in axial coordinates.

No parallelogram in this union can have a third edge direction. Among all edges in that direction choose one of maximum supporting-line coordinate along a normal. At a generic point of its relative interior the outer bank must be exposed: a parallelogram on that bank would have an opposite parallel edge with larger coordinate. Exposure on a positive interval contradicts the two-direction boundary identity. This accounts for split contacts and disconnected components. Consequently in axial coordinates all paired regions here are tiled by axis-aligned $a$-by-$b$ or $b$-by-$a$ rectangles with integral vertices. Euclidean angles in the axial picture need not be right angles.

The replaced contour never increases $y$. Apart from its horizontal levels, the interval in the residual region at coordinate $y$ runs from the contour to the slant $x=0$. This follows also from its two boundary crossings with opposite orientations, with cancellation when they coincide. A vertical token at horizontal coordinate $x$ therefore requires $-x\in a\mathbb N_0+b\mathbb N_0$. The vertical piece of token 0 is tested before its horizontal piece. A horizontal slice through interiors of rectangles proves this condition even at a T-junction level by choosing the slice strictly between adjacent vertex levels.

**Two residue tests.** Project the directed endpoints of the residual boundary onto $(\mathbb Z/s)^2$ for $s=a$ or $b$, keeping separate horizontal and vertical endpoint currents. Every individual rectangle has zero current for each axis. The pair of sides of length $s$ has zero endpoint differences, and the other two sides project on top of each other with opposite orientations.

* Modulo $a$, the only vertical contour steps with nonzero endpoint differences are the $c-a$ tokens 2. Their successive starting $y$ residues are distinct, progressing by $-c$, since the remaining vertical pieces have length $a$. The wall contributes the return chord at $x=0$. Cancellation at the first $y$ forces the first token to have $x=0$ modulo $a$; at each next $y$ the previous endpoint forces the same residue. The chain ends at the wall's other endpoint.
* Modulo $b$, only the $b$ tokens 1 have nontrivial horizontal endpoints. Their successive starting $x$ residues are all different since $\gcd(c,b)=1$. Cancellation at each such $x$ requires all their $y$ residues to be the same. All $b$ possible common residues are tested.

For a prefix with counts $(i,j,k)$, the current corner is $(cj-bi,-ai-ck)$. The checker extends it by each token still available, tests the width and the two residues, and reconstructs the compulsory whole owner on the indicated bank. It rejects positive overlap with the preceding owner. At completion, the area is evaluated twice: by shoelace on the original word and by adding the $c$ removed triangles to the areas of the horizontal slices of the remainder. Both counts must agree. The signed population forces the tile count to be an odd multiple of $c$.

There remain 42 necessary words at 3431, with area counts $925,999,1073,1147,1221,1295,1369,1443$. There remain 109 necessary words for the first 5063 inventory, with counts from 1247 to 2021 in steps of 86. Pairwise compatibility of all distant owners and the existence of a rectangle tiling have not been inferred from the slicing tests. The second 5063 inventory uses six directions and remains outside this staircase argument. All counts are for the height-two cell under the stated equality hypothesis.

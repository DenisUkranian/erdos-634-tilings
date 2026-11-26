# A terminal boundary requires sixteen unmatched owners

Write $R=\mathbb Z[\rho]$, $\rho=e^{i\pi/3}$ and $z=(a+b\rho)/c$. Use the standard vertex-phase frame. In axial coordinates $(x,y)$ representing $x+y\rho$, $[p,q]$ denotes the ordinary two-coordinate determinant. Twice the axial area of a tile equals $ab$. Let $d=a-b$. The two input triples are $(33,7,37)$ and $(35,13,43)$.

## Physical strips counted from the unmatched tiles

Group actual long-side half-turn mates into pairs. Each pair fills a parallelogram of sides $a,b$ at a common short height. Its short edge directions lie on two of the three axes at that height. For the full board, subtract the CCW boundaries of the individual unmatched tiles from the exterior boundary. The resulting chain is exactly the sum of all paired parallelogram boundaries. Separate this identity by physical edge direction. This works with holes, split contacts, and any translates because the equality holds as oriented segment chains.

Rotate the selected height to zero. For $e_j=\rho^j$, $j=0,1,2$, give each boundary piece in direction $\pm e_j$ the signed weight $\pm\ell$ at its normal coordinate $t=[e_j,p]$, with $p$ any point on the piece. Call the cumulative sum up to $t$ the width $W_j(t)$. It measures only the pairs using axis $j$. Their opposite sides contribute a positive jump at the lower supporting line and an equal negative jump at the upper one. The separation is the other side length, since the axial determinant of distinct unit axes has absolute value one. Therefore for actual starting offsets $u_i,v_i$,
$$
W_j(t)=a\sum_i {\bf1}_{[u_i,u_i+b)}(t)+b\sum_i {\bf1}_{[v_i,v_i+a)}(t).
$$
In particular every value belongs to $a\mathbb N_0+b\mathbb N_0$. Its integral $J_j$ equals $ab$ times the number of pairs using this axis. It can also be calculated as the sum of $[p,q]$ over all directed residual pieces parallel to $e_j$, by summing the first moments of the jumps with a minus sign. With $K$ pairs this gives $0\le J_j\le abK$ and $\sum_j J_j=2abK$ at a single height.

There is a second necessary condition. In each direction separately take the endpoint differences $[q]-[p]$ of the residual directed pieces after projecting to the torus $\mathbb R^2/sR$, for $s=a,b$. Each pair gives zero. Edges of length $s$ close on the torus. The other two edges are opposite translates by a period. Endpoint differences respect subdivision. This argument holds for real translates. Reduction to integer residues below is made only for the connected contour.

The same identities apply to any selected union of actual pairs. In `control143.py` the exterior and all unmatched triangle boundaries are the input on the left. On the right the checker reconstructs each pair and compares interval values at every change of support and all integrated counts. It also checks every direction-labeled endpoint coefficient on both tori after rotating each class by its own inverse height. Both complete 143 tilings have 23 unmatched tiles, 60 pairs and six physical classes to check.

## Why the small cut has one positioned tour

Take an occupied exterior-free terminal short node of either prime tree. For the increasing tree rotate its short height to zero so the parent has relative height $-1$. For the decreasing tree use complex conjugation after normalization and orient the image boundary CCW. The congruence class of the board is immaterial to this local calculation. The root's inward long-edge alphabet is now $D\rho^j$, where $D=a+b\bar\rho=(a+b)-b\rho$; the other bank's effective edges are $c\rho^j$. Call these low and high respectively **by effective long-edge height**. The low letters are the selected root tiles and the high letters are reversed long edges of parent tiles. Every outward long side in the terminal node has a whole half-turn mate. Inward whole mates cancel as well. The signed cut identity identifies the boundary of the entire terminal union with these two banks of remaining unmatched edges. Deleting the individual low owners leaves exactly the physical parallelogram pairs within the root. See the [terminal translate proof](../../../2026-11-20/semiprimes/continuation/common-obstruction/terminal/TERMINAL_TRANSLATES.md) and [signed cut identity](../../../2026-11-20/semiprimes/continuation/charge-transport/flux/SIGNED_CUT_TRANSPORT.md).

Suppose there are $m<16$ owners. The previous [exterior-free area and parity bounds](../boundary-word/README.md) give $m=10,12,14$ for 3431 or $12,14$ for 5063. In particular $m\le14$. The perimeter of the union is at most $mc$. The isoperimetric inequality gives $n\le (mc)^2/(\pi\sqrt3\,ab)<6c$ for its population, as checked with $\pi>3.1$, $\sqrt3>1.73$. The earlier terminal theorem gives $n\ge2c$.

The finite graph of directed *whole* edges has balanced endpoint divergence, even when distinct edges intersect or overlap partway. Each endpoint-connected component has an Euler tour. For one such closed tour $J$, use its integer winding number to weight every tile of the full tiling. This weight is constant in each tile interior since every tour segment is a supported tile side. It vanishes outside the board. Across a generic point of a side the jump is the oriented multiplicity of the tour there. Subdivision at all vertices and crossings therefore recovers $J$ as the sum of the weighted CCW tile boundaries. Its signed area $n_J$ in tile units is the sum of the weights.

Let $L,H$ be the signed counts of even minus odd direction exponents in the two alphabets of $J$. The ordinary and height-alternating boundary characters on the weighted tile boundaries give
$$
(c-d)\mid c(L+H),\qquad(c+d)\mid c(L-H).
$$
Indeed each CCW tile contributes $(d-c)\epsilon$ and $(d+c)(-1)^h\epsilon$, respectively; the two effective alphabets have consecutive heights. Rotating a frame only changes an overall character sign. Both divisors are coprime to $c$. Since $|L-H|<c+d$, we have $L=H$. Since $c-d$ is odd, it divides $L$. A nonzero $L$ would use at least $2(c-d)>14$ letters. Thus both characters vanish. The ordinary weighted signed tile population is zero, and reducing modulo two gives $2\mid n_J$.

With the tour translated to zero, every determinant of two of its original steps is divisible by $c$. Same-alphabet determinants are multiples of $c^2$ and mixed ones have a factor $c$. The shoelace sum thus gives $c\mid abn_J$, hence $c\mid n_J$. Moreover its two bank displacements $Dx,cy$, with $x,y\in R$, satisfy $Dx+cy=0$ and $|x|=|y|$. If $x$ were invertible modulo $cR$, then $D$ would vanish there. Its two displayed coordinates rule this out. The inverse-by-conjugation formula now gives $c\mid |x|^2$. Each bank has even size and one has at most six letters. Hence $|x|=|y|\le6<\sqrt c$, and $x=y=0$. In either bank zero displacement and zero character force all three signed axis counts to vanish, by the [signed-axis formula](../boundary-word/README.md).

Any nonzero-area component uses at least 10 or 12 letters, respectively. Indeed $|n_J|\ge2c$, the perimeter bound holds for absolute signed area of a closed walk, and its length in letters is even. For a nonsimple polygonal walk one may split at intersections, sum simple signed areas, and use $\sum P_i^2\le(\sum P_i)^2$. The total area is positive, so exactly one component has nonzero area. Every other component has at most four letters. Its signed axis counts vanish in each bank. Consecutive opposite steps would coincide along a whole side and their two owners in the same bank, with fixed hand and short height, would be actual half-turn mates. Thus cyclically consecutive inverse steps are impossible. A cyclically reduced four-letter word with zero signed axis counts must form a nondegenerate parallelogram: the two nonparallel generators alternate with their opposites. Distinct bank axes are nonparallel. Its area is nonzero. This rules out every extra component.

The resulting single tour has $n=2c$ or $4c$. Both alphabets occur, since a one-alphabet tour has shoelace sum divisible by $c^2$, contrary to $c^2\nmid abn$. Rotate the cycle to start with a low letter preceded by a high letter, rotate the plane by a unit to make that low exponent zero, and translate the starting point to zero. The tour now has integer vertices in this one frame. Arbitrarily translating separate cycles would not have justified the strip or torus tests.

## Exhaustion of the remaining small words

A low long step $D\rho^j$ has an interior owner with third vertex $p+a\rho^j$ when its start is $p$. Subtracting its CCW boundary replaces that step by $a\rho^j,b\rho^{j-1}$, in that order. A high step stays $c\rho^j$. The modified contour equals the sum of the boundaries of $K=(n-\#\text{low})/2$ actual pairs. It may self-intersect as a walk; all the physical strip and endpoint tests are chain identities.

For a word of length $2r$ split at the midpoint. Start the first half and the reversal of the last half at the same origin. Reversal negates every direction and reverses the order of the two short pieces of each repaired low step. Necessary equalities for the halves are equality of all six original signed axis counts, equality of both direction-labeled endpoint currents on the two tori, and a difference of original shoelace sums equal to $abn$. Separate absolute placement of the halves is unnecessary because their original start and end agree.

`word_join.cpp` adds fixed integer weights modulo $2^{64}$ to these integer equalities, and looks up every first half with the required sum. Equal data always have equal sums, irrespective of collisions. The bit filter is populated from every first-half key; all passes undergo a sorted equal-key lookup. Every collision can only add a candidate. All cyclically reduced words in the normalization above are included. Each emitted candidate is checked by the exact width test in `terminal.py`.

The second calculation in `area_review.cpp` uses exact integer tuples. It joins on signed axis counts, original shoelace sum and three repaired directional moments modulo $ab$. It tests $0\le J_j\le abK$ on the full words. Then `review_terminal.py` calculates every individual endpoint coefficient on both tori and tests the strips. It does not use the weights or bit filter.

| $c$ | Contact owners tested | Words after the first join, before the width test | Words passing all tests |
|---:|---:|---:|---:|
| 37 | 10, 12, 14 | 0, 0, 44 | 0, 0, 0 |
| 43 | 12, 14 | 0, 0 | 0, 0 |

The second calculation obtains the same counts after its exact endpoint test. This proves $m\ge16$ for every occupied exterior-free terminal short node of either target.

## Charging these tiles to the board

Use the two physical cuts on the path from the axial exterior to the slant exterior, with sizes $m_1,m_2$ and residual signed populations $D_{\rm res}$ in the three intervening regions, as defined in the [nested-cut theorem](../boundary-word/README.md). In one tree each unmatched tile crosses a unique edge. For $s$ occupied exterior-free nodes, of which $t$ are terminal, their entering edges are distinct from the two designated cuts. Finiteness gives $t\ge1$ when $s>0$. If $C$ is the previous per-node floor (10,12 respectively), then
$$
M\ge m_1+m_2+\max\left(\|D_{\rm res}\|_1,16t+C(s-t)\right).
$$
Take the maximum separately over the two trees, since those trees can charge the same tile. Substituting 16 in the existing exact direction-inventory enumeration gives $M\ge123$ for 3431 and $M\ge165$ for 5063 whenever either tree contains an occupied exterior-free short node. Below those thresholds the existing spine dichotomy forces all three native short-cell classes as the only possible locations.

## A local sharpness check

The previous [3431 strip](../../../2026-11-21/semiprimes/charged-branches/BALANCED_SHORT_STRIP.md) has 74 interior tiles with two unmatched end tiles and fourteen parent owners. For 5063, the corresponding previous strip needed 26 parent owners. The new contact word, with low letters encoded by $j$ and high by $6+j$, is
$$
0,\ 1^6,\ 9,\ 3,\ 4^6,\ 6
$$
where superscripts mean repetition. It bounds 86 actual root tiles. Fourteen are unmatched and 36 half-turn pairs fill the remainder. Two parent tiles supply the other bank. The root has 43 tiles of each sign. After shifting by $(400+1/43,100)$ all 88 tiles lie strictly inside the specified board. The vertex-phase tree calculation places the root in a single exterior-free class, with both parent long sides at that class. The outer boundary after adjoining the parents uses only axes of the parent height. The checker reconstructs congruence from the original tile representation, checks every pair for positive-area intersection, and verifies the complete oriented line currents of the root against the word. This permits a two-owner parent bank locally. The complement of the target board is not tiled by this certificate.

## Exact signed-bank alternatives below the nonnative threshold

In the native regime the [closed-gate theorem](../../../2026-11-20/semiprimes/continuation/global-closure/spine/CLOSED_GATES_AND_NATIVE_THROUGH.md) puts every unmatched tile on an open long gate. It therefore crosses exactly one of the two distinguished edges in the increasing tree. In particular $M=m_1+m_2$ and all six entries of the residual signed-population vector vanish, even when these two boundary populations are above their respective lower bounds.

Retain the notation $(p_1,q_1,p_2,q_2)$ for signed banks in the [nested-cut equations](../boundary-word/README.md). Setting the residual vector to zero gives $O_2=0$, $O_1=-c$, $E_1=E_2=p_2=ck$, $q_1=-d-ck$ for an integer $k$. Substitution into the two character identities gives
$$
(p_1,q_1,p_2,q_2)=(-2c-dk,\,-d-ck,\,ck,\,c+dk).
$$
Consequently $M=|p_1|+|q_1|+|p_2|+|q_2|+2r$, where $r$ sums the lesser of the positive and negative counts in each of these four physical banks. This is a sign count and does not identify any of these tiles as geometric mates.

| Board and hypothesis | $k$ | Signed physical banks | Permitted $r$ after the junction test |
|---|---:|---|---|
| 3431, $M<123$ | $-1$ | $(-48,11,-37,11)$ | $1,\ldots,7$ |
| 5063, $M<165$ | $-1$ | $(-64,21,-43,21)$ | $0,\ldots,7$ |
| 5063, $M<165$ | $0$ | $(-86,-22,0,43)$ | $0,\ldots,6$ |

The list is exhaustive under the indicated hypotheses because $|ck|\le M$ and the absolute bank sum cannot exceed $M$. `native.py` also checks the previously proved displacement floors on both cuts. For 3431 the exclusion of $r=0$ is proved in [the junction calculation](JUNCTIONS.md). For 5063, $k=0$ allows a balanced height-two component. Both complete 143 controls realize the corresponding four-bank formula at $k=0$, with tuple $(-14,-2,0,7)$ and $r=0$. These alternatives leave all higher-$M$ cases subject to the general regional and phase budgets.

# Nested phase cuts and the physical population of a slant boundary

26 November 2026. Both original counts remain **OPEN**. This checkpoint uses main at `c30ad572d5ef98a92d421afc8c48b2ac8ea9fd77`. All heights and signs below are in the standard vertex-phase frame.

Let $M$ count tiles without an actual half-turn mate across the entire long side. A full-side reflection across that side is still counted unless it is a half-turn mate. The following bounds hold for complete tilings of the specified F2 boards with arbitrary translations, reflections and T-junctions.

| Board | Every tiling | If any occupied short node is exterior-free in either prime tree | At the lowest possible value of $M$ in our bound |
|---|---:|---:|---|
| 3431 | $M\ge107$ | $M\ge117$ | The height-two cell has 925 to 1443 tiles, in steps of 74 |
| 5063 | $M\ge149$ | $M\ge161$ | In one of the two possible height-two direction inventories, its cell has 1247 to 2021 tiles, in steps of 86 |

Thus a small unmatched population forces all tiles into the three native cells in both trees. This is a deduction from two physical cuts and the area of a remote branch. Membership in three native cells by itself does not give the older two-height bounds 555 or 731. No computation below uses those bounds. No row asserts existence at the lower bound.

## Two nested cuts

Write $d=a-b$, $A=b(2a+b)$, $B=a(a+2b)$, $z=(a+b\rho)/c$. The vertices are $O=0,X=A,Y=B\rho$. In either prime tree take the two edges joining the nodes of the axial exterior and the slant exterior. At the edge of physical heights $k-1,k$, let $S_k$ be the component on the slant side, for $k=1,2$. Thus $S_2\subset S_1$. In the decreasing tree these are complements of rooted subtrees. Exactly one complete CCW exterior side, $X\to Y$, is assigned to each component. Write $E_k,O_k$ for its signed even- and odd-short-height populations. Each is divisible by $c$ because it is a sum over exact short nodes omitting the exceptional core. The corresponding whole-board values are $-d,-c$.

Let $p_k$ count signs of tiles going from the high short node to the low long node across this particular cut. Let $q_k$ be the opposite bank's signed count. Write $m_k$ for the number of actual unmatched tiles in these two banks together. The cut chain is the exterior slant plus the high bank's CCW long edges minus the low bank's CCW long edges. Taking the component on the slant side gives this same identity in either tree. For a complement, subtract the rooted identity from the whole-board boundary identity, exchanging the two banks. The ordinary and alternating characters give

$$
p_k-q_k=(c-d)(E_k+O_k)/c-c,\qquad
p_k+q_k=(-1)^k\big[(c+d)(E_k-O_k)/c+c\big].
$$

The vector to be supplied by the crossing edges is $Y\to X$, of length $c^2$. Consequently $m_k\ge c$, $m_k\ge |p_k|+|q_k|$, and $m_k\equiv p_k+q_k\pmod2$. Half-turn mates cancel in the same bank. The two cut edges count disjoint physical tiles.

Partition the board tiles by short node into the complement of $S_1$, the difference $S_1\setminus S_2$, and $S_2$. After accounting for the actual unmatched banks, the even and odd residual charges, respectively, are

$$
D=(-d-E_1-q_1,\ -c-O_1,\quad
E_1-E_2,\ O_1-O_2-p_1-q_2,\quad E_2-p_2,\ O_2).
$$

Indeed the low bank of cut one has short height zero. The high bank of cut one and the low bank of cut two have short height one. The high bank of cut two has short height two. Both tiles of a half-turn pair always have the same short node, height and opposite signs, including off the spine. Therefore the six residuals must be paid for out of the remaining unmatched tiles, giving the unrestricted bound

$$
 M\ge m_1+m_2+\sum_i |D_i|.
$$

For a finite verification of a lower bound, test $M\le L=3c+d$. Any larger $M$ already exceeds the claimed floor. On either cut $(|E_k|+|O_k|)/c\le\lfloor L/c\rfloor$, since the unmatched population pays for both charges. The checker `nested.py` loops over this entire integer diamond, not over a catalogue of geometric placements. The two target minima and the unique quadruples at those minima are

| Board | $p_1,q_1,p_2,q_2$ | $m_1,m_2$ | All six residuals |
|---|---|---|---|
| 3431 | $-48,11,-37,11$ | $59,48$ | zero |
| 5063 | $-64,21,-43,21$ | $85,64$ | zero |

The earlier signed-cut paper exhibited these two formal assignments and explicitly left their minimum and geometry open. The calculation here proves the lower bound and its equality conditions. All unmatched tiles at equality occur on the two distinguished edges, in each tree separately.

## Paying for exterior-free cuts

If an exterior-free subtree is occupied, it contains at least $2c$ tiles. Its boundary is the sum of its two banks of unmatched whole long sides as oriented chains. Cancellation can shorten the perimeter, hence perimeter is at most $cm$ for $m$ unmatched tiles on that cut. The planar isoperimetric inequality, applied to all components (holes only increase perimeter for fixed area), gives
$$
 c^2m^2\ge 4\pi(2c)\,ab\sqrt3/4.
$$
If $m<c+d$, the alternating cut equation forces the alternating subtree charge to vanish, since its nonzero units cost at least $c+d$ unmatched tiles. Then $p+q=0$ there and $m$ is even. Using only $\pi>3$ and $\sqrt3>12/7$ gives $m\ge10$ for 3431, $m\ge12$ for 5063. This argument also covers a subtree with balanced signs and internal T-junctions.

Let $C$ be that floor. If this tree has $s$ distinct occupied exterior-free short nodes, their entering edges count disjoint populations outside the two distinguished crossing classes. Thus one may replace the last term of the nested bound by $\max(\|D\|_1,sC)$. Apply it separately in the tree that contains the exterior-free node.

The sharper calculation in `remote.py` includes the exact displacement in each distinguished cut. Rotate away the factor $z^{k-1}$; the displacement then has the form $c u+(a+b\rho)v=z^{1-k}(A-B\rho)$ for axial integers $u,v$. Enumerate $v=x+y\rho$ of hex norm at most the candidate budget, and test integral $u$ by division. For a bank of displacement $(x,y)$ in its own units and character $s$, the signed multiplicities along headings $0,2,4$ are uniquely $(t+x,t,t-y)$ with $3t=s-x+y$. The characters of the low and high *direction alphabets* are $-p_k,q_k$, respectively, because the latter bank is reversed in the cut chain. The sum of absolute multiplicities lower-bounds the gross number of steps. This enumeration gives $M\ge117,161$ for $s\ge1$. It includes both prime trees because it uses physical heights and the component facing the slant.

The existing two-tree classification then puts every tile in $R,A+zR,A+z^2R$ at short heights 0, 1, 2 if $M<117,161$, respectively. No additional universality is assumed for this classification. The 45/58 ordinary-node budgets, joint-cell reserves, terminal divisibility and gate theorem remain available under their original hypotheses. In particular $sC$ counts unmatched owners of real boundaries and cannot be added to the earlier ordinary-node population floors as though those were different tiles.

## Geometry beyond scalar charges

[Boundary words and area spectra](WORDS.md) derives a global necessary word for each cut, including the slant side. It also gives exact small-excess area spectra for a slant component whose even and odd charges both vanish. For example a balanced increasing-tree slant component with more than 2812 tiles at 3431 or more than 2236 at 5063 needs at least 51 or 57 unmatched crossing tiles, respectively.

[The equality case and the remaining rectangular region](RECTANGLES.md) uses a different, charged slant component. It proves the population restrictions in the first table from actual whole-tile owners, paired rectangles and modular conditions on the boundary word. The second angular inventory at 5063 is retained.

## Reproduction and scope

Run `python3 replay.py` in this directory, using standard Python with assertions enabled. The geometry control reconstructs two complete 143 tilings, checks the six residuals in both trees and rebuilds translated closed words from actual directed edges on all 46 induced cuts across the two tilings. Both have 23 unmatched tiles. The balanced slant component of each 143 example is empty and has seven crossings. It tests the zero-area boundary case; it does not supply a positive-area instance of the target equality case. An independent inventory computation and skeleton enumeration cross-check the area exclusions.

These results leave larger unmatched populations and the native equality candidates open. For the reference classification and the geometric inputs see the [spine theorem](../../../2026-11-20/semiprimes/continuation/global-closure/spine/SPINE_DICHOTOMY.md), [signed cut transport](../../../2026-11-20/semiprimes/continuation/charge-transport/flux/SIGNED_CUT_TRANSPORT.md), [common obstruction](../../../2026-11-20/semiprimes/continuation/common-obstruction/README.md) and [regional contact theorem](../../../2026-11-21/semiprimes/through-contact-closure/README.md). No new classification of tile shapes is needed for these F2 necessary conditions, and no closure of either original number follows.

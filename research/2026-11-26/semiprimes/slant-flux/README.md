# The slant contact and the two axial walls bound the number of occupied lifts

Let C be the axial lift, B the middle lift, T the slant lift, and R the number of occupied short-tile lifts other than C in the positioned joint-cell tree. Write n_C for the population at C and K = (N − n_C)/c − 2R. Every complete tiling of the specified F2 board satisfies the following bounds.

| F2 tile | N | Maximum R | Further necessary condition |
|---|---:|---:|---|
| (33,7,37) | 3431 | **41** | If K = 6, then n_C ≥ 175. |
| (35,13,43) | 5063 | **53** | K ≥ 8. If B is the only charged ordinary lift, it contains at least 473 tiles. |

Both original counts remain **OPEN**. The estimates hold with arbitrary contact subdivisions, hands, heights and admissible translates. The quantitative inputs from earlier work are the [positioned tree](../joint-cell-tree/TREE.md), [individual gate capacities](../joint-cell-tree/BRANCHING.md), [signed cut equations](../charge-variation/README.md) and [axial and ordinary population estimates](../axial-reserve/README.md).

## 1. Two physical banks must supply the displacement of a whole board side

Work in the reflected path frame with the board vertices 0, c² and H z², where H = a(a+2b), ρ = exp(iπ/3), z = (a+bρ)/c, and U_j = ρʲ. The slant side in the standard frame is the directed base from 0 to c² in this frame. C, B, T have short heights 2, 1, 0. In short coordinates let q be the obtuse vertex, u = q − aU_j, w = q + bU_(j+s), with hand s = ±1. The signed population counts each tile with sign s(−1)ʲ.

Cut the positioned tree at B–T and take the union of tiles on the T side. The cut-chain theorem gives its boundary as the exterior slant plus CCW whole long edges of T→B owners minus CCW whole long edges of B→T owners. This follows by subdividing at all physical contact endpoints and canceling each internal pair of intervals. The lifted side marker is common to both incident tiles even at a subdivided contact. All other lifted edges lie on one side of the cut. The CCW long edge is −s c z^(h+s) U_j at short height h. Thus summing displacement and dividing by c gives the exact vector identity
$$
  \sum_{B\to T} U_j + \sum_{T\to B} zU_j=c.
$$
It also holds when the T bank is empty. An exterior-free balanced branch can contain tiles on either side of the cut. The formula counts its contribution via the actual bank owners.

On an ordinary lift, the axis-wise sum of periodic short-edge endpoint differences vanishes. Complementary whole long edges have equal endpoints modulo c in the appropriate chart. The full exterior segment at T also has equal residues. Apply a real linear functional to the displacement identity and bound its two bank sums *separately*, retaining the signed current at each gate.

Explicitly at 5063, write a gate vector Q in the order used in the [full-torus checker](duals.py). The first c labels are the negative hand at residue Re_ax((a+bρ)u), and the next c are the positive hand at Re_ax((a+b bar(ρ))u), all modulo c. Here Re_ax takes the first axial coordinate. The last 2c entries of each saved potential are its gate weights λ. Put W_B = sum of 2 Re(c U_j) over B→T, and W_T = sum of 2 Re(c z U_j) over T→B, with ordinary Euclidean real part Re. Then W_B+W_T=2c². Testing the four short endpoints, the sign and the native long edge of every one of 12c² tile columns gives
$$
  100000(2c^2)\le 17145280\,n_B+2400002\,n_T
       -\lambda_B\cdot Q_B-\lambda_T\cdot Q_T .
$$
The native gate is at residue zero on each bank in the path chart. The boundary and population coefficients do not require the other gate currents to vanish.

For example, if B has only the signed native currents (+43,−43) in axial, slant order, T has all signed currents zero, and n_B ≤ 258, n_T ≤ 86, the two upper bounds on 100000 times the projection are **81,147,407** and **206,400,172**. They total 287,547,579, strictly below the required 369,800,000. This rules out the case even if the signed-zero gates have physical owners.

A second full-torus table for B with only native signed currents (+86,−43) gives n_B ≥ 40129535/100002. For this table alone, normalize the positive axial current to the negative hand by q ↦ −bar(q), preserving signs. The local source is zero and the two native gates still have residue zero. The odd block parity implies **n_B ≥ 11c**. In particular this holds if B is the only charged ordinary lift.

## 2. Enumerating small excess budgets without assuming a bounded tree

Use the path-frame corrected charges g_C=(G_C−d)/c and g_v=G_v/c otherwise, where d=a−b. The odd sum is 1 and the even sum is 0. Mark C,T and all charged ordinary lifts. Retain the spine C,B,T in their minimal subtree. Off the spine retain every charged lift and every branching lift, and suppress only uncharged one-child vertices. A suppressed segment records one distinct incident gate direction at each retained endpoint. All directions outside the marked subtree have signed current zero by the full cut equations. No physically occupied branch is asserted removable from a tiling.

At K ≤ 8 every off-spine leaf consumes at least three extra blocks, by the earlier single-signed-gate bound. Thus at most two such leaves exist. The retained tree has degree at most four, counting the possible leaves C and T. No retained ordinary lift is monochromatic since all its owners would have to use at most four gates, each with capacity at most α times its population, with 4α < 1 on both boards. Each charged ordinary lift therefore spends at least one extra block. If there are m retained off-spine vertices, l leaves and f uncharged branching vertices, they spend at least m+2l−f blocks. For nonempty branches f ≤ l−1 by the rooted-forest degree sum. Hence m ≤ K−2.

The [census](hull.py) generates all labeled attachment forests up to that size. Successive off-spine vertices take any earlier parent, including any of C,B,T. Either parity is allowed across suppressed segments. Block counts at retained ordinary lifts are 2 plus nonnegative extras totaling at most K. Empty B or T can be relaxed to balanced capacity 2c with zero extra. All possible nonmonochromatic charges of the required population parity are tried. At least one charged lift requires at least 5c by the earlier result. In particular the census can require that some retained capacity is at least 5c. For each direction write e,o for the far corrected even and odd sums. The required signed currents are
$$
 q_{\rm odd}=d e-c o+2cI_C-cI_T,\qquad
 q_{\rm even}=d o-c e-dI_C.
$$
At C the outgoing current on each off-spine direction is d o−c e from the exterior-free cut, and the current toward B is d+c g_C minus the other currents. These are disjoint signed gates of one physical lift.

The checker applies both sign budgets, the individual gate capacities and the previously certified one-gate, native and four-block tests. At B it preserves the native directions in axial, slant order. For 5063 it then applies the [780 integer endpoint inequalities](../../../../research/2026-11-21/semiprimes/MINIMAL_ODD_EXCLUSION_5063.md#4-an-exact-dual-inequality-valid-for-every-physical-placement). Their per-tile bounds hold at any population, with the right side equal to the actual lift population times the per-tile constant. Independent residue shifts of the two gate arrays are realized because the two gate forms are linearly independent modulo c. For two identical extra currents every unordered pair of distinct nonnative labels is tested. The implementation may pass larger stars untouched to the axial test. At 3431 it uses 11 projected integer inequalities verified on every projected column, allowing every extra residue and either hand.

At 5063 with K ≤ 7 exactly 38 relaxed profiles enter the translated tests. Two remain. One has a nine-block B with native currents (+86,−43), excluded by the eleven-block bound. The other has a six-block B with (+43,−43) and a two-block, zero-current T, excluded by the two physical bank sums. This proves K ≥ 8. With n_C ≥ 75 it gives R ≤ 54. Equality would require n_C = 75, K = 8 and g_C = −1 by the previously proved sign split at 75.

## 3. The core sees both its native gate and an ordered pair of walls

Switch explicitly to the **standard frame** for C. The board is 0,A,Hρ with A=b(2a+b). The map to path coordinates is
$$
 x\longmapsto H z^2-\rho z^2\bar x.
$$
It sends h to 2−h, j to 4−j and s to −s. In particular it reverses every signed gate total. The incoming middle direction at C has standard hand +1. In standard short coordinates its normalized gate label is
$$
 (u_x-a b^{-1}u_y)\bmod c=-aH b^{-1}\bmod c.
$$
Indeed the negative-hand path form on H−ρ bar(u) equals aH−(a u_y−b u_x). The other standard hand uses u_x−b a⁻¹u_y. The order of the gates in the next table is native followed by the one other nonzero gate, if present.

| Situation | Candidate standard signed gate currents at C |
|---|---|
| 5063, R=54 | (43,−22), (21), (0,21) |
| 3431, K=6 and n_C≤101 | (37,−26) |
| 3431, K=7 and n_C=64 | (0,−26), (−26) |

These are outputs of the complete relaxed census followed by the middle filters. In the 3431 six-block case the census forces g_C=−1, and only two of the nine relaxed profiles survive the middle tests. In the seven-block case the minimum-core signs force g_C=0, and two of eight eligible profiles survive. The single coordinate projection on each hand records every signed gate for that hand and the total signed current of the other hand. The core endpoint source is the directed difference on 0→A and Hρ→0, retaining their distinct axes. Testing the projected integer potentials with that source eliminates every row and every nonnative translation except the 3431 six-block case at positive-hand labels 0, 26 and 27.

For these last three positions use both endpoint coordinates and a directed path of integer positions on each entire wall. From position i there is a step of length a, b or c whenever it stays on the wall. A length-c step has zero cost and uses no core owner in this relaxation. An a or b step is assigned one of its two possible oriented core tiles. In standard directions the sign of an a owner on these walls is positive and that of a b owner negative. A triangle cannot contribute a short edge to each wall because the two short edges have opposite directed characters and the two walls have the same directed character. A long edge touching a supporting wall in a positive length lies fully on that wall; the same holds for a short edge. Thus an actual tiling supplies two paths and each paid step consumes a distinct actual core tile.

Add the difference of the two wall-state weights to the usual core tile score whenever the tile pays a step. Their sum telescopes on both complete paths. The three exact bounds on n_C, in label order, have numerators **11613747, 11622392, 11603626**, all with denominator **100002**. A second calculation discards the wall-state potentials and finds the minimum deficit by shortest paths over every wall word and both owner choices. Its three numerators are at least as large. This proves n_C > 101 in all the remaining positions. Since at K=6 the standard signed core population is 11 and n_C ≡ 27 mod 37, the next possible size is 175.

Finally R ≥ 42 at 3431 would give n_C+37K ≤ 323. The previous n_C≥64 and K≥6 leave only K=6 with n_C≤101 or K=7 with n_C=64. Both alternatives are excluded above. At 5063 all three possible core gate profiles for R=54 fail, so R≤53.

## Replay and scope

From this directory run `python3 replay.py | diff - STATUS.json` with NumPy and assertions enabled. The replay uses integer inequalities and complete finite residue ranges. All new potentials are in [potentials.json.gz](potentials.json.gz). The [coordinate checks](check_coordinates.py) reconstruct both complete 143 examples, their actual lifted bank owners, the native core gate, the two wall paths and the physical slant displacement. In each example the B-bank alone supplies (49,0). Constants and tables specific to 37 or 43 are checked at their own moduli. The new cap leaves lower values of R available on both boards. Excluding these values or proving some further condition independent of R is still necessary for an unrestricted negative answer.

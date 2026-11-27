# A gate displacement bound and the cost of hidden charge

Both original F2 counts are open. The base is main at `b220f08ce94ed0f5536be3ad1edb57416af1d102`. All statements below concern the positioned joint-cell tree of an arbitrary complete tiling, with whole long-edge owners and physical T-junctions. Use one tree throughout a count.

Let C be the axial lift, B the middle lift and T the slant lift. Let R count the occupied lifts other than C and write n_C for the population at C. Define K=(N−n_C)/c−2R. Keep the two spine edges. Of the other edges keep exactly those on which the two parity sums in the exterior-free side are not both zero. Call a nonempty edge component of this forest away from the spine a *detached component*. Let F count these components. For such a component H let E(H) be the sum of n_v/c−2 over its vertices.

| Necessary in every tiling | 3431 | 5063 |
|---|---:|---:|
| K minus the sum of E(H) | at least **7** | at least **8** |
| R plus half the sum of E(H) | at most **41** | at most **53** |
| E(H) for each detached component | at least **6** | at least **6** |
| Unmatched tiles on the internal edges of H | at least **126** | at least **130** |

In particular N ≥ n_C + c(2R + 6F + 7) or n_C + c(2R + 6F + 8), respectively. At equality E(H)=6 the entire component is a three-vertex path with populations 5c, 2c, 5c. This last conclusion bounds the length even when no bound on the number of balanced intermediate lifts is assumed. Neutral edges and the physical tiles on them still exist.

## Displacement at a single gate

In a short-lift chart write U_j=ρʲ for the six unit directions, ρ=exp(iπ/3). A tile has obtuse vertex q, short endpoints u=q−aU_j, w=q+bU_(j+h), hand h=±1 and sign h(−1)ʲ. At any one incident gate put L=ΣU_j over its tiles, including paired tiles if desired. This is the physical bank displacement in its own long-edge mesh units up to an overall orientation sign. Define the hexagonal norm of (x,y) as max(|x|,|y|,|x+y|). Then

    2 ||L|| ≤ n_v + 2·1[v=C].

This uses the entire population at the short lift. It requires neither a signed-current assumption nor a second gate. In the chart of a negative-hand gate translate its label to zero. Project to φ(x,y)=x−(b/a)y modulo c. The negative gate label of a tile is φ(u). Project each short endpoint difference separately on its axis. For the length-a side add h([q]−[u]) on axis j and for the length-b side add h([w]−[q]) on axis j+h, with axes read modulo three. Summation gives zero at an ordinary lift by the [localized endpoint identity](../axial-reserve/README.md). A full exterior slant returns to its initial residue. At C the two complete axial walls supply the two endpoint differences.

Give weight −1 to (axis 1, residue 0) and (axis 2, residue a), and zero elsewhere. For each individual tile add its weighted short-endpoint score to 2(x_j+y_j) if it uses the chosen gate, where U_j=(x_j,y_j). This sum is at most one. The [integer verifier](replay.py) substitutes the 12c combinations of φ(q), j and h. The same two entries work on both boards and on the 143 control. Each axial wall can change the summed endpoint score by at most one. Summing gives the inequality in the x+y direction. Rotating the chart gives the six supporting linear forms, and conjugating gives the other hand. Rotations through 60 degrees may reverse the sign convention for signed populations but no signed current occurs in this inequality.

**Native consequences.** If the B-owned bank has zero *displacement* on a native cut, its opposite bank supplies the entire slant. In middle-mesh units its vector is D=(a+b,−b). Thus n_C≥2(a+b)−2 at the axial cut, or n_T≥2(a+b) at the slant cut. The core residue forces n_C≥101 or 118, respectively by board. The ordinary block condition forces n_T≥3c on either board. A cancelling B bank and a bank of two unmatched B owners both have zero displacement.

There is a separate result for zero *signed current*. If n_C is its minimum 64 or 75, a zero-signed axial B bank has at least **14** unmatched owners. If n_T=2c a zero-signed slant B bank also has at least **14**. Indeed let (x,y) be its oriented sum in its own long mesh. Its signed net counts on axes 0,1,2 are x+t, y−t, t, where 3t=y−x since its directed alternating character is zero. The sum of their absolute values is a lower bound on the number of owners. In the [reflected native chart](../terminal-contact/TWO_OWNER.md), multiply (x,y) by z or its conjugate according to the cut, z=(a+bρ)/c. The result P is integral since D and the opposite bank are integral. Apply the displacement inequality to D−P. The checker tries every |x|,|y|≤14, which includes every bank with at most 14 owners. It lists the remaining vectors at 14. Existence at 14 is open.

## A balanced two-block lift between two signed gates

Suppose a 2c-tile ordinary lift has currents +c and −c on two gates. The sign budgets force every positive tile onto the first gate and every negative tile onto the second. All of those tiles are unmatched. Opposite-hand sign-exclusive support is excluded by the [short-endpoint peeling proof](../axial-reserve/README.md). For same-hand support use a sign-preserving chart change, normalizing the positive gate to hand minus and residue zero. Give the negative gate each nonzero residue in turn. Each allowed projected tile gives a column of short endpoint differences. If a row has only one coefficient sign, every column using it has zero multiplicity. Repeat to stability.

At 3431 only offsets 3, 4, 30 survive, at 5063 only 5, 8, 30. For *each* surviving offset only one heading for each sign remains, and those headings differ by three. The [replay](REPLAY.json) includes the exact surviving axes. Thus each bank contains exactly c co-directed long sides. On an exterior-free incident edge the opposite bank must supply their full displacement by the [physical cut identity](../joint-cell-tree/TREE.md). In that bank's long mesh it is a rotation or reflection of (a,b), whose hexagonal norm is a+b. If the neighbor is ordinary, it therefore needs at least 2(a+b)>2c tiles. This step uses physical displacement in addition to the two scalar gate equations.

## Separating the source and the detached components

Use reflected path signs, with corrected charge (G_C−d)/c at C, ordinary charge G_v/c elsewhere, and d=a−b. The sum of even corrected charges is zero and the odd sum is one. Write (e,o) for the two block sums beyond an exterior-free edge. The absolute signed currents of its two banks are |ce−do| and |de−co|. The pair vanishes exactly at (0,0). In fact either coordinate vanishing forces both to vanish here, by coprimality and the strict bounds |e|,|o|<c from [parity variation](../charge-variation/ROOTED.md). Endpoints of a kept exterior-free edge are occupied.

On the whole tree consider the two integer flows which send the even and odd charges toward the exterior along unique paths. On every discarded edge each flow vanishes. Summing divergence over a detached component proves that each parity sums to zero inside that component. At a leaf its only kept gate carries the entire nonzero short charge. Its adjacent edge has one far parity sum of magnitude |G_v|/c and the other zero, up to joint sign. There must be at least two leaves and at least two distinct leaf edges: a component consisting of one edge would have one vertex of each parity, contradicting parity neutrality. Each leaf edge therefore pays at least c+d unmatched owners on its two physical banks. Each leaf needs at least 5c short tiles by the [one-signed-gate estimate](../axial-reserve/README.md). This proves the two component floors. Vertices and owner sets of distinct detached components are disjoint. Each E(H) is even by population parity and neutrality.

If E(H)=6, precisely two leaves use the entire excess. They each have 5c tiles and charge of magnitude c by the same single-gate estimate. The component is a path. Any internal short lift has 2c tiles. A charged lift of that size would be monochromatic and would use only its at most two nonzero gates. The [one-gate capacities](../joint-cell-tree/BRANCHING.md) then sum to less than its population. Thus every intermediate charge is zero and the opposite leaf charges have the same parity. If the path had length at least four, its second internal vertex counted from a leaf (distance two from that leaf) would have signed gate currents +c and −c by the cut equations. Its neighbor toward that leaf is an ordinary 2c lift, impossible by the displacement theorem. Hence the path has length two. Its center has two nonzero currents ±d. In the same sign-preserving normalization, the two center gates must have the same hand, with offsets 3, 4, 30 at 3431 or 5, 8, 30 at 5063. The [3431 weights](../terminal-contact/two_gate_potentials.json) and [5063 weights](central_5063.json) give this separate restriction without sign exclusivity: on a 2c center, d times the difference of the two gate weights cannot exceed 2c times the maximum column score. The replay tries every offset and the opposite hand. At 5063 a charged 5c leaf with its sole kept gate toward the spine cannot be physically terminal, by the 83/13 terminal estimate. It has occupied descendants across a zero-current edge.

Let E be the sum of the E(H). Ignore the charges in detached components only when computing the *source* profile. No signed gate in the spine component changes: each omitted component attaches through zero-flow edges and has both parity sums zero. The actual counts of B, C and T and all of their endpoint and wall constraints remain available. The population excess available to retained source vertices is at most K−E. This is an allocation of disjoint costs, not a new tiling with branches erased. The source still has odd total one. In the [small-excess proof](../slant-flux/README.md), the marked source hull has exactly the same degree, leaf, sign, and one-signed-gate tests: the evidence needed for each is the actual population and signed gates of a retained vertex. The arguments at budgets below six likewise use only these data at retained vertices, as in [the original excess proof](../axial-reserve/README.md). Thus the verified source census applies with budget K−E. Algebraically N=n_C+c(2(R+E/2)+(K−E)). The small-core exclusions in the slant and wall theorem give R+E/2≤41 or 53 by the same integer calculation; E/2 is integral. In particular the 5063 source needs at least eight extra blocks even in the presence of detached charges.

The contact payments can also be added to the exterior reserve. Let P_0 denote the previously proved neutral-edge payment (16Z+2I, with the [two-owner increments](../terminal-contact/TWO_OWNER.md) when applicable), and V_S the sum of absolute odd charges in blocks outside the detached components. Then the total unmatched count M satisfies

    M ≥ P_0 + 2(c+d) F + max(A, (c+d) V_S),     A = 107 or 149.

Indeed after counting the zero-current edges, set aside all unmatched owners on the internal edges of every detached component. Their signed sums separately at each parity within that component are zero: all its vertex charges sum to zero by parity, and each removed boundary bank has signed sum zero at its own vertex. Each component lies on a single side of both native edges. The [two native cuts and six residuals](../boundary-word/README.md) still give A on the remaining owners. The odd-vertex variation estimate also applies on the remaining vertices and their incident signed banks as in the [contact reserve](../terminal-contact/REMOTE_BOUNDARY.md). This argument counts a component inside another neutral branch just once.

## The last two six-block profiles at 3431

Use the reflected path frame throughout this section. In the previous exhaustive census at budget six, the only two source profiles passing the middle endpoint tests have B of size 74 with currents (+11,−11) toward (C,T). Their T sectors both have corrected parity sums (1,0). Indeed the signed B-to-T current is 26e−37o−37=−11; the variation bound gives e=1,o=0. The opposite bank at T toward B has signed current +37. The possibilities are as follows.

* T has 74 tiles and gates +37,−37. Two other ordinary lifts have five blocks and signed charge +37 each, one at each parity. All other ordinary lifts in this source profile have two blocks when occupied.
* T has 185 tiles and only the native signed gate +37. One further ordinary lift has five blocks. All other occupied source lifts have two blocks.

In the first case apply the two-gate theorem at T to its nonnative edge. The neighbor beyond this edge is odd and needs more than 74 tiles. No positively charged odd source lift is in the T-sector, which has odd sum zero and no negatively charged odd source lift. Thus this neighbor must be balanced and has only 74 tiles. It cannot belong to a detached component, since this particular edge has nonzero current. This excludes the first profile.

In the second case let (x,y) and (u,v) be the sums of U_j on the B-to-T and T-to-B banks in their respective long meshes. The [slant identity](../slant-flux/README.md) reads (x+yρ)+z(u+vρ)=37. The three [integer potentials](k6_duals.json.gz) count the same short endpoint rows as above, now including the signed gate rows. At B use both torus coordinates modulo 37 and all gate labels of both hands. At T use φ(x,y)=x−a y/b modulo 37 for its active positive hand, and one total for the other hand. Native labels in this chart are zero. Add 10000 times the selected horizontal coordinate of the native heading to the score of each tile at that gate, and bound each column by its actual maximum D. Then 10000 times the bank projection is at most nD minus the sum of the prescribed gate currents weighted by the potential. The [verifier](six_blocks.py) obtains

| Bank projection | Integer upper numerator over 10000 |
|---|---:|
| x at B | 118773 |
| −x at B | 118026 |
| u at T | 321604 |

Rotations by 120 degrees preserve both signs, both zero labels and the homogeneous endpoint rows. The two B bounds therefore give max(|x|,|y|,|x+y|)≤11 by integrality. On the negative-hand B bank the heading character is +11; on the positive-hand T bank it is +37. Since U_j has coordinate difference congruent to (−1)ʲ modulo three, x−y≡11 and u−v≡37 modulo three. The integral vector equation leaves only

| (x,y) | (u,v) |
|---|---|
| (−7,3) | (47,−11) |
| (3,4) | (36,−10) |
| (4,−7) | (37,0) |

Every u exceeds 32, contradicting the independent T projection bound. This removes budget six without any upper bound on the axial population.

## Two-block and five-block slant lifts at the 5063 eight-block threshold

Of the twelve source profiles that pass the earlier middle test at budget eight, four give B-to-T signed current −21. The T-sector then has parity block sums (1,0), and T-to-B has current +43. At B the native current pair is either (+21,−21) at 172 tiles or (+64,−21) at 301 tiles. Each admits two options for T in the earlier census. In the 86-tile option its second signed gate is −43. The other gate leads to an odd ordinary lift in the T-sector, which must supply a displacement of hexagonal norm 48. No charged odd source lift lies in this sector, since all odd source charges in these profiles are nonnegative and their sector sum is zero. All unlisted occupied source lifts have 86 tiles. The neighbor needs at least 96, which excludes both of these profiles.

In the other two profiles T has 215 tiles with only its +43 native signed gate. Repeat the slant projection calculation at modulus 43. Now the integer B projections in the two 120-degree orbits are bounded by 33,33 or 25,25, respectively. At T the positive-x orbit is bounded by 35 and its opposite by 33. A further integer endpoint potential for the T vector (32,−23), with two displacement multipliers, requires at least 2220267/10001 tiles at T. Solving B+zT=43 over integral vectors with heading characters 21 and 43 leaves four possible vector pairs in the 172-tile B case and two in the 301-tile case. The [exact lists](K8.json) are necessary conditions only. The [checker](eight_blocks.py) verifies every column on both banks using the [integer weights](k8_duals.json.gz).

Run `python eight_blocks.py | diff - K8.json`, `python replay.py | diff - REPLAY.json` and `python six_blocks.py | diff - K6.json` in this directory. The first test recomputes all directed gate vectors in both complete 143 controls in two ways, using short-chart tile headings and physical long-edge endpoints after removing actual pairs. The second uses the earlier source census and checks every integer-potential column. The unrestricted floors sharpen the population and contact budgets. Larger source budgets remain, so there is no classification-based closure of either original count.

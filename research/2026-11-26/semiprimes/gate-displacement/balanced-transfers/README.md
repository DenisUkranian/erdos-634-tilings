# Integral displacement on both banks of a signed transfer

The two original counts remain open. The results below concern the positioned lift tree of any complete tiling of the two F2 boards. They use the [source and detached-component decomposition](../README.md). A gate is *physically active* when its bank has an owner left after removing actual whole-long-side half-turn pairs. Its signed current is the sum of tile signs in that bank. A physically active gate can have zero signed current.

| Necessary condition | 3431 | 5063 |
|---|---:|---:|
| Minimum excess E of a detached component | 8 blocks | 6 blocks |
| Maximum number F of detached components | 5 | 7 |
| Minimum population of an exterior-free subtree neutral in both parities and containing a charged lift | 518 | 688 |

The 5063 equality case at six excess blocks requires **at least 222 distinct unmatched owners** incident to its three lifts and at least **five additional occupied outward branches**. These 222 include owners on the component side of its neutral boundary edges. The earlier neutral-edge payment can overlap this part.

## Two signed banks at a balanced ordinary lift

Write d=a−b and z=(a+bρ)/c, with ρ=exp(iπ/3). Assume an ordinary lift of population 2c has just two nonzero signed gates, with values +d and −d. Use the sign-preserving hand normalization of the [two-gate lemma](../README.md). The gates have the same hand. On the negative hand use the residue of the short endpoint under φ(x,y)=x−by/a modulo c. Translate the positive bank to residue zero. The remaining offsets form one orbit under 120-degree rotation on each board. Fix the other residue to 4 at c=37 or 8 at c=43. This preserves the two signs.

For a gate let U=(x,y) be the sum of ρʲ over its tiles in its own long mesh. An actual pair contributes zero. For the negative hand, z⁻¹U must be integral in the short-lift mesh. Indeed the opposite long bank consists of steps c times units in that mesh. The two directed banks differ by the exterior displacement on their physical cut. This displacement is zero on an exterior-free cut. For a native cut the slant in the standard short chart of height h is a unit times c²z^(2−h), divisible by c at the ordinary native heights 1,2. Conjugating or rotating the chart transports this congruence. This argument uses the physical tree cut before taking displacement. The [independent plane argument](../../joint-cell-tree/MOMENTS.md) obtains the same congruence by restricting endpoint divergence. No bound on the total range of heights is used.

If the negative-hand bank has signed current q, its net counts on axes 0,1,2 are x+t,y−t,t with 3t=y−x−q. Indeed U₂=ρ−1, and the current is minus the alternating heading character. Thus its owner cost is at least |x+t|+|y−t|+|t|. Also max(|x|,|y|,|x+y|)≤c by the [gate displacement bound](../README.md). Since the two banks use different tiles, their costs sum to at most 2c. These tests leave 918 or 1566 pairs of integral vectors.

For completeness the finite certificate uses one column for every projected obtuse vertex, heading and hand. Its entries are the signed short-endpoint differences on each axis, the signed bank rows, and the two coordinates of the heading at each selected negative-hand bank. At an ordinary vertex the endpoint rows sum to zero. Signed rows sum to the prescribed two currents and zero elsewhere, with all opposite-hand gates combined. For any table of integers y, a tiling satisfies
$$y\cdot\mathrm{target}\le 2c\max(1,\max_i y\cdot\mathrm{column}_i).$$
The [verifier](transfers.py) checks every column and every remaining candidate. The first pass eliminates all 918 pairs at 3431. At 5063 it leaves four. For three of these, include the two zero-current banks specified in the certificate, enumerate their possible displacements by the same divisibility and remaining-owner bound, and apply the column test again. The [output](TRANSFERS.json) leaves just
$$
 U_0=(-25,3),\qquad U_8=(25,-3).
$$
The corresponding net axis counts on the first bank are (−23,1,2), with opposite counts on the other bank. Each bank needs at least 26 owners. The [integer projected histogram](projected_histogram.json) is an exact 86-tile-count solution of these one-coordinate equations, even with zero displacement on every unmarked negative-hand gate. The verifier sums its columns exactly. Thus a contradiction for this last case must use more than these projected constraints. The histogram assigns no physical positions.

## Physical activity of a five-block leaf at 5063

At an ordinary 215-tile lift suppose exactly one gate has nonzero current, of magnitude 43. Normalize its hand to positive, its sign to positive and its label to zero. A sign-preserving conjugation followed if necessary by rotation exchanges hands, and a half-turn reverses the signed current. There must be at least **three other physically active gates of the same hand**, even if all opposite-hand gates are available. At least 20 unmatched owners lie outside the distinguished gate. If its heading sum in this normalization is (27,−10), the latter floor rises to 42.

As an independent preliminary check of the pair model, allow just one further active gate. If it has the same hand, the normalized labels are 0 and k≠0. Rotation by 120 degrees reduces k to fourteen representatives. Project the short-endpoint rows onto the positive-hand form x−ay/b. If it has the opposite hand, translations can set both active labels to zero since the two forms are independent modulo 43. In this case retain both torus coordinates. Assign integer weights to the homogeneous endpoint rows and to the two signed gate rows with prescribed values 43,0. Unmatched owners may use the two gates. Every other tile must belong to a physical pair. The mate of (q,j,h) has obtuse vertex u+w−q and heading j+3 with unchanged hand, as follows by the half-turn about the midpoint of the long edge [u,w]. The score of any allowed single is at most D, and that of any pair is at most 2D. The target exceeds 215D in every case. A lift with only the distinguished active gate is covered as well.

For the stronger same-hand result, retain all projected positive-hand signed rows and one opposite-hand signed total. Every physical pair and every opposite-hand single is allowed, as are singles on the primary positive gate and on two secondary positive labels. For each integer table set D=floor((43 times its primary weight minus one)/215). Verify the pair bound 2D and the single bound D at the primary label and on every opposite-hand tile. Determine every secondary label for which *all* singles score at most D. The table then excludes every pair of these labels, and also its rotations under 120 degrees about label zero. The 248 tables cover all 861 unordered pairs of secondary labels. This proves the three-extra-gate requirement independently of the torus two-gate test.

For the outside-owner count, keep the signed rows of all positive-hand gates and the total of the other hand, the population row and optionally the distinguished vector. In the supplied tables, the score per actual pair and per distinguished single is at most zero. Every other single scores at most 100000. The two target scores are 1974517 and 4068958. The outside banks each have signed current zero, hence each contains an even number of singles. This proves the two floors. Charging only singles outside the primary gate on its own hand gives respective numerators 1704004 and 3103860, hence at least 18 or 32 same-hand outside owners. All columns, half-turn pairs, label orbits and integer numerators can be checked in [leaf.py](leaf.py) and [LEAF.json](LEAF.json).

In an exterior-free 5c,2c,5c path with E=6, the central bank facing the leaf has current d times the sign of that leaf charge by the [cut characters](../../charge-variation/ROOTED.md). In the common physical chart the CCW vectors at a negative-hand center gate sum to +cz⁻¹U_center, in units of the center's short mesh. Those at the positive-hand leaf gate sum to −cU_leaf in the same units. They agree on the exterior-free cut. For the positive leaf this gives (27,−10); for the negative leaf apply a half-turn. Each main leaf bank therefore costs at least 43, each center bank at least 26, and each leaf has at least 42 other unmatched owners. These four bank populations and the two outside populations are disjoint, giving 2(43+26+42)=222.

For every exterior-free edge, physically unmatched owners force occupancy on the other side. Indeed an empty far side has zero boundary chain and opposite coincident segments of the same length pair along each line (compare consecutive starts of equal-length intervals). A nonempty side with only one mesh represented would give a supported one-alphabet Jordan circuit, excluded by the [supported-cycle theorem](../../terminal-contact/REMOTE_BOUNDARY.md). Thus the three extra same-hand gates at each leaf give six distinct edges outside the three-vertex path. At most one points toward the exterior spine; at least five lead to occupied disjoint outward branches. More generally, let L≥1 count exterior-free even lifts of size 215 with just one nonzero signed gate of magnitude 43. The bipartite graph of these lifts and their occupied odd neighbors is a forest with at least 4L edges. There are at least 3L+1 odd neighbors. They each cost at least 2c and the total odd population is an odd multiple of c. Consequently n_odd≥(6L+3)c. In particular the odd-population regime n_odd≤301 allows no such even lift.

## Global block counts and neutral subtrees

Use R,K,E(H),F exactly as in the [source theorem](../README.md). On 3431, E(H)=6 is impossible by the two-bank theorem at its center. E(H) is even, hence K≥7+8F and R+4F≤41. Every detached component needs at least three occupied vertices. At least one ordinary odd vertex in the source supplies nonzero charge, so R≥3F+1 and F≤5.

On 5063 let f of the F>0 components have E=6. The others have E≥8. Of the at least 5f outward neutral edges just proved, at most F−1 lead directly into another detached component: contract the disjoint components in the tree, and these particular links form a forest. The remaining child roots are distinct occupied ordinary vertices, outside both the detached components and the spine component. Counting also one ordinary source vertex gives
$$
53\ge R+\tfrac12\sum E(H)\ge 7F-f+1+\max(0,5f-F+1).
$$
The right-hand side is at least 7F+1−(F−1)/5, which exceeds 53 for F≥8.

For an occupied exterior-free subtree with net zero charge at each parity, the entering edge is discarded. Each charged vertex belongs to a detached component wholly inside the subtree because its gate currents sum to its charge. At 3431 such a component costs at least (2·3+8)c=14c. At 5063 an E=6 component costs 12c plus at least five outward occupied neighbors, all inside the subtree. Otherwise the same count gives at least 14c. Equality requires a single three-vertex path filling the subtree. Its two charged leaves require at least 5c each and its balanced center at least 2c. If both leaves had exactly 6c, both nonzero charges would be even in blocks, violating the single-gate bound of (4304/1001)c per charge block. Consequently at least one leaf has exactly 5c. Its charge is ±c by the single-signed-gate estimate. This leaf needs three extra physically active gates, and at most one can exit the entire subtree. This contradicts the assumption that the three vertices already fill it. Its total population is an even multiple of c by neutrality, hence at least 16c.

In the [minimum native two-owner case](../../terminal-contact/TWO_OWNER.md), the entire middle region is balanced **at every occupied lift** for both boards. The previous result proved this at 5063 and below 12c at 3431. At 12c for 3431 its only possible charged case was the three-lift path with center 2c and currents ±26. The two-bank theorem excludes this center even at an ordinary native lift. None of these arguments changes the hypotheses of the separate native two-height bounds or identifies the reflected path frame with the standard vertex-phase frame.

## Replay

Run the following in this directory with Python 3 and NumPy, with assertions enabled. Certificate verification uses integer arithmetic and requires no optimizer.

```sh
python transfers.py | diff - TRANSFERS.json
python leaf.py | diff - LEAF.json
python control143.py | diff - CONTROL.json
```

The last test reconstructs both complete 143 tilings, measures the CCW long-bank vectors directly after removing physical pairs, compares with the heading sums, checks the divisibility at every ordinary gate and verifies the mate formula on all sixty pairs of each tiling. The numerical exclusions at 37 and 43 use their own integral tables. The source with no detached component and larger charged regions remain possible under these necessary conditions.

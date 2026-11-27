# The first charged unmatched population fails in the physical board

Suppose an ordinary short lift away from the two-edge exterior path has nonzero charge. At 3431 a complete tiling requires at least **151** unmatched tiles. At 5063 the corresponding minimum is at least **173**. The previous floors were 149 and 171. These stronger floors concern the **entire physical population** of unmatched tiles. The additive accounting after reserving neutral banks still uses its own earlier constants. Both original questions remain open.

The [charged seam theorem](../../../2026-11-26/semiprimes/charge-variation/CHARGED_SEAM.md) determines the geometry if the previous floor is attained. In the standard vertex-phase frame there is one off-path terminal lift adjacent to the axial lift. Its entering edge has $c$ terminal and $a-b$ axial singles of standard sign $-1$. Every unmatched tile uses this or one of the two exterior path edges. Two first-cut words A and C survived. Removing the prescribed axial owners along that cut leaves a region containing only axial and terminal tiles. All its boundary edges have the axial marker. Remaining singles use only the charged edge. Actual pairs use either short lattice.

## A forced wall and the native translate

In the axial short chart let $\rho=\exp(i\pi/3)$ and $z=(a+b\rho)/c$. Write the terminal lattice as $t+z^s R$, with $s=\pm1$ and $0\le t<c$. Here $R=\mathbb Z[\rho]$. The native middle neighbor of the axial lift contains the axial-to-slant corner $X=b(2a+b)$, so it is $X+zR$. Its label in these standard coordinates is 30 at 3431 or 4 at 5063. The label zero of the reflected path coordinates refers to a different origin. The previous charged-contour census omitted positive-hand label zero and included the native positive-hand label. The [corrected census](../../../2026-11-26/semiprimes/charged-contour/README.md) tests zero, excludes the actual native neighbor, and reproduces the same profile counts. Two additional exact integer certificates cover the missing label for word C.

The repaired positive boundary of word A contains the following straight side with a strictly convex corner at each end, in axial coordinates.

| Board | Start | End | Side length | Positive-hand label | Negative-hand label |
|---|---|---|---:|---:|---:|
| 3431 | $(231,120)$ | $(120,231)$ | 111 | 30 | 34 |
| 5063 | $(455,240)$ | $(240,455)$ | 215 | 4 | 28 |

Every tile edge covering a positive length of this side lies wholly on the side. Extending it past an endpoint would leave the region locally at that strictly convex corner. Thus the side length is $ax+by+cz$ for nonnegative integer counts. Direct enumeration gives only $(x,y,z)=(0,0,3)$ or $(0,0,5)$ respectively. All these edges must be terminal singles: a long side at axial physical height has an adjacent short height, and every other possible adjacent lift is outside the residual. Their long endpoints belong to the root and terminal translates. In particular the side start fixes $t$. In the two hands the label of an axial point is $x-ay/b$ or $x-by/a$ modulo $c$. The positive label in the table is precisely the native neighbor and cannot be the distinct off-path edge. This leaves one negative translate per board.

## Exact test of the remaining regions

Cancel the oriented unit segments of the repaired cut and the axial exterior. The resulting chain is a single simple positive contour in each case. A pair contributes its short marker at each end of a line interval. A single contributes its short marker at a short edge and its neighbor's marker at the long edge. Consecutive intervals of a physical tiling have the same marker at their common endpoint. Half-integral probes in the scale-$c$ lattice miss all vertices. This argument uses the physical location of the outer boundary and admits T-junctions.

Enumerate pairs in the two known meshes and every single with long endpoints in both and sign $-1$. The [verifier](charged_equality.py) checks all six allowed oriented single templates in each hand against the independent charged-contour formulas. On a probe, use a vertex for each ordinate and marker. The test deletes a crossing object if its interval is on no path between the two axial boundary endpoints of a section component. A disconnection suffices for exclusion.

Repeat the probe list while the pool is shrinking. All deletions preserve any exact tiling. A disconnected component of a section proves impossibility immediately. Reaching a fixed point would leave that case open. No bound on the number of passes is needed because the pool is finite.

The corrected ordered-circuit and area census already excludes word C on 3431 and its positive hand on 5063. For its 43 remaining negative-hand translates at 5063 the new section test uses all sign-allowed singles, without narrowing their six heading counts to the surviving profile. [CHARGED_EQUALITY.json](CHARGED_EQUALITY.json) records the full list, including both remaining word A cases. Each failure index identifies a disconnected section in the repeated, deterministic probe list. Every trial fails. Removing actual pairs changes tile count by two, so the total number of unmatched owners is odd. Excluding equality gives the two new bounds.

## Where the signed imbalance can lie

Consequently, for total unmatched population at most 149 or 171 respectively, every off-path short lift has zero signed charge. The standard-frame odd charge $-c$ lies entirely at the native middle lift, the only odd lift on the exterior path. Each occupied exterior-free branch is neutral in both parities. Applying the [disjoint contact and area reserve](README.md) with its original exterior contribution 107 or 149 gives the following limits on all tiles away from the exterior path.

| Board and unmatched budget | Occupied off-path short lifts | Maximum number of distinct off-path tiles |
|---|---:|---:|
| 3431, $M\le149$ | one | 1850 |
| 3431, $M\le149$ | two | 888 |
| 5063, $M\le171$ | one | 344 |

More than the listed number of off-path lifts is impossible in these budgets. In particular at least 4719 tiles of the 5063 board would have one of the three native short lifts. To verify the table, the total neutral-edge payment is at most 42 or 22. Each edge costs at least 16. Its population is a multiple of $2c$ by signed neutrality and parity, and is at most $(mc)^2/(\pi\sqrt3 ab)$ by perimeter. At 16 owners it is exactly $2c$. For two edges on 3431 each costs at most 26, so a nested pair has at most 666 distinct far tiles. For disjoint edges maximize the sum of the two area bounds rounded down to multiples of 74 over even costs of sum at most 42. This gives 888. These statements concern the actual physical tiling, before any bank is removed from signed accounting.

## Reproduction

First run `python replay.py | diff - STATUS.json` in the [charged-contour directory](../../../2026-11-26/semiprimes/charged-contour). In this directory run `python charged_equality.py --workers 4 > local-charged.json` and compare with the recorded file. The section implementation indexes shapes by their obtuse corner and precomputes the maximum projected reach of their actual vertices. It checks every relevant candidate. It uses exact integer ordinates with a common denominator and checks divisibility at every interpolation. The complete 143 controls reconstruct all physical pairs and singles and test that this implementation preserves every one in each of the 198 and 181 sections.

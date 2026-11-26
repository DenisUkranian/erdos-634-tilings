# Signed branch populations and the two exterior banks

For any complete tiling of either target F2 board, let \(V=\sum_{v\ {\rm odd}}|G_v|/c\) on the positioned joint-cell tree. The sum uses actual short-tile populations with the reflected path-frame signs. Then
\[
 V\le39\quad(3431),\qquad V\le59\quad(5063).
\]
If the corresponding upper bound is attained, **at least one of the axial and slant markers is a leaf** in the minimal subtree spanning both markers and all charged odd lifts. Both original existence questions remain open.

## Cost of a physical branch

Use the notation and [cut equations](README.md) of the [disjoint branch reserve](OFF_HULL.md). Write H for the minimal subtree above, C and T for the exterior markers, and B for the middle vertex of their two-edge path. For an odd charged v choose its sign σ so that its normalized charge is ck, with k positive. A component outside H attached at v contains no charged odd vertex or exterior marker. Let w be its even root. With signs multiplied by σ, the signed banks of v→w and w→v are dj and cj, with d=a−b. For j nonzero put h=|j|. The whole component contains at least
\[
 ch+4c\quad(3431),\qquad ch+6c\quad(5063).
\]

First, at **every ordinary lift** each signed gate count q satisfies \(2|q|\le n\). Orient signs so q is positive and write P,M for the two sign populations. The unsigned positive gate count is bounded both by P and by αP+(1−α)M with α<1/2, by the [localized gate capacity](../joint-cell-tree/BRANCHING.md). If P≤M use the first bound, otherwise the second. Hence the root of the component contains at least 2ch tiles.

If another occupied even lift is present, the path to it passes through an occupied odd lift by [the exterior-free mesh-cycle theorem](../joint-cell-tree/TREE.md). Both additional lifts need at least 2c tiles. The population is therefore at least (2h+4)c. The branch block count has the parity of j since its signed total is σcj and c is odd. At h=1 this improves six blocks to seven. For h≥2 the displayed claim follows directly.

If w is the only occupied even lift, its own signed population has magnitude ch. Every child direction of w has zero signed gate current by the cut identities; it contains neither a charged odd lift nor an occupied even lift. Its gate toward v is its only nonzero signed gate. If other tiles occur they include at least 2c balanced odd tiles. The [single signed-gate bound](../axial-reserve/README.md) at w gives at least (3810/1002)ch or (4304/1001)ch at w before adding those tiles. If there are no other tiles use the stronger [physical terminal bound](../joint-cell-tree/TREE.md) (91/22)ch or (83/13)ch. In each alternative round the total up to a number of blocks congruent to h modulo two. This proves the claim for every h≥1. The proof retains the short tiles of all balanced branches.

## A degree and population inequality

At v let ℓ be its degree in H, and cx its minority population. Then its positive current at any gate in its own sign normalization is at most p=cx+floor(αck). Let
\[
 J=\max(0,\lceil(ck-\ell p)/d\rceil).
\]
The net outward current in units of d is at least J when J>0. Thus at least g=ceil(J/floor(p/d)) exterior-free gates carry nonzero current if J>0, and the denominator must be positive. Initially use g=0 for J=0. If ℓ=1 and (k+2x)c is below the single-signed-gate lower bound for charge ck, increase g to at least one. With all outward signed currents zero, the sole hull direction would carry ck, contradicting that lower bound.

The outward components at different charged odd lifts are disjoint. Each even owner on a hull gate directed into a charged odd lift is counted only there. Put F=2 or 3 for the two boards in order. The half-excess budget satisfies
\[
 \frac{N-(c+d)V}{2}\ \ge\ \sum_{v}\left(cx+Fc g+\max(0,cJ-dk)\right).
\]
Indeed for outward indices j_i with sum t, the counted even-bank owners and other tiles of the outward components cost at least c∑|j_i|+2Fcg+|dk−ct|. The last term counts the residual signed bank required on hull gates. The terms cx account for the actual odd short tiles beyond absolute charge. The established minimum minority and 5063 unit-leaf restrictions from the preceding reserve also apply.

For the charged odd vertices put S=∑(2−ℓ). The tree degree identity gives exactly
\[
 S=(\deg_H C-1)+(\deg_H T-1)
       +\sum_{u\notin\{C,T\},\ u\text{ outside the charged odd set}}(\deg_H u-2),
\]
where the last sum ranges over vertices of H other than C,T and the charged odd vertices (including every other even vertex regardless of its charge). Each summand is nonnegative. The [integer checker](exterior_reserve.py) first maximizes S independently of the arrangement of the two signs, subject to their absolute charge sums (V+1)/2 and (V−1)/2 sharing one budget. Starting with the previous bounds of 45 and 63 gives the following exact relaxation.

| N | V | Budget | Maximum S |
|---:|---:|---:|---:|
|3431|45, 43, 41, 39|298, 361, 424, 487|−2, −1, 0, 1|
|5063|63, 61, 59|484, 549, 614|−1, 0, 1|

## Charging the exterior banks when S is zero

Equality S=0 forces C and T to be leaves and every other vertex apart from charged odd lifts to have degree two. The side toward C and the side toward T at B each contain zero odd charge. Since V>1, a charged odd vertex lies off the path C,B,T. Its route to that path must attach at B. Consequently B is a charged odd lift of degree ℓ≥3.

In path signs, let e and f be the corrected even charge sums in blocks on the two exterior sides at B. The cuts specify the following actual signed owners.

| Direction at B | B owners | Owners on the opposite bank |
|---|---:|---:|
| C | 2c+de | A=d+ce |
| T | −c+df | D=cf |

The even sums are corrected by subtracting d only on the side containing C. The previous [even variation bounds](OFF_HULL.md) imply |e|,|f|≤c. With the sign σ of B, write q=σ(2c+de), r=σ(−c+df). Apply the sign budgets and individual capacity p to both q and r. In the previous expression for J replace ℓp by q+r+(ℓ−2)p. Other charged odd vertices keep their original charges and costs.

Pay for the **whole populations** of C and T at B. No tile there can pay a hull bank directed at another charged odd lift since both are leaves in H. Neither marker belongs to an outward component counted elsewhere. The earlier [axial sign bounds](../axial-reserve/README.md) give
\[
 n_C\ge L=\max(64,|A|+8)\text{ or }\max(75,|A|+5).
\]
Indeed the two signs at C have population at least 8 or 5 by the respective sign residues, and at least |A| tiles of one sign must supply that gate. The ordinary gate bound gives n_T≥2|D|. With Δ=dk−σ(A+D), the even owners and outward component populations paid at B now cost at least
\[
 E=L+2|D|+2Fcg+\max(|\Delta|,2cJ-\Delta).
\]
To check the last term directly, the unpaid hull banks have signed sum Δ−ct. The outward branches pay at least c∑|j_i| in addition to their reserves. For J=0 the triangle inequality suffices. For J>0 use t≥J as well. The contribution to the doubled excess is at least 2cx+E−dk. The other vertices must supply surplus at least ℓ−2.

The checker tries each sign and charge of B, its degree, minority population and both corrected exterior charges. After pruning cases whose other vertices or minority alone exceed the budget, the least required total half-excess is 430 at 3431 and 1150 at 5063, exceeding 424 and 549, respectively. The pruned cases already fail the budget. Thus the zero-surplus rows are impossible. Since V is odd, the stated bounds follow. At the first remaining value S≤1, so the degree identity forces at least one exterior marker to be a leaf.

Run `python3 exterior_reserve.py | diff - EXTERIOR_RESERVE.json` in this directory. The replay reconstructs both complete 143 controls directly from coordinates. The native bank pairs in path signs are (14,2) and (−7,0) in both. Neither example has a nonzero exterior-free branch attached to a charged odd lift. The quantitative branch bounds use the target-specific capacity and endpoint certificates.

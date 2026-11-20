# The (231,259,280) triangle cannot be tiled by (33,7,37)

**Theorem.** In the basis $1,\rho$ with $\rho=e^{i\pi/3}$, the triangle $F$ with vertices $0,231,280\rho$ has no tiling by congruent triangles of sides $33,7,37$. Its area would require 280 tiles. The proof allows reflections, arbitrary real translations and T-junctions. It concerns this particular target and tile.

## Reduction to three finite orientation intervals

Set $z=(33+7\rho)/37=e^{i\beta}$. Every tile direction relative to the horizontal has a unique expression $\rho^j z^h$ with $j$ modulo six. This follows by propagating across positive-length contacts and using the irrationality of $\beta/\pi$ as in the [straight-cut proof](../README.md). The short sides of one tile have a common height $h$ and its long side has height $h+1$ or $h-1$. Write $n_h$ for its unsigned population. The three counterclockwise edges of $F$ are $(231,0,0),(259,-1,2),(280,0,4)$ in length, height and phase notation.

We use two earlier project lemmas. The [height-divisibility proof](../../../../../i120-global-oct7/HEIGHT_LEVELS.md) includes precisely the F1 normalization used here. It gives $37\mid n_h$ for $h\ne0$ and $n_0\equiv280\equiv21\pmod{37}$. For clarity, the whole-edge identity for the tail above a height $k$ subtracts the exterior boundary above $k$. The resulting chain consists of full 37-edges in $37z^k\mathbb Z[\rho]+37z^{k+1}\mathbb Z[\rho]$, of index 37 relative to $z^k\mathbb Z[\rho]$. Outside the two exterior heights there is no exterior term on the far side. At the separating cut the sole exceptional side is one segment of length $259=7\cdot37$ at height $-1$, so it can be included as seven whole steps. Closed walks in this lattice have determinant area divisible by 37. The unit determinant area is $231$, coprime to 37.

The [line-count lemma](../../../LINE_COUNTS.md) excludes $n_h=37$ wherever every exterior contribution on each line of height $h$ is a multiple of 37. Every $h\ne0$ satisfies that condition, including $-1$ because its only exterior side has length 259. Thus each occupied height other than zero uses at least 74 tiles.

For the two signed boundary sums in the straight-cut proof, let $g_h$ count positive tiles minus negative tiles at height $h$, taking the sign for which the short-edge contribution is $33-7=26$. The ordinary total per tile is $-11$ times this sign, and the height-alternating total is $63(-1)^h$ times the sign. This follows from the representative edges $(33,0,0),(37,-1,3),(7,0,5)$ and from reflection and rotation. The exterior sums are $231+259+280=770$ and $231-259+280=252$. Consequently
$$
 \sum_h g_h=-70,\qquad \sum_h(-1)^h g_h=4,
 \qquad \sum_{h\text{ odd}}g_h=-37.
$$
At height 0, reducing the ordinary boundary sum modulo the full long-edge length gives $26g_0\equiv231+280\equiv30\pmod{37}$, hence $g_0\equiv4\pmod{37}$. A population $n_0=21$ would require an odd $g_0$ in $[-21,21]$. That interval has no such representative. Therefore $n_0\ge58$. Four occupied heights would already require $58+3\cdot74=280$ tiles. Equality makes every population even and hence every $g_h$ even, contradicting the odd sum $-37$. There are at most three occupied heights and zero is one of them.

There can be no vacant height between zero and an occupied height. If the vacant height is $k>0$, apply the whole-edge cut identity to the tail strictly above $k$. If $k<0$, use the tail at heights at most $k-1$. In each case the far tail has zero exterior contribution on its own side of the cut, even when $k=-1$. The vacant height contributes no tiles, leaving only whole 37-edges of direction height $k$ in the boundary chain. This is the [whole-edge gap argument](../../../FULL_BOARD.md). Closed boundary walks on a rotated translate of $37\mathbb Z[\rho]$ give total determinant area divisible by $37^2$. Since $\gcd(231,37^2)=1$, a nonempty such tail would have at least 1369 tiles. Thus all possibilities are contained in $[-2,0]$, $[-1,1]$, or $[0,2]$.

## The endpoint contradiction

Write $\eta=7-3\rho$, $\bar\eta=4+3\rho$. Then $\eta\bar\eta=37$ and $z=\rho\eta/\bar\eta$. In a band $[L,U]$, multiply all coordinates by $g=\eta^{-L}\bar\eta^U$. At short height $h$, each of the twelve oriented templates has integer axial displacement vectors. Up to a power of $\rho$, its unit short directions are multiples of $\eta^{h-L}\bar\eta^{U-h}$. The target corners are integral in this coordinate system.

On each physical line, the sum of oriented tile boundaries equals the oriented exterior boundary. Take endpoints on that line. At an endpoint with zero exterior demand, a placement contributing one sign is impossible once every placement contributing the opposite sign has been ruled out. At an exterior corner that requires a sign, eliminating all placements of that sign is a contradiction. For an oriented template and a specified endpoint, its translation is forced. In particular, if that endpoint is integral, every placement that could meet the obligation is among the integer translations tested. This justifies the contradiction for arbitrary real translations without postulating a lattice for the full tiling.

The independent verifier checks geometric containment of every possible opposing placement against the target half-planes. It starts from an empty set of rejected placements, verifies every implication in chronological order, and verifies the absent required sign at the stated exterior corner. The table records the three completed replays. A positive sign means the start of a counterclockwise exterior edge.

| Short heights | Initially contained placements | Verified packed implications | Individual deductions | Required corner and sign |
|---|---:|---:|---:|---|
| $[-2,0]$ | 1,114,288,638 | 23,563,740 | 476,796,533 | vertex 0, axis $(40,-33)$, start |
| $[-1,1]$ | 1,116,707,764 | 23,952,238 | 474,961,183 | vertex 1, axis $(1,0)$, end |
| $[0,2]$ | 1,106,923,257 | 22,428,099 | 470,456,497 | vertex 1, axis $(7,33)$, end |

All allowed bands lead to a contradiction. The geometric conclusion is independent of any choice of a cut of $F$.

## Replay

The replay uses a little-endian Linux system, a C++17 compiler, standard shell tools, and about 2 GB of scratch disk.

```sh
sh replay.sh
```

The script copies the [existing endpoint producer and verifier](../../../../../2026-11-19/nov19/equilateral231/cert/README.md) into a fresh build directory, checks their input hashes, and applies [the target changes](target.patch). Their original versions in repository commit `26de6448a4c82749a94d248d38f993a9da1e97e9` also work. The geometric change in the target is the replacement of the third vertex $231\rho$ by $280\rho$. The verifier reads the complete forward proof, without an extraction stage. The three traces are deterministic. Their [SHA-256 digests](SHA256SUMS) and [verifier outputs](replay.txt) are recorded. Optional arguments to the script are the directory containing the two original C++ sources and a build directory. The script leaves generated traces there for inspection.

As a negative control for each trace, exchanging the two sign masks in its first packed record made the independent verifier reject the very first implication. A complete rerun of the packaged script regenerated all three recorded digests.

# Populations across the two native cuts and arbitrary exterior-free branches

Both original counts remain **OPEN**. The base for this calculation is main at `e2924b5644ca404dbc42ebd97116bc90d8ead0fd`. Work on the positioned tree of a complete tiling with the reflected path-frame signs. For each subtree let $e,o$ be its total even and odd charges in blocks of $c$, after subtracting $d=a-b$ at the axial marker $C$. The full board has corrected totals $(0,1)$. Let $B$ be the middle vertex and $T$ the slant marker. Removing $B$ gives a $C$-sector, a $T$-sector and the union of all other sectors.

| Necessary condition | 3431 | 5063 |
|---|---:|---:|
| Maximum $\lvert e-o\rvert$ in either native sector | 14 | 18 |
| Maximum $\lvert e-o\rvert$ in the union of all other sectors at $B$ | 17 | 23 |
| Maximum $\lvert e-o\rvert$ on any individual exterior-free cut | 17 | 23 |
| Size of the slant side of a native cut if the middle bank cancels as a physical chain | 1369 | 1849 |

In particular, **if the middle lift contains a tile, at least one of its two native gates contains an unmatched tile**, even if both gates have signed current zero. The conclusions permit arbitrary hands, heights, translates, and contact subdivisions. The numerical bounds use the [total even and odd variations](EVEN_VARIATION.md) and the physical [lift and cut theorem](../joint-cell-tree/TREE.md).

## Cancellation on a native bank fixes the population on one side

Cut either native edge. Select the side containing $T$, namely the $T$-sector for the edge $BT$ and the complement of the $C$-sector for $BC$. Its exterior chain consists of the single complete slant. The cut-chain identity expresses the rest of its boundary as the difference of the two banks of whole long sides. If the $B$-owned bank is the zero oriented chain, the remaining edges all have the middle physical height, since their long marker is $B$. They have length $c$ and six equiangular headings.

Consider the directed multigraph formed by these oriented whole edges and the slant chord, reversing signs as required by the cut identity. Its endpoint boundary vanishes, including at T-junctions, by taking the boundary of the boundary as a chain. It decomposes into closed edge walks. Deleting the single slant chord from its walk leaves a mesh walk connecting the two slant endpoints. Every other walk lies in some translate of the same mesh of step $c$. On the chord walk the vertices, including the two chord endpoints, also lie in one translate. Translate the start of each walk to zero separately. In axial coordinates for that rotation, the determinant sum around each walk is divisible by $c^2$. This argument needs neither simple walks nor a common translate for different components. Adding the determinant sums gives $abm$ up to the common choice of orientation, where $m$ is the population on the selected side. This follows by summing the signed areas of its tiles, including those with subdivided contacts. Since $\gcd(ab,c)=1$, this gives $c^2\mid m$.

Independently compute the parity of $m$ from the two characters. For $i=C,T$ the signed current from $B$ into its gate is
$$
 q_C=d e_C-c o_C+2c,\qquad q_T=d e_T-c o_T-c .
$$
A cancelling bank has zero signed current: on each oriented line the two opposite unit headings of a fixed gate have opposite signs, and all owners contribute intervals of the same length. Since $|e_i|\le W/2<c$ and $\gcd(c,d)=1$, cancellation on $BC$ gives $(e_C,o_C)=(0,2)$, and cancellation on $BT$ gives $(e_T,o_T)=(0,-1)$. In either case the selected slant side has actual total signed population $-c$. It contains an odd number of tiles. Since $N<3c^2$, the unique possible value is **$m=c^2$**.

If both middle banks cancel, the $T$-sector therefore has $c^2$ tiles and the $C$-sector has $N-c^2$. These sectors are disjoint. No tile remains at $B$ or in any other sector there. A bank consisting entirely of half-turn pairs has zero oriented chain because the two owners traverse their common long side oppositely. This proves the unmatched-owner assertion. If both signed currents vanish and $B$ is occupied, a noncancelling bank there has unmatched owners of both signs. This distinction between scalar and physical cancellation is essential. The proof uses neither absence of the entire middle height nor a two-height restriction.

## A lower bound at every depth of a branch

For an exterior-free branch rooted in parity $p$, let $x,y$ denote its net charges of parity $p,1-p$, respectively, in blocks. Use the same coordinates for a disjoint forest with all roots of parity $p$. Partial sums for every subcollection belong to the rectangular ranges obtained from the even variation $W=38,58$ and odd variation $V=39,59$. Indeed the positive and negative even sums have magnitude $W/2$ or less, and the odd sums are bounded by $(V+1)/2,(V-1)/2$.

Deleting the root of the branch leaves a forest with charges $(y,z)$. The root has signed population $G=c(x-z)$, its own bank toward the parent carries $u=cx-dy$, and all its other gates carry signed total $v=dy-cz$. The opposite bank toward this branch carries $dx-cy$. These formulas follow by substituting the two parity sums in the cut characters and summing the child cuts. They also follow by subtracting the entering bank from the signed short population, since each short tile has exactly one long marker. Thus the two populations used to pay $|u|+|v|$ are disjoint.

Use tile counts $P,M$ for the two signs at a root. A distinguished ordinary bank of signed current $s$ requires
$$
 D|s|\le A P_s+$D-A$M_s ,
$$
where $P_s,M_s$ are the populations aligned with and opposed to $s$. The numerator and denominator $(A,D)$ are $(43,222),(8,43)$. Also impose the [ordinary sign divisibilities and one-block exclusion](../joint-cell-tree/TREE.md), and the [5063 monochromatic two-block exclusion](README.md). For a nonzero vector the branch root is occupied by the supported-cycle theorem, so it costs at least two blocks.

Let $L_p(x,y)$ bound the tile count in one such branch from below in blocks, and $F_p(x,y)$ do the same for a forest. For a nonzero vector the following exhaustive alternatives give a certified recursion.

1. **No child has nonzero net vector.** Then $y=z=0$. A genuine terminal costs at least $t|x|$ blocks, where $t=91/22,83/13$. With occupied descendants the root has just one nonzero signed gate and costs at least $s|x|$ blocks, where $s=3810/1002,4304/1001$. At least two additional blocks occur in the descendants. Round the root separately to an integer congruent to $x$ modulo two. The [single-gate estimate](../axial-reserve/README.md) allows physically occupied signed-zero gates.
2. **Exactly one child has nonzero vector.** Its vector is $(y,z)$. Use both one-bank capacities, separately at $u,v$, since the other children have zero signed currents. Add $L_{1-p}(y,z)$. If just one of $u,v$ is nonzero, also use the single-signed-gate bound at this root.
3. **At least two children have nonzero vectors.** Use the one-bank bound at $u$ and the disjoint payment $|u|+|v|$ at the root. From the nonzero child vectors one can pick a vector $a$ such that the rest sum to a nonzero vector $b$. Otherwise every vector would equal their total, forcing this total and all the vectors to be zero. This proof uses ordinary integer vectors; it also works if the total is zero. For the children use the minimum of $L_{1-p}(a)+F_{1-p}(b)$ over $a+b=(y,z)$ with both nonzero.

For a forest of nonzero total either one nonzero tree accounts for that total or the same two-part split applies. Components of zero vector keep all their physical tiles. A zero additive payment for them gives a valid lower bound. In particular $F_p(0,0)=0$ allows the empty forest.

[The recursion](rooted.py) starts with two blocks on each nonzero vector and caps at the first block count exceeding $N$. The [separate checker](forest_review.py) takes the output tables as proposed lower bounds. It enumerates the two physical sign populations, each possible child total, and all two-part splits by complementary indexing. It checks that every table entry is at most every applicable payment. Structural induction on the finite physical tree, decomposing a forest by its number of nonzero trees, then proves the tables sound without any assumption about fixed-point uniqueness or an upper bound on tree depth. The cap represents a bound above the board budget. Both parities give the following examples for $F_p$, in whole blocks.

| $(x,y)$ | 3431 | 5063 |
|---|---:|---:|
| $(1,0)$ | 5 | 7 |
| $(0,1)$ | 7 | 9 |
| $(1,1)$ | 8 | 10 |
| $(1,-1)$ | 10 | 12 |
| $(2,-2)$ | 18 | 20 |

## Use at the exterior and on arbitrary cuts

On a remote cut add the single-tree bound on the inside to the two [outside parity-sector bounds](EVEN_VARIATION.md). The opposite bank contributes to the outside parity opposite the root. For an empty side allow zero. Enumeration yields the third row of the first table.

At $i=C,T$ write $\delta=1$ for $C$ and zero for $T$. For a candidate sector with net $(e,o)$, the root has inward bank $ce-do+d\delta$. After deleting it the rest is an odd-rooted exterior-free forest of state $(o,z)$. Pay the root with signed total $c(e-z)+d\delta$, outward total $do-cz$, and distinguished inward gate. At $C$ use its sign residues, size floor and axial source allowance from the [even variation theorem](EVEN_VARIATION.md). Minimize this payment plus $cF_1(o,z)$ over $z$.

Let $(e_R,o_R)$ refer to all other sectors at $B$. They cost at least $cF_0(e_R,o_R)$. Here $e_R=-e_C-e_T$, the charge at $B$ is $ck=c(1-o_C-o_T-o_R)$, and the signed $B$-owners on the remaining gates total $h=de_R-co_R$. Add the **whole** $B$ population, bounded below by $|q_C|+|q_T|+|h|$, by the separate capacities on $q_C,q_T$, and by its sign and block restrictions. Allow an empty $B$. The four populations are disjoint. Require the total to be at most $N$ and the sector absolute charges to respect $W,V$, including $|k|$ in the odd variation. The resulting necessary tests retain 567005 and 1704465 integer quintuples. Maximizing across them gives the first two rows. This census deliberately allows both native banks to have zero signed current; the additional physical-chain test proved above is a separate conclusion.

Run `python3 forest_replay.py | diff - ROOTED.json` here with Python and NumPy. The [recorded replay](ROOTED.json) includes the two complete 143 examples. Their sector partitions are $(38,0,0;105)$ and $(52,0,0;91)$ in $C,T,R;B$ order. Directly reconstructed banks at $B$ have signed values $(14,-7,0)$ in both. Comparing endpoints and actual half-turn mates gives 14 and 7 unmatched middle owners on the two native gates in each tiling. The checker reconstructs both oriented cut chains and compares their determinant sums with the exact sector populations. Neither has an occupied exterior-free branch or a cancelling middle bank on a native cut. The coordinate check tests the conservation and disjoint payments there; the nontrivial cancellation implication is geometric. The target-specific capacity constants are applied only at their own moduli. Eliminating the remaining sectors and verifying the original classification reduction would still be required for a negative answer.

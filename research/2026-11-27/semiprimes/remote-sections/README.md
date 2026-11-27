# A physical contact bound for branches with occupied descendants

Assume a complete F2 tiling with either target tile. In the [lifted tree](../../../2026-11-26/semiprimes/joint-cell-tree/TREE.md), take any occupied branch directed away from the exterior path. Write $n$ for the number of tiles on its far side and $m$ for the number of unmatched owners on the two banks of its entering edge. Each owner is a whole tile remaining after actual long-side half-turn pairs cancel. A nonterminal branch has an occupied strict descendant.

| Hypothesis on the branch | 3431 | 5063 |
|---|---:|---:|
| Nonterminal | $m\ge18$ on the entering edge itself | $m\ge18$ on the entering edge itself |
| Nonterminal with a two-owner bank | **$m\ge32$** | **$m\ge38$** |
| Nonterminal with a two-owner bank and $n=4c$ | **$m\ge36$** | **$m\ge38$** |

The [three-lift exclusion](THREE_LIFTS.md) gives the 32-owner floor at 3431. The [charged equality theorem](CHARGED_EQUALITY.md) increases the minimum total unmatched population with an off-path charge to 151 and 173, respectively.

In particular, **on both boards every exterior-free cut with exactly sixteen unmatched owners encloses exactly $2c$ tiles in a single terminal lift**. The previous 3431 estimate allowed the entering edge to pay sixteen and assigned two owners from a child edge to its parent. The pointwise statement allows disjoint cost accounting even when the child edge is priced separately. These claims allow arbitrary heights, translations, reflections and split physical contacts. Both original triangle counts are open.

## A global charge and area reserve

For each neutral occupied exterior-free branch $e$, let $b_e$ be 16 for a terminal branch and otherwise the strongest applicable table entry. Neutral means that *each* of the two far signed parity totals is zero. Let $V$ be the sum of absolute odd short charges measured in units of $c$, $d=a-b$, and $M$ the total number of unmatched tiles. Then

$$
 N\ \ge\ M\ \ge\ \max(A,(c+d)V)+
 \sum_{e\ {\rm neutral}}\max\!\left(b_e, 2\left\lceil\frac{\sqrt{\pi\sqrt3\,ab\,n_e}}{2c}\right\rceil\right).
$$

Here $A=107,149$ in board order, or $149,171$ when any off-path short lift carries nonzero signed charge. Every branch in this sum has an even number of owners. Its boundary has length at most $cm_e$, while its area is $n_e ab\sqrt3/4$. Apply plane isoperimetry to the actual region, including all components and holes. Owners on distinct edges of the lifted tree are distinct tiles. Both removed neutral banks have zero signed current at their own lift. The [exterior reserve proof](../../../2026-11-26/semiprimes/terminal-contact/REMOTE_BOUNDARY.md) therefore charges the displayed maximum to the other owners. This accounts for nested branches at both levels without physically deleting a balanced branch. The bound does not use a native two-height assumption.

## Reduction to the two physical short lattices

The [short-contact census](../../../2026-11-26/semiprimes/terminal-contact/REMOTE_BOUNDARY.md) leaves only a terminal $2c$ at sixteen owners on 5063. On 3431 the additional possibility is $4c=148$ tiles in two adjacent short lifts. Fewer than sixteen owners were excluded there, and seventeen are impossible on either board by the [alternating exterior-free cut character](../../../2026-11-26/semiprimes/boundary-word/README.md). The 148-tile case has 24 normalized positive outer contours.

For a two-owner bank with $m-2<a$, the [two-path census](../../../2026-11-26/semiprimes/terminal-contact/TWO_OWNER.md) lists the possible pairs $(n,m)$. At $n=4c$ the only lengths are 24, 30, 34 for 3431 and 30 for 5063. For 5063 all other cases under this length hypothesis have $n=2c$ and are terminal. This census imposes signed neutrality on these two-owner branches. Evenness rounds the next possible lengths up to 36 and 38.

If an exterior-free $4c$ branch is nonterminal it has exactly two adjacent occupied lifts with $2c$ tiles each. Every ordinary occupied lift costs at least $2c$, and every exterior-free path to an occupied lift has an occupied root. This argument does not constrain the rest of the tiling.

Work in the far root's short chart. Write $R=\mathbb Z[\rho]$, $\rho=e^{i\pi/3}$, $z=(a+b\rho)/c$. Normalize the outer circuit to run CCW with a far-owner long step $c\bar z\rho^j$ (low) or a reversed near-owner step $c\rho^j$ (high). For the two-path census in its original units the exceptional step is $z$ and the pure steps are units. With the pure bank far, rotating by $\bar z$ gives the required chart. With the pure bank near, conjugate and reverse traversal. These two assignments are both enumerated. This chart is local to the physical cut.

Remove all far owners on this outer contour. Replace each low step by the two successive short steps of lengths $a,b$ with headings $j,j-1$. A high step stays. The near-owner apex for a high step is $a\bar z\rho^j$ from its start and the low-owner apex is $a\rho^j$, by taking their actual short sides. One 3431 word has overlapping prescribed owners. For every other word the reduced oriented unit chain is one simple CCW polygon of doubled axial area $ab(4c-\#\text{low})$. The checker verifies a single successor and predecessor on each unit vertex. Unit edges of this triangular lattice cannot cross away from endpoints. Winding number therefore determines the entire residual region. Its child still contains **all $2c$ tiles**, since all removed owners lie in the far root.

## Testing whether the child can occupy its required area

Use coordinates scaled by $c$. The root has lattice $cR$. A neighboring lattice has form $(ct,0)+uR$, where $u=a+b\rho$ or its conjugate and $0\le t<c$. The intersection with the root in unscaled coordinates has index $c$: reducing the conjugate multiplier modulo the prime $c$ gives a nonzero rank-one matrix of determinant zero. The intersection in either hand has equation $x+wy=0\pmod c$. Horizontal shifts represent every coset. This includes a possible back-projection to an already used physical cell.

Each remaining triangle either has an actual half-turn mate or uses the edge between these two lifts. After the prescribed outer owners are removed, every remaining gate other than the child edge has either already had its unmatched bank removed or has an empty exterior-free far side with zero long-bank chain. On each physical line a zero finite sum of signed intervals of the same length has zero signed multiplicity at each start, by inspecting starts in order. Opposite copies at a fixed gate are actual mates. Thus there are four allowed kinds of objects: pairs in either mesh, and singles in either mesh pointing to the other. For obtuse corner $q$, heading $j$, hand $h$, and mesh multiplier $v$, the other corners are $p=q-av\rho^j$ and $s=q+bv\rho^{j+h}$. The fourth corner of a pair is $p+s-q$. A single's long endpoints must lie in both meshes. The checker lists all mesh points in the polygon's bounding box in its own mesh coordinates. It requires all object corners to be inside the closed polygon. This permits extra candidates across concavities or overlapping each other.

On a line $2x'=t'$, with $t'$ odd and $x'$ the first axial coordinate after a unit rotation, all vertices are avoided. On each connected section of the residual, the true objects must give a path of contiguous intervals from the lower endpoint to the upper endpoint. Remove any crossing object whose interval lies on no such path. Objects missed by the line survive. Induction preserves all true objects of every tiling, even at T-junctions.

There are two exact reasons for rejection. A section can have disconnected endpoints. Alternatively, give **each surviving child pair capacity two and each surviving child single capacity one**. If their sum falls below $2c$, every possible selection has too few child tiles. This upper bound deliberately counts incompatible candidates together. It can reject a nonterminal branch even when the polygon passes ordinary section connectivity on every probe.

| Outer family | Words | Prescribed overlap | Lattice choices rejected by disconnected section | Rejected by child capacity |
|---|---:|---:|---:|---:|
| 3431, sixteen owners and 148 tiles | 24 | 0 | 1776 | 0 |
| 3431, two-owner bank and 148 tiles | 6 | 1 | 296 | 74 |
| 5063, two-owner bank and 172 tiles | 2 | 0 | 0 | 172 |

The disconnection test also applies to a sole root: root pairs are present in every tested pool. In particular among the short two-owner words at 3431 enclosing 148 tiles, only the length-30 word with two far owners can remain, and it requires a terminal root. The capacity argument uses a genuinely occupied child.

## Replay and checks

Run from this directory with Python 3, NumPy, assertions enabled, and a C++17 compiler.

```sh
python replay.py > local.json
diff -u RESULT.json local.json
```

[RESULT.json](RESULT.json) records every contour, repaired polygon and count. The replay regenerates the outer words from the exhaustive joins. The [line checker](slices.cpp) uses the common denominator $2\operatorname{lcm}(a,b,a+b)$ for crossings: after rotation every primitive edge is a root unit or a child unit, whose nonzero first coordinate divides this denominator after doubling. Each interpolation checks exact divisibility. Forward reachability uses increasing interval starts; backward reachability uses decreasing starts. The finite probe schedule suffices for the listed eliminations.

On both complete 143-coordinate tilings the checker reconstructs all 60 actual pairs and 23 singles. In all 198 and 181 sampled sections respectively it retains every one of these objects. Hence any marked subpopulation retains its exact tile capacity. Independently, the [rational section control](../../../2026-11-26/semiprimes/terminal-contact/attached/section_control.py) concatenates actual intervals directly and tests both endpoint graphs. The target-specific outer branch hypotheses are absent on these controls. Larger branches, native contacts and the global signed source still permit profiles under these necessary conditions.

The independent [fraction-based audit](review.py) rebuilds the catalogs in lattice array coordinates, interpolates reduced rational endpoints, and infers child membership from each surviving short edge. Run `python review.py` for one translate of each contour or `python review.py --all` for the complete second implementation.

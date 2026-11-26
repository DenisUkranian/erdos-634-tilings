# The slant word and its area

In the notation of the main theorem each subtree cut boundary is a sum of complete unmatched long edges and its assigned exterior edges. Use the complement if it contains the shorter exterior list. The two axial sides always belong together. Thus at most one exterior segment, the slant, is needed. Write $n$ for the population on this chosen side. The effective signs of the crossing edges reverse if one takes the complement.

The directed multigraph of these **whole** edges has zero endpoint divergence. This follows by taking the boundary of the chain identity. It is valid before splitting edges at T-junctions, since inserting subdivision points leaves endpoint divergence unchanged. Each connected component is Eulerian. Translate the closed tours to a common origin and concatenate. Their total shoelace sum is unchanged, as translating a closed walk adds the determinant of the translation with zero displacement. Rotate the cyclic word to put its exterior letter last if present. The sum of axial determinants is $abn$; the word is allowed to cross itself. Its component translations are used only for bookkeeping.

Thus each cut requires a word with prescribed two directional alphabets, bank characters, displacement and signed area. Any lower bound on the length of such a word can replace the crossing lower bound for that cut. Distinct edges in one tree count disjoint unmatched tiles. The ordered walk condition is necessary even when long sides partially cancel on the actual boundary.

## A balanced slant component

Take the increasing tree's cut from height one to two. Suppose that the two parity charges in the slant component both vanish. Then $p_2=0$ and $q_2=c$. Put $m=c+2r$. After rotation by $z^{-1}\rho^{-4}$, let $D=a+b\rho$. The crossing word has displacement $cD$, followed by the exterior letter $-cD$. Low and high long-side vectors are respectively $c\rho^j,D\rho^j$. Their signed counts over even versus odd $j$ are 0 and $c$. Rotation by an even unit preserves these signs.

**Paired inventory lemma.** For $r^2<c$ the crossing word consists, as an inventory, of $c$ copies of $D$ and $r$ opposite vector pairs on the two alphabets. The pairing is algebraic; these are still unmatched physical tiles.

To see this write its displacement $cx+Dy=cD$ with $x,y\in R=\mathbb Z[\rho]$. Then $\bar D x/c\in R$. In $R/cR$ the nonzero element $\bar D$ annihilates $x$, so $x$ is not a unit there. A unit norm modulo $c$ would give the inverse by conjugation. Hence $c\mid\operatorname{Norm}(x)$. The low bank has $u$ steps of zero character, with $u\le2r$. Pair its positive and negative directions arbitrarily. Each pair in normalized units is the difference of two of $1,\rho^2,\rho^4$. Each difference is zero or has length $\sqrt3$ and is divisible by $1-\rho^2$ of norm 3. Consequently $3\mid\operatorname{Norm}(x)$ and $\operatorname{Norm}(x)\le3r^2<3c$. Here $c$ is prime and distinct from 3, so $x=0$. Each bank now has a prescribed displacement and character. The three signed multiplicities are unique by the formula in the main theorem. They are $(0,0,0)$ in the low bank and $(c,0,0)$ in the high bank, proving the lemma.

*Area calculation.* The slant population is even and divisible by $c$, so write $n=2c\ell$. For an inventory of $r$ pair generators $v_i$ and $c$ forward steps $D$, its doubled axial area satisfies
$$
abn\ \le\ 2c\sum_i|\det(D,v_i)|+
                    2\sum_{i<j}|\det(v_i,v_j)|.
$$
Delete the two occurrences of each opposite pair successively. Its area contribution is twice the determinant with the intervening displacement. That displacement has at most $c$ copies of $D$ and at most one net copy of either sign of each other remaining generator. The exterior letter is last and has zero shoelace contribution. This proof covers unordered, disconnected and intersecting tours.

The inventory calculation keeps all six choices of pair axis with repetition. For each inventory, an integer recurrence builds a path to a prescribed multiset of used steps. The endpoint at each multiset is fixed. Appending $v$ adds $\det(\mathrm{endpoint},v)/c$ to the scaled area. The recurrence stores its maximum and a bit set of attainable deficits from that maximum. A prefix deficit is preserved if the better prefix receives the same suffix. Therefore deficits greater than the inventory upper bound minus the smallest still queried final area may be discarded. Previously attained values persist on adding an adjacent opposite pair. All larger values are excluded by exhausting the inventories whose area bound reaches them.

| Extra pairs $r$ | Maximum $\ell$ for 3431 | Maximum $\ell$ for 5063 |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 5 | 3 |
| 2 | 12 | 8 |
| 3 | 18 | 11 |
| 4 | 25 | 17 |
| 5 | 31 | 22 |
| 6 | 38 | 26 |

Every integer from zero to the displayed maximum is attained **as a formal word** in that row. A larger value is impossible for a true boundary with that budget. No converse for tile placements follows.

An independent recurrence deletes the $c$ identical forward steps and orders the remaining $2r$ vectors. If a forward step is inserted after neutral prefix $v$, it adds $2\det(v,D)$ to the neutral shoelace sum. Any distribution of the forward steps among the gaps is allowed. The second checker uses a repeated finite sum of gap heights. It reproduces every entry through three pairs and checks each rejection below the geometric upper bound at all remaining pair budgets. These calculations are integer-only. Neither presupposes a connected physical subtree.

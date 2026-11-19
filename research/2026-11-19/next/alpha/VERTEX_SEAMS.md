# Straight seams in a Group-1 alpha-isosceles tiling

Let $1\le u<v$ be coprime. Put $a=uv, b=v^2-u^2, c=v^2, Q=b+c, P=b+2c$. Use $\alpha,\beta,\gamma$ for the angles opposite $a,b,c$. Then $3\alpha+2\beta=\pi$. Let $A_g$ have base angles $\alpha$, equal sides $gbc$, and base $gbQ$. Write $\Theta_t$ for the triangle with apex $\alpha$, equal sides $tbv$, and base $tbu$. The natural-number scales here refer to these specific shapes.

**Proposition.** A tiling of $A_g$ in which a complete straight segment of tile edges joins a vertex to the opposite side exists if and only if at least one of the following holds.

1. $\Theta_{gv}$ admits a tiling by the unit tile.
2. $Q\mid g$, and $A_{gc/Q}$ admits a tiling by the unit tile.

The edges in the straight segment can come from different tiles and can have T-junctions. The endpoint on the opposite side must lie in its relative interior. No tile interior meets the segment: an edge of one tile cannot enter the interior of another tile with disjoint interior. An open tile interior meeting the line segment at an intermediate mesh vertex would also meet a subsegment. Thus each tile lies in one of the two closed subtriangles, and both are tiled.

**Proof.** The rational noninteger $2\cos\gamma=-u/v$ implies $\gamma/\pi$ is irrational, since the sum of a root of unity and its inverse is an algebraic integer. Thus $\alpha/\pi$ is irrational. At an external corner every contribution is a full tile angle. Expressing the angles as $\beta=(\pi-3\alpha)/2$, $\gamma=(\pi+\alpha)/2$ gives the unique possible inventory $\alpha$ at each base corner and $\alpha+2\beta$ at the apex. In particular, only the apex can start a seam. Up to interchanging the resulting triangles, its angular split has one of the forms $\beta\mid\alpha+\beta$ and $\alpha\mid2\beta$.

In the first case the subtriangle adjacent to the $\beta$ sector has angles $\alpha,\beta,\gamma$. Its side joining the $\alpha$ and $\beta$ vertices is one entire outer leg and has length $gbc$. Its scale relative to the original tile is $gb$ and it admits the ordinary triangular grid. The residual triangle has two base angles $\alpha+\beta$, one leg of length $gbc$, and hence is $\Theta_{gv}$. Conversely a tiling of that triangle gives the seam by the known hub construction.

In the second case, the subtriangle adjacent to the $\alpha$ sector has two base angles $\alpha$. Its base, this time, is one outer leg of length $gbc$. The necessary count and length condition for this same type gives $s b Q=g b c$ with $s$ a positive integer. Hence $s=gc/Q$ and $Q\mid g$ since $\gcd(c,Q)=1$. The remaining triangle has angles $\alpha,2\alpha,2\beta$, with side $gbc$ opposite $2\alpha$. This side has length $cQ$ in the canonical Paliy triangle, giving scale $t=gb/Q$. When $Q\mid g$, it is integral and Paliy's construction tiles that complementary triangle. Both implications follow. The area identity for this second split is $bQ(gc/Q)^2+QP(gb/Q)^2=bQ g^2$, since $c^2+bP=Q^2$.

**Consequences.** Every $g<Q$ admits a vertex-seam tiling exactly when $\Theta_{gv}$ admits a tiling. For $u=1,g=1$, Bonfioli's bound $tu\ge2v$ for $\Theta_t$ excludes such a seam for every $v\ge2$. For $u=v-1,g=1$, his stronger bound $t\ge v+2$ excludes it as well. In particular the $N=136$ and $N=517$ candidates have no vertex-seam tiling. Bonfioli's 18 November paper flags an inherited gap in one internal audit of his general $u=1$ necessity proof. The $N=136$ seam consequence also has the independent small-target calculation below. A [complete geometric exclusion](AUDIT136.md) and an independent [finite weight certificate](ENDPOINT_LP136.md) cover every tiling of this concrete target.

**The 280-tile target.** In the triangle with sides $90,90,140$, the exclusion of $\Theta_6(2,3)$ rules out every complete straight seam from any vertex. For a direct check, a $\beta$ sector at the apex cuts off a copy of the tile scaled by $90/9=10$. It occupies 50 units of the base, its cut side has length 60, and the remaining triangle has sides $90,90,60$. An $\alpha$ sector instead cuts off a triangle similar to the outer triangle whose base has length 90. Its area in tile units would be $280(90/140)^2=810/7$, an impossibility. Each of the two interior edge rays at the apex must therefore end at an interior vertex of any hypothetical tiling. Existence of a tiling with both rays ending in the interior remains open. See the [unrestricted theta-six exclusion](../theta6/PROOF.md).

Such a tiling would also lack the reflection symmetry of its outer triangle. Reflection fixes the apex, at which exactly one incident tile has angle $\alpha$. If the tiling were invariant, this particular tile would have to be invariant under reflection. Its three distinct side lengths preclude that symmetry. The same argument applies to every $A_g$ in the proposition.

## A forced interior vertex and two T-junctions

Every tiling of $A_g$ contains an interior vertex at which exactly four tile corners meet, one $\beta$ and three $\gamma$. Consider every point that is a tile vertex. An interior point is either filled by a full turn of tile corners, or lies inside the straight side of one tile, leaving a half turn for the corners of the other tiles. A noncorner vertex on the outer boundary also has a half turn. In an angular inventory $(A,B,C)$ counting $\alpha,\beta,\gamma$, irrationality of $\alpha/\pi$ and $\beta=(\pi-3\alpha)/2$, $\gamma=(\pi+\alpha)/2$ give the following complete possibilities.

| Available angle | Corner counts $(A,B,C)$ | Contributions $A-C$ |
|---|---|---|
| $2\pi$ | $(0,1,3),(2,2,2),(4,3,1),(6,4,0)$ | $-3,0,3,6$ |
| $\pi$ | $(1,1,1),(3,2,0)$ | $0,3$ |

Let $I_d$ count full-turn vertices with $d$ incident tiles and $H_5$ count half-turn vertices with five tile corners. The three outer corners each contribute $+1$ to $A-C$. Every tile has one $\alpha$ and one $\gamma$, so the total is zero. Consequently

$$I_4=1+I_8+2I_{10}+H_5.$$

At an $I_4$ vertex each of the three $\gamma$ corners has a side of length $b$, and the $\beta$ corner has none. Because there are three such incidences, one of the four rays has a length-$b$ side on one bank and a side of a different length on the other. The shorter of those sides ends inside the longer one. Hence every $A_g$ tiling has an internal T-junction.

For $(a,b,c)=(6,5,9)$ one bank starts with length 5 and the other with length $L\in\{6,9\}$. At distance 5 along that ray, the longer edge continues, and the next side on the short-edge bank must begin there. It has length at least 5, so it continues beyond distance $L<10$. The endpoint at distance $L$ of the first long edge is therefore a second T-junction, on the opposite bank. Both points lie in the interior because each is in the interior of a tile side whose line passes through the strictly interior four-tile vertex. Thus any proposed 280-tiling must contain this four-tile vertex and **two distinct T-junctions on the same ray**, at distances $5$ and either $6$ or $9$ from it.

## Proper triangular pieces for $u=1$

For $u=1, f=v\ge3, g=1$, a properly contained triangular union of unit tiles, if it exists in $A_1$, is similar to the unit tile. This consequence uses the listed prior necessities for the Group-1 shapes. It concerns triangular subregions, including those that do not touch any outer corner.

Indeed $A_1$ contains $bQ$ tiles, where $b=f^2-1, Q=2f^2-1, P=3f^2-1$. A $W_M$ requires $M\ge f$, so its area $QM^2\ge Q f^2>bQ$. The Paliy triangle requires at least $QP>bQ$. Another alpha-isosceles subtriangle needs a positive integer scale, and all such areas are at least $bQ$. A theta subtriangle requires $t\ge2f$, giving area $bt^2>bQ$.

The remaining possible type is the beta-isosceles $T_M$, with equal sides $Mf^3$, base $MP$, and base angles $\beta$. Since $f^3>P$ for $f\ge3$, its minimum width is its altitude to a leg, equal to $MP\sin\beta$. The outer $A_1$ has minimum width $bc\sin\alpha$, its altitude to its base. For a contained triangle its minimum width cannot exceed the outer minimum width, regardless of orientation. The sine law gives $\sin\beta/\sin\alpha=b/f$. Thus containment requires $M\le f^3/P<f/2$. Bonfioli's side-run corollary excludes $T_M(1,f)$ for $2M\le f$. This treats every nonsimilar target shape for this tile. It does not impose any requirement that an actual tiling possess a larger triangular subregion.

For $f=3$ these dimensions are $(72,72,136)$ on $(3,8,9)$. The theta candidates with sufficiently small area have $t=1,2,3,4$; $t=4$ does not fit by minimum width, since $\Theta_t$ has minimum width $tbf\sin\alpha$, requiring $t\le f$. Thus it suffices to exclude $t=1,2,3$. The exact corner search checks these small cases without the general theta necessity result.

## Sources and authorship

- [Beeson, arXiv:1206.2229v6, §14.3 (alpha condition and conjecture)](https://arxiv.org/html/1206.2229v6#S14.SS3).
- [Paliy's two-piece triangle](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/docs/two-piece-construction.md), also Beeson's Theorems 15 and 18, §§11.3 and 11.6.
- [Paliy's scale constructions, §5](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/docs/universal-rational-scales.md). The first gluing also appears in Beeson's Corollary 8 and Bonfioli's alpha-hub proposition.
- [Bonfioli's side-run, theta, W and beta necessities](https://github.com/ElVec1o/erdos_634_proof/blob/119bec0dd0158ddeb239686d5464eb7104e3b42d/paper/erdos-634.tex), especially Corollaries 1.7 and `cor:thetakill`.
- [Bonfioli's 18 November theta and hub discussion, including the audit qualification](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v6_main.tex#L389-L431).
- [Paliy's uniform reduction, §4 (five target types for this angle group)](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/uniform-reduction/PROOF.md).

The seam necessity and width comparison above are deductions in this investigation. Priority and journal peer review have not been established.

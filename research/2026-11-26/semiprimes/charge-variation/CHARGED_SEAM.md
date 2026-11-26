# A charged lift off the exterior path needs 149 or 171 unmatched tiles

Let $M$ count tiles without a half-turn mate on their whole long edge. If a lift off the exterior path has nonzero signed short population, then $M\ge149$ on the 3431 board and $M\ge171$ on the 5063 board. At these respective endpoints the first cut has only **two possible positioned boundary words per board**. They leave only 471 or 693 tiles, respectively 935 or 1365 tiles, outside the middle lift. Existence in any of these cases remains open. The result allows balanced occupied branches, both hands, all translations and T-junctions.

## A common three-cut inequality

Use the **standard frame** throughout the spine census. Root the [lifted tree](../joint-cell-tree/TREE.md) at its exterior path $C,B,T$ (heights 0,1,2). Delete the two spine edges and call the three regions axial, middle and slant. For the cut toward the slant at level $i=1,2$, let $E_i,O_i$ be its signed populations and $p_i,q_i$ the outward and inward signed owner counts in the convention of the [nested cuts](../boundary-word/README.md). Half-turn pairs contribute zero. Write $m_i$ for the actual number of unmatched owners. The residual signed populations of the three regions after removing these two banks of each cut are
$$
D=(-d-E_1-q_1,-c-O_1,\ E_1-E_2,O_1-O_2-p_1-q_2,\ E_2-p_2,O_2).
$$
The same equations hold on the lifted tree by its physical chain identity. Both spine boundaries have the prescribed full slant displacement.

Take the subtree spanned by $C,T$ and all nonzero short charges. If it extends off the exterior path, it has an off-path leaf $v$. The exterior-free component beyond its entering edge has just one nonzero short charge, $cg$ at $v$. If $v$ is odd the odd and even banks there have signed counts $cg,dg$. If $v$ is even these counts are interchanged. This follows by substituting the two component charges into the two cut characters with zero exterior term. It does not require the two bank populations to be monochromatic or any balanced descendant to be empty. Both banks are in one of the three regions. Insert $cg,dg$ in the appropriate two entries of the six-vector $L$, leaving the other entries zero. Each unmatched owner uses exactly one lifted edge, hence
$$
M\ge m_1+m_2+(c+d)|g|+\|D-L\|_1 .
$$
In particular the signed charges needed on an extra cut need not be paid twice out of the regional reserve.

The finite minimization in [charged_cut.py](charged_cut.py) uses integral cut characters, the slant displacement and the minimum unsigned direction counts for its signed bank vectors. For $M\le320$, each component satisfies $|E_i|+|O_i|\le320$ because its half-turn pairs cancel. Both charges are multiples of $c$ on the slant side. For either displacement alphabet enumerate the two axial coordinates within the hexagonal distance bound. Subtract its displacement to get the other bank's vector. Its character and vector determine all three signed axis counts uniquely. The sum of their magnitudes is the unsigned lower bound. The [direction formulas](../boundary-word/remote.py) include the rotation of the second cut. Values above the ceiling already exceed every entry below.

| Leaf parity | Axial region | Middle region | Slant region |
|---|---:|---:|---:|
| Even, 3431 | 171 | 159 | 203 |
| Odd, 3431 | 149 | 181 | 181 |
| Even, 5063 | 213 | 193 | 263 |
| Odd, 5063 | 171 | 235 | 221 |

## Distance to the only odd charge

For each odd short lift, its incoming even long owners have total sign $dG_v/c$ in either consistent frame. This follows from the cut characters or the [receiving-bank calculation](README.md). The two signed populations require at least $(c+d)|G_v|/c$ unmatched owners, disjoint as the odd marker varies. Hence $M\ge(c+d)V$. In particular $M<3(c+d)$ forces $V=1$. Write $v$ for the unique charged odd lift. Its standard-frame charge is $-c$.

For the following local calculation **negate standard signs to use the path-frame equations** and keep the same named markers. Consider any nonspine edge. On an exterior-free side with unit odd charge, the absolute bank sum has the form
$$
F(i)=|ci-d|+|di-c|
$$
for integral corrected even charge $i$ (or its simultaneous sign reversal). Its minimum $f$ is 22 or 42, obtained at $i=1$. On a side with no odd charge the cost is $(c+d)|i|$. If the distance from $B$ to a nonnative $v$ is $2r$, every intermediate odd vertex on their path contributes at least $2f$: its two path edges both cut off the charged side or its complement. Neither is a spine edge. At $v$ itself the short and incoming signed populations cost at least $c+d$. These odd markers and $B$ count disjoint tiles.

At $B$ charge location fixes the odd populations beyond the two spine cuts. In standard signs $(O_1,O_2)$ is $(0,0)$ for the axial direction, $(-c,-c)$ for the slant direction, or $(-c,0)$ for a middle branch or $v=B$. Set $h=-(E_1-E_2)/c$, the path-frame sum of corrected even charges in the other directions at $B$. Their cost is at least $(c+d)|h|$ unless they contain $v$. In that last case one distinguished off-spine gate costs $F(i)$ and the others together at least $(c+d)|h-i|$. Minimizing these terms together with the spine displacement costs gives:

| Board | $v=B$ | Toward $C$ | Toward $T$ | Other direction |
|---|---:|---:|---:|---:|
| 3431 | 107 | 86 | 118 | 118 |
| 5063 | 149 | 106 | 170 | 170 |

For a nonnative $v$, add $c+d+2(r-1)f$ to the appropriate entry. For example, before $M=189$ at 3431 a displaced source can only be at distance two, and before $M=181$ it must lie beyond $C$. Before $M=195$ at 5063 it can only be adjacent to $C$. On either board at the charged-leaf endpoint the leaf table requires an odd leaf and the distance bound places it adjacent to $C$. These thresholds apply to $M$, independently of the number of odd tiles.

## Exact boundary at the endpoint

At $M=149$ or $171$ under the off-path charge hypothesis, both bounds are equalities. The unique axial minimum has $(p_1,q_1,p_2,q_2)=(-c,0,0,c)$ and zero middle even residual. All unmatched owners occur on the two spine gates and the $C$–$v$ gate. Indeed the $v$ contribution is exactly $c+d$, so its incoming bank has just $d$ unmatched owners, all aligned in sign. A gate there away from the path has aligned signed even count divisible by $c$, hence zero, and equality precludes unmatched owners on it. Equality at $B$ leaves no owners beyond the two spine gates. Every other odd marker contributes zero. Any nonempty additional exterior-free component would then have zero physical boundary by the lifted cut identity, an area contradiction.

Work again in **standard** signs. Let $a,b,c$ denote the side lengths, and put $l=3,5$ on the respective boards. On the first cut the unique minimal signed direction triples in the two alphabets are $(b,-l,a)$ and $(0,-l,l)$. The second cut has $(0,0,0)$ and $(0,0,c)$, giving the straight slant with $c$ middle-tile owners and zero area beyond it. The first cut has no opposite-letter cancellations because it realizes the sum of the absolute entries of its triples. Its five available letters all advance strictly in one common linear coordinate (in the middle coordinates below use $x-y$ for the high and low letters, except low-4 also has positive increment $a-b$). Thus there is no directed circuit. The endpoint boundary is one source and one sink, so the whole chain is a single path from $Y$ to $X$.

Use middle coordinates $z^{-1}(p-Y)$ and number the letters as follows. The last column gives the boundary of the remaining pairs after removing a middle-tile owner when present. Write $u_0=(1,0),u_1=(0,1),u_2=(-1,1)$.

| Letter | Count | Displacement | Repaired steps |
|---|---:|---|---|
| 0 | $b$ | $(a+b,-b)$ | $a u_0,-b u_2$ |
| 1 | $l$ | $(a,-a-b)$ | $-a u_2,-b u_1$ |
| 2 | $a$ | $(-b,-a)$ | $-a u_1,-b u_0$ |
| 3 | $l$ | $(c,-c)$ | $-c u_2$ |
| 4 | $l$ | $(0,-c)$ | $-c u_1$ |

The reverse slant adds $b u_2,a u_1$ repeated $c$ times. These steps result from replacing the CCW long side of each removed middle tile by its two short sides. The two other first-path letters retain the reversed core long side. This gives the entire directed boundary of the actual half-turn pairs at $B$, even if their union is disconnected.

### Ordered-word exclusion

Each pair is an $a$-by-$b$ parallelogram on two unit axes. On the torus of periods $sR$, $s=a,b$, its direction-labeled endpoint differences sum to zero. On a line of fixed normal residue this forces the sum of signed lengths to vanish modulo $s$. The following reductions precede the exact path census:

* On axis 0 modulo $a$ only the $a$ occurrences of the length-$b$ part of letter 2 contribute. Their starts on each normal residue have multiplicities invariant under a shift by $b$ along the line, by endpoint cancellation. Since $a,b$ are coprime all $a$ starts have the same $y$ residue and use every $x$ residue once. The first repaired piece changes $y$ by $-a$. Modulo $b$ the $b$ occurrences of letter 0 likewise have one $y$ residue and distinct $x$ residues.
* On axis 1 modulo $a$ only letters 1 and 4 remain. Their starts have the same $x$ residue as the original letter. Each normal class must satisfy $bi+cj=0\pmod a$, $0\le i,j\le l$. The only solutions are $(0,0),(l,l)$ on both boards.
* On axis 2 modulo $a$ all slant starts have normal $x+y=0\pmod a$. At a nonzero normal the surviving pieces come from letters 0 and 3. Their counts satisfy the same congruence with $0\le i\le b$, $0\le j\le l$. Every nonzero solution consumes more than half of the $l$ available letters 3. Consequently all nonzero normals used by letters 0 and 3 are identical.

[seam.cpp](seam.cpp) enumerates all paths satisfying these conditions, extending alternately from their two specified endpoints. It then checks full torus currents, containment and disjoint interiors of every path and slant owner, and the [physical width and area inequalities](../terminal-contact/TERMINAL.md). Coordinates for containment and intersections are integral after multiplying by $c$. In particular every pair is counted twice in the sum of directional strip integrals divided by $ab$. The middle lift is balanced, so its population must be divisible by $2c$.

### Integer starts of the strip intervals

An additional test couples the three axes. Write $W(t)$ for the cumulative width in one axis, so a pair with side $a$ on the axis contributes height $a$ for $b$ consecutive integer slices, and vice versa. Let $P_t,Q_t$ be the numbers of the two types starting at $t$. The jumps $J_t=W(t)-W(t-1)$ satisfy
$$
J_t=a(P_t-P_{t-b})+b(Q_t-Q_{t-a}).
$$
Starting below the support, this fixes all $P_t\bmod b$ and $Q_t\bmod a$. Subtract the two interval families corresponding to the least nonnegative residues. The remaining width divided by $ab$ must be a nonnegative integral sum of intervals of lengths $b$ and $a$. On each positive run its area has the form $bi+aj$. Matching each unit rise to a unit drop reachable by steps $a,b$ is necessary: each interval is a forward edge, and a finite integral flow decomposes into source-to-sink paths. All rises, drops and distances here are actual integer slice coordinates. A choice of $i$ adds $bi$ to the original number of pairs presenting an $a$ side on this axis. Across all axes these counts must add to the number of pairs, since each parallelogram has one axis of length $a$. [strip_starts.py](strip_starts.py) tests this shared count and the matching; neither assumes that separately feasible interval decompositions use the same set of pairs.

| First paths left | 3431 | 5063 |
|---|---:|---:|
| After the three normal-residue conditions | 26,866 | 801,726 |
| Full endpoint currents | 766 | 1,792 |
| All positioned owners compatible | 166 | 373 |
| Width semigroups and area | 6 | 8 |
| Integer interval starts and shared pair count | 2 | 2 |

In both cases the surviving words are $2^a3^l1^l4^l0^b$ and $4^l2^a1^l0^b3^l$. Their respective middle populations are 2960 and 2738 at 3431, or 4128 and 3698 at 5063. These are necessary boundary words; no completion is asserted. Larger $M$ and cases with every off-path lift balanced remain open.

Run `python3 seam_replay.py | diff - SEAM_STATUS.json` with a C++17 compiler. Both complete 143 coordinate controls give 60 actual pairs and satisfy the new interval-start and orientation accounting. The ordinary native signed-bank relaxation independently recovers their observed $M=23$. They do not instantiate the target-specific charged equality. [Recorded replay](SEAM_STATUS.json).

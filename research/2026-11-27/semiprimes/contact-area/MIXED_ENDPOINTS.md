# The first whole-board mixed endpoint fails on each board

Let an exterior-free gate in the standard lifted tree have nonzero signed far populations on both parities. Let $M$ count all tiles of the board without a physical half-turn mate, and let $Z$ count such tiles on exterior-free gates whose two signed far populations vanish. Then
$$
 M\ge\max(175,173+Z)\quad(N=3431),\qquad
 M\ge\max(215,213+Z)\quad(N=5063).
$$
The additive terms come from the [four-gate theorem](FOUR_GATES.md). The improvement by two at the first physical endpoint concerns the total $M$. The [mixed-branch population bound](TWO_GATE_POPULATION.md) applies at any $M$.

## What equality forces at the native middle lift

Set $d=a-b$. At the old whole-board minimum $M=173$ or 213, $Z=0$. The four-gate minimization gives exactly one signed row on each board. The [replay](positioned_mixed.py) asserts its complete contents. The mixed gate has $(E,O)=(-c,-c)$, odd far root $v$ and near bank in the axial native region. Its signed far and near banks are $-(c-d)$ and $c-d$. The deeper gate has even far charge $-c$, with signed banks $-c,-d$. The two native gate rows, in the notation $(p,q,E,O,m)$ of the four-gate theorem, are $(-c,0,0,0,49)$ or $(-c,0,0,0,63)$ followed by $(0,c,0,0,c)$. Both the exterior regional residuals and the shell residual vanish. All four costs sum to $M$. Thus every unmatched owner is on one of these four physical gates. The mixed gate has 24 owners at 3431 and 42 at 5063.

The mixed near node is the axial node $C$. Otherwise only its near bank could supply its short charge, and $c-d$ is not divisible by $c$. The deeper edge leaves $v$ directly, since its near bank alone would give an intermediate node charge $-d$. Any further occupied branch would be exterior-free and have positive area with zero boundary chain. Thus $v$ and its even child comprise the mixed subtree. The middle native lift $B$ is balanced. Its unmatched tiles occur only on the two native gates.

These facts recover all hypotheses of the **middle-region** argument in the [charged-seam proof](../../../2026-11-26/semiprimes/charge-variation/CHARGED_SEAM.md). The native displacements and their minimal owner counts force the same directed triples and the same straight slant. Removing the specified middle owners leaves only actual half-turn pairs in that middle region. The positional strip and word tests there leave exactly the same two possible first paths A and C. Their derivation places no constraint on the tiles deeper inside the axial region. Remove the specified axial owners of the first path as well. The residual boundary is the [previously computed axial polygon](../remote-sections/CHARGED_EQUALITY.md) for the relevant word. Its sides have the axial marker. Its interior can include both short lifts of the mixed branch.

## Exhausting the mixed contours at these endpoints

By the [physical circuit theorem](../../../2026-11-26/semiprimes/charged-contour/README.md), the whole mixed boundary is one positive Jordan circuit. Indeed its length is below $c+d$, so every constituent circuit has zero alternating charge and equal signed parity totals divisible by $c$. A circuit carrying a nonzero unit costs at least $2(c-d)$ owners. At most two other edges would remain at 3431 and none at 5063, too few for any further circuit. Its enclosed area is the complete mixed far population, at least 370 or 516 tiles.

Both hands of the incident short translate and all its positions must be included. For word C we use all $2c-1$ nonnative neighbors of $C$. For word A the convex-ended wall listed in the axial polygon proof has length $3c$ or $5c$. Listing the nonnegative representations of that length by $a,b,c$ gives only three or five whole long sides. Strict convexity at the endpoints prevents overhang. Each side lies on the residual boundary, so its owner has the axial long marker and no residual long mate there. It belongs to the mixed far bank: the other nonnative cut joins $v$ to its child and does not reach $C$. The positive-hand translate at the wall start is the native $B$, which forces the negative-hand translate 34 or 28. All four or six successive wall vertices are compulsory in the circuit and the prescribed wall steps join them in the positive boundary direction.

Write the alphabet in the axial chart. The far bank negative owners give the three even headings of the original charged-contour templates. The near bank positive owners are obtained by a half-turn of the three near negative templates. At 5063 each bank has 21 owners of its specified sign. At 3431 the bank characters have absolute sum 22 and the circuit has 24 edges. Exactly one letter of the entire contour has the opposite sign from its bank's specified sign. Allow each of the six possible template types for this letter, with one additional normal letter on that bank to preserve its signed count. For fixed bank counts the replay lists all heading triples on one bank and matches the exact displacement against each triple on the other. On each bank the three direction vectors are affinely independent, so a fixed total and displacement determine the triple.

For every candidate owner require both endpoints and its obtuse vertex inside the closed residual. In the free product of the three cyclic axis groups of order $q$, both short and long sides have their actual physical displacement as exponent along the projected axis. For a far letter of heading $j$ the axis is $j$ modulo three. For a near letter it is $j+s$ at $q=a$ and $j$ at $q=b$, since $cz^s=a+bU_s$. Half-turns preserve the axis and negate the displacement. Use both orders at 3431 and order 35 at 5063. Every actual cyclic rotation has identity word. The [bounded-inventory grammar](../../../2026-11-26/semiprimes/charged-contour/README.md) admits the additional seventh letter in its own axis group. A possible concatenation of displacements $D_1,D_2$ adds their determinant to the sum of doubled signed areas closed by the two chords. This gives a maximum area at each retained physical start. In units $qc$ the threshold is $ab/q$ times the population floor in blocks. At every pass all vertices of an actual circuit would survive both the identity and area requirements. For word A its required wall sites must also survive. The finite start set decreases until it stabilizes or becomes empty.

| Board | Translate and outer-word cases | Word A inventories rejected | Word C inventories rejected | Inventories retained |
|---|---:|---:|---:|---:|
| 3431 | 74 | 18 | 1314 | 0 |
| 5063 | 86 | 7 | 595 | 0 |

Thus the unique signed endpoint row on each board fails in physical position. The parity $M\equiv N\pmod 2$ gives the new bounds.

## Reproduction

From this directory run the following commands with assertions enabled, NumPy, SciPy and a C++17 compiler. The physical controls use both complete 143 coordinate files. The older six-letter census and its exhaustive small-grammar control can also be replayed with the generalized engine.

```sh
python3 endpoint_control.py | diff - ENDPOINT_CONTROL.json
python3 positioned_mixed.py | diff - POSITIONED_MIXED.json
(cd ../../../2026-11-26/semiprimes/charged-contour && python3 replay.py | diff - STATUS.json)
```

Both original counts remain open. The outstanding cases include larger unmatched populations and tilings in which no exterior-free gate carries both parity charges. No upper bound on the total unmatched population sufficient to contradict these lower bounds has been proved.

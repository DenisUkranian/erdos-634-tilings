# The contiguous interval through 279 and the next unresolved input

Bonfioli's public v6.0 program output contains 52,045 unresolved **nonsquarefree** counts at most \(10^6\), starting with \(236,280,284,332,351,423\). Its header distinguishes individual Lean exclusions from the rest of the census. It does not settle squarefree numbers or specify whether absent values are positive or negative. The first two entries directly establish that 236 and 280 were open in that release. [Pinned census](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/data/census/undecided_6.0.txt).

Combining Bonfioli's Theorem 1.3 for \(1\le N\le200\), the earlier exact reductions for \(N=231\) and the prime rows, the current certificate for 236, and the finite calculation below gives **139 positive and 140 negative counts through 279**. This interval uses the project's computer-assisted proof at 236. After the obstructions recorded for 280, its surviving target is alpha-isosceles with \((u,v,t)=(2,3,2)\). No complete straight vertex-to-opposite-side seam is possible for that candidate, by the [unrestricted theta-six exclusion](../theta6/PROOF.md). The smallest input left unresolved by the combined materials is **280**. [Current proof for 236](../beta/MESH_PROOF.md), [earlier geometric reduction at 280](../../nov19/alpha280/RESULTS.md), [alpha seam analysis](../alpha/VERTEX_SEAMS.md).

The positive counts from 201 through 279 are
\[
\begin{aligned}
&202,205,207,208,212,216,218,221,224,225,226,229,232,233,234,240,241,\\
&242,243,244,245,250,252,256,257,260,261,264,265,269,272,274,275,277.
\end{aligned}
\]
The remaining 45 integers in this interval are excluded, including 231 and 236. [Status and source for each of the 280 inputs](census279.json).

The arithmetic engine decides all 201–279 values except the nine below, and in particular decides every squarefree value in the interval. The negative decision for the squarefree number 231 uses the previous exhaustive geometric exclusion for its single surviving equilateral target. [Base engine](../../nov19/global/decision.py), [231 certificate](../../nov19/equilateral231/RESULT_UK.md), [Theorem 1.3](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/README.md).

| Counts | How the remaining shapes are decided |
| --- | --- |
| 204, 220, 228, 276 | Only theta and double-angle targets remain, at multiplier 2. The theta base word implies \(t\ge4\). Every candidate double-angle ratio \((f+e)/(f-e)\) here exceeds \(2t-1=3\), violating Bonfioli's Theorem F. |
| 236 | The unique beta triangle with tile \((20,9,25)\) is excluded by the current vertex-star certificate. |
| 240 | Paliy's equilateral 240-tile seed has side 60 and tile \((3,5,7)\). |
| 248 | W with \((e,f,t)=(6,7,2)\) is excluded by the W-gap theorem; the only W count at \(t=2\) is 28. |
| 264 | Paliy's F3 construction for \(a/b=5/3,\ c=7\) gives \(3(a+b)(a+2b)=3\cdot8\cdot11=264\). |
| 279 | Theta multiplier 3 is impossible; its double-angle ratio is \(31>5\); its W pair \((1,4,3)\) violates \(te\ge f\). Bonfioli also explicitly excludes 279. |

The replay checks each candidate in the overlist and raises an error on an unaccounted candidate. It retains the reference flag for the internal 236 certificate. The pinned Bonfioli paper explicitly records negative results for 204, 276 and 279; several other rows can be decided directly from its general theorems. [Replay](census279.py), [Bonfioli, Theorem F, examples, and theta base word](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_primes_and_N200.tex), [reduced theta word test](../norm91/RESULT.md), [W at multiplier 2](../../continuation/RESULTS.md), [240 seed](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/final-closure-oct8/equilateral240/PROOF.md), [positive F3 cone](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/universal-closure-oct8/global/F3_UNIFORM_CONE.md).

The separate exact coordinate replay checks the pinned original files for 240 and 264 against their Git blob identifiers. For each it recomputes every tile's three lengths, target containment, pairwise separation of interiors and area equality. All 28,680 pairs for 240 and all 34,716 pairs for 264 pass. This verifies both constructions by coordinates. [240 original](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/final-closure-oct8/equilateral240/equilateral_240.json), [264 original](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/group2-gamma-corners/f3-264.json), [independent checker](replay_census_positive.py), [results](replayed_census_positive.json).

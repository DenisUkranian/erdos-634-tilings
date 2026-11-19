# The (6,5,9) tile on the theta-six and alpha-two targets

Let $d=i\sqrt2$ and use rational coordinates $x+yd$. For the theta-six target $(90,90,60)$ the vertices are $0,60,30+60d$. The area is 180 unit tiles. The finite certificates exclude every tiling in which all vertices lie in $D^{-1}\mathbb Z[d]$ for $D=9$ and $D=27$.

| Target | $D$ | Surviving placements | Boundary demand | Positive excess | Certified lower bound |
|---|---:|---:|---:|---:|---:|
| theta-six | 9 | 76,470 | 183,324,756 | 2,977,784 | 180.346972 |
| theta-six | 27 | 152,456 | 180,557,650 | 546,228 | 180.011422 |

The pool enumerator uses exact lengths, containment and cancellation of oriented edge endpoints to remove impossible positions. For each remaining placement $t$, the independent verifier computes the weighted sum $w(t)$ at the starts of its three counterclockwise edges and subtracts the weights at the ends, using the unoriented line as part of the key. When the target boundary demand is $B$, a tiling with $n$ tiles would satisfy $B\le10^6n+\sum_t\max(0,w(t)-10^6)$. This follows from internal cancellations and from the fact that a placement can be used at most once. The integer weights yield the strict lower bounds in the table, each larger than 180.

In particular any theta-six tiling would require a length-five edge at height $|h|\ge4$, relative to the outer base and the unit direction $z=(-1+2d)/3$. If every length-five height were in $[-3,3]$, the length-six and length-nine displacements, at heights $h\pm1$ and $h\mp2$, would also lie in $3^{-3}\mathbb Z[d]$. The entire-seam connectivity argument in [GRID136.md](../GRID136.md) applies unchanged, placing all vertices in the excluded grid.

The [unrestricted theta-six exclusion](../../theta6/PROOF.md) now covers every rotation and translation. By the [straight-seam criterion](../VERTEX_SEAMS.md), it also excludes every tiling of the $(90,90,140)$ alpha-two target with a complete straight seam from a vertex to the opposite side. The case with both apex rays ending at interior vertices remains open.

As a separate constructive test, the archived $(6,5,9)$ tilings with 207, 224 and 320 tiles and Paliy's 322 construction were uniformly dilated by each integer from 1 through 12 and subdivided by the ordinary triangular grid. An exact scan of the 48 resulting tilings found no complete-edged embedded copy of theta-six or alpha-two. It recovered theta-eight in its published 320-tile example. This construction experiment was not used for either exclusion.

For alpha-two itself, the $D=9$ pool contains 259,328 positions. An endpoint relaxation conditioned on each of the three choices of corner tiles up to reflection reached a maximum equation residual below $1.5\times10^{-14}$ after 50,000 iterations. The solver used floating-point weights between zero and one. Attempts to extract a rational fractional cover or an actual tiling from these weights were inconclusive. This grid itself remains undecided for alpha-two.

Iterating vertex-fan and whole-edge tests reduced the grid to 196,212 positions. Reapplying those tests separately after fixing the two corner tiles left 191,882, 190,732 and 189,582 positions. The endpoint relaxations also failed to separate these smaller pools. For one of the closest integer weight vectors on the global pool, the sum of the 280 largest scores exceeded the target score by 560. This numerical search supplies no D9 exclusion for alpha-two.

From this directory run the existing pool generator, followed by the Python standard-library verifier. Each resulting pool has a companion file ending in `.shapes`.

```sh
c++ -O3 -std=c++17 ../../../nov19/alpha280/pool.cpp -o /tmp/pool659
/tmp/pool659 9 180 /tmp/theta-six-9
python3 verify_grid.py /tmp/theta-six-9 grid180-weights.tsv.gz
/tmp/pool659 27 180 /tmp/theta-six-27
python3 verify_grid.py /tmp/theta-six-27 grid180-d27-weights.tsv.gz
```

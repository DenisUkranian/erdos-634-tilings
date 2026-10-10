# Two additional structural deductions and an explicit obstruction to naive extrapolation

**9 October 2026 — research continuation.** These observations combine proved statements already in the Erdős 634 repository. They are *not* a solution of the full problem, a new 14430 exclusion, or a claim that a displayed sufficient construction is necessary.

## 1. High-ratio F3 tails cannot exhibit two separated extreme height gaps (when `ab` is even)

**Proposition.** Fix a primitive integral 120-degree triangle `(a,b,c)` with `c²=a²+ab+b²`, `ab` even, and

```
a/b > (5+sqrt(33))/2.
```

Consider a hypothetical multiplier-one F3 tiling of the canonical target, containing `N=3(a+b)(a+2b)` copies. In the short-edge height normalization of the repository, the exterior sides have heights 0, 2, 3. Let a *separating extreme gap* mean an empty height `k>=3` with occupied heights larger than `k`, or an empty height `k<=0` with occupied heights smaller than `k`. Then:

1. Every nonempty separated extreme tail consists of **exactly `2c²` tiles**.
2. The tail has just one positive-area connected component and contains no positive-area hole.
3. There cannot be **two distinct separating gap components**: neither two genuinely separated gaps on the same extreme side (with an occupied slab between) nor one gap on each of the upper/lower extremes.

The proposition does *not* rule out a gap between exterior heights 0, 2, and 3, nor does it forbid one separating extreme gap.

**Proof.** The general [whole-`c` boundary theorem](https://github.com/DenisUkranian/erdos-634-tilings/blob/main/research/gap-closure-oct8/structure/WHOLE_C_BOUNDARY.md) applies to any connected tail isolated across an empty height outside the exterior height interval. At such an interface every edge is an actual whole long `c` edge; arbitrary T-junctions do not change the result. Because `ab` is even, each positive-area component has tile population divisible by `2c²`, hence at least `2c²`. The area count satisfies

```
4c²−N = a²−5ab−2b² > 0
```

under the ratio hypothesis, while `N−2c²=a²+7ab+4b²>0`. Thus no such tail can contain 2 components, and its tile count must equal `2c²`. A hole would be filled by a disjoint positive-area region with the same class of whole-`c` boundary and therefore at least another `2c²` tiles, contradicting `N<4c²`.

If two separating gaps occur on opposite extremes, their tails are disjoint and require at least `4c²` tiles together, impossible. If two genuinely distinct gaps occur on the same extreme, one resulting nonempty tail is properly contained in the other, and each would have exactly `2c²` tiles, contradicting the positive number of tiles in the intervening occupied height levels. This proves the proposition. QED.

**Example.** For `(a,b,c)=(56,9,61)`, the unique `N=14430` candidate:

```
c² = 3721,   2c² = 7442,   4c² = 14884,
N = 14430,   N−2c² = 6988,
a/b = 56/9 > (5+sqrt(33))/2.
```

Any hypothetical extreme-height gap therefore separates exactly 7,442 tiles from the remaining 6,988; a second separated gap is forbidden. This is a necessary **search restriction**, not a proof that 14430 cannot be tiled.

## 2. Why the *exact* adjacent W construction does not automatically extend to nonadjacent `u,v`

Let coprime `0<u<v`, put `d=v−u`, `b=v²−u²` and `m=v+t`. The published [all-adjacent-scale construction](https://github.com/DenisUkranian/erdos-634-tilings/blob/main/research/gap-closure-oct8/group1/PROOF.md) uses a central strip whose short-direction left boundary at height `y=uv²` has `x=−v³` and whose horizontal width is `W=b(u+t)`. Accordingly its upper-right strip endpoint has

```
x_strip = −v³ + b(u+t).
```

The neighboring outer annulus in that *unchanged* macro decomposition has an endpoint

```
x_annulus = −u²v + b(t−1).
```

Their difference is the exact identity

```
x_strip − x_annulus = −b(v−u−1) = −b(d−1).
```

It vanishes identically when `d=1`, the case proved in the repository. For every `d>=2` it does not vanish: the two existing macro boundaries do **not** join. A naive substitution of nonadjacent parameters into the adjacent proof would therefore be invalid, even though its internal rectangles separately admit nonnegative `u,v` strip decompositions. A genuinely new transition region or a changed outer annulus is needed. This is an obstruction to *that formula only*, not a nonexistence result for W or beta tilings.

## 3. Coprimality is a normalization, not an extra geometric sector

If `u=dU, v=dV`, the tile `(uv,v²−u²,v²)` is `d²` times the primitive tile `(UV,V²−U²,V²)`. The W and beta target side lengths are `d³` times their counterparts at scale one in `U,V`. Hence a W/β tiling with unreduced multiplier `m` corresponds exactly to the primitive parameters at multiplier `dm`, with the same count `d²Q(U,V)m²=Q(U,V)(dm)²` (and beta analog). Noncoprime pairs therefore introduce no new shapes, branches, or tilings beyond the primitive spectra.

These three deductions together clarify which difficulties are genuinely geometric: nonadjacent **primitive** W/beta scale coverage, F3 at high side ratio, and global necessity-vs-sufficiency of the branch criteria.

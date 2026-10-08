# Empty orientation levels force square divisibility

7 October 2026. Research for Denis Paliy. This is a necessary condition,
not an exclusion of 154 and not a solution of Erdős 634.

Let a primitive integral 120-degree tile have sides `(a,b,c)`, with
`c²=a²+ab+b²`, and let `rho=exp(i*pi/3)` and `z=(a+b*rho)/c`.
Normalize an I120 target so that its exterior direction heights are
`-1,0,1`, with height zero on the base. Let `n_h` count its tiles whose
two short edges have height h. Arbitrary T-junctions are allowed.

## The square-divisibility theorem

For every positive integer k with `n_k=0`,

    c² divides sum_{h>k} n_h.                          (1)

For every negative integer k with `n_k=0`,

    c² divides sum_{h<k} n_h.                          (2)

**Proof of (1).** Apply the [whole-edge cut identity](../../../docs/height-cut-area.md)
at k. Since k is at least 1, the target boundary has no edge height
strictly greater than k. The identity therefore expresses the boundary
of the actual union of all short-height-greater-than-k tiles as a balanced
signed sum of selected **whole** c-edges.

In a 120-degree tile both short edges have height h and its c-edge has
height h-1 or h+1. A nonzero selected edge at this cut can only come from
a height-k tile whose c-edge has height k+1, or from a height-(k+1) tile
whose c-edge has height k. The former tiles do not exist, by `n_k=0`.
Consequently every selected step has length c and direction `rho^j z^k`.

Decompose the balanced whole-edge graph into closed directed walks.
After translation, every such walk has its vertices in `c z^k Z[rho]`.
Shoelace area is thus an integer multiple of `c² sqrt(3)/4`.
The sum of the signed walk areas equals the area of the actual tile
union, irrespective of holes, self-intersections of individual walks,
or coincident edges in its chain representation. That area also equals

    ab (sum_{h>k} n_h) sqrt(3)/4.

Primitivity gives `gcd(ab,c²)=1`; hence (1). Reflecting the configuration
reverses the height indices and proves (2). No claim that the selected
walks are themselves component boundaries is required. ∎

## Sub-c-squared tilings have contiguous height support

Suppose the I120 tiling has `N<c²` tiles and `c` does not divide N.
The existing [population theorem](../../i120-global-oct7/HEIGHT_LEVELS.md)
implies `n_0=N mod c`, so zero is occupied. Equations (1) and (2) imply
that no empty nonzero height can separate zero from another occupied
height: the corresponding positive tail would have at least c² tiles.
Thus its occupied heights form a contiguous integer interval `[L,U]`
with `L<=0<=U`.

Writing `r=N mod c`, with `1<=r<c`, the same population theorem yields

    U-L <= (N-r)/c.                                    (3)

For tile `(8,7,13)` and N=154 this gives

    L<=0<=U,   U-L<=11,   -11<=L<=U<=11.               (4)

There are 78 possible intervals containing zero of width at most 11.
The new two-class obstruction removes the width-zero and width-one
possibilities, leaving 75 possible exact supports, grouped into 40
reflection orbits. This is a finite family of direction bands, not a
feasible enumeration of all their placements and not a refutation.

## Stronger budget for partial placements of the 154 target

Let `k_h` be the already placed population at height h and put
`L=min(0,{h:k_h>0})`, `U=max(0,{h:k_h>0})`. Any completion must occupy
every integer height between L and U. It therefore contains at least

    11 + 13 max(0, ceil((k_0-11)/13))
       + 13 sum_{h=L, h!=0}^U max(1, ceil(k_h/13))      (5)

tiles. A partial placement for which (5) exceeds 154 cannot extend.
This improves the earlier contact-connectivity budget, which only
required extra occupied heights across gaps larger than two.

## Limits of the argument

The distinction between an empty level and an occupied level is
essential. At a cut with both adjacent populations present, selected
whole c-edges have two heights and generate a lattice of area index c,
not c². Replacing c by c² at that cut is unjustified.

There is a direct positive-region warning: the parallelogram with
side vectors `c` and `ac z` can be tiled with 2c copies of the tile,
all at short height one. Its boundary can be partitioned into c-steps
at heights zero and one. Thus positivity plus a mixed-height whole-c-step
boundary alone cannot imply c² divisibility. This example, proved in
the population note, does not assert that the parallelogram embeds in
the 154 target, but it rules out that proposed standalone lemma.

The known nonconvex pure-island example and its embedding in a triangular
target also preclude simply removing every extreme component by a local
opposite-chirality replacement. The present theorem makes no replacement
assertion. Neither three or more consecutive heights nor an extreme
height adjacent to another occupied height is excluded here.

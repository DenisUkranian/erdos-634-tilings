# I120 boundary search and orientation population budgets

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

**154 remains unresolved.** This note gives exact consequences of the
existing [height-population theorem](../i120-global-oct7/HEIGHT_LEVELS.md)
and reports an exploratory search of one boundary-count row. It supplies
no complete refutation certificate and no classification of all N.

## Population lower bound for a partial placement

Suppose an N-tile target satisfies the proved population conditions

    n_h = 0 (mod c), h != e;       n_e = N (mod c),

where e is the exceptional short-edge orientation height. Write
`r = N mod c`, with `0 <= r < c`. If a partial placement already has
`k_h` tiles at height h, every completion has at least

    L(k) = r + c max(0, ceil((k_e-r)/c))
                 + c sum_{h != e} ceil(k_h/c)

tiles. The proof is immediate but useful: each summand is the smallest
nonnegative integer in the required congruence class that is at least
the population already placed. These lower bounds concern disjoint
height classes, so they add. Therefore `L(k)>N` rejects the partial
placement. Passing the test does not establish extendibility.

For the canonical horizontal-base normalization of 154, `c=13`,
`e=0`, and `r=11`. The attached search puts one length-91 side
horizontal instead, using a reflection and a rotation; its exceptional
height is `e=-1`. It applies precisely this rounded-population test.

## The occupied heights have gaps of at most two

The graph whose vertices are actual tiles, with adjacency when two
tiles share a positive-length contact, is connected. To see this,
join interior points of two tiles by a path in the target interior,
perturbed to avoid all tiling vertices. Successive tiles traversed by
the path meet along an actual positive-length contact. This argument
allows T-junctions.

A tile of short-edge height h has edge heights h and h+1, or h and
h-1. Collinear contacting edges have the same height. Thus contacting
tiles have short heights differing by at most two.

Consequently the sorted set of all occupied heights has successive
gaps at most two: a larger gap would disconnect the contact graph.
If there are K occupied heights, its total span is at most `2(K-1)`.
When `r>0`, the exceptional height e is occupied and

    K <= 1 + (N-r)/c,
    |h-e| <= 2(N-r)/c  for every occupied height h.

For **154**, this proves `K<=12`, total occupied-height span at most
22, and, in the canonical normalization, **every occupied height lies
between -22 and 22**. In the attached reflected normalization the
containing interval is [-23,21]. This is a necessary finite orientation
range, not a bound independent of N and not a tiling criterion.

## An optional stronger budget, including missing intermediate heights

When `r>0`, form the sorted mandatory set

    H = {e} union {h : k_h>0} = {h_1 < ... < h_s}.

Between mandatory heights separated by d, at least
`max(0,ceil(d/2)-1)` further heights must be occupied. They are absent
from the partial placement, and none is the exceptional height because
e already belongs to H. Each therefore requires at least c tiles.
The disjoint gaps give the stronger necessary lower bound

    L_connected(k) = L(k)
       + c sum_{i=1}^{s-1} max(0, ceil((h_{i+1}-h_i)/2)-1).

This follows only from contact connectivity and the proved population
congruences. It is valid with arbitrary reflections and T-junctions.
The recorded probe used L, not this additional connectivity correction.

## Pure-long 91-side probe: exact scope

The remaining length-91 boundary count rows for 154 are

    (A,B,C) = (0,0,7), (2,7,2), (3,4,3), (4,1,4),

where the edge lengths are (8,7,13). The probe treats only `(0,0,7)`.
Fixing one equal side as the selected side loses no case within the
subcase that at least one equal side is pure-long: reflect the isosceles
target if necessary.

The target is represented in the Eisenstein basis `(1,rho)` by

    (0,0), (91,0), (1078/13,1232/13).

The seven consecutive 13-edges have two possible inward supporting
triangles each. All `2^7=128` choices are generated, with no assumed
orientation for their c-edges. This avoids silently discarding the
pure-long row. The existing exact corner-fan engine then tests these
roots, adding the rounded-population necessary condition above.

The recorded run completed its attempt on all 128 roots in about
50.3 seconds, visiting 1,152 states with at most 61 placed tiles:

- 112 roots were exhausted by the search engine;
- 16 roots timed out and remain `INCOMPLETE`;
- the rounded-population test rejected no states in this run.

**The 112 search exhaustions have not been independently replayed and
are not advertised as certified mathematical exclusions.** All 16
unresolved patterns begin with the same three inward orientations.
This is a search observation, not a proved forced-patch theorem.
There was no tiling found, and absence of a found tiling is not an
impossibility result. The other three boundary-count rows were not
searched here.

Replay the exploratory computation with:

```sh
python research/i120-boundary-oct7/probe_pure_long_side.py --seconds 120 --per-root 3
```

Timeout-dependent node counts may vary. The saved report is
[pure-long-report.json](pure-long-report.json); the search code is
[probe_pure_long_side.py](probe_pure_long_side.py).

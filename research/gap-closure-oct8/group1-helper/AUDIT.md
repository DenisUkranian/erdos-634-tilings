# Independent mathematical audit: one-class whole-c boundaries

8 October 2026. Verdict: **PASS**, with the hypotheses stated below.

Audited source: [WHOLE_C_BOUNDARY.md](../structure/WHOLE_C_BOUNDARY.md),
SHA-256 `68cf937fee3f4d7078d38c1bc915d01006109bc50408a7cd589c82dedf746211`.
The audit is mathematical; no numerical enumeration or solver status is
used. An independently derived Laurent-character proof is in
[WHOLE_C_INDEPENDENT.md](WHOLE_C_INDEPENDENT.md).

## Universal theorem

For a primitive positive integral 120-degree tile `(a,b,c)`, an actual
nonempty tiled region whose complete oriented boundary consists of whole
`c`-steps in **one common direction class modulo 60 degrees** satisfies
`c^2 | N` and `N >= 2c^2`. When `ab` is even, it satisfies `2c^2 | N`.
Holes and nonconvexity are allowed; no restriction on interior heights is
needed. Merely requiring long boundary edges in several different height
classes would not meet the hypothesis.

Checks completed independently:

* Primitivity gives pairwise coprimality, odd `c`, and `3` not dividing `c`.
* Each boundary walk has area in `c^2 sqrt(3)/4` times the integers, hence
  `c^2 | N`, including oppositely oriented hole boundaries.
* The two reference triangles give exactly the scalar current in (6).
  Ordinary and alternating height sums give (8), with its displayed signs.
* The odd-`ab` and even-`ab` parity arguments both give `M=3ab*r`.
  The character bounds give `c(c+|a-b|)|r| <= N`; at `N=c^2`, parity makes
  `r` nonzero in the odd-`ab` case. This excludes the first positive area
  multiple. In the even-`ab` case both character sums are even.

## Separating-gap application

The stated application also passes. Its relevant hypotheses are a convex
original target, an empty short height `k`, and no exterior contact of the
upper tail at heights above `k` (the reflected statement holds below).

At an upper/lower interface only height `k` can be common. Because short
height `k` is empty, every edge there is a full long edge of length `c`.
To make the seam argument explicit, take a maximal straight connected
chain of edges at this height. At an interior endpoint, one side cannot
stop while a long edge on the other side continues: the tile occupying
the first side beyond that endpoint would cross the continuing edge and
overlap the tile on its opposite side. Thus both side partitions have the
same endpoints. At an exterior endpoint convexity prevents an interior
straight seam from becoming a one-sided continuation along the exterior
supporting line. The two partitions consequently start together and have
the same step length `c`; their vertices coincide. Every upper/lower
interface therefore consists of whole matching `c`-edges. Exterior
height-`k` contacts are whole boundary `c`-edges as stipulated in the source.

Each nonempty positive-length-contact component of the tail now meets the
universal theorem. If `ab` is even and the full tiling has `N<4c^2`, there
is exactly one such component and it has exactly `2c^2` tiles. A hole would
be filled by another tiled region with the same one-class whole-`c`
boundary, requiring at least `2c^2` additional tiles. This contradicts
the strict total bound. Contacts at isolated vertices do not affect the
area or this argument.

For canonical scale-one F3, the exterior heights are `0,2,3`; the
height-`0` and height-`3` sides have lengths divisible by `c`. Hence the
source correctly limits this application to upper gaps `k>=3` and lower
gaps `k<=0`; it does not silently cover gaps at `1,2`.

In particular, for `(56,9,61)` and `N=14430`, any such separated tail must
have exactly `7442` tiles and no hole. This is **not** an impossibility
proof for `14430`, a bound on an occupied consecutive height interval, or
a classification of Erdős 634. No additional extreme-population family
claim is covered by this audit.

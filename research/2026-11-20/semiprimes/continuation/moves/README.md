# Changing a packing at the boundary of the unit F2 triangle

The primitive tile has sides $a>b>0$ and $c^2=a^2+ab+b^2$. With $p=a+2b$ and $q=2a+b$, the board has sides $bq,ap,c^2$ and area $pq$ tile units. All the arguments below allow reflections and T-junctions. The parity or aspect-ratio hypotheses for each result appear in its proof.

## What can actually be rebuilt?

For odd $a,b$, place the center of a particular rhombus at the midpoint of the side of length $c^2$. Exchange the grid lengths $a$ and $b$ along its two directions. The new long diagonals lie on the outer boundary. The old packing in the clipped rhombus contains $ab-a$ whole tiles and its replacement contains $ab$. This applies to any surrounding packing disjoint from its interior. [Construction, picture and exact check](BOUNDARY_GAIN.md).

In a fully occupied interior patch, two neighboring exchange rhombi admit two successive changes of grid. The second move introduces another direction across their former interface. The strip fits at unit scale throughout the residual mixed prime-product family. For $3431$ and $5063$ the strip contains 1036 and 2236 tiles. [General two-stage construction](RHOMBUS_SWITCHES.md) · [Independent switches along a strip](RHOMBUS.md) · [Exact size limit and the forest of neighboring cells](FOREST.md).

## What does every complete tiling have to do?

A straight contact is imbalanced if its two banks have different counts of the three whole side lengths between successive common endpoints. In every complete tiling such imbalances survive summation in at least two nonparallel directions. With exactly two, one board side consists entirely of long edges and a second board side has exactly $c$ long edges and $a-b$ edges of length $b$. [Formal edge proof](TWO_DIRECTIONS.md) · [Rigidity when there are only two directions](TWO_AXES.md) · [Shortest integer side relations](BLOCK_SIZES.md).

Integer edge weights that sum to zero around every tile give unconditional lower bounds of **138** and **146** interior T-junctions on the two boards. The verifier permits all direction heights. [Proof and integer certificates](TILE_WEIGHTS.md) · [Independent Laurent-coefficient bounds](PERIODIC_CERTIFICATE.md).

At small replacement budgets a completely filled patch cannot gain a new short-side height. The threshold is $2c$ changed positions. At any sparsely populated nonzero short-side height, whole-board tiles must also share a Euclidean lattice. On the 3431 board this excludes individual placements from the 3427 packing and forces every complete tiling to omit at least thirty of its positions. [Small replacements](SMALL_SURGERIES.md) · [Geometric component counts](COMPONENTS.md) · [Lattice theorem](../phase-height/PHASE_BRANCHES.md) · [Application to 3431](../phase-height/3431.md).

These are constructive local moves and necessary conditions on complete tilings. The scale-one existence questions at $3431$ and $5063$ remain open in this record. The known packings of 3427 and 5059 use different choices of tiles from the boundary-gain examples.

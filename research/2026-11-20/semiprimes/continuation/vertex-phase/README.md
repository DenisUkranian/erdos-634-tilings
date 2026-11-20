# Vertex fans and phase populations for the 3431 and 5063 boards

20 November 2026. Denis Paliy research project, with ChatGPT assistance.

**Both target counts remain open.** This package proves additional necessary
conditions, implements them in the unrestricted endpoint search, and preserves
reproducible controls and restartable search states. It contains no positive
tiling certificate or unrestricted impossibility certificate for either target.

| Tile `(a,b,c)` | Target count | Target side lengths | Present status |
|---|---:|---|---|
| `(33,7,37)` | 3431 | 511, 1369, 1551 | OPEN |
| `(35,13,43)` | 5063 | 1079, 1849, 2135 | OPEN |

The common frame is `rho=exp(i*pi/3)`, `z=(a+b*rho)/c`, with board
vertices `0`, `b*(2*a+b)`, and `a*(a+2*b)*rho`. The short height of a
tile is the common exponent `h` in the directions of its `a` and `b`
edges. The search includes arbitrary translations, orientations, reflections,
and T-junctions. No finite height or denominator restriction is imposed by
the necessary conditions below.

## Mathematical additions

### Every required exterior-free phase node is occupied

The earlier phase-tree theorem gave at least `2c` tiles in any occupied
ordinary node but allowed one vacant exterior-free ancestor with occupied
descendants. The [new argument](NO_PHASE_GAPS.md) removes that exception on
the two target boards. An empty root would separate a positive-area union of
tiles from the exterior by complete `c` edges of one direction height. Its
boundary contains a simple supported cycle in a translated triangular mesh.
The restored [ordered-boundary proof](pure_cycles/NO_REMOTE_GAPS.md) excludes
every such cycle on either board, at any rotation or translation.

For any collection `F` of distinct exterior-free ancestors required by
selected placements, their exact-node populations are disjoint. The core
has at least `j=N mod c` tiles outside those nodes. Therefore

\[
 2c|F|+j\le N.
\]

The no-gap argument alone gives 46 nodes at 3431 and 58 nodes at 5063.
Every node is counted by its own short tiles, even when it is an ancestor
of another counted node. The bound applies in each conjugate prime tree;
the two trees' costs cannot simply be added. The signed parity argument
below sharpens the first limit to **45**.

### Positive and negative direction signs have separate populations

For the exact placement convention `(q,h,j,s)`, define `epsilon=s*(-1)^j`.
Both signs describe positive-area tiles; neither is a negative-area piece.
The [signed population argument](SIGNED_PHASE_POPULATIONS.md) proves that
each sign population in an ordinary phase node is separately divisible by
`c`. The exceptional core has fixed residues, and two direction characters
also fix the whole-board sign totals and their height parity.

| Count | Core residues `(+,-)` | Whole-board populations `(+,-)` | Remaining `c`-blocks `(+,-)` |
|---:|---|---|---|
| 3431 | `(19,8)` | `(1684,1747)` | `(45,47)` |
| 5063 | `(5,27)` | `(2499,2564)` | `(58,59)` |
| 143 control | `(4,6)` | `(67,76)` | `(9,10)` |

If the allocated positive and negative blocks at even and odd heights are
`Pe,Po,Qe,Qo`, the exact numerical completion conditions are

\[
 Pe+Po\le K_+,\quad Qe+Qo\le K_-,\quad
 Pe+Qo\le K_++1,\quad Qe+Po\le K_++\delta_e,
\]

where `delta_e=1` at 3431 and `0` at 5063. These inequalities allow missing
completion populations; they do not incorrectly demand full counts from an
incomplete catalogue. Common capacities for each physical height additionally
couple the two prime trees: each capacity dominates both trees' sums at that
height, and the global inequalities apply to those common capacities.

The signed difference at odd short heights is exactly `-c`. Consequently at
least one ordinary node has an odd number of `c`-blocks and hence at least
three blocks. If `R` is the total number of occupied ordinary nodes, then

\[
 N\ge r_++r_-+2cR+c.
\]

This gives **R<=45 at 3431** and **R<=58 at 5063**. The
[remote attachment lemma](REMOTE_BOUNDARY_BUDGET.md) additionally forces two
distinct occupied ordinary nodes outside any nonempty remote subtree rooted
at physical height at most zero in the increasing-height tree: one at a lower
height and one supplying a long edge
on the outer height-two side. Thus at most **43 and 56 required nodes**,
respectively, can lie inside one such subtree. At least 175 and 204 tiles
lie outside it. These sharper bounds have the stated remote-subtree
hypothesis. The conjugate tree has the corresponding result for a root at
physical height at least two, with descent toward smaller physical heights.

### A minimal terminal node contains both signs

An exterior-free node with exactly `2c` tiles and no occupied strict
descendant has exactly `c` tiles of each sign. The
[terminal-node proof](TERMINAL_NODE_BALANCE.md) first pairs long edges
facing the empty descendant side. A hypothetical one-sign node then has
only one hand; line-incidence congruences exclude its remaining `2c` tiles
for each target shape. The proof is elementary, with small exact arithmetic
checks. A finite catalogue cannot establish that a node is terminal, and
an auxiliary capacity of two blocks is not its actual population. The
search therefore does not infer this terminal property from catalogue
absence or its normalized capacities.

### Complete local corner fans

The [corner argument](CORNER_FANS.md) enumerates all admissible local
arrangements around a selected tile vertex. Its angle budgets are `(6,6)`
for a full turn, `(3,3)` for a half-turn, and the appropriate smaller pair
at each board corner, in coefficients of the tile's acute angles. Every
outgoing ray has exactly six possible rigid corner placements before
containment filtering.

The half-turn case permits a tile whose side passes through the vertex.
That tile's continuous translation parameter is checked by exact rational
interval inequalities. It is not restricted to the generated catalogue or
a prescribed lattice. Angular at-most-one conditions exclude overlapping
sectors in the generated local set. These conditions are necessary locally;
they do not assert nonoverlap or coverage everywhere on the board.

## Implementation and evidence

The solver extends the existing
[complete-row endpoint search](../global-endpoints/integer/README.md).
`phase_budget.py` computes canonical nodes by Hensel lifting at the two split
primes. `population_search.py` provides unsigned per-node capacities;
`signed_population_search.py` separates the signs, and `joint_height_search.py`
adds shared height capacities. `corner_search.py` combines these restrictions with
the local circuits in `corner_oracle.py`.

Capacity variables are existential witnesses for a possible completion.
Their optional bounds derived from the current catalogue are justified by
reducing auxiliary allocations while preserving all selected-tile demands.
They do not claim that the catalogue contains every tile in a physical node.
The current-pool bounds are query-scoped, grow with the catalogue, and are
reinstalled after a solver rebuild.

The internal independent audits cover the
[cycle and empty-root proof](audits/NO_PHASE_GAPS.md) and
[unsigned population encoding](audits/POPULATION_SEARCH.md),
[signed and shared-height encoding](audits/SIGNED_POPULATIONS.md),
and [terminal-node proof](audits/TERMINAL_NODE_BALANCE.md).
The [remote attachment audit](audits/REMOTE_ATTACHMENT.md) separately checks
the two outside populations and the resulting 43/56 count.
The independent arithmetic checker compares canonical phase equality with
explicit division in the Eisenstein ring, without Hensel digits: 79,800
comparisons pass. Known 143-tile controls retain the full positive tiling
through the corner and population encodings and equivalent-context rebuilds.
Separate rejection and scope checks exercise deliberately invalid capacities,
incomplete catalogue growth, and removal of old query bounds.

These are internal mathematical and implementation checks. They do not
constitute external refereeing or proof-assistant verification of the prose.

## Reproduction

From the repository root, with ordinary Python 3 and assertions enabled:

```sh
python3 research/2026-11-20/semiprimes/continuation/vertex-phase/replay.py
```

The default run needs only Python's standard library. It checks the rational
cycle geometry, population arithmetic, independent phase keys, and two
positive 143-tile block constructions. To include the Boolean solver controls,
install the shared library `libz3.so.4` and run:

```sh
python3 research/2026-11-20/semiprimes/continuation/vertex-phase/replay.py --solver
```

The [separate construction experiment](constructive-control/RESULT.md)
supplies a reusable C++ beam search, two verified 14-block decompositions of
the known 143 board, and an exact proof that their particular incidence
pattern cannot be transferred to the two targets. Its unsuccessful target
searches are not impossibility certificates. Its positive certificate
checker uses only the Python standard library; optional topology lifting
uses SymPy, NumPy and SciPy.

## Search status and resumption

The final [machine-readable status](SEARCH_STATUS.json) records saved states,
resource stops and any unguarded probes. The compact checkpoints preserve
complete endpoint row keys and installed corner roots; restarting regenerates
their entire incident placement catalogues. Large transient SMT contexts and
trusted-local pickle files are not required to resume.

| Board | Saved candidate placements | Complete endpoint rows | Outcome |
|---:|---:|---:|---|
| 3431 | 89,925 | 11,423 | Inconclusive signed continuation; round limit |
| 5063 | 97,822 | 12,672 | Inconclusive unsigned continuation; checkpointed stop |

The saved 3431 model includes one expansion after its last completed query.
The two separate unguarded probes used smaller boundary models with shared
height capacities; both returned `UNKNOWN` at the 45-second limit. A larger
proof-enabled 3431 model stopped at its memory threshold before reaching a
query. The cheap 45/58 cardinality refinement was added after these target
runs and is covered by the final controls; no new target outcome is claimed
for that final code change. All recorded target runs have ended.

[Exact restart commands](REPLAY_AND_RESTART.md) regenerate either saved
geometry model with the current signed and shared-height restrictions.

An UNSAT answer with temporary incomplete-row assumptions is a request to
expand the catalogue. A nonempty returned core can contain redundant
assumptions, so the search also supports direct checks without those
assumptions. An unguarded UNSAT would still require an encoding audit and an
independently checked proof before it could be presented as a global
nonexistence theorem. Bare SAT of the necessary projection is not a tiling;
only an exact independently checked positive coordinate certificate can
establish existence. Timeouts and resource stops decide neither alternative.

The authoritative status of both original target questions remains **OPEN**.

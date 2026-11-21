# Whole-edge closure with phase-node population allocations

This optional wrapper combines the unrestricted physical search with an
existing exact allocation constraint. It does not exclude 3431 or 5063.
It uses actual whole-tile variables, complete endpoint rows, complete
opposite banks, exact nonoverlap constraints, the signed global reserve,
and two separately bounded phase trees. No height range or odd population
is fixed.

`population_whole_edge_search.py` wraps `PhaseWholeEdgeSearch` using the
unchanged historical
[`make_population_search_class`](../../../../2026-11-20/semiprimes/continuation/vertex-phase/population_search.py).
The mathematical inputs and their scope are documented in
[`PHASE_BRANCHES.md`](../../../../2026-11-20/semiprimes/continuation/phase-height/PHASE_BRANCHES.md),
[`NO_PHASE_GAPS.md`](../../../../2026-11-20/semiprimes/continuation/vertex-phase/NO_PHASE_GAPS.md),
and the existing
[`population projection audit`](../../../../2026-11-20/semiprimes/continuation/vertex-phase/audits/POPULATION_SEARCH.md).

## What the additional bound does

Let `c` be the hypotenuse, `j=N mod c`, and `K=(N-j)/c`.
Within one valuation tree, distinct nodes count disjoint populations of
tiles having those exact short nodes. The core population has the form
`j+c*k_core`. Every ordinary occupied node has population `c*k_v` with
`k_v >= 2`. An empty ordinary node has `k_v=0`.

For each currently generated node, the Boolean model introduces binary
bits for a nonnegative integer auxiliary allocation `k_v`. It imposes:

- `m_core <= j+c*k_core`, where `m_core` counts selected generated tiles;
- `m_v <= c*k_v` at ordinary nodes, together with `k_v != 1`;
- positive allocation at a selected tile's ordinary own node;
- positive allocation at each required exterior-free ancestor, except
  for the historically permitted empty-node exception on the 143 control;
- `sum_v k_v <= K` separately in each of the two valuation trees.

The target-specific absence of an empty required ancestor is enabled
automatically only for `(33,7,37)` and `(35,13,43)`. The 143 control uses
the older allowance of at most one such empty node per tree. The two
trees are alternative partitions of the same tiles: their population
costs are never added together.

The inherited ordinary-node cardinality bound remains available. The
new allocation bound is stronger than separate limits on the selected
tile count and the number of occupied nodes. For example, in the 3431
arithmetic, 3000 selected core tiles require at least
`ceil((3000-27)/37)=81` blocks. Forty-four additional occupied ordinary
nodes require at least 88 further blocks. Their total, 169, exceeds
`K=92`, even though the separate inequalities `3000<=3431` and `44<=45`
would both hold. This is a numerical illustration of the coupling, not
an assertion that such a geometric configuration exists.

| Board | `c` | Core residue `j` | Available blocks `K` | Bits per node |
| --- | ---: | ---: | ---: | ---: |
| 143 | 7 | 3 | 20 | 5 |
| 3431 | 37 | 27 | 92 | 7 |
| 5063 | 43 | 32 | 117 | 7 |

## Finite pools, query scope, and proof export

The allocations are auxiliary lower capacities, not claims that a
node's full actual population has already been generated. For a
physical tiling and any finite generated pool, restrict the tiling to
that pool. One can reduce each allocation to the least value that
accommodates the selected known tiles and any ancestor demand. This
preserves every condition above and only reduces the sum of allocations.

Consequently the historical factory also limits an ordinary allocation
by `max(2,ceil(M_v/c))` and the core allocation by
`ceil(max(0,M_core-j)/c)`, capped at `K`, where `M` counts all generated
candidates at the node. These are existential normalizations of the
current auxiliary model. They are not upper bounds on actual unseen
tile populations. They can increase when the candidate pool grows and
must be removed on every query pop.

The wrapper therefore makes two deliberate changes to the factory's
integration:

1. `query_bounds()` explicitly conjoins every
   `population_query_clauses()` term with the inherited total, charge,
   and ordinary-node bounds. The exported `query_count_bound` contains
   the complete query.
2. `flush()` calls the physical base directly, bypassing the historical
   population flush hook. No second copy of population caps is silently
   injected, and none is added to `permanent_assertions`.

Permanent statements are the node-bit implications and tile-to-node
requirements. Current-pool upper normalizations, own-population
capacities, and global block/exception caps are query statements. A
rebuild redeclares all allocation variables and restores permanent
statements; the next query regenerates its current bounds.

The necessary-model snapshot includes `phase_population_allocation`
with both signed trees, exact node keys, bit names, own tile indices,
ancestor flags and empty-node excuses, each permanent source clause,
and all query source clauses. It also records residue, block cap, bit
width, and whether the strict target theorem is enabled. The exported
positive-weight `pble` syntax is supported by the independent
[`Boolean proof encoder`](../audit/proof_cnf.py).
Geometric-source validation and an independently checked UNSAT proof
are still necessary before a target exclusion can be claimed.

A `--model-checkpoint` restart regenerates geometric obligations and
their actual placements through the new wrapper. Population nodes,
declarations, implications, and current bounds are reconstructed from
these placements. Arbitrary prior assertion strings are not imported.
The caller must supply any desired root file and root ID again; the
root-branch scope is preserved in the status report.

## Running the optional wrapper

The command-line interface is identical to the whole-edge driver's:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/population/population_whole_edge_search.py \
  33 7 37 --out /tmp/3431-population --no-grid \
  --edge-tiles-per-round 8 --vertex-fans-per-round 0 \
  --expand 100 --owner-rows-per-round 150 --rounds 100 \
  --timeout-ms 45000 --time-limit 600
```

This example is a bounded exploratory run. A timeout, resource limit,
or satisfiable partial projection does not exclude the board. Root
assumptions restrict an exclusion to the recorded branch; full closure
requires the unrestricted model or a verified cover of all root cases.

## Controls

The default verifier requires only the Python standard library:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/population/verify_population_wrapper.py
```

It checks the exact metric, area, boundary current and nonoverlap of the
same established 143-tile construction used elsewhere in this package.
Each of its two phase trees has populations 38 and 105, requiring 5 and
15 blocks, respectively. It also checks 376 projected subsets and 2772
integer identities for the positive-weight capacity formula.

Optional integrated controls require the existing native solver:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/population/verify_population_wrapper.py \
  --with-solver --workdir /tmp/population143-control
```

They select the actual 143 whole triangles, complete all their endpoint
rows and opposite banks, and fix allocation bits to the actual 5/15
block values. The control must remain SAT after an equivalent rebuild
and after regeneration from a geometric checkpoint. Allocating only 14
blocks to the 105-tile ordinary node must be UNSAT. A query on an earlier
small pool is popped before this larger model is built, testing that
obsolete caps do not persist. The command journal is inspected to
ensure weighted bounds occur only in live query scopes and that the
historical flush hook does not inject duplicate assertions.

`POPULATION_CONTROL_REPLAY.json` records the local integrated replay.
All these are controls of one actual 143 tiling and the surrounding
encoding. They do not constitute a second independent construction or
a nonexistence certificate for either target.

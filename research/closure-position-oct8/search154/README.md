# Strengthened exact search for the 154 candidate

8 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
The code searches the `(91,91,154)` target with congruent `(8,7,13)`
tiles. A resource-limited run is **INCOMPLETE**, never a negative theorem.

This version preserves the exact geometry and corner-fan enumeration of
[`closure-position-oct7/search154`](../../closure-position-oct7/search154/README.md).
It changes only the necessary population/completion bounds:

* every complete occupied support is an interval containing zero of
  length 3, 4, or 5 (twelve intervals altogether);
* the central population is at least 24;
* every occupied nonzero-height population is at least 26.

The central bound is proved in
[`CENTRAL_HEIGHT.md`](../central/CENTRAL_HEIGHT.md). The nonzero-height
bound is proved in
[`NO_THIRTEEN_HEIGHT.md`](../../closure-position-oct7/oct8-structural/NO_THIRTEEN_HEIGHT.md),
and the complete direction-inventory reduction is retained in the same
structural package. No unproved layer-inventory or geometric filtering
rule is used.

`inventory_completion.hpp` checks **all complete-support extensions** of
the partial height hull. At every height it combines the already placed
signed groups with the new population floor, then enforces residue modulo
13 and parity. The existing Laurent recurrence and boundary conditions
are unchanged. The geometric engine also uses the weaker cheap necessary
population bound over the partial interval before the full completion DP.

The new header received a separate internal review by the layer-geometry
audit agent. `check_inventory_completion.py` compares it with direct
population enumeration in Python: 24 cases pass, including the five
full five-height formal inventories, their partial subsets, and negative
controls. A positive formal inventory is not a geometric tiling.

The recorded search continues the previous local checkpoint with 213,883
closed states. Its three source-file hashes were checked against the
published old `checkpoint-digests.json` before loading. Those states were
excluded under weaker necessary conditions and remain safely excluded.
Interrupted states and their unresolved ancestors are not in the dead
set and are revisited. The strengthened implementation's own continuation
test reproduces a continuous 4,000-node trace exactly across a 1,000-node
checkpoint: 3,971 completed-state records agree.

`run600-report.json` records the completed bounded run: **INCOMPLETE**,
96,272 new state visits, 310,109 cumulative closed states, 507,489 generated
tile placements, and largest encountered partial placement of 121 tiles.
There is neither a positive tiling nor complete exhaustion. The size of
that partial placement is not a measure of closeness to a valid tiling.
The raw checkpoint files remain available locally; their exact sizes and
SHA-256 hashes are recorded in `checkpoint-digests.json`. No search is
left running.

`candidate-check.json` independently checks the generated geometry and
every triangle's height/signed-group metadata, and compares 600 candidate
queries with a rational six-side-permutation generator. The geometric
code is unchanged from the earlier separately checked engine; the new
checks do not substitute for a complete exhaustion certificate.

## Commands

From the repository root:

```sh
mkdir -p /tmp/erdos634-search154-strong
python research/closure-position-oct8/search154/check_inventory_completion.py
g++ -std=c++17 -O3 -Wall -Wextra research/closure-position-oct8/search154/fixed_search.cpp -o /tmp/erdos634-search154-strong/search
g++ -std=c++17 -O3 -Wall -Wextra research/closure-position-oct8/search154/resume_search.cpp -o /tmp/erdos634-search154-strong/resume
python research/closure-position-oct7/search154/check_resume.py /tmp/erdos634-search154-strong/search /tmp/erdos634-search154-strong/resume /tmp/erdos634-search154-strong/check-resume --output /tmp/erdos634-search154-strong/resume-check.json
/tmp/erdos634-search154-strong/search 600 100000000 /tmp/erdos634-search154-strong/fresh
g++ -std=c++17 -O2 research/closure-position-oct8/search154/candidate_query.cpp -o /tmp/erdos634-search154-strong/candidates
python research/closure-position-oct7/search154/check_fixed_search.py /tmp/erdos634-search154-strong/fresh-geometry.txt /tmp/erdos634-search154-strong/candidates --output /tmp/erdos634-search154-strong/candidate-check.json
```

For an existing trusted checkpoint, use its prefix as the first argument
of `resume`; the output prefix must differ:

```sh
/tmp/erdos634-search154-strong/resume /path/to/prior-prefix 600 /tmp/erdos634-search154-strong/continued
```

The old and new checkpoint formats are compatible. Raw checkpoint data
are operational state, not independently replayed negative certificates.
If the search exhausts, it still reports
`EXHAUSTED_REQUIRES_INDEPENDENT_REPLAY` and does not mark 154 as decided.
Any candidate positive tiling likewise requires separate exact geometric
verification. No resource limit counts as an exclusion.

## A further bound, not enabled in the recorded search

[`POSITIONAL_RESIDUE_BOUND.md`](POSITIONAL_RESIDUE_BOUND.md) proves a
lower bound on the number of future tiles by retaining each concrete
supporting line and its residual short-edge current modulo 13. It was
reviewed separately and checked on all sixteen subsets of a four-tile
grid and 1,178 partial subsets of the attributed Harries 88-tiling. The
standalone checker is `check_line_residue_bound.py`. This additional bound
is not silently attributed to the recorded search binary.

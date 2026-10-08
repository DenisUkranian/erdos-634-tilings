# Exact geometric search for the 154 candidate

8 October 2026. **Status: INCOMPLETE. No conclusion about existence or
nonexistence of a 154 tiling is obtained here.**

The fixed target is `(0,0),(154,0),(49,56)` in Eisenstein coordinates,
and the congruent tile has sides `(8,7,13)`. The search starts from the
empty target and branches over every admissible fan at a chosen convex
corner of the uncovered region. Reflections are included. It is a C++
port of the exact rational frontier search, with integer arithmetic and
additional proved necessary inventory conditions.

The fixed denominator is `D=13^11`; coordinates are 64-bit integers and
determinants, norms and products of normalized directions use signed
128-bit integers. This denominator covers the proved direction range.
Templates are generated for heights -11 through 11, a superset of the
permitted exact supports. Partial placements are rejected only if they
cannot extend to **any** interval containing zero of length 3 through 8.
The completion filter is documented in `../dual/inventory_completion.hpp`
and separately checked by `../dual/check_inventory_completion.py`.

`run600-report.json` records an unrestricted-root 600-second run:
103,897 visited states, 302,684 generated tile placements, and maximum
partial size 122. It reached its resource limit; that maximum size is
not evidence of a nearly complete tiling. The search remains unfinished.

After a 30-second checkpoint smoke run, a further 600 seconds were run
from the saved closed states. `continued600-report.json` records 104,700
additional visits, 213,883 cumulative closed states, 407,857 generated
placements, and maximum partial size 125. Its status is also
**INCOMPLETE**. Across the three sequential runs there were 214,038
visits, including repeated unresolved ancestors. No search is left running.

These runs used the previously proved 3--8-height filter. The later
[all-nonzero-height obstruction](../oct8-structural/NO_THIRTEEN_HEIGHT.md)
and its strengthened 3--5-height consequence were not incorporated into
the recorded binaries. Their absence weakens pruning but does not make
the older necessary conditions invalid. No new filter is silently
attributed to these reports.

## Reproduce the search and geometric checks

From the repository root, choose a temporary directory outside the source
tree for the large trace and geometry files. For example:

```sh
mkdir -p /tmp/erdos634-search154
g++ -std=c++17 -O3 -Wall -Wextra research/closure-position-oct7/search154/fixed_search.cpp -o /tmp/erdos634-search154/search
/tmp/erdos634-search154/search 600 100000000 /tmp/erdos634-search154/run
g++ -std=c++17 -O2 research/closure-position-oct7/search154/candidate_query.cpp -o /tmp/erdos634-search154/candidates
python research/closure-position-oct7/search154/check_fixed_search.py /tmp/erdos634-search154/run-geometry.txt /tmp/erdos634-search154/candidates --output /tmp/erdos634-search154/candidate-check.json
g++ -std=c++17 -O2 research/closure-position-oct7/search154/primitive_query.cpp -o /tmp/erdos634-search154/primitives
python research/closure-position-oct7/search154/check_primitives.py /tmp/erdos634-search154/run-geometry.txt /tmp/erdos634-search154/primitives --output /tmp/erdos634-search154/primitive-check.json
```

Node totals at a time limit depend on machine speed. Replacing the node
cap `100000000` by a smaller fixed integer gives a deterministic prefix
provided the time limit is not hit first.

`candidate-check.json` verifies every one of the 302,684 generated
triangles from the recorded run: exact three side lengths, positive area,
containment, and every triangle's height and signed-group metadata used
by the pruning filter. Six hundred deterministic candidate queries are compared
with an independent rational six-side-permutation implementation, including
height and signed group classification.

`primitive-check.json` compares 303 fan queries (7,221 alternatives)
with a rational implementation using independently enumerated alpha/beta
angle quotas. It also checks 1,708 pairwise compatibility queries, including
integral and nonintegral partial edge contacts. A positive triangular grid
of four tiles has six compatible pairs and exactly zero residual boundary.
The stored primitive report uses the earlier 29,367-triangle smoke-run
geometry; the command above repeats the same checks on fresh geometry.
These checks verify the indicated implementations, not exhaustion of the
search tree.

## Continue a trusted local checkpoint

Each completed run writes geometry, a dead-state trace, and a JSON report.
Only completely rejected states are recorded. A resource-limit exception
propagates without recording the interrupted node or its unresolved
ancestors. The continuation program restores the exact point/triangle
identifiers and begins again at the empty root, skipping only stored
closed states. Previously unfinished ancestors are explored again.

```sh
g++ -std=c++17 -O3 -Wall -Wextra research/closure-position-oct7/search154/resume_search.cpp -o /tmp/erdos634-search154/resume
python research/closure-position-oct7/search154/check_resume.py /tmp/erdos634-search154/search /tmp/erdos634-search154/resume /tmp/erdos634-search154/check-resume --output /tmp/erdos634-search154/resume-check.json
/tmp/erdos634-search154/resume /tmp/erdos634-search154/run 600 /tmp/erdos634-search154/continued
```

The output prefix must differ from the input prefix. The continuation
trace includes the previous trace, so its checkpoint is self-contained.
`check_resume.py` compares a continuous 4,000-node run with a 1,000-node
checkpoint followed by 4,000 additional visits. It requires the entire
continuous dead-state trace to be an identical prefix of the continued
trace. This tests deterministic continuation across an interrupted branch.
The stored `resume-check.json` reports that all 3,964 closed-state records
of the continuous run matched exactly. `checkpoint-digests.json` records
the SHA-256 digests and byte sizes of the last local checkpoint files;
the approximately 104 MB of raw operational checkpoint data are not
included in the repository. The supplied commands regenerate checkpoints.

Checkpoint files are **trusted operational state**, not independently
replayed mathematical certificates. If the search ever exhausts, it
reports `EXHAUSTED_REQUIRES_INDEPENDENT_REPLAY`, and `N154_decided` remains
false. A separate complete replay would be required before publishing a
negative geometric theorem. A reported placement likewise needs an
independent tiling verification. `INCOMPLETE` is never an exclusion.

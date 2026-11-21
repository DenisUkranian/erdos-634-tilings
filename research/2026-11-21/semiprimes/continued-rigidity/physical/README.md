# Physical searches with proved phase and population restrictions

21 November 2026. **Neither 3431 nor 5063 is excluded.** These runs
continue the whole rigid-placement model within the two separately proved
minimal remaining odd-population regimes. All recorded target runs end at
a resource limit or an inconclusive solver status.

## Necessary restrictions, without a guessed geometric cutoff

`scoped_physical_search.py` uses the existing complete incident-placement
oracle. A completed physical endpoint/direction row contains every actual
contained placement admitted by the independently proved scope. Each
variable chooses one whole triangle; all partial contacts remain allowed.

| Conditional mode | Complete short-height support | Standard-frame odd signs | Standard-frame even signs |
|---|---|---|---|
| 3431, odd population 111 | `{0,1,2}` | `(37,74)` | `(1647,1673)` |
| 5063, odd population 215 | `{0,1,2}` | `(86,129)` | `(2413,2435)` |

The sign pairs are `(positive,negative)`. They are upper bounds on a
partial selected population, not equalities incorrectly imposed before
all placements have been generated. The three-height restrictions must
not be used for the larger odd populations, which remain open.

At 3431 the standard-frame phase envelopes are `R+zR` at height zero,
`A+zR` at height one, and `A+zR+z^2R` at height two. At 5063 every vertex
lies in the proved ideal `(z/c)R`. With `--cell-reserve`, a single shared
phase choice selects the one-, two-, or four-cell skeleton, and one
shared binary integer supplies the four-cell parameter. The runs retain
the original complete parameter interval `1<=x<=42`; the later small-cell
exclusions are not retroactively attributed to them.

The [independent encoding audit](../cells5063/SCOPED_SEARCH_AUDIT.md)
checks the coordinate transformations, sign reversal, nine pairs of
phase types, partial population caps, and preservation of these
constraints during solver rebuilds.

## Recorded runs

| Search | Generated placements | Completed physical rows | Recorded result |
|---|---:|---:|---|
| 3431/111, guarded continuation | 122276 | 17506 | 80-round limit |
| 5063/215, guarded continuation | 200180 | 18326 | Column resource limit |
| 5063/215, with shared cell caps | 231707 | 21726 | Column resource limit |
| 3431/111, permanent rows only | 80999 | 11506 | 25-round limit |
| 5063/215, permanent rows and shared cell caps | 91619 | 6126 | Solver inconclusive after a 25-second check |

These are candidate and row counts, not numbers of possible tilings
exhaustively tested. The guarded method uses explicitly temporary
equations on unfinished rows to guide expansion. Its conflicts are
not global certificates. The final 5063 cell-cap model was also checked
without temporary row assumptions and returned `unknown` after 45
seconds. In particular no final unguarded contradiction was obtained.

The separate `permanent_physical_search.py` uses only completed rows.
At each integer partial selection it adds exact incompatibility clauses
for overlapping triangle interiors and completes actual residual rows.
All calculations use exact axial integer coordinates with the proved
height-dependent denominator. A satisfying partial selection can still
have unbalanced unselected rows and is not a tiling. Even a numerical
or solver-reported infeasibility would require an independent certificate
audit before becoming a theorem.

The permanent-row run for 3431 obtained partial selections, but none
closed all physical rows. Its final recorded selection had 1395 tiles,
4079 residual rows, and 3088 overlapping pairs before those conflicts
were added. This is an exploratory intermediate state, not an admissible
packing or a positive certificate.

## Positive control and preservation

The guarded search found a complete 143-tile control. The independent
polygon verifier reconstructs all rational vertices and proves its exact
metric, containment, area, and full oriented boundary current. It has
38 tiles at short height zero and 105 at height one. The independent
full-current identity certifies both coverage and nonoverlap.

`verify_physical_controls.py` replays this positive certificate, checks
that the scoped geometry and exact overlap code accept it, and audits
the format and scope of the saved target reports. It does not rerun the
large target searches or verify any negative target certificate.

The `checkpoints` directory contains deterministic compressed JSON row
and point snapshots, plus the original run statuses. The executable
pickle files and large solver journals are not required to read these
artifacts. Restarting from rows recomputes all incident placements; a
permanent-row snapshot does not preserve previously discovered overlap
clauses, which can be derived again. The status files are historical
measurements and need not be reproduced byte for byte.

From the repository root:

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/physical/verify_physical_controls.py
```

An optional continuation, requiring the system Z3 shared library, is:

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/physical/scoped_physical_search.py \
  --mode 5063-215 --cell-reserve \
  --rows research/2026-11-21/semiprimes/continued-rigidity/physical/checkpoints/run5063-cells/complete_rows.json.gz \
  --point-checkpoint research/2026-11-21/semiprimes/continued-rigidity/physical/checkpoints/run5063-cells/coverage_points.json.gz \
  --out /tmp/erdos634-5063-scoped --rounds 50 --max-columns 350000
```

No duration or resource setting is interpreted as mathematical coverage
of the remaining 3431 or 5063 cases.

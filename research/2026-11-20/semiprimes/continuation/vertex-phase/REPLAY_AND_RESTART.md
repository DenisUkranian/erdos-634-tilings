# Replay and restart instructions

These commands assume the package is installed as
`research/2026-11-20/semiprimes/continuation/vertex-phase/` in the existing
repository. Run them from that directory. Python 3 and the same installed
`libz3.so.4` as the original integer search are required. `phase_budget.py`
belongs beside the solver extensions.

## Short exact controls

```sh
python3 verify_corners.py ../global-endpoints/integer
python3 verify_populations.py ../global-endpoints/integer .
python3 verify_signed_solver.py ../global-endpoints/integer .
python3 verify_signed_solver.py ../global-endpoints/integer . --joint-heights
```

These replay the exact 143-tiling, local corner and through-edge controls,
unsigned/signed node populations, equivalent solver-context rebuilds, and
the arithmetic parity-completion test. The controls do not decide a target
board. Strict no-empty-ancestor mode is scoped to the two audited targets,
not assumed in the 143 control.

## Continue either saved endpoint model

Use the matching portable row and corner files from the package's checkpoint
directories. They regenerate finite permanent endpoint equations and local
corner circuits. They do not freeze any seed tile or any saved assignment.

```sh
python3 corner_search.py 33 7 37 \
  --base-dir ../global-endpoints/integer --phase-dir . \
  --signed-populations --joint-heights --no-phase-empty \
  --rows checkpoints/3431/complete_rows.json.gz \
  --corner-checkpoint checkpoints/3431/corners.json \
  --out resumed3431 --core-policy few_missing --expand 80 --corner-rows 1 \
  --angular-cliques --rebuild-every 0 --timeout-ms 45000 \
  --max-columns 150000 --max-rss-mb 1800 --rounds 100 \
  --checkpoint-every-query --stop-file STOP3431

python3 corner_search.py 35 13 43 \
  --base-dir ../global-endpoints/integer --phase-dir . \
  --signed-populations --joint-heights --no-phase-empty \
  --rows checkpoints/5063/complete_rows.json.gz \
  --corner-checkpoint checkpoints/5063/corners.json \
  --out resumed5063 --core-policy few_missing --expand 80 --corner-rows 1 \
  --angular-cliques --rebuild-every 0 --timeout-ms 45000 \
  --max-columns 150000 --max-rss-mb 1800 --rounds 100 \
  --checkpoint-every-query --stop-file STOP5063
```

The RSS limit is a graceful checkpoint trigger checked between operations.
It is not a hard operating-system memory limit and cannot guarantee survival
of a single large native solver allocation. A pre-query checkpoint minimizes
lost permanent rows after such an interruption. When the initial model already
exceeds the requested memory budget it may stop before any query; report that
as a resource stop, not as a solver answer. The recorded larger continuations
needed up to approximately 2 GB, and proof-enabled probes can require more.

## Unguarded probes

For an explicit check of the permanent necessary model without temporary
endpoint assumptions, add

```sh
--global-probe-every 10 --global-probe-timeout-ms 45000
```

The probe keeps the current tile-count, population, and joint-height query
caps active but supplies no temporary-row assumptions. It records its exact
scope and outcome in `global_probes.json`. A SAT answer is only a finite
necessary-model assignment, not a tiling. An UNKNOWN or timeout is inconclusive.
For an initial probe, omitting `--proof` avoids the potentially substantial
cost of retaining proof data. If an unguarded UNSAT is found, rerun the exact
saved model with proof production enabled and audit the proof and encoding.
When `--proof` is supplied from the start, the code obtains the proof before
another solver query or scope change, then saves the model and marks it as
requiring that independent audit. An UNSAT response without its proof remains
a candidate for verification.

The existing negative cores obtained under temporary assumptions remain
conditional even when this stronger mathematics is enabled. They cannot be
published as a nonexistence proof.

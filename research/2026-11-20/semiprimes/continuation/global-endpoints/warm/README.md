# Focused 5063 warm-start continuation

Research record, 20 November 2026. This numerical continuation does not decide whether the 5063 board is tileable.

## Recorded stopping state

The focused run stopped during iteration 254 because the primary numerical LP reached its 120-second limit. The process exited normally after saving the checkpoint; no mathematical result was produced.

The saved checkpoint is marked iteration 253 and contains **60,066 endpoint rows, 94,313 real columns, and 144 exact point cuts**. It includes the 3,000 new columns added after the last successfully optimized LP. That last LP, at iteration 253 with 91,313 columns, had phase-I objective approximately **0.04435204435204454**, entirely endpoint artificial residual; its negative-tile mass was zero. The global pricing oracle examined 567,243 omitted incident placements and found 299,017 with positive reduced score. Thus this positive finite-pool objective was explicitly not a nonexistence certificate.

The last full-primal check occurred at iteration 252. It had total positive mass approximately 5063, retained seed mass approximately 3038.8333333333, and **7,879 nonzero endpoint residuals on rows not yet installed**. The next 1,000 of those rows were installed. This was not a complete boundary cancellation and was not an ordinary tiling.

| Iteration | Endpoint rows | Real columns | Point cuts | Primary basis | Primary seconds | Primary result |
|---:|---:|---:|---:|---|---:|---|
| 250 | 57,066 | 91,313 | 72 | Cold | 71.46 | Phase I = 0 |
| 251 | 58,066 | 91,313 | 96 | Reused | 20.56 | Phase I = 0 |
| 252 | 59,066 | 91,313 | 120 | Reused | 3.21 | Phase I = 0 |
| 253 | 60,066 | 91,313 | 144 | Reused | 58.28 | Phase I ≈ 0.04435204435 |
| 254 | 60,066 | 94,313 | 144 | Reused | 120.07 | Time limit; no optimal value reported |

These are observed times on evolving LPs, not a controlled speed benchmark. They demonstrate successful basis transfer, including after new endpoint rows and point cuts. The last column-addition step still exhausted its time limit.

The exact checkpoint SHA-256 is `a1f85e338d012b929086b34f7489e5b92c78b6d8d18659b2562c152a2a101804`. The extension folder also contains `checkpoint_5063.pickle.gz`, `warm5063.log`, and a machine-readable `run_summary.json`. Decompress the checkpoint before resuming. Loading a new process starts with a cold numerical basis, while preserving the full saved mathematical search state.

## Reproducible implementation

`warm_solver.py` is the frozen point-cut solver with the three numerical LP calls replaced by `warm_lp.WarmLP.solve`. The geometric templates, admissibility conditions, endpoint oracle, point inequalities and exact certificate stopping rules are unchanged. Put `warm_solver.py` and `warm_lp.py` beside the files in the portable package to run them without workspace-specific imports.

The wrapper accesses the HiGHS bindings bundled with SciPy at `scipy.optimize._highspy._core`. This private API was tested with SciPy 1.17.0. It reconstructs the current numerical LP and transfers the preceding basis by persistent column and row identifiers. New real columns start at their lower bound; new rows start basic. Endpoint artificial columns retain their identities when more real columns are inserted. Separate bases are retained for the primary LP, the exact-area secondary LP, and its inequality-budget fallback. Bases remain in process memory; the ordinary checkpoint stores the mathematical search state, so the first solve after a restart is cold.

The 143 positive control completed and its output passed the separate exact positive-tiling checker. A small two-step LP also checked remapping when a real column is inserted before the endpoint artificial columns. These checks validate the numerical plumbing; only the independent exact certificate checkers can establish a mathematical target result.

The recorded focused command, run in the existing 5063 checkpoint directory, was:

```sh
PYTHONPATH=../lp SEED_JSON=../lp/seed_5063.json \
RESUME=checkpoint_5063.pickle LP_LIMIT=120 \
CUTS_PER_ITER=24 MAX_POINT_CUTS=480 GROW=1000 BATCH=3000 \
SPARSE_DUAL=0 ITERATIONS=256 \
python3 ../warm_solver.py 35 13 43 > warm5063.log 2>&1
```

It began from saved iteration 249: 57,066 endpoint rows, 91,313 real columns and 72 point cuts. The last iteration allowed by this command is 255.

To resume the supplied extension as a sibling directory of `lp`, run the following from the extension directory. This resumes from the saved state and is not a replay of the already completed iterations.

```sh
gzip -dk checkpoint_5063.pickle.gz
PYTHONPATH=../lp SEED_JSON=../lp/seed_5063.json \
RESUME=checkpoint_5063.pickle LP_LIMIT=120 \
CUTS_PER_ITER=24 MAX_POINT_CUTS=480 GROW=1000 BATCH=3000 \
SPARSE_DUAL=0 ITERATIONS=256 \
python3 warm_solver.py 35 13 43 > resumed5063.log 2>&1
```

## Concrete next search change

The current search prices new placements only against the primary phase-I objective. At phase I = 0, the secondary LP maximizes retained seed placements over the existing columns, then adds missing endpoint rows and overlap cuts. This can reduce retained seed mass sharply even though undiscovered columns could preserve more of the seed.

A subsequent experiment should price against the secondary retention objective before adding further rows. For this pricing LP, use the inequality budget `sum(x)<=N`, set negative and artificial variables to zero, keep all installed endpoint equalities and coverage inequalities, and give cost −1 to positive seed placements and 0 to other placements. Its budget and coverage dual multipliers are nonpositive. Every omitted placement with positive reduced score is therefore incident to a supported endpoint row, because all seed placements are already present. The same finite global oracle can enumerate the improving columns. Add these columns, reoptimize retention, and only then continue row generation. The exact-area secondary solve may still select the displayed primal after this pricing stage.

This proposed step was not implemented or run in the focused continuation. A retention value over an incompletely priced finite pool is not a global bound and is not a nonexistence proof.

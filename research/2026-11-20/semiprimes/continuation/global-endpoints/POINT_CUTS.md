# Point-coverage cuts for the global endpoint LP

20 November 2026. This is a search implementation, not a tiling or a
nonexistence certificate for either outstanding board.

`global_endpoint_pointcuts.py` is a separate extension of the stabilized
endpoint engine. It imports exact geometry from `point_coverage.py`.
For each selected rational point P it adds

    sum_T x_T 1[P strictly inside T] <= 1.

Positive columns have coefficient +1 when they contain P strictly;
negative tile columns have coefficient -1. Endpoint-row artificial
variables have coefficient zero. Thus the original signed decomposition
remains feasible for the points admitted by the separator. The separator
checks that property exactly before installing a point.

Every true tiling satisfies the inequality, including at T-junctions:
strict interiors of different tiles are disjoint, and points on edges
have contribution zero from those tiles.

## Exact geometry and complete global pricing

Tile vertices use the existing c-power coordinates. Cut points have
arbitrary exact rational coordinates, so centroids and pair-intersection
points introduce no denominator restriction. Three integer determinant
inequalities decide strict membership. The cut matrix is rebuilt exactly
for all current columns when a new point is installed; every subsequent
column receives all applicable cut coefficients. Exact incremental masks
are reused for pricing.

Spatial bins and finite centroid/pair budgets are used only to discover
promising violated points. They never decide a matrix coefficient or a
global reduced cost. The separator tests centroids of selected positive
tiles and centroids of exact convex intersections of selected pairs, then
evaluates signed coverage at each selected point. It retains only points
whose coverage exceeds one numerically and whose initial signed seed has
coverage at most one exactly. Choosing an unhelpful point is harmless:
the inequality is necessary for every true tiling regardless of its
current numerical violation.

All point-row duals are nonpositive. A newly priced positive column has
score equal to its endpoint score, plus the nonpositive budget dual,
plus the point duals for points in its strict interior. Therefore a tile
incident to no nonzero endpoint row has nonpositive reduced score. The
same finite 24-placement oracle at each supported endpoint row remains
globally complete, with arbitrary orientations and translations.

The exact certificate exporter writes the independent verifier's schema:
endpoint weights are sign-converted, point penalties are nonnegative,
and `boundary_arithmetic` is explicit. For point penalties lambda_i,
the adjusted boundary lower bound is B-sum(lambda_i), and a tile's
adjusted score is endpointscore-sum(lambda_i inside that tile). The
strong top-N positive-score test is applied. Any reported candidate
still requires the separate exact verifier before a mathematical claim.

## Stabilization and constructive steering

The primary LP uses positive variables in [0,1], unbounded nonnegative
negative-tile variables, and signed mass at most N. Each endpoint row
also has positive and negative artificial columns of cost one, with zero
budget and point coefficients. This prevents unbounded endpoint dual
values. A phase-I value of zero means that both negative and artificial
mass vanish in that restricted master; it is not a full tiling by itself.

At phase-I zero, the secondary steering LP first tries to impose positive
mass exactly N while retaining as much of the original positive seed as
possible. If that optional heuristic is infeasible or times out, it falls
back to mass at most N. The primary global LP remains unchanged. The
secondary equality is never used as a global nonexistence condition.

New violated point cuts are installed before generating more endpoint
rows. When no tested point is violated, the existing full endpoint-row
separation proceeds. A finite tested set of points does not certify
global non-overlap.

## Controls and use

Run `python3 check_point_coverage.py` for 648 exact point-membership
checks against independently prescribed barycentric inequalities, plus
overlap clipping, negative-column cancellation and mask checks.

The known 143 construction was also replayed with no cuts and with a
preinstalled nonempty cut. Both runs preserved all 143 tiles, phase-I
zero, exact mass 143, and no false point violation. Logs are in `point143`.

The engine accepts the previous RESUME checkpoint format. New checkpoints
also include `coverage_points`, `coverage_I`, `coverage_J`, `coverage_V`.
Always run in a separate working directory to preserve old checkpoints.

Useful environment options are `RESUME`, `ITERATIONS`, `LP_LIMIT`,
`CUTS_PER_ITER` (default 12), `MAX_POINT_CUTS` (240), `CUT_CENTROIDS`
(1200), `CUT_PAIRS` (2000), and `STEER_EXACT_AREA` (1). `BATCH` and
`GROW` retain their existing column/row-generation meanings. Optional
`CUT_POSITIVE_PHASE=1` also attempts point cuts during positive phase I.

The short 5063 continuation from checkpoint 239 found hundreds of
violated point-coverages while maintaining secondary mass exactly 5063.
These are successful separation steps, not a decision for 5063.

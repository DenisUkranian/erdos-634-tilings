# Rigid cells and a global physical completion budget

21 November 2026. **3431 and 5063 remain OPEN.**

The [global physical cell-reserve theorem](GLOBAL_PHYSICAL_CELL_RESERVE.md)
combines complete physical contact rows with the number and cell locations
of retained positive and negative odd tiles. It gives an explicit completion
cost that dominates the earlier signed charge-repair budget. If a retained
packing has positive odd count `P`, negative odd count `Q`, and largest
positive population `p_max` in one odd joint cell, every completion needs
at least

\[
2c\left\lceil\frac{\max\{P+(c+\mu-p_{\max})_+,Q+c\}}c\right\rceil-c
\]

odd tiles, where `(c,mu)=(37,2)` or `(43,5)`. The theorem combines this with
the complete-row minimum, the known odd-population restrictions, and the
even charge-repair budget. A stronger optional form charges and rounds the
reserves node by node, including all unobserved cells safely.

* [Global theorem and proof](GLOBAL_PHYSICAL_CELL_RESERVE.md).
* [Exact arithmetic controls](verify_global_completion_budget.py).
* [Arithmetic replay](GLOBAL_COMPLETION_BUDGET_REPLAY.json): 1,786,484
  comparisons with the earlier budget, 376,449 retained-node checks, and
  82,062 complete odd-population checks in the stated small abstract model.

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/global/verify_global_completion_budget.py
```

## Rigid unit-charge cells

The [unit-charge minority theorem](UNIT_CHARGE_CELL_MINORITY.md) uses
actual supporting lines and rigid ordered-role uniqueness. An ordinary
Euclidean cell of charge `+/-37` at 3431 needs at least two minority
tiles; one of charge `+/-43` at 5063 needs at least five. Their total
populations are therefore at least 41 and 53. No fixed global height
range or odd population is assumed.

Its global corollary strengthens the signed reserve at every ordinary
phase node and combines those disjoint populations over all odd heights.
It remains below the total available population for some unexcluded
phase inventories and is not a nonexistence proof of either target.

* [Written proof and global corollary](UNIT_CHARGE_CELL_MINORITY.md).
* [Standard-library exact verifier](verify_cell_minority.py).
* [Replay](CELL_MINORITY_REPLAY.json): all minority values 0 through 4
  excluded at 5063, and values 0 and 1 excluded at 3431.
* [The 25 surviving relaxed 5063 line networks at minority 5](CELL_MINORITY_FRONTIER_5063.json).
* [An integral signed next-case incidence control](SIGNED_LINE_FRONTIER_5063.json).

The last two files supply abstract line-incidence data. They do not
supply line coordinates, exact endpoint currents, geometric packings,
or full tilings. The signed control also passes the opposite-role
overlap constraint at an individual intersection; the geometric
interaction of distinct intersections remains missing.

Run from the repository root:

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/global/verify_cell_minority.py
```

## A balanced cylinder countercontrol

[An explicit 16-tile packing](BALANCED_CYLINDER_COUNTERCONTROL.md) has eight
tiles of each sign, exact actual-transverse cylinder endpoint equations,
and pairwise disjoint interiors. A compact height-one version also fits
strictly inside the 5063 board. It disproves a proposed divisibility-by-six
restriction for balanced kernels below `2c`. It imposes neither full joint
gates nor whole-board filling, and both signed axis inventories are zero.

* [Exact integer verifier](verify_balanced_16_lift.py).
* [Coordinates and 120 separating-axis certificates](BALANCED_16_NONOVERLAP.json).

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/global/verify_balanced_16_lift.py
```

## Board obstruction for the uniform charged fan family

The [exact chord theorem](UNIFORM_FAN_BOARD_OBSTRUCTION.md) rules out
containing the explicit `c`-fan, `3c`-tile charged cylinder construction
inside the target board at height one. Nonoverlap forces integer anchor
spacings at least 39 for 3431 and 45 for 5063. The resulting carrier sections
exceed every available height-one short-axis board chord by at least
`81/10` and `175/8`, respectively. Translation and rotations by 60 degrees
cannot help. This does not classify or exclude other `3c` kernels.

* [Integer and rational verifier](verify_uniform_fan_obstruction.py).
* [Exact replay](UNIFORM_FAN_OBSTRUCTION_REPLAY.json).

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/global/verify_uniform_fan_obstruction.py
```

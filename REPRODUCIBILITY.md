# Reproducing the exact certificates

The reproduction code checks the finite coordinate constructions in this repository. It does **not** mechanically prove the universal prime-case candidate, the all-parameter construction theorem, or the full classification in Erdős problem 634.

## Requirements

- Python 3.10 or later.
- Python standard library only for generation and certificate verification.
- No network access, geometric floating-point tolerance or external solver is needed for these checks.

Run the commands from the repository root using ordinary Python execution. Do not use `python -O`, `python -OO` or `PYTHONOPTIMIZE`: assertion-based checks must not be disabled. The generator and the independent checker reject optimized execution explicitly.

## Complete repository replay

```bash
python3 scripts/reproduce.py
```

A successful replay must finish with exit status zero and the final marker:

```text
ERDOS634_FINITE_REPLAY=PASS
```

The runner writes its report to [`verification/replay.json`](verification/replay.json). This generated report is excluded from the payload manifest by design; it must not replace any retained input certificate. Read the complete report: an interrupted run, timeout or partial log is not a successful verification. Runtime depends on the machine.

The complete finite replay covers:

| Component | Checked scope |
|---|---|
| Main construction family | Exact coordinate examples for 77, 322 and 897 tiles; a separate geometric replay for 322 |
| Geometric bridges | Six original examples and seven further $W$/isosceles examples through [`scripts/check_scale_bridges.py`](scripts/check_scale_bridges.py) |
| Theta-isosceles constructions | Six exact certificates with 48, 75, 108, 147, 243 and 300 tiles through [`scripts/generate_theta.py --check`](scripts/generate_theta.py) |
| Separate odd-theta replay | [`scripts/verify_theta_odd.py`](scripts/verify_theta_odd.py) checks all 2,775 pairs for 75 tiles, all 10,731 pairs for 147 tiles and all 29,403 pairs for 243 tiles, plus containment, total area and subdivided boundary cancellation |
| $N=105$ boundary collars | [`scripts/verify_n105_collars.py`](scripts/verify_n105_collars.py) checks 45-tile and 57-tile **partial placements**, including all 990 and 1,596 tile pairs; it does not establish a complete 105-tiling |
| Two fixed-collar obstructions | [`scripts/verify_n105_collar_refutations.py`](scripts/verify_n105_collar_refutations.py) reconstructs a blocked inner corner in each named collar and excludes all four possible first tiles; this proves only that these two fixed partial placements cannot extend |
| Eventual constructions and transfers | [`scripts/check_eventual_families.py`](scripts/check_eventual_families.py) checks exact **macroregions and integer subdivision counts** over 132 admissible parameter pairs and transfers over 199 parameter pairs; these are not individual-tile replays of the large constructions |
| Verifier rejection tests | Ten cases: one valid input and nine invalid inputs |

The payload checksum list is in [`verification/manifest.json`](verification/manifest.json).

## Generate the 322 construction

```bash
python3 scripts/generate_tiling.py 2 3 output.json
```

The parameters are $u=2$, $v=3$. The primitive tile is $(a,b,c)=(6,5,9)$, and the output count is $(b+c)(b+2c)=14\cdot23=322$.

Generation and verification are separate roles: the construction program supplies candidate coordinates, while the independent instance checker verifies the geometric object. The current generator writes deterministic geometry data only. The retained historical JSON certificates also contain a verification record with runtime measurements; reproduction compares the geometry fields and ignores that older verification/timing record. Timings are environmental observations, not mathematical correctness conditions.

The complete runner also executes `scripts/check_n105_invariants.py`: it replays the six exact factor-pair exclusions in the irrational 120-degree equilateral branch at 105, recovers the two 60-degree candidates, and checks the stated formal boundary identity. These arithmetic checks do not establish a complete 105-tiling or a global exclusion.

The complete runner includes the eventual-construction macrogeometry check. It can also be run separately:

```bash
python3 scripts/check_eventual_families.py
```

Its output, also recorded in [`verification/eventual-family-checks.json`](verification/eventual-family-checks.json), reports a sweep over 132 admissible primitive parameter pairs and 199 parameter pairs for the transfers between shapes. The complete runner includes these results in its replay report. The checker verifies exact macroregion geometry and integer subdivision counts, including examples with nonsquarefree $b$. It does not expand every large example into individual tiles or substitute for the all-parameter proof in [`docs/eventual-rational-families.md`](docs/eventual-rational-families.md).

## Coordinate convention

Each stored pair of integer numerators $(X,Y)$ represents

$$
\left(\frac{X}{d},\frac{Y\sqrt D}{d}\right),
$$

where $d$ is the certificate's common denominator. For the retained 322 certificate, $d=18$ and $D=32$.

Squared physical distances are therefore computed exactly from $\Delta X^2+D\Delta Y^2$, divided by $d^2$. Incidence, containment and intersection-area tests can be performed in the unscaled rational coordinate plane because the positive diagonal scaling preserves these properties.

## Expected geometric facts for the 322 certificate

| Item | Expected value |
|---|---:|
| Tiles | 322 |
| Tile side lengths | $5,6,9$ |
| Target side lengths | $81,115,126$ |
| Each tile's area | $10\sqrt2$ |
| Target area | $3220\sqrt2$ |
| All unordered tile-pair intersections | 51,681 |
| Positive-area pair intersections | 0 |
| Distinct certificate vertices | 195 |
| Interior atomic edges | 474 |
| Boundary atomic edges | 42 |
| Distinct T-junction vertices | 24 |

The checker verifies congruence, orientation and target containment. It computes pairwise polygon intersections using exact arithmetic and checks that each has area zero. Containment, disjoint interiors and the equality of total areas prove coverage of the target.

For the edge check, every tile edge is split at all certificate vertices lying on it. Each interior atomic segment must occur once in each direction, and every outer atomic segment must appear once in the target boundary direction. This explicitly allows and checks T-junctions rather than imposing an edge-to-edge tiling assumption.

## Independence and scope

[`scripts/verify_322.py`](scripts/verify_322.py) reads the coordinate certificate without importing [`scripts/generate_tiling.py`](scripts/generate_tiling.py). Its polygon-intersection method differs from the generator's separating-axis method. Both implementations are internal to this project.

The checker is designed for the stated 322 instance; it is not advertised as a universal validator for every possible input schema or arbitrary triangle tiling. The general construction theorem follows from the proof in [`docs/two-piece-construction.md`](docs/two-piece-construction.md), not from finitely many successful tests.

The candidate prime classification requires mathematical review of its geometric arguments and stated external dependencies. A successful run here says nothing stronger than the finite verification scopes documented above.

The theta certificates are [`data/theta-48.json`](data/theta-48.json), [`data/theta-75.json`](data/theta-75.json), [`data/theta-108.json`](data/theta-108.json), [`data/theta-147.json`](data/theta-147.json), [`data/theta-243.json`](data/theta-243.json) and [`data/theta-300.json`](data/theta-300.json). Their generator is [`scripts/generate_theta.py`](scripts/generate_theta.py). The complete spectrum $N=3t^2$ for $t\ge4$ uses the proof of scale addition and the small-scale obstructions, not an exhaustive infinite computation.

To regenerate and check all six theta certificates separately:

```bash
python3 scripts/generate_theta.py --check
```

The $N=105$ collar certificates, [`data/n105-collar-5-21-19.json`](data/n105-collar-5-21-19.json) and [`data/n105-collar-7-15-13.json`](data/n105-collar-7-15-13.json), leave interior regions unfilled. Their successful verification establishes only that the stated partial placements pass the listed exact geometric checks. It does not show that either placement can be extended to a complete tiling or eliminate all arguments involving boundary collars.

The separate [four-placement proof](docs/n105-fixed-collar-obstructions.md)
and replay now establish that neither of those two fixed collars can extend.
The complete runner includes both exact one-node refutations and reports
`global_N105_decided: false`. These local obstructions do not exclude other
collars or all tilings at 105.

## Recording an independent replay

Please record the repository commit, operating system, Python version, exact command, exit status and complete output. If examining the proof itself, distinguish a check of one lemma from a review of the entire prime-case deduction. See [CONTRIBUTING.md](CONTRIBUTING.md).

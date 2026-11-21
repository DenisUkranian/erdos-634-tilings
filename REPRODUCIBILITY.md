# Reproducibility and verification boundary

**v0.3.0 + 21 November 2026 continuation**

## 21 November 2026: mandatory neighbors, global pair reserves, and the signed integer image

The new package is part of `scripts/verify_all.py` and runs independently as:

```sh
python3 research/2026-11-21/semiprimes/integer-closure/replay.py
```

Its six proof replays use Python's standard library. They check exact rigid
countercontrols, a contained balanced six-tile patch, 167 full periodic
endpoint kernels and seven integer square determinants, explicit signed
native witnesses, actual-coordinate mandatory neighbor obstructions, both
complete 143-tilings, paired population and height reserves, and an independent
2-SAT/geometric audit. The latter compares 28,933 small formulas against full
truth enumeration. The global pair reserve has 72,384 direct arithmetic
checks and 288 exact local neighbor choices.

The [global theorem and scope](research/2026-11-21/semiprimes/integer-closure/README.md)
distinguish the necessary bank test from full tiling feasibility. The lattice
image theorem explicitly permits negative coefficients. Neither finite
exploratory lift scans nor inconclusive mixed-integer target runs prove a
target exclusion. The existing 31-value four-cell list and all original
open target statuses are unchanged.

## 21 November 2026: physical completion reserves and integer cell gaps

The new exact package is included in `scripts/verify_all.py`:

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/replay.py
```

Its twelve checks use Python's standard library and a C++17 compiler.
They replay the rigid support-line minority exclusions, finite arithmetic
controls for the unrestricted physical completion theorem, all balanced
kernel exclusions at sizes 2, 4, 8, 10, and 14 for both targets, exact
nonoverlapping cylinder controls, a family-specific board-chord obstruction,
phase coordinates, the reduced 218,905-scheme containing list, ten new
integer dual certificates, rational two-cell witnesses for both native
roles, and the independent full 143-tile geometric control.

The small-kernel replay uses a separately written C++ search and an explicit
component induction. The dual checker verifies 221,880 new polygon-column
inequalities. The rational two-cell checker freshly verifies all 1,849
Fourier blocks from its hashed dependency and all four new cell points;
integer norm estimates prove exact feasibility, positivity, and both sign
gate capacities. Numerical optimizer output is not used as a proof.

The [global theorem](research/2026-11-21/semiprimes/continued-rigidity/global/GLOBAL_PHYSICAL_CELL_RESERVE.md)
is a written universal argument with an independent internal audit.
Its arithmetic controls are not an exhaustive physical search or a
proof-assistant formalization. The new package does not rerun its large
optional target searches: their saved row snapshots and reports record
resource stops, with no verified target contradiction. The older complete
5063 minimal-mode and two-height exclusions retain their separate full
replays in the coordinator. **Both original counts remain open.**

## 21 November 2026: rigid placements and the remaining five-block geometry

The latest exact controls are included in `scripts/verify_all.py`:

```sh
python3 research/2026-11-21/semiprimes/global-closure-next/rigid-body/verify_rigid_body.py
python3 research/2026-11-21/semiprimes/global-closure-next/global-strengthening/verify_current_controls.py
python3 research/2026-11-21/semiprimes/global-closure-next/global-strengthening/verify_abstract_joint_graph.py
python3 research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/verify_cylinder_lift.py
python3 research/2026-11-21/semiprimes/global-closure-next/five-block-two-heights/replay_single_offset.py
python3 research/2026-11-21/semiprimes/global-closure-next/global-strengthening/verify_two_block_balance.py
python3 research/2026-11-21/semiprimes/global-closure-next/global-strengthening/verify_one_height_cells.py
python3 research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/native-215-5063/verify_5063_cylinder_packing.py
```

These use Python's standard library; the single-offset replay also needs
a C++17 compiler. It freshly rechecks all 65 certificates and 780
transformations, then exhausts **9,112,001** profiles with no survivors.
The proof and independent geometric audit therefore reduce 5063 at
total odd population 215 to short heights `{0,1,2}`. The two smaller
node/cell checkers cover the arithmetic in the remaining one-, two-,
and four-class classification; the universal geometric steps remain
written proofs with explicitly linked dependencies.

The 3431 lift checker reconstructs the finite convolution on all 16,428
columns, 47,964 contained placements, 133 contained translations, and
6,736,849 exact residue/offset sampling cases. It also rechecks the
original rational Fourier certificate. The resulting fractional point
lies in the convex hull of actual nonoverlapping packings of exactly
111 tiles. Required charge and contact equations hold in the average,
not in every individual packing. This is a limitation theorem, not a
positive or negative decision of 3431.

The corresponding 5063 checker replays the new 43-root, 1,849-block
rational native-215 certificate, all 22,188 lifting columns, 65,028
contained initial placements, 410 contained translations, and 32,597,870
exact sampling cases. It proves a point in the exact-215 packing convex
hull with density at most `43/82`; profile constraints again hold only
in the mixture. Neither a floating optimizer nor a numerical tolerance
enters these proof steps.

The physical-current controls distinguish Boolean actual placements
from integer aggregated residue multiplicities. The independent 143
control has residue multiplicity as large as three. The graph-limit
checker gives exact abstract inventories passing all joint charge,
centering, and covariance constraints without claiming physical contacts.
The accompanying [physical charge-budget theorem](research/2026-11-21/semiprimes/global-closure-next/rigid-body/PHYSICAL_CHARGE_BUDGET.md)
has a separate internal mathematical audit; no minimizing integer
certificate exceeding either target budget has been obtained.

The optional full 3431 cylinder-catalogue pricing check covers all
4,207,420 placements with NumPy and exact integer coefficients. Its
bound is below 111 and it is not a required input to the lifting proof.
The optional integer torus search reached its resource limit without
a primal point or a certified contradiction. Neither optional numerical
search is interpreted as an impossibility proof.

## 21 November 2026: a global joint contact graph

The [global theorem and precise scope](research/2026-11-21/semiprimes/global-closure-next/README.md)
combine the two prime trees into a graph with one edge per unmatched
physical tile. Its signed charge flows, area demands, band connectivity,
and centroid inertia use one common tile budget. The written theorem
applies to all odd populations in the established phase framework; it
does not yet decide either target.

Run the exact finite controls:

```sh
python3 research/2026-11-21/semiprimes/global-closure-next/contact-budget/verify_contact_budget.py
python3 research/2026-11-21/semiprimes/global-closure-next/geometry3431/verify_first_moment_lift.py
python3 research/2026-11-21/semiprimes/global-closure-next/large-population/verify_odd_branch_budget.py
```

The first independently reconstructs two complete 143-tile controls,
their paired long sides, both trees, all charge and area currents, the
joint graph, exact rational minimum flow energies, and every graph-cut
inequality on those controls. These controls test the formulas; the
universal theorem is the accompanying written proof.

The second verifies a rational lifting map on all 16,428 periodic columns
at 3431, producing 65,712 strictly contained placements and preserving
each first transverse endpoint moment. Together with the previously
certified rational 111-mass witness, it proves a limitation of this
fractional relaxation, without asserting nonoverlap or an integer tiling.
The third checks the finite charge/gate arithmetic for the new 5063
branch bounds, including the conditional `n_odd>=387` theorem for a
native height-one layer with signs `(86,43)` and the exclusion of
`n_odd=215,n_1=129`. Its prior certificate check covers saved hashes and
accounting; the full certificate replay is the next section's command.
All three new commands use only the Python standard library and are
included in the root coordinator. Optional numerical probes are not
proof steps.

## 21 November 2026: complete 5063 minimal-odd exclusion

Run the exact certificate checker and the complete charge enumeration:

```sh
python3 research/2026-11-21/semiprimes/replay.py
```

This uses Python's standard library and a C++17 compiler, without an optimizer.
It checks the 65 certificate hashes, all 1,442,220 integer tile inequalities,
780 transformed cuts, translation and reflection rules, integer-range bounds,
and independent small Cartesian enumeration controls. It then repeats the
full scan of 34,672,599 profiles; 17,800,359 pass sign reserves and none passes
all cuts. The final full scan is independent of the intermediate adaptive
pool. The root replay coordinator includes this command.

`--saved-enumeration` checks the recorded scan instead of repeating it and
explicitly marks that distinction in its report. The committed coordinator
[replay record](research/2026-11-21/semiprimes/REPLAY.json) records a fresh
complete enumeration. The earlier
[final enumeration record](research/2026-11-21/semiprimes/gate-model/FINAL_PROFILE_ENUMERATION_5063.jsonl)
and [final audit](research/2026-11-21/semiprimes/audit/FINAL_DUAL_REPLAY_5063.json)
are retained separately.

The resulting theorem is `n_odd>=215` for every complete tiling of the
specified 5063 board. It does not exclude larger odd populations, decide
3431, or close either original tile count. See the
[proof and geometric dependencies](research/2026-11-21/semiprimes/MINIMAL_ODD_EXCLUSION_5063.md).

The additional five-block arithmetic control and the exact 3431 rational
relaxation witness are also included in the root coordinator:

```sh
python3 research/2026-11-21/semiprimes/charged-branches/verify_five_block_scope.py
python3 research/2026-11-21/semiprimes/global-invariant/verify_3431_rational_projection.py
```

The first accompanies the written proof that height one is unavoidable at
five odd blocks. The second checks 37 root enclosures and all 1,369 Fourier
blocks, then proves exact rational feasibility and positivity of the full
3431 endpoint relaxation at 111 tiles. Neither is a complete target decision.

## 21 November 2026: global geometric restrictions

Run the seven deterministic exact suites, without an optimizer or placement search:

```sh
python3 research/2026-11-20/semiprimes/continuation/global-closure/replay.py
```

They check the complete three-cell catalogue and positive control, actual
closed-gate mates and through-contacts, the two-gate integer certificates
requiring at least five odd blocks in that entire class, the universal
single-cell gate inequalities, the exact 5063 certificate forcing a charged
remote even branch in the minimal mode, simultaneous ordered-quotient periods,
and mixed-syllable countercontrols. The new proofs have independent internal
reviews. These checks do not exclude unrestricted tilings of 3431 or 5063.
[Proofs and precise remaining cases](research/2026-11-20/semiprimes/continuation/global-closure/README.md) ·
[Fresh exact replay](research/2026-11-20/semiprimes/continuation/global-closure/REPLAY.json).

## 20 November 2026: vertex and phase controls

The new finite standard-library controls are included in the root replay:

```sh
python3 research/2026-11-20/semiprimes/continuation/vertex-phase/replay.py
```

They check the supported-cycle geometry, strict and signed population
arithmetic, terminal-node line counts, 79,800 independent phase comparisons,
and two positive decompositions of the known 143 board. The optional solver
controls require `libz3.so.4`:

```sh
python3 research/2026-11-20/semiprimes/continuation/vertex-phase/replay.py --solver
```

The [fresh replay record](research/2026-11-20/semiprimes/continuation/vertex-phase/REPLAY.json)
includes the final source hashes and exact output. It covers the known tiling,
rejection checks, growing-catalogue query scopes and solver rebuilds. It does
not decide 3431 or 5063, rerun their large searches, or formally verify the
written geometric proofs. [Proofs and restart instructions](research/2026-11-20/semiprimes/continuation/vertex-phase/README.md).

## 20 November 2026: semiprime endpoint controls

Run the finite exact controls with Python 3 and assertions enabled:

```sh
python3 research/2026-11-20/semiprimes/continuation/global-endpoints/replay.py
```

This checks the independent global dual verifier, the known positive 143
certificate, three corrupted positive inputs, and the census of all 210,035
semiprimes through one million. It does not decide 3431 or 5063, rerun the large
inconclusive searches, or validate the geometric manuscripts used by the
arithmetic reduction. Solver-specific instructions, audits and exact scope are
in the [package README](research/2026-11-20/semiprimes/continuation/global-endpoints/README.md).

## 9–10 October 2026 supplements and source-integrity check

See the [full dated source index](research/updates-2026-10-10/README.md) for preserved packages, mathematical scope and traceability. To verify the exact original archive and its 220 directly published text mirrors without third-party Python libraries, run:

```sh
python3 scripts/verify_oct10_archive.py
```

This checks the ZIP SHA-256 `fda301389453d0579d45c595e59552769baf363138084444d4df07ee26a8d048`, hashes/sizes of all 242 source members, and byte-for-byte equality of 220 small UTF-8 files. The 22 large/binary members remain inside the ZIP. Phase 2 original `reproduce.py` was run successfully on the extracted original package, but no fresh full scientific replay, independent validation of universal geometric lemmas, or fresh heavyweight 135-LRAT replay is asserted here. CI also runs the integrity check.

## All adjacent W/beta scales — 8 October 2026

The [new theorem](research/gap-closure-oct8/group1/PROOF.md) supplies every
integer scale `m>=v` when `v=u+1,u>=2`. Its universal dissection is verified
symbolically on the entire two-parameter domain. The separate 5022 check
reads only the coordinate certificate and uses exact integer arithmetic:

```sh
python research/gap-closure-oct8/group1/check_all_adjacent_symbolic.py
python research/gap-closure-oct8/examples/check_5022.py
```

The [independent mathematical audit](research/gap-closure-oct8/literature/ADJACENT_INDEPENDENT_AUDIT.md)
explains why the polynomial checks imply a nonoverlapping positive
partition, including the empty last layer at `t=2`. This does not classify
smaller scales or arbitrary parameter pairs, and does not decide14430.

## General F3 and adjacent-W constructions — 8 October 2026

The [current package](research/universal-closure-oct8/README.md) includes
a direct 4830 construction and two parameterized geometric theorems.
The positive witnesses can be regenerated and checked without a solver:

```sh
python research/universal-closure-oct8/f3-general/construct_f3_mixed.py
python research/group2-mixed-gamma/verify_spatial.py research/universal-closure-oct8/f3-general/f3_4830_macro.json
python research/universal-closure-oct8/verify_4830_boundary.py research/universal-closure-oct8/f3-general/f3_4830_integer.json /tmp/4830-boundary-check.json
python research/universal-closure-oct8/global/check_f3_uniform_cone.py
python research/universal-closure-oct8/group1/check_adjacent_symbolic.py
python research/universal-closure-oct8/group1/adjacent_formula.py --u 3 --output /tmp/W575-formula.json
python research/universal-closure-oct8/group1/verify_general_geometry.py /tmp/W575-formula.json
```

The uniform F3 result uses its written large-size estimate and all 710
integer witnesses in the complete finite remainder. The adjacent-W result
uses a positive dissection proved for every parameter; its symbolic checker
verifies polynomial identities and signs on the entire range. The finite
unit-coordinate checks do not supply an extrapolation premise.

The separate complete135 position reduction and the final SAT-certificate
gate are documented in the package. A solver's UNSAT verdict, an unfinished
proof-checking run, or an LP timeout alone is not a negative certificate.
These targeted checks are additional to the historical suite below; the
full historical coordinator is not claimed to run every new compiled
program automatically.

## Complete60/154 certificates and240/375 constructions - 8 October2026

The [new package](research/final-closure-oct8/README.md) supersedes the earlier
154-unresolved status. The [154 proof](research/final-closure-oct8/154-audit/GLOBAL_154_PROOF.md)
links every arithmetic/structural gate and gives commands for the three complete
five-height bitmap generators and the independent replayer. C++17 and roughly
3GB free memory per sequential case suffice. A resource interruption never
counts as an exclusion. Trace SHA-256 hashes and independent reports are frozen.
The exact elimination rule uses only nonnegative variables, with no solver.

The [60 proof](research/final-closure-oct8/e60-position/PROOF.md) gives the two
complete four-height generators and independent forcing-row replays, together
with the necessary structural and all-branch arithmetic checks. Each full run
regenerates its trace in seconds on the development machine.

The [240/375 construction](research/final-closure-oct8/equilateral240/PROOF.md)
and [15-region seed](research/final-closure-oct8/equilateral240/MACRO_240_PROOF.md)
can be regenerated without an optimizer. Full independent geometry reports
check all28,680 and70,125 tile pairs respectively. These additions were verified
separately; the historical full-suite coordinator below has not been represented
as having run all new compiled checks automatically.


## Equilateral constructions — 8 October 2026

The [construction theorem](research/closure-position-oct8/equilateral-small/CONSTRUCTIONS.md)
proves equilateral `(3,5,7)` tilings with `15m²` tiles for every `m>=6`.
The new finite inputs are the complete 540-, 735- and 960-tile certificates;
the previous `m>=9` result is attributed to Zhang. The supplied coordinates
can be verified with Python's standard library, without a solver:

```sh
python research/closure-position-oct8/equilateral-audit/independent_geometry.py research/closure-position-oct8/equilateral-position/cpsat/T30_30_0-1_certificate.json
python research/closure-position-oct8/equilateral-audit/independent_geometry.py research/closure-position-oct8/equilateral-small/equilateral_540.json
python research/closure-position-oct8/equilateral-audit/independent_geometry.py research/closure-position-oct8/equilateral-small/equilateral_735.json
python research/closure-position-oct8/equilateral-audit/independent_geometry.py research/closure-position-oct8/equilateral-small/equilateral_960.json
python research/closure-position-oct8/equilateral-audit/check_negative_controls.py
```

The independent checker imports neither the constructor nor the search
program. It checks every unit tile, target containment, every pair of
tiles and exact area equality. The three full equilateral checks include
145,530, 269,745 and 460,320 tile pairs respectively. The
[audit reports](research/closure-position-oct8/equilateral-audit/README.md)
bind the coordinate files by SHA-256. Corrupted side lengths, duplicated
tiles and displaced tilings are separately rejected.

To regenerate the full coordinates from the saved 180-tile seed, run
`python construct_new.py` inside
`research/closure-position-oct8/equilateral-small/`. This construction
also needs no solver. Search programs used to discover the seed have
separate dependencies; their verdicts are not needed to check its geometry.
These focused commands are additional to the historical coordinator below.

## Positional and direction-band additions — 8 October 2026

The [direction-band package](research/closure-position-oct7/README.md) gives
the written geometric proofs and separate exact checks for the 154 candidate.
Its historical conclusion was 3–5 consecutive occupied heights; the new
complete positional certificates above now decide154. The [central-height addition](research/closure-position-oct8/central/CENTRAL_HEIGHT.md)
now also proves `n_0>=24`; nonzero occupied heights still have population
at least 26. The new nonzero-height population bound comes from supporting-line
incidence and nonoverlap; formal edge inventories alone do not prove it.
The package includes independent implementations of the finite inventory
enumerations and precise commands to reproduce their frozen reports.

These additional commands are separate from the historical coordinator
below. The small arithmetic checks use the Python standard library. The
imported full two-height positional certificate has its own reproduction
pipeline requiring NumPy, SciPy and GNU g++ with C++17; the fresh replay
checks all 873,496 placements, 19,222,288 matrix entries and 678,493 forced
assignments. See the [input audit](research/closure-position-oct7/input-audit/AUDIT.md).
The compiled search and 4830 macro probes remain exploratory; a resource
limit is recorded as `INCOMPLETE`, never as a negative certificate.

The new central-height proof, boundary profiles, exact angle-fan enumeration
and general affine-line residue bound have separate lightweight checks:

```sh
python research/closure-position-oct8/central/check_central_eleven.py
python research/closure-position-oct8/central/check_base_profiles.py
python research/closure-position-oct8/central/check_fans.py
python research/closure-position-oct8/search154/check_line_residue_bound.py
```

The historical [154 search report](research/closure-position-oct8/search154/run600-report.json)
is explicitly `INCOMPLETE`. The new affine-line residue bound was not enabled
in that recorded run. Neither a timeout nor a positive formal inventory
is a mathematical decision of 154. See the
[8 October package index](research/closure-position-oct8/README.md) for
separate proven statements, positive certificates and exploratory searches.

## Final synthesis additions — 7 October 2026

The [final synthesis package](research/final-synthesis-oct7/) contains
seven lightweight exact checks, now included in the full coordinator:

```sh
python research/final-synthesis-oct7/check_class38_nonperiodic.py
python research/final-synthesis-oct7/check_f3_height_density.py
python research/final-synthesis-oct7/arithmetic/check_matrix.py
python research/final-synthesis-oct7/arithmetic/check_full_matrix.py
python research/final-synthesis-oct7/w-beta/check_boundary_filter.py
python research/final-synthesis-oct7/w-beta/check_formal_direction.py
python research/final-synthesis-oct7/i120/check_transfer.py
```

Their [fresh combined report](research/final-synthesis-oct7/FRESH_CHECKS.json)
records only these seven executions. The universal density, nonperiodicity,
local-descent and geometric statements require their written proofs and
listed dependencies; separate internal proof reviews are linked in the
package. No full historical-suite replay, external refereeing, numerical
elliptic rank or decimal density is asserted by this update.

The retained 900-second I120 search and bounded F3 macro searches have
separate exploratory reports. An `INCOMPLETE` run is never a negative
certificate. The finite formal-direction check reproduces an earlier
result rather than establishing a new geometric theorem.

## Entire published suite

Python 3.11 or later; verification uses the standard library. Do not use `-O`, `-OO`, or `PYTHONOPTIMIZE`: some preserved legacy checks rely on assertions, and the coordinator explicitly rejects optimized execution.

```bash
python scripts/verify_all.py --jobs 2
```

The coordinator checks the file manifest, syntax, local links and scope flags, then runs every finite suite in disposable copies. Original certificates and frozen reports are not overwritten. A fresh report is written to `audit-output/full-replay.json`, which is ignored by Git. Runtime depends on hardware; the exact rational N105 checks can take several minutes. A process timeout is a failure to finish, never a mathematical exclusion.

## Suites and their scope

| Command, from repository root unless noted | What is checked |
|---|---|
| `python research/infinite-minimal/verify_orbit.py` | Exact finite orbit, two curve group laws, dual square lift, primitive coefficient normalization, local valuations and the small class-38 exclusions. Infinitely many actual minimal multipliers follow from the written local-group, real-density and prior constructive-tail proof, not from this finite sample. |
| `python research/seam-certificates/verify_seams.py` | Original-side contact trees and exact integer atom reconstruction in the retained 322-tiling. This checks the certificate method on one example; it does not enumerate all disks or settle an unresolved count. |
| `python research/local-descent/run_checks.py` | All signed even descent covers for each certificate; both projective charts in modular obstructions; true odd-F3 and even/positive-rank controls; family input and scope restrictions. The universal prime-family deductions require the written proof. Surviving local covers are never a positive global decision. |
| `python research/elliptic-sectors/run_checks.py` and `python research/elliptic-sectors/check_alpha_maps.py` | Complete reduced-form comparisons, exact elliptic maps, primitive F3 round trips, QP allocation versus forward enumeration, alpha candidates including factors of 3, scope controls, and universal alpha rational-function identities. No general rank algorithm or Mordell–Weil basis computation. |
| `python research/composite-support/run_checks.py` | Nine quartic identities/discriminants; allocation versus independent forward coefficient enumeration through 5000; scoped general-tool statuses; exact class-22 interfaces; rank-zero central-value certificate; fresh replay of the old 88-tile certificate. It does not execute a general S-unit solver. |
| `cd research/group2-trapezoids && python check_family.py` | 420 primitive ordered seed triples, 64 balanced corner instances, exact macro certificates, two fully expanded small seeds and five corruption rejections. |
| `cd research/group2-trapezoids && python check_balanced_f4.py` | Complete 1380- and 3105-tile F4 examples; all unit pairs, a nonprimitive normalization case and four corrupted certificates. |
| `cd research/group2-trapezoids && python check_free_k.py` | Free-parameter corner construction, arithmetic criterion and full unit examples outside the original scaled-shave domain. The criterion concerns this construction only. |
| `cd research/group2-trapezoids && python check_target_bridges.py` | F2/F3 target transfers for 70 primitive triples at two scales; scale-one tests verify only the macro partition, not tileability. |
| `cd research/group2-trapezoids && python verify_f2.py certificates/f2_balanced_8_7_13_m2.json` | Exact congruence, containment, coverage and all 2,047,276 pairs of the 2024-tile F2 example. |
| `cd research/attempt-obstructions && python check_corner_chord.py` | Five congruent corner tiles, disjointness, exact complement, chord avoidance and a certified square-root inequality. This is a partial configuration refuting a proposed scalar bound, not a full tiling. |
| `cd research/w-beta-caps && python run_checks.py --output fresh.json` | 48 exact symbolic identities; 45 caps, 90 collars, 112 full targets; 34,959 macro pairs; 300 expanded unit triangles and 10,908 unit pairs; arithmetic scale checks and rejected corruptions. The universal construction and its quantifiers are proved in the accompanying text. |
| `cd research/group2-f4 && python run_checks.py --output fresh.json` | 80 primitive macro instances; complete 88-, 352- and 546-tile certificates with all-pairs exact geometry; six corrupted/out-of-scope cases rejected. The general construction requires the symbolic proof. |
| `python scripts/check_repository.py` | Every included file, SHA-256 manifest, Python/JSON syntax, local link targets, scope sentinels and expanded coordinate-stream hash. |
| `python scripts/reproduce.py` | Preserved 77/322/897 and theta constructions; all old N105 collar/fan regressions; scale bridges, annuli/seeds, N21 reduction and certificate, and verifier rejection tests. This legacy runner alone is not the complete current suite. |
| `cd research/n105 && python verify_all.py --jobs 2` | Four complete fixed-instance certificates, arithmetic reduction, capped-chain and mutation regressions. The global theorem also needs the manuscript's published and geometric inputs. |
| `cd research/general-spectra && python verify_certificate.py construction_116640.json --expand` | 36 macroregions, 630 macroregion intersections and the shape/containment of all 116640 expanded triangles. Internal disjointness uses explicit standard subdivisions. |
| `cd research/general-spectra && python check_general_formulas.py` | Supplementary parameter/scale checks, 52 macro-constructions and seven rejected mutations; not an extrapolated universal proof. |
| `cd research/uniform-sectors && python run_checks.py --output fresh.json` | Modular restrictions, independent arithmetic enumeration, 554 macrocertificates, complete 2006-tile pair checks and rejected corruptions. The infinite theorem also requires the written proof and its stated classification inputs. |
| `cd research/square-class-saturation && python run_checks.py --output fresh.json` | Norm/cone criteria, exact strip cutoffs, constructive plans and 193 full macrocertificates, including corrupt-certificate rejection. No general small-scale sufficiency is inferred. |
| `cd research/c-relations && python check_relations.py --max-v 40` | Exhaustive finite integer-chain regression against the written parameterization; not the geometric prime induction. |

The first command is read-only except an optional requested report. The individual historical programs may update local reports; use the coordinator to isolate such writes.

## Root coverage, not a timeout or a search count

The N105 checkers independently regenerate root geometry and compare identities, not only a supplied number. The final root totals are 120,15,1788,120 for tiles (7,8,13), (5,19,21), (7,13,15), (5,16,19), respectively. The fourth original certificate stores 22552 states. A checker can validly visit fewer stored nodes if its own sound necessary conditions reject earlier; complete root/fan coverage and checked terminal conditions are decisive. `INCOMPLETE` never means refuted.

The historical false rule that marked an interior tile merely touching the exterior with its obtuse vertex is not used. A marked external junction must be supported by a tile with a whole edge on that same external side. The positive T-junction regression checks that distinction and the endpoint conditions of the new chain rule.

## Frozen hashes and mutable output

`verification/manifest.json` binds source, data and published document bytes. `scripts/build_manifest.py` deliberately rebuilds this ledger for a new publication; it is **not** a mathematical test. Do not regenerate hashes merely to make a failed integrity check disappear. `verification/replay.json` is a legacy mutable output excluded from that manifest; the coordinator produces fresh reports under `audit-output/` instead.

The F3 vertex-inventory package hash is also updated for the explicit
editorial correction recording the later 990 construction. Its inventory
algorithm and retained fixtures are unchanged.

Each imported research package retains a `SHA256SUMS.txt`. For this publication the package manifests are synchronized with the explicitly documented editorial changes. Original ZIP digests are in [import-provenance.json](verification/import-provenance.json). The expanded gzip coordinate file is bound both as a file and by its uncompressed stream digest, since gzip timestamps alone can change compressed bytes.

The 6 October seam-certificate continuation corrects one explanatory sentence
in `research/uniform-sectors/PROOF.md`: atomic seams of the full convex
integer-sided tiling are integral, although additive cancellation does not
require that fact. Its package hash is updated for this explicit correction;
the sector theorem and its algorithms are unchanged. The two new finite
audits above are included in the coordinator; their infinite mathematical
claims still depend on the separately stated written proofs.

## Abstract disk certificates (6 October 2026)

The [new checker](research/disk-certificates/) reconstructs the retained
322-face tiling from incidence alone and certifies nonoverlap using the
[written degree-one argument](docs/audits/disk-realization-2026-10-06.md).
Unlike the earlier seam replay, it requires no coordinate certificate as
an input or geometric validation dependency. Its independent exporter
provides provenance for the retained combinatorial example.

```sh
python research/disk-certificates/verify_disk.py research/disk-certificates/disk-322.json
python research/disk-certificates/test_disk.py
```

The latter is integrated in the full coordinator. Four positive and thirteen
adversarial inputs are retained, including nontrivial holonomy and a 4-pi
fan whose holonomy is trivial but whose boundary is invalid. This addition
does not claim a fresh replay of every older research suite, a new tiling
count, or a general classification.

The independent [F3 vertex-inventory replay](research/f3-vertex-defects/)
checks the new written defect identities on two prior constructions:

```sh
python research/f3-vertex-defects/check_inventory.py
```

Its geometric inputs are the previous free-parameter construction and the
F2-to-F3 attachment; it does not independently recheck every tile pair or
decide either scale-one candidate.

## Arithmetic continuation (6 October 2026)

```sh
python research/arithmetic-continuation/check_norm_remainder.py
python research/arithmetic-continuation/check_split_part.py
python research/arithmetic-continuation/check_other_split_branches.py
python research/arithmetic-continuation/check_global_split_part.py
python research/arithmetic-continuation/check_global_sector_cli.py
```

All five commands are read-only by default and accept `--report PATH` to write
a fresh report. Optimized Python execution is explicitly rejected. The
first compares the norm parametrization with an independent square search
and counts subthreshold representations. The other commands compare restricted
split-factor lists with direct coefficient enumeration, including all eight
surviving rows in the global odd-multiplier theorem. None checks new
tiling coordinates or turns an arithmetic candidate into a small-scale
existence decision. Their universal conclusions require the written proofs
and the previously established constructive tails. All five commands are
included in the full coordinator; this update does not assert a fresh run
of every older, unchanged suite.

The last command checks the scoped membership tool's conclusive YES/NO,
unresolved small-scale status and input rejection. To inspect N=990, run
`python research/arithmetic-continuation/classify_global_sector.py 110 3`:
it now reports YES using the newly proved nested-corner construction. See the
[package instructions](research/arithmetic-continuation/) for the exact
domain and runtime limitations.

The [source continuation audit](docs/audits/source-continuation-2026-10-06.md)
also records the attribution correction for the F3 vertex-count argument.

## Nested corners and the complete ratio cone (6 October 2026)

```sh
python research/group2-nested-corners/run_checks.py
python research/group2-nested-corners/check_balanced_7_5_small.py
python research/f3-descent-attempt/semigroup_tail.py
python research/arithmetic-continuation/check_squarefree_f3_front.py
```

The first command independently verifies the complete 345-, 506- and
990-tile coordinate certificates, the coordinate-free 990 disk, and a
negative overlap mutation. The second verifies exact semigroup witnesses
for all 240 primitive triples with `1<a/b<=7/5` and `b<4900`; it compares
complete parameter and direct-side enumerations. Together with the written
uniform `b>=4900` theorem, this closes the whole stated ratio range.
The third checks the conductor algorithm, including factor-three
normalization. The fourth is a finite regression for the separately
proved infinite family of squarefree F3-only arithmetic candidates.
All are included in the coordinator. This publication records focused
replays of these new checks, not a fresh run of every unchanged suite.

## Gamma-corner continuation (7 October 2026)

```sh
python research/group2-gamma-corners/run_checks.py
python research/group2-gamma-corners/check_two_axis_obstruction.py
python research/f3-descent-attempt/check_full_signature.py
python research/arithmetic-continuation/check_global_sector_cli.py
```

These focused replays check the 264-tile coordinate and disk certificates,
the precise restricted obstruction for the 4830 gamma remainder, the exact
symbolic edge-signature identity, and the membership tool's ordered F3
seed handling. The new seed is not applied to the exchanged target or to
F2/F4 without a separate proof. All are included in the coordinator;
this update does not assert a fresh run of every unchanged suite.
The infinite geometric assertions require their written proofs.

## Optional rebuild of publication outputs

The two new PDFs have editable sources. PDF rebuilding additionally needs Pandoc, XeLaTeX, pdfLaTeX, standard TeX packages and DejaVu fonts. No font files are distributed. From repository root:

```bash
python scripts/build_publication_outputs.py
```

This rebuilds the N105 and spectra PDFs and regenerates the expanded coordinate gzip. For coordinates alone use `--coordinates-only`; for the PDFs alone use `--pdfs-only`. Changes in typesetting tool versions or PDF metadata can change PDF hashes; treat a rebuilt artifact as a new publication snapshot, inspect it, then intentionally update the manifests. Do not expect a byte-identical PDF across TeX distributions.

## Mathematical boundary

The [complete class-22 theorem](docs/square-class-22.md) uses established
elliptic-curve arithmetic as well as the tiling spectra. Its new central-value
checker uses exact intervals and a rigorous infinite-tail bound, but cites
the conductor, local reduction types and root number. Modularity and the
rank-zero theorem are mathematical inputs, not software-verified theorems.
The [fixed-support theorem](docs/fixed-prime-support.md) likewise invokes a
published effective unit-equation result. No general S-unit enumeration or
bounded geometric campaign to compute its exact bases is claimed.

The [square-class tail/ray tool](research/square-class-tails/) implements
the finite tests in [the written theorem](docs/square-class-tails.md).
Its test suite compares inverse divisor formulas with a separate forward
parameter enumeration and checks scope-sensitive outputs. The bounds
reducing infinitely many exponents to finite coefficients are proved in
the note; they are not inferred from the test range.

The [quantitative density theorem](docs/quantitative-density.md) is a
written universal argument, including its [long-seam geometric input](docs/long-seams-density.md).
No finite checker is presented as proof of its asymptotic conclusion.
The separate [extreme-island embedding package](research/extreme-pure-embedding/)
checks an exact hierarchical construction: its 4,822,335 unit tiles are
specified by standard subdivisions, not expanded or tested pairwise.
The package README gives the exact replay commands and the boundary of
the local-switch obstruction.

Exact arithmetic eliminates numerical rounding in the implemented finite predicates. A separate geometric implementation reduces shared-code risk. Neither establishes external refereeing or formalizes the human lemmas and published classification theorems. In particular, finite CI does not prove the candidate all-primes induction, the all-parameter construction arguments, or a complete classification of all positive N.

The [claim ledger](STATUS.md), [N105 dependency note](docs/n105-global.md), [general spectra attribution](docs/general-spectra.md), and [full-solution roadmap](docs/full-solution-roadmap.md) keep those boundaries explicit.

## Integrated continuation: uniform reduction (30 September 2026)

The [uniform-reduction note](docs/uniform-reduction.md) and its complete source, test data, and separately checked positive witnesses are included in this publication. Its results are necessary spectra, two squarefree congruence obstructions, a finite candidate overlist, and formal boundary-signature witnesses. They are not a complete all-integer classification. The N=154 search is recorded as INCOMPLETE. The root verification coordinator now also replays all supplementary tests of this module in a disposable copy. Historical reports are retained with their original preparation scope.

## Integrated October modules

The original October package sources and their internal manifests are preserved byte-for-byte. ZIP digests are in [october-imports.json](verification/october-imports.json). The outer repository manifest additionally covers their integration. Fresh coordinator reports are separate from the historical `verification.json` records. The source packages’ statements that they did not push GitHub describe their original preparation, not the present integration.

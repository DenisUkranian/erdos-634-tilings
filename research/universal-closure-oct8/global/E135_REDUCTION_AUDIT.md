# Complete135 position reduction: independent audit

8 October 2026. This note certifies a finite residual problem. It does not
by itself assert that135 is possible or impossible.

The separate residual decision has since been completed by an independently
checked LRAT proof; see [the full 135 theorem](GLOBAL_135_PROOF.md).

The arithmetic gate leaves the equilateral triangle of side45 and tile
(3,5,7). The separately proved no-gap and signed-charge restrictions put
all occupied short-edge heights in a consecutive interval containing zero
with at most nine members. Therefore five bands and their reflections cover
every hypothetical tiling:

    [-4,4], [-3,5], [-2,6], [-1,7], [0,8].

The exact band lattice is g Z[rho], where eta=2+rho,
g=eta^L/conjugate(eta)^U and z=eta/conjugate(eta)=(3+5rho)/7.
Each band dictionary contains all lattice translations of all twelve
mirror/rotation templates per height, retaining exactly those contained
in the target. No height within a band is required to occur.

The producer `../e135/rle_equilateral135.cpp` represents the candidate
anchors of one template on one horizontal row as disjoint inclusive integer
intervals. This compresses the entire dictionary; it is not a sampling of
placements. Initially the allowed anchors are the intersection of three
translated target scanlines, hence a single integer interval when nonempty.

At any positioned endpoint-current row with zero target right-hand side,
if the remaining coefficients have only one sign, all variables carrying
that sign are forced zero. A trace record consists of five signed32-bit
little-endian integers: direction ID, vertical scanline index, first x,
last x, and sign. It applies the preceding valid inference simultaneously
to every integer x in the inclusive range.

`replay_e135_rle.cpp` is a separate verifier. It obtains initial target
scanlines by exact rational intersection with the three boundary segments,
instead of the producer's directed halfplane formulas. It reconstructs and
checks every template's side norms and area. For each recorded cut it tests
every opposite-sign endpoint family separately by interval intersection;
it never calls the producer's interval union/difference functions. It also
checks that no nonzero target-current row is in the range. It then deletes
only the named sign, using a separately implemented single-interval split.

A range may have become partly vacuous due to previous cuts. This is valid:
absence of opposite-sign support and zero target right-hand side suffice.
The verifier does not incorrectly require a surviving same-sign placement
at every point of a previously batched range.

All five full traces were replayed. Every surviving placement was compared
exactly, in order, with the producer's complete final dictionary:

| Band | Initial placements | Checked range records | Final placements |
|---|---:|---:|---:|
|[-4,4]|420445247592|49479639|246600|
|[-3,5]|420583549524|50644031|246600|
|[-2,6]|420309426351|50429425|246558|
|[-1,7]|420224867466|49218545|186798|
|[0,8]|420441801582|50973015|83163|

The PASS reports are `e135_rle_{center,offset1,offset2,offset3,edge}_replayed.json`.
The smaller five-height control also independently replayed successfully.

A second independent program, `check_e135_pool_embedding.py`, converts each
remaining anchor by direct inversion of the coordinate matrix and builds
its tile vectors directly from the physical rotations z^h rho^j. Thus it
does not reuse the producer's transformed-template normalization routine.
It verifies exact containment and shows that all five dictionaries and
all their reflected copies are subsets of the same246600-placement pool.
That pool is itself reflection invariant; its canonical physical-coordinate
SHA256 is

    7a9182ff37328cc6e5b7c6fe822bbcf529687ecd12a0bc31927e6633d71f715a.

The normalization report is `e135_pool_embedding_verified.json`. Coordinates
have common denominator7^8; records sort the three vertices and then sort
all triangles, packing six signed64-bit little-endian coordinates each.

**What remains after this audit:** decide the binary endpoint-current
system on that complete246600-placement pool. A SAT failure without a
checked proof or a resource limit is insufficient. A verified satisfying
integer assignment would need its exact geometric certificate checked.
This audit makes no claim about that final decision.

## Further exact Boolean presolve

`presolve_boolean_rows.cpp` derives forced0/1 assignments and parity
identifications from individual exact current rows. Each step records its
original row index. `check_boolean_presolve.py` independently replays the
implications: to justify a unit or equality, it conditions the row on each
violating Boolean assignment and proves impossibility by exact bounds,
gcd, or exhaustive enumeration when at most two variables remain.

The verifier uses different union representatives and reconstructs the
entire reduced equation set independently. It also verifies every original
variable's saved parity/fixed-value map. For the246600-variable pool this
produces197124 free variables and166392 rows after6649 units and42827
identifications. All49476 steps and all output rows passed replay.
The result is an equivalent binary system, not an infeasibility proof.

Coefficients larger than one are retained as repeated signed literals.
A SAT encoding must count these multiplicities. An unweighted count135
constraint must not be added to the merged variable list: original tile
counts carry the equivalence-class multiplicities and parities.

## Reproduction

```sh
python3 research/universal-closure-oct8/global/reproduce_e135_reduction.py /tmp/e135-reproduction
```

This regenerates and independently checks all five traces, deleting each
large trace after its successful replay and retaining the final dictionaries.
`--existing` replays preserved traces without modifying them. A timeout is
reported as incomplete, never as a proof.

For an exported original residual model:

```sh
g++ -std=c++17 -O2 research/universal-closure-oct8/global/presolve_boolean_rows.cpp -o /tmp/presolve135
/tmp/presolve135 /tmp/e135-k7-center.model.txt /tmp/e135-dsu
python3 research/universal-closure-oct8/global/check_boolean_presolve.py /tmp/e135-k7-center.model.txt /tmp/e135-dsu /tmp/e135-dsu-checked.json
```

The auxiliary model-to-geometry gate is separately checked by
`../e135/check_unit_metric_model.py`: it reconstructs all246600 exact
triangles and all247770 positioned endpoint rows, then compares the entire
equation multiset with the input model. The PASS report is
`../e135/unit_metric_model_verified.json`. Thus this modeling step is an
explicit separate dependency, rather than an assumption inside the presolver.

# Exact supporting-line and packing limits for 3431

**3431 remains open.** This directory gives an exact result about the
proposed strengthening of its minimal 111-odd-tile model.

The complete cylinder model retains each actual transverse supporting
line and uses every contained native height-one placement. It still
periodizes the longitudinal coordinate by 37. A finite positive
convolution proves that its projection onto residue/gate/population data
is exactly the old torus projection. In particular, the previously
certified rational population-111 profile survives.

Averaging 133 strictly contained translates produces a stronger
rational witness. It lies in the convex hull of actual integral,
nonoverlapping, contained partial packings of **exactly 111** height-one
tiles. Its density is at most `111/133` at every point. The required sign
populations, gate currents, and cylinder equations hold only in the
mixture; no individual packing with that full profile is asserted.
The distinction is

\[
 \operatorname{conv}(P_{111})\cap H
 \quad\hbox{versus}\quad
 \operatorname{conv}(P_{111}\cap H).
\]

Thus generic packing inequalities, even all inequalities valid for the
exact-111 packing hull, cannot eliminate this fractional witness using
only the retained linear equations. A successful obstruction must
couple those equations to a common integer configuration or use
additional physical conditions.

## Required exact proof

* [CYLINDER_LIMIT.md](CYLINDER_LIMIT.md): full proof, explicit scope,
  convolution, contained translations, and finite exact-111 packing
  decomposition.
* [verify_cylinder_lift.py](verify_cylinder_lift.py): standard-library
  verifier; it also reruns the existing exact rational torus certificate.
* [CYLINDER_LIFT_REPLAY.json](CYLINDER_LIFT_REPLAY.json): checked data,
  source hashes, all 133 translations, and exact inequalities.

From the repository root:

```bash
python research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/verify_cylinder_lift.py
```

Expected result: `checks: PASS`, with 16,428 operator columns, 47,964
strictly contained single-patch placements, 133 strict contained
translates, and 6,736,849 checked residue/sampling-offset cases. The
finite convex recipe represents 80,842,188 exact-111 packings when
repeated components are retained. It is verified by interval counts,
not by materializing that many packings. Run without `-O` because the
imported source checker uses assertions.

## Optional complete catalogue and pricing control

[cylinder_model.py](cylinder_model.py) generates all **4,207,420**
contained native height-one placements, 137,307 cylinder endpoint rows,
and 74 gate rows. The optional exact dual certificate is stored as
deterministic gzip in `PERIODIC_DUAL_FULL_CATALOGUE.json.gz`.

```bash
python research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/verify_cylinder_dual.py research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/PERIODIC_DUAL_FULL_CATALOGUE.json.gz --out research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/FULL_CATALOGUE_PRICING_REPLAY.json
```

The independent checker enumerates the entire bounding box, tests all
three vertices against all three board sides, and checks a complete
143 tiling as a positive control. It proves the fixed-profile lower
bound `105304866294/1000000002`, which is below 111. This pricing control
requires NumPy, but no optimizer. It is not needed for the rational
feasibility theorem.

`periodic_dual_control.py` reproducibly discovers the periodic dual with
SciPy before integer rounding and exhaustive pricing. Its numerical
log is `PERIODIC_DUAL_DISCOVERY.json`.

## Optional exploratory material

`column_generation.py` contains the restricted-master discovery code,
with every pricing pass covering the full 4,207,420-column catalogue.
The small logs in `run_native_f2/` and `run_native_f2_ipm/` document a
simplex timeout and unsuccessful interior-point solves. They are
retained as numerical provenance only. They are not proof inputs, and
the exact convolution theorem supersedes the search for a separating
cylinder dual.

`SINGLE_OFFSET_AUDIT_REPLAY.json` is a separate cross-audit of the new
5063 two-height exclusion. Its `fresh_exhaustive_enumeration: false`
flag records that this audit independently reran all certificate,
symmetry, and small-enumeration checks while using the author's saved
complete 9,112,001-profile enumeration. It is not a 3431 proof input.

## Parallel native-215 result for 5063

The separately verified continuation in
[native-215-5063/README.md](native-215-5063/README.md) applies the same
finite lemma to the new rational native profile at 5063. There are 410
strict contained translations, giving density at most `43/82` and a
convex decomposition into integral nonoverlapping partial packings of
exactly 215 tiles. Its required sign and gate/current data again hold
only in the mixture. It has its own checker and replay and does not
change the frozen 3431 certificate.

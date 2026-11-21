# Native 215 cylinder and packing-hull witness for 5063

**5063 remains open.** The exact source profile with signs `(129,86)`
and native gate currents `(42,1)` extends to actual supporting-line
cylinder equations. Averaging 410 strictly contained translates gives
a rational point in the convex hull of actual integral nonoverlapping
partial packings of exactly 215 native height-one tiles.

The required signs, gate profile, and cylinder equations hold only in
the mixture. No one packing with that full profile is constructed.

* [CYLINDER_PACKING_LIMIT_5063.md](CYLINDER_PACKING_LIMIT_5063.md): general
  finite lifting and fixed-cardinality packing lemma, the 5063 proof,
  and its precise limitation.
* [verify_5063_cylinder_packing.py](verify_5063_cylinder_packing.py): exact
  standard-library replay, including the complete rational source check.
* [N5063_CYLINDER_PACKING_REPLAY.json](N5063_CYLINDER_PACKING_REPLAY.json):
  verified counts, all 410 translations, and source hashes.

```bash
python research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/native-215-5063/verify_5063_cylinder_packing.py
```

Expected result: `checks: PASS`; 22,188 operator columns, 65,028 strictly
contained initial placements, 410 strictly contained translated hulls,
32,597,870 checked residue/sampling-offset cases, and exact component
cardinality 215. The global density bound is `43/82<1`.

The finite convex recipe represents 391,174,440 packings if repeated
components are counted. They are verified through interval counts,
without materializing each full packing. Run without `-O`; no optimizer
or external numerical package is needed.

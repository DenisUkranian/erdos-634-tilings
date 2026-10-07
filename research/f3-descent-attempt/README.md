# F3 descent and small-polygon investigation

[F3_FULL_SIGNATURE_BARRIER.md](F3_FULL_SIGNATURE_BARRIER.md) proves that
every primitive F3 coefficient passes the complete translation-invariant
directed-edge signature, exact tile-count/area bookkeeping, and known
height-population congruences. The witness is an unplaced orientation
inventory, never a tiling. `check_full_signature.py` checks the identity
symbolically; `full_signature_report.json` records its zero remainder.
The subsequent [gamma-corner construction](../group2-gamma-corners/PROOF.md)
gives actual F3 tilings for `b<a<=2b`, including 264 with `(a,b,c)=(5,3,7)`.
Thus `bc>=a²` is now disproved as a necessary condition for F3 tileability,
independently of the formal signature barrier.

[TERNARY_SEMIGROUP_TAIL.md](TERNARY_SEMIGROUP_TAIL.md) proves a constructive
conductor bound for `<a,b,c>`. Combined with the nested-corner theorem, it
gives multiplier-one tilings, and consequently all positive integer
multipliers, uniformly for every primitive tile with `1<a/b≤7/5`.
The proof joins the uniform tail `b≥4900` to a complete 240-witness
certificate below that bound. More generally it covers every closed ratio interval below
the root `ρ_*≈1.46557`, once b exceeds the explicit sufficient threshold.
`semigroup_tail.py` replays the exact residue algorithm and prints a
deterministic report; `--report PATH` optionally saves it.

[SMALL_POLYGONS.md](SMALL_POLYGONS.md) proves a universal small-count
rigidity theorem for convex balanced polygons with three 60-degree side
axes. It excludes every `ab`-by-`c` 60-degree parallelogram tiling by the
primitive 120-degree triangle `(a,b,c)`: area would require `2c` tiles,
but such a small tiling can only consist of paired a-by-b lozenges.

For `(8,7,13)` it rules out a proposed 26-tile strip inside one 54-tile
auxiliary region. It does not rule out the whole auxiliary region or
990; a different enlarged-corner construction can bypass that strip.

The proof combines exact chirality-count Laurent factorization with
median-cut lattice divisibility. It allows arbitrary T-junctions and
does not assume that an extreme component is pure or convex.

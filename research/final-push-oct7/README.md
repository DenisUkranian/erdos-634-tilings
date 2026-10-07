# Three general geometric routes: results and remaining gap

7 October 2026. This continuation does **not** complete Erdős problem 634.
No previously unresolved count is declared positive or negative here.
The fixed-N decision procedure and certificate checkers are not presented
as the requested classification of all counts.

## A. A positive F3 reduction without an aspect-ratio cutoff

For every primitive plus-norm tile with `a>b>0` and
`c²=a²+ab+b²`, the canonical primitive F3 target has a positive partial
partition into three c-fold tiles, three b-fold tiles, one 2b-fold tile,
and a specified simple hexagon. The seven macrotriangles have disjoint
interiors and ordinary integer subdivisions into the original tile.
The remaining hexagon has area equal to

    N_H = 2b(3a−2b)

unit tiles; thus the count identity is

    3(a+b)(a+2b) = 3c² + 7b² + N_H.

The [geometric proof](f3/FAN_HEXAGON.md) includes universal containment
inequalities, nonintersection and exact cross-sections of the remainder.
The [independent current calculation](pentagon/SHORT_HEIGHT_OBSTRUCTION.md) checks
the limitation: the remainder cannot be filled using only one common
short-edge height, or only the associated parallelograms. Additional
orientations are essential for this particular filling. A successful
filling would be sufficient for primitive F3, but extraction of this
partition from an arbitrary F3 tiling is not claimed.

## B. A genuine all-orientation obstruction in a W cap

The [parallelogram parity theorem](w/PARALLELOGRAM_PARITY_AND_CAP.md)
proves that every parallelogram tiled by the primitive W tile
`(uv,v²−u²,v²)` contains an even number of tiles, allowing reflections,
all relative orientations and T-junctions.

For the unchanged troublesome parallelogram in the scaled `+d` cap,
this forces `u|d²`. If u is squarefree, that specific region is tileable
if and only if `u|d`; sufficiency is the existing grid construction.
In particular the `(6,5,9)` `+1` cap cannot be repaired by filling that
same region in additional orientations. A construction crossing its
boundary remains possible in principle. This is not a necessity theorem
for the full W target.

## C. Positive multiple coverage does not locally split into tilings

The [nine-tile angular construction](duality/LOCAL_MULTIPLICITY.md)
gives, for every 120-degree triangular tile, an exact local twofold cover
which cannot be divided into two single covers. Five of its sectors
have an induced odd cycle of positive-area intersections. This refutes
a universal local sheet-decomposition step. It does not construct an
untileable triangular target with a fractional tiling, and does not
decide a global existence equivalence.

The [ordered boundary-word calculation](duality/NONCOMMUTATIVE_BOUNDARY.md)
also proves that groups of any prime exponent cannot obstruct F3. This
includes nonabelian receiving groups. Higher prime-power and general
group quotients, and positive geometric realizations, are not settled.

## What remains

Route A still needs a mixed-orientation filling or a different general
partition. Route B still needs an actual replacement that crosses the
failed cap interface, or a necessary global extraction theorem. Route C
still needs a genuinely global positive-completion or integrality result.
The local counterexample rules out one proof mechanism, not every such
global theorem.

Neither 154 nor 4830 is decided by this continuation. In particular,
the unique primitive F3 candidate for 4830 remains an actual geometric
existence question. The complete [thirteen-row gap map](../../docs/global-gap-2026-10-07.md)
still applies. A full answer must settle every remaining count, including
the infinitely many primitive candidates; these lemmas do not do so.

## Verification scope

Written universal proofs were read independently within this project.
Exact finite checks accompany the F3 macrogeometry, boundary calculations
and local multiplicity construction. They are regression evidence for
the stated lemmas, not formal verification of all mathematics or a fresh
replay of the entire historical repository suite.

```bash
python research/final-push-oct7/f3/check_fan_hexagon.py
python research/final-push-oct7/pentagon/check_currents.py
python research/final-push-oct7/duality/check_duality.py
```

The top-level claim ledger and all retained reports continue to mark the
complete problem as unresolved.

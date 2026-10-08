# Equilateral constructions and continued work on 154

Denis Paliy, research with ChatGPT assistance. 8 October 2026.

**For every integer `m>=6`, an equilateral triangle of side `15m` can
be tiled by `15m²` congruent `(3,5,7)` triangles.** The new positive
multipliers are 6, 7 and 8; Zhang already supplied every `m>=9`.

| Equilateral side | Tile count | Complete unit coordinates | Independent exact audit |
|---:|---:|---|---|
| 90 | 540 | [Certificate](equilateral-small/equilateral_540.json) | [PASS](equilateral-audit/equilateral_540_independent.json) |
| 105 | 735 | [Certificate](equilateral-small/equilateral_735.json) | [PASS](equilateral-audit/equilateral_735_independent.json) |
| 120 | 960 | [Certificate](equilateral-small/equilateral_960.json) | [PASS](equilateral-audit/equilateral_960_independent.json) |

The [construction theorem](equilateral-small/CONSTRUCTIONS.md) starts
with a new 180-tile trapezoid, extends it by elementary tiled bands,
and uses the cyclic three-trapezoid assembly. The table supplies actual
unit coordinates, not merely a proposed macro expansion. The
[independent checker](equilateral-audit/README.md) verifies every tile,
containment, all tile pairs and total area using exact integers.
Checking and regenerating these constructions require no solver.

Sides 105 and 120 are counterexamples to the specific nonexistence
conjectures in Zhang, *Tiling Triangles with 2pi/3 Angles*,
arXiv:2512.22696v4, §3.1. These numbers are **side lengths**, with tile
counts 735 and 960. The proof includes a careful source comparison;
no priority assertion beyond the inspected sources is made. This does
not prove that 540 is minimal or classify all admissible counts.

## Contents and verification scope

| Package | Result or role |
|---|---|
| [Equilateral construction](equilateral-small/CONSTRUCTIONS.md) | Written infinite-family proof, elementary construction program and full 540/735/960 certificates. Earlier bounded macro probes are retained with their original scope. |
| [Independent geometry audit](equilateral-audit/README.md) | Separate implementation checking the 180- and 315-tile trapezoids and all three complete equilateral targets; corruptions are rejected. Internal implementation independence is not external refereeing. |
| [Positional seed search](equilateral-position/README.md) | Discovery programs, search reports and the complete 180-tile seed. The proof uses its independently checked coordinates, not a solver's assertion. |
| [Central height for 154](central/CENTRAL_HEIGHT.md) | New theorem `n_0>=24`, excluding all 28 possible eleven-tile inventories through affine-line incidence and the exterior base. |
| [Base profiles and angle fans](central/BASE_BOUNDARY.md) | Complete 2561 boundary-edge profiles and additional necessary fan-inventory tests. Some individual formal inventories fail; surviving controls are not tilings. |
| [Affine-line chord filter](layers/AFFINE_LINE_CHORD_FILTER.md) | Position-sensitive necessary layer conditions. Five-height formal controls still survive the stated relaxation. |
| [Continued 154 search](search154/README.md) | Exact search continuation remains `INCOMPLETE`; no positive tiling or global negative certificate. A separately proved [residue bound](search154/POSITIONAL_RESIDUE_BOUND.md) was not enabled in the recorded run. |

Combined with the preceding [direction-band proof](../closure-position-oct7/README.md),
every hypothetical 154 tiling still has 3–5 consecutive short-edge
heights, with `n_0>=24` and at least 26 tiles at each occupied nonzero
height. Twelve bands remain, seven up to reflection. The present
update does not reduce that band list further.

**154, 4830 and the complete classification in Erdős 634 remain
unresolved in this work.** Reproduction commands and dependency
boundaries are in the root [REPRODUCIBILITY.md](../../REPRODUCIBILITY.md).

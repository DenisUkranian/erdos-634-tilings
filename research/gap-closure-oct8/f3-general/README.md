# General F3 attempt: high-ratio hexagon structure

**No universal F3 construction or obstruction is proved here.** The
previous 4830 construction and its uniform cone remain valid; this folder
addresses the still-missing high-ratio continuation.

`HEXAGON_STRUCTURE.md` proves two scoped facts:

* The sufficient fan hexagon is the positive union of two equilateral
  triangles of side ab and an explicitly tiled parallelogram. A seed at
  that particular minimum equilateral scale would therefore fill it.
* The proposed 2(a+c)-tile formal two-height inventory cannot be realized
  by concatenating all of its b designated c-edges into one straight bc
  seam. The proof retains their supporting lines. It does not exclude
  other placements or added opposite-orientation pairs.

`deform_equilateral.py` is an exploratory exact-integer model for one
fixed sufficient macro topology: the 15 convex grid regions of the
previous E60=(3,5,7) seed. Shared positions, grid-edge directions, integer
step lengths, T-junction orders and target containment are constrained.
It requires `ortools`. With the original parameters it reproduces exactly
the previously verified 240-triangle coordinate set; the control and
comparison reports are retained.

For equilateral targets of sides 504 and 1008 with tile (9,56,61), the
same fixed model returns `INFEASIBLE` in both cases. This is an unsuccessful construction attempt, not a
certified geometric obstruction. It does not exclude a different macro
topology, a tiling of that equilateral triangle, or the 14430 F3 target.
In particular, the known seed's low-grid components are joined at corners;
a different topology can have freely translated components attached
through T-junctions.

No general current-to-placement principle is assumed. The new positive
W-adjacent construction from the preceding turn changes the angle family
and cannot automatically fill this 120-degree F3 hexagon.

Reproduce the retained construction experiments (requires `ortools`):

```bash
python research/gap-closure-oct8/f3-general/deform_equilateral.py --a 3 --b 5 --c 7 --side 60 --seconds 5 --output research/gap-closure-oct8/f3-general/E60_control.json
python research/gap-closure-oct8/f3-general/deform_equilateral.py --side 504 --seconds 30 --output research/gap-closure-oct8/f3-general/E504_deformed.json
python research/gap-closure-oct8/f3-general/deform_equilateral.py --side 1008 --seconds 30 --output research/gap-closure-oct8/f3-general/E1008_deformed.json
```

The positive control has all 240 triangles of the original certificate
exactly, after rational normalization; `deformation_checked.json` records
that comparison. These experimental `INFEASIBLE` statuses have no separate
proof certificate and are retained only as failures of the specified
search model, not as published tiling nonexistence results.

# Physical-current audit and exact limits of global graph moments

21 November 2026. These results continue the attempt at an unrestricted
geometric obstruction. **Neither original count 3431 nor 5063 is
settled by this package.**

* [Full physical currents and nonoverlap](FULL_CURRENT_AND_NONOVERLAP.md):
  a finite family of actual CCW polygon placements with nonnegative
  integer multiplicities and exact full physical current equality is
  already a tiling. The whole-board model already uses rigid Boolean
  placements. Overlap clauses can help its incomplete search, but are
  redundant at complete physical current closure. A periodic residue
  model does not have that implication.
* [Exact graph and global-moment limit](ABSTRACT_GRAPH_LIMIT.md):
  the established larger-population abstract axis inventories pass
  all new joint charge energies, connectedness, area energies and
  centering corrections. Exact orientation-covariance completions
  show that every tensor version of these global moments also passes.
  None of these abstract objects has a common physical realization.
* [Two-block balance in the one-height 5063 regime](TWO_BLOCK_BALANCE_5063.md):
  if every odd tile has height one, every 86-tile exact height-one node
  is balanced, including the native nodes. A new supporting-line
  argument excludes monochromatic 86-tile classes with at most two
  minority-hand tiles; the exact gate residues would force precisely
  such a distribution. This still does not exclude the 215-tile layer.
* [One-height 215 cell classification](ONE_HEIGHT_CELL_CLASSIFICATION_5063.md):
  the native Euclidean class is occupied; the layer has one, two, or
  four joint cells. In the four-cell case the complete sign matrix has
  one integer parameter `1<=x<=42`. An isolated charged 129-cell is
  excluded by a precise transfer of the original 65 profile certificates.
  The complete containing list has 296,521 phase and sign skeletons;
  their geometric feasibility has not been decided.
* [Independent cylinder-lift audit](CYLINDER_LIFT_AUDIT.md): the new
  3431 cylinder point lies in the convex hull of contained nonoverlapping
  integral partial packings of exactly 111 tiles. Its prescribed sign
  and gate data hold only in the mixture. The full mathematical proof
  and exact replay were independently checked.
* [Independent native 215 cylinder audit](N5063_CYLINDER_PACKING_AUDIT.md):
  the analogous 5063 source certificate and 410-translate lift also
  pass. All 32,597,870 interval-cardinality cases give exactly 215
  nonoverlapping contained tiles per component; the required signs
  and currents remain properties of the fractional mixture.
* [Independent physical-budget audit](PHYSICAL_BUDGET_AUDIT.md): the
  finite complete-row obstruction criterion and depth-`N` completeness
  of actual placement expansion are sound; no target inequality above
  the available tile count has yet been established.

The first note is supported by small exact controls which separate
the mathematical hypotheses. Two actual nine-tile triangular tilings
satisfy full currents and nonoverlap. Their fractional average has
the same full current but overlaps. A different set of nine distinct,
contained, congruent integer placements has the correct area and
periodic current but an overlap and a hole; its full physical current
has 12 uncanceled rows. These are general theorem controls, not
3431 or 5063 searches.

Run the deterministic standard-library checks from this directory:

```sh
python3 verify_current_controls.py
python3 verify_abstract_joint_graph.py
python3 verify_two_block_balance.py
python3 verify_one_height_cells.py
```

The recorded outputs are
[`CURRENT_CONTROLS_REPLAY.json`](CURRENT_CONTROLS_REPLAY.json),
[`ABSTRACT_JOINT_GRAPH_REPLAY.json`](ABSTRACT_JOINT_GRAPH_REPLAY.json),
[`TWO_BLOCK_BALANCE_REPLAY.json`](TWO_BLOCK_BALANCE_REPLAY.json), and
[`ONE_HEIGHT_CELL_CLASSIFICATION_REPLAY.json`](ONE_HEIGHT_CELL_CLASSIFICATION_REPLAY.json).

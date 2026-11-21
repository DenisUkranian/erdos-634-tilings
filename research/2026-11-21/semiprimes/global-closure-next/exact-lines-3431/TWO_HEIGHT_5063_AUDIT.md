# Independent audit of the 5063 two-height exclusion

21 November 2026. **Result: PASS under the stated five-block hypothesis.**
This audit concerns
[TWO_HEIGHT_EXCLUSION_5063.md](../five-block-two-heights/TWO_HEIGHT_EXCLUSION_5063.md).
Its conclusion leaves only odd short height one when `n_odd=215`;
neither the entire 215 mode nor the original count 5063 is excluded.

## Geometric reduction checked independently

The `2c` and `3c` odd layers each occupy exactly one node in each tree:
two positive odd nodes would require at least `4c` tiles at that height.
The intersection of their two node classes is one Euclidean translate.
The separate sign divisibility therefore applies to each whole layer.

If the middle `2c` layer were monochromatic, the previously audited
exterior-free two-block theorem forces both of its nodes onto the
exterior chains. Their intersection at height one is the native class.
The other odd layer has charge `c(1-2 sigma)` and enters each child
subtree entirely or not at all. At a remote gate the current residue is
therefore either `(0,-1)` for a positive middle or `(0,3)` for a negative
middle, modulo 22. Neither admits a nonzero current of the required
sign and magnitude at most 16. The two remaining native gates hold at
most 32 tiles, contradicting 86. A zero current means an empty gate
only in this monochromatic argument; that restriction is respected.

Once the middle is balanced, the other layer has signs `(86,43)`.
The actual-median identities force a nonzero height-two step because
the median parameter is one or two and 22 divides neither. Its real
lower-bank tile belongs to the unique height-one class and anchors
that class to the native lattice. This uses an actual path and tiled
subregions, rather than an abstract boundary word.

For the outer charged class, every child subtree has zero odd charge:
the outer layer is at the parent level, and the only other odd layer
is the balanced middle, entering wholly or not at all. If both parent
nodes were exterior-free, all gate currents would be multiples of 22,
contradicting their sum 43. Thus the relevant exterior ancestor exists.
At height 3 or -1 there is exactly one child containing all three
outer sides, by the established exterior-chain classification. All
other child subtrees are exterior-free.

The unique whole-boundary child includes the exceptional even core.
Its even charge is `d+ce`; its odd charge is zero; and the boundary
character is `-3ab`. Substituting these into the signed cut identity
gives `Q=(d(d+ce)+3ab)/c=c+de`. This checks both the single offset
and its sign. The other 85 gates have `Q=de`. Reflection by negative
conjugation exchanges hands and preserves the tile sign. Normalizing
the distinguished residue changes labels and does not move a tiling
inside the board.

## Transfer and finite enumeration

The old endpoint certificates isolate the selected Euclidean class.
All other short-height classes have zero endpoint potential there;
whole complementary long sides have displacement `cU_j` after
normalization and vanish. Neither odd height -1 nor 3 is an exterior
side height. Thus the universal residue-column inequalities transfer
without any containment, native-phase, or terminal-node assumption
that is absent from the new class.

The positive gate bound 51, negative reserve 43, and total positive
reserve 86 give ordinary charges in `{-1,0,1,2}`, at most three
positive ordinary units, and at most one negative unit. The
distinguished charge is forced to be `m-p`. The opposite hand's
residue-zero gate is correctly included among the 85 ordinary gates.
Sorted positive multisets with multiplicity at most two, and a
negative index disjoint from their support, enumerate every net vector
once. Independent combinatorial counts reproduce all seven rows and
the total **9,112,001**.

The C++ source tests every independent upward/downward shift for each
of the 780 transformed cuts using integer arithmetic. I reviewed its
index mapping, multiset recursion, reserve tests, stopping flag, and
rejection accounting. The saved complete run has zero survivors and
rejections summing to 9,112,001.

I independently executed the replay with `--saved-enumeration`. It
reran all 65 base certificate checks, 1,442,220 exact column inequalities,
780 transformed-cut comparisons, geometric symmetry checks, and the
independent Cartesian small controls. It returned `PASS` in 7.76 seconds.
The separate author runs regenerated the full 9,112,001-profile
enumeration; this audit did **not** rerun that long enumeration, and
its saved output explicitly records `fresh_exhaustive_enumeration: false`.

The audit replay is
[SINGLE_OFFSET_AUDIT_REPLAY.json](SINGLE_OFFSET_AUDIT_REPLAY.json).

## Reviewed hashes

| File | SHA-256 |
|---|---|
| Theorem document | `75dd64cc0ff25680c2108556c4d00003133daa197d52022dc792946b6347d578` |
| Replay checker | `85fc1781bbf15b8f34907a541f86692a690de2be9fc6ff551971abd1de4ee799` |
| C++ enumerator | `091d72963dced5fa81471ba7984323fc00674dcb5cfedcab337f767b4cf7ecb7` |
| Complete saved enumeration | `cd3bdb7884ee11e1cd3bd453e79c6c20148ca73b3e05b50878a04c7b0aa7cd67` |

The remaining conclusion `short heights in {0,1,2}` follows from the
occupied-parent theorem once all other odd heights are absent. At
most two exact height-one nodes in each tree allows at most four
Euclidean intersections. The theorem correctly does not assert one
native class, unsigned joint-cell divisibility, deletion of balanced
cells, or a direct transfer of a whole-node current to a proper cell.

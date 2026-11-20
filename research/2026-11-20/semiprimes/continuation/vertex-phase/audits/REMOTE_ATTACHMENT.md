# Independent audit of the remote-subtree attachment bound

The audit-time paths and hashes below identify the working snapshots. Publication relocates imports, renames the signed replay scripts, and adds the separately checked shared-height explanation and explicit conjugate-tree scope. The final code hashes and fresh executed controls are recorded in [the package replay](../REPLAY.json). These internal audits are not external refereeing.

20 November 2026. Audited snapshots:

- `theory/REMOTE_BOUNDARY_BUDGET.md`: `001cdebb9cf1d827ffeb512822d9146fbe1426edc857a3ab0e246baf452211b2`
- `theory/SIGNED_PHASE_POPULATIONS.md`: `8c638803c264643894c26528711d23c68c35881e058c5c2a8ea9d12b0590ea27`
- `theory/NO_PHASE_GAPS.md`: `576995d283e2522723b21f9cb37e049d4d948d37227a467e96a938b9bd7438eb`
- `theory/verify_no_phase_gaps.py`: `30eecffb6141f7f4562bb68f4eb59870f06473a21c1ce59cf9c6591a9be5db1f`

**Assessment.** The attachment argument in Sections 2–3 is sound, conditional on the established integral-offset contact and ordinary-node population lemmas. It proves outside populations at least 175 and 204. Combining it with the global signed-parity node bound gives at most 43 and 56 required nodes within one such remote subtree. No phase-current localization or terminal-node theorem is needed for these bounds.

## The attachment contradiction

Use the tree in which descendants have increasing physical height, with outer heights `0,2,0`. Let the exterior-free subtree `S` have root height `k<=0` and contain a tile. Every boundary tile is outside `S`: a short edge would put its own node at an excluded outer node; a long edge crossing the parent/root cut would have outer height `k-1<0`.

Assume every outside short height is at least `k`. This gives the same lower bound globally, since inside short heights are at least `k` by definition. Both parts of the tiling are nonempty and a generic path in the board crosses a positive-length contact between them.

There are exactly two possible contact-node locations. If the common edge node is in `S`, the outside short node must be the parent of the root, at height `k-1`, contradicting the assumption. Otherwise the inside tile has the root as its short node, and the common edge node is the root's parent at height `k-1`. The opposite short height must then be `k`; the other possibilities `k-1` and `k-2` are globally absent.

On the entire maximal supporting run of this last contact, every edge is consequently a length-`c` long edge from a short-height-`k` tile. No outer interval can occur because this direction height is negative. Both banks have the same finite support and their partitions start at the same endpoint and advance in equal lengths `c`. They match whole edge to whole edge. A shared endpoint lies in both tiles' height-`k` short cosets, making those cosets identical. The supposed outside tile therefore belongs to the root of `S`, a contradiction.

This argument establishes an occupied outside node of height below `k`, without assuming the root itself occupied or imposing a Euclidean lattice restriction on unrelated tiles.

## The two distinct outside populations

Every outer side contains a whole long tile edge. If a side were partitioned into `r` short edges only, their `r` obtuse tile corners would have to occupy the `r-1` interior junctions, at most one per junction. The outer corners have angles below 120 degrees and cannot host an obtuse corner. This is impossible.

Apply this to the outer side of height 2. A long boundary edge has short height 1 or 3, so it supplies an ordinary occupied node outside `S` distinct from the negative-height node forced by attachment. The core is a third distinct exact node outside `S`. Their populations give `M>=j+2c+2c`, namely 175 or 204. This bound does not include an extra parity block.

Separately, `G_odd=-c` implies an odd total of population blocks at odd heights. At least one ordinary node therefore has at least three blocks. The resulting bound on **all** occupied ordinary nodes is 45 at 3431 and 58 at 5063. Required nodes inside `S` are occupied by the no-vacant-ancestor theorem, while the two attachment/boundary nodes lie outside it. Hence `R+2<=45` or `R+2<=58`, yielding 43 and 56. The extra parity block can be inside or outside `S`; its location is not assumed.

I ran the final `verify_no_phase_gaps.py`; all arithmetic bounds passed. The geometric reasoning above, rather than that finite arithmetic replay, justifies the attachment lemma. The statement is scoped to the increasing-height tree with `k<=0`; changing to the conjugate prime requires transforming both the height direction and outer heights. Weighted solver use must avoid charging the same outside node twice. Neither whole-board tiling problem is decided by this audit.

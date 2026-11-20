# Independent audit of the terminal-node arguments

20 November 2026. Internal mathematical review of the three notes below.
No solver was run for this audit. This is not external refereeing or
proof-assistant verification. The hashes identify the reviewed working
snapshots, after correction of the arithmetic typo described below.

| Note | SHA-256 |
|---|---|
| `TERMINAL_TRANSLATES.md` | `b9f86a5055e6c7740db39a8ac51901f1ff9ebd6d495cd8b14ffe8305ffb050a9` |
| `CHARGED_TERMINAL_PATCH.md` | `b1f4ae22f649f129dcc48c98b24a7162e7fe8b2335165ebcdf90e614415a2e26` |
| `WHOLE_C_DOMAIN.md` | `9a8fb3cff90894b88d6617d607834638a0683447c8853461ef8d63d66a68f70a` |

**Assessment.** I found no remaining proof error in these statements,
using their stated primitive odd tile assumptions and the cited
integral-offset, phase-node and single-block line-incidence lemmas.
Their conclusions have the scopes stated in the notes. None proves
nonexistence of a complete 3431 or 5063 tiling.

## 1. The physical boundary-chain replacement is valid

For a terminal exterior-free node at physical height `h` in the
increasing-height prime tree, a long edge at `h+1` has its edge node
strictly below the selected node. Terminality excludes every possible
neighboring short node there except the original height-`h` node;
exterior-freeness excludes an outer interval. Thus each bank consists
of full length-`c` intervals with common endpoints, and their
partitions agree. The mate is the half-turn, with the same short
height and hand and the opposite sign.

The mate remains in the same Euclidean translate `L`: its obtuse
vertex is the sum of the two common long endpoints minus the first
obtuse vertex. All three points already belong to the affine lattice
`L`. It is therefore legitimate to cancel these long-edge terms in
the boundary of the union of the selected `L` tiles.

Crucially, **no selected short edge is deleted**. On any maximal
height-`h` run containing such an edge, integral offsets put every
endpoint in `L`. Every incident short-height-`h` tile is then in that
same translate and the same phase node, hence is selected. All other
terms on the run are whole long edges of height `h`; no exterior
height-`h` contribution exists. The complete interval identity on
each run therefore replaces the entire selected short-edge chain by
signed whole long edges. This is equality of geometric segment chains,
not just equality of total lengths or areas.

After the outward long pairs cancel, the only original long edges
left have height `h-1`. Hence the resulting boundary is a balanced
integral chain with displacement vectors in `c(E_h+E_(h-1))`. Its
closed walks may occupy different translates of that lattice, and
may have signed multiplicities. Translating each closed walk before
computing its area is valid; the lattice determinant is `c` in axial
coordinates. Its total doubled axial area is the actual `ab*m(L)`.
Coprimality gives the claimed population divisibility. The separate
sign divisibility and exclusion of population `c` then follow from
the per-line character congruences, as stated. Reversing the tree
changes the remaining alphabet to `E_(h+1)` and preserves the proof.

The two lowering obstructions are also correctly scoped. A nonzero
character prevents a replacement using only the opposite height
parity. A single balanced pair's parallelogram has outer sides shorter
than `c`, so lower-height long sides cannot cover them. Neither
argument supplies a positive lowering operation for a larger patch.

## 2. The charged patch is a polygon example, not an F2 completion

The large triangle has side lengths `ac,bc,c^2`; its standard grid
has `c^2` tiles of short height one and sign sum `-c`. The two rows
of parent teeth have the asserted side norms. Their disjoint open
`x` intervals, their placement on the outside banks of the two large
short sides, and the separation at `x=a^2` establish disjoint interiors.
Each tooth shares a positive-length base with the large triangle, so
the resulting polygon has connected interior.

The parent teeth cover both height-one sides completely. Its remaining
boundary has height zero, while no tile has short height greater than
one. The chosen positive-valuation node is therefore terminal and
exterior-free **in this tiled polygon**. This correctly refutes a
zero-character assertion for all tiled polygons.

The affine map `F(x,y)=(y,c^2-x-y)` has linear part a 240-degree
rotation, so it preserves heights, areas and the sign convention.
The six-point hull and the transformed target inequalities establish
containment. I found one arithmetic typo in the initial prose: at
`(c^2-a,a)` the third expression is `aH-Ac^2`, not `c^2(a-A)`.
It has now been corrected. The exact values are `-648376` and
`-1920346`, respectively, so the required negativity and containment
are unchanged. Static inspection of `verify_charged_patch.py` confirms
that its containment test uses the direct inequality on the transformed
macro vertices, not the erroneous factorization.

The fixed F2 placement also has the claimed exterior-free phase node:
its translation belongs to `z*A_pi`, whereas the ancestor of the outer
height-two edge is the distinct coset `A+z*A_pi`, with `A` a prime-adic
unit. This says nothing about new descendants in an unknown completion.
The notes expressly retain that distinction. The example does not
refute a terminal theorem that additionally uses the entire F2 tiling
or its complement.

## 3. The whole-c domain theorem retains the necessary connectivity

For `m=c`, the two boundary characters are multiples of `c`, have odd
parity and absolute value at most `c`. Thus all signs agree and all
short heights have the same parity. Across a positive-length contact,
a height difference of two would place two oppositely directed long
sides on the common line and force opposite character signs, even for
a partial contact. A difference of one is excluded by parity. The
explicit edge-contact connectivity assumption therefore forces a
single short height.

The whole-`c` boundary representation supplies a multiple-of-`c`
exterior current on each line of that height, so the existing
single-block line-incidence argument applies. The proof correctly
does not replace this step by cancellation of all short currents when
the boundary merely has a representation using neighboring long
edges. Its simpler shortcut is restricted to the stronger inside-long-
side hypothesis. Collections connected only at isolated vertices are
explicitly excluded from the connectivity step.

The local `2c` parallelogram example and the limitation at `3c` are
consistent with the theorem. They do not assert the existence of a
compatible exterior F2 tiling. Both original target problems remain
open.

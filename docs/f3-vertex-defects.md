# Necessary vertex defects in the 120-degree F3 branch

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026.**

This note supplies necessary geometric conditions for F3 certificates. It
does not itself construct or exclude the scale-one candidates 990 and 4830.
A subsequent [nested-corner construction](../research/group2-nested-corners/PROOF.md)
resolves 990 positively; 4830 remains unresolved.
The local vertex inventory and triple-obtuse accounting are prior results
of [Beeson–Zhang, arXiv:2604.01314v1](https://arxiv.org/html/2604.01314v1),
Table 2 and the proof of Lemma 3.5, Table 3. Their proof of Lemma 3.4 also
contains the boundary c-edge argument. We specialize these results to F3
and record the mismatch-injectivity and unit-atom consequences for use in
the seam-certificate search. No external priority is asserted.

Let the primitive integer tile have sides `a,b,c`, with

    c² = a²+ab+b²,

and opposite angles `α,β,γ`, so `α+β=π/3` and `γ=2π/3`.
The F3 target has angles `(α,2α,3β)` and sides proportional to

    (c², c(a+2b), 3b(a+b)).

Reflections and arbitrary T-junctions are allowed. The two shorter sides
are unequal: `a=b` would give the impossible integer equation `c²=3a²`.
Also `α/π` is irrational. Indeed, `2cos α=(a+2b)/c` is rational and
strictly between 1 and 2. If α were a rational multiple of π, this number
would be an algebraic integer, hence an integer, a contradiction.

## Complete local angle inventory

By substituting `β=π/3−α`, irrationality makes the three target corner
fans exactly `α`, `2α`, and `3β`, respectively. They contain no γ.

At an interior vertex which is not in the relative interior of a tile
side, the possible counts of `(α,β,γ)` are exactly

    (0,0,3), (2,2,2), (4,4,1), (6,6,0).

Let their populations be `x,y,z,w`. At a T-junction exactly one tile
contributes a flat angle π. The remaining corner counts are exactly

    (1,1,1) or (3,3,0).

Let these two T-junction populations be `p,q`. At a straight external
boundary vertex the same two corner inventories apply, without a flat
tile; let their populations be `r,s`. Vertices inserted artificially in
the interior of an otherwise uninterrupted edge are not counted.

These lists follow from `i=j` and `i+2k=6` in the interior, or
`i+2k=3` on a straight half-plane. At most one flat tile can occur at a
genuine T-junction, since two would exhaust the entire angle.

## A forced triple-obtuse vertex

This is the accounting in Beeson–Zhang's proof of Lemma 3.5, Table 3:
their `C−S=2S₂+1` becomes (1) under
`C=x`, `S=z+q+s`, and `S₂=w`. We reproduce it to fix the notation used
in the subsequent mismatch argument.

Every tile contributes one α and one γ. Counting these angles gives

    N = 3 + 2y + 4z + 6w + p + 3q + r + 3s,
    N = 3x + 2y + z + p + r.

Subtracting proves the exact identity

    x = 1 + z + 2w + q + s.                              (1)

In particular, every F3 tiling has an interior vertex occupied by exactly
three γ corners. This conclusion does not depend on the scale.

## Mismatched radial edges force T-junctions

At a triple-γ vertex there are three radial contacts. Each incident tile
places one a-side and one b-side along its two radial contacts. A radial
contact is called mismatched when one incident side has length a and
the other length b. There are either one or three mismatched contacts:
among the six side incidences exactly three have length a, so the number
of mismatches is odd.

Each mismatch forces a T-junction at distance `min(a,b)` from its
triple-γ vertex: the shorter side ends strictly inside the longer side.
This point is inside the target: it lies strictly between an interior
source vertex and the endpoint of the longer side in the convex target.
Different mismatches, even from different triple-γ vertices, force
different T-junctions. To see this, at the forced T-junction the unique
flat tile identifies the longer side; that side has exactly one γ
endpoint, which recovers the source triple-γ vertex and its radial
contact. This proves injectivity without assuming edge-to-edge matching.

Write `x₁,x₃` for the triple-γ vertices with one and three mismatches.
Then `x=x₁+x₃`, and

    p+q ≥ x₁+3x₃ = x+2x₃.

Combining with (1) yields

    p ≥ 1 + z + 2w + s + 2x₃.                           (2)

Thus every F3 tiling contains at least one T-junction with corner fan
`α+β+γ` in addition to its flat tile. In particular, no F3 tiling in this
integer-sided irrational-angle setting is edge-to-edge. Equation (2)
is necessary only; it supplies no contradiction to a general tiling.

## External c-edges and a forced unit atom

The first conclusion below is already in Beeson–Zhang's proof of Lemma
3.4. The count is written explicitly here for the F3 boundary.

Every external side contains a whole c-edge. If that side is partitioned
into `K` whole tile edges, each boundary a- or b-edge contributes one γ
endpoint. No γ endpoint fits a target corner, and a straight boundary
vertex permits at most one γ. The `K−1` internal junctions can therefore
accommodate at most `K−1` such edges.

More precisely, if `s_L` junctions on this side have the all-acute fan
`3α+3β`, and `h_L` other junctions have a γ contributed by a tile that
does not place an edge on that external side, then

    number of boundary c-edges on L = 1+s_L+h_L.

Consequently the total number of external c-edges is at least `3+s`.

There is also an exact consequence of the integer-atom theorem in
[the seam-certificate note](exact-seam-certificates.md). Suppose
`|a−b|=1`. At any mismatched radial contact, the segment from the shorter
side's endpoint to the longer side's endpoint has length one. Both
endpoints are original tile vertices. Its subdivision into atomic seam
edges has positive integer lengths, so it is exactly **one atom of
length one**. Every F3 tiling of a primitive consecutive-side tile
therefore contains a unit seam atom.

For the sole arithmetic F3 candidate at `N=990`, the tile is `(8,7,13)`
and the target is `(169,286,315)`. Every possible tiling must obey (1),
(2), place a c-edge on all three sides, and contain a unit seam atom.
For `N=4830`, the candidate tile is `(24,11,31)` and the target is
`(961,1426,1155)`; the first three restrictions still apply, while the
unit-atom conclusion does not follow because `|a−b|=13`.

These constraints narrow certificate structure but do not settle either
candidate. In particular, neither a forced unit atom nor a forced
T-junction is an obstruction under the allowed definition of tiling.

The [inventory replay](../research/f3-vertex-defects/README.md) checks the
exact identities on the existing F3 constructions for `(5,3,7)` and
`(8,7,13)` at multiplier two. Both have exactly one triple-γ vertex, so
the lower bound `x≥1` is sharp. Their existence also illustrates why this
accounting alone is consistent with a tiling rather than a scale-one
nonexistence proof.

# Independent audit: an occupied remote even cell needs a parent long edge

21 November 2026. This audit supports the visibility theorem in
[INVISIBLE_EVEN_NODES](../target3431/INVISIBLE_EVEN_NODES.md). It is a
geometric argument, not a consequence of periodic endpoint equations.
**Neither 3431 nor 5063 is closed.**

## Exact hypotheses

Consider a complete tiling of one of the specified target triangles by
its fixed primitive tile `(33,7,37)` or `(35,13,43)`. Use the reflected
path frame with `R=Z[rho]`, `z=(a+b*rho)/c`, and assume:

1. Every tile has short height 0, 1, or 2.
2. Every height-one tile has all vertices in the single native cell `zR`.

These are the established minimal-odd hypotheses for 3431. They also
hold in the native one-cell subcase of the 215-odd-tile mode for 5063.
They are not asserted for every larger odd population or other odd-cell
configurations.

The phase classification and occupied-parent theorem then give the even
cells `L_r^-=rz+R` at height zero and `L_r^+=rz+z^2R` at height two,
with `0<=r<c`. A nonzero `r` is one exterior-free terminal exact node.
The proof below concerns one such remote cell `L`, with short height
`h=0` or `h=2`.

**Claim.** If `L` is occupied, at least one actual odd tile has a long
side at its corresponding short-height gate. Equivalently, a remote even
cell whose odd-parent long-edge population is zero must be empty.

Absence of parent long edges is an assertion about an unsigned physical
population. It is strictly stronger than zero signed gate current.
Equality of periodic mate multiplicities is also insufficient to infer
the hypothesis.

## 1. Actual short edges cancel within the selected cell

Suppose, for contradiction, that `L` is nonempty and that no odd tile has
a long side in its short-height gate. Let `U` be the union of all tiles
of `L`.

On any positive-length contact along a height-`h` line, the integral-offset
lemma places all edge endpoints in one translate of `z^h R`. Therefore
an opposite short edge belongs to another selected tile of `L`. An
opposite long edge would belong to a tile with short height `h-1` or
`h+1`. One of those heights is absent (`-1` or `3`); the other is one,
and such an odd long edge is prohibited by the hypothesis at this gate.
The remote cell has no exterior short-side interval.

Thus every positive-length part of every selected short edge has another
selected tile on its other side. Their oriented interval currents cancel
exactly on actual supporting lines. Short-to-short T-junctions are
permitted; this argument does not require whole short-edge pairing.

## 2. The remaining boundary has just one long height

The one-accessible-gate theorem applies under the stated hypotheses. Each
selected long edge outside the native height-one parent gate has its
whole same-height half-turn mate in `L`. Their long-edge boundary
contributions cancel. Consequently every boundary interval of `U` is
carried by a selected long side of length `c` at direction height one.

This cancels edge contributions, not tiles or their areas. In particular
`U` remains a bounded finite union with positive area. Remote even tiles
cannot expose a long side on the board boundary: their long heights are
odd, while the board sides have heights zero and two. Together with the
preceding short-side observation, `U` has no positive-length outer
boundary contact. Isolated contacts with the outer boundary cause no
problem.

## 3. Why partial cancellation cannot shorten a selected long edge

Normalize the selected cell to `R` by subtracting its origin and dividing
by `z^h`. A selected long displacement has the form

\[
 \rho^j(a+b\rho)\quad\text{or}\quad
 \rho^j(a+b\rho^{-1}).
\]

These vectors are primitive in the axial integer lattice. Before the
unit rotation their coordinate pairs are `(a,b)` and `(a+b,-b)`, whose
coordinate gcds are one; unit rotations preserve primitivity.

It follows that a length-`c` selected long edge contains no other
selected-cell lattice point in its relative interior. Along one of its
supporting lines, two selected long edges with overlapping interiors
therefore have the same endpoints and are the same whole segment. If
their tiles lie on opposite banks, the two whole contributions cancel;
if they lay on the same bank, their interiors would overlap, which is
forbidden in an actual tiling.

No selected-edge endpoint lies inside another remaining selected edge.
Two transverse selected edges cannot cross in their relative interiors:
their incident selected triangle interiors would overlap near the
intersection. Thus the remaining boundary can be represented by an
embedded graph of whole length-`c` segments, with disjoint open edges.

An outside odd tile may have a vertex in the relative interior of one
of these boundary edges. Such a T-junction changes how the outside bank
is partitioned; it does not introduce a selected-cell vertex or split
the selected graph's representation. No exclusion of these T-junctions
is used.

## 4. A supported simple cycle follows

Orient the remaining whole edges as the boundary of `U`. At each vertex
the number of incoming and outgoing edges agrees, because this is the
boundary of the sum of the selected triangle chains. The graph is
nonempty: a bounded positive-area union has nonzero boundary.

A finite nonempty balanced directed graph contains a directed cycle.
Removing repeated vertices yields a simple cycle. Since opposite
coincident edges have already canceled and the graph is embedded, this
is a nondegenerate simple polygonal loop of positive enclosed area.
Neither connectedness nor simple connectedness of `U` is required;
holes and components meeting at vertices are allowed.

Every edge vector of this cycle is `c*z*rho^j`. Following the cycle from
one initial vertex places all its vertices in one translate of `c*z*R`.
The loop is in the actual tile skeleton. Its enclosed disk lies inside
the convex board and is a union of whole tiles: no open tile interior
can cross its boundary. The disk need not consist exclusively of tiles
of `L`, which is why the supported-cycle theorem is applied to the full
tiling rather than to an assumed simply connected selected patch.

The previously proved
[supported pure-mesh cycle exclusion](../../../../2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/NO_REMOTE_GAPS.md)
forbids exactly such a cycle in either target, at every rotation.
This contradiction proves visibility.

## 5. Counting consequence and limits

Distinct remote even cells have distinct parent gates in their respective
hands. Every occupied remote cell is therefore counted by the set of
parent-used gates. The converse need not hold: odd parent tiles can
pair with each other at a gate whose even node is empty.

For 3431, let `K_occ` count occupied balanced remote even nodes and
`K_parent,0` count parent-used zero-current remote gates. With native
currents `u,v`, and `S` charged remote gates of current magnitude 26,
the sign counts `(74,37)` imply

\[
 K_{\rm occ}\le K_{\rm parent,0}
 \le\frac{111-|u|-|v|-26S}{2}.
\]

The second inequality uses unsigned integer populations: every used
zero-current gate has at least one positive and one negative odd tile.
It does not need a nonzero periodic mate defect.

In the native `(22,15)` profile with all remote currents zero, the exact
endpoint excess certificate improves `K_parent,0<=37` to
`K_parent,0<=34`. Visibility now justifies the additional consequence
that **at most 34 remote even nodes are occupied** in this profile.
This remains an upper bound, not an impossibility proof.

The proof relies on the actual target tiling, its one-native-odd-cell
normal form, and the existing supported-cycle theorem. It must not be
transferred to an arbitrary periodic cylinder inventory, a general local
patch, a different board, or a configuration with other occupied odd
cells or short heights. In particular it does not contradict the
small-shape two-parent control, which has actual parent long edges and
is not a tiling of either target board.

## Dependencies

- [Minimal odd phase classification](../../../../2026-11-20/semiprimes/continuation/global-closure/median/MINIMAL_ODD_PHASE_CLASSIFICATION.md).
- [One accessible long-edge gate](../../charged-branches/ISOLATED_GATE_TERMINAL_COST.md).
- [Occupied-parent and embedded-cycle arguments](../../../../2026-11-20/semiprimes/continuation/vertex-phase/NO_PHASE_GAPS.md).
- [Supported-cycle theorem and exact geometric checker](../../../../2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/NO_REMOTE_GAPS.md).

This is a separate internal geometric audit. Finite certificate replays
check their stated arithmetic inequalities; they do not replace the
topological and contact arguments above, and no proof-assistant or
external-referee verification is claimed.

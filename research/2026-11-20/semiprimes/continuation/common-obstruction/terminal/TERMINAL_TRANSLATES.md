# Euclidean translates inside a terminal phase node

Research continuation, 20 November 2026. This note proves a local
structural lemma and records two obstructions to a naive lowering
argument. It does not prove nonexistence of either F2 target.

Use the canonical board and notation of the published
`continuation/vertex-phase` notes: `R=Z[rho]`,
`z=(a+b*rho)/c`, and a tile has common short height `h`, long height
`h+1` or `h-1`, and character sign `epsilon=s*(-1)^j`.
Choose the prime phase tree whose physical heights increase down the
tree. Let `v` be an exterior-free occupied node at height `h`, with
no occupied strict descendant. Thus `v` is terminal in the full
tiling. Put `E_h=z^h R`.

## 1. Population divisibility in each Euclidean translate

**Lemma.** For every Euclidean translate `L=q+E_h`, the number `m(L)`
of tiles in the terminal node whose vertices lie in `L` is divisible
by `c`. If positive, it is at least `2c`. Its positive and negative
populations are separately divisible by `c`.

Every tile of short height `h` belongs to exactly one such translate.
Fix a nonempty class `L` and let `U_L` be the union of all its tiles.
Consider its complete positively oriented boundary as an integral
segment chain.

Every long edge of height `h+1` belongs to a whole-edge half-turn
pair in the terminal node. Indeed its edge node is a child of `v`;
the absence of occupied descendants leaves only short-height-`h`
tiles on either bank, and exterior-freeness removes exterior edges
there. Both banks have the same partition into lengths `c`.
The pair shares endpoints and therefore belongs to the same
Euclidean translate `L`. These long-edge terms cancel in the boundary
of `U_L`.

No short edge has been discarded in that cancellation. On a maximal
run of height `h` containing a short edge of `U_L`, the integral-offset
lemma puts every endpoint in the same translate `L`. All short-height-
`h` tiles incident on that run belong to `L` and hence to `v`; they
are selected. Complementary edges have length `c`. There is no
exterior edge on such a run, because its height-`h` phase node is the
exterior-free node `v`. Summing these interval identities replaces
all selected short-edge terms by signed whole `c`-edges of height
`h`.

The only other terms are the selected long edges of height `h-1`.
They may be internal or exterior and are retained. Consequently the
boundary of `U_L` has a representation by whole vectors in

\[
 \Lambda=c(E_h+E_{h-1}).
\]

It is a finite balanced endpoint chain. Each closed walk has its
vertices in a translate of `Lambda`, independently of other walks.
After dividing coordinates by `z^h`, the lattice is `c(R+z^{-1}R)`.
Its axial covolume is `c`, by the primitive norm identity and the
index-`c` calculation used in the phase population theorem. The
doubled axial area of the chain is therefore divisible by `c`.
Since the same area is `ab*m(L)` and `gcd(ab,c)=1`, we obtain
`c | m(L)`.

Short-edge character cancellation on the same individual runs gives
`c | G(L)`, where `G(L)=m_+(L)-m_-(L)`. Because `c` is odd, the two
counts `m_+(L),m_-(L)` are separately divisible by `c`. If `m(L)=c`,
all its tiles would have one sign. The published single-block
line-count exclusion applies to these same per-line congruences and
rules this out. Thus every occupied translate has at least `2c`
tiles.

The proof keeps the short sides of every outward half-turn pair.
Only the matched long sides disappear. Removing the short sides as
well would invalidate the area argument.

For the conjugate prime tree, replace the remaining alphabet
`E_{h-1}` by `E_{h+1}` and reverse the descendant direction. The
same statement holds.

### Consequences

If a terminal node has population less than `4c`, all its tiles lie
in one Euclidean translate. In particular a terminal node of
population `2c` or `3c` has this intrinsic Euclidean lattice even if
other nodes at the same physical height occur elsewhere in the board.

Combined with the published terminal balance theorem, a terminal
exterior-free node of population `2c` on either target consists of
exactly `c` tiles of each sign in this single translate.

This is a localization of the existing extreme-height translate
proof. Global maximality of the physical height is unnecessary;
terminality and exterior-freeness of the selected phase node provide
the required whole-edge pairing.

## 2. Lowering a nonzero character needs more than one new height

For the union of tiles in the terminal node, let `G` be its signed
population and put `d=a-b`. The two boundary characters are

\[
 C(\partial U)=(d-c)G,\qquad
 C_*(\partial U)=(d+c)(-1)^hG.
\]

If the same region could be tiled entirely at short height `h-1`,
its first character would force the replacement signed count to be
`G`; its second would force
`(-1)^(h-1)G=(-1)^hG`. Therefore `G=0` is necessary.
More generally, a replacement using only heights of parity opposite
to `h` is impossible whenever `G` is nonzero. This is an obstruction
to a one-step lowering operation, not an impossibility theorem for a
replacement using several lower heights of both parities.

## 3. A balanced pair does not provide a positive local lowering move

Take the union of a tile and its half-turn mate across the long edge
of height `h+1`. It is a parallelogram with side lengths `a,b` and
outer side height `h`; its character is zero.

This parallelogram has no tiling by congruent tiles all of whose
short heights are at most `h-1`. Its outer sides can then only be
covered by long edges of short-height-`h-1` tiles. Such edges have
length `c>a,b`, so no entire such edge fits on any side of the
parallelogram. An edge of a contained tile which meets a straight
outer side in a positive interval lies wholly on its supporting line
and inside that side segment. Hence covering only a proper part of
the long edge cannot evade the length obstruction.

Thus zero character alone supplies no local positive lowering move.
Any proposed removal of a terminal branch must construct a
replacement for a larger region and preserve the original boundary;
discarding balanced pairs leaves holes.

## 4. Remaining gap

Neither the translate lemma nor the published `2c` balance theorem
proves `G=0` for an arbitrary terminal node. Populations `3c` and
above, with separately divisible signs, remain possible under these
arguments.

Even a theorem that all terminal exterior-free nodes have zero
character would need another global step: the distinguished ordinary
node at physical height 1, containing the outer height-2 edge node
in its subtree, is not exterior-free. It can carry the entire odd
character `G_odd=-c`; the 143 control illustrates this distinction.
No positive branch-removal operation, and no contradiction for that
distinguished node, is established here.

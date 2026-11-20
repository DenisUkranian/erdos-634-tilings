# Independent review of the terminal-translate lemma

20 November 2026. Reviewed
[`TERMINAL_TRANSLATES.md`](../terminal/TERMINAL_TRANSLATES.md), SHA-256
`b9f86a5055e6c7740db39a8ac51901f1ff9ebd6d495cd8b14ffe8305ffb050a9`.

I found no error in the replacement-chain or area-divisibility argument.
The hypotheses must remain an exterior-free node terminal in the full
tiling. An arbitrary ordinary node or a catalogue with no generated
descendants does not supply them.

For a selected translate `L=q+z^h R`, every terminal outward long edge
is whole-matched with a tile at the same short height and hand. Sharing
endpoints puts its half-turn mate in the same translate. Cancelling only
these matched long-edge terms is legitimate; cancelling their short
sides would discard part of the actual boundary.

On a maximal height-`h` supporting run meeting a selected short edge,
integer physical offsets place all endpoints in `L`. Every short-height-
`h` tile on the run therefore has all its vertices in `L`, and is among
the selected tiles. The remaining terms are whole long sides of length
`c`; there is no exterior term. The replacement of the selected short
chain by those long sides is an equality of geometric chains, not just
of total signed lengths. Endpoint measures are consequently unchanged.

After adding the uncancelled selected long edges at height `h-1`, the
result is an endpoint-balanced finite integer chain. Each of its
endpoint-connected components lies in a translate of
`c*(z^h R+z^(h-1)R)`. Components need not share a common translate.
The area calculation can be applied to their closed walks separately,
because each closed walk's signed area is translation-invariant.

After rotation by `z^(-h)`, the difference lattice is
`c*(R+z^(-1)R)`. It is an integral Eisenstein sublattice of index `c`:
its generators are `cR` and `(a+b-b*rho)R`, and the established index
calculation applies. Hence every closed walk has doubled axial area a
multiple of `c`. Summing signed areas gives `ab*m(L)`, so coprimality
implies `c|m(L)`.

The selected supporting-line currents also give `c|G(L)`. Since `c`
is odd, both sign populations are individually divisible by `c`.
The one-block line-incidence argument needs exactly these per-line
congruences and distinct placements, so it excludes `m(L)=c` without
a new geometric assumption. Thus a terminal node of population `2c`
or `3c` occupies just one Euclidean translate.

The two lowering warnings are sound. Changing every replacement tile
to the opposite height parity contradicts the two boundary characters
unless `G=0`. Conversely `G=0` is not sufficient: the balanced long-edge
pair has boundary sides of length `a,b<c`, which no tile with lower
short height can cover using its necessarily long side. This does not
exclude a replacement of a larger region using both height parities.

The mixed-cycle control in the companion boundary note supplies a larger
balanced example with `2c` tiles. It does not establish a complete board
tiling, nor disprove the possibility of a suitably enlarged global
branch-removal operation. Neither audited result settles 3431 or 5063.

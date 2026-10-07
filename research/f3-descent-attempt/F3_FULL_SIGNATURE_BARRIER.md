# Every F3 count passes the full translation-invariant edge signature

**Research directed by Denis Paliy, with ChatGPT assistance — 7 October 2026.**

This is a limitation of an obstruction method, not a geometric tiling.
For every primitive positive integer 120-degree tile with a>b, every
F3 target at integer multiplier one has a positive formal orientation
multiset with exactly the required number of tiles, the complete directed
edge-length signature of the target, and the required total area.
The same multiset satisfies the known short-height population congruences.
Its tiles are not assigned positions, and no nonoverlap is asserted.

Consequently none of these tests, even taken together, can exclude 4830
or prove a necessary inequality `bc≥a²` for arbitrary F3 tilings.
The later [gamma-corner construction](../group2-gamma-corners/PROOF.md)
actually disproves that proposed inequality: `(5,3,7)` has a 264-tile F3
tiling, although `bc=21<25=a²`. The formal identity below remains useful
as a universal limitation of direction-only additive obstructions.

## The complete signature and an exact identity

Put `ρ=exp(iπ/3)`, `Z=a+bρ`, `z=Z/c`, `δ=a−b`, `h=a+2b`, where
`c²=a²+ab+b²`. Use the reference triangle `R=conv(0,a,Z)`.
The angle `arg z` is an irrational multiple of π, so edge directions
are uniquely indexed by an integer height and a rotation modulo 6.

Work in

    A = Z[T,X,X⁻¹]/(T³+1).

Here X records the height and T records rotation by π/3. Directed reversal
negates the signature, explaining `T³=-1`. This retains all three
independent signed direction coordinates at every height; it does not
impose the additional relation `T²−T+1=0` of physical complex vectors.
Thus this is the full translation-invariant directed-edge length signature,
not just the alternating rotation character obtained by setting T=-1.

The counterclockwise signatures of R and its reflection are

    P=a+bT−cX,
    Q=−a+bT²+cX⁻¹.

In canonical coordinates the F3 target has vertices

    0,  c²,  ch z³.

Its directed third-side displacement satisfies
`ch z³−c²=3b(a+b)ρ z²`; hence its signature is

    B=c²+3b(a+b)TX²−chX³.

There is the exact identity

    B = [c(1−T)X+hX²]P + [cX+δTX²]Q.                 (1)

To verify it, the constant coefficient is c². The X coefficient is
`c(b−a+δ)T=0`. After reducing `T³=-1`, the X² coefficient is

    (−c²+ah−bδ)+(c²+bh−aδ)T = 3b(a+b)T.

The scalar term vanishes by `c²=a²+ab+b²`, and the X³ coefficient is
`−ch`. Identity (1) is also replayed by the exact symbolic checker in
this folder.

## Positive populations and padding to the correct count

The negative coefficient `−cT` in (1) is c positive copies rotated
through `4π/3`, since `T⁴=-T`. Thus (1) is the signature of the
following genuinely nonnegative orientation inventory:

| Chirality | Short height | Rotation index modulo 6 | Number |
|---|---:|---:|---:|
| R | 1 | 0 | c |
| R | 1 | 4 | c |
| R | 2 | 0 | h |
| reflected R | 1 | 0 | c |
| reflected R | 2 | 1 | δ |

Its total is `L=3c+h+δ=3c+2a+b`. The F3 count is

    N=3(a+2b)(a+b).

One has N>L: writing S=a+b, the norm gives c<S, hence L<5S, while
N≥3S² and every primitive integer norm tile has S≥8.
Furthermore `N−L` is even. Indeed c is odd. If a is odd, both N and L
have parity `1+b`; if a is even, b is odd and both are even.

Add `(N−L)/2` pairs consisting of a tile and its half-turn, all at
short height 2. Each pair has zero full signature. The resulting positive
formal multiset has exactly N congruent tiles, signature B, and total
area equal to the F3 target's area. The area statement counts the tiles
with multiplicity; it does not place them in the target.

The resulting short-height populations are

    n₁=3c,    n₂=N−3c,    n_j=0 otherwise.

These meet the F3 median-cut restrictions `c|n_j` for every `j≠2` and
`n₂≡N (mod c)`. Such congruences therefore do not remove the witness.

For `(24,11,31)` the unpadded inventory has 152 tiles. Adding 2,339
half-turn pairs gives N=4830, with height populations `(93,4737)`.
For `(8,7,13)` it has 62 tiles; adding 464 pairs gives N=990.

## Scope

Equation (1) shows that every additive invariant obtained by applying a
linear functional to this complete translation-invariant signature passes.
It does not address position-dependent boundary data, vertex realization,
convex containment, or the existence of an abstract disk certificate.
Those geometric conditions remain essential.

No implication from a positive orientation inventory to a tiling is used.
This distinction is particularly important here because the formal witness
also applies to all presently unresolved F3 parameters.

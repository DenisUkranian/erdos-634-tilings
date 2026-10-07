# Adjacent longest boundary edges for I120, F1, and equilateral targets

7 October 2026. Denis Paliy, research with ChatGPT assistance.

This extends the project's [F1 boundary lemma](../n105/BASELINE_LEMMAS.md)
to the I120 target. It is a necessary condition, not a decision of 154
or a classification of all tiling counts. No external review or priority
claim is made.

## Theorem

Let a>b>1 and c be primitive positive integer side lengths with

    c² = a²+ab+b².

Write α,β,γ for the opposite angles. Thus γ=2π/3 and
0<β<α, α+β=π/3. Suppose a triangle has corner angles

    α+k₁β, α+k₂β, α+k₃β,

where the kᵢ are nonnegative integers summing to 3. If it is tiled by
congruent copies of this tile, **each external side has two consecutive
whole c-edges**. Reflections and arbitrary T-junctions are allowed.

The possible corner triples, up to order, are I120 `(k₁,k₂,k₃)=(0,0,3)`,
F1 `(0,1,2)`, and the equilateral target `(1,1,1)`.

## Proof

Primitivity implies gcd(a,b)=1. Also
`2 cos β=(2a+b)/c` is rational and lies strictly between √3 and 2.
If β/π were rational, this number would be a rational algebraic integer,
hence an integer, a contradiction. In particular, an angle kβ can only
be filled by k tile angles β: writing

    rα+sβ+tγ = kβ

and substituting α=π/3−β and γ=2π/3 gives `r+2t=0` and `s−r=k`.
Nonnegativity forces r=t=0 and s=k. This includes k=0.

Every target corner is smaller than γ, since its angle is at most
`α+3β=π/3+2β<2π/3`. None equals β.

Fix one target side. Its boundary-supported tiles partition it into
whole edges. Mark a junction only when one of these boundary-supported
tiles has its γ angle there. A tile merely touching the side at its
γ vertex does not supply a mark. Every a- or b-edge contributes one
mark; these marks are distinct internal junctions, because a target
corner cannot contain γ and a straight boundary junction cannot contain
two γ angles. Call a c-edge endpoint blocked if it is marked or is a
target corner.

**A boundary c-edge cannot have both endpoints blocked.** Suppose that
PQ=c belongs to tile PQR, with angles β,α,γ at P,Q,R, respectively.
Then PR=a and QR=b.

If Q is marked, the gap directly across QR between PQR and the
boundary-supported marking tile has angle β. If Q is a target corner,
that gap has angle kβ for some k in {0,1,2,3}. When the gap is positive,
the first tile in it has angle β at Q, and its edge along QR has length
a or c. Both exceed b. Hence R is in the relative interior of that
edge, and this crossing tile occupies a straight sector at R. When
the gap is zero, QR is external and R is on the target boundary.
In either case an additional γ angle at R is impossible: respectively
`π+2γ>2π` or `2γ>π`.

An additional γ directly across PR at P is likewise impossible. At a
marked P the remaining gap is α; at a target corner the full angle is
already less than γ. Moreover PR is internal: otherwise PQ and PR
would be the two external rays at P, making the target corner equal
to β.

On its opposite side, PR is therefore covered by a chain of whole tile
edges of total length a. The endpoints cannot be overrun. Extending
past P leaves the target. Extending past R either leaves the target
or enters the crossing tile just found. At an intermediate junction,
the straight boundary supplied by PR forces the opposite edges to
continue along PR. This justifies the whole-edge assertion even in the
presence of T-junctions.

The chain contains no c-edge, since c>a. An a-edge would occupy the
whole chain and put a γ angle at P or R, both excluded. Thus all its
edges have length b. This gives a=jb for an integer j>0, contradicting
gcd(a,b)=1 and b>1. The blocked-endpoint assertion follows.

Finally suppose the fixed target side has n boundary edges, k of
which have length c. Its n−k non-c edges supply exactly n−k marked
internal junctions, so k≥1 and precisely k−1 internal junctions are
unmarked. Each of the k c-edges needs an unmarked internal endpoint
by the assertion. Two must use the same junction. They are consecutive
c-edges. This also proves k≥2. ∎

## Consequence for 154

For tile `(8,7,13)` and target `(91,91,154)`, write `(A,B,C)` for the
numbers of whole edges of lengths `(8,7,13)` on an external side.
Every side must have C≥2, and at least one adjacent pair of 13-edges.
The length-91 sides consequently have only the following count rows:

    (0,0,7), (2,7,2), (3,4,3), (4,1,4).

The two rows `(1,10,1)` and `(8,2,1)` from the earlier one-c-edge
condition are excluded. On the length-154 side, 14 of the earlier
17 count rows remain. The [checker](check_i120.py) exhaustively
enumerates both lists and verifies the elementary angle inventories.
It does not claim to mechanically verify this geometric proof.

These are counts and an adjacency restriction, not boundary placements
or fillings. None of the four remaining length-91 rows is excluded by
this theorem. In particular the row `(0,0,7)` must not be discarded.
The existence of a 154-tiling remains unresolved.

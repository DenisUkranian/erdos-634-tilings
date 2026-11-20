# Independent review of signed phase-cut transport

20 November 2026. Internal mathematical review; no additional solver run.
Reviewed final snapshot `SIGNED_CUT_TRANSPORT.md`, SHA-256
`494c5aadf9a38128f9aca6e11b4a6e6b1fe4be2d1bf68032ea5b06f03c6d5ff1`.
The final review also covers `CHARGED_PARENT_TRADEOFF.md`, SHA-256
`52ef41c34a49e99f8e357833fd5156a9464789bff866a3705c84bb5706e741c3`.

**Assessment.** I found no error in the cut-chain identity, its two signed
transport formulas, the physical surviving-fraction interpretation, or the
stated bidirectional-cut and rounding consequences. The final displacement,
area and charged-parent refinements were also reviewed without finding a
mathematical error. The conclusions use the
full tiling and the cited pure-cycle exclusion for the two target boards.
They do not decide either target.

## The boundary chain and exterior correction

Let `I` indicate membership of an edge node or a short node in the subtree.
The chain formed by summing `I(edge-node)` times every oriented tile side
is exactly `Gamma_S`, by nodewise interval cancellation. Subtract it from
`sum I(short-node)*boundary(tile)`. Short sides disappear because their
edge node equals the short node. The only remaining long-side terms cross
the unique parent/root cut: root-to-parent sides have coefficient `+1`,
parent-to-root sides coefficient `-1`. This proves
`partial U_S-Gamma_S=A_e-B_e` as a physical geometric chain, including
partial contacts. It does not replace `Gamma_S` by the outer intervals
actually exposed by the selected union.

Applying the ordinary character gives
`c(P_e-Q_e)=(c-d)G_S+b(S)`. A root-to-parent long side has height parity
opposite to the physical root height, and a parent-to-root long side has
the root height parity and a minus sign in the chain. The alternating
character therefore gives
`c*(-1)^k*(P_e+Q_e)=(c+d)G_star_S-b(S)` in either tree. The exterior
correction is essential at the distinguished height-one spine and at an
empty outer-edge node.

## Physical displacement and area

The new identities (8a) and (8b) follow from the same geometric-chain
identity, without another cancellation hypothesis. `Vec(u,w)=w-u`
telescopes on a closed polygonal boundary and under subdivisions.
Consequently `Vec(A_e)-Vec(B_e)=-Vec(Gamma_S)` has the correct sign.

For axial coordinates, `Det(u,w)=det(u,w)` is also additive under
subdivision along the segment. Its sum around a positively oriented tile
is `ab`, twice its axial area. Euclidean rotations preserve this
determinant sum, while reflection followed by restoration of positive
orientation preserves its positive value. Summing over the selected
tiles therefore gives

`ab*n_S=Det(Gamma_S)+Det(A_e)-Det(B_e)`.

The axial board sides from the origin and back have determinant zero;
the remaining positive side from `(A,0)` to `(0,B)` contributes `AB`.
Since `AB=abN`, the exterior term is exactly `abN*delta_2`, including
when the selected subtree is empty but contains the outer-edge node.
Actual long-side half-turn mates have opposite traversals of the same
segment, so their displacement and determinant contributions cancel.

These identities require actual endpoint coordinates. The abstract
port-flow example supplies no such coordinates and has not been shown
to satisfy these additional geometric equations. It is a countermodel
to the scalar/axis population and flow projection, not a certificate
for every positional condition in the enlarged note.

## The physical fractions really count boundary support

For an exterior-free cut the two chains have different heights, so they
cannot overlap along a positive-length interval with each other. After
cancellation within `A_e`, its surviving intervals are exactly the boundary
at the parent height; after cancellation within `B_e`, its negative is the
boundary at the root height. On a surviving interval there is only one
contributing tile from its corresponding class. This uses the actual
nonoverlapping full tiling, not merely formal current balance.

Cancellation of internal intervals pairs opposite directed characters.
Thus the full signed sums equal the surviving signed length fractions:
`P_e=sum epsilon*f_T` and `Q_e=sum epsilon*f_T`. Each fraction lies in
`[0,1]`. A positive fraction excludes a full half-turn mate, since that
mate would have the same short node and would place both banks on the
same side of the selected union. The `P` class may expose a genuine outer
interval even when the subtree is exterior-free; the note correctly
includes it. The `Q` class supports the opposite, outside bank.

The expanded pointwise bank proof is correct. On a `P` interval the
edge node is the outside parent; an opposite selected tile can therefore
only be another root-to-parent crossing tile. On a `Q` interval the edge
node is the root; an opposite unselected tile can only have the parent
as its short node, so it belongs to the same `Q` class. Exterior-freeness
rules out a `Q` interval on the outer board. These observations justify
pointwise cancellation even at partial contacts, without an assumption
that the whole crossing sides match one another.

The two boundary alphabets count disjoint interval interiors. Summing
their surviving lengths therefore gives the complete perimeter, including
holes and components. Hence `perimeter(U_S)/c=sum f_T>=|P_e|+|Q_e|` is
valid. Parity belongs to the complete unmatched tile classes, not to their
weighted fractions or arbitrary boundary subsets. No lower bound of two
whole edge lengths follows merely from a nonzero zero-signed-flow class;
the note explicitly avoids this inference.

## Bidirectionality and safe summation

If either crossing chain vanishes, the remaining boundary is a balanced
whole-`c` chain at one height with nonzero signed area. Its endpoint
components yield a supported pure-mesh simple cycle, excluded on both
target boards. Thus both surviving chains are nonzero. In particular,
neither crossing tile class can be entirely half-turn paired. This
justifies occupancy of both the root and its immediate parent, without
assuming that parent exterior-free.

If one signed flow is zero, its nonzero surviving chain has both signs
with positive fractions. It therefore needs at least two boundary-carrying
tiles. Applying this separately to both zero flows gives four such tiles
for a balanced nonempty cut. The stronger physical reading does not rely
on applying a parity statement to a fractional boundary subset.

Every tile uses one short-node/long-node tree edge. Distinct cuts in a
single tree therefore charge disjoint tile classes, and the proposed sum
of absolute flows, or the positive zero-flow correction, counts each
unmatched tile at most once. At a fixed node, classes on distinct incident
edges are likewise disjoint; sign-specific rounding follows from actual
node divisibility. Adding the analogous costs from both prime trees
without a shared accounting variable would double-count, and is correctly
excluded.

All these assertions concern actual full-tiling subtrees. An unenumerated
mate, an apparent terminal catalogue node, or the signed sum of only
selected columns cannot be substituted. The exact abstract two-tree
axis-flow witness in the sibling `joint` note satisfies the scalar and
axis conservation and exterior-free-cut population conditions. Its
missing positional geometry is precisely what the displacement and area
equations retain; no realization of those coordinates is asserted.

## Charged parent tradeoffs

The companion note is valid for terminal occupied exterior-free nodes
of the actual complete tiling. For a unit charged leaf, (13) gives
`P=sigma*c,Q=sigma*d`, so its parent supplies at least `d` unmatched
tiles of the indicated sign. Different child classes are disjoint.
Signed rounding and elimination of `x-y=z` give formulas (4) and (5)
correctly. Occupied parents and their terminal children are distinct
nodes, and the grouped bounds stay within one prime tree.

For a core-attached leaf the parent's physical height is zero, so the
leaf has odd height `1` or `-1`. Writing the full even populations as
`E_+=r_++cX,E_-=r_-+cY` gives

`Y-X=(d+r_+-r_-)/c=delta`.

At 3431, `delta=1`, so the unconstrained even minimum is `(19,45)`;
at 5063, `delta=0`, and it is `(5,27)`. A positive child requires
at least `d` positive core tiles. In both cases this forces `X>=1`
and raises both even sign allocations by one block, producing even
totals `138` and `118`. For a negative child the baseline even
inventories already cover the necessary negative core reserve, giving
totals `64` and `32`. The extra even correction may be distributed
between the core and other even nodes; the note correctly states an
aggregate bound.

The real outer-side supplier argument in Section 3 is also sound.
All target board angles are less than 120 degrees. If a board side
had `m` short tile sides and no long side, each short side would
require its tile's obtuse endpoint on that board side. No such endpoint
fits a board corner, and the `m-1` internal subdivision vertices can
each accommodate at most one obtuse angle. This is impossible. Convex
containment ensures that a tile side on the supporting board line
lies wholly on that outer side, so partial interior contacts do not
invalidate the counting argument.

A whole long side on the height-two exterior has an odd-height tile
with positive sign, because the positive outer character there is
negative and the long-side character is `-c*epsilon`. That tile
cannot belong to the selected leaf. For a height-one leaf, its long
edge node would then place the exterior node in the leaf's descendant
subtree; for a height-minus-one leaf, the supplying short height is
different. The positive supplier therefore belongs to another ordinary
odd node. Its entire sign population is divisible by `c`, proving at
least `c` positive odd tiles outside the leaf.

If the leaf charge is `+c`, the outside odd charge is `-2c`, giving
outside odd signs at least `(c,3c)` and population at least `4c`.
If the leaf charge is `-c`, the outside odd charge is zero, giving
at least `(c,c)` and population `2c`. These outside populations are
disjoint from the leaf and all even tiles. Combining the leaf minimum
`3c` with the even minima yields exactly:

| Target | Positive leaf | Negative leaf |
|---:|---:|---:|
| 3431 | `111+148+138=397` | `111+74+64=249` |
| 5063 | `129+172+118=419` | `129+86+32=247` |

No extra claim of a `c^2` leaf minimum, additive use of both prime
trees, or a target impossibility is made. These refinements are
rigorous necessary tradeoffs whose numerical costs remain below the
available total population.

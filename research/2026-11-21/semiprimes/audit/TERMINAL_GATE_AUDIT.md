# Independent audit of the isolated terminal-gate bounds

21 November 2026. This review concerns the new certificates in
`../charged-branches/`, on top of repository commit
`e2f3cba5e1e046e78fae853ca17ff54c2e8f8a72`. It does not claim to
exclude either complete tiling. The decisive geometric hypothesis is
the established **minimal odd population** `n_odd=3c`.

## 1. The previous forced-charge certificate still passes

I independently replayed the existing
`REMOTE_ZERO_MIN_43_IPM.json` through its polygon-based checker. All
22,188 integer inequalities passed, with maximum score `1,000,002`
and multiplier `3,115,886`. Both complete 143 projection controls
passed. Consequently the existing conclusion at 5063 is available:
under `n_odd=129`, at least one remote even terminal node is charged.
The replay does not exclude nonzero remote charges.

## 2. Why every other gate of a remote even class is closed

Use the path frame, where the minimal-mode theorem gives only heights
0, 1, 2 and a unique occupied height-one Euclidean class `zR`.

For a remote height-two class `L_r=rz+z^2R`, `r!=0`, its
increasing-tree node is terminal. Every upward long edge at height 3
therefore has a whole long-edge half-turn mate. For a downward long
edge, consider its decreasing-tree height-one edge node. All height-two
tiles have the same exterior-containing decreasing-tree parent. The
unique height-one child containing exterior edges is the native one;
all its other height-one children are exterior-free.

If a nonnative height-one child had a height-zero tile below it, the
occupied-parent/no-gap theorem would force that height-one node to be
occupied. This contradicts uniqueness of the occupied native height-one
node. Thus along a downward long-edge run in such a child there are no
height-zero or height-one suppliers. Both banks consist entirely of
length-`c` sides of height-two tiles. Their partitions begin and end
together and hence coincide whole side by whole side. The opposite tile
is the half-turn mate; reflection would have short height zero and
belong to the excluded subtree. Shared endpoints ensure that the mate
belongs to the same joint Euclidean class `L_r`.

The only possibly unpaired downward sides therefore have their endpoints
in the native class `zR`. The height-zero case is the conjugate argument:
only an upward gate to `zR` can be open. This proof uses absence in the
**actual complete tiling**, not absence of catalogue columns. Balanced
occupied even nodes are not declared empty.

## 3. The accessible residue is independent of the remote translation

Normalize a height-two tile by writing its beta endpoint as
`u=rz+z^2U`, with `U=x+y*rho` integral. Then

`u in zR` if and only if `zU in R`, because `r` is integral.

The two numerators of `zU` are `ax-by` and `bx+(a+b)y`. The norm
identity and invertibility of `a,b mod c` make their zero conditions
equivalent. Thus the accessible downward gate is exactly

`ax-by=0 mod c`.

For height zero, writing `u=rz+U` similarly gives the upward gate
`ay-bx=0 mod c`. Complex conjugation sends `U=(x,y)` to
`(x+y,-y)` and changes the hand. Its downward gate numerator is
`ax+(a+b)y`, congruent to `-a/b` times the original upward numerator.
Hence it maps precisely this open upward gate to the certificate's
open downward gate. The sign is reversed, which is harmless for the
absolute-charge result below.

## 4. Endpoint cancellation and the absolute charge

Each remote class has no exterior short-side contribution. Extend its
three periodic endpoint tables by zero outside that Euclidean class.
All selected short-edge contributions sum to zero: internal endpoint
differences telescope even at partial contacts, while a complementary
whole long side at the same height has displacement `c*rho^j` in
normalized coordinates. Its endpoints are either both outside the
class or both in the same residue, so it contributes zero. Other
short-height classes also contribute zero.

The complete selected population is a disjoint union of singles at the
accessible gate and whole half-turn pairs. The certificate's inequalities
therefore sum to `D*n >= t*G`. A local half-turn of all normalized
coordinates maps `q` to `-q`, `j` to `j+3`, preserves the zero gate
and pair relation, and reverses the sign. Applying the same inequalities
to these transformed columns gives `D*n >= -t*G`. No assertion that
the transformed patch fits the original board is needed: the column
inequalities cover every position. Thus

`D*n >= t*abs(G)`.

I replayed `verify_terminal_gate.py` with both exact certificates and
inspected its CCW polygons, gate recognition, half-turn placement, and
score summation. It imports no optimizer. For both hands it checks
the side norms and positive area. Pair charges cancel exactly, and all
permitted residues occur.

| Target | Exact ratio `t/D` | Single columns | Directed pair checks | Rounded population for `abs(G)=c` |
|---:|---:|---:|---:|---:|
| 3431 | `2093/506 = 91/22` | 222 | 16,428 | `5c = 185` |
| 5063 | `83/13` | 258 | 22,188 | `7c = 301` |

For 5063 and `abs(G)=2c`, the bound is `14c=602`.
The rounding uses separate divisibility of the positive and negative
node populations: `n/c` is an integer congruent to `G/c mod 2`.
It is not ordinary rounding to an arbitrary integer tile count.

## 5. Scope and remaining gap

The gate-isolation argument is valid for every remote even class in the
proved `3c` normal form. It must not be advertised as a theorem for
every terminal node of every unrestricted tiling: outside the minimal
mode, additional height-one parents or other heights can open further
gates.

At 5063 the old forced-charge theorem combined with this result proves
that some remote even node has at least 301 tiles. The odd 129-tile
population is disjoint from that node, giving at least 430 tiles in
those two sets; this remains far below 5063. Parent-bank tiles are
already counted among the odd 129 and cannot be added again. At 3431
a charged remote node has not been forced by the earlier certificate.
Both complete existence questions remain open.

## 6. Exact primal controls delimit the local relaxation

I also inspected and replayed `verify_periodic_primal.py` on the two
reduced witnesses. For each positive rational reduced column the code
lifts uniformly over all `c` points of its `psi` fibre; pairs are lifted
with the geometrically correct half-turn mate. It reconstructs the full
two-coordinate short-edge currents and verifies every row is exactly
zero, using `Fraction`. The populations are `3367/22` at 3431 and
`3569/13` at 5063, both with charge `c`; they meet their checked dual
values exactly. These are feasible fractional points of the same full
periodic endpoint relaxation. Thus the claimed optimality of `91/22`
and `83/13` for that relaxation is justified. The witnesses do not
supply integer finite placements or a boundary cancellation on real
supporting lines, so they establish no geometric tiling or completion.

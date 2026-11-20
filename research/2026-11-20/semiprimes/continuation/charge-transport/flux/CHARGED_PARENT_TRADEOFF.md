# Charged terminal nodes and the population reserved at their parents

20 November 2026. These are necessary conditions for complete positive
tilings of the 3431 and 5063 unit F2 boards. The nodes, charges, and
terminality refer to the actual complete tiling. A selected partial
packing or an auxiliary allocation is insufficient. The bounds do not
decide either target.

Use the canonical frame and notation of `SIGNED_CUT_TRANSPORT.md`:
`d=a-b`, the core has physical height zero, and

\[
 G_{\rm odd}=-c,\qquad G_{\rm even}=-d.
\]

Every ordinary exact node has separately divisible sign populations
`n_v^+,n_v^-` in `c Z`, and an occupied ordinary node has population
at least `2c`. We work in one prime tree at a time. Counts from the
two trees must not be added.

## 1. A unit charged terminal node reserves a signed parent population

Let `v` be a terminal occupied exterior-free node in the complete
tiling, with parent `p` and charge `G_v=sigma*c`, where `sigma=+1`
or `-1`. Terminal means that its proper descendant subtree contains
no tile. The signed transport formulas give

\[
 P_{p,v}=\sigma c,\qquad Q_{p,v}=\sigma d.             \tag{1}
\]

Thus at least `d` actual unmatched tiles of sign `sigma` belong to
the parent and carry its long-edge transport toward this child.
This is a statement about physical tiles: after cancellation of
whole long-edge half-turn mates, the remaining signed class still
has sum `sigma*d`. The fraction-of-edge bank argument in the main
note also realizes this signed amount on the physical contact.

Since `n_v/c` has the same parity as `G_v/c` and is at least two,

\[
 n_v\ge3c.                                            \tag{2}
\]

There is no inference here that a charged terminal node has population
at least `c^2`, or that its entire parent population is unmatched.

Suppose a parent has `r_+` positive and `r_-` negative unit charged
terminal children. A tile at the parent has only one long-edge node,
so the child classes are disjoint. Consequently

\[
 n_p^+\ge d r_+,\qquad n_p^-\ge d r_-.                 \tag{3}
\]

At an ordinary parent put

\[
 \ell_+=\left\lceil\frac{d r_+}{c}\right\rceil,
 \qquad
 \ell_-=\left\lceil\frac{d r_-}{c}\right\rceil.
\]

Signed rounding and occupancy imply

\[
 \boxed{n_p\ge c\max\{2,\ell_++\ell_-\}.}              \tag{4}
\]

If the actual parent charge is known to be `G_p=cz`, write
`n_p^+=cx`, `n_p^-=cy`. The constraints are
`x-y=z`, `x>=ell_+`, `y>=ell_-`, and `x+y>=2`. Eliminating `x`
gives the more precise necessary bound

\[
 \boxed{n_p\ge c K_p(z),\quad
 K_p(z)=z+2\max\left\{\ell_-,\ell_+-z,
                         \left\lceil\frac{2-z}{2}\right\rceil
                  \right\}.}                         \tag{5}
\]

The sum of signed outgoing classes at a node equals its charge.
Therefore parent tiles whose long-edge nodes are not among these
children have signed total

\[
 G_p-d(r_+-r_-).                                       \tag{6}
\]

They are distinct from the classes counted in (3), and supply at
least the absolute value of (6) additional unmatched tiles. This
can be inserted into the per-node rounding formula in the main
note. It is not a separate additive population cost when the sign
inventory already required by (5) covers those tiles.

For example, one positive child attached to a balanced ordinary
parent requires at least `d` positive parent tiles toward the child
and at least `d` negative parent tiles toward other nodes. Because
`0<d<c`, the already required population `(c,c)` covers both
reserves. No extra `2c` beyond that parent's ordinary `2c` minimum
has been proved in this example. A charged parent of charge `+/-c`
requires at least `3c` by parity, while a parent of charge `2c` is
not excluded from a monochromatic `2c` population by this argument.

If there are `r` such terminal nodes and `p` distinct ordinary
parents, their tile populations are disjoint: a parent with an
occupied child cannot itself be terminal. Thus, including the
fixed core residue population,

\[
 N\ge3cr+2cp+(r_+^{\rm core}+r_-^{\rm core}).          \tag{7}
\]

The stronger grouped values (4) or (5) may replace `2c` for any
parent whose data are known. Count a common parent once, and keep
this estimate within a single prime tree.

## 2. A core parent couples the reserve to the global even charge

The core residues and global even charge are

| Target | `(a,b,c)` | `d` | Core residues `(r_+,r_-)` | `delta=(d+r_+-r_-)/c` |
|---:|---:|---:|---:|---:|
| 3431 | `(33,7,37)` | 26 | `(19,8)` | 1 |
| 5063 | `(35,13,43)` | 22 | `(5,27)` | 0 |

Every non-core node at an even height has sign populations divisible
by `c`. The total even-height sign populations therefore have the
form

\[
 E_+=r_++cX,\qquad E_-=r_-+cY,
 \qquad X,Y\ge0,\qquad Y-X=\delta.                    \tag{8}
\]

Here the totals include the core excess and all other even nodes.
For a core with `r_+^{\rm child}` positive and `r_-^{\rm child}`
negative unit charged terminal children, (3) gives

\[
 r_++cX\ge d r_+^{\rm child},\qquad
 r_-+c(X+\delta)\ge d r_-^{\rm child}.                 \tag{9}
\]

The least nonnegative integer `X` satisfying these inequalities
gives the necessary even-population bound

\[
 E_++E_-\ge r_++r_-+c(2X+\delta).                      \tag{10}
\]

This is an aggregate bound. The correction forced by `G_even=-d`
need not occur entirely at the core.

With no child reserve, the smallest even inventories are `(19,45)`
at 3431 and `(5,27)` at 5063, of totals **64** and **32**. One
positive terminal child requires `d` positive core tiles. Since
`r_+<d` in both targets, `X` must increase by one; (8) forces `Y`
to increase by one as well. The even-population lower bounds then
increase by **`2c`**, to **138** and **118**. One negative terminal
child requires only `d` negative core tiles; the baseline inventories
already cover that reserve, so they give no such increase.

## 3. The outer height-two side supplies positive odd tiles outside the leaf

Assume now that the unit charged terminal node `v` is attached
directly to the core and is exterior-free. Its physical height is
1 in the increasing tree, or -1 in the conjugate tree.

Every outer side contains a whole long tile side. To see this, first
note that all three board angles are less than 120 degrees. The
angle at zero is 60 degrees, and at the other endpoints the cosine
formulas give values greater than `-1/2`. If an outer side consisted
only of `m` short tile sides, each would place its 120-degree vertex
at an endpoint. No such vertex can occur at either board corner;
and each of the `m-1` internal subdivision points can accommodate
at most one such obtuse angle. The resulting `m` required obtuse
vertices cannot fit. Partial contacts do not alter this count:
a tile side on a supporting line of the convex board lies wholly
on the board side.

Choose a long tile side on the outer height-two side. Its tile has
odd short height 1 or 3. The counterclockwise outer character there
is negative, and a tile's long-side character is `-c*epsilon`.
This tile therefore has `epsilon=+1`.

It does not belong to `v`. For a physical-height-1 child of the
core, such a long side would put the outer height-two edge node
in the child's descendant subtree, contrary to exterior-freeness.
For a physical-height-minus-one child, the supplier has a different
short height. Thus there is a positive odd tile outside the leaf.
All odd exact nodes are ordinary, and sign divisibility now yields

\[
 n_{\rm odd,outside}^{+}\ge c.                        \tag{11}
\]

This argument uses a real outer side and a real supplying tile.
It does not assume that the entire outer side consists of long
tile sides, or that every long side is wholly matched internally.

## 4. Target-specific costs for a core-attached unit charged leaf

If `G_v=+c`, the other odd nodes have total charge `-2c`, since the
global odd charge is `-c`. Equation (11) forces their negative
population to be at least `3c`, so their population is at least
`4c`. Together with (2),

\[
 n_{\rm odd}\ge n_v+4c\ge7c.                          \tag{12}
\]

If `G_v=-c`, the other odd nodes have charge zero. Equation (11)
forces at least `c` tiles of each sign, giving

\[
 n_{\rm odd}\ge n_v+2c\ge5c.                          \tag{13}
\]

Combine these with the even reserves from Section 2:

| Target | Leaf charge | Leaf minimum | Outside odd minimum | Even minimum | Necessary total |
|---:|---:|---:|---:|---:|---:|
| 3431 | `+c` | 111 | 148 | 138 | **397** |
| 3431 | `-c` | 111 | 74 | 64 | **249** |
| 5063 | `+c` | 129 | 172 | 118 | **419** |
| 5063 | `-c` | 129 | 86 | 32 | **247** |

If the actual leaf population exceeds `3c`, replace the leaf column
by that actual population; the corresponding outside-odd and even
lower bounds remain valid.

These are real population tradeoffs, not impossibility results.
In particular, a negative unit charged leaf can carry the global
odd defect while requiring only a relatively small additional
population. The abstract exterior-spine model in `../joint` has
no occupied exterior-free node at all, so it avoids these leaf
bounds. It remains an algebraic relaxation, not a geometric tiling.

## 5. Arithmetic replay and scope

Run

```sh
python3 verify_parent_tradeoff.py --out CHARGED_PARENT_REPLAY.json
```

The dependency-free checker verifies the target table, the even
reserve formulas, both leaf-sign costs, and (5) against direct
integer enumeration over a documented finite control range. It
also checks the board-angle inequalities used in Section 3. The
range comparison is a control of the formula, not a proof by
finite enumeration; the unrestricted derivation is given above.
It does not find a tiling, prove completeness of a partial packing,
or certify the impossibility of either target.

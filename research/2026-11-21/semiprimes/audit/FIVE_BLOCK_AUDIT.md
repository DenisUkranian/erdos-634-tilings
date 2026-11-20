# Independent review of the five-block height theorem

21 November 2026. I reviewed `../charged-branches/FIVE_BLOCK_SCOPE.md`,
including the argument forcing height one. The conclusion is sound
under the stated hypothesis `n_odd=5c`, for each of the two target
boards. It does not exclude that population or either complete tiling.
The frozen 5063 certificate index and certificates are not used or
changed by this additional structural argument.

Every odd exact node is ordinary, even if its subtree contains an
exterior node. The exceptional population residue belongs to an even
height in either frame. Hence every occupied odd node has at least
`2c` tiles, and five odd blocks allow at most two such nodes in either
single tree. Distinct physical heights are distinct nodes, so there
are at most two occupied odd heights. This does not add the two trees'
population budgets. If two odd heights occur, their populations are
`2c,3c`; each uses one exact node in each tree and consequently one
Euclidean class by the existing vertex-lattice intersection theorem.

The exterior long-side requirement is applicable: both target triangles
have all corners below 120 degrees, and a boundary side partitions into
whole tile sides. A side consisting entirely of short sides would need
more obtuse tile vertices than its internal partition points can hold.
The height-zero side therefore supplies odd height -1 or 1; a height-two
side supplies odd height 1 or 3.

An odd height at least 5 forces occupied height 3 through increasing-tree
parents, all above the highest exterior height. The independent base
supplier adds -1 or 1, a forbidden third odd height. The conjugate-tree
argument excludes odd heights at most -3. Any even height outside
`[-2,4]` then forces one of these excluded odd parents. The unbounded
height argument is complete; its validity does not depend on the small
finite arithmetic control in the accompanying script.

## Height one cannot be absent

The proof uses an already established upper median path, rather than
asserting a new uniqueness theorem about the full high/low interface.
A height-two step would have a height-one tile on its lower bank. Thus
absence of height one implies `K=0`. The median charge identities and
the total positive/negative odd populations `3c,2c` give
`-1<=t<=4`, while `K=0` and `gcd(c,d)=1` give `d|t`. Since
`d` is 22 or 26, `t=0`.

The lower and upper odd charges are consequently `-c,2c`. Regional
divisibility, sign parity and the `2c` positive-population minimum force
the odd populations to be exactly `3c,2c`. Each region has just one odd
height. The existing median path has only its endpoints on the base,
and its height-one edges cannot overlap an outer height-two side in
positive length. Actual long-side boundary suppliers therefore place
height -1 in the lower region and height 3 in the upper region. This
justifies `n_3=2c` with every height-three sign positive.

If a height-four node were occupied, it would be exterior-free and
terminal. Its immediate parent would be the unique occupied height-three
node. Bidirectional transport supplies at least one unmatched parent
tile; because all these parent signs are positive, its signed count
`Q` is strictly positive. Terminal transport gives `Q=dg` with integer
`g`, hence `Q>=d`.

The parent population is one Euclidean class and the child is one of
its upward gates. No outer side has height three, so the general gate
capacity applies without an exterior correction. It gives `Q<=43/3<26`
at 3431, or `Q<=16<22` at 5063. Thus no height-four node can occur.
The height-three node itself is now an exterior-free terminal node of
population `2c`, all of one sign, contradicting the existing terminal
balance theorem. This proves that height one is occupied.

The final allowed odd-height sets are exactly the three remaining
necessary alternatives `{1}`, `{-1,1}`, and `{1,3}`. Parent occupancy
then gives the stated short-height intervals `[-2,2]` or `[0,4]`,
and `{0,1,2}` if the only odd height is 1. Neither feasibility of these
alternatives nor a unique native height-one class is asserted.

All six relative links in the reviewed note resolve. No additional
placement search or full 5063 enumeration was needed for this review.

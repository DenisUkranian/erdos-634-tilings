# Joint cells of the two prime phase trees

20 November 2026. Necessary conditions for every tiling of the 3431 and
5063 boards. **Both target questions remain open.**

## 1. Intersecting the two prime partitions

Use the frame and signs of
[the signed phase theorem](../../vertex-phase/SIGNED_PHASE_POPULATIONS.md).
Thus `R=Z[rho]`, `z=(a+b rho)/c`, the short height is `h`, and
`epsilon=s*(-1)^j` for a placement `(q,h,j,s)`.

At a fixed physical height, intersect one node of the positive-valuation
tree with one node of the conjugate tree. Within `R[1/c]`, a nonempty
intersection is exactly one translate

\[
 L=q+z^hR.
\]

Indeed the difference, divided by `z^h`, is integral at both primes over
`c`. It is integral at every other Eisenstein prime because all tile
vertices belong to `R[1/c]`. The converse is immediate. Call this a
**joint cell**. This is a partition of the tiles of a fixed short height,
not an assertion that their union is geometrically connected.

Let `n_L^+,n_L^-` count the signs in the cell and put
`G_L=n_L^+-n_L^-`.

**Joint current theorem.**

\[
 G_L\equiv0\pmod c
\]

for every joint cell other than `h=0,L=R`. At that exceptional cell,

\[
 G_{0,R}\equiv-(a-b)\pmod c.
\]

To prove this, fix a maximal straight run of height `h`. Integral physical
offsets imply that every endpoint on it differs from any chosen endpoint
by an integer multiple of `z^h rho^j`. Thus the run has a single joint
edge cell, and its directed lengths cancel in that cell independently.
Short edges of the selected cell contribute `(a-b)G_L`; complementary
long edges contribute multiples of `c`. The height-two outer side has
length `c^2`. Both height-zero outer sides belong to the single joint
cell `R`, and their character is `A+B`, congruent to `N` modulo `c`.
Since `a-b` is invertible modulo `c` and `N+(a-b)^2=3c^2`, the claims
follow.

The same argument works separately on each short-edge supporting line,
not only after summing the three axes. The one-block line-incidence
argument in [LINE_COUNTS](../../../LINE_COUNTS.md)
therefore excludes an ordinary joint cell containing exactly `c` tiles:
its charge would force all `c` signs to agree, and the line-incidence
contradiction applies without requiring unsigned cell divisibility.

In particular,

\[
 |G_L|=c\quad\Longrightarrow\quad
 n_L\ge c+2\quad\hbox{and both signs occur in }L.       \tag{1}
\]

This theorem is stronger than the separate congruences on the two prime
partitions: divisibility of every row and column sum of a matrix does
not imply divisibility of its individual entries.

**No unsigned cell divisibility is asserted.** An unrestricted joint-cell
boundary involves three consecutive long heights. Their generated
lattice can have axial covolume one, so the two-height area argument
for an individual prime-tree cut cannot simply be reused here.

## 2. A reserve of balanced pairs in every ordinary node

Fix an ordinary node in either prime tree. Its opposite-prime nodes
partition it into joint cells. Write

\[
 n_v^+=cp,\quad n_v^-=cq,\quad
 g_L=G_L/c,\quad
 P=\sum_L\max(g_L,0),\quad Q=\sum_L\max(-g_L,0).
\]

Put `e_L=min(n_L^+,n_L^-)`. Then, exactly,

\[
 n_L^+=c\max(g_L,0)+e_L,\qquad
 n_L^-=c\max(-g_L,0)+e_L.
\]

Consequently `E=sum e_L` is a multiple of `c`, and

\[
 p=P+E/c,\qquad q=Q+E/c.                              \tag{2}
\]

Let `m` be the number of joint cells with `|g_L|=1`. By (1), each such
cell has `e_L>=1`, so

\[
 \boxed{p\ge P+\lceil m/c\rceil,\qquad
        q\ge Q+\lceil m/c\rceil.}                    \tag{3}
\]

Thus a node with at least one unit-charge cell must reserve at least
one additional block of **each** sign, beyond the positive and negative
variations of its cell charges. If its population is `kc`, then

\[
 m>0\quad\Longrightarrow\quad
 k\ge\sum_L|g_L|+2.                                  \tag{4}
\]

The reserve is counted in actual node populations. Costs from the two
prime partitions must still not be added together.

## 3. Consequences for the joint charge graph

At a fixed height form the bipartite graph of nonzero joint charges:
its two vertex sets are occupied nodes of the two prime trees, and an
edge is a cell with `G_L!=0`.

- A balanced node with `2c` tiles has no incident edge. A cell of charge
  `+c` would exhaust all `c` positives and contain no negatives, which
  is the excluded monochromatic `c`-cell; the negative case is identical.
- A monochromatic node with `2c` or `3c` tiles occupies just one joint
  cell. Every nonempty cell would have at least `2c` tiles, because a
  monochromatic cell has population a positive multiple of `c` and
  population `c` is excluded.
- Every ordinary node with total population `2c` or `3c` has charge-graph
  degree at most one. For `3c` with both signs, (4) allows only one
  charged cell, of charge `+c` or `-c`. For `2c`, the preceding cases
  are exhaustive.
- Hence every vertex of a joint charge-graph cycle has population at
  least `4c`. A cycle with `r` nodes in each prime partition demands
  at least `4cr` tiles at that height. In particular an ordinary
  four-cycle demands at least `8c` tiles. The height-zero exceptional
  core must be excluded when applying the ordinary-node assertion.

These are arithmetic and incidence restrictions. A graph cycle has not
been converted to a supported Euclidean `c`-mesh cycle, and the existing
geometric no-cycle theorem cannot yet be applied to it. This is the
remaining issue in using the joint graph to exclude an entire tiling.

The four-cycle bound is sharp for these arithmetic conditions alone.
Take the following matrix of `(positive,negative)` cell populations:

\[
 \begin{pmatrix}
 (c+1,1)&(c-1,2c-1)\\
 (c-1,2c-1)&(c+1,1)
 \end{pmatrix}.
\]

Its charges are `[[c,-c],[-c,c]]`. Every row and column has population
`(2c,2c)` and attains the reserve bound, while each unit-charge cell
contains both signs. The total is `8c`. This is an arithmetic example,
not a set of tile placements; excluding its geometric realization needs
an additional argument.

The known exact 143 control passes the joint-current identities. Its
standard-frame cells have `(n^+,n^-)=(18,20)` in the height-zero core
and `(49,56)` at height one.

## 4. Evidence and remaining obstruction

The proof uses the existing integral-offset and signed population theorems.
The finite checker preserves the exact known 143 tiling and verifies its
joint charges and both prime-node reserve inequalities. It does not
exhaust possible target matrices or formally verify the geometric input.

From this directory in the repository:

```sh
python3 verify_joint_cells.py ../..
```

The [native gate calculation](NATIVE_GATE_BOUND.md) additionally detects
transport inside a single Euclidean mesh. Its two-height and native-phase
hypotheses are additional restrictions and are not consequences of this
joint-cell theorem. The current obstacle is to connect joint charge
transport to unavoidable actual supported geometry, rather than only
node populations or a restricted phase model.

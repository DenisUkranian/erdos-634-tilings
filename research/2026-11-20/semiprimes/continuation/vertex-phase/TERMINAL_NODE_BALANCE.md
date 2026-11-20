# A minimal terminal phase node has both signs

20 November 2026. A conditional strengthening of the phase population
bounds for the unit F2 boards 3431 and 5063. It applies to arbitrary
tilings, including reflected tiles and T-junctions. It does not exclude
either board.

Use the normalization and sign convention of
[Signed phase populations](SIGNED_PHASE_POPULATIONS.md): a tile is
`(q,h,j,s)`, where `s=+1` or `-1`, its short height is `h`, its long
height is `h+s`, and its sign is `epsilon=s*(-1)^j`. Fix either prime
phase tree. An occupied node is **terminal** if no strict descendant
contains a tile at its exact short node. An **exterior-free** node is
one whose entire descendant subtree contains no outer-edge node.

**Theorem.** For either tile `(33,7,37)` or `(35,13,43)`, an
exterior-free terminal node with exactly `2c` tiles contains exactly
`c` positive and `c` negative tiles.

The terminal condition concerns the full tiling. The absence of
descendants in a finite search catalogue does not establish it.
In particular this theorem does not raise the unconditional ordinary
node minimum above `2c`.

## 1. A terminal node with one sign has only one hand

First choose the prime for which `z` has positive valuation, so
children have physical height one larger. Let `v` be a terminal node
at short height `h`. Consider a tile in `v` whose long height is
`h+1`. Its long-edge node is a child `w` of `v`.

Every tile meeting a positive-length interval of that edge has the
same height-`h+1` edge node `w`, by the integral-offset lemma. Its
short node can only be `w` itself or one of its adjacent nodes.
Terminality excludes `w` and all its children, leaving only `v`.
Exterior-freeness excludes an outer boundary interval in `w`.
Consequently every edge on either bank of the entire supporting run
is a length-`c` edge of a tile in `v`. The banks have common endpoints,
so their partitions into equal lengths `c` coincide.

The mate across the whole long edge is the half-turn of the first
tile. It has the same `h,s` and replaces `j` by `j+3`, which reverses
`epsilon`. A node with only one sign can therefore have no such
tile. All its tiles have `s=-1`.

For the conjugate prime tree, descendant heights decrease. The same
argument pairs every long-height-`h-1` edge and leaves only `s=+1`
in a node with one sign. Thus in either tree a terminal node with
one sign necessarily has a single hand as well.

## 2. The three families of supporting lines

We prove that an exterior-free node cannot have exactly `2c` tiles
which share both one sign and one hand. At fixed hand and sign only
three of the six rotations occur. After naming the three unoriented
axis families cyclically, every tile has its `a` edge on family `i`
and its `b` edge on family `i-1`, with indices modulo 3. Reversing the
hand reverses this cycle and does not change the argument.

Let `r_i` be the number of distinct supporting lines in family `i`
used by these short edges, and put `r=r_0+r_1+r_2`. On a particular
line let `M,L` count its `a,b` edges. Nodewise cancellation on each
maximal connected run gives

\[
 aM-bL\equiv0\pmod c.                                      \tag{1}
\]

Here the common sign makes all `a` contributions have one directed
sign and all `b` contributions the other. The complementary edges
have length `c`; there is no exterior contribution in this node.
Summing over the runs of the line gives (1), even if other phase
nodes use disconnected runs on that same infinite line. Also

\[
 \sum M=\sum L=2c.                                         \tag{2}
\]

For a fixed pair of lines from different families, the hand fixes
which is the `a` line and which is the `b` line. The two opposite
120-degree sectors then have opposite signs. Therefore at most one
tile of the chosen hand and sign can occupy that crossing. This
gives

\[
 2c\le r_0r_1+r_1r_2+r_2r_0\le\left\lfloor r^2/3\right\rfloor,
 \qquad M,L\le r-1.                                      \tag{3}
\]

More precisely, on a family-`i` line,
`M<=r_(i-1)` and `L<=r_(i+1)`. If `n_i` is the number of tiles whose
`a` edge has family `i`, the aggregate pair on that family is

\[
 \left(\sum_{i\text{-lines}}M,\sum_{i\text{-lines}}L\right)
   =(n_i,n_{i+1}).                                       \tag{4}
\]

The one-hand condition is essential in (3): with both hands, assigning
the `a` and `b` roles in the other order can give another tile with
the same sign at an unordered crossing.

## 3. The tile `(35,13,43)`

Equation (1) is equivalent to `8M+13L=0 (mod 43)`. Each used line
therefore has integers `t>=1,s` satisfying

\[
 8M+13L=43t,\qquad
 2M=t+13s,\qquad 2L=6t-8s.                              \tag{5}
\]

In particular `s=t (mod 2)`. Since `L>=0`,
`s<=3t/4<t`. Hence `s<=t-2`. Summing (5) and using (2) gives

\[
 \sum t=42,\qquad \sum s=10,\qquad r\le16.
\]

But (3) now says

\[
 86\le\lfloor16^2/3\rfloor=85,
\]

which is impossible.

## 4. The tile `(33,7,37)`

Equation (1) is equivalent to `11M+10L=0 (mod 37)`. On each used
line there are integers `t>=1,s` with

\[
 11M+10L=37t,\qquad
 2M=4t-10s,\qquad 2L=3t+11s.                            \tag{6}
\]

Again `s=t (mod 2)`. From `M>=0` we have `s<=2t/5<t`, and hence
`s<=t-2`. Equation (2) now gives

\[
 \sum t=42,\qquad \sum s=2,\qquad r\le20.               \tag{7}
\]

Thus `M,L<=19`. Neither entry can be zero: (1) would force the
other to be a positive multiple of 37. Also (1) is equivalent to
`L=10M (mod 37)`, and `L=1` would require `M=26 (mod 37)`, which
is unavailable. Every used line consequently has `M>=1,L>=2`.
The cyclic capacities imply that all three families occur and
`r_i>=2` for each `i`.

When `1<=M,L<=9`, the only possible pairs are

\[
 (M,L)=(4,3),(8,6).                                     \tag{8}
\]

If all `r_i<=9`, every line has the ratio `M/L=4/3`, contradicting
the equality of the two totals in (2).

There is therefore a family of size `R>=10`. It is unique, since
all three families have size at least 2 and `r<=20`. The other two
families each have size at most 8, so every line in the large family
has one of the pairs (8). Its aggregate `M+L` counts two disjoint
rotation classes and is at most 74. Each line contributes at least
7, so `R=10`; moreover all ten lines must have pair `(4,3)`, since
one `(8,6)` would increase the total from 70 to 77.

Call the large family 0. Equation (4) gives

\[
 (n_0,n_1,n_2)=(40,30,4).                               \tag{9}
\]

For family 2 the aggregate pair is therefore `(4,40)`. Its line
capacities are `M<=r_1<=8,L<=r_0=10`. In these ranges (1) permits
only `(1,10),(4,3),(8,6)`. To attain the aggregate `(4,40)` there
must be exactly four copies of `(1,10)`. Thus `r_2=4`.

For family 1 the capacities are now `M<=r_0=10,L<=r_2=4`.
The only permitted pair is `(4,3)`. But its aggregate `L` must be
`n_2=4`, which is not a multiple of 3. This is the final contradiction.

## 5. Consequence and scope

The [signed population congruences](SIGNED_PHASE_POPULATIONS.md)
give `n_v^+,n_v^-` separately divisible by `c` at an exterior-free
node. If `n_v=2c`, the possible sign inventories are
`(2c,0),(c,c),(0,2c)`. A terminal node with one sign would also have
one hand by Section 1, and Sections 3–4 exclude that possibility.
Its inventory is therefore exactly `(c,c)`.

Equivalently, an exterior-free node with exactly `2c` tiles and only
one sign must have an occupied strict descendant in either prime
tree. This is a restriction on completions, not a justification for
declaring a node terminal merely because its descendants have not
been enumerated. A node of population `3c` or more is not classified
by this argument.

The elementary numerical claims can be replayed with
`python3 verify_terminal_node_balance.py`. The checker verifies the
integer congruences and the small pair lists used above; the geometric
pairing and line-incidence arguments are proved in the text.

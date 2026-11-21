# An unrestricted odd-charge budget through physical phase gates

21 November 2026. Research continuation for the unit F2 board with
`(a,b,c)=(35,13,43)` and `N=5063`. **5063 and 3431 remain open.**

This note combines the signed charge of entire subtrees, the certified
capacity of their actual parent gates, and disjoint populations. Its
statements do not impose a height cutoff. It also explains exactly when
the previous 65-certificate exclusion remains valid in the presence of
additional odd-height tiles.

## 1. Frame and results

Use the path frame

\[
 R=\mathbb Z[\rho],\quad \rho=e^{i\pi/3},\quad
 z=(35+13\rho)/43,\quad d=a-b=22,
 \qquad T=\operatorname{conv}\{0,c^2,a(a+2b)z^2\}.
\]

The tile sign is `epsilon=s*(-1)^j` for the usual placement `(q,h,j,s)`.
The complete board has total odd charge `G_odd=c`. Positive and negative
populations at each ordinary exact node are separately divisible by `c`;
an occupied ordinary node has at least `2c` tiles. Every odd exact node
is ordinary, in either prime tree. These are the existing
[signed population results](../../../../2026-11-20/semiprimes/continuation/vertex-phase/SIGNED_PHASE_POPULATIONS.md),
transported by the isometry in
[the actual-median note](../../../../2026-11-20/semiprimes/continuation/charge-transport/geometry/ACTUAL_MEDIAN_CHARGES.md).

**Theorem A: a one-sign remote odd node has a global cost.**
If an exterior-free exact odd node in either prime tree contains exactly
`2c=86` tiles, all of one sign, then

\[
 \begin{array}{c|c}
 \text{sign of its 86 tiles}&\text{total odd population of the full board}\\
 +&n_{\rm odd}\ge7c=301\\
 -&n_{\rm odd}\ge9c=387.
 \end{array}                                                    \tag{1}
\]

The node need not be terminal. The populations in (1) are global,
including all phases and all physical heights.

**Theorem B: balanced extra branches cannot repair the old native mode.**
Suppose the *entire* height-one population consists of exactly 129 tiles
in the native Euclidean class `zR`, with exactly 86 positive and 43
negative signs. Then some upward child subtree and/or downward child
subtree of that class has nonzero odd charge. These disjoint off-middle
subtrees have total odd charge zero, so both charge signs occur. In fact

\[
 \boxed{n_{\rm odd}\ge9c=387.}                                  \tag{2}
\]

The sign inventory in this hypothesis is essential. Merely assuming
`n_1=129` in a larger tiling does not imply `G_1=+c`.

**Corollary C: one complete part of the five-block mode is excluded.**
A hypothetical tiling with `n_odd=215` cannot have `n_1=129`. In either
remaining two-odd-height alternative, the height-one population must
therefore be 86 and the other odd height must have 129 tiles. The
single-odd-height alternative still has `n_1=215`. This is a reduction
of the five-block mode, not its complete exclusion.

## 2. An exact node with 86 tiles of one sign is a single Euclidean class

The [joint-cell theorem](../../../../2026-11-20/semiprimes/continuation/common-obstruction/joint/JOINT_CELLS.md)
partitions an exact node into positioned Euclidean classes
`q+z^h R`. Each class at an odd height has signed population divisible
by `c`, and a class of exactly `c` tiles of one sign is impossible.

If all `2c` tiles of the exact node have the same sign, every nonempty
class therefore has a positive population which is a multiple of `c`.
The only possible division other than one class of size `2c` would be
two classes of size `c`; that division is excluded. Thus the full node
is a single Euclidean class. No unsigned divisibility theorem for a
general joint cell is being assumed.

The [two-block terminal balance theorem](../../../../2026-11-20/semiprimes/continuation/vertex-phase/TERMINAL_NODE_BALANCE.md)
shows that this one-sign exterior-free node is not terminal. Choose an
occupied descendant, then take the first child on its ancestor chain.
The occupied-ancestor and occupied-parent theorems ensure that this
child subtree is nonempty and that the parent crossing is a genuine
physical contact. The child remains exterior-free.

Let `Q` be the signed number of parent tiles whose long edge uses that
child gate. All such tiles have the parent's sign. The
[bidirectional-cut theorem](../../../../2026-11-20/semiprimes/continuation/charge-transport/flux/SIGNED_CUT_TRANSPORT.md)
therefore makes `Q` nonzero with that sign. All these parent tiles lie
in the single Euclidean class just proved. There is no exterior side
at its odd short height. The sign- and hand-symmetric
[gate-capacity theorem](../../../../2026-11-20/semiprimes/continuation/global-closure/median/NATIVE_GATE_CAPACITY.md)
gives

\[
 43|Q|\le8(2c)=688,
 \qquad 1\le|Q|\le16.                              \tag{3}
\]

The count in (3) is a count of actual parent-bank tiles, not an
independent abstract port capacity. Terminality of the child has not
been used.

## 3. Subtree charge and the proof of Theorem A

The child's physical height is even in either tree. For its complete
subtree `S`, put

\[
 G_{\rm even}(S)=c e,\qquad G_{\rm odd}(S)=c o,
 \qquad e,o\in\mathbb Z.
\]

It is exterior-free, so all its exact nodes are ordinary. The two
signed cut identities give

\[
 P=c e-d o,\qquad Q=d e-c o.
\]

In particular at 5063

\[
 \boxed{Q=22e-43o\equiv o\pmod{22}.}                \tag{4}
\]

All odd populations of the parent, `S`, and the remaining complement
are disjoint unions of ordinary exact nodes in this one tree. Their
separate sign counts are multiples of `c`. A union of odd nodes with
charge `k c` has population at least `c m(k)`, where the elementary
lower envelope is

\[
 m(0)=0,\qquad m(1)=m(-1)=3,\qquad
 m(k)=|k|\quad(|k|\ge2).                            \tag{5}
\]

For `k=+/-1`, the magnitude bound permits one block, but one occupied
ordinary node already requires at least two blocks; sign parity then
requires at least three. Formula (5) is a necessary lower bound, not a
claim that every such inventory has a geometric realization.

If the parent sign is `sigma in {+1,-1}`, total odd charge `c` yields

\[
 \frac{n_{\rm odd}}c
 \ \ge\ 2+m(o)+m(1-2\sigma-o).                      \tag{6}
\]

The geometrically permitted child currents must also satisfy (3)--(4).
These restrictions give minima 7 for `sigma=+1` and 9 for `sigma=-1`.
Here are short proofs which avoid any unbounded numerical search.

For a positive parent, suppose the total had at most five odd blocks.
The remaining odd tiles have charge `-c` and at most three blocks. A
child subset can then have odd charge only `o=0,-1,-2`: a positive
charge would require at least one positive block, but a `+c` union
needs three blocks, leaving no room to supply the remaining negative
charge. Equivalently, enumerate its nonnegative sign-block counts
bounded by the remaining `(1,2)` inventory, discarding a one-block
union. None of the residues `0,21,20` has a positive representative
between 1 and 16. This contradicts (3)--(4). Odd-block parity gives
`n_odd>=7c`.

For a negative parent, a total of at most seven odd blocks leaves at
most `(4,1)` positive/negative blocks elsewhere, with charge `3c`.
An allowed child union can have odd charge only `o=0,1,2,3,4`; charge
`-c` would require a forbidden one-block union because at most one
negative block remains. None of these residues has a negative
representative between -16 and -1 modulo 22. Thus `n_odd>=9c`.

The bounds are sharp only for this arithmetic relaxation. Examples
attaining its lower envelopes are `sigma=+1,e=2,o=1,Q=1` with seven
odd blocks, and `sigma=-1,e=-2,o=-1,Q=-1` with nine. They are not
positive tilings or realizable branch certificates.

This proof does not transfer the same numbers to 3431. There the
pure-sign gate capacity is at most 14, and `Q=26e-37o`. For example
`e=o=-1` gives positive `Q=11` with only five odd blocks; `e=4,o=3`
gives negative `Q=-7` with only five. These are arithmetic controls
showing why the claimed 301/387 thresholds are specific to 5063.

## 4. A general charge law at the native height-one class

Assume now the complete height-one population is the single native
class `zR`. In its own coordinates a tile's beta endpoint `u` gives
the upward gate `r=phi(u)=a u_y-bu_x mod c` and downward gate
`r=psi(u)=a u_x-bu_y mod c`. There are 43 gates of each hand. Denote
by `S_+(r)` its child subtree in the increasing-height prime tree and
by `S_-(r)` its child subtree in the decreasing-height tree.

Write the odd charges in these subtrees as

\[
 G_{\rm odd}(S_\pm(r))=c o_\pm(r).
\]

The even charge is a multiple of `c`, except that `S_+(0)` contains
the exceptional path-frame height-two core, with residue `d`. Thus
write it as `c e_-(r)` in the downward subtrees, and as
`d*[r=0]+c e_+(r)` in the upward subtrees. The exterior character of
`S_-(0)` is `c^2`, while that of `S_+(0)` is
`-(A+B)=-(2c^2-d^2)`, where `A=b(2a+b)` and `B=a(a+2b)`.
All other such subtrees have no exterior term.

For an even-root cut the general identity, with the exterior term
`b(S)` retained, is

\[
 Q=\frac{dG_{\rm even}(S)-cG_{\rm odd}(S)-b(S)}c.
\]

Consequently the actual parent gate currents satisfy

\[
\boxed{\begin{aligned}
 Q_+(r)&=2c\,[r=0]+d e_+(r)-c o_+(r),\\
 Q_-(r)&=-c\,[r=0]+d e_-(r)-c o_-(r).
\end{aligned}}                                                   \tag{7}
\]

These equations concern whole subtrees. Their even descendants may
be charged, and their contacts may have arbitrary T-junctions.
No statement that every neighbor is a terminal node is needed.

### Why the off-middle odd populations form a disjoint partition

In the increasing tree, a tile of odd height at least 3 has a
height-one ancestor. If that ancestor were exterior-free, the
occupied-ancestor theorem would force it occupied; if it contains
exterior edges, it is the unique native height-one exterior ancestor.
Since the sole occupied height-one node is native, its ancestor must
in either case be that native node. The tile therefore belongs to
exactly one of the upward child subtrees `S_+(r)`.

The conjugate-tree argument puts every odd-height tile at height at
most -1 in exactly one downward child subtree `S_-(r)`. Upward
subtrees have heights at least 2 and downward ones have heights at
most 0, so their odd populations are mutually disjoint even though
two different prime trees are used. They partition *all* odd tiles
outside height one.

Under Theorem B's sign hypothesis, `G_1=c=G_odd`. Hence

\[
 \sum_r o_+(r)+\sum_r o_-(r)=0.                      \tag{8}
\]

This conclusion uses the explicit `G_1=c` hypothesis. It is not
inferred from the number 129 alone.

## 5. Exact transfer of the 65 certificates

Suppose, towards contradiction, that every `o_+(r),o_-(r)` is zero.
The complete height-one population then has all the properties needed
by the previous [finite profile exclusion](../../MINIMAL_ODD_EXCLUSION_5063.md).
For clarity, the full list of transferred premises is:

| Premise of the finite profile proof | Reason it still holds |
|---|---|
| 129 height-one tiles in `zR`, signs `(86,43)` | Explicit hypothesis of Theorem B. |
| `Q_+(r)=86+22e_+(r)` at the native upward gate, `22e_+(r)` elsewhere; `Q_-(r)=-43+22e_-(r)` at the native downward gate, `22e_-(r)` elsewhere | Equation (7), with every off-middle odd subtree charge zero. |
| All `e` are integers | Signed divisibility at ordinary nodes and the unique even-core residue. |
| `sum e=0` | Sum all gate currents; each height-one tile occupies exactly one gate bin and the total signed population is 43. |
| Every positive gate current is at most 51, every negative current has magnitude at most 43 | The same global one-class gate capacity and the same total negative inventory. |
| Remote `e in {-1,0,1,2}`; positive units total at most 3, negative units at most 1 | Divide the current bounds and the disjoint positive/negative reserves by `d=22`. |
| Native upward `e in {-5,-4,-3,-2}`, native downward value fixed by total sum | The preceding current bounds and `sum e=0`, exactly as in the enumerator. |
| All-bin sign reserves `sum max(Q,0)<=86`, `sum max(-Q,0)<=43` | These bins are disjoint physical long-side classes of the same 129 tiles. |
| Zero total periodic endpoint weight and every translated/reflected/rotated dual inequality | No outer side has height one; long edges at height one have normalized displacement `43 rho^j`, giving zero endpoint weight. Tiles at all other heights add zero regardless of their populations or positions. |

The actual profile must therefore occur in the *same* fully enumerated
universe of 34,672,599 profiles, with 17,800,359 passing the sign
reserves. The 65 checked integer certificates leave zero survivors.
This is the previously completed proof, applied to an identical set
of necessary equations; it is not a new numerical infeasibility claim.

In particular, **the enumerator does not use terminal-node populations,
301-tile branch bounds, a finite total-height range, whole-edge pairing
at zero-current gates, or absence of extra odd tiles**. None of those
properties is transferred here. Direct inspection of
[`enumerate_profiles.cpp`](../../gate-model/enumerate_profiles.cpp)
and its [independent audit](../../audit/PROFILE_CUT_AUDIT.md) identifies
the exact current inequalities just listed.

Thus some off-middle `o` is nonzero. By (8), both charge signs occur.

## 6. Population consequence: why 301 total odd tiles are still insufficient

For each of the disjoint odd subtree populations, apply (5).
If nonzero integer charges sum to zero, their total forced population
is at least four blocks: if the total positive charge is one, both
signs cost at least three blocks each; if it is at least two, the
sum of absolute charges alone is at least four.

Hence Theorem B first gives `n_odd>=3c+4c=7c`. If equality held,
the off-middle odd population would have exactly four blocks. The
only way to attain four with nonzero balanced charges is one charge
`+2` population of two blocks and one charge `-2` population of two
blocks. Any unit charge would already cost three blocks on its sign.

Each of these two-block populations is a single occupied odd exact
node in its corresponding tree, because two occupied ordinary nodes
would require four blocks. The negative one consists of exactly `2c`
negative tiles. Its physical height is outside 1. At height at least
3 it is exterior-free in the increasing tree; at height at most -1 it
is exterior-free in the decreasing tree. Theorem A therefore forces
at least nine odd blocks in the *whole tiling*, contradicting seven.
Odd-block parity proves (2).

This argument only uses a four-block equality case to strengthen the
bound. It makes no claim that nine blocks can actually occur.

## 7. Full proof of the five-block localization needed for Corollary C

Assume `n_odd=5c` and `n_1=3c`. The established
[five-block height theorem](../../charged-branches/FIVE_BLOCK_SCOPE.md)
allows only odd-height sets `{1}`, `{-1,1}`, or `{1,3}`. The first is
inconsistent with `n_1=3c` and total `5c`. Thus there is exactly one
other odd height `k=-1` or `k=3`, with population `2c`.

At this other height there is one exact node in each tree: two
occupied nodes in one tree would each require at least `2c`. The
node is exterior-free in the increasing tree when `k=3`, and in
the decreasing tree when `k=-1`. Its sign inventories can only be
`(2c,0)`, `(c,c)`, or `(0,2c)`. Theorem A excludes both one-sign
options at a total of five odd blocks. The extra layer is therefore
balanced and the height-one layer has charge `+c` and signs `(2c,c)`.

The `3c` height-one tiles also occupy one exact node in each tree.
Their intersection is a single Euclidean translate `q+zR`, by the
joint-cell lattice theorem. We now prove `q+zR=zR`; this is not an
assumed native normal form.

Choose any actual vertex-simple upper median path and its genuinely
tiled lower polygon `D`. Its odd charge satisfies

\[
 G_{\rm odd}(D)=c(t-1),\qquad t\in\mathbb Z.
\]

Each of the two odd heights lies entirely on one side of this path:
otherwise both sides would contain at least `2c` tiles at that
height, exceeding its total of `2c` or `3c`. The extra height is
balanced, so the lower odd charge is either zero or `c` according to
whether `D` contains the height-one layer. Thus `t=1` or `2`.

The path's signed number `K` of height-two steps has the exact form

\[
 K=(c-d)t-dj_0,\qquad j_0\in\mathbb Z.
\]

If it were zero, coprimality of `c,d` would force `d|t`, impossible
for `d=22` and `t in {1,2}`. There is consequently a real height-two
path step. Its lower-bank tile has short height one, so `D` contains
the entire height-one layer, and `t=2`.

Every path vertex lies in `zR`: the path starts at zero and its
steps are `c z rho^j` or `c z^2 rho^j`, both in `zR`. A vertex of
the identified height-one bank tile is therefore in `zR`. All of
that tile's vertices, and hence the unique whole height-one class,
must be in `zR`. This proves the required native localization and
all sign hypotheses of Theorem B.

Theorem B now demands at least `9c` odd tiles, contradicting `5c`.
This proves Corollary C.

## 8. Remaining five-block alternatives and scope

The following necessary possibilities are left by this note:

| Odd short heights | Height-one population | Other odd population |
|---|---:|---:|
| `{1}` | 215 | 0 |
| `{-1,1}` | 86 | 129 at -1 |
| `{1,3}` | 86 | 129 at 3 |

The last two rows do not automatically have height-one charge `+c`.
A balanced 86-tile height-one class, for example, leaves odd charge
`+c` in the other layer, changing the offset currents in (7). Applying
the old 129-profile certificates directly to that situation would be
unjustified. Nothing here excludes every row of the table, all larger
odd populations, or the original count 5063. No corresponding full
profile exclusion is available for 3431.

## 9. Replay

Run from the repository root:

```sh
python3 research/2026-11-21/semiprimes/global-closure-next/large-population/verify_odd_branch_budget.py
```

The standard-library checker verifies the exact gate bounds, all
sign-block allocations below the two thresholds, the residue
contradictions, equality controls for the retained arithmetic model,
the native-cut offsets, the finite-profile counting parameters, and
the four-block equality case. It also checks the recorded hashes and
accounting of the existing 65-certificate proof. It does not rerun a
numerical optimizer or infer an unrestricted theorem from a finite
height enumeration. The geometric arguments are proved above; the
previous exact certificate package remains an explicit dependency.

The separate [internal mathematical audit](LARGE_POPULATION_AUDIT.md)
reviews the geometric transfer and reports an independent run of the
arithmetic checker. It does not constitute external peer review or
proof-assistant formalization.

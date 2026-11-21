# At five odd blocks, 5063 has only short heights 0, 1 and 2

21 November 2026. This continuation excludes **both** two-odd-height
alternatives in the five-block mode. **The original count 5063 remains
open**, as does 3431.

## 1. Statement

Use the path frame for `(a,b,c)=(35,13,43)`, with

\[
 d=22,\quad \rho=e^{i\pi/3},\quad R=\mathbb Z[\rho],\quad
 z=(35+13\rho)/43,\qquad
 T=\operatorname{conv}\{0,c^2,a(a+2b)z^2\}.
\]

Signs are `epsilon=s*(-1)^j`, and the complete board's odd charge is
`G_odd=c`. Let `n_h` denote the entire population at physical short
height `h`, over all phases and both hands.

**Theorem.** If a complete positive 5063 tiling satisfies
`n_odd=215=5c`, then

\[
 \boxed{n_1=215,\qquad n_h=0\text{ at every other odd height}.}     \tag{1}
\]

Consequently all its short heights lie in `{0,1,2}`. In each prime tree
there are at most two occupied height-one exact nodes, hence at most
four occupied height-one Euclidean classes. A unique native height-one
class is **not** asserted.

The prior
[five-block height theorem](../../charged-branches/FIVE_BLOCK_SCOPE.md)
and [odd-branch budget](../large-population/GLOBAL_ODD_BRANCH_BUDGET.md)
leave, before this note, precisely the possibilities

* `n_1=215`;
* `n_1=86` and `n_{-1}=129`;
* `n_1=86` and `n_3=129`.

We exclude the last two with a new geometric reduction and a complete
finite exclusion of **9,112,001** integer profiles. This exclusion
reuses the previously independently checked 65 endpoint certificates;
it does not use a numerical solver's infeasibility verdict.

## 2. In either two-height alternative, the 86-tile middle is balanced

Assume `n_1=2c` and `n_k=3c`, where `k=-1` or `3`. Each of these
layers occupies exactly one node in each prime tree, since every
occupied ordinary odd node has at least `2c` tiles. Each layer is
therefore a single Euclidean translate of its short-height lattice.
Its sign counts are separately multiples of `c`.

Suppose the height-one layer is monochromatic, with sign
`sigma in {+1,-1}`. Its charge is `2 sigma c`, so the other layer's
charge is

\[
 G_k=c(1-2\sigma).
\]

The [global one-sign two-block theorem](../large-population/GLOBAL_ODD_BRANCH_BUDGET.md)
requires at least seven or nine total odd blocks if either exact node
of this layer is exterior-free. There are only five. Its exact nodes
in **both** trees are consequently exterior-containing. At physical
height one, the intersection of the two exterior ancestor chains is
exactly the native class `zR`, by the
[two-tree exterior-chain classification](../../../../2026-11-20/semiprimes/continuation/global-closure/spine/SPINE_DICHOTOMY.md)
and the standard-to-path isometry.

For each upward or downward child gate of that native class, the
full-subtree identity is

\[
 Q_+(r)=2c\,[r=0]+d e_+(r)-c o_+(r),\qquad
 Q_-(r)=-c\,[r=0]+d e_-(r)-c o_-(r),                 \tag{2}
\]

where `c o` is the subtree's total odd charge and `e` is an integer
with the even-core residue subtracted when necessary. Formula (2)
is proved, with its exterior terms, in the
[odd-branch budget](../large-population/GLOBAL_ODD_BRANCH_BUDGET.md).
It does not require the middle charge to be `+c`; that hypothesis is
needed only for the zero-sum consequence elsewhere in that note.

Every child subtree contains either the entire other odd layer or
none of it. The middle layer itself is at the parent height and is
not selected by any such child cut. Thus

\[
 o_\pm(r)\in\{0,1-2\sigma\}.                       \tag{3}
\]

For a remote gate `r!=0`, (2) gives

\[
 Q_\pm(r)\equiv o_\pm(r)\pmod{22}.                 \tag{4}
\]

There are no opposite signs in the parent class, so a nonempty gate
has current of sign `sigma` and magnitude equal to its tile count.
The sign-symmetric physical gate capacity gives `1<=|Q|<=16`.

* If `sigma=+1`, the residues in (3)--(4) are `0` and `-1=21 mod22`.
  Neither has a positive representative in `[1,16]`.
* If `sigma=-1`, the residues are `0` and `3`. Neither has a negative
  representative in `[-16,-1]` modulo22.

Every remote gate is therefore empty. The two native gates each
contain at most 16 tiles by the same capacity inequality, while every
height-one tile uses exactly one gate. This would give
`86<=16+16=32`, a contradiction.

The 86-tile middle is balanced. Its signs are `(c,c)`, and the other
129-tile layer consequently has charge `+c` and signs `(2c,c)`.
This argument uses actual gate populations; a zero current becomes an
empty gate here only because the entire parent layer has one sign.

## 3. The balanced middle is also forced to be native

Choose any actual vertex-simple upper median path and its genuinely
tiled lower polygon `D`. At each of the two odd heights, a positive
population on either side of this path is at least `2c`. Since the
whole layer has `2c` or `3c` tiles, neither layer can be split between
the two sides.

The middle is balanced and the other layer has charge `+c`, so
`G_odd(D)` is either zero or `c`. The exact median identity gives

\[
 G_{\rm odd}(D)=c(t-1),\qquad t\in\{1,2\}.
\]

Its signed height-two step count has the form

\[
 K=(c-d)t-dj_0,\qquad j_0\in\mathbb Z.
\]

If `K=0`, coprimality of `c,d` would force `d|t`, which is impossible
for `d=22` and `t=1,2`. A height-two path step therefore exists. Its
lower-bank tile has short height one, so the entire middle layer is
below the path. Every path vertex lies in `zR`, since the path starts
at zero and has steps `c z rho^j` or `c z^2 rho^j`. The identified
bank tile anchors the unique middle Euclidean class to `zR`.

Thus the two alternatives have a balanced native 86-tile middle and
one other 129-tile class of odd charge `+c`. We do **not** transfer the
old two-offset profile equations to that other class without deriving
its different exterior terms.

## 4. The charged outer class has exactly one exterior gate

Let `L=q+z^kR`, `k=-1` or `3`, be the other odd class. Its entire
129-tile layer is one exact node in each tree. Normalize its coordinates
by choosing an origin in `L` and dividing by `z^k`. Each tile becomes
one of the same integral residue columns used by the old endpoint
certificates, with the same sign `epsilon`.

Every upward or downward child subtree of this class has **zero odd
charge**. Its own odd layer is at the parent level and is excluded by
the cut. The only other odd layer is the balanced middle, which enters
a subtree as a whole exact node or not at all.

Suppose both exact nodes of `L` were exterior-free. Then all their
child subtrees would be exterior-free, all even charges in them would
be multiples of `c`, and exact signed cut transport would give
`Q=d e` at every gate. Summing all disjoint long-side gate currents
would make the class charge `c=43` divisible by `d=22`, impossible.
Thus at least one of its exact nodes is exterior-containing.

At height 3 the increasing-tree node is necessarily exterior-free:
all outer heights are 0 and 2. Its conjugate-tree node must therefore
be on the exterior ancestor chain. Because 3 is above *all* outer
heights, precisely one of its downward children contains all three
outer sides. At height -1 the symmetric argument leaves precisely one
upward child containing all three outer sides. Every other gate's
child subtree is exterior-free. The fact that the exterior nodes form
one chain in each tree is the cited exterior-chain theorem, not an
assumption about a finite placement catalogue.

The complete outer character in this frame is

\[
 b(T)=c^2-[A+B]=-3ab=-1365,
 \qquad A+B=2c^2-d^2.
\]

The unique exterior-containing child includes the exceptional even
core, whose signed population residue is `d`; its even charge is
`d+c e`. Its odd charge is zero. Hence the general even-root cut
identity gives

\[
 Q=\frac{dG_{\rm even}-cG_{\rm odd}-b(S)}c
   =\frac{d(d+c e)+3ab}{c}
   =c+d e,                                         \tag{5}
\]

using `d^2+3ab=c^2`. At every other gate the same equation gives
`Q=d e`.

Reflection `w -> -conjugate(w)` in normalized coordinates exchanges
the two hands and preserves `epsilon`. A change of origin within
`R` can place the distinguished gate at residue zero. Thus both
physical height alternatives reduce to a common necessary profile:

\[
 \boxed{Q_+(0)=43+22e_0,\qquad Q_g=22e_g
        \text{ at all other 85 gates},\qquad \sum_g e_g=0.}       \tag{6}
\]

The residue shift is a change of labels and endpoint potentials. It
does not assert that a shifted tiling fits the original board.

## 5. The entire single-offset profile universe

The class has signs `(86,43)`. The already certified single-gate
positive capacity is 51, and no negative current exceeds magnitude
43. Consequently every ordinary gate has

\[
 e_g\in\{-1,0,1,2\}.
\]

Disjoint gate bins give total ordinary positive units at most three
and ordinary negative units at most one. Write these totals as `p,m`.
Each ordinary net vector is uniquely represented by a sorted multiset
of `p` positive indices, at most two copies per index, and either no
negative index or one negative index outside that multiset. There are
85 ordinary indices; **the opposite hand's residue-zero gate is an
ordinary index**, not a second distinguished gate.

The distinguished charge is forced by (6): `e_0=m-p`. Its current is
`43+22(m-p)`. The allowed rows and their exact counts are:

| `p` | `m` | Distinguished current | Number of profiles |
|---:|---:|---:|---:|
| 0 | 0 | 43 | 1 |
| 1 | 0 | 21 | 85 |
| 1 | 1 | 43 | 7,140 |
| 2 | 0 | -1 | 3,655 |
| 2 | 1 | 21 | 303,450 |
| 3 | 0 | -23 | 105,910 |
| 3 | 1 | -1 | 8,691,760 |
| **Total** | | | **9,112,001** |

For `p` positive units on `k` distinct ordinary gates, the number is

\[
 \binom{85}{k}\binom{k}{p-k}(85-k)^m,
 \qquad k\le p\le2k.
\]

Summing gives the displayed counts. The excluded row `p=0,m=1`
would have distinguished current 65, exceeding capacity 51. All
listed rows satisfy the aggregate sign reserves: positive current at
most 86 and negative magnitude at most 43. This is an exhaustive
finite containing universe for every actual class under (6).

## 6. Exact exclusion using the existing endpoint certificates

The previous [65-certificate index](../../gate-model/CERTIFICATES_5063.json)
supplies endpoint tables and gate weights whose universal integer
column inequalities are

\[
 W(\tau)+\epsilon(\tau)\lambda_{s(\tau)}(r(\tau))\le D.
\]

The [independent verifier](../../audit/verify_profile_duals.py)
checks all 22,188 single-tile residue classes for each certificate,
including both hands and all integral translations. At the selected
odd height, no outer edge has that short height. Endpoint weights
therefore telescope to zero over the whole tiling; complementary
long edges at that height have displacement `43 rho^j` in the
normalized class and contribute zero. Other Euclidean classes are
assigned zero weights. These assertions are unchanged when the class
has height -1 or 3 or an arbitrary permitted translation.

Every physical 129-tile class in question must consequently satisfy
all 780 transformed cuts, including their independent residue shifts:

\[
 \max_u\sum_r Q_+(r)\lambda_+(r+u)
 +\max_v\sum_r Q_-(r)\lambda_-(r+v)\le129D.          \tag{7}
\]

The new enumerator `enumerate_single_offset.cpp` tests (7) on the
complete universe in Section 5. Its complete execution reports

\[
 \boxed{\text{profiles visited}=9,112,001,\qquad
        \text{profiles satisfying every cut}=0.}
\]

No new floating optimization is needed: the already checked universal
column inequalities apply to this newly proved profile universe.
The geometric source of the offset is different from the earlier
`(+86,-43)` native model, which is why a new full enumeration is
required and supplied here.

Thus the charged 129-tile class from either two-height alternative
cannot exist, proving (1).

## 7. The remaining five-block problem

With only odd height one occupied, an even short height at least four
would have an exterior-free increasing-tree node whose occupied parent
has absent odd height at least three. An even short height at most -2
would similarly force absent odd height at most -1 in the conjugate
tree. Therefore all short heights are 0, 1 and 2.

At height one, each occupied exact node consumes at least `2c`, so
215 tiles permit at most two nodes in either tree. Intersecting the
two node partitions gives at most four Euclidean classes. The possible
exact-node population partitions remain `(5)` or `(2,3)` in units
of 43. A nonnative two-block node is balanced by the preceding global
odd-node theorem, but that alone does not classify the full joint
2-by-2 population matrix.

In particular, a charged Euclidean cell may share an exact node with
another balanced cell. Its separate current cannot then be substituted
for the whole-node current in a phase-cut identity. Neither deleting
that balanced cell nor automatically applying the old 129-profile
proof to the remaining cell is justified.

The single-height 215 mode, all larger allowed odd populations, and
the original count 5063 remain undecided by this note. The proof also
does not decide 3431.

## 8. Reproduction and verification boundary

Run from the repository root:

```sh
python3 research/2026-11-21/semiprimes/global-closure-next/five-block-two-heights/replay_single_offset.py
```

The replay rechecks all 65 integer certificate files and 780 transforms,
compiles the new C++17 enumerator, compares its complete accepted sets
with an independently written Cartesian enumeration on small controls,
and reruns all 9,112,001 profiles. It requires Python's standard library
and a C++17 compiler, not SciPy or an optimizer. `--saved-enumeration`
uses the saved complete run and explicitly records that distinction.

The geometric transfer, especially the sign-sensitive monochromatic
middle exclusion and the unique whole-boundary gate, is part of the
written proof. Finite arithmetic controls do not replace those
arguments or establish a proof-assistant formalization.

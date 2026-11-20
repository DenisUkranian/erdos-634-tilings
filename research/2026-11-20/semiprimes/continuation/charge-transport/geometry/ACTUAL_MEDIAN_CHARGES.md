# Actual median cuts and the minimal odd population

20 November 2026. This note concerns complete positive tilings of the two
unit F2 targets. It proves a charge-separation identity and conditional
structure when the total odd-height population is `3c`. It does **not**
exclude that population, establish a global `5c` bound, or decide either
target.

The identities are tested on two complete positive 143 tilings. A separate
exact two-tile corner packing records why a proposed boundary shortcut
fails. The corner packing is not a full target tiling.

## 1. Frame and inputs

Use the path frame of the project's `paths/TWO_PATHS.md`:

\[
 \rho=e^{i\pi/3},\qquad z=(a+b\rho)/c,\qquad d=a-b,
 \qquad (O,B,C)=(0,c^2,a(a+2b)z^2).
\]

The base has height 0 and the other two sides have height 2. For a
placement `(q,h,j,s)`, the obtuse vertex is `q`, the other vertices are
`q-a*z^h*rho^j` and `q+b*z^h*rho^(j+s)`, and
`epsilon=s*(-1)^j`. In this frame the total odd and even characters are

\[
 G_{\rm odd}=c,\qquad G_{\rm even}=d.                 \tag{1}
\]

The sign in (1) is deliberate: the standard frame used by the
`vertex-phase` package has `G_odd=-c`. Its isometry to this frame is

\[
 F(x)=a(a+2b)z^2-\rho z^2\overline{x}.
\]

It maps `(h,j,s)` to `(2-h,4-j,-s)`, reversing `epsilon` and preserving
height parity.

We use the following already proved inputs, without a finite placement
catalogue:

* The whole-edge upper median path and its genuine tiled lower polygon,
  from `paths/TWO_PATHS.md`.
* The two segment characters and upper-path congruences, from
  `paths/UPPER_RIGIDITY.md` and `cycles/LONG_EDGE_PAIRS.md`.
* At every odd height, on either side of an actual upper median cut,
  a positive population is a multiple of `c` and at least `2c`.
  Lower-side divisibility is in `TWO_PATHS.md`; upper-side divisibility
  follows by subtraction from the board, and the same per-line
  single-block exclusion applies. The exceptional outer height 2 is even.
* In either prime tree, an ordinary occupied exact node has population
  at least `2c`; the intersection of the two exact nodes at height `h`,
  among the global vertex coordinates in `R[1/c]`, is a Euclidean
  translate of `z^h R`. Here `R=Z[rho]`. These are the phase-population
  and joint-cell statements.
* For these two targets, a nonempty exterior-free subtree has an
  occupied immediate parent. This is the bidirectional-cut theorem
  in `../flux/SIGNED_CUT_TRANSPORT.md`, using the supported pure-cycle
  exclusion. Merely allowing an empty exterior-containing ancestor
  would not give this last conclusion.

## 2. The exact odd-charge split

Choose any vertex-simple upper median path, including one after actual
long-edge half-turn pairs have been cancelled. Orient it from `O` to `B`.
It has whole length-`c` steps at heights 1 and 2. Let `J,K` be their
respective signed direction counts, each step of heading `z^h*rho^j`
contributing `(-1)^j`.

Let `D` be the genuine tiled polygon between this path and the base,
and let `E` be the entire upper remainder. The positive boundary of
`D` is the base followed by the reversed path. Its ordinary and
height-alternating characters are

\[
 C(\partial D)=c^2-c(J+K),\qquad
 C_*(\partial D)=c^2+c(J-K).
\]

Since each tile contributes `(d-c)*epsilon` and
`(d+c)*(-1)^h*epsilon`, respectively, write the usual congruences as

\[
 J+K=d+(c-d)i,\qquad J-K=d+(c+d)j_0,
 \qquad t=(i-j_0)/2\in\mathbb Z.                     \tag{2}
\]

The integer parity follows because `c-d,c+d` are odd and the two
left sides have equal parity. Direct division gives

\[
 G(D)=c(i-1),\qquad G_*(D)=c(j_0+1).
\]

Consequently

\[
 \boxed{G_{\rm odd}(D)=c(t-1),\qquad
        G_{\rm odd}(E)=c(2-t).}                     \tag{3}
\]

Also `G_even(D)=c(j_0+t)`. These are actual charges of tiled regions,
not merely charges of an open path inventory.

For a canonical shortest path, `J=d,K=0,i=j_0=t=0`. It therefore
separates odd charges `-c` below and `+2c` above. A general upper
median path is not required to have `t=0`.

## 3. Conditional structure at total odd population `3c`

**Theorem.** Suppose either target has a complete tiling with exactly
`3c` tiles of odd short height. In the path frame:

1. Every upper median path has `t=2`.
2. All odd-height tiles have height 1 and lie below every such path.
3. All these height-1 tiles belong to the single Euclidean translate
   `zR`; their sign populations are `2c` positive and `c` negative.
4. No short height outside `0,1,2` occurs.
5. The upper remainder of each upper median path contains only
   short-height-2 tiles, all in the native Euclidean translate `z^2 R`.
6. Height 0 must occur somewhere in the board.

These conclusions leave possible height-zero tiles and height-two
islands below the median path. They do not reduce the whole tiling to
the two-height hypothesis of `SUPERLINEAR.md`.

### Proof of 1 and 2

If both sides of the cut contained odd-height tiles, each side would
contain at least `2c` such tiles. Their sum would exceed `3c`.
Hence one side contains no odd-height tile. Formula (3) forces
`t=1` or `t=2`.

There must be a height-2 step on the path. Indeed (2) gives

\[
 K=(c-d)t-dj_0.
\]

If `K=0`, then `d` divides `t`, since `gcd(c,d)=1`. But `d=26` or
`22`, while `t` is 1 or 2. Thus `K` is nonzero. A height-2 upper-path
step has a short-height-1 bank tile on the lower side. The lower
side consequently contains odd tiles; all odd tiles lie there, and
(3) forces `t=2`.

Since each occupied odd height in the board contains at least `2c`
tiles, the total `3c` permits only one odd height. The bank tile just
identified proves that height is 1.

### Proof of 3, including the native-translate assertion

All height-1 nodes are ordinary. In either prime tree, a positive exact
node consumes at least `2c` tiles. Thus the `3c` height-1 tiles occupy
one exact node in each tree. Their common vertices belong to the
intersection, which is one translate `q+zR` by the joint-cell theorem.
This uses the previously proved global vertex-lattice inclusion;
it would not follow from two arbitrary unrelated p-adic cosets.

Every upper-path vertex belongs to `zR`. The path starts at zero,
and its step vectors are `c*z*rho^j` or `c*z^2*rho^j`; both belong
to `zR`, since `c*z=a+b*rho` is in `R`. On the height-2 step found
above, a vertex of the height-1 bank tile is therefore in `zR`.
Its obtuse vertex differs from that vertex by an element of `zR`.
The translate `q+zR` must be `zR` itself.

Finally (1) and the total population give `n_1^+=2c,n_1^-=c`.
In the standard frame the corresponding translate is
`b(2a+b)+zR`, not the unshifted `zR`.

### Proof of 4

There are no odd heights except 1. If an even height `h>=4` were
occupied, its exact node in the increasing-physical-height tree would
be exterior-free: the outer heights are only 0 and 2. The occupied-
parent conclusion would require tiles at the absent odd height `h-1`.
For an even `h<=-2`, use the conjugate tree instead; its required
parent has physical height `h+1`, again an absent odd height. These
contradictions leave only heights `0,1,2`.

### Proof of 5

The upper remainder has no odd tiles and therefore only heights 0
and 2. Select all its height-zero tiles. Their short-height-zero
edges cancel internally: the upper remainder has boundary heights
1 and 2 only, and no height-1 tile lies within that remainder to
supply a long-height-zero contact.

The selected long-height-minus-one edges are whole half-turn pairs.
Globally only height-zero tiles can meet these runs; the other possible
short heights `-1,-2` are absent. The upper remainder has no boundary
at height minus one, so both members of each such pair are selected.
After these cancellations, the positive boundary of the selected
union is a whole-`c` chain at height 1. If the selection were nonempty,
its positive area would yield a supported simple pure-height `c`
cycle, contradicting the target cycle theorem. No height-zero tile
therefore occurs in the upper remainder.

To prove the final lattice assertion without assuming convexity of the
remainder, use the following elementary anchoring lemma.

**Boundary-vertex anchoring lemma.** Suppose a polygonal region has a
finite positive tiling by triangles. If all its polygon vertices lie
in a positioned lattice `L` and every directed tile-edge vector lies
in the additive group of `L`, then all tile vertices lie in `L`.
Multiple components and reflex polygon vertices are allowed.

Join tiles when they share a corner, and fix one connected component
of this graph. Choose a linear functional with distinct values on all distinct
vertices of the tiling, and maximize it over the finitely many vertices
of this component. Let the maximizing vertex be `v`. All rays from `v`
to another corner of a tile in the component lie strictly in the
functional's decreasing half-plane. The total angle occupied by the
component at `v` is consequently strictly less than pi.

If `v` were not a polygon vertex, the region would locally have angle
pi or `2*pi`. Every incident tile having a corner at `v` belongs to
the chosen component. At most one other incident tile can have `v`
strictly inside one of its edges: two such half-plane sectors would
leave no positive angle for the selected tiles. Thus at an interior
point the chosen component occupies angle pi or `2*pi`, and at a
smooth boundary point it occupies angle pi. Each case contradicts
the strict half-plane conclusion. Hence `v` is a polygon vertex in
`L`. Edge vectors and shared corners propagate lattice membership
through its entire graph component. Apply this argument to every
component. For a remainder with touching polygonal components, apply
it to each open component; every non-smooth boundary point is among
the designated polygon vertices.

For the upper remainder, designate every path/outer-arc contact as a
polygon vertex; contacts ending a coincident boundary segment are path
vertices as well. Each resulting polygon vertex is a board vertex or an
upper-path vertex. All of them lie in `z^2 R`: the step vectors divided
by `z^2` are `c/z` times a unit or `c` times a unit, and
`c/z=a+b-b*rho` belongs to `R`. The board vertices satisfy the same
claim. Every short-height-2 tile-edge vector belongs to `z^2 R`,
including its long vector, which is a difference of its short vectors.
The anchoring lemma proves that every tile in the upper remainder is
in the native translate `z^2 R`.

This argument is about this particular upper remainder. It does not
justify discarding height-zero tiles from the lower polygon or the
entire board, or locating all height-two islands below the path in
the same translate.

### Proof of 6

If height 0 were absent, the complete tiling would use only heights 1
and 2. The established physical-line certificate in `SUPERLINEAR.md`
requires at least `8c` tiles at height 1 on either target (and at
least `9c` after the two-height parity). This contradicts `n_1=3c`.
Thus height zero is unavoidable in the hypothetical minimal case.

## 4. Base gaps and the missing boundary chain

Under the conditional theorem, every height-1 long edge on the base
has both endpoints in `zR` on the real axis. Primitivity gives

\[
 zR\cap\mathbb R=c\mathbb Z.
\]

Each connected base gap between these length-`c` edges has length
`kc` and is covered entirely by height-zero short edges. Therefore

\[
 am+bn=kc,\qquad m,n\in\mathbb Z_{\ge0}.              \tag{4}
\]

The first nonzero possibilities are:

| Tile | Minimum positive `k` | First short-edge partition |
|---|---:|---|
| `(33,7,37)` | 4 | `3a+7b=4c` |
| `(35,13,43)` | 6 | `7a+b=6c` |

These are arithmetic necessities, not constructions of filled gaps.
If there are `r` long base teeth, their signs are all negative, and
there are exactly `c-r` negative height-1 tiles left off the base.
The total gap length is also `c(c-r)`.

Let `U_0` be the union of **all** height-zero tiles, `Gamma_base` the
whole oriented base, `L_01` the whole CCW long-edge chain of the
height-zero tiles whose long height is 1, and `L_10` the corresponding
chain of the height-one tiles whose long height is 0. Cancellation
on the height-zero runs gives

\[
 \boxed{\partial U_0-\Gamma_{\rm base}=L_{01}-L_{10}.} \tag{5}
\]

The two remaining alphabets have heights 1 and 0. An internal
height-zero short edge of `U_0` can meet an internal long-height-zero
edge of a height-one tile. Such a term lies in `L_10`; it need not
be a base tooth or belong to a half-turn pair. Native height-one
phase alone does not eliminate these terms. Replacing (5) by a
single-height-1 chain would therefore be unjustified.

The negative-tile budget does not by itself remove the problem:
when some base teeth are missing, the `c-r` remaining negative
height-one tiles may contribute precisely these internal contacts.
A quantitative lower cost for this additional chain is still needed.

## 5. The corners do not force an odd-height base tooth

There is an exact even-height pair at the path-frame corner `O`:

\[
 T_0=(q=a,h=0,j=0,s=+1),\qquad
 T_2=(q=az^2,h=2,j=0,s=-1).
\]

Both have long edge `O -> cz`. Their obtuse vertices lie on opposite
sides of that edge; the two boundary short sides of length `a` lie
on `OB` and `OC`. Their beta angles sum to the board angle `2 beta`.
Both triangles are contained in each target, and their interiors are
disjoint. Thus a local corner argument cannot force a height-one
long base tooth at `O`.

`verify_even_corner.py` checks the exact placements, containment,
areas, and opposite-bank separation, and independently enumerates
(4). It also checks the 143 shape. This is a two-tile partial packing;
no completion is asserted.

## 6. Two complete positive controls

`verify_actual_median.py` verifies the original 143 certificate and
the separately obtained macro certificate supplied here. It checks
each tile's exact area and containment, and equality of the positive
oriented tile boundary chain with the board. This proves one-fold
coverage, including the absence of positive-area overlap.

It then performs the stated isometry, cancels actual opposite long
edges, enumerates every vertex-simple upper path in the remaining
small graph, computes its exact enclosed area, and classifies every
tile by a rational centroid winding test. The current examples each
have exactly one reduced upper path.

| Complete 143 control | Upper-path length | `J,K` | `t` | Lower tile count | Upper tile count |
|---|---:|---|---:|---:|---:|
| Repository certificate | 16 | `-2,14` | 2 | 105 | 38 |
| Independent macro certificate | 16 | `-2,14` | 2 | 91 | 52 |

For both controls, `i=2,j_0=-2`; the lower polygon uses only height
1 and has odd charge `+7`, and the upper remainder uses only height
2 and has odd charge zero. Formula (3) is checked against these actual
tile populations. The macro control has `91=13c` odd tiles, so even
an otherwise tempting universal estimate `n_odd>=2c^2+c` would fail
at this positive control.

The replay files are `ACTUAL_MEDIAN_REPLAY.json` and
`EVEN_CORNER_REPLAY.json`. The additional full control is
`macro143_certificate.json`. Run:

```sh
python3 verify_actual_median.py
python3 verify_even_corner.py
```

The scripts find the existing continuation directory from their
ancestors. The median script also accepts `--continuation`, `--macro`,
and `--out` for an explicit replay location.

## 7. Remaining global gap

The minimal `3c` mode is now confined to a native height-one layer
inside a three-height tiling, with a genuine height-zero portion below
every upper median path. The physical internal chain `L_10` remains.
Neither the cut identities, the base-gap arithmetic, nor the even
corner controls bound its full geometric cost strongly enough to
exclude the mode. A global `5c` odd-population theorem, still less
nonexistence at 3431 or 5063, is not proved by this note.

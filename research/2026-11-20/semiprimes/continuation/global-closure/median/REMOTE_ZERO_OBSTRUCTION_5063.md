# The minimal 5063 case requires a charged even terminal branch

21 November 2026. This theorem concerns **every** hypothetical complete
5063 unit F2 tiling with odd-height population `3c=129`, including
tilings with nonnative height-zero and height-two populations. It
proves that at least one exterior-free even terminal node has nonzero
signed charge. It does not prove that the complete tiling is impossible.

No whole-mate condition is imposed in the new residue certificate.
In particular, occupied balanced remote nodes are allowed to support
unmatched contacts. They are not treated as empty nodes.

## 1. Every remote gate is an actual even terminal node

Use the path frame, with `(a,b,c)=(35,13,43)` and `d=a-b=22`.
The established minimal-odd localization gives only short heights
0,1,2; all height-one vertices belong to `zR`; and their sign
populations are

\[
 n_1^+=86,\qquad n_1^-=43,\qquad G_1=43.              \tag{1}
\]

`MINIMAL_ODD_PHASE_CLASSIFICATION.md` identifies all possible even
classes. Each nonnative height-zero class is a terminal exterior-free
node in the decreasing-height tree, and each nonnative height-two
class is one in the increasing-height tree. In both cases the
immediate parent is the unique height-one node.

After division by `z`, write a height-one tile's obtuse vertex as
`q=(x,y) in R`, its beta endpoint as `u=q-a*rho^j`, and its sign
as `epsilon=s*(-1)^j`. Label its long-edge gate by

\[
 r_+(u)=a u_y-bu_x\pmod c\quad(s=+1),\qquad
 r_-(u)=a u_x-bu_y\pmod c\quad(s=-1).                  \tag{2}
\]

Residue zero is the corresponding native exterior gate. Each other
residue corresponds to one exact even node, not an arbitrary group
of Euclidean cells. Let `Q_r^+` and `Q_r^-` be the signed numbers
of actual height-one tiles whose long edges use these gates.

For a remote node `v`, let `G_v=cg_v`. The exact node-current
equation is `dG_v-cH_v=0`. At even height zero or two, the absent
short heights -1 and 3 leave only height-one contributors to `H_v`.
Equivalently, the terminal cut formula gives

\[
 \boxed{Q_r^\pm=d g_v\qquad(r\ne0).}                  \tag{3}
\]

The charge `g_v` is an integer by ordinary-node signed divisibility.
An empty node has zero charge as well. Consequently, if all remote
even terminal nodes were balanced, then

\[
 Q_r^+=Q_r^-=0\qquad(1\le r<c).                       \tag{4}
\]

Balanced occupied nodes can have nontrivial actual contacts; only
their **signed total** is set to zero in (4).

## 2. A complete-residue inequality with no pairing assumption

Keep all `12c^2=22,188` translated orientation classes for the
height-one layer, represented by `q mod cR`, all six rotations,
and both hands. Every column is a **single tile**. No placement is
removed because its gate is nonnative, and no mate is required.

Let `f_j(x,y)` be three integer tables, indexed by axis `j mod 3`
and `(x,y) mod c`. Use the table at an integral normalized point,
and zero at a point outside `R`. An oriented height-one segment
receives the difference of its endpoint values; other heights
receive zero. Let `W(T)` be the sum on a tile's two CCW short sides.

The whole-tiling sum of these weights is zero. Indeed every whole
long side of height one has normalized displacement `c*rho^j`.
Its endpoints either both belong to `R` with the same residue or
both lie outside `R`. Its weight is zero in either case. There is
no outer side of height one. The endpoint differences telescope
on all partial contacts and subdivisions, giving

\[
 \sum_{h(T)=1}W(T)=0.                                \tag{5}
\]

The certificate also supplies integer gate weights `lambda_r^+`
and `lambda_r^-`, with native weights
`lambda_0^+=lambda_0^-=0`. It verifies, for **every** one of the
22,188 single columns,

\[
 W(T)+\epsilon(T)
       \bigl(t+\lambda^{s(T)}_{r_{s(T)}(u(T))}\bigr)
 \le D.                                             \tag{6}
\]

All integer translations are covered because the gate labels and
endpoint tables depend only on `q mod cR`. Summing (6), then using
(1), (4), and (5), gives

\[
 \boxed{Dn_1\ge ct.}                                 \tag{7}
\]

The native gate currents are left completely free in this argument.
There is no fixed native parameter `f`, no bound on an individual
residue multiplicity, and no prescribed boundary-tooth inventory.

## 3. Exact certificate and contradiction

`REMOTE_ZERO_MIN_43_IPM.json` contains all integer tables and the
constants

\[
 D=1\,000\,002,\qquad t=3\,115\,886.
\]

The independent standard-library checker reconstructs every CCW
triangle from its short sides, recognizes its short-edge axes by
the exact Eisenstein norm, and checks (6) with integers. Across all
22,188 columns, the largest score is exactly `D`, and the smallest
is `-4,162,910`. Every native gate multiplier is checked to be zero.

Equation (7) therefore gives

\[
 n_1\ge\frac{133\,983\,098}{1\,000\,002}
      =\frac{66\,991\,549}{500\,001}>129=3c.          \tag{8}
\]

This contradicts the minimal population (1) under hypothesis (4).
Thus at least one remote signed current is nonzero. By (3), its
corresponding even terminal node has nonzero signed charge.

**Charged-branch theorem.** Every complete 5063 tiling with
`n_odd=129` has an occupied exterior-free terminal node of physical
height zero or two with `G_v!=0`, immediately adjacent to the unique
height-one layer. This is stronger than merely forcing a remote
node: the previously allowed possibility that all remote nodes are
balanced is excluded.

The proof does not require integrality of the native parameter in
the earlier fixed-profile experiments. The numerical LP generator
allows that parameter to vary continuously by omitting its equations
altogether; the exact summed inequality is valid for every native
gate current satisfying the actual total charge.

## 4. Quantified population and actual contact cost

Write the forced node's charge as `G_v=43g`, where `g` is a nonzero
integer. It is an ordinary terminal node. Occupied ordinary nodes
have at least `2c` tiles, and the established
[terminal-balance theorem](../../vertex-phase/TERMINAL_NODE_BALANCE.md)
says that a terminal exterior-free node with exactly `2c` tiles is
balanced. Hence

\[
 \boxed{|G_v|\ge43,\qquad n_v\ge129.}                 \tag{9}
\]

Use the exact terminal transport formulas from
`../../charge-transport/flux/SIGNED_CUT_TRANSPORT.md`. The two signed
crossing counts are

\[
 P=43g\quad\text{on the terminal-node bank},\qquad
 Q=22g\quad\text{on its height-one parent bank}.       \tag{10}
\]

The physical bank argument permits partial long-edge exposure. Its
signed surviving length, measured in full long-edge units, equals
the whole signed crossing count; each individual tile supplies at
most one such unit. Therefore at least `43|g|` actual tiles on the
inside bank and `22|g|` on the parent bank carry positive-length
parts of the physical interface. These populations are disjoint:

\[
 \boxed{\text{at least }65|g|\ge65
        \text{ actual boundary-carrying crossing tiles},}         \tag{11}
\]

including at least `22|g|>=22` tiles of the height-one parent.
These are actual contacts in the complete tiling, not catalogue
columns or auxiliary allocation blocks.

The parent tiles in (10)–(11) are already part of the 129 odd tiles
in (1); they must not be added again to a whole-board population
count. The terminal-node population in (9) is even-height and is
disjoint from that odd population. The 43 inside bank tiles are
already part of the node's population and likewise must not be
added a second time.

The universal single-class gate capacity provides a further finite
charge restriction. Every parent gate has at most 51 positive
tiles, while the entire parent population has only 43 negative
tiles. Since its signed gate current is `22g`,

\[
 \boxed{g\in\{-1,1,2\}.}                             \tag{12}
\]

For `g=2`, the parent bank needs at least 44 positive tiles and the
terminal node has even block population. Its charged `2c` case is
excluded by terminal balance, so `n_v>=4c=172`. No stronger general
terminal bound, such as `c^2` or `6c`, is asserted here.

## 5. Exact replay and positive controls

```sh
python3 verify_remote_zero_minimum.py REMOTE_ZERO_MIN_43_IPM.json \
  --out REMOTE_ZERO_MINIMUM_REPLAY.json
```

The checker imports no LP/model generator. It independently checks
every integer inequality and projects both previously verified
complete 143 controls. Their height-one populations are 105 and 91;
each has charge 7, all endpoint residue currents zero, native signed
gate currents `(14,-7)`, and every remote signed current zero.
Both positive controls pass. The 5063 certificate is applied only
to its own tile parameters.

The optional generator `remote_zero_minimum.py` uses a sparse
minimum-population LP with all single-tile columns, zero remote
currents, and charge `c`. It has no forced mates or population upper
bound. An earlier timed numerical attempt supplies no proof; the
integer table check and the summation argument above supply (8).

The conclusion leaves larger odd populations and the minimal case
with one of the charged terminal branches in (12) unresolved.
Neither 5063 nor 3431 is globally excluded by this note.

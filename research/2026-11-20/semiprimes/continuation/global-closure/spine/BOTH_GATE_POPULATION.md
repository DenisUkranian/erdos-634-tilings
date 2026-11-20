# The full exterior-spine class has at least five odd population blocks

21 November 2026. This is an exact conditional exclusion theorem for
the **entire** class classified in `SPINE_DICHOTOMY.md`. For both
targets, a tiling with no occupied exterior-free short node in either
prime tree has odd-height population at least `5c`. Consequently a
target tiling with the minimal odd population `3c` must have an
occupied exterior-free short node in at least one tree.

This theorem does not exclude all spine tilings, all tilings with
odd population `3c`, or either target itself. The geometric hypothesis
is essential to the two closed-gate pairing rules used below.

## 1. Put all three spine cells in the native path frame

In the standard frame the only permitted short cells are
`R`, `A+zR`, and `A+z^2R`, at heights 0,1,2. Apply the established
path isometry

\[
 F(x)=Bz^2-\rho z^2\overline{x},\qquad
 A=b(2a+b),\quad B=a(a+2b).
\]

It sends `(h,j,s)` to `(2-h,4-j,-s)`. The identity
`B-A*rho=c^2*conjugate(z)^2` shows that the three cells become

\[
 h=0:R,\qquad h=1:zR,\qquad h=2:z^2R.                 \tag{1}
\]

The board has outer heights 0 and 2. The sign convention in this
frame gives `G_odd=+c`. Since the sole odd height is one,

\[
 G_1=n_1^+-n_1^-=c.                                  \tag{2}
\]

The height-one population occupies one ordinary exact node in each
tree. Its positive and negative populations are separately divisible
by `c`, so `n_1/c` is an odd integer.

Rotate by `1/z`. The height-one short mesh is now `R`; its downward
long sides have edge cell `z^-1R`, and its upward long sides have
edge cell `zR`. For an integer native point `p=x+y*rho`,

\[
 \begin{aligned}
 p\in R\cap zR &\iff ay-bx\equiv0\pmod c,\\
 p\in R\cap z^{-1}R &\iff ax-by\equiv0\pmod c.
 \end{aligned}                                                     \tag{3}
\]

These follow by multiplying `p` by the numerator of `z^-1` or `z`;
the norm relation makes divisibility of either displayed numerator
equivalent to divisibility of both coordinates. The two congruences
are independent over `F_c`: their coefficient determinant is
`b^2-a^2`, nonzero for the two target triples.

## 2. Every possible height-one tile is represented

Use the native placement `(q,j,s)` with vertices

\[
 u=q-a\rho^j,\qquad q,\qquad w=q+b\rho^{j+s}.
\]

Its sign is `epsilon=s*(-1)^j`.

An upward tile (`s=+1`) has an open gate exactly when `u/z in R`;
a downward tile (`s=-1`) has an open gate exactly when `u*z in R`.
These are the two tests in (3). If the appropriate gate is closed,
the theorem in `CLOSED_GATES_AND_NATIVE_THROUGH.md` forces its actual
whole-long-side half-turn mate, at

\[
 q'=q-a\rho^j+b\rho^{j+s},\qquad j'=j+3\pmod6,
 \qquad s'=s.                                         \tag{4}
\]

The pair has one tile of each sign. Its two long endpoints have
the same appropriate gate value, so the mate is also closed.

Partition the actual height-one tiles as follows: keep every open-
gate tile as a single, and group every closed-gate tile with its
unique actual mate. Reduce integer obtuse vertices modulo `cR`.
Every resulting column is one of:

* `12c` open single columns, covering both hands and all six
  rotations at every permitted gate residue;
* `6c(c-1)` closed pair columns, using rotations `j=0,1,2` for
  the representative and (4) for the other member.

The total is 8,436 columns for `c=37` and 11,352 for `c=43`.
Residue multiplicities are arbitrary nonnegative integers. Distinct
physical pairs can have the same residue column. An open-gate pair
can simply be represented by its two permitted single columns.

This covers all actual placements under (1). It imposes no extra
window, particular orientation inventory, or prescribed base teeth.

## 3. Periodic endpoint functionals

Choose three integer tables `f_j(x,y)`, with `j mod 3` and
`(x,y) mod c`. On a height-one side in the rotated frame, assign
endpoint value `f_j` at points in `R` and zero at points outside
`R`. The segment weight is the value at its end minus the value
at its start. Other physical side heights receive zero weight.

These functions telescope on all subdivisions. A whole long edge
of physical height one has displacement `c*rho^j` in the rotated
frame. Its endpoints either both belong to `R`, in the same residue,
or both lie outside `R`; its weight is zero. There is no exterior
height-one side. Therefore

\[
 \sum_{\text{height-one tiles }T}w_f(T)=0,              \tag{5}
\]

where `w_f` is the sum of the two CCW short-side weights.
This remains true with arbitrary partial contacts. It does not
assume that other-height vertices lie in `R` after rotation.

Suppose integers `t,D`, with `D>0`, satisfy

\[
 w_f(T)+t\epsilon(T)\le D
       \quad\text{for every open single},             \tag{6}
\]
\[
 w_f(T)+w_f(T')\le2D
       \quad\text{for every closed pair}.             \tag{7}
\]

The sign multiplier cancels in a pair. Summing (6) and (7) over the
actual partition, then using (2) and (5), gives the unrestricted
bound within the spine class

\[
 \boxed{n_1\ge \frac{ct}{D}.}                          \tag{8}
\]

## 4. Exact certificates and the five-block conclusion

The saved files `BOTH_GATE_MIN_37.json` and `BOTH_GATE_MIN_43.json`
contain the complete integer endpoint tables and the following
constants:

| Tile | Single columns | Pair columns | `t` | `D` | Exact bound `ct/D` | After odd `c`-block divisibility |
|---|---:|---:|---:|---:|---|---:|
| `(33,7,37)` | 444 | 7,992 | 3,784,753 | 1,000,001 | `140035861/1000001` | **185 = 5c** |
| `(35,13,43)` | 516 | 10,836 | 4,516,698 | 1,000,001 | `194218014/1000001` | **215 = 5c** |

For both certificates `t>3D`. Thus (8) excludes `n_1=3c`.
Since `n_1/c` is odd, its next possible value is at least five.
In this class all odd tiles have height one, proving

\[
 \boxed{n_{\rm odd}\ge5c.}                             \tag{9}
\]

By the exact spine dichotomy, any target tiling with `n_odd=3c`
therefore has an occupied exterior-free short node in at least
one prime tree. This is a genuine forced-branch theorem for that
minimal-population case. The earlier abstract axis-flow examples
with `15c` or `17c` odd tiles are consistent with it.

**Forced terminal-leaf corollary.** In every hypothetical target tiling
with `n_odd=3c`, an occupied exterior-free **terminal node of even
short height 0 or 2** must occur. Its immediate parent is the unique
occupied height-one node in the corresponding tree.

Indeed the previously established
[minimal-odd localization](../../charge-transport/geometry/ACTUAL_MEDIAN_CHARGES.md)
leaves only heights 0, 1 and 2, with all height-one tiles in the native
joint cell. Both height-one exact nodes therefore contain an exterior
edge in their descendant chains. The exterior-free node just forced
must have height 0 or 2. A height-zero exterior-free node in the
increasing-height tree would require an occupied height-minus-one
immediate parent, which is absent. It is therefore exterior-free in
the decreasing-height tree, where all its descendants have absent
negative heights; it is terminal. The height-two case is the reverse:
it is terminal in the increasing-height tree. The occupied-parent
theorem places either parent at height one, where only the native
exact node is occupied.

This corollary does **not** show that the forced terminal leaf has
nonzero signed population. A balanced even leaf can still be necessary
to repair contacts while the odd charge remains in the native middle
cell. Excluding those possibilities requires further geometry.

## 5. Independent replay and the 143 control

`verify_both_gate_torus.py` uses only the Python standard library.
It does not import the numerical generator or its sparse matrices.
For every residue/orientation column it constructs the actual CCW
triangle, identifies short sides by the exact Eisenstein norm,
and calculates their directed endpoint weights. Gate membership is
checked directly by coordinate integrality of `u/z` or `u*z`, as
well as by (3). It verifies (6) and (7) with integers for all 19,788
target columns. The largest scores are exactly `D` for singles
and `2D` for pairs.

The checker also transforms the previously verified complete 143
tiling to this native path frame. Its height-one layer has 105
actual tiles, with signs `(56,49)`. The exact projection consists
of 21 open singles and 42 actual closed pairs. Every one of its
`3c^2` endpoint residue equations has zero residual. This checks
the pairing, gate, and periodic-current conventions against a
real positive tiling.

```sh
python3 verify_both_gate_torus.py --out BOTH_GATE_REPLAY.json
```

The optional `both_gate_torus.py` generator uses a floating-point
LP only to find endpoint tables. The proof is (8) and the independent
integer checks. Initial numerical infeasibility reports and an
unsuccessful timed dual search are not used as proof evidence.

The result closes exactly the class
`{no occupied exterior-free node in either tree} intersect {n_odd=3c}`.
It leaves larger odd populations and the minimal case with occupied
exterior-free branches unresolved.

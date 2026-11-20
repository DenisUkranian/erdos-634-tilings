# An exact obstruction to a proposed ordered-quotient calibration

21 November 2026. This note tests an attempted global proof route for the
3431 and 5063 tiling questions. It does **not** settle either question.
It gives two exact reasons that a natural product-of-trees argument is
too weak in its present form, together with replayable certificates.

1. Two positive, disjoint, congruent tiles fitting inside either target
   already contribute opposite coefficients to the same product-tree
   square. Physical positivity does not give a coefficientwise positive
   filling in that complex.
2. Every linear tile-count calibration supported only on the squares of
   the board's own filling, and valid for every abstract translated tile,
   has value at most `19408/3235 < 6` at 3431 and
   `28377/2795 < 11` at 5063. These ceilings follow from explicit exact
   positive rational witnesses, not from a numerical optimality claim.

The second statement is a limitation of a specified relaxation. It is
not a restriction on every possible use of ordered boundary information.

## 1. The exact two-dimensional invariant

Use the standard board

\[
 T=\operatorname{conv}\{0,A,B\rho\},\qquad
 A=b(2a+b),\quad B=a(a+2b),\quad
 \rho=e^{i\pi/3},\quad z=(a+b\rho)/c.
\]

The ordered quotient maps already established in
[the simultaneous quotient theorem](../../../2026-11-20/semiprimes/continuation/global-closure/topology/SIMULTANEOUS_QUOTIENTS.md)
take a directed physical unit segment of heading `z^h rho^j` to

\[
 X_{j+h}^{s^h}\in\mathcal A=C_a*C_a*C_a,\qquad
 Y_j^{t^h}\in\mathcal B=C_b*C_b*C_b,
 \quad s=bc^{-1}\pmod a,\quad t=ac^{-1}\pmod b.
\]

Here `X_(i+3)=X_i^(-1)` and similarly for `Y`, and `s^2=t^2=1`
in their respective residue rings. Each tile boundary is trivial in
both groups. Thus any actual tiled disk has consistent group labels
on its subdivided skeleton, including at partial contacts.

Let `T_A,T_B` be their Bass--Serre trees. A factor coset is the centre
of a star whose leaves are the elements of that coset. A unit edge
changes each group coordinate along the unique two-edge path in its
factor star. To make an oriented map into the one-skeleton of
`T_A x T_B`, change A first and B second when `j mod 6` is 0, 1 or 2;
use the reverse order otherwise. Reversing a physical edge then
reverses exactly the same product-tree path.

An oriented edge of either tree is directed from a factor centre to
a group leaf. For a closed mapped boundary, there is a unique finite
cellular square 2-chain having that boundary. Indeed the product of
two trees is contractible and has no 3-cells, so its second cellular
boundary map is injective and every finite 1-cycle bounds.

The checker constructs this filling directly. For every A-edge at
a B-vertex, multiply its signed coefficient by minus the root-to-vertex
B-path and sum the resulting squares. It then independently takes
the cellular boundary of the resulting 2-chain and compares it with
the developed original path. The equality is checked for all 72
height/rotation/hand classes, for each target and the positive 143
control. Six height residues suffice because both quotient maps are
periodic in `h` modulo six.

If a physical tiling has tiles `T_i`, subdivision and internal-edge
cancellation imply the exact additive identity

\[
 F(\partial T)=\sum_i F(\partial T_i).
\]

The group labels at the start of a tile left-translate its canonical
filling in the two factors. This identity is necessary for every
physical tiling; it does not characterize physical realizability.

## 2. A positive pair already folds

In axial coordinates take the two CCW triangles

\[
 (0,(a,0),(a,b)),\qquad (0,(a,b),(0,b)).
\]

They are the two halves of the parallelogram with side lengths `a,b`,
sharing their full length-`c` edge. Both have determinant area `ab`,
disjoint interiors, and are congruent to the required tile. The whole
parallelogram fits in the target, since its only nontrivial containment
inequality is `Ba+Ab <= AB`, checked exactly.

Their directed boundaries have edge data

\[
 (a,0,0),(b,0,1),(c,1,3)
\]

and

\[
 (c,1,0),(a,0,3),(b,0,4),
\]

respectively, where entries are `(length,height,direction index)`.
The common long edge cancels. The exact fillings give:

| Tile | First tile norm | Second tile norm | Union norm | Squares with opposite tile coefficients |
|---|---:|---:|---:|---:|
| `(5,3,7)` | 28 | 26 | 36 | 9 |
| `(33,7,37)` | 156 | 154 | 164 | 73 |
| `(35,13,43)` | 184 | 182 | 196 | 85 |

Norm here is the sum of the absolute values of square coefficients.
All additions and boundaries are checked with integers. An explicit
oppositely signed square in each pair is saved in the replay report.

Consequently, a claim that all positive physical tiles contribute
nonnegative coefficients in a common orientation of these squares
is false. Changing a square's orientation reverses both coefficients
and cannot remove their disagreement.

This does not exclude a nontrivial linear functional whose *total*
value is bounded on each tile. It excludes the much simpler argument
that absence of coefficientwise cancellation follows from geometric
positivity.

## 3. A straight segment of length ab disappears

There is a structural loss of information even before tiling is
considered. **A straight physical segment of length `ab` maps to the
zero cellular 1-chain in the product of the two trees.** Its endpoint
group labels also return to their starting values.

For a fixed physical direction, the unit-step exponents in the two
cyclic factors are units modulo `a` and `b`. Since `gcd(a,b)=1`, the
`ab` successive states visit every pair of factor residues exactly
once. For any fixed B-leaf, each A-leaf edge is traversed once into
and once out of the A-star; these cancel. The B-edge calculation is
identical. Left translation preserves this statement. Its filling is
therefore zero as well, by uniqueness.

The checker tests all 36 height/direction classes, but the preceding
argument proves the assertion without enumeration. In particular,
removing multiples of `ab` from each straight boundary side does not
change this auxiliary invariant:

| Target | Actual boundary lengths | Lengths modulo ab | Product-tree filling norm |
|---:|---|---|---:|
| 3431 | `511,1369,1551` | `49,214,165` | 266 |
| 5063 | `1079,1849,2135` | `169,29,315` | 476 |

The shortened words are group-theoretic images, not boundaries of
the original physical triangles. No geometric substitution is allowed
on the basis of this equality.

## 4. Exact ceiling for calibrations supported on the board filling

Let `S` be the finite set of squares where the target board filling
`F_B` is nonzero. A calibration of the type tested here assigns real
weights `w_s` to `s in S` and zero to every other square. Suppose it
is normalized by

\[
 \langle w,L_{g_A,g_B}F_{h,j,\sigma}\rangle\le1
\]

for every abstract left translation `(g_A,g_B)` and every tile
height, rotation and hand. Then every physical `N`-tiling would imply
`<w,F_B> <= N`.

The accompanying certificates give positive rational coefficients
`lambda_i` and explicit abstract translated tiles with

\[
 \left.\sum_i\lambda_i L_iF_i\right|_S=F_B|_S.
\]

Their total costs are:

| Target | Exact positive terms | Sum of coefficients |
|---:|---:|---:|
| 143 control | 3 | `3` |
| 3431 | 109 | `19408/3235` |
| 5063 | 214 | `28377/2795` |

Therefore, for every normalized calibration of this specified type,

\[
 \langle w,F_B\rangle
 =\sum_i\lambda_i\langle w,L_iF_i\rangle
 \le\sum_i\lambda_i.
\]

This proves the two ceilings stated at the start. No exact optimality
claim is required: a single positive rational witness proves the
upper bound. The numerical solver was used only to discover weights;
the replay reconstructs all of them as fractions and checks every
selected square equality exactly, without importing a solver.

There are nonzero uncontrolled coefficients outside `S`, explicitly
counted in the replay. Thus these are **projected** witnesses, not full
2-chain fillings. They are also not physical tile placements. The
theorem does not bound calibrations allowed to use additional squares,
nor calibrations whose tile inequalities incorporate further physical
location restrictions.

## 5. The precise stronger quantity left unresolved

One legitimate next invariant is the full positive integral filling cost

\[
 \mathcal A_\square(F_B)=
 \inf\left\{\sum_i m_i:
 F_B=\sum_i m_i L_iF_i,\quad m_i\in\mathbb Z_{\ge0},
 \quad\text{finite support on all squares}\right\}.
\]

Every physical tiling supplies such an identity with total cost `N`.
Hence a proof that `A_square(F_B)>N` would be a genuine nonexistence
obstruction. Neither the small projected certificates above nor the
two-tile folding example decides that full integer problem. The
period loss and local cancellations explain why replacing it by a
board-supported linear calibration is inadequate.

No claim of full closure, a new target population lower bound, or a
physical completion is made here. Both 3431 and 5063 remain open.

## 6. Reproduction

From this directory run:

```sh
python3 verify_product_tree.py
```

The replay uses only the Python standard library. It verifies exact
cellular boundaries, the actual positive-pair counterexample, all
period controls, and the exact rational projected certificates. Output
is `PRODUCT_TREE_REPLAY.json`.

`projected_calibration_probe.py` is the optional SciPy discovery script.
Its saved floating diagnostics are retained separately and are not
proof inputs to the exact replay. The positive rational proof inputs
are in `projected_calibration_certificates.json`.

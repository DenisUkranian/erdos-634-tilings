# Native even nodes retain an inhomogeneous boundary cost

21 November 2026. **3431 and 5063 remain OPEN.** These are exact necessary
bounds under a stated three-height, one-odd-cell hypothesis. They do not
apply automatically to every larger odd population.

## 1. Hypotheses and the accessible gate

Work in the reflected path frame with board

\[
0,\quad c^2,\quad Bz^2,
\qquad z=(a+b\rho)/c,\quad A=b(2a+b),\quad B=a(a+2b).
\]

Assume that all short heights are 0, 1, 2 and every height-one tile has
vertices in the single native cell `zR`, where `R=Z[rho]`. These conditions
hold in the established [3431 minimal-odd normal form](../../../../2026-11-20/semiprimes/continuation/global-closure/median/MINIMAL_ODD_PHASE_CLASSIFICATION.md).
They also hold in the native one-cell subcase of the remaining 5063
215-tile odd mode. Remote **even** classes may be occupied.

In either native even cell every long edge outside the unique native
height-one gate has an actual whole half-turn mate in the same even cell.
For long heights -1 and 3, no other short heights can occur on those lines.
For a nonnative gate at height one, a mixed-height long mate would put a
height-zero or height-two tile in the descendant subtree of an unoccupied
exterior-free height-one node. The occupied-parent theorem excludes this.
This is the same argument as the
[one-accessible-gate theorem for remote terminals](../../charged-branches/ISOLATED_GATE_TERMINAL_COST.md),
with the native exterior contribution retained explicitly below.

Normalize the exceptional height-two core by dividing coordinates by `z^2`.
Its singles have hand `s=-1` and gate `psi(u)=a*u_x-b*u_y=0 (mod c)`.
All other tiles occur in whole half-turn pairs. Keeping arbitrary pairs
also at the accessible gate only relaxes the model.

## 2. The boundary source must not be discarded

The normalized board vertices are

\[
O=(0,0),\qquad X=(B,-A),\qquad Y=(B,0).
\]

Use endpoint currents with `+1` at the terminal endpoint and `-1` at the
initial endpoint of a counterclockwise edge. The two exterior short-height
two sides give the periodic source

\[
b_0=\delta_O-\delta_Y,\qquad
b_1=\delta_Y-\delta_X,\qquad b_2=0,                 \tag{1}
\]

where coordinates are reduced modulo `cR` and the subscripts denote the
three unoriented axes. The long exterior side has height zero and supplies
no row at this height. Complementary whole long edges of length `c` have
equal endpoint residues and vanish in these rows.

For a tile `(q,j,s)`, with `u=q-a U_j`, `w=q+b U_(j+s)`, the short current is

\[
s\,[e_{j,q}-e_{j,u}+e_{j+s,w}-e_{j+s,q}].           \tag{2}
\]

Thus every hypothetical core satisfies `sum columns = b`, not zero.
This distinction produces a stronger population reserve than using only
its positive and negative sign residues.

## 3. Exact certificates and rounded populations

Each certificate contains three integer endpoint tables `f`, an integer
charge weight `t`, and a positive integer denominator `D`. With `W(T)`
the table pairing with (2), the independent verifier checks

\[
W(T)+t\epsilon(T)\le D
\quad\hbox{for every accessible single},
\]

\[
W(T)+W(T^*)\le2D
\quad\hbox{for every whole half-turn pair}.          \tag{3}
\]

Summing (3) over the actual decomposition and using (1) proves

\[
\boxed{n_{\rm core}\ge(\langle f,b\rangle+tG_{\rm core})/D.} \tag{4}
\]

No optimizer status enters (3)--(4). All translated placements are covered
by their residue columns, and each column inequality is checked with
integers. For the three 3431 cases the replay checks 222 singles and 8,214
pairs per table; for 5063 it checks 258 singles and 11,094 pairs.

Write `G_core=d+c*g_u`, with `d=a-b`. In this path frame the core sign
residues are `(8,19)` modulo 37 and `(27,5)` modulo 43. Correctly rounding
both signs gives:

| Target | `g_u` | Core charge | Exact lower bound | Required core population |
|---|---:|---:|---:|---:|
| 3431 | -2 | -48 | `21064508116/100000001` | **212** |
| 3431 | -3 | -85 | `35970666295/100000001` | **397** |
| 3431 | -4 | -122 | `51093809348/100000001` | **582** |
| 5063 | -3 | -107 | `67699999951/100000001` | **677** |

For example, charge -48 and residues `(8,19)` allow precisely populations
`64+74k`, for nonnegative integer `k`. The exact bound in (4) is greater
than 210, so the next allowed population is 212.

## 4. The native ordinary height-zero node

The native height-zero cell has a different boundary source: its only
exterior side at that height has length `c^2`, so its two endpoints agree
modulo `cR`. Its periodic source is therefore **zero**.

Reflecting the normalized one-accessible-gate certificate gives

\[
n_0\ge\frac{91}{22}|G_0|\quad(3431),\qquad
n_0\ge\frac{83}{13}|G_0|\quad(5063).                 \tag{5}
\]

The exact tables and their integer replays already appear in
[ISOLATED_GATE_TERMINAL_COST](../../charged-branches/ISOLATED_GATE_TERMINAL_COST.md).
The new point is their applicability to this native ordinary node: the
length-`c^2` exterior source vanishes in precisely the endpoint rows used
by those tables.

For 3431 with `G_0=37g_d`, separate sign divisibility yields respective
floors `185,370,481` for `g_d=1,2,3`. At charge zero the valid floor is zero
unless occupancy is independently known; an occupied ordinary node still
requires at least 74. The native height-zero cell may be empty, as the
143 control demonstrates.

For the surviving empty-remote 5063 profile `(Q_+,Q_-)=(20,23)`, one has
`g_u=-3`, `g_d=3`. Equation (5) requires at least 903 height-zero tiles,
and (4) requires at least 677 height-two tiles. Together with the 215 odd
tiles this gives only `N>=1795`, well below 5063. This calculation is not
a target contradiction.

## 5. Verification and remaining scope

Run:

```sh
python3 research/2026-11-21/semiprimes/full-closure-attempt/core-budget/verify_core_budget.py
```

The standard-library verifier independently reconstructs every endpoint
column, half-turn pair, exterior source, exact score, and sign rounding.
It also transforms the known 143 tiling to the path frame. The actual
height-two core contains 38 tiles, has charge 2, decomposes into two
accessible singles and 18 actual whole pairs, and has precisely source (1).

The discovery script uses SciPy to suggest weights. The proof replay does
not import it. These are written research arguments with independent
internal checks; no external referee report or proof-assistant verification
is claimed. Remaining charge profiles, larger odd populations, and both
original counts are still open.

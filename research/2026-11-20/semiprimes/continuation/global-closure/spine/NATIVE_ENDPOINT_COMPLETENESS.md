# A complete finite geometric model of the two-tree spine class

21 November 2026. The preceding `SPINE_DICHOTOMY.md` is an unrestricted
classification under the hypothesis that neither prime tree has an
occupied exterior-free short node. This note gives a finite endpoint
model **equivalent to a positive tiling of that entire class**. The
model is not claimed infeasible for either target.

## 1. Enumerating all placements, with no guessed radius

Use `R=Z[rho]`, `z=(a+b*rho)/c`, `A=b(2a+b)`, and `B=a(a+2b)`.
Put `t_0=0` and `t_1=t_2=A`. Every candidate tile has a unique key

\[
 (m,n,h,j,s),\qquad m,n\in\mathbb Z,\quad
 h\in\{0,1,2\},\quad j\in\{0,\ldots,5\},\quad s\in\{-1,1\},
\]

with obtuse vertex

\[
 q=t_h+z^h(m+n\rho)
\]

and other vertices `q-a*z^h*rho^j` and
`q+b*z^h*rho^(j+s)`. Keep the placement exactly when its three
vertices belong to the closed board. Distinct keys give distinct
physical placements: the scalene tile identifies its obtuse vertex
and unequal short sides, and different heights cannot give the same
direction modulo a sixth root of unity.

For a template `(h,j,s)`, let `E` be its three native offsets

\[
 E=\{-a\rho^j,\;0,\;b\rho^{j+s}\}.
\]

Write `z^h=(u+v*rho)/D_h`, with `D_h=c^h`, and for each
`e=alpha+beta*rho` in `E` put

\[
 X_e=u\alpha-v\beta,\qquad
 Y_e=v\alpha+(u+v)\beta.
\]

Containment is precisely the following three integer inequalities:

\[
\begin{aligned}
 -um+vn&\le t_hD_h+\min_{e\in E}X_e,\\
 -vm-(u+v)n&\le\min_{e\in E}Y_e,\\
 (Bu+Av)m+[-Bv+A(u+v)]n
 &\le AB D_h-Bt_hD_h-\max_{e\in E}(BX_e+AY_e).
\end{aligned}                                                   \tag{1}
\]

Thus the anchors for each template are exactly the integer points of
a bounded triangle, possibly empty. There is no heuristic translation
window. The inverse rotation `z^-h` of the three board vertices gives
an exact bounding box for `(m,n)`. For each integer `n` in that box,
(1) gives one exact interval `m_min(n)<=m<=m_max(n)` using integer
floor and ceiling operations. The union of these row intervals is
the full catalogue.

The dependency-free implementation `native_spine.py` counts the
intervals without materializing their individual placements. It also
provides a placement iterator, exact vertices, exact endpoint rows,
and the complete incident-placement oracle for any specified row.

| Board | Height 0 | Height 1 | Height 2 | Complete contained placements |
|---:|---:|---:|---:|---:|
| 143 | 9,123 | 8,675 | 8,856 | **26,654** |
| 3431 | 4,218,554 | 4,207,420 | 4,205,971 | **12,631,945** |
| 5063 | 12,860,166 | 12,830,527 | 12,832,985 | **38,523,678** |

These counts include contained placements which cannot occur in any
complete tiling. No compatibility, corner-fan, bank, or boundary
semigroup filter has been imposed in this table. Keeping these extra
columns does not affect the equivalence below.

## 2. A finite integer system equivalent to a positive tiling

Put all vertex coordinates over the common denominator `D=c^2`.
For a directed polygon side `p->q`, use the primitive integer
unoriented direction of `q-p`. Its endpoint current contributes
`+1` at `(p,direction)` and `-1` at `(q,direction)`. Each triangle
has six such point/direction rows. The board has six rows as well.

Let `C` be the complete catalogue from Section 1, and `M` the
finite matrix of all these actual endpoint currents. Include every
row occurring in a candidate or in the board, and let `b` be the
board current. The exact model is

\[
 \boxed{Mx=b,\qquad x_T\in\mathbb Z_{\ge0}\quad(T\in C).}       \tag{2}
\]

Equivalently one can require `x_T` Boolean. Nonnegative integrality
already implies it for any solution, as follows.

**Completeness and sufficiency theorem.** System (2) has a solution
if and only if the board has a positive tiling with no occupied
exterior-free short node in either prime tree. Every solution uses
exactly `N` distinct candidates, with pairwise disjoint interiors
and complete coverage.

**Necessity.** The spine theorem puts every tile of such a tiling
in `C`. Give its placement variable value one and the others zero.
Interior banks cancel as oriented intervals, and subdivision into
partial contacts introduces equal opposite endpoint terms. Hence
all equations (2) hold.

**Sufficiency.** For each supporting line, sum the directed interval
functions supplied by the selected tile sides and subtract the board
side function. Its distributional derivative is exactly the endpoint
current on that line. Equation (2) makes this derivative zero. The
function has compact support on the line, so the function itself is
zero. Therefore the full oriented polygon boundary current cancels.

Let `F` be the sum of the tile indicator functions with multiplicities
`x_T`, minus the board indicator. It is constant on every open cell
of the finite edge arrangement. The zero boundary current makes its
values equal across every generic edge crossing. A generic path to
the unbounded outside cell consequently proves `F=0` almost everywhere.

Every selected triangle has a nonempty interior. Positivity now
forces `x_T<=1` and forbids positive-area overlaps between distinct
selected triangles. Every open arrangement cell inside the board is
covered once; the closed union of the finitely many triangles then
covers the entire board. Area gives

\[
 ab\sum_Tx_T=AB=abN,
\]

so exactly `N` placements are selected. Their allowed cells give the
converse direction of the spine theorem. This proves the claim.

The argument allows arbitrary T-junctions and partial contacts. No
edge-to-edge hypothesis or explicit pairwise overlap catalogue is
needed when **all** endpoint equations and nonnegative integrality
are imposed. A fractional solution or a solution of only aggregate
axis currents is insufficient.

## 3. Complete rows allow a smaller necessary model

A specified endpoint and unoriented side direction admit at most
24 congruent placements before containment and native-cell filtering.
The code tries the 36 native orientation templates, solves the exact
integer anchor condition at each relevant endpoint, and retains
precisely those candidates from `C` contributing to the given row.

One can therefore impose any finite set of **complete** endpoint
equations without enumerating millions of unrelated placements.
Add all possible exterior-edge placements, exact exterior coverage,
and the upper bound of `N` selected tiles. Every tiling in the spine
class projects to this necessary model. An independently verified
UNSAT result for its permanent equations would exclude the entire
class. Temporary equations with incomplete incident catalogues
cannot support that conclusion.

Unlike the unrestricted height/phase search, there is a finite
complete catalogue to exhaust here. A fair expansion which eventually
completes every realized endpoint row terminates in the full model
(2), if allowed sufficient resources. This is a completeness result,
not a claim that the present implementation or available resources
reach that point.

## 4. The restricted complete-row solver

`spine_sat.py` reuses the existing independently audited endpoint
solver and replaces `Geometry.admissible` itself. It requires

\[
 h\in\{0,1,2\},\qquad z^{-h}(q-t_h)\in R,             \tag{3}
\]

before applying the solver's existing exact containment and boundary
arithmetic tests. Thus (3) is applied to **every** candidate returned
by each 24-placement incident oracle, including later expansions.
It is not implemented by deleting variables from one initial pool.

The boundary arithmetic tests exclude only placements which cannot
occur in any positive tiling: boundary offsets must allow both
remaining lengths to be sums of `a,b,c`. Their existing proof is in
the solver's `AUDIT_GLOBAL_INTEGER.md`. They are not included in
the raw counts in Section 1.

The optional `--closed-gates` and `--corners` upgrades retain forced
whole mates and exact native through-contacts. Their proofs and positive
controls are in `CLOSED_GATES_AND_NATIVE_THROUGH.md`.

The wrapper marks every checkpoint and model as restricted to the
complete spine class. A verified unguarded UNSAT result would close
that class and leave the occupied-exterior-free branch of the global
dichotomy. Guarded UNSAT, resource limits, and timeouts remain
inconclusive. An inherited solver message containing the word
"global" is relative to this explicitly restricted oracle.

The exact 143 positive control was supplied as a candidate seed,
not forced as selected variables. The wrapper returned SAT, exported
143 placements, and the independent metric/current verifier checked
their congruence, containment, area, and zero endpoint residuals.
The full catalogue's 143 row counts were also independently checked
by exhaustive bounding-box containment, and every one of the known
143 placements was retained at all six rows by the incident oracle.

## 5. Reproduction and current conclusion

```sh
python3 native_spine.py --out SPINE_CATALOGUE.json
python3 spine_sat.py 5 3 7 --out sat143 \
  --seed-json /path/to/continuation/global-endpoints/tiling_143.json \
  --rounds 3 --timeout-ms 10000 --proof
python3 /path/to/continuation/global-endpoints/verify_endpoint_tiling.py \
  sat143/solution.json
```

Both scripts accept the explicit existing-project paths shown by
`--help` (`native_spine.py` uses `--control`; `spine_sat.py` uses
`--continuation`). The counted catalogue is complete for the classified
native class; the SAT search is a separate attempt to decide its
geometric feasibility. The enumeration and positive control alone
do not exclude either target or establish a native normal form for
tilings with occupied exterior-free nodes.

The exploratory target outcomes are summarized in
`SPINE_SEARCH_STATUS.json`. The strengthened geometric searches stopped
at memory resource limits: 3431 had 28,159 columns and 449 complete
rows, while 5063 had 42,138 columns and 1,164 complete rows. Their
unguarded probes returned `unknown` at the time limit. Guarded UNSAT
results retained incomplete-row assumptions. These outcomes do not
exclude the complete spine class, and no further rounds are presented
as a mathematical conclusion.

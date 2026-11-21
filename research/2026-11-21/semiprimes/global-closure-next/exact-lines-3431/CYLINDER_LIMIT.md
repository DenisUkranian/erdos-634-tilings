# Actual supporting lines do not remove the fractional 3431 profile

21 November 2026. **Exact theorem; the tiling question remains open.**

The complete contained native-height-one cylinder relaxation for
`(a,b,c)=(33,7,37)` has a rational feasible point with population 111,
positive population 74, negative population 37, native gate currents 22
and 15, and zero remote gate currents. This statement retains every
actual transverse supporting-line coordinate. Only the longitudinal
coordinate along an edge is periodic modulo 37.

The witness also satisfies the positive gate capacities 44 and the
individual placement bounds `0 <= y <= 1`. A first lift violates a
specific point-packing inequality. Averaging 133 contained translates
repairs that issue: a second exact rational witness satisfies **every
valid linear inequality for integral nonoverlapping contained partial
packings of exactly 111 height-one tiles**. An explicit finite convex
decomposition proves this stronger assertion.

This remains a fractional witness. The required positive/negative
populations, gate currents, and cylinder equations hold in the convex
mixture; they are not asserted for any one integral packing in the
decomposition. No tiling, and no impossibility of tiling, follows.

More generally, a finite positive linear map lifts **every** feasible
nonnegative torus point into this contained cylinder model while
preserving every residue-column mass. Thus this cylinder upgrade has
exactly the same projection onto residue columns, gate currents, and
populations as the torus model. Searching for further linear cuts from
these cylinder equations cannot eliminate the certified 111 profile.

## 1. Exact finite geometry and the cylinder equations

Use the path frame, with board vertices `0`, `c^2`, and `B*z^2`, where
`B=a(a+2b)` and `z=(a+b*rho)/c`. Divide this frame by `z`. Height-one
tile anchors are then integer axial coordinates `q=(x,y)`.

For convenience the three board vertices, multiplied by `c`, are

\[
 (0,0),\quad(c^2(a+b),-c^2b),\quad(Ba,Bb).
\]

Let

\[
 U_0=(1,0),\ U_1=(0,1),\ U_2=(-1,1),\quad U_{j+3}=-U_j.
\]

A tile `(q,j,s)`, with `0 <= j < 6` and `s in {-1,1}`, has other
vertices `u=q-aU_j` and `w=q+bU_(j+s)`. Its four short-edge endpoint
terms are

\[
 +s(j,q),\quad -s(j,u),\quad +s(j+s,w),\quad -s(j+s,q),
 \tag{1}
\]

with axis labels taken modulo three. The cylinder row at a point is

\[
 \begin{array}{c|c|c}
 \text{axis}&\text{actual transverse coordinate}&\text{longitudinal residue}\\
 0&y&x\pmod c\\
 1&x&y\pmod c\\
 2&x+y&y\pmod c.
 \end{array}
 \tag{2}
\]

A whole complementary long side of length `c` has identical rows at
its endpoints and therefore vanishes. Arbitrary subdivisions telescope.
There is no exterior board side of short height one. Consequently the
sum of (1) is zero at every row (2) in any actual tiling in this native
height-one regime.

This is a necessary projection of physical endpoint current. In
particular, it still identifies endpoints on the same supporting line
separated by `cU_i`. Full physical endpoint current does not make that
identification.

The complete catalogue contains **4,207,420** contained placements and
137,307 cylinder endpoint rows, with 74 further gate rows. The catalogue
generator tests exact integer row intervals; the independent dual
checker uses a different enumeration of every integer anchor in the
bounding box and every orientation, testing all three vertices against
all three sides.

## 2. A finite convolution on the triangular lattice

Set `t=(800,-36)`. Let `X,Y,K` range independently over
`{0,...,c-1}` and put

\[
 q=t+XU_0+YU_1+KU_2=(800+X-K,-36+Y+K).
 \tag{3}
\]

Write `m(q)` for the number of triples giving `q`. This is an integer
between one and `c` on its support. Its support is the 3,997-point
hexagon

\[
 |x-800|\le36,\qquad |y|\le36,\qquad |x+y-800|\le36.
 \tag{4}
\]

For every residue `r=(r_x,r_y)` modulo `c`,

\[
 \sum_{q\equiv r\;(\mathrm{mod}\;cR)}m(q)=c.
 \tag{5}
\]

Indeed, after choosing `K`, there is exactly one `X` and exactly one
`Y` in the specified range producing `r`.

Given arbitrary torus column weights `x_(r,j,s)`, define actual placed
weights

\[
 \boxed{y_{q,j,s}=\frac{m(q)}{c}\,x_{(q\bmod c),j,s}}
 \tag{6}
\]

on the support (4), and zero elsewhere. This is a positive rational
linear map `L`. Equation (5) says that aggregating (6) by residue gives
exactly the original vector `x`. In particular, it preserves total
population, sign populations, individual gate populations, signed gate
currents, and every other linear datum of the original residue columns.

## 3. Why every actual supporting-line equation is preserved

Define three integer functions

\[
\begin{aligned}
 L_0(v)&=\#\{(Y,K): -36+Y+K=v\},\\
 L_1(v)&=\#\{(X,K): 800+X-K=v\},\\
 L_2(v)&=\#\{(X,Y): 764+X+Y=v\}.
\end{aligned}
 \tag{7}
\]

Each free pair ranges over `{0,...,c-1}^2`. For a fixed actual line
transverse to axis zero, the remaining uniform variable `X` gives one
representative of every longitudinal residue. Thus

\[
 \sum_{\substack{q\equiv r\;(\mathrm{mod}\;cR)\\q_y=v}}m(q)
 =L_0(v)
 \quad\text{whenever }v\equiv r_y\pmod c.
 \tag{8}
\]

The right side is independent of `r_x`. For axis one the analogous
identity uses the free variable `Y`, and for axis two it uses `K`.
The latter translates along `U_2` while fixing `x+y`.

The two endpoints of any short edge in (1) have the same transverse
coordinate as its anchor for that axis. Therefore (8) applies equally
to its start and end: neither the offset `-aU_j` nor `bU_(j+s)`
changes the relevant transverse coordinate.

Let `E` expand a torus endpoint row into actual cylinder rows by
assigning the factor `L_i(v)/c` to every compatible real transverse
coordinate. Equations (6)--(8) give the operator identity

\[
 \boxed{A_{\mathrm{cylinder}}L=E A_{\mathrm{torus}}.}
 \tag{9}
\]

In particular, a zero torus endpoint vector maps to a zero cylinder
endpoint vector. The checker verifies (9), after multiplying by `c`,
column by column using only integer counters. It separately checks all
4,107 axis/residue marginal identities (8).

Conversely, aggregation of cylinder rows by their transverse residue
gives the torus equations. Together with (5), this proves equality of
the two projected nonnegative feasible sets. The claim concerns this
linear relaxation, with continuous placement weights.

## 4. Strict containment and the exact rational 111 witness

Every one of the twelve oriented tiles at every anchor in (4) is
strictly inside the board. There are **47,964** such placed columns.
Testing their three vertices against the three integer board
halfplanes gives the strictly positive minimum determinant

\[
 143,854,520>0.
\]

Thus the lift uses genuine permitted rigid positions from the full
contained catalogue. No excluded or exterior placement is used.

Apply (6) to the exact rational torus witness from
[N3431_PROFILE_LIMIT.md](../../global-invariant/N3431_PROFILE_LIMIT.md).
The source witness is defined by the exact correction
`x_*=x_0+M^dagger(b-Mx_0)` and a verified rational inverse-norm bound.
The present checker reruns that complete source verification, including
all 1,369 Fourier blocks; it does not rely on saved numerical status.

By (5) and (9), the lifted point has exactly

\[
 n=111,\quad n_+=74,\quad n_-=37,\quad
 Q_0^+=22,\quad Q_0^-=15,
\]

with every remote gate current zero. The positive gate caps 44 are
preserved. Every supported weight is strictly positive.

The source approximate point has maximum coordinate
`524232213366 / 10^12`; its squared correction norm is bounded by
`2964060 / 10^24`. The exact inequality

\[
 (10^{12}-524232213366)^2>2964060
\]

proves every source coordinate is less than one. Since `m(q)/c <= 1`,
all lifted coordinates are also less than one. Hence simply imposing
the continuous bounds `0 <= y <= 1` does not remove this point.

## 5. A concrete packing inequality that the lift violates

For any packing, and any point `p`, the sum of selected tile indicators
whose **interiors** contain `p` is at most one. Consider the point

\[
 p=(80801/101,\ 1/103)
\]

in the normalized coordinates used above. It lies on none of the
edges of the supported tiles. The source approximate point and the
lift give coverage

\[
 F_0(p)=\frac{260060874905985}{37000000000000}
       \approx 7.028672294756351.
\]

The exact corrected witness still has coverage greater than one. To
verify this without expanding its large rational correction, let
`w_(r,j,s)` be the sum of multiplicities `m(q)` of lifted tiles from
that residue column whose interiors contain `p`. Cauchy--Schwarz and
the verified source correction bound give

\[
 |F(p)-F_0(p)|^2
 \le\frac{2906918851320}{(37\cdot10^{12})^2}.
\]

The squared numerator of `F_0(p)-1` is

\[
 49756153913823488682588820225,
\]

which strictly exceeds `2906918851320`. This is an exact violated
packing inequality. It removes this explicit fractional witness.
It does **not** prove that all cylinder witnesses violate a packing
constraint, and it does not exclude a 3431 tiling.

## 6. Averaging 133 copies satisfies every point-packing inequality

The convex hull of every vertex of every supported tile is the axial
hexagon with centre `(800,0)` and radius

\[
 R=(c-1)+a=69.
\]

Its six vertices are `(800,0)+69U_j`. Translating this entire hexagon
by `c(u,v)` leaves it strictly inside the board for exactly **133**
integer pairs `(u,v)`. The complete search is finite: containment of
the hexagon centre requires

\[
 -21\le u\le18,\qquad -7\le v\le7.
\]

Testing the six vertices against the three board sides finds the 133
translations. The minimum halfplane determinant of all accepted
hexagons is `1418284>0`. The replay lists every translation.

Let `T` be this translation set and define

\[
 \bar m(q)=\sum_{t\in T}m(q-ct),\qquad
 \bar y_{q,j,s}=\frac{\bar m(q)}{37\cdot133}
                    x_{(q\bmod37),j,s}.
 \tag{10}
\]

This is the average of 133 shifted copies of (6). Each shift is by
`cR`, so it preserves every gate label and longitudinal residue and
only relabels actual supporting lines. Thus (10) still satisfies all
cylinder equations and all the same residue, gate, and population data.

For a fixed resulting anchor `q`, the preimages `q-ct` are distinct
members of the same residue class. Equation (5) therefore proves

\[
 0\le\bar m(q)\le c=37,\qquad
 \bar y_{q,j,s}\le\frac{x_{(q\bmod37),j,s}}{133}.
 \tag{11}
\]

The checker finds 226,663 supported anchors, or 2,719,956 oriented
placed columns. Their support is entirely in the complete contained
catalogue.

For a fixed residue and orientation `(r,j,s)`, distinct anchors differ
by a nonzero vector in `cR`. Such a vector has Euclidean length at
least `c`, since the squared norm of a nonzero integer axial vector
is the positive integer `u^2+uv+v^2`. The diameter of a tile is exactly
`c`. Two of its interior points are at distance strictly less than
`c`, so these translated tiles have disjoint interiors.

Consequently at most one tile from each fixed residue/orientation
family contains any point in its interior. Summing (11) over families
gives the uniform bound

\[
 \sum_{q,j,s}\bar y_{q,j,s}\,
             \mathbf1_{p\in\operatorname{int}(T_{q,j,s})}
 \le\frac{\sum_{r,j,s}x_{r,j,s}}{133}
 =\frac{111}{133}<1
 \quad\text{for every point }p.
 \tag{12}
\]

Thus **every** fractional point-packing inequality is satisfied, with
one common strict slack. Every conflict-clique inequality is also
satisfied: a clique contains at most one tile from each such family.

There is a direct stronger interpretation. For each residue/orientation
family and each `k=1,...,37`, take the integral partial packing

\[
 P_{r,j,s,k}=\{(q,j,s):q\equiv r\pmod{37R},\ \bar m(q)\ge k\}.
\]

Give it weight `x_(r,j,s)/(37*133)` and give the empty packing weight
`22/133`. These nonnegative weights sum to one and reproduce (10)
coordinate by coordinate. All components are genuine integral,
nonoverlapping, strictly contained partial packings. Their nonempty
cardinalities range from 99 to 168. This already proves that (10)
lies in the convex hull of arbitrary-cardinality partial packings.

## 7. A convex decomposition using exactly 111 tiles in each packing

The cardinality variation in the preceding decomposition can be removed.
Fix a residue/orientation family. Write `D=37*133=4921` and define

\[
 w_q=111\bar m(q),\qquad p_q=\frac{w_q}{D}.
\]

Equations (5), (10), and (11) imply

\[
 0<w_q\le4107<D,\qquad
 \sum_{q\equiv r}w_q=111D.
 \tag{13}
\]

The desired conditional marginals `p_q` therefore belong to the
111-subset polytope of this family. The following elementary construction
avoids invoking a polytope theorem.

Order the supported anchors of this residue lexicographically. Partition
the integer positions in `[0,111D)` into successive half-open intervals
of lengths `w_q`. For a sampling offset `t in {0,...,D-1}`, select every
anchor whose interval contains an integer congruent to `t` modulo `D`.
There are exactly 111 such integers in the entire range. Since every
interval has length less than `D`, none contains two of them. Thus
every sample is a set of **exactly 111 distinct anchors**.

Each anchor is selected for exactly `w_q` sampling offsets. Choosing
the offset uniformly gives its inclusion probability `w_q/D=p_q`.
All selected triangles have the fixed residue and orientation, so the
distance argument above makes every sample a nonoverlapping contained
partial packing.

Finally choose the residue/orientation family with probability
`x_(r,j,s)/111`. These probabilities sum to one. The resulting marginal
of a placed tile is

\[
 \frac{x_{r,j,s}}{111}\frac{111\bar m(q)}D
 =\bar y_{q,j,s}.
 \tag{14}
\]

This proves that (10) belongs to the convex hull of **integral,
nonoverlapping, contained partial packings of exactly 111 height-one
tiles**. The finite recipe has 80,842,188 components if repetitions
are retained. The verifier checks all 6,736,849 residue/sampling-offset
cardinalities by cyclic interval difference counts; the twelve
orientation/hand choices share those same anchor counts.

Each component has one orientation and one sign. The required sign
populations 74 and 37, the prescribed signed gate profile, and the
cylinder endpoint equations hold **only in the mixture**. They are
not asserted for an individual component. In particular, the theorem
does not replace a fractional realization by one admissible integral
height-one configuration.

## 8. What has and has not been decided

The new theorem establishes a real limit of the proposed line-based
upgrade: retaining every actual supporting line while keeping period
`c` along the line leaves the entire periodic feasible projection
unchanged for this board. Finite-support first-moment obstructions and
additional cylinder dual cuts cannot close the 111 profile.

The averaging theorem adds a stronger limitation. Let `P_111` be the
set of actual contained nonoverlapping height-one partial packings of
111 tiles, and let `H` denote the required cylinder/sign/gate equations.
We have constructed a rational point in

\[
 \operatorname{conv}(P_{111})\cap H.
\]

We have not shown that `P_111 intersect H` is nonempty. In general,
intersecting a convex hull with equations does not give the convex hull
of the discrete configurations that individually satisfy the equations.
No collection of inequalities valid for every packing in `P_111`,
combined only with these linear equalities, can remove the constructed
fractional point. A successful argument must preserve the joint
integer relationship between packing geometry and the required
charge/current data, or use additional physical conditions.

Longitudinally distinct endpoints are also still identified in the
cylinder model. The full Boolean physical endpoint model already
present in the project retains actual placements and exact endpoint
locations; its geometric equivalence gives coverage and nonoverlap.
An unfinished solution of that complete model is not an infeasibility
proof. Adding such conditions is logically meaningful, but their mere
presence does not imply an UNSAT result.

This theorem therefore neither establishes nor refutes the claim that
the complete rigid problem for 3431 is infeasible. It certifies why the
specific continuous cylinder route cannot supply that conclusion.

## 9. Reproduction and numerical provenance

From the repository root:

```bash
python research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/verify_cylinder_lift.py
```

The standard-library verifier writes `CYLINDER_LIFT_REPLAY.json` and
checks the finite convolution, every operator column, strict
containment, the source rational certificate, coordinate upper bounds,
the single-patch packing violation, all 133 strict contained translates,
and the exact-111 convex packing decomposition. Run without `-O`: the
imported source verifier uses Python assertions.

`cylinder_model.py` supplies the complete 4,207,420-column catalogue.
`column_generation.py` implements a restricted master with exhaustive
pricing against all of those columns and exports only integer-rounded
duals re-priced on the full catalogue. `verify_cylinder_dual.py`
independently checks such an exported dual using bounding-box
enumeration and a complete 143 tiling as a positive control.

As a full-catalogue pricing control, `periodic_dual_control.py` discovers
a periodic dual and embeds it into the cylinder rows. Its exported
integer certificate `PERIODIC_DUAL_FULL_CATALOGUE.json.gz` has the exact
fixed-profile population bound

\[
 n_1\ge\frac{105304866294}{1000000002}
       >105.30486608.
\]

The independent replay checks this inequality against **all 4,207,420
contained placements**, with no restricted pool, and verifies the
complete 143 positive control. The bound does not exclude 111. The
full-catalogue replay command is

```bash
python research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/verify_cylinder_dual.py research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/PERIODIC_DUAL_FULL_CATALOGUE.json.gz --out research/2026-11-21/semiprimes/global-closure-next/exact-lines-3431/FULL_CATALOGUE_PRICING_REPLAY.json
```

`PERIODIC_DUAL_DISCOVERY.json` records the separate numerical optimizer
result near 105.30486631. Neither that approximation nor the exact
lower bound is used to prove existence of the rational 111 witness.

The exploratory master runs in `run_native_f2/` and
`run_native_f2_ipm/` did not produce a certified optimizer conclusion:
the simplex run timed out, and the interior-point runs returned
`kUnknown` with residuals. Their logs are numerical provenance only.
The finite convolution proof supersedes the search for a separating
cylinder dual; no solver status is used in the theorem.

# Regional contact certificates with a global remaining-tile budget

21 November 2026. **Both 3431 and 5063 remain open.** This theorem
strengthens the supported-polygon charge test using complete catalogues
of actual whole owners. It permits arbitrary physical heights and
T-junctions. The control below gives a strict, attained strengthening on
an integer-area hole with nonzero odd charge; it is not a target
refutation.

The geometric inputs are the supported-region argument in
[`AREA_CYCLE_CUTS.md`](../corner-tests/AREA_CYCLE_CUTS.md), the complete
whole-bank catalogue in
[`GLOBAL_CONTACT_THEOREM.md`](../GLOBAL_CONTACT_THEOREM.md), and the two
established directed-edge characters. The certificate is a localized,
signed-cost version of the general
[`shared-owner capacity certificate`](../audit/OWNED_CONTACT_CAPACITY.md).

## 1. Supported regions and their exact minority budget

Let `B` be finitely many contained whole triangles with disjoint
interiors. Let `R` be a region whose polygonal boundary is supported by
their sides and/or the exterior of the board. A simple supported hole,
a union of disjoint such holes, and the board with their interiors
removed are permitted. Boundary subdivisions need not be whole tile
sides. All conclusions below are conditional on a full nonoverlapping
tiling containing the triangles in `B`.

Every tile interior in that completion lies wholly inside or wholly
outside `R`. Indeed, crossing an open boundary segment would overlap
its selected supporting triangle; crossing at a vertex would contain
a neighborhood meeting an occupied triangle interior. Apply this
argument to all boundary components. Write `n_R` for the area of `R`
in tile units. The oriented boundary characters determine its exact
even and odd signed populations `G_e(R),G_o(R)`. These are the formulas
in the polygon note, with each inner boundary oriented clockwise.

Fix `alpha_e,alpha_o` independently in `{−1,+1}`. A whole triangle
`T` in `R` has cost

\[
 \kappa_\alpha(T)=
 \frac{1-\alpha_{h(T)\bmod2}\epsilon(T)}2\in\{0,1\},
 \qquad \epsilon(T)=s(-1)^j.
\]

Call cost-one triangles minorities relative to this choice of signs.
This label is only a counting device; both kinds are positive-area
whole triangles. In any completion their exact number is

\[
 \boxed{M_\alpha(R)=
 \frac{n_R-\alpha_eG_e(R)-\alpha_oG_o(R)}2.}       \tag{1}
\]

The usual scalar condition `n_R>=|G_e|+|G_o|` only says that (1) is
nonnegative for all four choices. Actual contacts can force a positive
minority count and thereby strengthen that condition.

## 2. The finite weighted-contact theorem

Let `S` be any known selected whole triangles inside `R`; it may include
supporting triangles from `B`. The union of `B` and `S`, after canonical
deduplication, must be geometrically compatible. Choose finitely many
open unit contacts `e` on the boundary of `R`, with the bank inside `R`
specified. Each contact is precisely the interval `(k,k+1)` for an
integer `k`, measured from an endpoint of a selected whole side (or the
corresponding integer-anchored exterior boundary side). An arbitrary
length-one subinterval is not sufficient: it could straddle two actual
owners. Complete local catalogues must include every actual whole
triangle which can own that integer-offset bank interval.

Use the integer-offset lemma to enumerate the six side shapes and all
integer shifts. Delete a candidate only by an exact justified reason:
for example, failure of board/region containment or strict overlap with
a **distinct** selected whole triangle. The same canonical whole tile
is never excluded for overlapping itself. If a known inside supporting
triangle owns the contact, include it in `S` and the residual below,
or retain its one selected canonical variable in `Q`. In particular,
a candidate that would cross the
supported boundary can be excluded by a demonstrated overlap. Do not
replace a whole candidate by independent choices at its other contacts.

Let `Q` be the canonical union of the surviving candidates, excluding
the triangles in `S`. For each contact put `A[e,T]=1` when `T` owns it.
Put

\[
 r_e=1-\#\{T\in S:T\text{ owns }e\}.
\]

Nonoverlap makes the count zero or one. Whole coverage, integral offsets,
and the complete candidate catalogue give the exact equation

\[
 \sum_{T\in Q} A[e,T]x_T=r_e.                    \tag{2}
\]

A candidate in several catalogues has one canonical variable `x_T`.
All counted candidates must lie wholly inside `R`. Let `C_j` be any
certified spatial clique among `Q` and known `S`, and put

\[
 b_j=1-|C_j\cap S|,\qquad
 \sum_{T\in C_j\cap Q}x_T\le b_j.               \tag{3}
\]

For instance, a common strict interior point certifies a clique.
Its capacity is never inferred merely from distinct contact labels.

**Theorem.** Choose arbitrary rational contact weights `lambda_e` and
nonnegative rational clique weights `mu_j`. If the finite exact column
check gives, for every `T in Q`,

\[
 \boxed{\sum_e\lambda_e A[e,T]
        -\sum_{j:T\in C_j}\mu_j
        \le\kappa_\alpha(T),}                  \tag{4}
\]

set

\[
 L=\sum_e\lambda_e r_e-\sum_j\mu_j b_j,
 \qquad m_S=\sum_{T\in S}\kappa_\alpha(T).
\]

Every completion satisfies

\[
 \boxed{
 n_R\ge\alpha_eG_e(R)+\alpha_oG_o(R)
       +2m_S+2\max\{0,\lceil L\rceil\}.}        \tag{5}
\]

**Proof.** Multiply (2) by `lambda_e`, sum, subtract the weighted
inequalities (3), and apply (4):

\[
 L\le\sum_{T\in Q}\kappa_\alpha(T)x_T
   \le M_\alpha(R)-m_S.
\]

The second inequality drops only nonnegative costs of unlisted
triangles. It is valid because `Q` and `S` are disjoint whole-tile
populations. The right side is a nonnegative integer, so it is at
least `max(0,ceil(L))`. Equation (1) proves (5).

Negative contact weights are sound because (2) is an equality. They
are useful: nonnegative weights alone assign zero to any contact
admitting a cost-zero candidate unless another term compensates it.
Signed weights can exploit correlations among contacts. Nonnegative
clique weights additionally exploit spatial incompatibility. All such
claims reduce to the explicit rational column checks (4).

This proof does not reconstruct a mandatory even long bank from a
partial odd family. That reconstruction requires the complete odd
family, as stated in
[`PAIRED_BANK_RESERVE.md`](../../integer-closure/global-geometry/PAIRED_BANK_RESERVE.md).
Here the finite catalogue is complete only for each chosen actual
contact, which is sufficient for (2).

## 3. Reserving trapped regions in the global budget

Let `P_1,...,P_k` be supported regions with pairwise disjoint interiors,
each having known integer area `n_i` and charges `(G_e^i,G_o^i)`.
Let `R` be their complement in the board. It can have holes or several
components. Every full tile belongs to exactly one of these regions
up to its zero-area boundary. Therefore

\[
 n_R=N-\sum_i n_i,\qquad
 G_e(R)=-d-\sum_iG_e^i,\qquad
 G_o(R)=-c-\sum_iG_o^i.
\]

Applying (5) to complete contacts on the complement bank yields

\[
\boxed{
 N\ge\sum_i n_i
 +\alpha_e\!\left(-d-\sum_iG_e^i\right)
 +\alpha_o\!\left(-c-\sum_iG_o^i\right)
 +2m_S+2\max\{0,\lceil L\rceil\}.}               \tag{6}
\]

Thus exact areas reserved behind supported boundaries, the residual
odd/even imbalance, and the actual outside owners must fit one global
tile budget. One outside tile may touch several trapped regions. It
must still appear in a single column in (4); its entire contact load
is checked against one unit of minority cost. One must not sum
separately optimized hole-bank counts which charge that tile twice.

The local form (5) can be applied inside each hole as well. It is
compatible with the phase-node bounds: the constraints are imposed
on the same selected whole-tile variables. Their separate lower
reserves cannot automatically be added, because they may refer to
the same omitted tiles. A combined dual certificate must retain the
shared columns or an explicitly justified disjoint partition.

## 4. A strict geometric control with charged boundary and shared owners

Use the established exact143 tiling in
`continued-rigidity/physical/CONTROL_143.json`, with its zero-based
tile order. Remove tiles **1, 2, 3**. The seven remaining tiles
`0,4,5,7,11,13,15` support a convex polygon with encoded vertices

```text
(151,15,1), (25,0,0), (200,15,1), (225,30,1),
(176,30,1), (171,27,1), (156,18,1).
```

An encoded point `(x,y,e)` means `(x+y*rho)/7^e`. Its doubled axial
area is 45, so `n_R=3`. Its characters are `W0=-5`, `W1=-9`, giving
`G_e=0`, `G_o=1`. The old area/charge/parity conditions all pass and
give only the lower bound `n_R>=1`.

On the side of length five from `(176,30,1)` to `(151,15,1)`, the
outside supports split the boundary into lengths **1, 3, 1**. The
two split points are T-junctions. Each of its five unit contacts
has exactly one compatible complete inside owner:

```text
T = ((176,30,1), 1, 0, -1),
```

which is tile 2 of the control. It has odd short height and sign −1.
Choose `alpha_e=-1`, `alpha_o=+1`, no known interior triangles, no
clique weights, and weight `1/5` on each of the five contacts. The
single shared owner's column load is exactly one. Hence `L=1` and
(5) gives

\[
 \boxed{n_R\ge1+2=3.}
\]

This is a strict and attained strengthening of the scalar bound.
Equality uses the unique negative odd owner and leaves two positive
odd tiles. In particular no even tile can occur in a completion of
this region: the sole permitted minority slot is already occupied,
and its even signed total is zero.

Assigning weight one to all five contacts would falsely demand five
minority tiles. The column check rejects that attempted certificate
because the one whole owner's load would be five. This supplies a
concrete countercontrol to independent-contact counting, including
the relevant T-junctions.

## 5. Exact replay and the missing target certificate

Run:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/population/verify_contact_budget_theorem.py
```

The standard-library script checks the complete143 physical control,
the supported polygon and its exact characters, and the six-shape
integer-shift bank catalogues against the independent rational metric
constructor. It verifies all candidate exclusions using exact overlap
and convex containment, the five-contact shared-owner certificate,
and rejection of the fivefold overcount. It also enumerates small
Boolean incidence examples for signed contact weights, spatial clique
multipliers, integer ceiling, and known-owner residuals. These abstract
incidence controls test the finite inequality and claim no geometric
realization or target exclusion. Finally it checks the complement
bookkeeping for one and two disjoint regions in the actual143 tiling.

The agent responsible for the independent global proof audit reviewed
the theorem, the integer ceiling, known-owner residuals, and complement
accounting, and independently reran the standard-library controls.
The review requested the explicit integer anchoring and distinct-owner
exclusion hypotheses now stated in Section 2; with those clarifications
it found no further scope issue. This is an internal mathematical and
implementation review, not external refereeing or formal proof
assistant verification.

A target local exclusion requires an actual complete, geometrically
verified catalogue and rational weights for which

\[
 m_S+\max\{0,\lceil L\rceil\}
 >\frac{n_R-\alpha_eG_e(R)-\alpha_oG_o(R)}2.
\]

Equivalently, a complement certificate can make the right side of
(6) exceed `N`. Its no-good is conditional on every selected support,
known triangle, and unary exclusion used in constructing it. A global
result must exclude every remaining root or produce an unrestricted
refutation. The present exact143 control attains its budget and
excludes neither target. No claim that contact rigidity automatically
decides 3431 or 5063 is made.

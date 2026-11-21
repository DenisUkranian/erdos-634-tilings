# A finite global theorem for actual contacts and the remaining tile budget

21 November 2026. This is a necessary-condition theorem and an exact
completion criterion. It does **not** by itself exclude 3431 or 5063.

Use the standard F2 frame

\[
D=\operatorname{conv}\{0,A,B\rho\},\quad
A=b(2a+b),\quad B=a(a+2b),\quad
N=(a+2b)(2a+b),
\]

where \(c^2=a^2+ab+b^2\), \(d=a-b\), and
\(\rho=\exp(i\pi/3)\). Both targets have primitive odd sides and prime
\(c\). A placement is a whole congruent triangle, with canonical variable
\(x_T\in\{0,1\}\), short height \(h(T)\), and sign
\(\epsilon(T)=s(-1)^j\).

## Theorem

Start with the complete finite catalogues for every exterior unit
interval of \(D\), and let \(V\) contain all their admissible whole
placements. Add any further finite set of admissible whole placements.
Choose any finite set of vertex-fan obligations, whole-edge obligations,
and physical endpoint-current rows. Generate **every** candidate that can
participate in each chosen obligation or row, adding those placements to
\(V\). This demands completeness at the full exterior and the selected
local obligations, not completeness of the entire placement universe.

Every full tiling of \(D\) induces a Boolean assignment on \(V\) satisfying
all the following conditions simultaneously.

1. The actual exterior sides are covered once; every chosen complete
   physical endpoint row has the exterior current prescribed by \(D\).
2. Complete vertex fans use actual selected triangles. An interior
   half-fan includes a selected whole through tile on its other bank.
3. For each queried interior side \(e\) of a selected triangle, every
   open unit interval of \(e\) has exactly one selected opposite-bank
   neighbor from its complete local catalogue.
4. Distinct selected triangles have disjoint interiors. In particular,
   any finite group sharing a strict interior point has sum at most one.
5. With \(S=\{T\in V:x_T=1\}\), and \(G_o(S),G_e(S)\) the sums of
   \(\epsilon(T)\) at odd and even short heights,

   \[
   \boxed{|S|+|-c-G_o(S)|+|-d-G_e(S)|\le N.}
   \tag{1}
   \]

6. At the two target shapes, in **each** prime valuation tree separately,
   the ordinary nodes occupied by selected triangles or required as
   exterior-free ancestors satisfy

   \[
   \boxed{2cR+j+c\le N,\qquad j=N\bmod c.}
   \tag{2}
   \]

   Thus the corresponding node counts are at most 45 and 58. Costs from
   the two trees are not added. The stronger per-node allocation model
   may additionally reserve the complete selected population inside each
   individual node, as described below.
7. At either target, selected whole long sides cannot support a simple
   cycle in one translated triangular mesh of step \(c\), at any height.
8. Every simple polygon whose boundary is supported by selected whole
   sides encloses an integer number \(n(P)\) of tiles. Its two boundary
   characters determine integer charges \(G_e(P),G_o(P)\), and

   \[
   n(P)\ge |G_e(P)|+|G_o(P)|,\qquad
   n(P)-G_e(P)-G_o(P)\in2\mathbb Z.
   \tag{4}
   \]

   More strongly, if a set \(S_P\) of distinct selected or compulsory
   whole tiles lies inside that polygon, then

   \[
   \boxed{|S_P|+|G_e(P)-g_e(S_P)|+|G_o(P)-g_o(S_P)|\le n(P).}
   \tag{5}
   \]

All omitted placements remain allowed. No height interval, odd population,
coordinate radius, or finite placement box is imposed.

Conversely, a finite selection of contained, nonoverlapping whole tiles
which covers the exterior exactly and satisfies condition 3 for **every
selected side** is a tiling of \(D\). A partial finite model satisfying
only some queried sides does not satisfy this completion conclusion.

## Complete finite geometric catalogues

The [integer-offset lemma](../../../2026-11-20/semiprimes/continuation/first-cuts/CORNER_RAYS.md)
applies on a maximal connected run of collinear sides. All constituent
side lengths are integers; cancellation of the two banks forces their
endpoints to have one common arclength residue modulo one.

At an interior half-fan vertex, its extreme sides end on the through
line. Therefore an actual through side of length \(\ell\) has the vertex
at an integer offset \(1,\ldots,\ell-1\). For a fixed directed line and
bank there are exactly two whole triangle shapes per choice
\(\ell\in\{a,b,c\}\). Before containment filtering there are at most

\[
2(a+b+c-3)=148\text{ or }176
\]

through candidates.

For an entire selected side of length \(L\), an opposite side of length
\(\ell\) begins at integer offset

\[
1-\ell\le t\le L-1.
\]

Its positive overlap with unit interval \((k,k+1)\) is equivalent to
\(t\le k<k+1\le t+\ell\). The raw whole-bank catalogue size is

\[
\boxed{6L+2(a+b+c)-6\le370\text{ or }434.}
\]

Each candidate contributes one complete triangle, shared by every contact
which refers to it. For the interval candidate set \(C(e,k)\), the exact
necessary encoding is

\[
x_T\Rightarrow\bigvee_{Q\in C(e,k)}x_Q,
\qquad \sum_{Q\in C(e,k)}x_Q\le1.
\tag{3}
\]

The second clause is unconditionally valid because all such candidates
overlap on the same open bank. The encoding is **not**
\(\sum_Qx_Q=x_T\): neighbors may exist when \(T\) is absent.

## Charge and population proof

The two additive directed-edge characters are \((-1)^jL\) and
\((-1)^{h+j}L\). Their sums around a tile are respectively
\((d-c)\epsilon\) and \((d+c)(-1)^h\epsilon\). On the board both
characters sum to \(A+B-c^2=3ab=(c-d)(c+d)\). Consequently every full
tiling has total charges \(G_o=-c\) and \(G_e=-d\).

The omitted tiles must supply exactly the residual charges in (1).
Each omitted odd tile changes only the odd charge, by one in absolute
value; each omitted even tile changes only the even charge. Their number
is therefore at least the sum of the two absolute residuals. The four
choices of signs expand (1) into ordinary Boolean cardinality bounds.

The node theorem [NO_PHASE_GAPS.md](../../../2026-11-20/semiprimes/continuation/vertex-phase/NO_PHASE_GAPS.md)
provides the geometric input for (2). Selected triangles occupy their
own nodes, and every exterior-free ancestor of an occupied node is
occupied. Different ordinary nodes in one tree count disjoint tile
populations, each at least \(2c\). The core has at least \(j\) tiles.
Odd signed total \(-c\) forces one ordinary population to have an odd
number of \(c\)-blocks, hence at least \(3c\). This supplies the extra
\(c\), even when that node is outside the listed subset.

The stronger existing [per-node capacity projection](../../../2026-11-20/semiprimes/continuation/vertex-phase/POPULATION_BUDGETS.md)
uses integer allocations \(k_v\). For each tree, the selected population
\(m_v\) satisfies

\[
m_v\le j\mathbf1_{v=\mathrm{core}}+ck_v,
\quad\sum_vk_v\le(N-j)/c,
\]

with ordinary \(k_v\ne1\) and required ordinary ancestors having
\(k_v\ge2\). This couples crowded nodes with sparsely represented but
necessarily occupied nodes. Unused allocated capacity represents omitted
placements; it is not set equal to the generated population.

The cycle clauses use the existing
[supported-cycle theorem](../../../2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/NO_REMOTE_GAPS.md).
They retain integer-area mixed-height cycles; the pure-mesh obstruction
cannot be transferred to them.

## Local polygons and compulsory contact owners

Write the vertices of a positively oriented simple supported polygon in
axial coordinates as \(v_0,\ldots,v_m=v_0\). The exact number of tile
areas is

\[
n(P)=\frac{\sum_{i=0}^{m-1}\det(v_i,v_{i+1})}{ab}.
\]

For its directed boundary pieces, let \(W_0=\sum L(-1)^j\) and
\(W_1=\sum L(-1)^{h+j}\). Set

\[
E_0=\frac{W_0}{d-c},\quad E_1=\frac{W_1}{d+c},\qquad
G_e=\frac{E_0+E_1}{2},\quad G_o=\frac{E_0-E_1}{2}.
\]

In a full tiling no tile interior crosses a supported boundary: crossing
an open boundary segment would overlap the selected whole tile supporting
it. The polygon is therefore tiled independently by whole tiles. Additivity
of the two characters proves the displayed charge formulas, integrality,
and (4). Removing the distinct interior owners \(S_P\) leaves exactly
the residual signed charges in (5); each further tile supplies at most one
unit of one charge. This proves (5). Shared owners are counted once even
when they satisfy several contacts or several boundary subintervals.

For any \(\alpha_e,\alpha_o\in\{-1,1\}\), (5) gives a useful contact
capacity form:

\[
\#\{T\in S_P:\epsilon(T)=-\alpha_{h(T)\bmod2}\}
\le \frac{n(P)-\alpha_eG_e(P)-\alpha_oG_o(P)}2.
\tag{6}
\]

Here \(\alpha_0=\alpha_e\), \(\alpha_1=\alpha_o\). Complete inside-bank
catalogues can force a minimum number of such owners. A minimum exceeding
the right side excludes the boundary support even when its area is an
integer. Fractional allocation of contact owners is not assumed to be a
physical realization.

The [polygon implementation and controls](corner-tests/AREA_CYCLE_CUTS.md)
use exact simple boundary walks, including all selected T subdivisions.
They keep valid integer mixed-height holes. Every forbidden finite patch
remains forbidden under any isometry; a transformed patch must still be
contained in the board to become a candidate occurrence. Expanding each
occurrence into its actual supported polygon lets the independent metric
auditor check the new no-good directly, without trusting the pattern
matching procedure or assuming a symmetry of the board.

## Completion and certificate scope

For the completion statement, suppose an interior boundary of the finite
selected union remained. Away from finitely many vertices, it contains
an open subinterval of a selected tile side with empty space on the other
bank. The complete side condition supplies a selected neighbor there,
a contradiction. Exact exterior coverage and positive area then force
the selected union to be the connected board. Its area gives exactly
\(N\) tiles.

A verified UNSAT certificate for any unrestricted finite model satisfying
the stated completeness rules excludes the corresponding board. A model
conditioned on a corner root excludes only that root; all 128 surviving
roots must then be covered. SAT on a partial model, resource exhaustion,
and success on positive controls make neither kind of exclusion.

The independent [semantic and Boolean proof audits](audit/README.md)
separate the geometric generation rules, the finite formula encoding,
and the actual refutation trace. No target refutation is claimed here.

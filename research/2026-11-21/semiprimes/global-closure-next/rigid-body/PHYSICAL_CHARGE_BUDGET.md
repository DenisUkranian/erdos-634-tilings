# A finite global budget with rigid placements and signed charges

21 November 2026. **Neither 3431 nor 5063 is excluded by this theorem.**
It gives a precise finite obstruction criterion combining actual contacts,
nonoverlap, integer choices, and the number of tiles available to complete
the odd and even signed charges. It also explains why writing down the
hard-body model is not itself a nonexistence proof.

## 1. Physical rows and the finite candidate set

Fix the triangular board and the congruent triangular tile. Use actual
endpoint/direction rows: a directed side contributes at its two physical
endpoints, with the actual unoriented line direction retained. Let `b_r`
be the board's coefficient at row `r`, in one consistent sign convention.

Choose any finite set `R_0` of such rows. Let `V(R_0)` consist of **all**
admissible actual congruent placements which have a nonzero coefficient
at at least one row in `R_0`. There are at most 24 geometrical placements
at a specified endpoint and line direction: three choices of side length,
two rays, two assignments of the other side lengths, and two sides of
the line. Consequently

\[
 |V(R_0)|\le 24|R_0|.
\]

Exact containment and any independently proved necessary boundary
arithmetic may remove candidates. Arbitrary resource cutoffs may not.
This is the complete-row oracle already implemented in the
[whole-board search](../../../../2026-11-20/semiprimes/continuation/global-endpoints/integer/README.md).

Join two candidates in a graph `H` when their open interiors overlap.
Each vertex means one complete rigid triangle in one actual position,
not an independently selectable collection of its sides. Distinct keys
for the same physical placement are either canonicalized or made
mutually incompatible.

In the established orientation and phase framework let
`g_o(P)=epsilon(P)` for an odd-height tile and zero otherwise, and
`g_e(P)=epsilon(P)` for an even-height tile and zero otherwise.
In the path frame the complete target charges are

\[
 (G_o,G_e)=(c,d),\qquad d=a-b.
\]

In the standard frame both signs are reversed. These character identities
are inputs proved in the
[actual-median note](../../../../2026-11-20/semiprimes/continuation/charge-transport/geometry/ACTUAL_MEDIAN_CHARGES.md),
not consequences assumed for a partial packing.

## 2. Global physical charge-budget theorem

Let `F(R_0)` be the finite collection of subsets `I` of `V(R_0)` such that

1. `I` is independent in `H`, so its actual triangles have disjoint interiors;
2. every selected physical row balances:

\[
 \sum_{P\in I} C_r(P)=b_r\qquad(r\in R_0).
\]

Define the signed charges of this partial selection by

\[
 g_o(I)=\sum_{P\in I}g_o(P),\qquad
 g_e(I)=\sum_{P\in I}g_e(P).
\]

The minimum over an empty feasible collection is `+infinity`.
Every complete `N`-tiling satisfies

\[
 \boxed{N\ \ge\ L(R_0):=
 \min_{I\in F(R_0)}
 \left\{|I|+|c-g_o(I)|+|d-g_e(I)|\right\}.}       \tag{1}
\]

Thus `L(R_0)>N` is a global impossibility certificate. The minimization
uses integer placement choices, true physical contact equations, and
actual nonoverlap. A fractional relaxation of this minimization may
produce a smaller value and cannot replace its integer meaning.

### Proof

Take a complete tiling and retain precisely its tiles belonging to
`V(R_0)`. They form an independent subset `I`. Every omitted tile has
zero coefficient on every row of `R_0`, by the **complete** enumeration
of the incident placements. Hence `I` satisfies the displayed equations.

The omitted odd tiles have total signed charge `c-g_o(I)`. Each has
charge `+1` or `-1`, so there must be at least `|c-g_o(I)|` of them.
The omitted even tiles similarly require at least `|d-g_e(I)|` tiles.
The two omitted populations and the retained population are disjoint.
Their sum gives (1). This argument does not assume that the remaining
tiles are terminal, balanced, native, or confined to the currently
generated placement pool.

For the two targets the explicit necessary inequalities are

\[
 \begin{aligned}
 3431&\ge \min_{I\in F(R_0)}
  \{|I|+|37-g_o(I)|+|26-g_e(I)|\},\\
 5063&\ge \min_{I\in F(R_0)}
  \{|I|+|43-g_o(I)|+|22-g_e(I)|\}.
 \end{aligned}
\]

The absolute values account for the further tiles needed to repair
the **whole-board** imbalance. They do not assert that such repair
tiles can actually be placed.

### Using the proved odd-population restrictions

Let `n_o(I)` and `n_e(I)` be the retained counts. If `A_o` is any
proved containing set for the full odd population, define

\[
 m_o(I)=\min\{m\in A_o:m\ge n_o(I)+|c-g_o(I)|\}.
\]

The same proof gives the stronger necessary bound

\[
 N\ge \min_{I\in F(R_0)}
 \{m_o(I)+n_e(I)+|d-g_e(I)|\}.                    \tag{2}
\]

For 3431 one may use `A_o={3c,5c,7c,...}`; for 5063 the checked
minimal-mode exclusion improves this to `A_o={5c,7c,9c,...}`.
Restricting either set to values at most `N` is harmless. The additional
three-height localization at 5063 applies only when the chosen total
odd population is `5c`; it must not be imposed on every member of `A_o`.

## 3. Why a complete finite rigid model exists in principle

Start with the six nonzero endpoint/direction rows of the board. At
each stage enumerate every admissible congruent triangle incident to
the rows already found, and add all of those triangles' endpoint rows.
Count one **tile step** each time the expansion passes from a row to
an incident tile. Keep every placement already found.

**Finite-depth completeness.** In the established exact placement
framework, expansion to tile depth `N` contains every tile of every
possible `N`-tiling. No separate height, denominator, or radius cutoff
is required for this mathematical statement.

To prove this, fix a hypothetical full tiling and make its finite
bipartite incidence graph, with a vertex for each of its actual tiles
and a vertex for every endpoint/direction row occurring in those tiles.
Connect a tile to each row where its coefficient is nonzero.

Every component containing a tile meets a nonzero board row. Otherwise
all of that component's rows have zero board coefficient, and every
tile contributing to one of them belongs to the same component.
The full tiling equations then give zero endpoint current for the
entire component. Exact endpoint currents determine the full physical
boundary current: on each actual supporting line the difference is a
compactly supported interval function with zero derivative, hence zero.
Green's area formula would therefore make the sum of the positive
areas of that component zero. This is impossible.

A simple path from a nonzero board row to any chosen tile uses at most
`N` tile vertices. The complete incident oracle includes each step of
that path. The claimed depth bound follows.

The resulting catalogue is finite but can be enormous. Its mere
existence gives no useful runtime or impossibility verdict. It shows
exactly where integrality enters: with `N` actual positive tiles the
number of tile vertices on a simple path is at most `N`. A fractional
mass of `N` need not have support of size at most `N`.

## 4. What is sufficient for a positive or negative verdict

On the finite depth-`N` catalogue, impose Boolean placement choices,
the complete physical endpoint equations at every represented row,
and the count `N`. Then a satisfying assignment is exactly a tiling;
full positive integer current closure already implies containment,
coverage and nonoverlap, as proved in the
[physical-current theorem](../global-strengthening/FULL_CURRENT_AND_NONOVERLAP.md).
Explicit overlap clauses are valid and may improve search propagation.

A rigorously verified infeasibility certificate for a **necessary**
finite projection such as (1) or (2) would suffice for a negative
verdict. Full depth-`N` expansion is not required if a smaller complete-row
projection already yields a certified contradiction.

Temporary finite-pool rows have a different status. If an unfinished
row omits one of its incident placements, its equation can exclude a
real tiling that uses the omitted tile. A conflict using such a row is
not a certificate for (1). This is why the existing solver distinguishes
permanent complete rows from temporary guarded equations.

**No inequality `L(R_0)>3431` or `L(R_0)>5063` has been established in
this continuation.** The theorem formalizes the required global
contradiction; it does not supply one by definition.

## 5. Internal audit

The finite-row quantifier, residual-charge bound, and incidence-component
completeness argument were independently checked within this work.
The existing complete incident oracle has separate exact metric
controls; `verify_rigid_body.py` rechecks a complete 143-tile positive
certificate and exact examples separating periodic, fractional, and
fully physical current systems. These finite controls support the
implementations and distinctions, not a proof-assistant formalization
of the universal theorem.

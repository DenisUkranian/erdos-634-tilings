# One global charge, contact, and tile budget

21 November 2026. **The original counts 3431 and 5063 remain OPEN.**

This continuation derives a necessary theorem valid at every odd-height
population in the established prime-tree framework. It combines the two
prime trees in one physical contact graph, retaining the odd charge,
the area behind the contacts, and the finite number of available tiles.
It does not require a unique odd phase, terminal remote branches, or
the minimal three-height localization.

The later [physical cell-reserve theorem](../continued-rigidity/global/GLOBAL_PHYSICAL_CELL_RESERVE.md)
strengthens the complete-row completion cost using retained cell locations
and rigid minority reserves. Its [continuation package](../continued-rigidity/README.md)
also reduces the four-cell parameter to 31 values and gives exact rational
witnesses for both remaining two-cell native roles. The earlier results
below remain valid with those additional restrictions and method limits.

## Latest continuation: rigid placements and the remaining five-block mode

The newly checked [two-height exclusion](five-block-two-heights/TWO_HEIGHT_EXCLUSION_5063.md)
leaves only `n_1=215` when the full 5063 odd population equals 215.
It excludes all **9,112,001** profiles in a newly derived single-offset
universe using the 65 exact endpoint certificates. Every short height
is consequently 0, 1, or 2. A separate actual-line incidence argument
proves [balance of every 86-tile height-one node](global-strengthening/TWO_BLOCK_BALANCE_5063.md).
The [remaining cell classification](global-strengthening/ONE_HEIGHT_CELL_CLASSIFICATION_5063.md)
has one, two, or four occupied Euclidean classes; in the last case their
sign populations depend on one integer `x=1,...,42`. This is not an
exclusion of 215 or of the larger allowed populations.

At 3431 the [full cylinder lift](exact-lines-3431/CYLINDER_LIMIT.md)
retains actual transverse supporting lines, while reducing longitudinal
coordinates modulo 37. The existing rational 111 profile survives.
An average over 133 contained lattice translates lies in the **convex
hull of real, contained, nonoverlapping integer packings of exactly
111 tiles**. Its charge and cylinder equations hold in the mixture;
they are not asserted in any individual packing. Thus additional linear
inequalities valid for all such packings cannot separate this point.

The same construction now applies to one surviving
[native 215 profile at 5063](exact-lines-3431/native-215-5063/CYLINDER_PACKING_LIMIT_5063.md).
A new exact rational certificate supplies signs `(129,86)` and native
gate currents `(42,1)`. Averaging 410 contained translates gives a
point in the convex hull of actual nonoverlapping packings of exactly
215 tiles, with density at most `43/82`. The profile conditions again
hold only in the mixture. This does not restrict the five-block layer
to a single phase and does not produce an integer realization.

The [physical-current audit](global-strengthening/FULL_CURRENT_AND_NONOVERLAP.md)
shows that full actual boundary-current equality with nonnegative
integer rigid placements already implies exact coverage and nonoverlap.
This logical condition is present in the existing complete physical
model. The [finite physical charge-budget theorem](rigid-body/PHYSICAL_CHARGE_BUDGET.md)
couples actual contact equations, overlap incompatibilities and the
missing odd/even charges in one integer minimization. It also proves
finite depth-`N` completeness of the incident expansion. Neither the
formulation nor its finite-depth bound supplies a target contradiction.

Finally, [exact abstract graph witnesses](global-strengthening/ABSTRACT_GRAPH_LIMIT.md)
show that the earlier larger-population inventories pass the joint
charge, connectivity, centered-area and full covariance tests below.
The available centroid budget remains too large in this projection.

## The main theorem

Cancel actual whole-long-side half-turn pairs as boundary currents,
keeping all their tiles in every population and area calculation.
If `M` tiles remain unmatched, the joint graph `H` has exactly `M`
edges: one per physical unmatched tile. Its vertices are the cuts in
the increasing and decreasing prime trees. A tile joins its two
assigned cuts. At each vertex `e`, set

\[
 F_e=3n_e-Nw_e-(U_e-V_e),
\]

where `n_e` is the full child-subtree population, `w_e` counts its
selected whole exterior sides, and `U_e,V_e` are its two unmatched
crossing-bank populations. Exact signed transport gives `P_e,Q_e`
from the odd and even subtree charges; the actual banks satisfy
`U_e>=|P_e|`, `V_e>=|Q_e|`, with the required parities.

The same graph must carry both unit-magnitude signed charge flows
and a real area flow of divergence `F`. Put `alpha_e=P_e-Q_e` and
`beta_e=sigma_e(P_e+Q_e)`, where the part sign `sigma_e` is +1 in
the increasing tree and -1 in the decreasing tree. Their minimum
squared flow energies satisfy

\[
 \boxed{\alpha^T L_H^\dagger\alpha\le M\le N,
 \qquad\beta^T L_H^\dagger\beta\le M\le N.}
\]

The area flow additionally obeys

\[
 \boxed{F^T L_H^\dagger F\le
 \frac{c^2}{3a^2b^2}
 \left[N\bigl(A^2+B^2+c^4-a^2-b^2-c^2\bigr)
 -(N-M)(a^2+b^2-ab)\right],\qquad M\le N.}
\]

Here `A=b(2a+b)`, `B=a(a+2b)`, `c^2=a^2+ab+b^2`, and `L_H`
is the graph Laplacian with one unit of conductance per tile.
The pseudoinverse can be replaced by an exact rational solve after
grounding one vertex of each connected component. Equivalent inequalities
hold for every real potential and every graph cut. A centering correction
and a tensor refinement retain additional geometric information.

Each active physical-height band of the graph is connected. At a fixed
band its vertex subtrees partition the actual tiles, so sums of their
areas and charges are physical sums rather than repeated ancestor counts.
The signed charges and the area demand must therefore cross the same
sets of available physical contacts.

* [Full joint theorem, charge flows, connectivity, and proof](common/JOINT_CONTACT_GRAPH.md).
* [One-tree corollary, paired-tile reserve, and charge/area elimination](contact-budget/GLOBAL_CHARGE_CONTACT_BUDGET.md).
* [Independent internal proof audit](common/CONTACT_INERTIA_AUDIT.md).
* [Exact geometric control checker](contact-budget/verify_contact_budget.py) and [replay](contact-budget/CONTACT_BUDGET_REPLAY.json).

## What the theorem adds, and what it has not decided

The graph records which two cuts use the same tile. Separate branch
counts lose this incidence information, and adding the two tree budgets
would count a tile twice. The new energy inequality uses the joint
incidences and only one centroid budget. Paired tiles continue to consume
a precisely known part of that budget even after their currents cancel.

To exclude a target with this theorem, one must show that every allowed
integral contact graph, charge assignment, and population assignment
violates at least one of its constraints. That minimization has not been
completed. The board-wide numerical budget alone is too coarse to give
the desired contradiction. This package asserts a global necessary
theorem, not such an exclusion.

The earlier complete [5063 minimal-mode proof](../MINIMAL_ODD_EXCLUSION_5063.md)
still gives `n_odd>=215`. At 3431 the full `n_odd=111` case remains
open. Neither target has a complete positive tiling here.

## A further conditional restriction at 5063

The [odd-branch budget theorem](large-population/GLOBAL_ODD_BRANCH_BUDGET.md)
uses the same physical principle: a subtree charge must pass through
an actual gate of its parent population. In the path frame, an
exterior-free odd exact node of 86 tiles, all positive, forces at
least 301 odd tiles globally; if all 86 are negative, the bound is
387. No terminality or height cutoff is assumed.

The earlier 65-certificate contradiction also extends to a precise
larger-population hypothesis. If the entire height-one layer is the
native class `zR`, with **86 positive and 43 negative** tiles, the
full tiling needs at least **387 odd tiles**. The sign inventory is
an explicit hypothesis, not a consequence of 129 tiles alone.

At total odd population 215, this initially excluded height-one population
129. The newer two-height proof now gives the following complete status
of those former alternatives:

| Odd heights | Height-one tiles | Other odd tiles | Current status |
|---|---:|---:|---|
| `{1}` | 215 | 0 | Open; one, two, or four occupied classes |
| `{-1,1}` | 86 | 129 at height -1 | Excluded by the single-offset proof |
| `{1,3}` | 86 | 129 at height 3 | Excluded by the single-offset proof |

No remaining configuration is asserted realizable.
[Independent internal audit](large-population/LARGE_POPULATION_AUDIT.md)
and [exact arithmetic replay](large-population/ODD_BRANCH_BUDGET_REPLAY.json)
state the proof dependencies and limitations.

## An exact boundary of the 3431 moment method

The existing strictly positive rational periodic witness at mass 111
can be lifted to contained placements preserving all first transverse
endpoint moments and the gate populations. Every periodic column is
replaced by four rationally weighted translates with a common mean
anchor. The exact checker verifies all 16,428 column identities and
65,712 strict containment checks.

Thus these positional moments alone cannot exclude that fractional
profile. The construction permits fractional multiplicities and overlaps;
it does not satisfy the full contact, area, and coverage requirements of
the global theorem.

* [Precise lifting theorem and proof](geometry3431/FIRST_MOMENT_LIMIT.md).
* [Exact lifting checker](geometry3431/verify_first_moment_lift.py) and [replay](geometry3431/FIRST_MOMENT_LIFT_REPLAY.json).
* [Optional numerical diagnostics and their separate scope](moments/README.md).

## Reproduce the finite controls

From the repository root, with Python assertions enabled:

```sh
python3 research/2026-11-21/semiprimes/global-closure-next/contact-budget/verify_contact_budget.py
python3 research/2026-11-21/semiprimes/global-closure-next/geometry3431/verify_first_moment_lift.py
python3 research/2026-11-21/semiprimes/global-closure-next/large-population/verify_odd_branch_budget.py
```

These commands use only the Python standard library. The first starts
from two complete 143-tile coordinate certificates and independently
checks metric, containment, complete boundary currents, both prime trees,
charge transport, centroid identities, exact graph energies, charge-cut
capacities, and active-band connectivity. Both tilings have 60 actual
half-turn pairs and 23 unmatched tiles. A separate abstract graph control
shows that retaining joint incidences can strengthen either individual
tree bound; that control is explicitly not a tiling.

The third checks the new branch-budget arithmetic and the hashes and
accounting of the prior 65-certificate dependency. A fresh full replay
of that dependency is supplied separately by `../replay.py`.

The universal result is a written mathematical proof with internal review.
The finite controls check its formulas and implementation on the stated
inputs; they are not a formal proof-assistant verification or an exhaustive
search of either target. All three commands are included in the root replay
coordinator.

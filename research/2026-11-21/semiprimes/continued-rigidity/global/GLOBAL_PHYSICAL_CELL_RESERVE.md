# A global physical completion budget with cell reserves

21 November 2026. **3431 and 5063 remain OPEN.**

This theorem combines the new rigid unit-cell minority bound with complete
physical contact rows. It strengthens the completion cost of a retained
packing, rather than adding two lower bounds that may count the same tiles.
All odd heights and ordinary phase nodes are allowed.

## 1. Inputs and conventions

Normalize the signed odd charge to `+c` and the signed even charge to
`d=a-b`. This is the path-frame convention; reverse all signs when using
the standard frame. In either convention the charge labels may be normalized
this way without changing any population.

The following facts are established by the
[joint-cell framework](../../../../2026-11-20/semiprimes/continuation/common-obstruction/joint/JOINT_CELLS.md),
[signed phase populations](../../../../2026-11-20/semiprimes/continuation/vertex-phase/SIGNED_PHASE_POPULATIONS.md),
and the [unit-charge minority theorem](UNIT_CHARGE_CELL_MINORITY.md):

* Every odd joint cell has charge `c*g`, for an integer `g`.
* At every ordinary node of either prime tree, the positive and negative
  tile populations are separately divisible by `c`. Odd nodes are ordinary.
* A cell of charge `+/-c` contains at least `mu` tiles of each sign, where
  `mu=2` for `(33,7,37)` and `mu=5` for `(35,13,43)`.

In particular, every positively charged odd cell has at least `c+mu`
positive tiles. For charge `+c` this is the minority theorem; for charge
at least `2c` it follows from `2c>=c+mu`.

Let `R` be a finite set of actual endpoint/direction rows. Enumerate
**every** contained congruent placement incident to a row of `R`, and let
`F(R)` be all subsets of this complete catalogue that have pairwise disjoint
interiors and balance the board coefficient at every row of `R`. These are
the exact hypotheses of the
[physical charge-budget theorem](../../global-closure-next/rigid-body/PHYSICAL_CHARGE_BUDGET.md).
An arbitrary finite placement pool is not a substitute for this complete
incident catalogue.

For `I in F(R)`, define:

* `P_I,Q_I`: its retained positive and negative odd populations;
* `p_L,n_L`: its retained positive and negative populations in odd joint
  cell `L`;
* `p_max=max_L p_L`, with value zero if no odd tile is retained;
* `n_e(I),g_e(I)`: its retained even population and signed even charge.

The actual positions of the retained whole triangles determine their cells.
One cannot independently allocate their side contacts or relabel their cells
to reduce the cost below.

Let `A_o` be a proved containing set for the full odd population, and write
`round_A(t)=min{m in A_o:m>=t}`, with an empty minimum equal to infinity.
The current choices are

\[
\begin{array}{c|c|c|c|c}
N&c&d&\mu&A_o\\\hline
3431&37&26&2&\{3c,5c,7c,\ldots\}\cap[0,N]\\
5063&43&22&5&\{5c,7c,9c,\ldots\}\cap[0,N].
\end{array}
\]

The independent even-population lower bounds are `b_e=64` and `b_e=32`,
respectively; see the derivation in the global corollary of
[the unit-charge theorem](UNIT_CHARGE_CELL_MINORITY.md). They may be omitted
by setting `b_e=0` without affecting validity.

## 2. Explicit physical cell-reserve theorem

For a retained packing define

\[
T(I)=\max\{P_I+(c+\mu-p_{\max})_+,\ Q_I+c\},
\qquad
O(I)=2c\left\lceil\frac{T(I)}c\right\rceil-c.       \tag{1}
\]

Every full tiling satisfies the finite, globally valid bound

\[
\boxed{
N\ge\min_{I\in F(R),\ |I|\le N}
\left[
\operatorname{round}_{A_o}(O(I))
+\max\{b_e,\ n_e(I)+|d-g_e(I)|\}
\right].}                                             \tag{2}
\]

Consequently a rigorously verified value greater than `N` excludes the
target. The formula uses integer whole-triangle choices, actual contact
geometry, the spatial allocation of retained tiles among joint cells, and
the tile budget still available for charge repair.

### Proof

Take a hypothetical full tiling, and retain precisely its tiles incident
to the rows in `R`. Completeness of the catalogue makes this an element
`I` of `F(R)`.

Let `P,Q` be the full positive and negative odd populations. They satisfy
`P-Q=c` and `P,Q in cZ`. Because the total odd charge is positive, at least
one odd joint cell has positive charge. Its positive population is at least
`c+mu`. At most `p_max` of these positive tiles were retained in `I`, so
the omitted positive population is at least `(c+mu-p_max)_+`. Therefore

\[
P\ge P_I+(c+\mu-p_{\max})_+.
\]

Also `Q>=Q_I`, hence `P>=Q_I+c`. Rounding `P` up to a multiple of `c`
gives (1), since `n_odd=P+Q=2P-c`. The proved set `A_o` supplies the next
rounding in (2).

The omitted even tiles have signed charge `d-g_e(I)` and therefore
number at least its absolute value. This yields the even term in (2).
The full odd and even populations are disjoint; no retained tile is counted
twice. Taking the minimum over all feasible retained packings proves (2).

### Comparison with the earlier physical budget

Without the cell term, the odd charge-repair estimate is

\[
P_I+Q_I+|c-P_I+Q_I|
=2\max\{P_I,Q_I+c\}-c.
\]

Rounding it to the admissible odd populations accounts for the divisibility
by `c`, but not for where the retained positive tiles lie. Formula (1)
adds the unavoidable positive supply for a charged cell. Thus (2) dominates
the earlier residual-charge bound; it is not its sum with an unrelated
cell-population estimate.

For example, if `I` contains at least `c` positive tiles in each of `k`
distinct odd joint cells, every completion satisfies

\[
\boxed{n_{\rm odd}\ge(2k+1)c.}                         \tag{3}
\]

Indeed, if the full positive population were at most `kc`, those `k` cells
would each contain exactly `c` positive tiles and no positive tile could
lie elsewhere. None of them could have positive charge, contradicting total
charge `+c`. Divisibility therefore gives `P>kc`, hence `P>=(k+1)c`.
The earlier count-and-charge estimate for exactly `kc` retained positive
tiles was only `(2k-1)c`.

Equation (3) gives concrete sufficient physical-row targets. If every
feasible retained packing forced by some complete row family contains such
tiles in at least 46 distinct cells for 3431, or 59 distinct cells for 5063,
then the even lower bounds would give contradictions:

\[
64+93\cdot37=3505>3431,\qquad
32+119\cdot43=5149>5063.
\]

No row family with either property has been found. These are explicit
sufficient thresholds, not properties asserted of all tilings.

## 3. Stronger node-rounded completion costs

The explicit bound can be strengthened without knowing the full phase
forest. Fix either prime tree. Let `V(I)` be its odd ordinary nodes met by
the retained packing. Let `C_v(I)` be the finite set of observed joint cells
inside node `v`.

Assign an integer `g_L` to every observed cell, representing its possible
**full** charge divided by `c`. Introduce an integer `h_v` for the aggregate
charge of all other, unobserved cells in node `v`, again divided by `c`.
Define

\[
e_L(g)=\max\{0,\ p_L-cg_+,\ n_L-c(-g)_+,\
                   \mu\,\mathbf1_{|g|=1}\}.             \tag{4}
\]

This is the additional balanced reserve of the *full* cell relative to its
charge, with retained signs already included. It is not an extra population
to add to `p_L+n_L`.

Set

\[
\begin{aligned}
q_v&=\sum_{L\in C_v(I)}g_L+h_v,\\
s_v&=\sum_{L\in C_v(I)}|g_L|+|h_v|,\\
e_v&=\sum_{L\in C_v(I)}e_L(g_L)
                +\mu\,\mathbf1_{|h_v|=1},\\
B_v&=\max\left\{2c,\ cs_v+2c\left\lceil e_v/c\right\rceil\right\},\\
r&=1-\sum_{v\in V(I)}q_v,\\
F(r)&=c|r|+2c\,\mathbf1_{|r|=1}.
\end{aligned}                                          \tag{5}
\]

For this tree put

\[
\mathcal O_\tau(I)=
\min_{g,h}\left\{\sum_{v\in V(I)} B_v+F(r)\right\}.       \tag{6}
\]

The minimization is finite: restrict every `|g_L|`, `|h_v|`, and `|r|` to
at most `floor(N/c)`, as every actual completion must satisfy these bounds.
Additional independently proved gate or charge restrictions may be imposed.
An empty admissible set gives infinity.

In (2) one may replace `O(I)` by

\[
\max\{\mathcal O_1(I),\mathcal O_2(I)\}.                 \tag{7}
\]

These bounds do not add populations from the two prime trees: the maximum
is used because both trees classify the same tiles. A stronger joint
optimization may share the `g_L` variables between the two trees and minimize
the maximum of their two costs. Independent minimizations followed by a
maximum are already valid.

### Why aggregating unobserved cells is safe

Any union of odd joint cells with aggregate charge `+/-c` has minority
population at least `mu`. If one constituent cell has unit charge, its
minority tiles already supply this reserve. Otherwise all nonzero cell
charges have magnitude at least `2c`. Integer charges of magnitude at least
two that sum to `+/-1` must have absolute sum at least five; the union then
contains at least `5c` tiles and at least `2c>=mu` minority tiles. This
proves the `h_v` contribution in (5), with no assumed bound on the number
of unobserved cells.

### Proof of the node bound

In a cell of full charge `cg`, write its full populations as
`cg_+ + e` and `c(-g)_+ + e`. Retention and the minority theorem require
`e>=e_L(g)`. Do the same for the union of unobserved cells in the node.
The node's total balanced reserve is an integer multiple of `c`, because
its positive and negative populations are multiples of `c` and its
aggregate positive-charge and negative-charge parts are multiples of `c`.
Consequently that reserve is at least `c*ceil(e_v/c)`. The node's population
is at least the displayed `cs_v+2c*ceil(e_v/c)`.

An observed node is occupied and cannot consist of exactly `c` tiles: that
would give unit charge with no minority tiles. Its population is therefore
at least `2c`, justifying the maximum in (5).

Unobserved nodes together have charge `cr`. If `|r|=1`, their union has a
positive minority population by the preceding cell argument, and that
population is divisible by `c` by node divisibility. Their population is
therefore at least `3c`. In the other cases `c|r|` is always a valid bound.
This proves `F(r)` and then (6). Every actual completion determines allowed
values of `g,h,r`, so taking the minimum cannot exclude one improperly.

The cost in (6) supplies formal full positive and negative populations
containing all retained signs, with difference `c`. At least one charged
cell or aggregated unobserved part must be positive, and that part requires
at least `c+mu` positive tiles. Hence it also satisfies the argument of
Section 2. In particular, (6) is at least the explicit bound (1).

## 4. Status

The [standard-library verifier](verify_global_completion_budget.py) checks
1,786,484 exact integer comparisons with the earlier rounded charge budget;
the new expression never decreases it. In the stated search range it is
strictly stronger in 83,732 cases for 3431 and 98,566 cases for 5063.
It also checks every displayed spread example and the exact sufficient
thresholds. An independent small abstract population model supplies 376,449
retained-node accounting checks, 82,062 full odd-population checks, and 1,434
checks of the unobserved-unit-charge aggregation. The
[replay](GLOBAL_COMPLETION_BUDGET_REPLAY.json) records the ranges and scope.
These are arithmetic controls of the proved formulas, not physical
infeasibility certificates.

An independent internal proof audit also checked the optional node
optimization: the hidden-cell aggregation, reserve divisibility, observed
and unobserved node floors, cost parity, and domination of the explicit
formula. No gap was found in that audit.

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/global/verify_global_completion_budget.py
```

Equations (2) and (6) are global necessary inequalities with explicit
completion costs. They do not assume a terminal branch, a fixed height
range, or a specified total odd population. Their geometry is supplied by
the complete physical-row selection; their reserves use the independently
checked rigid-cell theorem. The inequalities still require a concrete
row family or additional structural argument that makes the minimum exceed
the available population. No such contradiction has been obtained for
3431 or 5063.

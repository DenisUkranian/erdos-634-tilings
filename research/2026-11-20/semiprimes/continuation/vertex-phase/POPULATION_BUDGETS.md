# Per-node population constraints for unrestricted endpoint projections

20 November 2026. These are necessary conditions for the two target boards.
They do not establish a tiling or a nonexistence certificate. The implementation
uses two separate valuation-tree models, never the sum of their costs.

## Mathematical inputs and scope

The tile is primitive, with odd sides a>b>0 and c^2=a^2+ab+b^2. The supplied
phase arithmetic additionally requires prime c and is used for c=37 and 43.
The board has vertices 0, b(2a+b), and a(a+2b)*rho, with rho=exp(i*pi/3).
Its tile count is N=(a+2b)(2a+b).

The existing `phase-height/PHASE_BRANCHES.md` provides the following facts
for each of the two Eisenstein valuation trees, with the height direction
reversed for the second tree.

* Each tile belongs to one short-height phase node.
* Every ordinary node has population zero or a multiple of c at least 2c.
* The sole exceptional node is the integral height-zero core, whose population
  is congruent to j=N mod c, where 0<j<c.
* An exterior-free ancestor of an occupied descendant can be empty at most
  once in the whole tree.

The companion no-remote-gaps theorem strengthens the last input for the 3431
and 5063 boards: every such ancestor is occupied. The implementation's
`--no-phase-empty` option is therefore explicitly restricted to these two
side triples. The known 143 control is checked with the general allowance.

## Finite projection with auxiliary population blocks

Generate any finite set of physical placements and endpoint equations. For
each tree, include every short node of a generated placement and every
exterior-free ancestor required by one of them. Also include the core even
if it has not yet appeared among the placements. Attach an auxiliary
nonnegative integer k_v to every included node.

For the core, its allocated capacity is j+c*k_v. For an ordinary node the
capacity is c*k_v and k_v=1 is forbidden. If m_v is the number of selected
generated placements belonging to v, impose

    m_v <= j+c*k_v       at the core,
    m_v <= c*k_v         at every ordinary node,
    sum_v k_v <= (N-j)/c.

A selected tile also forces every listed exterior-free ancestor flag. A
forced ancestor needs k_v>=2, except that the general model permits one
explicit exceptional empty flag e_v. An empty flag requires k_v=0. In the
two target boards' strict mode every e_v is false.

These conditions include ordinary nodes that contain exterior headings;
they are stronger than charging only a constant 2c for remote ancestor
flags and counting known exterior tiles separately. They also round each
known population up to its allowed c-block capacity.

To prove necessity, take any actual tiling and select exactly its generated
placements. For each included node set k_v to its actual population divided
by c, subtracting j at the core first. These numbers satisfy all individual
constraints. Included short-node populations are disjoint, so their sum
cannot exceed N. Nodes and placements omitted from the finite model can
only weaken the inequality. The cited ancestor theorem supplies the flags
and the allowed empty-node count. Apply this argument independently to
each tree.

The constraints do not say that the selected generated placements already
fill the capacities. The unused capacity represents other, ungenerated
placements and is essential to the unrestricted quantifier argument.

## Boolean encoding

Let K=(N-j)/c. Each k_v is encoded in `K.bit_length()` binary variables.
The global weighted pseudo-Boolean inequality is simply sum k_v<=K.
For an ordinary node the binary value one is forbidden by

    least_significant_bit => some higher bit.

Selecting any known placement in that node forces some higher bit, hence
k_v>=2. If the entire generated group has at most 2c members, that implication
already supplies its population inequality. Larger groups receive the exact
inequality m_v<=c*k_v. The core receives its analogous inequality as soon as
the generated group has more than j members.

All weights can be positive. For B binary bits, rewrite the ordinary bound as

    m_v + c*sum_i 2^i*(not bit_i) <= c*(2^B-1),

and add j to the right-hand side for the core. No floating-point quantity or
integer-arithmetic solver theory is used. Current group and global bounds
are installed in the temporary query scope, as is the existing whole-pool
tile-count cap. They are emitted again for every query and remain active
when a proposed unconditional UNSAT is rechecked without row assumptions.
Obsolete weaker bounds are not accumulated across queries.

## A safe allocation normal form

Auxiliary capacities may be reduced when they exceed all requirements of
the current finite projection. If an ordinary node has M generated placements,
one may restrict k_v to at most max(2,ceil(M/c)); at the core the upper bound
is max(0,ceil((M-j)/c)). This is a normal form for auxiliary witnesses, not a
physical upper bound on the node population of an unknown tiling.

Indeed reduce any larger k_v to this value. Every selected group still fits,
every required ordinary ancestor still receives at least two blocks, the
forbidden value one is avoided at ordinary nodes, and the global upper bound
only becomes easier to satisfy. Empty flags are unchanged. Thus every
satisfying assignment of the original projection has one in the stated
normal form with exactly the same selected placements. When M<=2c an
ordinary allocation can be just zero or two, eliminating most unused binary
degrees of freedom. These upper bounds are also query-scoped because M can
grow in later expansions.

## Verification and limitations

`verify_populations.py` reconstructs the exact node populations of the known
143-tiling in both trees. It fixes all generated placement variables and every
population bit, flag, and empty-node variable to this explicit witness. It
checks the combined corner/population system, repeats after a complete solver
context rebuild, and rejects the prohibited one-block ordinary population.
The replay output is `VERIFY_POPULATIONS.txt`.

A target response of UNSAT with any temporary endpoint-row assumptions
remains inconclusive. The population bounds do not turn a partial finite
pool into a complete placement catalogue. A positive certificate still needs
the independent exact physical tiling verifier, and a negative result still
needs an unconditional refutation with the mathematical and solver proof
checked independently.

## Signed refinement and parity completion

`signed_population_search.py` uses the independently checked signed population
theorem in `SIGNED_PHASE_POPULATIONS.md`. Its physical tile sign is
epsilon=s*(-1)^j in `Geometry`'s counterclockwise convention. At every ordinary
phase node, the populations of the two signs are separately multiples of c.
The core has separately fixed residues.

| N | Core (+,-) residues | Total (+,-) tiles | Available (+,-) blocks | Even negative-block excess |
|---:|---|---|---|---:|
| 3431 | (19,8) | (1684,1747) | (45,47) | 1 |
| 5063 | (5,27) | (2499,2564) | (58,59) | 0 |
| 143 control | (4,6) | (67,76) | (9,10) | 0 |

In particular the 143 core has minimum signed population 10, not merely its
unsigned residue 3. Every ordinary node has two block allocations k_plus and
k_minus. Their sum is zero or at least two. A selected placement requires at
least one block of its own sign and a nonempty node. Larger generated groups
have their exact separate population-capacity inequalities. Required ancestors
use the same nonempty-node condition and the same audited empty-node policy.

Write P_e,P_o,Q_e,Q_o for the included allocated positive/negative block sums
at even/odd heights; core excess blocks are even. Let Kp,Kq be the two table
budgets and delta the last column. Unknown nodes are handled by the four bounds

    P_e+P_o <= Kp,       Q_e+Q_o <= Kq,
    P_e+Q_o <= Kp+1,     Q_e+P_o <= Kp+delta.

No equality is imposed on an incomplete placement or node pool. These bounds
are exactly the condition that the four partial block sums can be completed
to nonnegative integer totals with odd negative excess one and even negative
excess delta. Equivalently,

    max(P_e,Q_e-delta) + max(P_o,Q_o-1) <= Kp.

The implementation again uses each valuation tree separately. Its allocation
normal form caps an ordinary sign allocation at max(2,ceil(M_sign/c)), retaining
the freedom to allocate a required ancestor's blocks to either sign. Capping
it merely at ceil(M_sign/c) would be unsound when the known group is empty.
Core sign capacities use the corresponding signed residue. Decreasing an
excessive ordinary sign allocation to a value at least two preserves node
nonemptiness, and every global parity bound has nonnegative coefficients, so
these normal forms preserve a witness for every actual tiling.

The odd-height signed block difference is minus one. Therefore an actual
tiling contains an ordinary node with an odd positive block count, which is
at least three. If R is the total number of occupied ordinary nodes, their
blocks cost at least 2R+1. Consequently any finite set of required ancestor
flags has size at most floor((Kp+Kq-1)/2), plus the allowed empty-flag count
in the general model. The strict target limits are **45 for 3431 and 58 for
5063**. This is a bound on actual nodes, not an assertion that the normalized
partial allocation itself must display an odd populated node. The final
code includes this cheap propagation inequality; it was added after the
recorded target runs.

`verify_signed_solver.py` checks exact signed populations on the full 143
control, fixes all placement and auxiliary variables in the combined corner
system, repeats after a rebuild, and rejects a one-block ordinary population.
It also exhaustively compares the four inequalities with an explicit integer
completion search on 20,736 small partial-count quadruples. The output is
`VERIFY_SIGNED_POPULATIONS.txt`.

## Coupling the two trees at each physical height

`joint_height_search.py` strengthens the pair of projections without adding
physical placements. It introduces one common block capacity H_(h,sign) for
each encountered physical short height h and each tile sign. A node at tree
level ell has physical height h=tree_sign*ell. For each tree separately,
require the sum of its included sign-block allocations at h to be at most
H_(h,sign), then impose the same four global parity bounds on the H variables.
The earlier separate-tree bounds are retained only as redundant propagation
constraints.

In a genuine tiling, total sign population at a fixed physical height is
the same whichever valuation tree partitions it. At h=0 subtract the one
fixed core sign residue; at every other height subtract zero. The resulting
population is a nonnegative multiple of c and supplies a common witness H.
The included node populations in either tree are only a subset of that
height's actual population. Thus both tree inequalities hold with this one
witness. There is no addition of the costs of the two trees. The strengthening
comes from bounding the sum over heights of their separate maximum demands.

The two positive-coefficient PB terms for each height/sign encode

    sum(node bit weights) + sum(negated H bit weights) <= 2^B-1.

No physical upper bound on H is introduced beyond the four global budgets.
The control command adds `--joint-heights` to `verify_signed_solver.py`;
it fixes the common H bits directly from the 143 tiling's physical heights.
`VERIFY_JOINT_HEIGHTS.txt` records the full witness and rebuild checks.

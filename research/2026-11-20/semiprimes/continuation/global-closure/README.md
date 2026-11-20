# Global geometric restrictions for the two unit F2 targets

**Subsequent update, 21 November 2026:** the entire 5063 `n_odd=129` mode, including charged remote branches, has now been excluded. Every complete tiling of that board needs `n_odd>=215`. [New proof, exact certificates and complete replay](../../../../2026-11-21/semiprimes/README.md). The account below records the earlier stage; both original counts remain open.

21 November 2026. This continuation concentrates on restrictions for complete
tilings of **3431** and **5063**. Both original existence questions remain
**OPEN**. The new results classify an exhaustive alternative, exclude its
entire minimal-odd subcase, and bound actual contacts in an individual
phase cell. No finite placement search or numerical timeout is presented
as a nonexistence proof.

## 1. An exhaustive alternative for every complete tiling

Use the standard frame

\[
 R=\mathbb Z[\rho],\quad \rho=e^{i\pi/3},\quad
 z=(a+b\rho)/c,\quad A=b(2a+b),\quad B=a(a+2b),
 \qquad T=\operatorname{conv}\{0,A,B\rho\}.
\]

The two targets have tiles `(33,7,37)` and `(35,13,43)`. Each complete
tiling belongs to exactly one of these cases:

1. At least one prime phase tree has an occupied exterior-free short node.
2. Every tile belongs to one of the three fixed short-height/coset pairs
   `h=0, R`; `h=1, A+zR`; `h=2, A+z^2R`.

The second case is equivalent to the absence of occupied exterior-free
nodes in **both** trees. The proof intersects the two exterior-containing
ancestor chains and their exact valuation conditions. It assumes neither
a height cutoff nor a normal form obtained by removing tiles.

[Two-tree classification and proof](spine/SPINE_DICHOTOMY.md).

For the three-cell case, containment gives a complete finite catalogue,
and **all** actual endpoint equations with nonnegative integer tile
variables are necessary and sufficient for a positive tiling. Sufficiency
follows from cancellation of the full boundary current and positivity of
the coverage multiplicities. T-junctions are included. This is an exact
geometric formulation, not a feasibility decision.

Every long edge whose joint phase cell lies outside the three allowed
cells must have its actual whole-long-side half-turn mate. The closed
gate rule follows from the empty descendant subtree in at least one
prime tree. It does not assume that an omitted search variable is absent
from the tiling.

[Complete endpoint formulation](spine/NATIVE_ENDPOINT_COMPLETENESS.md) ·
[Closed gates and integer through-contact offsets](spine/CLOSED_GATES_AND_NATIVE_THROUGH.md) ·
[Independent internal review](spine/AUDIT_SPINE.md).

## 2. The entire three-cell class needs at least five odd blocks

**Theorem.** Every complete tiling of either target in the three-cell
class has at least `5c` tiles of odd short height.

In the path frame the three cells are `R,zR,z^2R`. Only height one is
odd, and its signed population is `+c`. Rotate its coordinates by `1/z`.
For a height-one tile with long endpoint `u=x+y rho`, the two possible
open gates are exactly

\[
 ay-bx\equiv0\pmod c\quad\text{(upward)},\qquad
 ax-by\equiv0\pmod c\quad\text{(downward)}.
\]

All other long gates force half-turn pairs. Integer endpoint potentials
on all `c^2` residues give the following exact bounds. Every permitted
single and every mandatory pair is checked; positions are unrestricted.

| Unit count | Exact lower bound for the odd population | After odd-block divisibility |
|---:|---:|---:|
| 3431 | `140035861/1000001 > 3*37` | **185 = 5*37** |
| 5063 | `194218014/1000001 > 3*43` | **215 = 5*43** |

The independent checker reconstructs CCW polygons and their short-edge
currents, without importing the optimization model. It checks 8,436 and
11,352 single/pair inequalities using integers. The complete positive
143 control has 105 height-one tiles and passes the same projection.

This excludes **every** hypothetical tiling that simultaneously has
`n_odd=3c` and has no occupied exterior-free node in either tree.
Consequently, any remaining `3c` tiling must contain a genuine occupied
exterior-free branch. In fact the previous minimal-odd localization
forces an **even terminal node at height 0 or 2**, with its immediate
parent in the unique occupied height-one layer. This required leaf may
have zero charge; it cannot simply be assigned the whole odd imbalance.
The theorem does not exclude the three-cell class when the odd
population is `5c` or larger.

[Population theorem, exact certificates and proof](spine/BOTH_GATE_POPULATION.md) ·
[Independent projection and integer-certificate audit](spine/AUDIT_BOTH_GATES.md).

The whole remaining `3c` mode also has an explicit phase normal form,
without a three-cell hypothesis. In the standard frame its permitted
classes are

\[
 h=0:rz+R,\qquad h=1:A+zR,\qquad
 h=2:A+rz+z^2R,\qquad 0\le r<c.
\]

This covers all **75** permitted classes at 3431 and all **87** at
5063. Nonzero even classes are exactly the possible exterior-free
terminal nodes. Their parent gate currents obey `Q_r=(a-b)g_r`, where
their node charges are `G_r=cg_r`. Thus their contact currents cannot
be chosen independently of the actual node charges.

[Complete minimal-odd phase classification](median/MINIMAL_ODD_PHASE_CLASSIFICATION.md) ·
[Integer node-current constraints and finite charge profiles](median/PER_GATE_INTEGRALITY.md).

## 3. Capacity of a specified contact phase

The endpoint potentials also give a separate one-cell inequality. If
`P_g` is the number of positive upward tiles using one specified long
gate, and `n_+,n_-` are the complete cell's sign populations, then

\[
\begin{array}{ll}
3431:&222P_g\le43n_+ +179n_-,\\[2pt]
5063:&43P_g\le8n_+ +35n_-.
\end{array}
\]

The statement applies to any one Euclidean phase cell whose short-height
endpoint balance has zero exterior contribution, including a translated
cell in an unrestricted tiling. The precise boundary hypothesis is stated
in the linked proof. The inequalities test all translations and both tile
hands, with no geometric search window.

More explicitly, suppose a real bank uses `m` distinct tiles from that
cell through one gate, and those bank tiles have signed imbalance `K`.
If the complete cell has population `n_L` and charge `G_L`, and both
sign versions have zero exterior weight (in particular, if no outer side
has this short height), then

\[
 \boxed{n_L\ge m+|K+\beta G_L|},\qquad
 \beta=68/111\text{ at 3431},\quad
 \beta=27/43\text{ at 5063}.
\]

This connects an actual contact bank and its charge to the number of
tiles required in its entire cell. It is not just a bound on an abstract
signed inventory.

In the previously established `3c` mode,
`n_+=2c,n_-=c`, so `P_g<=44` and `P_g<=51`, respectively.

For an actual upper median path, write its signed height-one and
height-two step counts as

\[
 J=cn-d,\qquad K=2c-dn,\qquad d=a-b.
\]

Under `n_odd=3c`, every positive height-two path-bank tile is counted in
the specified gate, so `K<=P_g`. The capacity bound excludes **both
`n=0` and `n=1`** on each target, not just the saturated case `K=2c`.
The surviving parameters from this argument are `n=2,3,4` at 3431 and
`n=2,3,4,5` at 5063. Their geometric completions remain undecided.

[Global gate-capacity proof and exact replay](median/NATIVE_GATE_CAPACITY.md) ·
[Independent capacity audit](median/AUDIT_GATE_CAPACITY.md) ·
[Separate review of the general-cell localization](median/AUDIT_GENERAL_GATE.md).

## 4. At 5063, balanced remote branches cannot support the minimal mode

**Theorem.** Every hypothetical complete 5063 tiling with `n_odd=3c`
has a **charged even exterior-free terminal node** at height 0 or 2.
The statement includes arbitrary occupied balanced branches elsewhere;
it assumes no three-cell spine condition.

To prove it, retain all `12c^2` single-tile residue columns in the
native height-one cell. Impose zero signed currents at remote gates,
as would follow if all those even nodes were balanced. No mate
condition is imposed. A new exact integer certificate gives

\[
 n_1\ge \frac{133983098}{1000002}
       =\frac{66991549}{500001}>129=3c.
\]

All **22,188** column inequalities were independently verified from
CCW polygons. Both complete 143 projection controls pass. Thus at
least one remote gate must carry nonzero signed current, and the
node-current identity makes its even terminal node charged.

For such a leaf, `G=43g` with `g!=0`. The existing terminal and
physical-transport theorems then require at least **129 tiles in the
leaf**, and at least **65|g| actual boundary-carrying tiles across its
two banks**, including at least **22|g| height-one parent tiles**.
The parent tiles already belong to the odd population; these numbers
must not be added as disjoint extra populations.

The gate capacities further give `g in {-1,1,2}` at 5063. Across
all remote gates there are at most three positive charge units and
one negative charge unit, because each height-one tile has just one
long side and hence belongs to one gate bin. Consequently a `3c`
tiling at 5063 would have **between one and four charged remote
terminal nodes**. Balanced occupied nodes are still permitted.

[Charged-branch theorem and exact certificate](median/REMOTE_ZERO_OBSTRUCTION_5063.md) ·
[Independent arithmetic and geometric audit](median/AUDIT_REMOTE_ZERO_MINIMUM.md).

## 5. Two ordered quotient states cannot both repeat along a median path

There is also an unrestricted positional theorem for every actual
vertex-simple upper median path. Give each whole long-edge step its
ordered labels in `C_a*C_a*C_a` and `C_b*C_b*C_b`. **No nonempty
consecutive subpath is the identity in both groups.**

The proof first shows that such a subpath would have displacement in
`ab*z*(cR+(a+b rho)R)`. At 5063, the shortest nonzero period already
exceeds the board diameter. At 3431, the six shortest period directions
fail the exact board chord tests, and the next shell exceeds the
diameter. Thus a jointly trivial subpath would repeat its physical
endpoint, contrary to vertex simplicity.

Both known complete 143 controls satisfy the quotient identities. The
target canonical words also have distinct joint prefix states, so this
theorem alone cannot prohibit every upper path. In particular, two
separate noncrossing word reductions do not by themselves force a
jointly trivial interval. The relation to the actual tiled disk remains
essential.

[Simultaneous quotient theorem, proof and geometric checks](topology/SIMULTANEOUS_QUOTIENTS.md).

## 6. Verification and the remaining closure problem

Run the deterministic exact checks from this directory:

```sh
python3 replay.py
```

The replay uses the Python standard library and existing exact project
geometry. It checks saved arithmetic certificates and complete positive
controls. It does not run a placement search or a numerical optimizer.
Optional certificate generators and the geometric search wrapper are
included separately with their exact scope.

The full three-cell endpoint searches at both targets stopped at
resource limits. Their unguarded queries produced no infeasibility
certificate. [Recorded search scope and outcomes](spine/SPINE_SEARCH_STATUS.json).

The unresolved global possibilities are now explicit: a `3c` tiling
using the classified even terminal branches (at 5063 at least one
must be charged), or a tiling with at least `5c` odd tiles, with or
without exterior-free branches. At 3431 the `3c` mode permits at most
three charged remote nodes, and a charged node is not yet forced.
Closing the original counts still requires a contradiction covering
those remaining cases or a complete positive tiling certificate.
No such certificate is claimed in this continuation.

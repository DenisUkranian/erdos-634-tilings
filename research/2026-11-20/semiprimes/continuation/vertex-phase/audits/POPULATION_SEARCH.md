# Independent audit of the phase-population projection

The audit-time paths and hashes below identify the working snapshots. Publication relocates imports, renames the signed replay scripts, and adds the separately checked shared-height explanation and explicit conjugate-tree scope. The final code hashes and fresh executed controls are recorded in [the package replay](../REPLAY.json). These internal audits are not external refereeing.

20 November 2026. Audited files and SHA-256 snapshots:

- `population_search.py`: `e1dc22fa98279a8e61556733dbe81938ef9563dff2cc0ff0c184edb54646a719`
- `phase_budget.py`: `e37952e42c38cb87d8ea93f2a17780b60e54f86d837c6e2b287b945d57327e33`

**Assessment.** I found no unsound restriction in the target-board projection at these snapshots, conditional on the phase-population theorem and the separately audited no-empty-exterior-free-root corollary. One missing input guard was identified during this audit and corrected: the implementation now explicitly requires odd coprime short sides. Previously it accepted, for example, `(16,5,19)`, although the theorem being cited here was stated for primitive odd F2 tiles. The target cases and the 143 control were already within the stated hypotheses.

## Phase-node arithmetic

The Hensel lift is for `r^2-r+1=0`. The chosen first root makes `v_pi(z)=+1`; the other root makes it `-1`. At prime `c`, the rational number `c` is a local uniformizer, so a point `(x+y*rho)/c^e` modulo level `l` is determined by `x+y*r mod c^(e+l)`. Removing common powers of `c` from this residue and its denominator gives a canonical key. If `e+l<=0`, the point lies in the zero coset, as implemented.

I independently compared node equality with exact division in the Eisenstein ring by explicit primes, without using Hensel digits. The primes were `(3,-1)` at `c=7`, `(7,-3)` at `c=37`, and `(6,1)` at `c=43`, together with their conjugates. All **79,800** tested comparisons passed, across both signs, positive and negative levels, rational anchors and unequal denominator representations. Representation-invariance and ancestor-cutoff checks also passed. This finite replay supplements the algebraic justification; it does not replace it.

For `required(tile)`, every omitted level lies at most `-e` and at most the smallest exterior level. The tile anchor and every integral exterior anchor are then in the zero coset, and at least one exterior edge node lies below that ancestor. Thus no exterior-free required ancestor is omitted by the cutoff. Testing one endpoint of an exterior side suffices: that entire edge has a single node at its own height. Reversing the tree replaces height by its negative, as in the implementation.

## Population variables are capacity witnesses

Write `j=N mod c` and `K=(N-j)/c`. The core allocation is `j+c*k0`. An ordinary node allocation is `c*k`, with `k=0` or `k>=2`. The Boolean condition `b0 implies (or b1 b2 ...)` forbids exactly `k=1`. A selected ordinary placement forces `k>=2`. The positive-coefficient pseudo-Boolean inequality is algebraically exactly

`number of selected known own placements <= residue + c*k`.

The global constraint is `sum(k)<=K` separately for each valuation tree. Distinct nodes count disjoint short-height populations. Required exterior-free ancestors are flagged; a flag either receives allocation at least `2c` or uses an empty-node excuse. Excuses force allocation zero, and their total is at most one in the older mode or zero in strict mode. External-spine nodes are not incorrectly forced occupied.

The new current-pool upper caps are valid **existential normalization**, not physical population bounds. Given any genuine tiling, restrict its selected placements to the generated pool. Reduce an ordinary auxiliary allocation to zero if there is no demand, or to `max(2,ceil(m_selected/c))` when selected tiles or ancestor demand require it. Reduce the core allocation to `max(0,ceil((m_selected-j)/c))`. This preserves all own-capacity and flag/exception requirements and decreases the global sum. Since `m_selected<=M_generated`, the implemented caps admit these normalized witnesses. They must not be described as saying that all actual tiles in a phase have already been generated.

## Query scope and rebuild

Current-pool caps are emitted after the live query's `push`, not inserted in the permanent-clause set. The base loop queues `pop` before subsequently added declarations and permanent constraints. Each new query regenerates caps from the current node and placement lists. A rebuild redeclares every stored population variable before replaying permanent clauses, then emits the current caps in the next query.

`check_population_scope.py` exercised the same queued-pop pattern. An ordinary pool growing from one to 75 placements at `c=37` correctly changes its normalized cap from two blocks to three; selecting all 75 with only two blocks is UNSAT. A core pool growing beyond residue 27 correctly permits and requires one additional block. These results persist after rebuilding; the current cap still rejects a fourth ordinary block. The old mode admits one flagged empty node, while strict mode rejects it before and after rebuilding. These are logical projection tests with deliberately overlapping placements, not geometric tiling controls.

Strict `no_phase_empty` is explicitly guarded to `(33,7,37)` and `(35,13,43)`. The existing 143 verifier supplies the separate geometric positive control and was reviewed; this audit does not claim an additional execution of that larger test.

## Meaning of solver outcomes

Every genuine full tiling induces an assignment to the permanent endpoint rows, corner conditions, and these normalized phase-capacity constraints even when many of its placements lie outside the generated pool. Thus a confirmed UNSAT result **without temporary row guards**, followed by an independent encoding/proof audit, can obstruct the unrestricted problem.

An UNSAT result using incomplete-row guards is only a request to expand their incident-placement catalogues. A resource stop is inconclusive. Bare SAT of this necessary projection is not a tiling. A positive candidate still requires all selected endpoint currents to balance, the exact count, and independent metric/coverage verification. No unrestricted UNSAT certificate or target tiling is established by this implementation audit.

Replays added by this audit: `check_phase_independent.py` and `check_population_scope.py` in the parent package directory. Their imports are relocated for this published layout; their check logic is unchanged.

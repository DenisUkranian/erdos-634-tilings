# Independent audit of signed phase populations

The audit-time paths and hashes below identify the working snapshots. Publication relocates imports, renames the signed replay scripts, and adds the separately checked shared-height explanation and explicit conjugate-tree scope. The final code hashes and fresh executed controls are recorded in [the package replay](../REPLAY.json). These internal audits are not external refereeing.

20 November 2026. Audited SHA-256 snapshots:

- `audit/signed_population_search.py`: `f80fdd1e83e078ee19c8eb3bb27c0ea15a7eabfade2b8b8f5f96079afad9c410`
- `audit/joint_height_search.py`: `f40207e155c13e5a9ae6b4d89489c03f3fb768dedad791bb1aa941d3ca5c69e6`
- `audit/verify_signed_populations.py`: `a0086f57557fe246015881a21df17e6271c668db0b2d668452c08a1c80a3a6c1`
- `theory/SIGNED_PHASE_POPULATIONS.md`: `8c638803c264643894c26528711d23c68c35881e058c5c2a8ea9d12b0590ea27`
- `phase_search/phase_budget.py`: `e37952e42c38cb87d8ea93f2a17780b60e54f86d837c6e2b287b945d57327e33`

**Assessment.** I found no unsound restriction in the signed necessary projection for the two target boards. In particular, the current-pool allocation caps and the treatment of omitted nodes are sound. This assessment uses the phase-population theorem and the separately audited no-empty-exterior-free-root result. It is not an independent proof of every prerequisite theorem or a decision of either target tiling problem.

## Signs, residues and parity

For a placement `(q,h,j,s)`, the implemented sign is `epsilon=s*(-1)^j`; it is a direction-character sign, not a geometric area sign. Direct substitution for both hands gives character contributions `(a-b-c)*epsilon` and `(a-b+c)*(-1)^h*epsilon`. The board totals give `P=(N-c-a+b)/2`, `Q=(N+c+a-b)/2`.

The nodewise congruences imply separate ordinary populations `c*k_plus`, `c*k_minus`. The core residues and excess-block budgets are:

| N | Core residues | Full positive/negative counts | Excess-block budgets | Even defect |
|---:|---|---|---|---:|
| 3431 | `(19,8)` | `(1684,1747)` | `(45,47)` | 1 |
| 5063 | `(5,27)` | `(2499,2564)` | `(58,59)` | 0 |
| 143 | `(4,6)` | `(67,76)` | `(9,10)` | 0 |

The core residues are removed once per tree and its excess belongs to even height. Conjugating the valuation reverses the node level, which preserves physical height parity. The core residue sum at 143 is 10, not `143 mod 7=3`; the implementation correctly retains both signed residues.

For partial block totals `Pe,Po,Qe,Qo`, a nonnegative numerical completion has totals `(E,O,E+delta,O+1)` with `E+O=Kplus`. Eliminating `E,O` gives exactly

`Pe+Po <= Kplus`, `Qe+Qo <= Kminus`,
`Pe+Qo <= Kplus+1`, `Qe+Po <= Kplus+delta`.

The equivalence follows by taking the two minimal totals `max(Pe,Qe-delta)` and `max(Po,Qo-1)`. Their sum must not exceed `Kplus`, and any remaining integer slack can be assigned to either total. This numerical completion may use unlisted nodes. It asserts neither geometric completion nor a parity equality for selected catalogue columns.

The final snapshot also uses the valid cardinality refinement `floor((Kplus+Kminus-1)/2)+empty_limit`. In a full tiling, the odd-height signed block difference is -1, so the total number of population blocks at odd heights is odd. At least one ordinary node therefore has an odd number of blocks, hence at least three. If `R_all` counts all occupied ordinary nodes, `N>=r_plus+r_minus+c*(2*R_all+1)`, giving limits 45 and 58 at the targets. Flagged occupied nodes form a subset of these actual nodes, and an old-mode empty flag uses one of the allowed excuses. The new cardinality constraint is consequently valid for partial catalogues even when normalized auxiliary block counts no longer display the actual odd population locally.

## Ordinary occupancy and capacity normalization

The Boolean occupancy predicate correctly means `k_plus+k_minus >= 2`. It allows `(1,1)`, `(2,0)` and `(0,2)`, while excluding `(1,0)` and `(0,1)`. A selected ordinary tile forces its own sign to be present and total occupancy at least two. The own-capacity pseudo-Boolean expression is exactly `m_selected <= residue+c*k_sign`. Omitting that expression when an ordinary sign group has at most `c` generated placements is safe: any selected tile already forces one block of that sign. At the core, omission is safe when the group fits within its fixed residue.

The ordinary per-sign cap `max(2,ceil(M_generated_sign/c))` is an **auxiliary witness normal form**, not an upper bound on the actual signed population of a full tiling. Start with the genuine full populations and restrict selected columns to the generated pool. Reduce every sign block allocation exceeding its cap. Known own demand still fits. Ordinary occupancy remains at least two: any reduced component is still at least two; components at most two are unchanged. Empty-node exceptions stay zero. Reducing core excess to `ceil(max(0,M_generated_sign-r_sign)/c)` similarly preserves demand and has no ancestor-occupancy requirement.

All four global constraints have nonnegative coefficients and are upper bounds. Hence these reductions preserve them, including the existence of numerical omitted-node parity completion. The same argument works separately for both trees; their global sums are not added together.

## Scope, rebuild and controls

Current-pool caps are emitted inside the live query scope. A queued `pop` precedes subsequently inserted declarations and permanent clauses. Rebuild redeclares stored signed symbols and restores permanent clauses; the next query regenerates the current caps. Strict zero-empty-node mode is restricted to `(33,7,37)` and `(35,13,43)`, while the shared phase class asserts odd coprime short sides and prime `c`.

Executed in this audit:

- `theory/verify_signed_populations.py`: passed exact sign and boundary arithmetic for 84 oriented placements per shape, the two targets and 143.
- `audit/verify_signed_populations.py`: passed the known 143 witness, reconstruction after rebuild, one-block rejection and 20,736 numerical parity-completion cases; 13,530 generated placements and 5,026 signed symbols.
- `construction/check_signed_scope.py`: passed mixed-sign occupancy, both sign-specific own-capacity thresholds, independent core residues, ordinary cap growth from two to three, queued-pop scope and rebuild, and strict empty-node rejection on both targets. It also checked omitted-node parity slack and both cross inequalities in both trees of both targets. Its overlapping placements are logical projection controls, not geometric tilings.
- `audit/verify_signed_populations.py --joint-heights`: passed the same 143 control and rebuild with actual signed populations at each physical height fixed explicitly. The final wrapper has 5,138 population/height symbols and 14 generated heights, from -6 through 7.
- `construction/check_joint_height_scope.py`: passed all the prior signed scope controls through the wrapper and direct shared-height tests on both targets. Two trees at the same physical height use one capacity; separating their demands between heights 2 and 4 gives UNSAT where the uncoupled class gives SAT. Both sign capacities, insertion of a new height after queued pop, and reconstruction after rebuild were checked.

No source change was required by this audit. Bare SAT of the necessary model is not a tiling. Guard-dependent UNSAT only calls for catalogue expansion. A global obstruction requires confirmed UNSAT without incomplete-row guards and an independent encoding/proof review. No such global certificate, or positive target tiling, was obtained here.

## Shared physical-height implementation

The additional variables `H[h,sign]` are mathematically sound with `h=budget.sign*node.level`. Each tree's sum of own-node blocks at that physical height may be bounded by the same `H`. Actual signed height populations, with the fixed signed core residue subtracted exactly at `h=0`, supply a simultaneous witness for both trees. The same four parity/global upper bounds can then be placed on `H`. Componentwise normalization of node allocations preserves the two lower bounds on `H`; `H` itself could be reduced to their maximum. This combines the two trees without adding their counts.

In `joint_height_search.py`, the positive-coefficient PB form is exactly `sum(node_blocks)+((2^width-1)-H)<=2^width-1`, hence `sum(node_blocks)<=H`. The two trees generate separate inequalities sharing the same `H`; the implementation never sums their demands. It introduces no extra current-pool upper cap on `H`. Height symbols are registered with the signed declaration list and consequently survive rebuild. Coupling inequalities and all four height-level upper bounds are regenerated within each query, using the current node groups. I found no scope or coupling error in the final wrapper snapshot above.

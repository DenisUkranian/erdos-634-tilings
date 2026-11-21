# Signed populations and shared physical-height capacities

`joint_whole_edge_search.py` is a second optional driver. It combines
the existing whole-tile geometry with the historical signed phase-node
and shared-height allocation factories. The unsigned driver and its
controls remain separate. Neither driver has established a full
exclusion of 3431 or 5063.

The class exported for other optional geometric wrappers is
`JointWholeEdgeSearch`. Its base is constructed as follows:

```python
Signed = make_signed_population_search_class(
    SimpleNamespace(Search=PhaseWholeEdgeSearch, atmost=core.atmost),
    PhaseBudget)
Joint = make_joint_height_search_class(Signed)
```

Both historical factories are reused without modification. Their
mathematical inputs are documented in
[`SIGNED_PHASE_POPULATIONS.md`](../../../../2026-11-20/semiprimes/continuation/vertex-phase/SIGNED_PHASE_POPULATIONS.md)
and the
[`independent signed/shared-height audit`](../../../../2026-11-20/semiprimes/continuation/vertex-phase/audits/SIGNED_POPULATIONS.md).
The new wrapper adds explicit query export and physical-driver
integration. Its positive controls check that integration; they do
not independently reprove all the geometric prerequisites.

## Signed allocation

For an actual placement `(q,h,j,s)`, use the established direction sign
`epsilon=s*(-1)^j`. A positive or negative sign labels a whole tile of
positive area. It is not a signed-area or fractional-tile variable.

At every ordinary node in either phase tree, the full populations of
both signs separately are nonnegative multiples of `c`. A nonempty
node contains at least two blocks in total. Thus its two auxiliary
block allocations may be `(1,1)`, `(2,0)`, or `(0,2)`, but not `(1,0)`
or `(0,1)`. Each selected tile forces capacity for its own sign and
positive total occupancy. Required exterior-free ancestors force total
occupancy, with the same target-specific strictness as in the unsigned
wrapper.

The core has fixed residues `r_+` and `r_-`, followed by nonnegative
excess blocks. The whole-board signed totals and remaining block caps
are:

| Board | Core residues `(r_+,r_-)` | Full signed populations `(P,Q)` | Block caps `(K_+,K_-)` | Even defect `delta` |
| --- | --- | --- | --- | ---: |
| 143 | `(4,6)` | `(67,76)` | `(9,10)` | 0 |
| 3431 | `(19,8)` | `(1684,1747)` | `(45,47)` | 1 |
| 5063 | `(5,27)` | `(2499,2564)` | `(58,59)` | 0 |

Here `delta=(a-b+r_+-r_-)/c`, and `K_-=K_++delta+1`.
The core residues are removed once in each description of the same
tiling. In particular, the signed core minimum at 143 is 10, although
the unsigned residue is 3.

Let `P_e,P_o,Q_e,Q_o` be the positive and negative allocated blocks at
even and odd physical heights, after removing the fixed core residues.
Exact elimination of the unknown nonnegative numerical completion
gives these four necessary inequalities:

```text
P_e + P_o <= K_+
Q_e + Q_o <= K_-
P_e + Q_o <= K_+ + 1
Q_e + P_o <= K_+ + delta
```

These allow unlisted completion tiles. They do not assert that selected
columns alone have the final signed totals, or that a numerical
completion has a geometric realization.

## Coupling the two phase trees

Node levels run in opposite directions in the conjugate tree. The
physical height associated with a node is `tree.sign*node.level`.
For each generated physical height and each tile sign, the factory
introduces one common capacity `H[h,sign]` and requires, separately
for each tree:

```text
sum(node allocations at physical height h and sign) <= H[h,sign].
```

The same four signed/parity upper bounds apply to the common `H`
capacities. Actual signed populations at each physical height, minus
the core residue at height zero, supply a simultaneous witness for
both trees. Therefore the two tree costs are not added. Their demands
at the same height share a capacity; demands at different physical
heights consume different capacities.

All placements retain unrestricted exact heights. Recording the
heights of currently generated nodes is a finite projection, not a
cutoff on possible ungenerated heights. The four completion inequalities
allow the omitted population.

## Safe integration and exported source information

The outer wrapper canonicalizes placements before entering the legacy
factory. This is needed because JSON root/checkpoint placements contain
lists, while the exact cached phase-node lookup requires tuple keys.

`query_bounds()` includes every signed and shared-height clause in
`query_count_bound`. `flush()` bypasses the historical signed flush
hook, which otherwise would silently inject a second copy. Permanent
assertions contain node-bit implications and selected-tile requirements.
Own-population capacities, current-pool normalizations, all global
signed/parity bounds, and shared-height coupling are live query bounds.
They are popped and regenerated as the pool grows.

The current-pool per-sign upper caps are existential normalizations
of auxiliary allocations, not upper bounds on the physical populations
of unseen tiles. The historical normalization proof is unchanged:
reducing an excessive sign allocation to its cap preserves selected
own demand; any reduced ordinary component is still at least two,
so total occupancy is preserved. All other allocation constraints are
monotone upper bounds. The shared `H` variables can remain at their
actual values or decrease to the maximum of the two tree demands.

The snapshot field `signed_phase_population_allocation` includes:

- the residues, signed totals, block caps, bit widths and even defect;
- both trees, exact node keys, signed bit groups, own tile indices,
  presence/occupancy expressions, ancestor flags and empty-node excuses;
- the permanent source clauses for every node and tile;
- physical-height keys and their shared signed bit groups;
- the complete query source list and its uncoupled/shared-height parts;
- explicit strict-mode, query-scope and semantic-audit requirements.

The independent model auditor must explicitly recognize and regenerate
this schema before a proof derived from it can be accepted. General
Boolean/PB-to-CNF support alone does not establish geometric necessity.
An unsupported signed/joint snapshot must fail closed. An UNSAT result
under a recorded root is limited to that root; full exclusion needs
the unrestricted model or a checked cover of all root cases.

## Controls and commands

The standard-library replay checks the actual143 metric, area, currents
and nonoverlap, both signed phase partitions, common physical-height
populations, and 13,333 exact numerical parity-completion cases:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/population/verify_joint_wrapper.py
```

The optional native-solver replay is:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/population/verify_joint_wrapper.py \
  --with-solver --workdir /tmp/joint143-control
```

The exact143 witness has signed core populations `(18,20)` and signed
ordinary populations `(49,56)`. Their excess/block counts are `(2,2)`
at physical height zero and `(7,8)` at physical height one. Both trees
give this same physical-height allocation.

The integrated replay installs all 335 actual endpoint rows and all
429 side obligations. It passes SAT with the actual 143 triangles
and allocations fixed, SAT after an equivalent rebuild, and SAT after
regeneration from a geometric checkpoint. Reducing the positive
ordinary-node allocation from seven blocks to six is UNSAT; reducing
the common positive capacity at height one to six is also UNSAT.
An earlier small-pool query is popped before the large model is built,
and the journal confirms that every weighted bound remains at live
query depth one with no duplicate legacy injection.

The recorded model has 12,127 whole-placement variables, 58 and 100
signed nodes in its two trees, 1,610 signed/shared-height auxiliary
variables, 640 signed/shared-height query clauses, and 51,916 permanent
assertions. `JOINT_CONTROL_REPLAY.json` records this local replay. It
uses the same single established 143 construction as the other controls.

The search command is the whole-edge command with the driver changed:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/population/joint_whole_edge_search.py \
  35 13 43 --out /tmp/5063-signed-joint --no-grid \
  --edge-tiles-per-round 8 --vertex-fans-per-round 0 \
  --expand 100 --owner-rows-per-round 150 --rounds 100 \
  --timeout-ms 45000 --time-limit 600
```

Resource limits and satisfiable finite projections remain inconclusive.
This wrapper neither changes the open status of either target nor
adds a proof claim to a bounded search.

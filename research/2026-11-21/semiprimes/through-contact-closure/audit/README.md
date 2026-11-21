# Independent geometry, encoding and finite proof audit

This directory separates three obligations: proving that a finite constraint
is necessary for every physical tiling, translating that finite constraint
to Boolean CNF, and checking an actual finite refutation. Passing controls
for these obligations does **not** exclude either target. No target UNSAT
certificate is asserted here.

Run the verifiers with ordinary Python. Optimized `python -O` execution is
explicitly refused, because exact verification uses mandatory assertions.

## Physical ownership and completeness

The inherited orientation and endpoint formalism is described in
[the global integer audit](../../../../2026-11-20/semiprimes/continuation/global-endpoints/AUDIT_GLOBAL_INTEGER.md).
The required [integer-offset lemma](../../../../2026-11-20/semiprimes/continuation/first-cuts/CORNER_RAYS.md)
has no edge-to-edge hypothesis. A maximal connected straight run is
partitioned into whole sides on each bank. Every side length is an integer,
so all its side endpoints have integer distances from a common run endpoint.
In particular, endpoints on opposite banks also have integer offsets.

Fix a vertex `p` of a selected tile and a proposed half-fan ray. A whole tile
whose side passes through `p` on the complementary bank is determined by:

1. a side length in `{a,b,c}`;
2. which of the two remaining side lengths meets the chosen endpoint;
3. an integer offset strictly between `0` and the chosen side length.

These give exactly six unshifted bank shapes and at most
`2(a+b+c-3)` raw through placements: **148** and **176** at the targets.
Containment and necessary exterior boundary arithmetic can remove candidates.
No candidate is removed by a height, phase, denominator or radius cutoff.
Offsets at a side endpoint belong to a corner fan, not a through case.

`through_geometry.py` reconstructs these shapes by the cosine law and signed
area. It does not import the search's inverse placement enumeration. For a
length `L` edge directed with the selected tile on its left, the same six
shapes, shifted by every integer `1-ell <= t <= L-1`, give the complete
opposite bank. The maximum raw size is
`6L+2(a+b+c)-6`, at most **370** and **434** at the two targets. Every open
unit interval has exactly one physical opposite-bank tile. Candidate tiles
covering the same interval overlap in their open interiors, so an
unconditional at-most-one clause is valid.

Every physical placement has one canonical variable throughout the model.
A single tile may own several contacts. The full143 control has **38** actual
through incidences, **29** distinct owner tiles, and an owner serving **3**
contacts. Requiring a different owner for each incidence would be unsound.

At an exterior point a positive-angle selected corner cannot coexist with
a through tile occupying the same interior half-plane. Thus only the
prescribed exterior fan is needed there. In the interior, a physical vertex
has either a full fan or one through tile and a complementary half-fan. The
irrational angle relation leaves the finite angle states used by the oracle.

## Why a finite model is globally necessary

An installed endpoint row includes **every** contained rigid placement
incident to that row, reconstructed independently from its 24 metric
candidates. An installed fan includes every viable corner path. Every
installed half-fan and whole-edge implication includes its entire local
integer-offset owner catalogue before becoming permanent.

Restrict a hypothetical complete tiling to the finite pool of these canonical
placements. Every completed row and conditional local obligation remains
valid: an omitted placement cannot contribute to the completed row or be a
missing candidate in one of its complete catalogues. Unselected finite-pool
tiles impose no conditional contact obligations. Spatial cliques constrain
only their listed placements and need no complete global catalogue.

The finite selected population is bounded by `N`; it is not required to equal
`N`. With the standard sign `epsilon=s*(-1)^j`, the inherited signed totals
are `G_odd=-c` and `G_even=-(a-b)`. Consequently the four finite-pool capacities
are

\[
\sum_{\substack{h\text{ odd},\,\epsilon=-\sigma\;\text{or}\\
                 h\text{ even},\,\epsilon=-\tau}}x_T
\le \frac{N+\sigma c+\tau(a-b)}2,
\qquad \sigma,\tau\in\{-1,1\}.
\]

These are simultaneous bounds on overlapping populations. They must not be
added as disjoint costs. They apply to all odd populations and all heights.

An UNSAT result for this complete finite necessary model would exclude every
tiling in its explicitly recorded root branch. To exclude the board by root
cases, the separately checked exhaustive three-corner list and **every**
surviving case must be covered. A timeout, resource stop or incomplete proof
does not remove any root.

## Exact semantic audit

`verify_snapshot.py` imports no search oracle, inverse placement code or SMT
solver. It independently checks:

- canonical, distinct, contained whole triangles;
- all exterior unit intervals and complete endpoint catalogues, endpoint
  signs, row equations and same-bank endpoint cliques;
- complete fan recursion and owned full/half/exterior fan implications;
- complete integer-offset owner catalogues and owner cliques;
- strict spatial point cliques, common open angular sectors and overlap pairs;
- whole-edge catalogues, spans, unit coverage obligations and bank cliques;
- target-specific supported long-cycle witnesses, with their inherited
  pure-cycle theorem checked separately by the package replay;
- optional ordinary phase-node flags and separate tree budgets, with
  independently enumerated Hensel digits and the inherited no-empty theorem;
- unsigned and signed population allocations, all selected sign/node
  capacities, and common physical-height capacities for the two prime trees;
- general supported polygons: exact simple boundary, representative tile-side
  support, area integrality, both signed characters, charge capacity and parity;
- retained root assumptions, source hash, total count and all four charge caps;
- equality of the complete regenerated and supplied permanent assertion sets.

An unrecognized extra assertion is rejected. The mathematical orientation,
integer-offset and signed-charge theorems are stated inputs to the finite
audit. The optional phase and supported-cycle families additionally rely on
the inherited target-specific theorems. Their board and arithmetic controls
are part of the package replay. The root file's exhaustive coverage is the
separate corner verifier's responsibility. This audit confirms an individual
model, not satisfiability or unsatisfiability.

Population allocation upper bounds are **current-pool witness normalizations**.
They are not upper bounds on an unknown physical node population. A real
completion supplies integer block capacities; these can be decreased to the
smallest capacities meeting the currently selected demands and required
ancestor occupancy. Such decreases preserve all global upper-bound budgets.
The auditor regenerates these caps in the exported query conjunction and
checks that only the fixed bit, occupancy and selected-tile implications are
permanent. Signed allocations keep the core sign residues, the four exact
parity-completion inequalities, and the shared physical-height capacities.
They never add the same physical population once for each prime tree.

The unsigned143 snapshot passed with 1,088 allocation variables and 196
weighted query clauses. The signed/joint143 snapshot passed with 1,610
allocation variables, 640 query clauses and six common physical heights.
Larger intermediate target snapshots have also been
audited, but their report hashes identify the particular saved states; they
are not final target certificates or solver refutations.

The frozen 770-variable positive boundary/root model can be checked with seven
deliberately corrupted variants using standard Python only:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/audit/verify_snapshot_controls.py
```

The independently reconstructed supported-polygon controls are:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/audit/verify_area_audit_controls.py
```

They check ten forbidden supports, reject thirty altered witnesses, and
refuse to forbid the three saved compatible mixed-height cycles. A pattern
search may discover translated, rotated or reflected occurrences of a
forbidden support. Exporting each occurrence as a concrete polygon witness
lets this audit check its actual geometry without trusting pattern matching
or assuming that the isometry preserves the whole board.

The full143 model also passed: 36,434 whole placements, 335 complete rows,
17,804 fan states, 1,195 complete owner catalogues and 19,109 permanent
assertions. Its recorded SHA-256 identifies the exact snapshot checked;
later search snapshots must be checked again.

To audit a fresh snapshot (plain JSON or gzip-compressed JSON):

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/audit/verify_snapshot.py necessary_model.json --verbose --report snapshot_audit.json
```

The reported model hash is taken after decompression, so compressing a saved
canonical JSON snapshot does not change its mathematical input identity.
Reports explicitly list each recognized optional metadata family, including
families with no cuts in that snapshot.

## Boolean encoding and proof replay

`proof_cnf.py` is a deterministic independent encoder for the exported Boolean
grammar. It supports literals, Boolean connectives, at-most cardinalities,
unit-weight exact cardinalities and positive-integer weighted `pble` bounds.
Weighted binary counters and Tseitin gates encode the
conditions without an SMT library. All source assertions, root assumptions
and explicit query count bounds are retained. Truth-table controls cover
**106 formulas / 474 input assignments**, including constants, repeated and
complementary literals.

`check_drat.py` uses standard Python to check the native SAT proof format:
all initial clauses, one bijective signed variable renaming, every RUP or RAT
addition, and a derived empty clause. It conservatively ignores deletions
and checks every subsequent addition against all retained clauses. This
policy is sound but can reject a deletion-sensitive valid proof. Exact
initial unit reduction is independently regenerated when used. A solver's
`unsat` string or an UNSAT core is never accepted as the proof itself.

Five frozen CNF/DRAT controls, an explicit RAT control and six invalid-proof
rejection tests run without any installed solver:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/audit/verify_proof_pipeline.py --replay-only
```

The optional generation path uses local `libz3.so.4` native SAT to propose an
ASCII DRAT trace, then runs the independent checker. It has been tested with
Z3 4.13.3. Proofs may be too large for this deliberately small checker; this
is a resource limit, never an exclusion.

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/audit/proof_cnf.py necessary_model.json candidate
python3 research/2026-11-21/semiprimes/through-contact-closure/audit/run_cnf_proof.py candidate.cnf candidate.drat --timeout-ms 60000
```

All three links are needed for a target certificate: the geometric snapshot
audit, equivalence of its exact CNF export, and a successful independent
refutation replay. Root-conditioned certificates additionally need exhaustive
root coverage. None is substituted by positive controls.

`verify_refutation.py` composes these three checks without importing a solver:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/audit/verify_refutation.py necessary_model.json candidate.cnf candidate.drat --propagated-cnf candidate.drat.propagated.cnf --report refutation_audit.json
```

Omit `--propagated-cnf` only when the proof's initial clauses are the original
CNF (for example a refutation by initial unit propagation). A root-conditioned
result is labelled `VERIFIED_ROOT_UNSAT`; it does not claim exhaustive root
coverage. No target report from this command has been produced.

## Review of the global contact theorem

The opening hypothesis of [GLOBAL_CONTACT_THEOREM.md](../GLOBAL_CONTACT_THEOREM.md)
now explicitly includes the complete exterior interval catalogues before any
further finite placements or local obligations are chosen. This is essential:
an arbitrary finite pool, including the empty pool, need not contain a full
tiling's exterior covering tiles. With the stated hypothesis, restriction of
any full tiling to the finite pool preserves exterior coverage and every
installed complete endpoint, fan and whole-bank obligation. Unqueried
interior placements remain possible.

The signed reserve follows from the two whole-board characters and therefore
applies without a fixed odd population. The ordinary-node bound counts exact
short-node populations, which are disjoint within one prime tree even when
the nodes lie on a common ancestor chain. The extra odd block belongs to the
full ordinary population; it need not lie in the selected subset. The two
trees' costs are not added. Their shared-height capacities dominate each
tree's same-height sum separately, as the signed/joint audit checks.

For the converse, the selected union is a finite closed polygonal subset of
the board. If it covers the exterior but is a proper subset, a nonempty gap
has an interior boundary segment. Away from the finitely many tile vertices,
that segment is an open part of a selected side with an empty opposite bank.
The condition on every selected interior side supplies a selected neighbour
there and gives a contradiction. Containment and full pairwise nonoverlap
are hypotheses of this converse; passing a partial collection of point or
contact cuts does not establish them. The completed union's area then gives
exactly `N` tiles. No further scope gap was found in this formulation.

# Independent audit of whole-edge banks and supported-cycle cuts

21 November 2026. **Neither 3431 nor 5063 is excluded.** This is a
separate implementation and mathematical-scope review of the new
whole-edge driver, its supported-cycle hook, and the optional phase
budget wrapper. It is not an external expert endorsement or a formal
verification of the entire project.

The review found no soundness issue in the inspected implementation.
The controls below distinguish successful preservation of a known
tiling, rejection of a deliberately invalid local assignment, and the
additional effect of a global geometric theorem.

## Whole opposite banks are complete local catalogues

For a selected side parametrized by `[0,L]`, an opposite tile's side of
length `ell` can start at any integer offset

\[
1-\ell\le t\le L-1.
\]

These are exactly the integer offsets with positive-length intersection.
The [integer-offset lemma](../../../../2026-11-20/semiprimes/continuation/first-cuts/CORNER_RAYS.md)
applies because the selected side supplies an actual endpoint on the
straight run. It imposes no unjustified condition on an arbitrary
interior point. The oracle enumerates both endpoint orders for each of
the three side lengths on the opposite bank. The six reference shapes
are translated before containment is tested, so a reference placement
outside the board cannot hide a valid translated neighbor.

All contact endpoints are integral in this coordinate. Requiring each
open unit interval to be covered therefore covers the whole selected
side except its finitely many endpoints. The conditional coverage
clause is active only when the selected tile is present. The at-most-one
clause for its opposite-bank candidates is valid unconditionally: two
such triangles covering the same open unit interval have overlapping
interiors on that bank. No local orientation, height, or population
restriction was added to the catalogue.

Every candidate is inserted through the common exact tile registry.
The same triangle can satisfy many unit intervals and several different
contact obligations, but has one Boolean variable and consumes one
unit of the global tile budget. The joint control explicitly checks
coordinate-denominator aliases and orientation representatives `j+6`.

## Permanent assertions, rebuilds, and geometric restart

The inherited driver flushes construction before pushing the temporary
count query. After a SAT result it queues `pop` **before** adding overlap
clauses, complete endpoint rows, whole banks, or supported-cycle cuts.
The refinement hook therefore installs those necessary clauses at
solver depth zero, even though the pop and subsequent assertions can
be sent in one batch.

The new [joint checker](verify_joint_encoding.py) exercises exactly
that queued-pop sequence. It inspects the serialized SMT commands,
checks that every recorded permanent assertion occurs at depth zero,
and repeats the positive and negative queries after rebuilding the
solver. Rebuild also redeclares the inherited corner-fan auxiliaries
and the optional phase auxiliaries before replaying their definitions.
The production driver respects this ordering; the installation methods
are not an API for adding permanent clauses inside a live query scope.

The inspected geometric restart regenerates complete rows and actual
contact obligations. It rechecks overlap geometry and reconstructs
supported cycles. It does not import arbitrary saved SMT assertions or
the previous branch's root literals. The current root is supplied
explicitly. The known 143 tiling survives this restart.

## The cycle conjunction has the stated global scope

[LONG_CYCLE_CUTS.md](LONG_CYCLE_CUTS.md) audits the inherited supported
pure-mesh cycle theorem and the helper's exact witnesses. That theorem
applies to both target shapes at every height and translation. It does
not apply to arbitrary mixed-height cycles or to the 143 control.

The implementation merges identical undirected physical long sides
before graph traversal. Opposite-bank copies of one side cannot create
a two-edge cycle. A returned simple cycle uses one selected supporting
triangle per distinct side. Its no-good remains necessary even when
other selected triangles in the current partial Boolean model overlap
or leave open endpoint rows: a full completion containing those cycle
supports would still contradict the geometric theorem.

For each target the integration control uses three contained,
nonoverlapping triangles supporting a triangular long-side cycle.
All nine whole-edge obligations are installed. This finite necessary
model is SAT before the cycle clause. Requiring all three supports
becomes UNSAT after the clause; requiring only the first two remains
SAT. Both results persist after rebuild. This demonstrates a real
strengthening of the local necessary model, not a complete target or
corner-root exclusion.

## Optional separate phase budgets

The wrapper uses the exact existing `PhaseBudget` node arithmetic.
A selected triangle forces its own ordinary short node and every
exterior-free ancestor returned by the complete ancestor calculation.
Only the ancestors use the target-specific
[no-vacant-ancestor theorem](../../../../2026-11-20/semiprimes/continuation/vertex-phase/NO_PHASE_GAPS.md).
An occupied ordinary own node may be counted even when it is not
exterior-free. The core `(0,0,0)` is excluded from ordinary nodes.

For each prime tree separately, the core reserve `j=N mod c`, the
ordinary-node cost `2c`, and the additional signed-parity block `c`
give

\[
R\le\left\lfloor\frac{N-j-c}{2c}\right\rfloor
=\begin{cases}45&N=3431,\\58&N=5063.\end{cases}
\]

The two tree costs are never added. Unselected placements do not force
their node flags. The wrapper applies these target theorems only to
the two target shapes. The joint control repeats its SAT/UNSAT and
rebuild checks with this wrapper enabled. The independent existing
phase checker compares the Hensel node computation to exact division
by Eisenstein primes, including representation invariance and complete
exterior-free ancestor sets.

## Controls and reproduction

The audit ran on Python 3.12.14, Linux x86-64 with glibc 2.41, from base
commit `fa77b1f1c36dcac3db5be8ffa45f11fb096e59d7` plus this uncommitted
package. The joint replay records hashes of the inspected new modules.
The solver controls require the repository's existing libz3 binding;
the whole-edge geometric replay alone uses the Python standard library.

| Control | Exact observation |
|---|---|
| Complete 143 geometric tiling | All 143 triangles, area, metric, endpoint current, and nonoverlap pass |
| Actual 143 opposite banks | 25 exterior and 404 interior sides; all 2002 unit contacts recovered |
| Delete one actual bank neighbor | All 442 such deletions violate the corresponding selected-side obligation |
| Small bank encoding | Actual selection SAT; one neighbor removed UNSAT; antecedent removed SAT |
| Full 143 solver integration | SAT with 429 whole-side obligations and 335 complete endpoint rows |
| Full 143 rebuild and geometric restart | Both SAT; 12,127 globally deduplicated columns |
| Target cycle supports, banks only | SAT at both targets |
| Same supports with cycle no-good | UNSAT at both targets, including after rebuild |
| Two supports after the no-good | SAT at both targets, including after rebuild |
| Same target checks with phase caps | Same results; declarations and permanent assertion scopes survive rebuild |

Commands from the repository root, all with exit code zero:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/whole-edges/verify_whole_edges.py --with-solver
python3 research/2026-11-21/semiprimes/through-contact-closure/corner-tests/verify_joint_encoding.py --with-phase
python3 research/2026-11-20/semiprimes/continuation/vertex-phase/check_phase_independent.py
```

The first command was rerun with its output and work directory directed
to scratch; its complete JSON output matched
[WHOLE_EDGE_CONTROL_REPLAY.json](../whole-edges/WHOLE_EDGE_CONTROL_REPLAY.json).
The additional complete output is
[JOINT_ENCODING_REPLAY.json](JOINT_ENCODING_REPLAY.json).
The all-height geometric cycle controls and the 128 initial roots per
target are recorded separately in
[LONG_CYCLE_REPLAY.json](LONG_CYCLE_REPLAY.json).

These are targeted correctness controls. They do not assert that every
selected model satisfies all spatial constraints, that every actual
placement has already been generated globally, or that any one of the
128 target corner roots is impossible. A finite necessary model's SAT
status remains inconclusive. Any later root-conditioned UNSAT result
still requires its actual clauses and proof scope to be checked before
it can exclude that root; both targets remain open here.

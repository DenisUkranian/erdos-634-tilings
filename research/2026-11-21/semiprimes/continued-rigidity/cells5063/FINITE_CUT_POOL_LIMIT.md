# The 65 published cell cuts alone do not exclude the two-cell 215 mode

21 November 2026. This is an exact limitation of a **specific finite pool
of necessary inequalities**, not a tiling construction and not a claim
that every periodic endpoint inequality is satisfied.

The remaining two-cell form can have one native 215-tile exact node in the
increasing tree, and a native balanced 86-tile node plus a remote charged 129-tile
node in the decreasing tree. Call the two Euclidean cells `A` and `B`:

| Cell | Increasing node | Decreasing node | Positive/negative tiles |
|---|---|---|---|
| A | native 215-tile | native 86-tile | `(43,43)` |
| B | native 215-tile | remote 129 | `(86,43)` |

The actual parent bank of an increasing-tree gate is the **sum** of
the currents from both cells. Their individual currents are not required
to be multiples of 22. In the decreasing tree each of these nodes is
filled by its one indicated cell.

The following integer current assignment satisfies all 780 symmetry
transforms of the published 65 certificate inequalities, including the
independent cyclic shifts of both gate lists in each cell:

| Cell/hand | Gate 0 | Gates 9, 11, 23, each | Every other gate |
|---|---:|---:|---:|
| A, upward | 8 | -3 | 0 |
| A, downward | 1 | 0 | 0 |
| B, upward | 34 | 3 | 0 |
| B, downward | 0 | 0 | 0 |

The cell charges are respectively `8-3-3-3+1=0` and
`34+3+3+3=43`. The positive/negative current reserves are `(9,9)`
for A and `(43,0)` for B, within their actual sign populations.
All single-cell sign-specific gate bounds also hold.

At the shared native upward node the currents add to 42 at gate 0 and
zero elsewhere. At the native downward node the current is 1 at gate 0
and zero elsewhere. The remote downward node has zero current in
every gate. Hence the complete node equations hold with

\[
 Q_{\rm up,native}(0)=86+22(-2)=42,\qquad
 Q_{\rm down,native}(0)=-43+22(2)=1,
\]

and zero charge units at all other gates. These are the same native
whole-node currents as in the existing one-cell rational 215 witness,
but distributed here across two formal Euclidean cell current lists.

## Exact verification and scope

For every published certificate with integer denominator `D` and
gate tables `lambda_up,lambda_down`, the independent checker verifies

\[
 \max_u\sum_r Q^L_{\rm up}(r)\lambda_{\rm up}(r+u)
 +\max_v\sum_r Q^L_{\rm down}(r)\lambda_{\rm down}(r+v)
 \le D n_L
\]

for both cells and each of the 12 geometric transforms. It reconstructs
the transforms directly, checks certificate hashes, and uses integer
arithmetic throughout. The sign capacities, sign reserves, complete-node
congruences, and fixed native currents are checked separately.

The small witness is saved in
[`TWO_CELL_FINITE_CUT_WITNESS.json`](TWO_CELL_FINITE_CUT_WITNESS.json).
Run `python3 verify_finite_cut_witness.py` for
[`FINITE_CUT_POOL_REPLAY.json`](FINITE_CUT_POOL_REPLAY.json).

No actual residue-column multiplicities, physical placements, or full
endpoint solution are supplied. In fact the new independently verified
[`shared_profile_cut_001.json`](shared_profile_cut_001.json) excludes this
particular assignment: cell B has exact lower population bound
`143166999/1000001`, strictly greater than 129. This does not change the
limitation of the original finite pool. The conclusion is only that
**these 65 certificates cannot
be reused as a complete contradiction for this shared-node two-cell
configuration**. The earlier isolated 129 proof is unaffected: its
complete gate lists belong to one class, which is precisely the
hypothesis absent here.

`probe_joint_gate_cuts.py` is a separate numerical discovery tool. The
saved four-cell fixed-profile infeasibility and free-profile time limit
are optimizer reports only. They are not exclusion certificates and
do not close any further phase skeletons.

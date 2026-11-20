# Independent audit: the 5063 obstruction with balanced remote gates

21 November 2026. The certificate and its geometric application were
checked independently of the LP generator. No remaining defect was
found in the stated conditional obstruction. This audit does not claim
that the complete `3c` mode, or either target tiling problem, is excluded.

## Audited snapshot

* Candidate certificate: `REMOTE_ZERO_MIN_43_IPM.json`, SHA-256
  `6234ed7caa598a9f6929edaf32fad52b946f07ff7c5c7b62b156c8fa148a6a80`.
* Independent standard-library checker: `verify_remote_zero_minimum.py`,
  SHA-256 `c77a4304e738aef5658dd53571e6c642543b0cb27d146bbdbf03b16419fea20b`.
* Exact replay: `REMOTE_ZERO_MINIMUM_REPLAY.json`.

The checker imports neither `remote_zero_minimum.py` nor either
placement-matrix generator. It constructs each triangle from its two
short vectors, orders its vertices counterclockwise, identifies its
short edges by their exact squared lengths, and forms the endpoint
weight from those directed edges.

## Exact arithmetic result

For every one of the `12*43^2=22,188` translated single-tile classes,
with both hands and all six rotations, the checker verifies

\[
 W(T)+\epsilon(T)\mu_{s(T),r(T)}+t\epsilon(T)\le D,
\]

where

\[
 D=1,000,002,\qquad t=3,115,886.
\]

The endpoint tables and remote-gate multipliers are all integers.
Both native-gate multipliers are exactly zero. The largest checked
column score is `1,000,002`; the smallest is `-4,162,910`.
No tolerance is used in these checks.

For a native height-one population with total signed charge `c=43`,
zero short-endpoint current, and zero signed current at every remote
gate, summing the column inequalities gives

\[
 n_1\ge\frac{43\cdot3,115,886}{1,000,002}
       =\frac{66,991,549}{500,001}>129=3c.
\]

The strict integer margin is

\[
 43t-129D=4,982,840>0.
\]

The native currents are unrestricted in this argument. In particular,
no fixed value of the native height-zero charge parameter is needed.

## Model and physical scope

The certificate covers every native height-one anchor modulo `c` in
both axial coordinates. It does not restrict the anchor to a position
box or presume that a finite geometric placement pool is complete.
All columns are single tiles. Neither whole-edge mates nor any special
matching of balanced remote gates is imposed. There is no per-column
population upper bound in the certified score inequality.

The endpoint functional is periodic modulo `c` on the selected native
height-one class and is extended by zero off that class. A long edge
at height one has both endpoints in that class, with equal residues,
or both outside it. Its endpoint weight is therefore zero. There is
no outer side of height one in the F2 board. Thus summing the complete
tilings' endpoint weights really does give zero for the selected
short-height-one population, including partial contacts.

The gate terms are signed tile counts. At a nonnative height-two node
in the increasing prime tree, the exact node equation reads
`dG_v=cQ_v`, because no height-three tile occurs and the node has no
outer contribution. At a nonnative height-zero node in the conjugate
tree, the same identity holds because height minus one is absent.
These are exact phase nodes, not an arbitrary grouping of translations.

In the proved minimal-odd normal form, all odd tiles are in the native
height-one class and their charge is `c`. Every nonnative node just
described is exterior-free and terminal. Therefore, if every such even
node had zero charge, all remote signed gate currents in the certificate
would be zero. The strict bound above would contradict `n_1=3c`.

It follows that a hypothetical 5063 tiling with total odd population
`3c` must contain at least one **charged even exterior-free terminal
node**: at height zero in the conjugate tree or height two in the
increasing tree, in the path frame. It need not be a unit-charge node.
This is an existence-of-a-charged-branch conclusion, not exclusion of
that branch.

## Positive controls

The independent checker also reconstructs the selected population from
both complete 143 controls. This tests the projection semantics, rather
than applying the 43-specific integer table to a different tile shape.
The two populations are 105 and 91, each with signed charge `+7`.
For both, every two-dimensional short-endpoint row is exactly zero,
all remote signed gate currents are zero, and the native currents are
`(up,down)=(14,-7)`.

These controls pass. They illustrate why zero signed current is not a
claim that a gate is empty or that all incident tiles are matched.
The new certificate respects that distinction.

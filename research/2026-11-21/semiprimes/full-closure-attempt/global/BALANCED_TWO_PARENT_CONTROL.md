# A balanced terminal node can have only two parent tiles

21 November 2026. **Neither 3431 nor 5063 is decided here.**

The proposed universal local estimate

\[
 \text{number of parent-bank tiles}\ge2b
\]

for a nonempty balanced terminal node with one accessible parent class
is false. An exact control at the primitive shape `(a,b,c)=(5,3,7)`
has fourteen node tiles, seven of each sign, and only **two** parent
tiles. All sixteen triangles are whole and have pairwise disjoint
interiors. The patch has the same positioned remote/native phase
conditions as the earlier balanced strip and fits strictly inside the
143 target board.

This does not refute a theorem restricted specifically to `(33,7,37)`
or `(35,13,43)`, nor a statement with additional hypotheses on the
entire complement of the target board. The proposed local universal
lower bound is what fails.

## 1. Exact coordinates

Normalize the node to short height zero and Euclidean class `R=Z[rho]`.
The parent class is initially `z^(-1)R`, where `z=(5+3rho)/7`.
A node label `(x,y,j,s)` denotes the triangle with vertices

\[
 q=(x,y),\quad q-5U_j,\quad q+3U_{j+s},
 \qquad U_j=\rho^j.
\]

The complete node consists of these fourteen labels:

```text
(-7,  2, 2,+1)   (-7,  2, 4,-1)   (-7,  7, 1,-1)
(-5, -8, 1,-1)   (-5, -3, 1,-1)   (-5, -3, 5,-1)
(-5, -3, 5,+1)   (-4,  2, 2,-1)   (-4,  2, 2,+1)
(-4,  2, 4,-1)   (-4,  7, 4,-1)   (-2, -8, 4,-1)
(-2, -3, 1,-1)   (-2, -3, 5,+1)
```

The two whole parent triangles have vertices

\[
 \{(-4,12),(-4,5),(-13/7,60/7)\},
\]
\[
 \{(-5,-13),(-5,-6),(-50/7,-67/7)\}.
\]

Their long edges are the two displayed vertical segments of length
seven. Every parent vertex lies in `z^(-1)R`, and each is a genuine
short-height-minus-one placement of the original tile. Their signs
are opposite.

## 2. Complete current cancellation and terminality

The complete actual short-edge endpoint current of the fourteen node
triangles is exactly the negative of the long-edge endpoint current
of the two parent triangles. This is equality on every actual
supporting line, with unreduced rational endpoints. No periodic
identification is used in that check.

There are four actual whole-long-side half-turn pairs among the node
triangles. The six remaining long edges all have height minus one
and belong to the selected parent class. In normalized coordinates
their beta endpoints `u` satisfy

\[
 5u_x-3u_y\equiv0\pmod7.
\]

Every tile whose long side is outside that selected parent gate has
its exact half-turn mate among the fourteen node tiles. In particular
all height-one node long edges pair. The boundary of the complete
sixteen-tile patch therefore has only height-minus-one directions.
The node is exterior-free and terminal in the tree increasing away
from the parent. There are no unrecorded node triangles in this
explicit polygon patch.

The whole patch is connected through positive-length edge contacts.
It is not an abstract inventory or a mixture of packings.

## 3. The remote/native positions and strict board containment

Apply conjugation, then translate by

\[
 S=z+35+14\rho=(250+101\rho)/7.
\]

Conjugation takes the parent from height minus one to height one.
Since `S in zR` and `S-z in R`, the transformed node class is
`z+R`, which is nonnative, while both parents lie in the unique
native class `zR`. The transformed boundary has only height-one
directions.

All sixteen transformed triangles lie **strictly** inside the
original 143 path-frame board

\[
 \operatorname{conv}\{0,49,55z^2\}.
\]

The checker evaluates all three oriented boundary half-plane
determinants at every vertex. The smallest determinant is `741/7`,
which is strictly positive. It checks all 120 triangle pairs by exact
separating axes and finds no interior intersection.

The patch is a valid counterexample to the local `2b` claim even
with strict board containment and the appropriate phase positions.
Completing its complement to a full tiling is a separate question;
no such completion is asserted.

## 4. Reproduction and provenance

```sh
python3 research/2026-11-21/semiprimes/full-closure-attempt/global/verify_balanced_two_parent.py
```

The verifier uses only the standard library. It reconstructs the
fourteen triangles from the labels, identifies the two parents at
height minus one, checks all metric, sign, current, pairing,
connectedness, phase, and containment statements, and writes
[BALANCED_TWO_PARENT_CONTROL.json](BALANCED_TWO_PARENT_CONTROL.json).

The optional discovery script `probe_balanced_terminal.py` found
this support with binary variables in a selected coordinate window.
The positive witness and its independent exact verification are the
result. A finite search failure, a solver lower bound in that window,
or a timeout would not establish an unrestricted minimum.

The earlier [balanced b-strip](../../charged-branches/BALANCED_SHORT_STRIP.md)
remains a correct construction at the two targets; its `2b` parent
count was expressly never claimed to be a general lower bound.

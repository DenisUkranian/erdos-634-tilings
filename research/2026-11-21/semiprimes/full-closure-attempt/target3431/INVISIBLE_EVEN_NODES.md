# Every occupied remote even cell has an actual parent contact

21 November 2026. A geometric consequence of the existing supported-cycle
theorem. **3431 and 5063 remain OPEN.**

## 1. Statement and scope

Work on either target board, with primitive tile `(a,b,c)=(33,7,37)` or
`(35,13,43)`. Use the path frame, `R=Z[rho]`, and
`z=(a+b*rho)/c`. Assume the three-height, one-native-odd-cell normal form:
all short heights are 0, 1, 2, and every height-one tile belongs to the
single native cell `zR`. The possible even cells are

\[
L_r^-=rz+R\quad(h=0),\qquad
L_r^+=rz+z^2R\quad(h=2),\qquad 0\le r<c.
\]

Call the cells with `r!=0` remote. The hypotheses hold throughout the
established [3431 minimal-odd normal form](../../../../2026-11-20/semiprimes/continuation/global-closure/median/MINIMAL_ODD_PHASE_CLASSIFICATION.md).
They also hold in the native one-cell, three-height subcase at odd
population 215 for 5063. No unrestricted assertion about larger odd
populations is made here.

**Visibility theorem.** Every occupied remote even cell has a
positive-length contact between one of its short sides and the long side
of a height-one tile. In particular, its associated parent long-edge gate
contains at least one odd tile.

The proof also shows that no occupied remote even cell can have its
**actual oriented short-edge boundary chain identically zero** after its
own internal cancellations. This refers to segments on actual supporting lines. Zero
signed gate current, zero periodic endpoint current, or equality of
residue mate counts does not assert this geometric cancellation.

## 2. Geometric inputs

The [joint-cell contact argument](../../../../2026-11-20/semiprimes/continuation/common-obstruction/joint/JOINT_CELLS.md)
places all endpoints on a maximal straight run of height `h` in the same
Euclidean edge cell: their physical offsets along the run are integers.
Consequently, short edges of another even cell cannot cancel the short
edges of the chosen cell. A remote even cell has no positive-length
exterior boundary interval at its short height.

The [one-accessible-gate theorem](../../charged-branches/ISOLATED_GATE_TERMINAL_COST.md)
gives actual whole half-turn mates, within the same even cell, for every
long side outside the unique accessible native height-one gate. Its proof
uses the three-height normal form and the occupied-parent theorem in both
prime trees. In particular it excludes mixed-height substitutes at an
inaccessible gate. The [native-core discussion](../core-budget/README.md)
explains the same hypothesis for the one-cell 5063 subcase. This input is
stronger than terminality in only one prime tree.

Finally, the [supported-cycle theorem](../../../../2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/NO_REMOTE_GAPS.md)
excludes every simple polygonal loop in the skeleton of a tiling of
either target whose edges form a triangular mesh of step `c`, at any
rotation and translation. The proof below constructs precisely such a
loop. It does not interpret an abstract phase-graph cycle as a geometric
cycle.

## 3. Proof of visibility

Fix an occupied remote cell `L` and let `U` be the union of all its tiles.
It is a finite bounded polygonal union of positive area. Suppose it has
no positive-length contact from one of its short sides to an odd long
side.

Each short side is covered on its opposite bank by short sides of the
same cell. Indeed, any complementary long side would belong to a
height-one tile, the only available adjacent short height; such a contact
has been excluded. Short sides in another cell are excluded by the
straight-run argument, and a remote cell has no exterior interval at its
short height. Thus the actual oriented short-edge chain of `U` is zero.

Sum the counterclockwise boundaries of all selected tiles. Cancel those
short-edge contributions and all inaccessible long-edge pairs supplied
by the one-accessible-gate theorem. These are cancellations of oriented
edge contributions, not removal of tiles or their areas. Every remaining
boundary segment is a long edge of length `c` at direction height one.

### Whole edges remain whole

Translate and rotate the chosen short-height cell to `R`. Its long-edge
vectors are unit multiples of `a+b*rho` or its conjugate. These are
primitive lattice vectors, because `gcd(a,b)=1`; multiplication by a unit
and conjugation preserve primitivity. Therefore a whole long segment
contains no other vertex of the selected cell in its relative interior.
On one supporting line, selected vertices differ by integer multiples of
the primitive long vector. Two selected length-`c` segments on that line
can overlap over a positive length only when they coincide completely.
Any further opposite long-edge cancellation is consequently whole to
whole.

Two remaining selected edges cannot cross in their relative interiors:
their incident nondegenerate triangles would overlap on a positive-area
sector near the crossing. A selected edge endpoint cannot terminate in
the interior of another selected edge, by the primitive-vector argument.
The remaining segments thus form an embedded graph with disjoint open
edges. A T-junction supplied by an outside tile may subdivide a contact
on the opposite bank. It does not add a selected-cell vertex or shorten
the whole edge in this graph. Reflections are included throughout.

### Holes, disconnected components, and vertex contacts

The resulting graph is the oriented boundary of `U`. At every vertex
the numbers of incoming and outgoing edges agree. It is nonempty: a
finite positive-area union cannot have zero boundary chain, as is also
seen by summing the oriented area formula over its tiles.

A finite nonempty balanced directed graph contains a closed directed
walk. Removing repeated vertices yields a simple directed cycle. Since
the graph is embedded with distinct open edges and has no edge remaining
in both directions, this is a simple polygon with positive enclosed
area. The argument permits holes, several components, and components
meeting only at vertices. It does not require that `U` itself be a disk
or that the extracted cycle be an outer boundary of `U`.

Every edge of this cycle is `c*z*rho^j` for an integer `j`. Starting at
one vertex shows that the whole cycle lies in one translate of `c*z*R`.
It is supported by actual whole tile sides. Its enclosed disk lies in
the convex outer triangle, and no open tile interior crosses its
boundary. It therefore satisfies the exact supported-cycle hypothesis,
which yields a contradiction.

This proves the visibility theorem. The same proof starts directly from
an assumed zero actual short-edge chain; the absence of parent contacts
is a sufficient way of obtaining that chain. No population estimate or
classification of equality at `2c^2` is needed.

## 4. Consequence for the 3431 gate count

For odd population 111 and the balanced-remote native profile
`(Q_up,Q_down)=(22,15)`, the independent certificate in
[the main note](README.md) proves

\[
K_{\rm parent}\le34,
\]

where `K_parent` counts remote gates containing any parent odd tile.
That inequality uses nonnegative integer unsigned gate populations and
the complete periodic endpoint equations. It does not itself count
occupied even cells.

Visibility now supplies the missing geometric implication. Each occupied
remote even cell has an actual short-to-parent-long contact, and the
associated remote gate is therefore nonempty in the odd inventory.
Distinct remote even cells have distinct gates in the appropriate hand.
Consequently

\[
\boxed{K_{\rm occupied}\le K_{\rm parent}\le34.}
\]

Equality of these two counts is not asserted: parent odd long sides can
occupy a gate whose even cell is empty by pairing with other odd long
sides. The result is an upper bound, and no incompatible universal lower
bound has been proved. Other charge profiles, larger odd populations,
and both original tiling questions remain open.

## 5. Dependencies, controls, and review scope

The geometric proof was independently checked in two internal reviews
against the primitive long-vector property, partial contacts, holes,
disconnected components, and the precise supported-cycle hypotheses.
The existing [empty-node proof](../../../../2026-11-20/semiprimes/continuation/vertex-phase/NO_PHASE_GAPS.md),
Section 4, uses the same embedded-boundary extraction after establishing
whole interface edges by a different argument. These are written
mathematical arguments, not proof-assistant formalization or exhaustive
enumeration of physical placements.

The inherited exact numerical input can be replayed from the repository
root:

```sh
python3 research/2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/check_remote_cycles.py
```

The two finite gate inequalities and their 143 geometric convention
control remain independently checked by:

```sh
python3 research/2026-11-21/semiprimes/full-closure-attempt/target3431/verify_gate_excess.py
```

The known 143 board is not a target of the supported-cycle exclusion, so
the visibility conclusion is not transplanted to it. Likewise, an
isolated balanced patch with long boundary edges at more than one height
does not satisfy the single accessible height used in this proof.

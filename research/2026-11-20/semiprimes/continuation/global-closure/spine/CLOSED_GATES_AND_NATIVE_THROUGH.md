# Whole mates at every closed spine gate

21 November 2026. This note strengthens the complete geometric spine
model by two necessary conditions. Both concern actual contacts, not
allocated populations. They assume the exact two-tree spine hypothesis
from `SPINE_DICHOTOMY.md`.

## 1. Every nonnative long gate is wholly paired

Let the three permitted short joint cells be

\[
 L_0=R,\qquad L_1=A+zR,\qquad L_2=A+z^2R.
\]

For a tile of short height `h` and hand `s`, its long edge has height
`H=h+s`. Represent its long-edge joint cell by either endpoint `p`.
Call this gate open when `H in {0,1,2}` and `p in L_H`, and closed
otherwise. This is an exact arithmetic test; it does not refer to
whether another candidate has already been enumerated.

**Closed-gate theorem.** In every complete tiling of the spine class,
a tile with a closed long gate has its whole-long-side half-turn mate
in the tiling.

**Proof.** The classification of exterior-containing nodes applies
to edge nodes as well as short nodes. If the long gate is closed,
its joint cell has an exterior-free exact node `v` in at least one
of the two prime trees. The tile's short node `p_0` is non-free by
the spine hypothesis, and it is adjacent to `v`. The node `v` cannot
be the parent of `p_0`: an exterior node below `p_0` would then also
lie below `v`. Therefore `v` is a child of `p_0`.

Every descendant of an exterior-free node is exterior-free. Since
the hypothesis prohibits all occupied exterior-free short nodes,
no tile has a short node anywhere in the subtree of `v`.

Now take a maximal supporting run containing the tile's long side.
The integral-offset theorem gives one edge node `v` for every side
in that run. No short side can contribute, because that would
occupy `v`. A long-side contributor has a short node adjacent to
`v`; all its possible child nodes are empty, so its short node must
be the parent `p_0`. There is no outer interval on this run with
edge node `v`, because `v` is exterior-free.

Both banks are consequently partitions of the same finite run into
whole edges of length `c`, all belonging to tiles of the same short
height and hand. The banks have the same first endpoint. Their
successive endpoints therefore agree at distances `c,2c,...`, even
if unrelated runs elsewhere have partial contacts. Across each
whole side, the same short height and opposite CCW long-side
directions identify the unique half-turn mate. This proves the
theorem.

For `(q,h,j,s)`, the mate is

\[
 \left(q-a z^h\rho^j+b z^h\rho^{j+s},\ h,\ j+3\pmod6,\ s\right).
                                                               \tag{1}
\]

Its short joint cell is unchanged. If this mate is not contained,
the original placement cannot occur in a spine tiling. If both
are candidates, their selection variables must be equal.

In particular, every actual unmatched long side of a spine tiling
must use one of the three open native joint cells. The theorem
does not require every open-gate long side to remain unmatched.
It also does not pair arbitrary long sides crossing between the
height-zero and height-two populations through the middle native
cell; that gate is open.

## 2. Native through-tiles have finitely many exact offsets

At an interior T-junction, a corner half-fan occupies one side of
a supporting line through `P`, and a tile crosses `P` through the
relative interior of one of its sides on the other bank.

The point `P` is an endpoint of an edge in the corner half-fan.
The through-side endpoints and `P` belong to the same maximal
supporting run. By the unrestricted integral-offset theorem, their
directed distances along its unit axis differ by integers. If the
through-side length is `L in {a,b,c}`, its offset therefore has
one of the values

\[
 t\in\{1,2,\ldots,L-1\}.                              \tag{2}
\]

This does not assume that the through-side is subdivided into whole
tile edges on both banks. It uses the common integer coordinate
on the maximal run, whose two banks are concatenations of the
integer side lengths.

For a specified oriented ray from `P`, there are six possible
through-tile shapes before translating along that ray. For each
shape, the existing corner oracle computes the exact rational
interval of contained translations. Intersect that interval with
(2), then retain only the translations satisfying

\[
 h\in\{0,1,2\},\qquad z^{-h}(q-t_h)\in R.
\]

This finite test contains every actual through-tile in a spine
tiling. If none survives, the corresponding half-fan is impossible.
If one survives, the corner implication merely allows that
half-fan; it does not assert that the through-tile is selected in
the partial model. The latter relaxation preserves necessity.

## 3. Implementation and positive control

With `--closed-gates`, `spine_sat.py` imposes the exact mate
equivalences (or excludes a placement with an inadmissible mate)
whenever a candidate is inserted. These conditions also apply to
later incident-oracle and corner-oracle expansions. The insertion
first registers its Boolean variable, so the mate's reciprocal
insertion terminates without duplication.

With `--corners`, the wrapper uses the existing complete angle-fan
implications and optional angular-overlap cliques. It replaces the
continuous through-translation existence test by the finite native
test in Section 2. The tile incident oracle still applies the
native restriction inside `Geometry.admissible`; changing only an
initial pool would not suffice.

The complete known 143 tiling passes with both upgrades. The solver
returns SAT, and the independent metric/current verifier confirms
143 distinct contained congruent tiles with exact coverage and
zero endpoint residuals. The separate `verify_spine_restrictions.py`
checks the native phase classification, mandatory mates, and all
actual through-contacts in this positive control.

These implications are globally necessary for the complete spine
class. Their presence in a finite projected model does not by
itself decide that model. Only an unguarded permanent-model UNSAT
result, with its encoding and proof checked, would close the class.

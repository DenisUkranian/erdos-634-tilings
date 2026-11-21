# Exact area and signed-population cuts for supported polygons

21 November 2026. **3431 and 5063 remain OPEN.** This note gives a
necessary geometric cut for any simple polygon supported by actual
selected tile sides. It permits mixed direction heights and does not
assume a minimal odd population or restrict the range of heights.

## 1. A supported polygon encloses complete tiles

Let a finite collection of contained triangles have pairwise disjoint
interiors. Suppose a simple polygon `P` of positive area is supported
by segments of their sides. Individual polygon edges may be proper
subsegments of whole sides, and their endpoints may be T-junctions.

In any full nonoverlapping completion containing those supporting
triangles, an open tile interior cannot cross any supported segment:
it would overlap the triangle on that segment's occupied bank.
Nor can it contain a polygon vertex, because that would contain a
neighborhood meeting an occupied triangle interior. By the Jordan
curve theorem, every tile interior lies wholly inside or wholly outside
the polygon. Its disk lies inside the convex board. Consequently the
disk is a union of complete unit tiles, up to their zero-area boundaries.

Write the counterclockwise polygon vertices in the axial basis
`1,rho`, with `rho=exp(i*pi/3)`. Set

\[
S(P)=\sum_i\det(v_i,v_{i+1}),\qquad
n(P)=\frac{S(P)}{ab}.
\]

The physical area of a unit tile is `ab*sqrt(3)/4`, so necessarily

\[
\boxed{n(P)\in\mathbb Z_{>0}.}
\]

This conclusion is about a full completion. The current partial
packing need not already fill the polygon. Conversely, an integer
area does not establish tileability and is not a reason to reject
a mixed-height cycle.

## 2. Its boundary also determines two signed populations

Put `d=a-b` and `z=(a+b rho)/c`. For each oriented boundary atom of
positive physical length `L` and heading `z^h rho^j`, define

\[
W_0(P)=\sum L(-1)^j,\qquad
W_1(P)=\sum L(-1)^{h+j}.
\]

Both quantities are additive under subdivision and change sign when
an edge is reversed. They therefore cancel on internal contacts,
including partial contacts and T-junctions. No assumption that a
polygon edge is a whole tile side is needed.

A tile `(q,h,j,s)` has sign `epsilon=s*(-1)^j`. Directly summing its
three counterclockwise sides gives

\[
W_0(T)=(d-c)\epsilon,\qquad
W_1(T)=(d+c)(-1)^h\epsilon.
\]

For example, at `s=1` the three oriented sides have headings
`(h,j)`, `(h,j+1)`, `(h+1,j+3)` and lengths `a,b,c`.
Their two character sums are exactly the displayed expressions.
At `s=-1` the counterclockwise order gives their corresponding
negative expressions, agreeing with `epsilon=-(-1)^j`. These are
the same direction characters used in the
[signed population theorem](../../../../2026-11-20/semiprimes/continuation/vertex-phase/SIGNED_PHASE_POPULATIONS.md).

Thus a completion of the polygon would have exact signed populations

\[
G_{\rm even}=\frac12\left(\frac{W_0}{d-c}+\frac{W_1}{d+c}\right),
\qquad
G_{\rm odd}=\frac12\left(\frac{W_0}{d-c}-\frac{W_1}{d+c}\right).
\]

Whole positive triangles require all three conditions

\[
\boxed{
G_{\rm even},G_{\rm odd}\in\mathbb Z,\qquad
n(P)\ge |G_{\rm even}|+|G_{\rm odd}|,\qquad
n(P)-G_{\rm even}-G_{\rm odd}\in2\mathbb Z.
}
\]

The inequality counts the minimum number of positive-area tiles
needed to supply the two signed totals. The parity follows because
each tile contributes one to the count and either `+1` or `-1` to
exactly one signed total. These conditions apply to arbitrary enclosed
tilings, including every possible larger odd population of a target.
They are necessary conditions only.

## 3. From a detected polygon to a permanent no-good

Choose one selected supporting tile for each polygon atom and let
`I` be the set of distinct chosen tile indices. A failure of any
displayed necessary condition proves

\[
\boxed{\neg\bigwedge_{i\in I}x_i.}
\]

Other selected owners of the same physical atom are not required for
this particular clause. An owner used on several atoms occurs only
once. Subdivision vertices introduced by other triangles need not be
retained as assumptions: they are still fixed points of the selected
supporting segments, and the same polygon remains supported.

The geometric and character argument received a separate internal
review by the agent responsible for the global proof audit. It is a
written mathematical deduction, not a proof-assistant formalization.

## 4. Detector and interface

[`area_cycles.py`](area_cycles.py) first takes a deterministic exact
nonoverlap subset of the selected model. It groups sides by their
exact supporting line and splits them at **every** retained endpoint
on that line, including endpoints belonging to another supporting
line. A sweep constructs interval atoms and their actual owners.

The resulting graph is planar: a transverse crossing of two triangle
sides would give overlapping triangle interiors. Exact angular order
then gives a half-edge boundary walk. The helper keeps positive
simple polygonal boundary walks and skips repeated-vertex walks.
Before emitting a cut it additionally checks polygon simplicity by
exact pairwise segment intersection tests and verifies positive area.
Holes, disconnected components, and unused selected triangles do not
invalidate an emitted simple polygon.

```python
from area_cycles import selected_area_cycles

for witness in selected_area_cycles(g, tiles, chosen, max_cycles=1):
    indices = witness['indices']
    # Add permanently: not(and(x_i for i in indices)).
```

Each witness records closed exact vertices, all oriented atoms, one
representative owner per atom, the other retained owners, the exact
tile-area ratio, both boundary sums, both signed totals, and the
failed necessary conditions. `use_characters=False` requests area
cuts alone. `max_cycles=0` removes the output-count cap.

Greedy discards, skipped nonsimple boundary walks, and the output cap
can miss other valid cuts. They weaken detection without weakening
the proof of any returned no-good. The helper is not an exhaustive
spatial solver and imposes no finite bound on possible future tile
placements.

## 5. Independent exact controls

Run from the repository root:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/corner-tests/verify_area_cycles.py
```

The standard-library verifier reconstructs every reported triangle and
atom using independent `Fraction` geometry. It checks containment,
metric, nonoverlap of each control packing, simplicity by a separate
line-parameter intersection test, supported atoms, exact directions,
area, character sums, and the resulting arithmetic failures.

The complete replay is
[`AREA_CYCLE_REPLAY.json`](AREA_CYCLE_REPLAY.json). It includes:

- Ten legal three-triangle partial packings: at heights
  `-5,-1,0,1,7` for each target, their supported triangular holes have
  noninteger tile areas `1369/231` and `1849/455`. All are rejected.
  Removing one support gives no cut. Adding an overlapping distractor
  leaves the valid supporting-owner clause unchanged.
- The existing mixed-height cycle controls for 143, 3431, and 5063.
  Their selected supports leave holes of **12, 72, and 84 tiles**,
  respectively. Both signed totals are zero, all three integer holes
  pass, and no cut is returned.
- The genuine complete 143 tiling. The detector finds exactly
  **143 unit-area faces**, with compatible signed populations and
  **38 strict side subdivisions** checked independently. It returns
  no forbidden polygon.

These controls prove the indicated local rejection and preservation
results. They exclude no complete target corner root. Any future
root exclusion still needs the complete necessary-model and solver
proof audit.

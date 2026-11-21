# Supported whole-long-side cycles give permanent target cuts

21 November 2026. **3431 and 5063 remain OPEN.** This helper makes an
existing global geometric obstruction available to a finite placement
search. It introduces no height, phase, population, or coordinate bound.

## 1. Exact inherited theorem and its scope

The theorem in
[NO_REMOTE_GAPS.md](../../../../2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/NO_REMOTE_GAPS.md)
states that neither target board, with tile `(33,7,37)` or `(35,13,43)`,
has a supported cycle in any full tiling. A supported cycle is a simple
polygonal loop in the tile skeleton whose edges belong to a translate of
a triangular mesh of step `c`. Its proof treats every mesh rotation.
Consequently it applies to **every integer direction height and every
translation**, not only to the native height-one mesh or to a minimal odd
population. It permits reflections and T-junctions.

This was checked against the statement and proof, including the rational
direction-width and thickness calculation. The restriction to the two
specific target boards is essential. The public helper returns no cuts
for the 143 control or any other shape. Geometric detection on other
shapes is available separately and makes no impossibility assertion.

The inherited numerical geometry can be replayed with:

```sh
python3 research/2026-11-20/semiprimes/continuation/vertex-phase/pure_cycles/check_remote_cycles.py
```

## 2. From selected tiles to a forbidden geometric cycle

A selected tile `(q,h,j,s)` has whole long-side endpoints

\[
u=q-a z^h\rho^j,\qquad w=q+b z^h\rho^{j+s},
\]

and that side has direction height `h+s`. Group these sides by this
height, canonicalize the exact endpoints, and identify a segment with
its reverse. If two tiles occupy opposite banks of the same whole side,
their two records create **one** undirected edge, not a two-edge cycle.

Each connected component lies in one translate of `c*z^k*R`, where `k`
is its common long height: this follows by walking from any chosen
vertex along its length-`c` mesh edges. The graph is therefore an
embedded subgraph of the ordinary triangular unit mesh. Distinct open
unit mesh edges cannot cross or contain a mesh vertex. A graph-theoretic
simple cycle with at least three distinct edges is a simple polygon
with positive area.

Every edge is supported by an actual whole side of one of the selected
triangles. An outside T-junction can subdivide its contact description
but does not remove that side from the skeleton or change the extracted
polygon. The convex target contains the enclosed disk. In any full
tiling no tile interior crosses a skeleton cycle, so that disk would be
filled by complete tiles. The supported-cycle theorem forbids it.

For one chosen representative tile index `i_e` at each distinct cycle
edge, this proves the permanent necessary clause

\[
\boxed{\neg\bigwedge_{e\text{ in the cycle}}x_{i_e}.}
\]

It is unnecessary to assume that the rest of the generated finite
catalogue is complete or that the cycle interior has already been
filled by selected tiles. A full completion would supply that filling.
The no-good is valid even if the currently selected model also contains
unrelated overlaps: a full tiling containing all its representative
triangles would still contain the forbidden cycle.

## 3. Public interface

```python
from long_cycles import selected_long_cycles

for witness in selected_long_cycles(geometry, tiles, chosen_indices):
    indices = witness['indices']
    # Add the permanent clause: not(and(x_i for i in indices)).
```

The function returns at most one cycle per connected component. Each
witness has:

- `height`: the common direction height;
- `indices`: distinct selected variable indices, in cycle edge order;
- `vertices`: exact `Geometry` points, including the repeated closing
  vertex;
- `edges`: endpoints, the representative variable index, and every
  selected owner of that same undirected physical segment.

The smallest selected index is the deterministic representative of an
edge. A different opposite-bank owner can produce a different valid
no-good in a later model. The helper does not claim that one
representative clause eliminates all alternative owners at once.

`raw_selected_long_cycles` performs geometric detection for any shape;
its output is not automatically forbidden. `selected_long_cycles`
checks the target shape before applying the inherited theorem. Neither
function traverses an abstract phase-node graph or treats a mixed-height
cycle as forbidden.

## 4. Exact controls and limitations

Run:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/corner-tests/verify_long_cycles.py
```

The verifier reconstructs the reported tile geometry independently using
`Fraction` coordinates. It checks long-side metric, common height, mesh
unit displacement, distinct vertices and edges, nonzero area, selected
owners, and the exact representative indices.

At both target shapes it checks contained nonoverlapping three-tile
supports for a triangular long-side cycle at heights `-5,-1,0,1,7`.
These are legal partial packings whose completion is impossible. It
also checks that a two-edge path and two opposite-bank copies of one
segment give no cycle, that either bank can provide a representative,
that disjoint components give separate cycles, and that a component
with several cycles contributes only one witness.

All 128 initial corner roots of each target have no such cycle. All
143 long sides of the known complete positive control were scanned;
the raw detector found no cycle, and the target-specific cut is disabled
there in any event. The replay is
[`LONG_CYCLE_REPLAY.json`](LONG_CYCLE_REPLAY.json).

These tests establish the stated finite geometry and implementation
properties. The universal no-good relies on the cited written
supported-cycle theorem; neither its proof nor this helper is a
proof-assistant formalization. No complete corner root is excluded by
these initial controls.

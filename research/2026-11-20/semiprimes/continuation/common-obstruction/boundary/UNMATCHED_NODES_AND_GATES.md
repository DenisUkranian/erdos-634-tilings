# Unmatched long edges and the population cost of phase gates

These are necessary statements for any complete tiling of either target
`(33,7,37; N=3431)` or `(35,13,43; N=5063)`. They allow arbitrary heights,
reflections, positions and T-junctions. The inputs are the integral-offset
contact lemma and supported-cycle argument in
[No phase gaps](../../vertex-phase/NO_PHASE_GAPS.md), together with
[exact-node signed populations](../../vertex-phase/SIGNED_PHASE_POPULATIONS.md).
No finite placement catalogue is assumed.

Fix either prime tree. An exact node counts only tiles whose own short
node is that node, not the full descendant subtree. A node is
exterior-free when no outer-edge node belongs to its descendant subtree.
The height-zero core is not exterior-free.

## 1. Every occupied exterior-free exact node has an unmatched long edge

For an exact node `v`, write `n_v` for its population and `U_v` for the
number of its tiles without a half-turn mate across their complete
`c`-edge. A half-turn mate has the same short height and shares an actual
endpoint with its tile. It consequently has the same exact short node;
there is no distinction between a mate inside the node and a mate
elsewhere in the full tiling.

**Theorem.** If `v` is occupied and exterior-free, then `U_v>0`.
In particular `U_v>=2` when `n_v` is even. Terminality is not required.

Let `h` be the physical short height and suppose every tile in `v` has
such a mate. Let `U` be their union, with its positively oriented boundary
chain. All their long sides cancel in the half-turn pairs. Their total
short-edge chain `Q` is therefore exactly the boundary of `U`.

Now sum the directed interval currents at height `h` in this one phase
node. The integral-offset lemma makes cancellation independent at each
node, including across partial contacts. Every short edge in this sum
belongs to a tile of `v`. Every other contribution is a whole long side
of length `c`, at height `h`, from a neighboring short node. There is no
outer contribution: an exterior edge at node `v` would contradict
exterior-freeness. If `L` is the sum of these whole long sides, then

`Q+L=0`

as geometric chains. Consequently the finite integer whole-edge chain
`L` is endpoint-balanced and its signed area is minus the positive area
of `U`. In particular it is not merely a collection of cancelling
backtracks.

After combining coincident oriented edges, each endpoint-connected
component has every vertex in one translate of `c*z^h*Z[rho]`. A closed
walk decomposition of `L` has nonzero total signed area, so a nontrivial
cycle remains after deleting backtracks. Unit edges of this triangular
mesh cannot cross or contain another mesh vertex in their relative
interiors. Removing repeated vertices yields a supported simple
pure-`c`-mesh polygon. Its edges are actual long tile sides. The supported
cycle theorem excludes it. Distinct translated components may overlap
partially, but this does not alter the existence or simplicity of the
cycle within the chosen component.

This contradiction proves the theorem. Since pairs remove two tiles,
`U_v` has the same parity as `n_v`, giving the even-population assertion.

### Signed refinement

Let `G_v=n_v^+-n_v^-`, with `epsilon=s*(-1)^j`. A half-turn pair has
opposite signs, hence

`U_v>=|G_v|`.

An ordinary node has `n_v=c*k_v`, `G_v=c*l_v`, and `k_v=l_v (mod 2)`.
Thus an occupied exterior-free node with even `k_v` has at least two
unmatched tiles; one with odd `k_v` has at least `c` unmatched tiles.
For a set of distinct such exact nodes, these unmatched populations
are disjoint. If `E` and `O` count its even- and odd-block nodes, then

`U_total >= 2*E+c*O`.

At the targets, the costs per odd-block node are 37 and 43. These are
lower bounds on unmatched tiles, not upper bounds on the node population
and not an impossibility certificate for the whole board.

## 2. A closed phase gate forces whole-edge pairing

Let `v` be any short node and `w` one of its children. Consider a tile in
`v` whose long-edge node is `w`. In the increasing-height tree this is a
short-height-`h`, long-height-`h+1` tile. In the conjugate tree the physical
heights are reversed.

**Gate lemma.** If `w` is exterior-free and has zero own population, that
long edge has a whole half-turn mate in `v`.

By the no-vacant-ancestor theorem, an exterior-free empty `w` has no
occupied descendants. On the maximal straight run containing the long
edge, the integral-offset lemma puts all edge intervals in node `w`.
The short node of each incident tile equals `w` or is adjacent to it.
Only its parent `v` remains possible: `w` and its children have no tiles.
There is no outer interval. Thus both banks partition the same finite
run into complete edges of length `c`. Starting at their common endpoint,
the two partitions coincide. The two incident triangles have the same
short height and hand, so their opposite rotations differ by 3; they are
half-turn mates.

Equivalently, an unmatched long edge directed toward a child can occur
only through an exterior-containing child or an occupied exterior-free
child. This is the safe geometric extension of the closed-gate pairing
used by native two-height endpoint certificates.

### The cost of active gates

Let `W` be any finite set of **distinct exterior-free child nodes** each
witnessed by such an unmatched long edge. Every node in `W` is occupied
and ordinary, so it contributes at least `2c` own tiles. Therefore

`2c*|W| + j <= N`,

with `j=N mod c`, when the only separately reserved population is the
core. If `F` is another set of required occupied ordinary nodes, the
safe combined cost is for the union `F union W`, not the sum of two
possibly overlapping lists. Signed height parity further gives

`|F union W| <= 45` at 3431, and `<=58` at 5063.

If independent lower populations `L(v)` are available at the named
nodes, their disjoint own populations give

`B + sum_{v in F union W} L(v) <= N`,

where `B` is a justified bound for tiles outside these exact nodes.
A gate costs 74 tiles at 3431 and 86 at 5063. The cost is charged once
per phase node. Several edges or Euclidean lattice translates using the
same child do not create additional costs. Populations from both prime
trees cannot simply be added: each actual tile belongs to one node in
each tree.

An ungenerated mate is not an unmatched edge. Therefore the absence of
a mate from a finite catalogue does not activate this gate constraint.
One must know the geometric nonmatching contact, or use variables that
allow every possible full-tiling mate.

## 3. A mixed-height directed cycle exists as an exact local packing

The pure-height hypothesis cannot be dropped from the supported-cycle
theorem on the basis of local geometry. The following small partial
packing fits strictly inside both target boards; the same construction
also fits the 143 positive-control board.

In axial coordinates, put

`V=(b,a)=c*z^(-1)*rho`, `T=(0,a*c)=a*c*rho`.

The parallelogram with vertices `Q,Q+V,Q+V+T,Q+T` is tiled by `2c`
short-height-zero triangles: partition the long direction into `c`
cells of width `a`, and split each cell along its `b` diagonal. Adjacent
cells give `c-1` half-turn pairs along `c`, leaving exactly two unmatched
end tiles. There are `c` tiles of each sign.

Along each long side, add `a` exterior teeth of short height -1 and
long height 0. Their bases divide that side into complete `c`-edges.
The two end sides are long edges of the interior end tiles at height -1.
With the correct bank choices, **every** edge of the parallelogram
boundary points from its tile's beta endpoint to its alpha endpoint.
It is a directed cycle of `2a+2` actual whole long edges: `2a` at height 0
and two at height -1. Its entire interior is tiled, and its outside
supporting teeth have disjoint interiors.

Take `Q=(ceil(a*b/c)+1+1/c,1)`. Its positive-prime valuation is -1.
All interior anchors differ from `Q` by integral vectors, so they occupy
one exterior-free height-zero coset. All bank tiles have short height -1
and lie outside that exact node. This realizes the local pattern of a
balanced `2c` node with exactly two unmatched long edges; it does not
prove that the node retains this population in a full completion.

| Board | Interior tiles | Exterior teeth | Directed cycle edges | Interior long-edge pairs |
|---:|---:|---:|---:|---:|
| 143 | 14 | 10 | 12 | 6 |
| 3431 | 74 | 66 | 68 | 36 |
| 5063 | 86 | 70 | 72 | 42 |

The three `mixed_cycle_*.json` files are exact local certificates.
`verify_mixed_cycle_controls.py` independently reconstructs all placements
using rational Eisenstein arithmetic, checks containment, all pairwise
interior disjointness, exact interior area, both cycle banks and every
beta-to-alpha direction, signs, half-turn pairs, and phase classification
by direct division by an Eisenstein prime. It does not import the search's
geometry or Hensel-node code. All three controls passed.

These are **partial packings**, not complete tilings or counterexamples
to a whole-board impossibility statement. They show why a proposed
argument must use a global attachment or population cost to eliminate
mixed-height cycles; thin-board containment and a tiled cycle interior
alone do not do so. The 3431 and 5063 cases remain undecided.

## 4. This balanced `2c` strip also cannot be lowered locally

For all three control shapes, `c<3a/2`. The parallelogram of Section 3
has no replacement tiling using only short heights at most -1, despite
its zero character and its existing balanced `2c` tiling.

Its two long boundary sides have direction height 0 and length `ac`.
In a putative lower-height tiling, they must be partitioned into exactly
`a` long edges of short-height-minus-one tiles. Their hand is fixed, so
the interior teeth are forced. Put `P_i=Q+i*c*rho` and `Q_i=P_i+V`.
On the left side the `i`-th tooth has vertices

`P_i, P_(i+1), P_i+(a/c)*V`.

On the right the `i`-th tooth has vertices

`Q_i, Q_(i+1), Q_(i+1)-(a/c)*V`.

For `1<=i<a`, the chord from `P_i` to `Q_i` is fully covered by edges
of the left tooth `i` and right tooth `i-1`: their respective chord
fractions are `[0,a/c]` and `[1-a/c,1]`, which overlap because `2a>c`.
No remaining tile interior can cross such a chord. These chords split
the strip into `a` cells with vertices `P_i,Q_i,Q_(i+1),P_(i+1)`.

Each cell has area `2c/a` in tile units and contains exactly its two
forced teeth, with disjoint interiors. Its remaining positive area is

`2(c-a)/a < 1`.

The remaining tiles would each be confined to a cell and have unit
area, a contradiction. The exact remainder areas are `4/5`, `8/33`
and `16/35` for 143, 3431 and 5063. This proves an obstruction to a
specific positive lowering operation, not to tiling the entire target.
It strengthens the smaller balanced-pair warning in
[Terminal translates](../terminal/TERMINAL_TRANSLATES.md).

## Reproduction

The JSON certificates and their independent verifier are self-contained:

```sh
python3 verify_mixed_cycle_controls.py
```

`make_mixed_cycle_controls.py` regenerates them using the project's exact
geometry class. `check_known143_gates.py` checks the gate lemma on the
known **complete** 143 certificate. That separate positive control has
60 whole-long-edge half-turn pairs and 23 unmatched tiles. The two prime
trees respectively contain 30 and 90 tiles at closed child gates; all
of those tiles have their required whole half-turn mates.

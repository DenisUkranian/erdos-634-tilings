# A one-direction obstruction for the reflected-corner remainder

8 October 2026. This is a restricted geometric obstruction, not a decision
of 4830 or a classification of all F3 tilings.

Let positive integers `a>b` satisfy `c²=a²+ab+b²`. Work in Eisenstein
coordinates, where `(x,y)` represents `x+y rho`, `rho=exp(i*pi/3)`, and
put `Z=a+b rho`. The translated reflected-corner remainder is

```
Q = [0, b(2a+b), ab(1+rho), b(a-b)rho].
```

It has area equal to `3ab` original `(a,b,c)` tiles. The earlier positive
attachments show that a filling of Q supplies both ordered F3 targets,
F2, and reversed F4. The following obstruction only concerns one possible
way to fill Q.

**Proposition.** Q cannot be tiled by copies of the `(a,b,c)` triangle
whose short sides all belong to the directions `rho^j`, `j=0,...,5`.
Reflections and arbitrary T-junctions are allowed.

**Proof.** Its two long non-axis sides have directed vectors
`b rho² Z` and `-b Z`, and each has length `bc`. No short tile edge can
lie on either of these sides. They therefore consist of exactly `b`
whole c-edges each. Each such edge forces its adjacent tile uniquely:
its short sides have lengths a and b and must be in the prescribed
three unoriented axis classes.

The same whole-edge observation applies to every internal maximal
straight c-seam: both sides partition the same segment into c-edges,
so their endpoints agree. Each internal c-edge consequently pairs its
two incident tiles into a parallelogram. Such a pair has zero signed
boundary-length current separately in each of the three short-axis
classes. This remains true even when its short edges have T-junctions.

Measure signed boundary current along `1`, `rho`, and `rho²`. The
short sides of Q contribute

```
(b(2a+b), -b(a-b), 0).
```

Along the directed side `-bZ`, each of its b forced tiles has the two
other directed edges `a` and `b rho`. Subtracting these tiles contributes
`(-ab,-b²,0)` to the remaining short current.
Along the directed side `b rho² Z`, each forced tile has the other
edges `-a rho²` and `b`. Subtracting these b tiles contributes
`(-b²,0,ab)`.

The current of the remaining region is therefore exactly

```
(ab, -ab, ab).
```

It is nonzero, whereas all its tiles must be paired parallelograms and
thus have zero such current. This contradiction proves the proposition.
If the forced boundary tiles were to overlap, a tiling would already be
impossible; the current argument only uses the hypothetical tiling.

For `(a,b,c)=(24,11,31)`, the 792-tile remainder has vertices

```
(0,0), (649,0), (264,264), (0,143).
```

There are 22 forced boundary tiles. They have disjoint interiors; the
385 putative paired-tile parallelograms would have to supply current
`(264,-264,264)`, which they cannot do. In particular any positive filling
of this sufficient region must use at least two short-edge direction
classes. Indeed, if its only class were not the base class, the base
would consist exclusively of c-edges, forcing `31 | 649`, which is false. This does **not** prove that the full 4830-tile F3 target is
impossible, and does not assert that every such F3 tiling contains Q.

## Checks and searches

`one_level.py` constructs the 22 forced tiles with exact integer
coordinates and checks that each long boundary segment permits exactly
one such tile. It writes `one_level_structure.json`.

`parallelogram_cp.py` was an exploratory positional search before the
current obstruction was extracted. Its 510,090 possible parallelogram
positions give 305,525 boundary rows and 35,706,300 nonzero entries.
Bound propagation finds a contradiction, recorded only as an
**uncertified restricted search diagnostic** in
`q792_one_level_report.json`. The mathematical proposition above does
not depend on the program or the large search.

`macro_pool_cp.py` instead allows multiple orientation classes by
collecting exact positions of integer-scaled original triangles from
successive convex-corner contacts, then imposing exact boundary-current
matching with Boolean CP-SAT variables. The derivative of each current
is recorded at every endpoint on its supporting line; this is equivalent
to matching every atomic interval and permits T-junctions. A verified
integral solution would be a genuine macro tiling. Failure of this
finite heuristic pool says nothing about arbitrary tilings.

The depth-2 pool contained 8,329 macro placements and 22,992 current
endpoint equations. CP-SAT returned INFEASIBLE for that pool in a total
17.94 seconds. The depth-3 generation stopped at its 180-second budget,
with 30,694 placements and 76,719 equations; CP-SAT likewise returned
INFEASIBLE for that pool. These two statuses are scoped solver reports,
not mathematical exclusions of broader recipe classes or of 4830.
No positive certificate was found in this attack.

# Independent audit of the fixed alpha-base count 21

29 September 2026. Separate implementation and internal mathematical review; no external refereeing or proof-assistant formalization is claimed.

The certificate [alpha-21-refutation.json](../../data/alpha-21-refutation.json) proves that a triangle of
side lengths `(12,12,21)` cannot be tiled by 21 congruent triangles with side
lengths `(2,3,4)`. Reflections, arbitrary rotations, and arbitrary T-junctions
are allowed. This is a statement about one tile and one target shape; by itself
it is not a proof that every triangle fails to admit a 21-tiling.

The independent checker is [verify_alpha21.py](../../scripts/verify_alpha21.py). It imports no code from
the search and does not trust its residual-boundary computations or memoized
state equivalences. Running it on the certificate gives:

- 391 certificate nodes, all reachable;
- 437 expanded states after every incoming placement history is checked;
- 158 expanded dead ends;
- maximum placement depth 18;
- all assertions pass using exact rational arithmetic.

The checked certificate SHA256 is
`68c4b0edd0eaeb2c99818d41522d40ef6e7062a2f800c0cc3fd78f7a1bbed74c`.

## Why the finite branching covers unrestricted tilings

Write coordinates `(x,y)` for the Euclidean point `(x,sqrt(15)y)`. The target
vertices are `(0,0)`, `(21,0)`, and `(21/2,3/2)`. Every tile has scaled double
area `3/2`.

At each certificate node the previously placed triangles are exactly contained
in the target and have pairwise disjoint interiors. The checker verifies that
the specified corner is an actual convex component of the uncovered local
angular region. In any completion, a tile covering the first boundary ray of
this sector must have a vertex at the corner: an interior point or a straight
edge point of a tile would require at least a half-plane, which cannot fit in a
sector strictly smaller than pi. Its incident side must lie along that ray.

There are exactly six possible congruent tiles with that property. Choose the
angle opposite side 2, 3, or 4; then choose which of its two adjacent sides lies
on the ray. Swapping those adjacent sides includes reflected tiles. The checker
constructs all six using the law of cosines. Any completion must choose one
whose remaining angular sector is a sum of tile angles, that is contained in
the target, and that has no positive-area intersection with an already placed
tile. Every such choice occurs as a certificate child, exactly once.

Every leaf has no possible choice. Consequently no completion exists at a leaf,
and finite induction up the tree proves nonexistence at the root. The checker
expands every memo reference, so this argument does not need a separate claim
that two search histories with the same boundary determine the same state.
The general assertion that every nonempty polygon has a convex corner is also
not required for this particular replay: the selected corner is verified at
each of the 437 expanded states.

## Checks independent of the search's main geometric mechanisms

**Local sector.** For each polygon edge, write its oriented half-plane test at
`p+epsilon*w` as `f(p)+epsilon*g(w)`. Its sign for every sufficiently small
positive epsilon is determined lexicographically, exactly. All edge rays
through the corner are sorted. The specified two rays must be consecutive;
the sector between them must be locally inside the target and outside all
placed triangles, while the sectors immediately before and after it must be
occupied or outside. Their positive cross product certifies convexity. This
uses tangent cones rather than subtracting or stitching residual polygons.

**Intersections.** The checker clips candidate triangles successively by the
three half-planes of each existing triangle. The rational area of every
intersection must vanish. This is independent of the search's separating-axis
intersection predicate.

**Angle inventory.** Let alpha, beta, gamma be opposite sides 2, 3, 4. Their
complex rotations in the scaled coordinates are
`(7/8,1/8)`, `(11/16,3/16)`, and `(-1/4,1/4)`. Elementary cosine comparisons give

$$
\frac\pi8<\alpha<\frac\pi6,\qquad
\frac\pi4<\beta<\frac\pi3,\qquad
\frac\pi2<\gamma<\frac{2\pi}3.
$$

If `i alpha+j beta+k gamma<pi`, necessarily `i+2j+4k<8`.
Every triple meeting that bound has total angle less than `4pi/3`, so a
positive imaginary coordinate of its rotation detects precisely the positive
angles below pi. Enumerating these bounded integer triples and including zero
yields the same 17 distinct angles as the search, by a different computation.

**No lattice restriction.** The checker never rounds coordinates, imposes a
mesh, or caps denominators. A corner and an oriented boundary ray force each
new tile's coordinates by its exact side lengths and angles. Thus rational
coordinates arise as a consequence of the forced placements; they are not an
extra condition placed on a hypothetical tiling.

## Audit finding

No completeness or geometric gap was found. The finite certificate and the
independent exact replay support the fixed `(12,12,21)` exclusion. They do not
establish global nonexistence for tile count 21 or solve all of Erdős problem
634. An external mathematical review remains distinct from this internal
adversarial audit.

## Public replay

The public certificate removes the original run's timing metadata without changing any state or branch. The checker was rerun on the exact public file; its deterministic report is [alpha21.json](../../verification/alpha21.json). The complete argument and fixed-shape spectrum consequence are in [the obstruction note](../alpha-21-obstruction.md).

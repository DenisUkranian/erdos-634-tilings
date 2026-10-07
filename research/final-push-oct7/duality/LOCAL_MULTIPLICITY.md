# Exact multiplicity does not provide local sheets

Let R be any triangle with angles alpha, beta, gamma satisfying

    gamma = 120 degrees,   alpha + beta = 60 degrees.

**Theorem.** Nine distinct congruent copies of R can be placed with one
vertex at a common point O so that, in some punctured disk about O,
their interiors cover almost every point exactly twice. They cannot be
partitioned into two subfamilies each covering that disk once.

## Construction and proof

Starting with a ray of angle zero, lay out successive angular sectors of
sizes

    gamma, gamma, alpha, gamma, gamma, beta, gamma, alpha, beta.    (1)

Their total is five times 120 degrees plus twice 60 degrees, hence
720 degrees. For each sector choose a congruent copy of R whose vertex
at O has the indicated angle and whose two incident edges run along the
sector's endpoint rays. Reflections are permitted. Choose the disk radius
smaller than every distance from O to the opposite edge of these nine
triangles. Inside this disk, triangle membership is precisely membership
in its angular sector. The consecutive intervals in (1) partition two
complete turns, so their projections onto the direction circle have
constant multiplicity two away from the finitely many endpoint rays.

Write t = alpha / 60 degrees, so 0 < t < 1, and measure directions in
units of 60 degrees, modulo 6. Number the nine triangles from 0 to 8.
The five gamma sectors are

    T0: [0,2],
    T1: [2,4],
    T3: [4+t,6] union [0,t],
    T4: [t,2+t],
    T6: [3,5].

In their interiors the intersection graph is exactly the cycle

    T0 -- T4 -- T1 -- T6 -- T3 -- T0.

The five successive intersections have positive angular lengths
`2-t, t, 1, 1-t, t`. Every other pair in this five-element set has
disjoint sector interiors. A partition into onefold subfamilies would
assign different subfamilies to every intersecting pair. An odd cycle
has no such two-coloring. This proves the assertion. It also proves the
stronger statement that the nine tiles cannot even be colored with two
colors so that each color class has disjoint interiors near O.

The triangles are distinct because their angular sectors at O are
distinct. Each positive angular intersection gives positive Euclidean
intersection area in the disk, irrespective of the lengths of the two
incident sides of the corresponding copies.

## What this does and does not rule out

An exact positive rational filling, after clearing denominators, is a
multiple covering. Converting it to an ordinary tiling requires an
integrality or decomposition theorem. The construction disproves a
universal *local* version asserting that every exact multiple fan of
congruent triangular tiles can be separated into single sheets.

It does **not** prove the existence of an untileable triangle with a
positive fractional tiling. No completion of this nine-tile fan to an
exact twofold cover of a whole triangular target has been constructed.
Global boundary constraints might exclude this fan, or a different
onefold tiling might exist even when the supplied multiple covering does
not decompose. Neither possibility is decided here.

In particular, this is a precise obstacle to one proof mechanism, not
a counterexample to a possible global normal-form theorem.

# What long-chord geometry does and does not force

3 October 2026. This note contains exact geometric checks, not a full tiling
certificate and not a nonexistence theorem.

For consecutive parameters `v=u+1`, `b=2u+1`, and `t=v/2`, write `S=bv²/2`
for either equal side of the theta target. Its base has length `rS`, where
`r=u/v`. The required pure-a/pure-c chain length is `L=uv²`, so
`ell=L/S=2u/b`. Normalize the equal sides to 1 and put

    h²=1-r²/4,
    A=(0,1), B=(-r/2,0), C=(r/2,0).

These coordinates have squared metric `dx²+h²dy²`.
The height of a swapped alpha-gap tile, in these units, is

    H=(c/S)h=2h/b.

## Arbitrary chords cannot yield the desired strict height bound

Already at `u=3,v=4`, the apex-to-base-midpoint chord has length `hS>L`.
The maximum distance on each side of its line is `rS/2=21`, whereas
`c sin(theta)=2 sqrt(55)<21`. This chord meets the compulsory apex tile,
so it is not sufficient to assess actual seams.

## A scalar width cutoff still fails after the five corner tiles are removed

An exact partial configuration at `u=51,v=52` shows the limitation persists
after placing five valid corner tiles. The parameters are

    (a,b,c)=(2652,103,2704), S=139256, L=137904.

Put `e=b/S=2/v²`, `f=c/S=2/b`. Place the unique apex alpha tile at
`A,E,F`, where

    E=A+e(B-A), F=A+f(C-A).

At each base corner place the ordinary a-by-b parallelogram split along
its c diagonal. At C its two vectors have length b toward A and length a
toward B; at B use the reflected configuration. This gives five congruent,
pairwise nonoverlapping tiles contained in the target.

Define

    z=ell²-h²(1-e)²,
    X=(E_x+sqrt(z),0).

The segment EX has length exactly L after restoring scale S. It avoids
the interiors of all five corner tiles. First consider the ambient convex
quadrilateral `EBCF`, formed by removing only the apex tile. Its smaller
maximum distance to the supporting line is attained at C and equals

    delta = h(1-e)/ell * [r(1+e)/2 - sqrt(z)].

The exact checker establishes for this ambient quadrilateral

    delta/H = 1.0021578953047363... > 1.

For a short exact verification of this ambient inequality, it is equivalent
to `sqrt(z)<T`, where

    T = r(1+e)/2 - f*ell/(1-e)
      = 950222558013 / 2015300577472 > 0,
    z = 46621798829321 / 209746397925376,
    T²-z = 29406733425106235 / 751005254726142136448 > 0.

**This is not yet the width of the actual unfilled region:** C belongs to
the occupied base-corner fan. To compute the actual complement, write each
fan as the parallelogram `O,U_O,W_O,V_O`, where `U_O` is the b-endpoint on
the equal side, `V_O` the a-endpoint on the base, and `W_O=U_O+V_O-O`.
The closure of the unfilled region has boundary

    E, U_B, W_B, V_B, V_C, W_C, U_C, F.

Its positive and negative support extrema relative to EX occur at `U_C`
and `U_B`, respectively. The smaller-side width is the distance to `U_C`,
which is

    delta_unfilled = h/ell * [r(1-e)/2 - (1-2e)sqrt(z)],
    delta_unfilled/H = 1.0014440090358487... > 1.

This strict inequality is equivalent to `sqrt(z)<T_unfilled`, with

    T_unfilled = [r(1-e)/2-f*ell]/(1-2e)
               = 78031853 / 165500400 > 0,
    T_unfilled²-z
               = 328208708437585759 / 12516747387695516160000 > 0.

Widths here mean the supremum distance within each half-plane portion of
the unfilled region, equivalently the maximum over its closure. In
particular, `U_C` is a boundary point approachable from the unfilled region;
the removed vertex C is not used for this conclusion.

The accompanying checker also verifies exact tile congruence and target
containment, all ten pairwise interior-disjointness conditions, and which
side of EX contains each tile. It checks the actual complement's simple
boundary and exact area, triangulates it exactly, and verifies that those
triangles avoid the occupied corner tiles. Finally it compares every
complement vertex with the claimed support extrema. It isolates the square
root between rational bounds; none of these verdicts depends on
floating-point tolerances.

The strict height margin is robust: moving X slightly toward C increases
chord length above L while preserving avoidance and `delta_unfilled>H`. A slightly
shorter internal subsegment of length L then has endpoints away from the
boundary and from the apex tile. This observation is only continuity of a
partial geometric configuration.

**Limitation.** The chord has not been tiled by a-edges or c-edges. No
completion of the remaining region is supplied. An actual pure chain has
additional direction, edge-partition, and endpoint constraints; these may
still provide an obstruction. Nor does width exceeding H imply that a
swapped alpha-gap tile fits: its required footprint may intersect occupied
tiles or the target boundary. The example rules out only the proposed
**scalar width cutoff** as a consequence of target convexity and these
corner fans. It does not rule out a more detailed corner-geometry
obstruction.

## Files

- `check_corner_chord.py`: exact arithmetic checker for the five-tile partial
  configuration and the chord inequality.
- `corner_chord_certificate.json`: exact parameters, square-root isolation,
  verified claims, and an explicitly labeled approximate ratio.

Exploratory floating-point calculations are not included as proof sources.
Their optimizers can miss narrow extrema and are not used for a global bound.

No claim of a sharp global width bound is made.

# Historical scope

This four-height check was subsequently subsumed by the complete five-height
checks and the global reduction in [GLOBAL_154_PROOF.md](GLOBAL_154_PROOF.md).
Any references below to heights still remaining describe this intermediate stage.

# Independent exclusion of the centered four-height band for 154

8 October 2026. This note extends the independently audited
[three-height exclusions](THREE_HEIGHTS.md). It excludes the complete
band `[-1,2]` and, by reflection, `[-2,1]`. It does not by itself exclude
`[0,3]`, `[-3,0]`, or any five-height band.

## Exact lattice for any finite band

Put `eta=3+rho`, `bar(eta)=4-rho`. Then

```
eta*bar(eta)=13,   z=eta/bar(eta),
2 eta + 2 bar(eta) - eta*bar(eta)=1.
```

The last identity proves that eta and bar(eta) generate the unit ideal.
Their equal powers also do: expand an odd power of a Bezout identity,
so every resulting monomial contains a sufficiently large power of at
least one of the two generators. Therefore

```
sum_(h=L)^U z^h Z[rho] = g Z[rho],
g = eta^L / bar(eta)^U.
```

Indeed after factoring g the generators are
`eta^(h-L) bar(eta)^(U-h)`. All belong to Z[rho]; the endpoint generators
are coprime powers, so their ideal is all of Z[rho]. Combined with the
existing integer-atom lattice lemma, this is the complete vertex
lattice, not a chosen numerical grid.

Multiplication by `1/g=eta^(-L) bar(eta)^U`, for L<=0<=U, gives an
integer-coordinate target. All unit short directions likewise become
`eta^(h-L) bar(eta)^(U-h)`, with common squared norm `13^(U-L)`.
The 12 orientations at each height are exactly the two mirror types
and the six sixth-root rotations used in the three-height theorem.

For `[-1,2]`, the exact target contains 9,475,103 lattice points and
294,008,822 complete candidate placements at the four heights. The
geometry is otherwise unchanged: all candidates lie in the fixed
triangle `(91,91,154)` and use `(8,7,13)` tiles.

## Distinct producer and verifier

The producer `../154-cpsat/full_band_packed.cpp` enumerates a dense
scanline grid using integer floor/ceiling inequalities, maintains
packed variable states, and records forcing-row IDs while propagating
endpoint-current equations.

The independent `replay_packed_band.cpp` does not import that generator
or its queue. It enumerates the entire bounding rectangle using direct
three-half-plane tests, obtaining the same dense lattice-point indexing
from actual contained points. It constructs every template by complex
multiplication, checks its exact side norms and area, and independently
counts all valid placements. It scatters their six endpoint incidences
into stored lower and upper row bounds.

For every recorded forcing row it verifies that the right side equals
the current lower or upper bound, determines the resulting assignments,
and updates the six incident rows of each assigned geometric triangle.
Thus the recorded rows carry no trusted numerical bounds or claimed
infeasibility status. All checks use exact integers.

The independent replay certified 108,084,789 forcing rows and
294,008,200 assignments before reaching this contradiction:

```
point:     (3276,1547) in transformed integer coordinates;
direction: (3,-4);
remaining row interval: [1,1];
required target current: 0.
```

The producer reaches its contradiction later because it processes
queued rows in a different order. The earlier independently reproduced
contradiction is sufficient. This proves the stated band exclusion.
The report is `four_center_replayed.json`.

## Reproduction

From the repository root:

```
g++ -std=c++17 -O2 research/final-closure-oct8/154-cpsat/full_band_packed.cpp -o /tmp/634-packed
/tmp/634-packed -1 2 /tmp/634-four-center 600 1
g++ -std=c++17 -O2 research/final-closure-oct8/154-audit/replay_packed_band.cpp -o /tmp/634-packed-replay
/tmp/634-packed-replay -1 2 /tmp/634-four-center.rows.bin /tmp/634-four-center-replayed.json 294008822
```

The 600-second producer budget must finish with `conflict=true` and
`incomplete=false`; a timeout has no negative implication. The second
program must report PASS with a contradictory exact row interval. The
large intermediate trace is regenerated from the preserved source and
need not be stored in the repository. This is internal independent
verification, not external peer review or a full exclusion of 154.

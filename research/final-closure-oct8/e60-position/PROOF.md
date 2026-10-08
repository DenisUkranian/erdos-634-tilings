# No tiling with N=60

8 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.
This is a computer-assisted nonexistence proof within the published angular
classification and rationality framework. Internal independent verification is
not external mathematical refereeing. No claim of historical priority is made.

**Theorem.** A triangle cannot be tiled by exactly 60 congruent triangles in
the sense of Erdős problem634.

## 1. All shapes and tiles

[The independent all-branch reduction](../class15/REDUCTION.md) enumerates every
arithmetic candidate at N=60. The classical spectra do not contain60. The four
nonclassical possibilities are the equilateral (3,5,7) candidate, two Group-1
theta candidates, and one double-angle candidate. The written long-seam and
two-longest-edge bounds exclude the last three. No candidate W/beta scale-one
exclusion is used. It suffices to exclude the equilateral triangle of side30
with tile(3,5,7).

## 2. Every tiling lies in one of two complete direction bands

Put rho=exp(i*pi/3), eta=2+rho, and z=eta/conjugate(eta)=(3+5rho)/7.
Short-edge height h means directions rho^j*z^h. Both tile chiralities and all
six rotations are allowed. The target sides have height0.

[The structural proof](../e60-structure/STRUCTURE.md) establishes n0>=11,
n_h>=14 for every occupied nonzero height, and absence of gaps in the occupied
height interval. The no-gap proof explicitly deals with the potentially
49-tile tail; it does not incorrectly use a pure-island lemma for mixed heights.
Thus there are at most four consecutive heights containing0.

Every such support is contained in one of [-1,2], [0,3], or their reflections.
Reflection of the equilateral target exchanges h and -h, with both chiralities
already included. It is therefore enough to exclude these two bands. Permitting
zero populations at the ends includes every shorter interval as well.

## 3. The coordinate lattice is necessary, not guessed

The whole-edge/atomic-seam lattice lemma gives all tiling vertices in

    Lambda[L,U] = sum(z^h Z[rho], L<=h<=U)
                = g Z[rho],   g=eta^L/conjugate(eta)^U.

The equality follows from coprimality of eta and its conjugate in Z[rho]. The
vertices of the target include0, so the translation is fixed. At extreme
long-edge directions there are only whole7-edges; their contact partitions
coincide. This handles T-junctions without assuming an edge-to-edge tiling.
The detailed general lattice argument and the endpoint-current construction
are recorded in [the 154 position proof](../154-cpsat/README.md).

Multiply all coordinates by1/g. The target becomes the integer triangle

    (0,0), 30/g, 30rho/g.

For each of its integer points and each h in[L,U], both orders of short lengths
3,5 and all six rotations yield twelve exact templates. All three vertices
must lie in the target. Convexity makes this equivalent to full containment.
This enumerates every possible tile placement in the band.

## 4. Finite exact necessary equations

For every lattice point and every unoriented edge direction, form the sum of
oriented edge starts minus edge ends. Each counterclockwise tile contributes
six signed endpoint entries. The right-hand side is the same endpoint current
of the counterclockwise target boundary. A genuine tiling necessarily satisfies
these equations: interior oriented edges cancel, including partial contacts.

Each distinct contained placement has a variable in[0,1]. Every genuine tiling
gives a zero-one solution. For one equation, the still possible sum has integer
bounds[lo,hi]. If its right-hand side equals an endpoint of that interval,
each term is forced to the corresponding zero or one value. If the right-hand
side lies outside the interval, no tiling exists. All arithmetic is integral;
no floating point optimizer or unresolved search is part of this refutation.

## 5. Complete certificates and independent replay

| Band | Complete placements | Independently replayed assignments | Final false inequality |
|---|---:|---:|---|
| [-1,2] | 3,918,936 | 3,918,875 | 0 <= 1 <= 0 |
| [0,3] | 3,917,313 | 3,917,239 | -1 <= 0 <= -1 |

`complete_bands.cpp` produces the forcing-row traces. The separately implemented
`replay_complete_bands.cpp` reconstructs all possible placements by direct
half-plane tests across the bounding box, rather than using the producer's
scanline formulas. It checks every template's side norms9,25,49 and area15,
independently counts the placements, constructs all row bounds by scattering
six entries per placement, and justifies each trace assignment. It reproduced
both contradictions. Replay can stop at an earlier contradiction than the
producer; their final assignment counts need not agree.

The reports are `center_replay.json` and `extreme_replay.json`. The field
`full_60_decided:false` in an individual band report means that this report
alone proves only the stated band. Sections1--5 together prove the theorem.

## Reproduce

Run from the repository root; only a C++17 compiler is needed:

```sh
c++ -O3 -std=c++17 research/final-closure-oct8/e60-position/complete_bands.cpp -o /tmp/e60_producer
c++ -O3 -std=c++17 research/final-closure-oct8/e60-position/replay_complete_bands.cpp -o /tmp/e60_verifier
/tmp/e60_producer -1 2 /tmp/e60_center 120 1
/tmp/e60_producer 0 3 /tmp/e60_extreme 120 1
/tmp/e60_verifier -1 2 /tmp/e60_center.rows.bin /tmp/e60_center_checked.json 3918936
/tmp/e60_verifier 0 3 /tmp/e60_extreme.rows.bin /tmp/e60_extreme_checked.json 3917313
python3 research/final-closure-oct8/e60-structure/check_structure.py
python3 research/final-closure-oct8/class15/reduce_class15.py
```

The binary traces are reproducibly generated in seconds and are not necessary
repository payload. This theorem closes N=60. It does not close N=135, N=4830,
or the full classification in Erdős634.

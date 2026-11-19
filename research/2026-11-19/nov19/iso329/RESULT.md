# No 329-tiling for the (33,7,37) tile

In Eisenstein coordinates ρ=e^(iπ/3), the isosceles test triangle is the convex hull of 0, 329 and 49+231ρ. Its sides are 259,259,329. Its area is 329 times that of the (33,7,37) tile. The separate arithmetic reduction in ../iso329_alt/REDUCTION_329.md identifies it as the sole candidate for a count of 329. This is a computer-assisted internal research result as of 19 November 2026, without external peer review.

## Short proof

1. The population result and the line, parity and area arguments in README.md bound the occupied short heights to a consecutive interval containing 0 of length at most four. Reflection in the symmetry axis negates the heights. Every interval is therefore contained, up to reflection, in either [0,3] or [−1,2].
2. For either band, if all tile vertices are multiplied by D=η^(−L)(η')^U, they lie in Z[ρ], with η=7−3ρ and η'=4+3ρ. The finite-band position lemma in README.md includes T-junctions. For each of the 48 orientations there is one unique 120° anchor; both possible orders of the two legs are present. The scanline sweep tests every integer anchor placing all three vertices inside the target.
3. For each physical point and unoriented direction, signed tile-edge starts minus ends equal the oriented target demand. If a zero-demand point can receive only one sign, all such placements are impossible. At an exterior corner, absence of its required sign contradicts a tiling. These implications follow by differentiating the signed interval currents on the actual supporting line. The C++17 program packed_replay.cpp applies them with exact integer run lengths. An independent native-lattice count agrees with all 65,681,363,443 placements for [0,3]. That band lacks the required positive incidence at its apex on iteration 108.
4. In [−1,2] the same unrestricted program begins with 66,005,127,488 contained translates and stabilizes after 106 iterations at 952,400 possibilities. The separate segments.cpp program requires that every point of each edge can be covered by oppositely oriented candidate edges on its line (including the reversed outer edge). It uses interval unions and compares integer endpoints. Run it with phase flag **0**, allowing arbitrary offset and multiple contacts. At iteration 39 it detects insufficient opposite coverage on the outer 259-leg with primitive direction (7,−3) and determinant intercept 401709, while 375,483 placements are still active. Thus the centered band is impossible as well.

These two *unrestricted* position searches do not rely on setting phases for any layer, choosing any boundary tiles, reducing first to exactly four nonempty levels, or single-precision/floating-point tolerances. Area, orientation and the finite dictionary are exact. The reported contradiction in each band is checked from candidate sets with necessary geometric conditions. Combined with the arithmetic reduction they exclude N=329. The unrestricted classification posed in Erdős problem 634 remains open.

## Reproduction

Use a 64-bit C++17 compiler. The two wide runs were completed separately on a machine with 9.7 GiB RAM. They can run sequentially to reduce peak usage. The temporary centered survivor list is approximately 14 MB.

```sh
c++ -O3 -std=c++17 packed_replay.cpp -o packed_replay
c++ -O3 -std=c++17 segments.cpp -o segments
./packed_replay 0 3
./packed_replay -1 2 0 1000 centered_four.txt
./segments centered_four.txt 0
```

Compare the printed results with packed-0-3.log, packed12.log and unpinned-center-segments.log. As a separate exact geometric corroboration, the four-level centered survivors coincide individually with the previously obtained three-level [−1,1] candidates after multiplication by 4+3ρ; centered-four-level-equality.txt gives the digest. The equality is unnecessary for the direct segment refutation. PHASES.md gives the stronger local-lattice restrictions and an additional positioned proof of the centered-band exclusion from a 465,602,541-placement dictionary.

A positive control for both kernels is the standard nine-tile grid in a threefold dilation of the tile:

```sh
./packed_replay -1 2 3 1000 control9.txt
./segments control9.txt 0 checked9.txt 3
```

## Independent computation for the one-sided band

A separately implemented bitmap version uses the earlier Paliy-repository style of translated endpoint bit masks, an inward target interval for each translated vertex, and a different unimodular shear (x,y)→(x−y,−3x+4y). The lower-layer pinning in PHASES.md is used. Height 3 can translate anywhere in the full band lattice. This independent dictionary contains 16,657,000,330 placements. On its 32nd wordwise sweep, 18,853 remained when the final edge of the base could no longer supply its required end incidence at the right base corner. In sheared coordinates the corner is (−106267,401709), and the primitive unoriented base direction is (323,−1221). The candidate interval lists and direction ordering are independent of the packed-scanline solver. A twofold dilation of the tile stabilizes with precisely the four grid placements.

```sh
c++ -O3 -std=c++17 paged_anchored_side.cpp -o paged_anchored_side
./paged_anchored_side 0 3 side 1200
./paged_anchored_side 0 3 control 120 0 2
```

See independent-side.log, independent-side.json, independent-side-four-control.log. Its JSON field N329_decided is false because that executable reports a **single restricted band**; the global conclusion combines both bands with the height proof above.

## Independent exhaustive centered phase audit

The geometry/count arguments in PHASES.md place every centered tiling, if one exists, in one of 37³ indexed phase triples. The separate graph-based queue in phase_current.cpp treats all 37×37 combinations of the first and third digits together for each fixed middle digit J. All 37 runs gave a missing required signed endpoint, with no segment test required in any group. Each involves about 24.65 million placements. The aggregate count includes common lower-layer placements tested in different groups. This is a distinct numerical algorithm from the scanline proof. It enumerates points in each translated unit lattice, builds six signed incidences per placement, and maintains per-row counts while deleting placements. It independently corroborates the centered-band exclusion conditional on the additional positioning argument.

```sh
python3 replay_grouped.py
```

Compare with grouped-centered-audit.json. For J=0 the dictionary contained 24,654,061 placements, with 145 survivors at the point of contradiction. For each J the result covers all 1,369 possible endpoint phase pairs. Combined coverage is 50,653 listed triples.

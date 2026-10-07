# Positional checks for the F3 gamma remainder

Research directed by Denis Paliy, with ChatGPT assistance, 7 October 2026.

The [proof](GAMMA_BOUNDARY_OBSTRUCTION.md) establishes infinitely many
primitive positive gamma remainders that cannot be filled at multiplier
one, even allowing all orientations. More strongly, along an explicit
continued-fraction sequence, every fixed finite set of initial
multipliers is eventually excluded by a necessary exterior-side
semigroup condition. The infinitude proof uses Siegel's integral-point
theorem; the supplied finite examples use only exact integer arithmetic.
This auxiliary nonexistence theorem does not exclude the full F3 targets.

In fact the existing F3 construction has a uniform threshold t=6 along
this sequence. Hence, for every fixed t>=6, infinitely many full F3
targets are tileable while their positive gamma remainders at the same
scale are not tileable by the same tile in any directions. This proves
that fillability of the gamma remainder is not a necessary condition
for F3 existence. The explicit tile `(2024,741,2479)` at t=6 already
provides such a counterexample, without the Siegel infinitude input.

For 4830, the necessary short-side inventory is realizable by an exact
15-tile patch inside the reduced gamma quadrilateral. This covers one
side and all seven of its straight boundary fans; it does not fill the
quadrilateral. Its 105 tile pairs, all coordinates, tile congruence and
containment are checked with rational arithmetic.

Run from the repository root:

```bash
python research/f3-position-invariants/check_boundary.py
python research/f3-position-invariants/check_infinite_boundary_examples.py
```

The retained outputs are `4830-boundary-collar.json` and
`infinite-boundary-examples.json`. No full tiling of 4830, or all-count
classification, is asserted.

## A vacuous diameter-only seam route

The c-edge source-to-relation method can yield a lower bound on target
diameter by the shortest nontrivial relation `nc=Aa+Bb`. That particular
bound cannot exclude any integer-scale F3 target: assuming a>b, the
identity `bc=c*b` gives such a relation already at n=b, while an F3 side
has length `t*c*(a+2b)>bc` for every positive integer t. This observation
only limits that diameter-only arithmetic estimate. It does not limit
position-sensitive continuation constraints on the actual seam.

# Independent audit: no thirteen-tile nonzero height, and the five-height bound

8 October 2026. Separate internal mathematical review and independent
integer implementation. This is not external refereeing or a formal proof.

**PASS.** The [nonzero-height theorem](../oct8-structural/NO_THIRTEEN_HEIGHT.md)
and the independent checks below imply that any tiling of `(91,91,154)`
by `(8,7,13)` has **three through five consecutive occupied short heights**,
including zero. There are twelve such intervals, or seven up to reflection.
Neither the count 154 nor the full Erdős problem is decided.

## 1. Geometric argument reviewed

For a fixed nonzero height h, integrate the oriented boundary identity on
each complete affine supporting line. Every tile edge on that line not
among the height-h short edges is a whole edge of length 13. At exterior
heights 1 and -1, the whole target side length is also divisible by 13;
at other nonzero heights no target side contributes. Therefore the signed
short-edge total on each individual line is divisible by 13. Partial
contacts, T-junctions, and disconnected unions cause no problem: the
argument integrates complete edge contributions and never assumes that a
long edge coincides with a whole short-edge chain.

With thirteen tiles, the alternating character of the three signed
currents is a sum of thirteen terms in `{1,-1}` and is divisible by 13.
It must be 13 or -13, so every tile has the same character. All 8-edges
then have one direction parity, and all 7-edges the opposite parity. This
reduces the possible short-edge orientations to six rigid types.

A supporting line containing m edges of length 8 and n edges of length 7
satisfies `8m-7n=0 mod 13`, `0<m+n<=13`. Enumerating these line pairs and
the six-type inventories is finite and exact. In every admissible
inventory some rigid tile orientation occurs more often than the product
of the maximum possible numbers of supporting lines for its two short
edges. Those lines are nonparallel. Two tiles of that orientation must
therefore share their gamma vertex, and hence coincide, contradicting
nonoverlap. No bound on the connectedness of a height component is used.

This argument excludes **population exactly 13**, not every odd multiple
of 13. Combined with the prior divisibility theorem it gives `n_h>=26`
for occupied nonzero h. It does not imply `26 | n_h`.

## 2. Independent enumeration

[check_no_thirteen_independent.py](check_no_thirteen_independent.py)
imports the earlier independent exact-coordinate edge model, and does
not import the producer's inventory list, symmetry representatives,
allowed line pairs, or line-count table. It:

1. Derives each short-edge signature from the two rational reference
   triangles and computes its alternating character.
2. Enumerates all 8,568 weak compositions of 13 into the six positive-
   character types; precisely 54 pass the three current congruences.
3. Computes the maximal supporting-line count by a separate recursive
   decomposition of each total pair into all allowed nonzero line pairs.
4. Checks a gamma-vertex pigeonhole contradiction for every inventory.
5. Applies half-turns for the opposite character and checks the resulting
   108 inventories form nine twelve-member rotation/reflection orbits.

Fresh result: **PASS**. The complete arithmetic report is
[no_thirteen_independent.json](no_thirteen_independent.json). Its geometric
input is the written affine-line argument in Section 1, not a numerical
optimizer status.

## 3. Independent six-height exclusion

Seven occupied heights would require at least `11+6*26=167>154` tiles.
Thus only the six-height case needs an additional exclusion.

[check_all_height_backward.py](check_all_height_backward.py) derives edge
matrices from the same frozen independent coordinate model and traverses
heights in the reverse direction from the producer. It enumerates signed
A-vectors, whereas the producer enumerates B-vectors. For every local
state it directly tests populations in steps of 13, starting at 11 for
height zero and 26 otherwise, and checks the required parity.

For six occupied heights the baseline is `11+5*26=141`. Reserving the
minima at the other heights leaves at most 39 tiles at any individual
nonzero height and 24 at zero. Thus enumerating every signed A-vector
of L1 norm at most 39 is exhaustive. Grouping by residues loses no vector.
The state is `(A_(h+1),B_h)`, with the minimum already used population;
future constraints depend only on this state, so retaining the cheapest
path is safe. Lower-height minima provide valid budget pruning. The
outside equations are checked at both ends. There is no time or state
cutoff.

Fresh result: **all six intervals of length six are EXACT_UNSAT**.
The five recorded formal controls of length five were separately expanded
into the twelve unsigned orientations and checked by summing the actual
edge signatures. Every control has exactly 154 tiles and every occupied
nonzero height has population at least 26. These are inventories without
positions, not positive geometric certificates.

The retained independent report is
[all_height_backward_verified.json](all_height_backward_verified.json).
It records the checker source, coordinate-model source, and exact witness
input hashes. Its most recent run completed in about 1.35 seconds in this
environment; this is an observation, not a complexity bound.

## 4. Reproduction and conclusion

From the repository root, without Python `-O`:

```sh
python research/closure-position-oct7/global/check_no_thirteen_independent.py
python research/closure-position-oct7/global/check_all_height_backward.py
```

The second command reads the five witnesses in
`oct8-structural/all_height_direction_probe.json` and records its SHA-256.
Both commands use only the standard library. The older frozen independent
checker and its reports have not been modified.

Combine the population floor, the six-height exclusion, the
[no-gap theorem](../heights/HEIGHT_GAPS.md), and the supplied complete
two-height obstruction. The surviving interval lengths are exactly the
necessary possibilities 3, 4 and 5. Their count is `3+4+5=12`; two are
reflection-fixed, giving `(12+2)/2=7` orbits. Actual geometric feasibility
within those intervals remains unresolved.

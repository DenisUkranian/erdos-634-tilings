# Reuse exact forbidden supports by physical isometries

21 November 2026. **3431 and 5063 remain OPEN.** A local forbidden
support already proved by an exact polygon witness can be reused at
every congruent occurrence in the current candidate catalogue. The
implementation adds no placements, assumes no symmetry of the board,
and makes no claim that the finite catalogue contains every future
placement.

## 1. Why one anchor determines the isometry

The triangle is scalene: `c>a>b`. Its obtuse vertex and its two acute
vertices are therefore distinguished by their side labels. An isometry
mapping one tile to another must map these labelled vertices correctly.
Once an anchor tile and its image are fixed, there is exactly one such
isometry, either direct or reflected.

Write the source anchor as `(q0,h0,j0,s0)` and its candidate image as
`(q,h,j,s)`. Recall `z=(a+b rho)/c`. If `s=s0`, the isometry is

\[
T(v)=q+u(v-q_0),\qquad
u=z^{h-h_0}\rho^{j-j_0}.
\]

It maps another tile `(qk,hk,jk,sk)` to

\[
\bigl(T(q_k),\ h+h_k-h_0,\ j+j_k-j_0,\ s_k\bigr),
\]

with its unit direction reduced modulo six. If `s=-s0`, the isometry is

\[
T(v)=q+u\overline{v-q_0},\qquad
u=z^{h+h_0}\rho^{j+j_0},
\]

and its tile image is

\[
\bigl(T(q_k),\ h-h_k+h_0,\ j-j_k+j_0,\ -s_k\bigr).
\]

Complex conjugation of an exact axial point is
`(x,y,e) -> (x+y,-y,e)`. All operations use integer numerators and
powers of `c`, followed by the existing canonical point reduction.
The multiplier has norm one, so metric, area, nonoverlap, and the
labelled triangle geometry are preserved exactly.

Every isometric occurrence of the whole support has some candidate
tile as the image of the fixed source anchor. Scanning every candidate
as that image therefore finds every occurrence already contained in
the finite catalogue. An occurrence is accepted only when every
mapped tile key is present in the global index. A missing image is
not created, selected, or assumed absent from the unrestricted problem.

This is a completeness statement about matching within a supplied
finite catalogue, not a bound on the full geometric tiling problem.

## 2. The transferred obstruction is independently visible

The source support must have an independently valid
[polygon-budget obstruction](AREA_CYCLE_CUTS.md). Isometry preserves
its supported simple polygon and its noninteger tile area, when that
is the failed condition. For the signed conditions, a direct map
multiplies tile signs by `(-1)^J`; a reflected map multiplies them by
`-(-1)^J`. A multiplier height `H` swaps the even and odd height
classes precisely when `H` is odd. Thus charge integrality, the sum
of absolute charges, and the population parity condition are also
preserved.

The implementation nevertheless exports each learned occurrence as
an ordinary `general_area_cycle_cuts` witness. It includes the actual
mapped vertices and representative tile indices, not merely an
assertion that the pattern matches. Under reflection it reverses the
polygon walk to restore counterclockwise orientation; side index
`k` becomes `(1-k) mod 3`. It recomputes area and both boundary
characters from the mapped directed atoms.

The existing independent snapshot auditor can therefore check the
actual polygon support and its no-good without trusting the matcher
or adding a new mathematical proof rule. A valid source polygon
with no failed condition is explicitly refused by the export helper.

## 3. Public interface and deduplication

```python
from pattern_isometries import (
    pattern_isometries, pattern_key, transform_area_witness,
)

key = pattern_key(g, tiles, source_witness['indices'])
for occurrence in pattern_isometries(
        g, tiles, index, source_witness['indices']):
    witness = transform_area_witness(g, source_witness, occurrence)
    # Add permanently: not(and(x_i for i in witness['indices'])).
```

The catalogue `tiles` and its dictionary `index` must use the solver's
canonical tile keys. The optional `anchor` argument is a position in
the source index list. Returned `image_indices` follow that source
order; `indices` is the sorted distinct support for the clause.
Each occurrence also records the anchor position, its candidate
image, reflection flag, multiplier height and unit direction, and
the two exact anchor points.

`pattern_key` normalizes each possible anchor to
`(q=0,h=0,j=0,s=1)`, sorts its transformed support, and takes the
least resulting tuple. This costs `O(k^2)` tile transforms for a
`k`-tile pattern. Keys are compared within one fixed tile shape.
They allow many previously expanded polygon cuts to share one source
pattern on restart. `pattern_congruence_key` is an equivalent public
name. Matching caches rotated relative offsets by target orientation
and tests a distant support member first; these are speed choices,
not extra geometric restrictions.

## 4. Compact exact seeds

The following small files contain `sides`, actual `tiles`, and ordinary
`general_area_cycle_cuts` witnesses with the existing rule identifier:

- [ISOMETRY_SEEDS_3431.json](ISOMETRY_SEEDS_3431.json): seven candidate
  tiles supporting two noncongruent forbidden patterns: the original
  triangular aperture and a subsequently discovered four-tile
  mixed-height support with hole area **34/7 unit tiles**.
- [ISOMETRY_SEEDS_5063.json](ISOMETRY_SEEDS_5063.json): 21 distinct
  candidate tiles supporting six noncongruent forbidden patterns.
  These include the observed five-tile mixed-height support whose
  hole has area **86/13 unit tiles**.

Different seed patterns need not coexist as a packing. Each witness's
own supporting subset is checked separately. The seed placements are
optional candidate variables, not assumptions that the full tiling
contains them.

[ISOMETRY_SOURCE_PATTERNS_5063.json](ISOMETRY_SOURCE_PATTERNS_5063.json)
preserves all six exact observed source cuts, their original candidate
indices, and the SHA-256 of their source snapshot. Two source cuts
are congruent and are deduplicated in the seed file. No full solver
snapshot is needed to check the compact source obstructions.

The new 3431 source is preserved separately in
[ISOMETRY_SOURCE_PATTERNS_3431.json](ISOMETRY_SOURCE_PATTERNS_3431.json),
with its four actual placements, complete polygon witness, original
indices, and source snapshot SHA-256. The extracted snapshot contained
33,911 candidates. Independent exact checks confirm that the four
triangles are contained and pairwise nonoverlapping. Their supported
polygon has twice axial area `1122`, hence

\[
n(P)=\frac{1122}{33\cdot7}=\frac{34}{7}.
\]

Its boundary sums are `W0=88`, `W1=36`, giving
`G_even=-26/7` and `G_odd=-30/7`. Both area integrality and signed
population integrality fail. This proves a reusable local forbidden
support, without restricting the odd population of a full tiling.

The 3431 search that discovered this pattern **initially used only the
original triangular seed**. The second pattern was learned during that
run and has now been added to the seed file for subsequent runs.
Historical results from the initial run should retain that distinction.

## 5. Independent controls and observed performance

Run from the repository root:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/corner-tests/verify_pattern_isometries.py
```

The independent matcher derives a complex affine multiplier directly
from the labelled physical vertices, using `Fraction` arithmetic. It
compares complete beta/obtuse/alpha vertex triples instead of native
height and phase keys. Its complete occurrence sets agree with the
production matcher for catalogues containing direct and reflected
copies, rotations, translations, and multiplier heights from `-5`
to `7`. These controls cover all six preserved 5063 sources and the
new four-tile 3431 source. Changing the source anchor leaves the occurrence set unchanged.
Mapped side labels, expanded polygon witnesses, and congruence keys
are checked. Missing members are not inserted and a deliberately
incorrect reflection witness is rejected.

The genuine complete 143 tiling supplies all 143 images of one
triangle under labelled isometries. Its valid unit-area source
polygon cannot be promoted into a no-good. The complete control
output is [PATTERN_ISOMETRY_REPLAY.json](PATTERN_ISOMETRY_REPLAY.json).
The replay also records the hashes of both current seed files.

The stable 5063 source snapshot contained **74,399** candidate tiles.
Native matching returned the following support sets. Every returned
labelled isometry and every expanded polygon witness was then checked
independently.

| Source | Support size | Hole area | Occurrences | Direct | Reflected |
|---|---:|---:|---:|---:|---:|
| 0 | 4 | 16/35 | 1494 | 798 | 696 |
| 1 | 5 | 86/13 | 90 | 36 | 54 |
| 2 | 3 | 484/455 | 365 | 182 | 183 |
| 3 | 3 | 484/455 | 365 | 183 | 182 |
| 4 | 3 | 1056/455 | 829 | 465 | 364 |
| 5 | 3 | 484/455 | 1168 | 576 | 592 |

Sources 2 and 3 are congruent, so those two rows should not be added
as independent families. The final recorded six-scan runtime was
about **0.65 seconds**; an earlier run took about 1.20 seconds.
These are observed runtime measurements for matching only, not
performance guarantees. JSON loading and independent checking are
outside the scan timings. The exact snapshot hash, individual times,
and verification flags are in
[PATTERN_ISOMETRY_BENCHMARK.json](PATTERN_ISOMETRY_BENCHMARK.json).

The optional benchmark can be repeated when that snapshot is available:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/corner-tests/verify_pattern_isometries.py --snapshot /path/to/necessary_model.json
```

The new result is reusable local obstruction propagation. It is not
an UNSAT certificate for either whole target or any complete corner
root, and it does not classify the ungenerated placements.

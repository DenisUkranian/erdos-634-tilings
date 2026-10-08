# No triangle admits a tiling by 154 congruent triangles

Denis Paliy, research with ChatGPT assistance. 8 October 2026.

**Theorem.** There is no tiling of a triangle by exactly 154 congruent
triangles, allowing reflections and arbitrary T-junctions.

This is a computer-assisted exclusion of one complete tile count in
Erdős problem 634. It is not a classification of every tile count. The
proof uses the published exhaustive angular classification and rationality
inputs specified below, together with the repository's written geometric
lemmas and three complete finite position-current refutations. Each of
the three refutations has been replayed by a separately written verifier.
No proposed scale-one W/beta exclusion or prime-case candidate is used.

## 1. Exhaustive reduction to one fixed tile and one fixed target

The [all-branch arithmetic gate](../arithmetic-gates/README.md), with its
[exact report](../arithmetic-gates/checked.json), gives precisely one
possible realization of 154, up to similarity, reflection and relabeling:

```
unit tile: (8,7,13);
large triangle: (91,91,154);
branch: I120, primitive parameters (a,b,c)=(8,7,13), multiplier 1.
```

Indeed `13^2=8^2+8*7+7^2` and `154=7*(8+2*7)`. The classical families
(squares, sums of two squares, or 2,3,6 times a square) do not contain
154: its squarefree part is 154, and its 7-adic valuation is odd.

Exhaustiveness of the nonclassical list uses Laczkovich's angular
classification, as tabulated in Beeson–Zhang, *Rationality of certain
triangle tilings*, arXiv:2604.01314v1, Table 1, and their Theorem 1.2 on
rational side ratios. The necessary integer-scale spectra and their
attributions are in
[the uniform reduction](../../uniform-reduction/PROOF.md). Factoring the
count coefficients leaves finite lists. The preserved divisor sieve and
a second implementation using proved bounded primitive-parameter ranges
agree on the entire candidate set, not only its cardinality.

It therefore suffices to exclude this single fixed geometric instance.

## 2. Every remaining tiling lies in one of five bounded height bands

Put

```
rho = exp(i pi/3),   z=(8+7rho)/13,
P = conv(0,154,49+56rho).
```

P has the three target side lengths. Normalize all directions relative
to its horizontal base. A tile's two short edges have directions
`rho^j z^h` for a common integer h, its **short height**; its long edge
has height h-1 or h+1. The angle of z is an irrational multiple of pi:
`2 Re(z)=23/13` is a nonintegral rational number, whereas a root-of-unity
sum with its inverse would be an algebraic integer. Thus distinct height
classes do not silently coincide modulo a sixth-root rotation.

The [fresh independent structural audit](../w-beta/154_STRUCTURAL_REVIEW.md)
reconstructs the following global argument, valid at T-junctions:

1. Whole-edge median cuts give `n_0=11 mod13` and `13|n_h` for h!=0.
   In particular height zero is occupied and `n_0>=11`.
2. An empty nonzero height separating zero from occupied heights would
   cut off a nonempty tail whose cardinality is divisible by 169.
   This follows by expressing its boundary as whole length-13 steps
   in one direction-height lattice and comparing exact areas.
   Since there are only 154 tiles, no such gap occurs. The support is
   therefore a consecutive interval containing zero.
3. An occupied nonzero height cannot have exactly 13 tiles. The
   [supporting-line argument](../../closure-position-oct7/oct8-structural/NO_THIRTEEN_HEIGHT.md)
   enumerates all admissible signed orientations; whole-line length
   congruences then force two identically oriented tiles to have the
   same 120-degree vertex. Hence every occupied nonzero height has at
   least 26 tiles.
4. Seven occupied heights would require at least `11+6*26=167` tiles.
   The six-height possibility is separately excluded by the complete
   three-direction signed-current recurrence. The reverse implementation
   was freshly rerun, without a time or state cutoff, on all six
   six-height intervals containing zero, and each exhausted as UNSAT.
   Its state, exact finite vector bounds, pruning justification, outside
   endpoint equations and replay results are written in the structural
   audit. This step does not incorrectly discard the feasible population
   sum `24+5*26=154`; those inventories are included in its enumeration.

Consequently every hypothetical tiling has at most five consecutive
occupied heights, including zero. Its support is contained in one of

```
[-4,0], [-3,1], [-2,2], [-1,3], [0,4].
```

Reflection `w -> 154-conjugate(w)` preserves P and sends h to -h.
Only the three representative bands `[-2,2]`, `[-1,3]`, `[0,4]` need be
checked. The position systems permit any subset of their five heights;
there is no assumption that every height in a band is used. Thus these
three systems also cover all one-, two-, three- and four-height tilings.

## 3. The complete vertex lattice, with no arbitrary placement mesh

The [finite-band vertex lemma](../../position-currents-oct7/PROOF.md),
proved using integer seam atoms and whole long-edge partitions at the
extreme directions, gives

```
Lambda_[L,U] = sum_(h=L)^U z^h Z[rho].
```

After the target vertex zero has been fixed, every vertex of an actual
tiling belongs to this lattice. The proof explicitly treats T-junctions
and does not require edge-to-edge gluing or an a priori grid.

For this tile the lattice has a particularly simple exact description.
Let `eta=3+rho` and `bar(eta)=4-rho`. Then

```
eta*bar(eta)=13,   z=eta/bar(eta),
2eta+2bar(eta)-eta*bar(eta)=1.
```

The last identity proves coprimality directly. Factoring
`g=eta^L/bar(eta)^U` from the lattice generators leaves
`eta^(h-L) bar(eta)^(U-h)`. Their endpoint terms are coprime powers;
raising a Bezout identity to a sufficiently large odd power proves
that they generate the unit ideal. Therefore

```
Lambda_[L,U] = g Z[rho].
```

Multiply P and the tile templates by `1/g=eta^(-L)bar(eta)^U` to obtain
integer Eisenstein coordinates. For computational economy an additional
sixth-root rotation is used in two cases; it is applied to both target
and every template and has no mathematical effect on completeness.

At height h the integer short unit vector is
`eta^(h-L)bar(eta)^(U-h)`, times that optional sixth root. The 12 templates
at that height have vertices

```
(0,8rho^j z^h,7rho^(j+2)z^h),
(0,7rho^j z^h,8rho^(j+2)z^h),       j=0,...,5,
```

expressed in the transformed integer coordinates. Both mirror types
are included. Translate each of the 60 templates by every lattice point
in P and retain it exactly when its other two vertices belong to P.
Because P is convex, this tests full containment. Every possible tile
has a unique 120-degree vertex, so this enumeration misses no placement.
The independent verifier reconstructs and checks every template's exact
side norms and positive oriented area.

## 4. Exact necessary currents and a checkable zero-elimination rule

Orient every tile boundary counterclockwise. For each edge A->B and
its unoriented line direction d, place coefficient +1 in row (A,d) and
-1 in row (B,d). This is the one-dimensional derivative of the signed
edge current on its supporting affine line. A point and direction fix
that line, so no position is discarded.

Internal edge currents cancel in a genuine tiling, including at
T-junctions. Therefore the sum of the selected placement columns must
equal the target's endpoint-current vector. Every selection variable
is nonnegative (and in a tiling is 0 or 1). The refutation needs only
nonnegativity, so it also rules out any nonnegative fractional solution
of these necessary position-current equations.

At a zero-right-side row, if all remaining coefficients have the same
sign, every variable occurring there must be zero. Remove those
placements and repeat. At a target row requiring +1, some positive term
must survive; at a row requiring -1, some negative term must survive.
Absence of the required sign is an exact contradiction.

The producer processes 64 endpoint rows at a time using bit masks. A
record specifies the direction, horizontal word and vertical coordinate,
and masks of rows with only positive or only negative support. The
independent verifier recomputes the current supports, checks that each
claimed mask has no opposite-sign support, verifies that it avoids all
nonzero target rows, and removes only the indicated signed incidences.
No producer-supplied numerical bound or asserted solver result is trusted.

## 5. Complete finite results and independent verification

All three entire five-height systems were enumerated and refuted:

| Heights | Basis rotation | Complete contained placements | Verified zero-mask records | Provably removed placements |
|---|---:|---:|---:|---:|
| `[-2,2]` | 0 | 4,773,371,018 | 28,902,031 | 4,773,370,672 |
| `[-1,3]` | 1 | 4,770,414,013 | 29,851,242 | 4,770,413,440 |
| `[0,4]` | 1 | 4,759,540,301 | 29,846,977 | 4,759,539,691 |

The basis rotation column is the exponent of rho. The remaining 346,
573 and 610 placements need not all be removed: each system already has
a nonzero target row with no surviving term of the required sign. The
terminal contradictions occur at the transformed target apex:

| Heights | Transformed apex | Required current sign | Surviving terms of that sign |
|---|---|---:|---:|
| `[-2,2]` | `(8281,9464)` | -1 | 0 |
| `[-1,3]` | `(-1365,16016)` | +1 | 0 |
| `[0,4]` | `(7049,10591)` | +1 | 0 |

The three separate PASS reports are
[center](bitmap_five_center_replayed.json),
[offset](bitmap_five_offset_replayed.json), and
[extreme](bitmap_five_extreme_replayed.json).
In total they independently check 14,303,325,332 candidate placements
and 88,600,250 mask records. Candidate totals are exact enumerations of
allowed positions, not counts of completed tilings searched.

The producer and verifier are separate programs. In particular the
verifier initializes the complete lattice positions by rational
intersection of horizontal lines with the target's three boundary
segments, whereas the producer uses directed half-plane floor/ceiling
formulas. It builds and norm-checks the rotated templates independently.
Every recorded elimination is replayed; no floating point tolerance,
heuristic pruning, imposed corner patch, optimizer status, or resource
limit supplies the negative conclusion.

A further [independent arithmetic/implementation audit](../154-code-audit/)
reproduced all three candidate counts by directly eroding half-plane
constraints. It compared the producer's word extraction and deletion
operations against individual-bit reference operations on 442,476 tests
under undefined-behavior sanitization. A known four-tile positive control
also survives the same positioned model and passes a separate exact
geometric check. These support the implementations; the full negative
claims rely on the replayed certificates and the written completeness
argument above.

## 6. Conclusion and reproduction

By section 2 every hypothetical 154-tiling is covered by one of the
three tested bands or its reflection. Section 3 enumerates every
placement in each band, section 4 supplies necessary current equations,
and section 5 proves all three systems inconsistent. The sole geometric
candidate is impossible. Section 1 then excludes every triangle and
every congruent tile shape at N=154. QED.

From the repository root:

```
python research/final-closure-oct8/arithmetic-gates/check.py
python research/final-closure-oct8/154-audit/reproduce_bitmap.py
```

The second command compiles the preserved C++17 producer and independent
verifier, regenerates each large trace in a temporary directory, replays
it, and deletes that intermediate trace before the next band. With
preexisting uncompressed traces, use `--existing-trace-dir PATH`; the
required names are `634-bitmap-five-{center,offset,extreme}.json` and
matching `.bitmap_trace.bin` files. The structural audit identifies its
separate reverse-recurrence and no-thirteen replay commands and reports.

All production runs used here finished with actual contradictions, and
all independent replays finished PASS. A timeout on another machine
must be reported as incomplete and is not a replacement for replay.
Trace/source hashes are preserved alongside these files. The result has
received internal independent checks, not external referee acceptance or
proof-assistant verification. The general Erdős 634 classification,
including other unresolved counts, remains outside this theorem.

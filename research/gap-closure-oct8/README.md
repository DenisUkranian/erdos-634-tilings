# Closing constructive gaps — 8 October 2026

Denis Paliy, research with ChatGPT assistance. These are partial results
for Erdős problem 634; the general classification remains unfinished.

## Completed general construction

For every integer `u>=2`, set `v=u+1` and fix the primitive tile
`(uv,2u+1,v²)`. **Every integer scale `m>=v` is realizable in both the
W and beta families**:

| Target sides | Number of congruent tiles |
|---|---:|
| `m(v³,u(2v²−u²),v(2u+1))` | `(2v²−u²)m²` |
| `m(v³,v³,u(3v²−u²))` | `(3v²−u²)m²` |

The [complete proof](group1/PROOF.md) supplies all missing seed scales in
`[v,v+u−1]` by a uniform positive dissection, then applies the earlier
arbitrary-seed `+u` cap. The [residual dissection](group1-helper/ADJACENT_ALL_SCALES.md)
has an elementary layered construction. Its whole parameter domain is
checked by exact polynomial identities and signs; sample computations
are not an extrapolation premise.

The [independent internal mathematical audit](literature/ADJACENT_INDEPENDENT_AUDIT.md)
checks the partition, metric, boundary argument, seed coverage, and the
degenerate empty layer at the endpoint `t=2`. Four full coordinate
examples have separate exact pairwise-intersection checks. This is
internal review, not external refereeing or formal proof-assistant verification.

The result lowers the previous general sufficient threshold
`uv−u+1=u²+1` to `u+1` in this entire adjacent-parameter sector.
It does **not** exclude smaller scales, and does not cover arbitrary
coprime parameters `v−u>1`.

## Concrete branch-isolated positive counts

The theorem constructs **5022** and **7502** with tile `(42,13,49)`.
Both have only that ordered W candidate in the complete arithmetic
overlist, even before optional scale-one removals. For 5022 the
[full 5022-tile certificate and independent integer check](examples/README.md)
are supplied. No historical priority is asserted for these individual counts.

## Other work and remaining gaps

The [whole-long-edge boundary theorem](structure/WHOLE_C_BOUNDARY.md)
allows arbitrarily many interior direction classes. If a tiled region
has boundary steps in one `c Z[rho]` direction lattice, then its tile
count is divisible by `c²` and is at least `2c²`. When `ab` is even,
it is divisible by `2c²`. Holes and T-junctions are allowed, with the
direction-normalization hypothesis stated in the proof. Two boundary
direction classes do not satisfy this theorem's hypothesis. This is a
necessary geometric restriction, not a general existence criterion.
An [independent Laurent-polynomial proof](group1-helper/WHOLE_C_INDEPENDENT.md)
derives the same conclusions by evaluating the boundary identity modulo
`3ab`; no finite enumeration is used in either proof.
The [final audit](group1-helper/AUDIT.md) also checks the separating-gap
application and binds the reviewed source by its content hash.

The [seed-extension note](literature/SEED_EXTENSION.md) applies an existing
triangle addition law; its weaker adjacent conductor is superseded by
the theorem above. Source attributions and the status of imported
negative claims are separated in the [literature audit](literature/README.md).

The [F3 residual analysis](f3-general/HEXAGON_STRUCTURE.md) identifies an
equilateral sufficient construction and proves the failure of a particular
single-seam realization of an unplaced inventory. It does not prove a
necessary normal form. Restricted template or solver failures do not
exclude arbitrary tilings.

In particular, **14430 remains unresolved in this work**. Its unique
ordered candidate is F3 with tile `(56,9,61)` at scale one. Neither this
case nor the general small-scale W/beta and F3 questions are closed by
the positive adjacent theorem.

## Reproduction

From the repository root, with Python 3:

```sh
python research/gap-closure-oct8/group1/check_all_adjacent_symbolic.py
python research/gap-closure-oct8/examples/check_5022.py
python research/gap-closure-oct8/group1/all_adjacent_formula.py --u 4 --t 3 --output /tmp/W2176.json
python research/universal-closure-oct8/group1/verify_general_geometry.py /tmp/W2176.json
```

The positive construction and its checkers require no optimizer. Discovery
scripts and incomplete F3 searches are retained separately and are not
dependencies of the theorem.

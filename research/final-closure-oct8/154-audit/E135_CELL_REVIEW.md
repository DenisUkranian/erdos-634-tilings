# Independent review of the 98-tile gap-tail exclusion

8 October 2026. This audit establishes a necessary direction-support
restriction for N=135; it does **not** decide N=135.

I read `../e135-structure/NO_GAPS.md` and checked its mathematical reduction
separately from the finite containment computation. The reduction is sound
with the stated whole-edge and height-divisibility inputs:

* Connectedness of the positive-length contact graph, and height difference
  at most two across a contact, imply that interior missing heights are
  isolated. Thus two positive gaps would give strictly nested tails, not
  two names for the same tail.
* A tail has cardinality divisible by 49. The 49-tile exclusion uses the
  Laurent character alone and does not depend on the total enclosing count.
  A 98-tile tail must have zero character: the nonzero alternatives
  M=+90,-90 require at least 11|M|/9=110 tiles.
* At an empty height k every edge of that direction class is a long edge.
  Since the outer boundary has height zero, each maximal relevant straight
  seam has whole length-seven partitions on both banks with the same ends.
  They match edge for edge. The tail's actual positioned boundary, and
  each of its interior-connected components, therefore consist of whole
  seven-edges, not arbitrarily cut residual segments.
* A 98-tile tail has one interior-connected component; a second component
  would have size 49, already impossible. Any bounded complementary hole
  would contain a positive multiple of 49 tiles by the same exact lattice
  area argument. Only 37 tiles lie outside the tail, so there is no hole.
* Its outer boundary is consequently in one affine copy of the triangular
  lattice with unit side 7z^k. It encloses 30 elementary cells. The zero
  boundary character forces exactly 15 cells of each orientation. The
  central 37-tile block has at most three occupied heights; the possible
  positive gap indices are k=1,2,3. Reflection handles negative gaps.

The last three cases were checked with a **separate implementation**,
`check_e135_cells_independent.py`. It imports neither the producer nor its
geometric functions. Whereas the producer rotates the target and obtains
inequalities in inverse coordinates, this verifier maps each cell forward
by 7z^k into the original equilateral target. It clips the translation
fundamental square by exact rational halfplanes and tests all three cell
vertices directly in physical coordinates when counting containment.

The finite enumeration covers all real translations. Every cell's allowed
translations form a closed convex polygon. At a translation attaining any
given collection of cells, the intersection of their allowed polygons is
nonempty, closed and bounded. It has an extreme point on the enumerated
constraint lines; that point contains at least the same collection. Thus
arrangement vertices suffice even for boundary-only or lower-dimensional
feasible translation sets. The independent anchor rectangle is justified
by the norm bound, rather than copied from the producer.

| Gap k | Potential cells | Arrangement vertices | Max up | Max down |
|---:|---:|---:|---:|---:|
|1|47|100|12|14|
|2|45|161|12|14|
|3|46|165|16|13|

The independent table agrees exactly with the producer. Every case lacks
15 cells of at least one orientation, contradicting the proposed tail.
Hence the occupied short-edge heights in any N=135 equilateral instance
are consecutive. The separate population/charge argument is needed for
the additional at-most-nine assertion; the cell computation alone does
not establish that bound or nonexistence of a tiling.

The checked output, including source hashes, is
`e135_cells_independent.json`. Reproduce with:

```sh
python3 research/final-closure-oct8/154-audit/check_e135_cells_independent.py
```

This is an independent implementation and internal mathematical review,
not an external peer review.

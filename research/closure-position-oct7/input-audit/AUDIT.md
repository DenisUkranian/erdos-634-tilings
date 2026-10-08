# Fresh audit of the supplied position-sensitive 154 certificate

7 October 2026. This is a separate internal replay and review, not external
referee approval or proof-assistant verification. The source baseline is
`d460b3d23a90953e9524fba5e7616be71b779efd`.

**Conclusion:** the supplied proof and certificate support the statement
that a tiling of `(91,91,154)` by `(8,7,13)` must use at least three
short-edge direction classes modulo 60 degrees. This audit found no gap in
that restricted conclusion. It does **not** decide 154 or Erdős 634.

## Fresh computations

The original archive and extracted input files were preserved. All 22
entries in its SHA256 manifest were independently recalculated and matched;
the archive and standalone note hashes are recorded in
`input-integrity.json`. The full `reproduce.py` pipeline was then executed
in a separate temporary copy, without using an existing generated matrix.

The fresh results, retained in `fresh-replay.json`, are:

| Check | Result |
|---|---|
| Complete lattice anchors | 56,183 |
| Orientations, both chiralities | 24 |
| Contained placements | 873,496 |
| Positioned boundary rows | 550,333 |
| Individually checked signed matrix entries | 19,222,288 |
| Retained forced assignments checked | 678,493 |
| Final contradiction | row 70104: residual 1 outside `[-1,0]` |
| Known 88-tile positive control | PASS; 3,828 exact tile-pair checks |
| Missing/duplicate tile controls | Both rejected |
| First certificate assignment deliberately reversed | Rejected as not forced |

The entire fresh pipeline took 13.53 seconds on this environment and its
maximum child resident set was 1,142,912 KiB. Generated temporary files
occupied approximately 252 MiB; they have not been copied into the research
repository. The performance figures are observations, not complexity bounds.

## Mathematical and implementation review

The following points were checked against the actual source code and the
repository's integer-atom and height-cut proofs.

1. The finite-band lattice follows from integer atoms at internal heights.
   At an extreme direction all available collinear sides have length `c`;
   maximal collinear components in the convex ambient target have matching
   whole-edge partitions on both banks. There is consequently no unaccounted
   fractional phase at these extreme directions. The identities involving
   `c*z^(L-1)` and `c*z^(U+1)` place their displacements in the claimed module.
2. For heights 0 and 1, the basis `1,(3+rho)/13` and congruence
   `p-3q=0 mod 13` are exact. The target inequalities and the row-by-row
   anchor bounds agree with the independent rectangular scan. Convexity
   makes vertex containment sufficient. The two orders of the short sides
   and six rotations at each of the two heights exhaust both chiralities;
   the unique 120-degree corner supplies the anchor.
3. The matrix builder's ambient-coordinate gcd and the audit's lattice-basis
   gcd define the same positioned primitive segments. The audit compares
   all signed entries, rejects repeated rows in any column, and independently
   reconstructs the target boundary. The integer sizes used by the generator
   are adequate for the explicit coordinate and determinant ranges.
4. The current criterion does not need an integrality theorem for its
   matrix. A nonnegative real solution implies weighted coverage one by
   cancellation of jumps across the finite edge arrangement. Each weight
   is therefore at most one. Refining at crossing points, even though such
   refinements are not separately stored as matrix rows, preserves equality
   of the segment currents.
5. Every retained certificate step is justified for arbitrary real weights
   in `[0,1]`. The C++ verifier recomputes the full cited row, checks the
   variable really occurs and has not previously been assigned, and checks
   that its proposed value is forced by a tight row bound. Its final
   contradiction is recomputed independently of the proof producer.
6. The passage from adjacent heights to all at-most-two-height cases uses
   additional written mathematics, not the computed matrix. The existing
   whole-edge cut identity gives `13 | n_h` for `h != 0`, so height zero
   occurs. Positive-length contact connectivity permits a second height
   only at distance one or two. With heights 0 and 2 only, a height-2
   component has its remaining boundary in whole length-13 edges of height
   1; its signed area gives `169 | number of component tiles`, impossible
   within 154 tiles. Reflection handles the negative heights. These
   arguments allow nonconvex components and holes through signed whole-edge
   boundary walks.

## Limits of this audit

The two-height certificate is exhaustive in positions **under that height
restriction**. It neither supplies nor assumes a universal bound of two
heights, a way to remove intermediate heights, or integer feasibility of
arbitrary fractional solutions. The component argument in item 6 ceases
to give whole length-13 boundary edges when an intermediate short height
is present. Three or more heights are not excluded here.

The geometry and matrix audits have different enumeration and atomization
implementations, but share the supplied metadata after its formulas were
reviewed. This is useful implementation diversity, not an assertion of
complete software independence. The original all-branch reduction to this
specific target is a separate result; it is not needed for the restricted
statement audited here.

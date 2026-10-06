# A necessary collar budget for a single pure-state replacement

6 October 2026. This lemma strengthens the existing
[nonconvex counterexample](nonconvex-chirality-counterexample.md), not a
nonexistence claim for global or mixed normalization.

Scale its `(3,5,7)` island by an integer M and subdivide to original unit
tiles. Its boundary requires opposite-state orientation-pair counts
`M²(930,-30,962)`. Surround it by an actual collar Q tiled in that opposite
pure state, so their union is a polygonal disk. If the entire union admits
an opposite-state filling, its counts are necessarily

    M²(930,-30,962) + n(Q).

Indeed, the opposite-state boundary lift closes around the island; lifted
vector areas add across the collar, and each collar tile contributes one
unit to its orientation pair. Therefore Q must already contain at least
`30M²` tiles of the second pair. In particular, bounded numbers of outside
tiles cannot suffice. A collar of fixed geometric width has area O(M), so
cannot suffice for arbitrarily large M either. This does not preclude a
collar of area O(M²), multiple intermediate moves, or moves using additional
orientation states, and it does not refute a finite parameterized grammar.

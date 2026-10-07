# Complete membership criterion for square class 78

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

Let S be the positive integers for which some nondegenerate triangle
can be tiled by that many congruent nondegenerate triangles, allowing
reflections and arbitrary T-junctions. Then, for every positive integer m,

\[
\boxed{78m^2\in S\quad\Longleftrightarrow\quad 2\mid m.}
\]

For even m, use the new tiling of the `(49,91,120)` triangle by 312
congruent `(3,5,7)` triangles and subdivide each tile into `(m/2)²`
congruent copies.

For odd m, the necessary angular spectra isolate F3. Its count and norm
equations yield an explicit positive rational point on
`y²=x³+156x²-2028x` with `v_2(x)=1`. The square class of x must be
one of 2,6,26,78; all four are excluded by elementary congruences modulo
13. This proves nonexistence for every odd multiplier without a rank
computation or an assumed complete basis of rational points.

- [Full proof and dependencies](../research/best-move-oct7/new-arithmetic/CLASS78.md).
- [Independent internal audit](../research/best-move-oct7/geometry/CLASS78_AUDIT.md).
- [Positive construction](../research/best-move-oct7/hexagon/F3_SMALL_A.md)
  and [independent unit-coordinate report](../research/best-move-oct7/hexagon/verification.json).
- [Full continuation package and reproduction commands](../research/best-move-oct7/README.md).

This closes one entire square class. It does not classify all tiling
counts or resolve the remaining 154 and 4830 cases.

# A connected whole-c boundary domain cannot contain only c tiles

20 November 2026. A local theorem about genuine tiled domains.

Let a connected polygonal domain be tiled by `m` congruent primitive
odd `(a,b,c)` tiles, using arbitrary short heights and T-junctions.
Assume its oriented boundary is a finite chain of whole length-`c`
segments in allowed tile directions, at arbitrary heights. The
segments may be long sides of neighboring outside tiles; they need
not all be long sides of tiles inside the selected domain.

Assume that the positive-length edge-contact graph of the selected
tiles is connected, as it is for the tiles of a polygon with connected
interior. A collection connected only at isolated vertices requires
separate treatment.

**Theorem.** The domain cannot have `m=c`.

Write `d=a-b`, `D=sum epsilon`, and
`D_*=sum (-1)^h epsilon` over the selected tiles. The ordinary and
alternating boundary characters give

\[
 (d-c)D\in c\mathbb Z,\qquad (d+c)D_*\in c\mathbb Z.
\]

Because `gcd(c,d)=1`, both `D` and `D_*` are divisible by `c`.
If `m=c`, they have absolute value at most `c` and odd parity.
Hence `|D|=|D_*|=c`. All tiles have the same sign, and all their
short heights have the same parity.

Two adjacent tiles have short heights differing by at most two.
If they differ by two, their common contact consists of long-edge
intervals at the intervening height. The two directed long sides
point in opposite directions along the supporting line. Each tile's
long-edge ordinary character is `-c epsilon`; the signs of the two
tiles must therefore be opposite. This argument does not require
whole-to-whole matching. It contradicts their common sign.

Parity excludes a height difference of one. Connectivity now implies
that all selected tiles have one short height `h`.

On every supporting line of height `h`, the signed exterior length
is a multiple of `c`, because the boundary consists of whole
`c`-segments. Internal edges cancel, and complementary long edges
also have lengths `c`. The published `LINE_COUNTS.md` single-block
argument therefore applies: `c` same-sign tiles at one short height
with these per-line congruences are impossible. This finishes the
proof.

If every boundary segment is specifically a long side of an inside
tile, the last step is shorter: the boundary has heights `h-1,h+1`
and no height-`h` segment, so all selected short-edge currents cancel,
giving `dD=0`, impossible. This shortcut is not valid for a boundary
that is merely represented by neighboring whole long edges: it may
have height-`h` segments made from several short edges of selected
tiles. The line-count argument handles that broader case.

## Limitation at three blocks

At population `3c`, the characters can have values `+/-c` as well
as `+/-3c`. Their absolute-value bounds no longer force either a
common sign or a common height parity. Thus the preceding argument
does not exclude `3c` and does not give a general odd-domain lower
bound of `c^2`.

In the purely geometric boundary sense, `2c` is an attainable local
count. A parallelogram formed by a tile and its half-turn mate across
an `a` side has side lengths `b,c`. Arrange `c` such cells along the
`b` direction. The resulting parallelogram has sides `bc,c`, contains
`2c` tiles, and its sides subdivide into whole `c`-steps at two
consecutive heights. These geometric steps on its short-side
boundaries are not asserted to be long edges of an existing outside
F2 completion.

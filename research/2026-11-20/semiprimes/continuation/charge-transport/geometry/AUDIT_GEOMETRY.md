# Independent review of actual median charges

This is a mathematical and source review of
[ACTUAL_MEDIAN_CHARGES.md](ACTUAL_MEDIAN_CHARGES.md), including its final
boundary-vertex anchoring lemma. No new placement search or solver run
was performed for this review. The existing exact replay reports and
their checking code were inspected.

Reviewed SHA256 values:

| File | SHA256 |
|---|---|
| `ACTUAL_MEDIAN_CHARGES.md` | `5a4ca8f6a58e028b5b6e91187be52daf671be9bbdad03daff582b5eacf2cf37e` |
| `verify_actual_median.py` | `914baeae7f09fc6dab8e84cf5d70a22176771185bf6242c1fd1654244a306424` |
| `verify_even_corner.py` | `e270beedce511f32bff0acf29ed08ed824b65d91bd317c7fcfc19b99af7bde73` |

The final publication CLI change was independently reviewed against
the original corner checker. It adds `main()`, optional `--out`, and
a rejection of Python `-O`; without `--out`, the checker only prints
its results instead of overwriting the adjacent replay file. The
`record` function, tested shapes, mathematical assertions and JSON
contents are unchanged. The other two reviewed files retain their
frozen hashes above.

**Assessment:** no error was found in the stated identities or the
conditional theorem for the two target boards. The assertions depend
on the cited full-tiling phase, median-polygon and supported-cycle
theorems. They do not exclude the minimal odd population, imply a
global `5c` bound, or decide either target.

## 1. Frame, signs and median split

The displayed isometry takes standard short height `h` to `2-h` and
changes the tile sign to its negative. Thus parity is unchanged, but
the standard totals `G_odd=-c,G_even=-d` become `+c,+d` in the path
frame. There is no sign mismatch between the two packages.

For the base-side polygon, the base followed by the reversed upper
path is the positive boundary. Its two characters are therefore

\[
 c^2-c(J+K),\qquad c^2+c(J-K).
\]

Substituting the two congruence parameters and dividing by the tile
characters gives

\[
 G(D)=c(i-1),\qquad G_*(D)=c(j_0+1).
\]

The two path counts have the same parity; because `c-d` and `c+d`
are odd, `i-j_0` is even. Consequently the stated integer `t` and
the exact split

\[
 G_{\rm odd}(D)=c(t-1),\qquad
 G_{\rm odd}(E)=c(2-t)
\]

are correct. The sum uses the total charge `+c` in this frame. A
canonical path has `t=0`; nothing in the argument forces an arbitrary
genuine upper path to be canonical.

## 2. What follows from exactly `3c` odd tiles

The positive odd populations on either side of a genuine upper median
cut are each at least `2c`. Hence all odd tiles must lie on one side,
and the split forces `t=1` or `t=2`.

The proof does need an actual long-height-2 path step. It obtains one
correctly: `K=(c-d)t-d*j_0`, so `K=0` would imply `d` divides `t`.
This is impossible for `d=26` or `22`. That step has a height-1 bank
tile below the cut. Therefore all odd tiles lie below, `t=2`, and
their unique occupied odd height is 1. The uniqueness uses `3c<4c`
and the ordinary positive-height-population lower bound.

At height 1, the same inequality allows only one exact own-node in
each prime tree. Their intersection, among the already established
global vertex coordinates in `R[1/c]`, is a single Euclidean translate
of `zR`. No unsigned divisibility of an arbitrary joint cell is
being assumed here. The upper path begins at zero and both its step
alphabets lie in `zR`, so the identified height-1 bank tile anchors
that translate at `zR` itself. The sign populations are then exactly
`2c` and `c`.

The standard-frame translate stated in the note is consistent with
the inverse isometry: it is `H*rho+zR`, with `H=a(a+2b)`, and this
equals `b(2a+b)+zR` because

\[
 H\rho-b(2a+b)=c^2\rho z^2\in zR.
\]

The exclusion of even heights outside `0,1,2` correctly uses the
occupied-immediate-parent theorem for a nonempty exterior-free
subtree. The chosen tree puts the parent of an occupied height at
the neighboring odd height toward the exterior. That odd height
would be absent. This argument concerns actual full-tiling nodes,
not apparent gaps in a finite catalogue.

## 3. The upper remainder, and the scope of cancellation

After the preceding deductions, the upper remainder contains only
heights 0 and 2, and its boundary has heights 1 and 2. Selecting all
its height-zero tiles therefore cancels their short-height-zero edges
internally: an exterior height-zero segment is unavailable, and no
height-1 tile remains there to supply a long-height-zero contact.

The long-height-minus-one edges pair completely. These runs have no
other available short-height class and no boundary segment of the
upper remainder. Cancelling those full pairs leaves a whole-length-`c`
height-1 chain bounding the selected positive-area union. A nonempty
selection would supply a supported simple pure-mesh cycle. Applying
the target cycle exclusion therefore removes height zero from this
particular remainder.

This is precisely where the location of the selected union matters.
The identical cancellation is unavailable for all height-zero tiles
in the board, or for the lower polygon. The note explicitly preserves
that distinction.

## 4. Boundary-vertex anchoring

The new lattice lemma is valid for the finite triangle tiling under
its stated hypotheses. Consider one component of the graph joining
tiles at common corners. Choose a linear functional with distinct
values at all distinct tiling vertices and maximize it on that
component. Every ray from the maximizing vertex along an incident
tile side points strictly into the decreasing open half-plane.
The finitely many incident corner sectors consequently occupy total
angle strictly less than pi.

If that vertex were not a polygon vertex, the local region would be
a full disk or a half-disk. All corner-tiles there belong to the same
graph component. At most one other tile can pass through the point
with the point strictly inside a side: its sector occupies a
half-plane, and two such sectors would leave no positive corner
sector. Thus the corner component would have angle pi or `2*pi`,
contradicting the strict maximum. The component is therefore anchored
at a polygon vertex. Membership in the positioned lattice propagates
through tile edges and shared corners.

For a disconnected or touching upper remainder, the note explicitly
designates non-smooth boundary points and path/outer-arc contacts as
polygon vertices. These are board vertices or path vertices. They
all lie in `z^2 R`: after division by `z^2`, path steps are integral
units times `c` or `c/z=a+b-b*rho`, and the board vertices satisfy
the same membership. Every height-2 tile-edge vector belongs to this
lattice as well. The lemma therefore proves that **all tiles in the
upper remainder** are in the native translate `z^2 R`, without
assuming convexity or whole-side adjacency.

This proves no corresponding statement for height-two islands below
the cut. The note does not assert one.

## 5. Counterchecks retained in the final note

The whole-board height-zero selection has the two-alphabet identity

\[
 \partial U_0-\Gamma_{\rm base}=L_{01}-L_{10}.
\]

The term `L_10` includes internal long-height-zero contacts with
height-one tiles. Their short-height-zero neighbors cannot be
discarded merely from native height-one localization. Thus this
identity cannot be replaced by a pure-height-1 boundary chain. The
base-gap calculation and the remaining negative-sign count are
necessary arithmetic only; they do not eliminate `L_10`.

The even-height corner pair is a valid local countercheck. Its two
tiles share `O -> cz`, have obtuse vertices on opposite sides, and
fit the target corner using short heights 0 and 2. The inspected
checker verifies containment and disjointness, while its replay
explicitly states the partial-packing scope. It does not assert a
completion or a counterexample to a global theorem.

Finally, absence of height zero would genuinely leave a two-height
board. The previously certified `8c` population lower bound (or its
odd-block refinement `9c`) then contradicts `n_1=3c`. This use of
the restricted certificate is valid because its extra hypothesis
has first been established in that conditional case.

## 6. Positive controls and final status

The inspected replay reports the two complete 143 controls with
upper-path data `J=-2,K=14,t=2`, and lower/upper counts `105/38` and
`91/52`. The checker first verifies positive tile-boundary equality
with the board, exact areas and containment; its later checks include
the actual bank side of every path edge and the native translates
of both regions. These examples test the identities and geometric
conventions. They do not instantiate the target-only hypothesis
`n_odd=3c` or certify the no-supported-cycle theorem for the 143 shape.

No remaining proof defect was found. The resulting theorem is a
rigorous conditional localization of the minimal odd-population
case. A lower bound for the true positional cost of the internal
chain `L_10` is still missing, so both target existence questions
remain open.

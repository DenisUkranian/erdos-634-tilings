# A balanced remote strip supported by only 2b parent tiles

21 November 2026. This is a **local positive packing**, not a complete
tiling of either F2 board. It shows that the previously displayed
`2a`-parent balanced strip does not give a universal local lower bound
on parent-bank population. In particular, local mixed-cycle geometry
does not force 33 negative parent tiles at 3431.

The construction fits strictly inside the original path-frame board,
uses a nonnative height-zero class `z+R`, and has every parent tile in
the unique native height-one class `zR`. It therefore respects the
positioned classes of the minimal-odd normal form as a partial packing.

| Target | Balanced interior | Parent bank tiles | Parent positive | Parent negative |
|---:|---:|---:|---:|---:|
| 3431, `(33,7,37)` | 74 | **14** | **7** | **7** |
| 5063, `(35,13,43)` | 86 | **26** | **13** | **13** |

No claim that these are minimum possible parent costs is made. An
unknown completion can add tiles to the interior phase node, change
its physical boundary, and require additional parent contacts. Hence
this example does not refute a hypothetical stronger theorem whose
proof uses the entire target-board complement.

## 1. The parallelogram and its balanced tiling

Put

\[
 R=\mathbb Z[\rho],\qquad z=(a+b\rho)/c,\qquad
 V=a+b\rho=cz,\qquad T=bc\rho,
\]

and choose the exact shift

\[
 S=z+c(22+3\rho).
\]

The selected region is the parallelogram

\[
 P=\operatorname{conv}\{S,S+V,S+V+T,S+T\}.             \tag{1}
\]

For `0<=k<c` use the following two original-shape tiles, in the usual
`(q,h,j,s)` notation:

\[
 (S+(k+1)b\rho,\ 0,3,+1),\qquad
 (S+a+(k+1)b\rho,\ 0,0,+1).                           \tag{2}
\]

Their common `a` side is the diagonal of the `k`-th cell. The cells
partition (1). The first tile has sign -1 and the second sign +1,
so the region contains exactly `c` tiles of each sign and has charge
zero.

The long edge of the second tile in cell `k` is the half-turn mate
of the first tile's long edge in cell `k+1`. There are `c-1` such
pairs. Exactly two long end edges remain unpaired, at the two sides
parallel to `V`. The two other boundary sides have physical height
zero and length `bc`.

## 2. Actual parent teeth: b on each bank

For `0<=i<b`, put

\[
 \beta_i^{L}=S+(i+1)c\rho,\qquad
 \beta_i^{R}=S+V+ic\rho.
\]

The parent tiles are

\[
 (\beta_i^L-bz,\ 1,1,-1),\qquad
 (\beta_i^R+bz,\ 1,4,-1).                             \tag{3}
\]

The left one has sign +1 and the right one sign -1. The identity

\[
 z(b+a\rho)=c\rho
\]

shows that their long edges are exactly the successive `c`-intervals
on the left and right sides of (1). Thus these are actual supporting
tiles, not an abstract division of a geometric boundary.

Every left tooth lies outside the parallelogram in the half-plane to
its left; every right tooth lies outside in the half-plane to its
right. On either bank the vertices lie between the consecutive base
endpoints in axial `y`, since `0<b^2/c<c`. Consecutive teeth therefore
have disjoint interiors. The two banks are separated by the whole
parallelogram, and all teeth are disjoint from its interior.

The patch contains `2c+2b` tiles. Its boundary consists only of
height-one edges: the two exposed interior long end edges and the
parent teeth's short sides. Every one of the selected region's four
boundary runs is a chain of actual long edges. Their beta-to-alpha
directions are consistently clockwise, so this is also a supported
directed mixed-height cycle with `2b+2` edges.

## 3. The exact phase conditions

Every interior tile has vertices in `S+R=z+R`, because `S-z in R`.
This is nonnative since `z notin R`.

Also `S in zR`: indeed `c/z=(a+b)-b rho in R`. The vectors `V=cz`,
`c rho`, and `bz` all belong to `zR`, so every parent vertex in (3)
lies in `zR`. All parent tiles consequently belong to the native
height-one Euclidean class.

For the patch as a completely tiled polygon, the selected height-zero
node is terminal in the decreasing-height tree: the patch contains
no negative short heights. It is exterior-free because all outer
edges have height one. Relative to the F2 board, the selected class
is the nonzero remote class `L_1^-=z+R`; it differs from the native
height-zero outer-edge class, and its decreasing subtree cannot
contain the height-two outer edges.

This exterior-free identification survives as a phase label in any
completion. The claim that the selected node contains exactly these
`2c` tiles does not survive automatically: a completion may add more.

## 4. Exact containment and replay

The path board has vertices

\[
 0,\qquad c^2,\qquad a(a+2b)z^2.
\]

`verify_balanced_b_strip.py` constructs every vertex with rational
arithmetic. For both targets it verifies strictly positive oriented
half-plane determinants at every board side, so every tile lies
strictly inside the original board. It also verifies:

* squared side lengths `a^2,b^2,c^2` and positive determinant `ab`;
* all pairwise interior-disjointness tests by separating edge lines;
* containment of every interior tile in the parallelogram and equality
  of their total area with its area;
* both real parent-bank partitions into `c`-edges;
* all `c-1` exact long-edge half-turn pairs and the two unpaired ends;
* the actual sign inventories and the exact memberships in `z+R`
  and `zR`.

The saved placements are `balanced_b_strip_3431.json` and
`balanced_b_strip_5063.json`. `BALANCED_B_STRIP_REPLAY.json` records
both successful exact checks.

```sh
python3 verify_balanced_b_strip.py
```

The only conclusion about the proposed 33-negative-parent bound is
its **local obstruction**: a balanced terminal polygon with the
correct positioned classes and strict target-board containment can
use only seven negative parent teeth. Excluding such a configuration
in a complete 3431 tiling requires a global completion argument.

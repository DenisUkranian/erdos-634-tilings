# A universal nine-tile collar for the scale-two W short side

7 October 2026. This does **not** decide W at scale two, any open N, or
Erdős 634. It proves that the newly forced short-side word has a genuine
local geometric realization for every consecutive parameter pair. The
remainder of the target is not tiled here.

## The precise result

Let `v>=3` be an integer, put

    u=v-1, a=uv, b=v²-u²=2v-1, c=v², Q=b+c, D=4v²-u².

The scale-two W triangle has side lengths `2v³, 2uQ, 2vb` and requires
`4Q` tiles. By the proved
[boundary theorem](../w-global-oct7/ADJACENT_C_EDGES.md), its short side,
from its `2alpha` corner to its `alpha+beta` corner, must have word
`c,c,a,a`.

**Proposition.** For every such v there are nine actual congruent tiles
inside that W target with pairwise disjoint interiors which realize the
entire word `c,c,a,a` and completely fill the angle fans at all five
vertices of this subdivided short side, including both target corners.

Consequently the side word together with its five local angle fans does
not itself contradict geometry. This proposition gives neither an
extension of the collar to a full tiling nor an obstruction to extension.

## Explicit coordinates

Coordinates `(x,y)` below mean physical coordinates `(x,y sqrt(D))`.
Put

    C=(0,0), A=(2(a+c),0),
    O=((2v⁴-4v²u²+u⁴)/v, uQ/v).

Then `CA=2vb`, `CO=2v³`, `AO=2uQ`; the target is `CAO`.
Define

    r=bQ/(2c), h=bu/(2c), s=b(b-c)/(2a), k=b/(2v),
    J1=(c,0), J2=(2c,0), J3=(2c+a,0),
    R0=(r,h), R1=(c+r,h),
    S0=(2c+s,k), S1=(2c+a+s,k),
    P=O/(2v),
    W=A + b(O-A)/(2uQ),
    U=J2 + c(R1-J2)/a.

The nine triangles are:

| Role | Vertices |
| --- | --- |
| First supported c-edge | C, J1, R0 |
| Second supported c-edge | J1, J2, R1 |
| First supported a-edge | J2, J3, S0 |
| Second supported a-edge | J3, A, S1 |
| Complete the fan at C | C, R0, P |
| Complete the fan at A | A, S1, W |
| Complete the fan at J1 | J1, R0, R1 |
| Complete the fan at J3 | J3, S0, S1 |
| Complete the fan at J2 | J2, S0, U |

Here P lies on CO and W on AO. At C the two angles are `alpha+alpha`;
at A they are `beta+alpha`. At J1 the two supported angles are
`beta,alpha`, and the added tile supplies gamma. At J2 and J3 the
supported angles are `beta,gamma`, and the added tile supplies alpha.
Thus all three straight fans total pi. The shorter radial side from
J2 to R1 lies on the length-c edge J2U, a legitimate T-junction.

Each triangle has squared edge lengths `a²,b²,c²` and positive doubled
coordinate area `bu/2`. These are rational-function identities in v.
The half-plane and nonoverlap inequalities also hold for every real
`v>=3`, not only for sampled integer parameters.

## Reproducible universal verification

Run

    python research/w-scale-two-oct7/check_symbolic_collar.py

The verifier uses only Python's standard library and the repository's
small rational-function arithmetic from
`../elliptic-sectors/check_alpha_maps.py`. It sets `v=3+x`, checks the
metric and area identities coefficientwise, and proves each required
weak inequality by nonnegative polynomial coefficients for `x>=0` with
a strictly positive denominator. No numerical approximation, sampling,
or external symbolic algebra package is used. Every pair of tiles has
an exact separating edge certified in `symbolic-collar-report.json`.
There are nine metric/area checks, all containment checks, and all 36
pairwise separation checks. This is a direct certificate of the stated
partial patch, not of the untiled remainder.

## Exploratory finite observations, not a universal classification

Before deriving this collar, exact local propagation from both four-tile
roots was tested for `v=3,...,12`; it immediately left at least two choices
at every convex residual vertex. `local_propagation.py` reproduces that
finite observation, with data in `local-propagation.json`. It is not a
complete tiling search.

Completing all five base fans in an exploratory enumeration for
`v=3,...,8` gave 48 surviving collars for the alpha-first second-c root
and eight for its reverse (nine or eleven tiles in total). These counts
were finite observations only, not a theorem for all v; the universal
result proved above is the explicit nine-tile patch. No full DFS was
rerun, and no negative conclusion is inferred.

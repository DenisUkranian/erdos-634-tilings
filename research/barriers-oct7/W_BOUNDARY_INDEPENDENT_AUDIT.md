# Independent audit of the W/beta adjacent-long-edge theorem

7 October 2026. Audit of ../w-global-oct7/ADJACENT_C_EDGES.md.

## Geometric proof

The blocked-endpoint argument is valid for Group-1 W and beta targets,
with no assumption whether a exceeds b. The endpoint naming matters:
the c-edge PQ has alpha at P and beta at Q, so QR=a and PR=b.
The beta endpoint Q cannot be a 2alpha or 3alpha target corner. If it
is a marked straight point or a theta=alpha+beta corner, its remaining
angle across QR is alpha. A first opposite edge has length b or c.
If no opposite edge crosses R, the first b edge and every remaining
edge of the complete Q-to-R bank must be b; neither an a-edge nor a
c-edge fits after the first positive b contribution. This contradicts
b not dividing a. If b>a, the first edge already crosses R.

The beta target corner is treated separately: QR is exterior and R
is on the target boundary. The second chain, across PR, is internal
because neither target has an alpha corner. Convexity blocks extension
past P. At R, extension either leaves the target or enters the crossing
tile found above. Gamma is forbidden at both endpoints, so a full
b-edge is impossible, and the remaining whole-edge bank would consist
entirely of a-edges, contradicting a not dividing b.

The argument also handles beta's 3alpha corner even when its numerical
angle exceeds gamma: exclusion of a gamma tile there follows from the
exact irrational-angle inventory, not a numerical comparison.

The resulting counting argument is sound: k long edges each require
an unmarked interior endpoint, but there are only k-1 such junctions;
therefore two long edges share one. The theorem applies directly to W and beta. For theta the alpha corner
requires the additional argument below; simply asserting PR internal
would be invalid.

## W56 root orientation

In metric dx^2+2dy^2 the target is

    O=(0,0), A=(56,0), C=(46,20).

The corner cosines are

    cos(angle O)=23/27=cos(beta),
    cos(angle A)=1/3=cos(alpha+beta),
    cos(angle C)=17/81=cos(2alpha).

Thus the forced word c,c,a,a goes from C to A, with vertices

    (46,20), (49,14), (52,8), (54,4), (56,0).

The initial draft had the A,C corner roles interchanged; this was found
independently during the audit, communicated, and corrected in the
source before any exclusion was asserted.

## Independent exact construction of the two roots

For a directed boundary edge XY of length L, prescribe distances r,s
from the third vertex to X,Y. Put w=Y-X and Jw=(-2w_y,w_x). In the
counterclockwise target orientation the unique inward vertex is

    Q=X + ((r^2+L^2-s^2)/(2L^2))w + (20/L^2)Jw.

This uses the actual unit tile's doubled coordinate area 20. Both
assignments of the other two side lengths were enumerated independently
of the search generator. Exact half-plane containment, separating-axis
pair checks, and the exact corner inventory leave precisely these two
four-tile roots. Listed from A to C, their third vertices are

    (49,4), (47,8), V, (133/3,50/3),

where V has exactly two possibilities:

    V=(1289/27,266/27) or V=(142/3,32/3).

They agree with ../w-global-oct7/W56-boundary-roots.json. Both roots are
contained and have disjoint interiors. The existing integer-seam,
convex-angle and integral-component-area filters accept both initial
roots. No initial convex residual sector has at most one candidate
placement under the existing exact corner routine; branching remains.

This audit verifies the boundary reduction and its exact starting
geometry. It does not prove either completion or impossibility of W56,
and an incomplete continuation search cannot provide either conclusion.


## Theta extension and a consequence already implied by the earlier base bound

For theta corners (alpha,theta,theta), the only extra blocked-edge case
has P at the alpha apex and PR exterior. Then R is on the target
boundary. Q cannot be the alpha apex because its tile angle is beta,
and theta has no beta corner. If Q is blocked it is consequently a
marked straight point or a theta corner. The same complete bank along
QR forces an edge crossing R. But QR is a chord connecting distinct
outer sides, and continuation beyond R exits the convex target. This
is impossible. The exceptional case is therefore excluded, and the
adjacent-c theorem holds on all three theta sides too.

The following consequence is not claimed as new: it is also implied by
the earlier bound b(t-1)>=2v in ../../docs/theta-branch.md.
Let u=v-1 and t=2. On the base, writing (A,B,C) for whole
edge counts gives

    Auv+B(2v-1)+Cv^2=2(v-1)(2v-1),    C>=2.

Reduction modulo v forces B congruent to v-2 modulo v, hence B>=v-2.
The total remaining length is at most

    (2(v-1)-(v-2))*(2v-1)=v(2v-1)<2v^2=2c,

contradicting C>=2. Thus theta scale two is impossible for every
consecutive coprime parameter pair, including v=2.

More generally the theta base length is ubt, with b=v^2-u^2. Its
edge equation gives B congruent to ut modulo v. Subtracting the least
nonnegative possible B leaves at most v*b*floor(ut/v). Two c-edges
therefore require the rigorous necessary condition

    b*floor(ut/v) >= 2v.

This is an explicit residue reformulation of the pre-existing two-c-edge
base condition, not a claim of a previously unavailable base obstruction.
It is not asserted sufficient, and does not settle other theta scales
or arbitrary counts N.

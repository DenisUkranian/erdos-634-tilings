# Plan C: exact geometric energy, and the limit of fixed moment order

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

**The full problem is not solved. Neither 154 nor 4830 is decided here.**
The result below concerns certification of a specified collection of
placements. It does not show that a moment-based existence criterion must
accept any untileable target: all counterexamples constructed below have
targets that also admit genuine tilings.

## 1. A positive quantity that measures exactly the missing geometry

Let a target triangle T contain N congruent triangular placements T_i,
counting repetitions. Suppose the total tile area is the area of T, and
write A for the area of one tile. Set

    f(x) = sum_i 1_{T_i}(x) - 1_T(x).

Then

    integral f(x)^2 dx = 2 sum_{i<j} area(T_i intersection T_j) >= 0.    (1)

Indeed, expand the square. Containment gives
`1_{T_i} 1_T = 1_{T_i}`, while `area(T)=NA`; the diagonal
terms cancel. Thus the placements form a tiling if and only if (1) is
zero. Zero means pairwise intersection interiors are empty. Their union
has full area in T; since the union is closed, any uncovered point would
produce a relatively open uncovered set of positive area, a contradiction.

This identity accommodates reflections and T-junctions. It is exact but
does not yet remove the pairwise placement problem. Computing the right
side for a proposed finite placement is straightforward polygon clipping.
Minimizing it over unknown placements is another formulation of the hard
existence problem, not a classification of N.

For the frozen first-moment witness at 4830, even before accounting for
intersections between its nine different placements, its repeated stacks
give the rigorous lower bound

    integral f^2 / A >= sum_t n_t(n_t-1) = 11,157,206.

This quantifies how far that particular witness is from a tiling. It
does not prove that another, nonoverlapping placement cannot exist.

## 2. No fixed polynomial moment degree certifies placements

**Theorem.** For every integer d >= 0 and every nondegenerate triangle R,
there is a triangle T and a multiset of N congruent copies of R such that:

- every copy is contained in T;
- count, total area and each orientation population equal those of a
  genuine tiling of T;
- for every polynomial p of total degree at most d, the sum of the tile
  integrals of p equals the integral of p over T;
- for each unoriented edge direction separately, the signed arclength
  integrals of p over tile boundaries equal those over the target boundary;
- nevertheless the displayed multiset has positive-area holes and overlaps.

One can take `M=2^(d+1)` and `N=M^2=4^(d+1)`.

**Proof.** Put one vertex of R at 0 and write its other vertices as u,v.
The usual M by M triangular subdivision tiles `T=MR` by M^2 congruent
copies of R. In its first row are the M translates

    R_j = j u + R,     0 <= j < M.

For each j let `epsilon_j=(-1)^(s_2(j))`, where s_2(j) is the sum of
the binary digits of j. The identity

    sum_{j=0}^{M-1} epsilon_j exp(j t)
       = product_{k=0}^{d} (1-exp(2^k t))

has a zero of order d+1 at t=0. Differentiation therefore gives

    sum_j epsilon_j j^r = 0,       0 <= r <= d.                 (2)

Change the multiplicity of R_j from 1 to `1+epsilon_j`, leaving all
other tiles unchanged. Every new multiplicity is either 0 or 2.
Equation (2) at r=0 preserves the number of tiles. All altered tiles
have the same orientation, so every orientation population is preserved.
Containment is unchanged.

For any polynomial p of degree at most d, each quantity

    integral_{R_j} p(x) dx

is a polynomial in j of degree at most d. The same is true for the
signed arclength integral of p along any fixed directed edge of R_j.
Equation (2) annihilates their weighted sums. It follows that all the
specified moments still match the genuine tiling and hence T.

But M/2 original positive-area tiles have been removed and M/2 have been
duplicated. The other tiles have disjoint interiors in the original
subdivision, so these are genuine holes and identical overlapping pairs.
In fact the energy in (1) is exactly `M*A`. This proves the theorem.

**Corollary for each realizable nonclassical shape.** Start with any
genuine N_0-tile triangular tiling. Subdivide every tile into M^2
congruent triangles, then apply the preceding replacement inside one
original tile. The target is unchanged; after normalizing the new small
tile back to its original size, the target is scaled by M. Thus the same
fixed-degree failure occurs at count `N=N_0*4^(d+1)` within the original
target-shape family. Reflections, integer tile sides after normalization,
and all exact orientation populations are preserved.

This rules out a universal proof that *a displayed placement is a tiling*
using only any fixed finite order of these polynomial moments, even with
containment and exact orientation inventories. It does not rule out
additional genuine nonoverlap or seam-order constraints, nor a special
moment obstruction for the individual numbers 154 or 4830.

### A stronger version with distinct placements and quadratic count

The coincident copies in the preceding proof are not essential. For every
d, one can instead require **all placements to be distinct**, with

    N=(d+3)^2.

Put `M=d+1`, `L=M+2`, and start from the standard L^2 tiling of LR.
Select the M same-orientation row tiles `R_j=j*u+R`, `1<=j<=M`.
Let

    P(X)=product_{j=1}^M (X-j),
    epsilon=1/(2*4^M),
    Q(X)=P(X)+epsilon.

At each endpoint `j +/- 1/4`, every factor of P has absolute value at
least 1/4, so `|P|>=4^(-M)>epsilon`. The signs of Q therefore agree
with those of P at these endpoints, which have opposite signs.
There is a root r_j in each disjoint interval `(j-1/4,j+1/4)`.
Since Q has degree M, these are all its roots and each is simple.
None is an integer, because Q(j)=epsilon at every integer root of P
and there is no other integer in the corresponding interval.

Replace R_j by `r_j*u+R`. Newton identities show that the sums of
the r_j^k equal the sums of j^k for every `0<=k<M`: only the constant
coefficient of the monic polynomial was changed. Since `d=M-1`, the
same polynomial-translation argument preserves all area and signed
directional edge moments through degree d. Count and orientation
populations are unchanged. Containment follows from
`0<r_j` and `r_j+1<L`. All new placements are distinct from one another
and from the unchanged grid tiles.

There are nevertheless positive-area overlaps. In affine coordinates
with u=(1,0), v=(0,1), write `delta=r_j-j`, so
`0<|delta|<1/4`. The unchanged downward grid triangle D_j has vertices
`(j+1,0),(j,1),(j+1,1)`. When delta>0, the point

    (j+1/2+delta/4, 1/2+delta/4)

lies strictly inside both D_j and the translated R_j. When delta<0,
the point `(j+delta/2,1/2)` lies strictly inside the translated R_j
and the unchanged downward triangle D_{j-1}. Both downward triangles
are present since the selected row is buffered at each end.
Strict inequalities persist in a neighborhood, proving positive-area
overlap. Correct total area and containment then also force a hole of
positive area.

The root locations are exact real algebraic numbers; no approximate
root computation is used in the proof. The construction works after an
arbitrary nonsingular affine map, so it applies to every tile R.
Subdividing each tile of a genuine N_0-tile nonclassical tiling by L^2
and modifying one refined tile gives the stronger family corollary at
`N=N_0*(d+3)^2`. Thus adding a no-identical-placements constraint does
not rescue fixed-degree moment sufficiency. The first construction is
still useful because all its altered placements remain on the original
exact grid; the stronger distinct-placement construction need not have
integer lengths between arbitrary crossing points.

## 3. A growing moment hierarchy is complete, but is not a classification

For comparison, there is an explicit sufficient bound depending on N.
Suppose N positively counted, counterclockwise triangular placements and
a counterclockwise target have matching signed directional edge moments
for all polynomials of degree at most 2N. Then they form a tiling.

Here is a direct proof; no assertion about efficient search follows.
Fix an unoriented edge direction. Subtract the target boundary measure
from the sum of tile boundary measures in that direction, with signs
according to a fixed direction vector. The resulting signed measure mu
is supported on E <= N+1 segments: a nondegenerate triangle has at most
one edge in this direction.
If E=0, the measure is already zero and no argument is needed.

Let its supporting parallel lines be L_1,...,L_s. To isolate L_k,
multiply a test polynomial in tangential coordinate t by the product
of linear defining equations for the other s-1 lines. This product is
a nonzero constant on L_k and zero on every other supporting line.
Explicitly, in a normal coordinate n with `L_j={n=n_j}`, use
`product_{j!=k}(n-n_j)`, whose value on L_k is the nonzero scalar
`product_{j!=k}(n_k-n_j)`.
The restriction mu_k to L_k is a step-function density whose derivative
is an atomic measure with at most 2E_k distinct atoms, where E_k counts
the original segments on L_k.

Vanishing integrals of `1,t,...,t^(2E_k-2)` against mu_k imply that its
derivative has zero moments through degree 2E_k-1: the degree-zero
derivative moment vanishes automatically, and the others follow by
integration by parts. The Vandermonde matrix on its distinct atom
locations is invertible. Hence the derivative, and then the compactly
supported step function mu_k itself, vanish.

The isolation tests have total degree at most

    (s-1)+(2E_k-2) <= 2E-2 <= 2N,

because `E_k <= E-s+1`. Therefore every directional measure vanishes.
The complete boundary current of `sum_i 1_{T_i}-1_T` vanishes; its
distributional gradient is zero. A compactly supported function with
zero distributional gradient is zero almost everywhere. Positivity of
the tile counts then gives containment, nonoverlap and coverage, up to
boundaries, and the closed-triangle argument gives exact coverage.

Thus moment order can be made sufficient by allowing it to grow with
the proposed placement size. The fixed-degree counterexamples explain
why a uniform finite-order shortcut is unavailable. Both this hierarchy
and the previously established disk criterion verify finite data for a
fixed N; neither supplies the sought structural classification of all N.

## 4. Consequence for the research plan

The promising part of Plan C is a *new positive geometric inequality*
that bounds (1) from below uniformly over the remaining candidate
families, or a genuinely restrictive ordered-seam theorem. Merely adding
second, third, or any other fixed-order polynomial moments cannot give
general geometric sufficiency. No such uniform positive lower bound or
ordered-seam theorem has been proved here. This route therefore has a
clear bottleneck and should not receive an open-ended sequence of
moment-LP experiments without an additional structural idea.

The standard-library checker `check-plan-c.py` verifies the signed
replacement and every bivariate area/edge moment through d for
`0 <= d <= 6`, independently by exact polynomial integration, and checks
the numerical lower bound for the frozen 4830 witness. It also checks
exact rational root-bracketing signs and Newton power sums for the
distinct-placement construction for `0<=d<=20`. The proofs above,
not these finite checks, establish the statements for every d and the
2N sufficiency bound.

# Unit multiplier in one orientation of the 120-degree F4 family

**Denis Paliy, research with ChatGPT assistance.** Derived 2 October 2026 UTC (3 October in Kyiv).

Status: exact construction, with a separate internal symbolic review and an independently implemented unit-coordinate checker. This is not a complete solution of Erdős 634. External review and broader novelty have not been established.

Let positive integers a<b<c satisfy c²=a²+ab+b². Primitivity is unnecessary for the construction. Let R have sides (a,b,c), with angle 120 degrees opposite c. Then the triangle with sides

    (ac, b(2a+b), c(a+b))

has a tiling by exactly (2a+b)(a+b) congruent copies of R. Consequently every positive multiplier in this oriented F4 / Harries row III family is realizable.

## Exact construction

Work in the plane identified with the complex numbers and put rho=exp(i*pi/3), u=b+a*rho. Thus |u|=c. Define

    O=0, A=bc, B=cu, D=(a+b)c,
    C=b(2a+b)u/c,
    E=A+ab*u/c,
    F=A+bc*rho.

The target is triangle ODC. It is partitioned by segments AB, AE, EC, ED into the four closed regions (interiors disjoint)

    OAB, ADE, DCE, AECB.

The first triangle is cR; the second and third are aR. The quadrilateral AECB is a trapezoid, namely the bR triangle FAE with its (b-a)R corner triangle FBC removed.

Useful exact identities, all obtained using rho²=rho-1 and c²=a²+ab+b², are

    |OD|=(a+b)c, |OC|=b(2a+b), |DC|=ac,
    |OA|=bc, |AB|=ac, |OB|=c²,
    |AD|=ac, |AE|=ab, |DE|=a²,
    |DC|=ac, |CE|=ab, |DE|=a²,
    |FA|=bc, |FE|=b², |AE|=ab,
    B=F+((b-a)/b)(A-F),
    C=F+((b-a)/b)(E-F).

In particular B and C lie on FA and FE, respectively. Also O,B,C are collinear in that order, since b(2a+b)-c²=a(b-a)>0. The order O,A,D follows directly from 0<b<a+b.

For an explicit symbolic check of the partition, divide all coordinates by c and set S=c². The quadrilateral A,D,C,B is convex because A and B lie on the two sides of triangle ODC. In these normalized Eisenstein coordinates the signed cross products of its successive directed edges against the vector to E are

    cross(D-A,E-A)=a³b/S,
    cross(C-D,E-D)=a³b/S,
    cross(B-C,E-C)=a²b(b-a)/S,
    cross(A-B,E-B)=a²b²/S.

All four are strictly positive, so E lies strictly inside A,D,C,B. Joining E to A,D,C divides that quadrilateral into ADE, DCE, and AECB, without crossing or overlap. Adding OAB proves the claimed target partition. This symbolic check was independently derived by a second internal reviewer. `check_macro.py` additionally checks the geometry over exact rational coordinates on the test range below.

Subdivide each kR triangle into k² unit copies using the standard parallel grid. In the bR triangle FAE, the corner (b-a)R triangle FBC is exactly a triangular portion of this same grid: the homothety center is the common vertex F and b-a is an integer. Removing those (b-a)² cells therefore leaves a genuine tiling of the trapezoid, with no cut unit tile and no signed/overlapping pieces.

The count is

    c²+2a²+b²-(b-a)²
      =c²+a²+2ab
      =2a²+3ab+b²
      =(2a+b)(a+b).

Scaling the target by any positive integer m and quadratically subdividing every enlarged tile gives count (2a+b)(a+b)m².

For (a,b,c)=(3,5,7), the macro counts are 49,9,9,21, exactly the four direction groups in Harries's archived 88-tile certificate. That certificate motivated this symbolic extension. The construction should be attributed as a generalization of Harries's concrete 88-tiling, not as an independently discovered 88-tiling.

## Audit against the source

Harries, [progress634.tex](https://github.com/jphme/math-problems/blob/67838578b5bd26aa66034fa46da96141be75de0e/progress634/progress634.tex), v0.5 (2026-08-28), describes row III at multiplier one as a two-grid staircase / half-parallelogram problem and presents 88 as the first worked instance. The displayed general construction above was not found in that text. His existing bound gives m≥3R(a,b), with R=ceil(a/b)+ceil(b/a). The pinned source commit is `67838578b5bd26aa66034fa46da96141be75de0e`. The geometry of his specific 88-tiling is credited as the starting point; no third-party source code or coordinate certificate is redistributed by this package.

Bonfioli's [source](https://github.com/ElVec1o/erdos_634_proof/tree/4bb61193bafa4471f7ba3a35324ae0f70bd2177c), inspected at commit `4bb61193bafa4471f7ba3a35324ae0f70bd2177c`, does not supply this all-multiplier F4 theorem either. Broader novelty is not certified.

## Why a>b is not automatically covered

The same formulas still satisfy the side and area identities, but b-a is then negative, so the corner-removal argument changes. Triangle BFC now lies inside OAB, but it is reflected at the beta corner: its adjacent a,c sides are interchanged compared with the quadratic grid of OAB. Thus it cannot simply be deleted from that standard grid.

A sufficient missing construction for this orientation is a tiling of quadrilateral OAFC, equal to OAB minus BFC, by

    c²-(a-b)²=3ab

unit copies. The other three pieces ADE, DCE, FAE are standard a²,a²,b² grids. This is a precise quadrilateral tiling problem, not a proved extension.

## Verification

From this directory, `python run_checks.py` checks every primitive norm triple with 1≤a≤300 and a<b≤500 (80 triples), verifying the asserted side lengths, homothety relations, target containment, pairwise macro separation, and count identity in exact rational arithmetic. The symbolic identities and standard grid construction above provide the proof beyond this finite check.

The same command independently checks complete expanded unit-coordinate certificates for (3,5,7) at multipliers 1 and 2, and (5,16,19) at multiplier 1. It checks every tile pair by exact bounding intervals followed, when needed, by rational convex clipping. Total pair counts are 3,828, 61,776 and 148,785. It also rejects duplicated or missing tiles, moved vertices, altered targets and multipliers, and use of the unproved reversed orientation. See [VERIFIED_RESULTS.json](VERIFIED_RESULTS.json).

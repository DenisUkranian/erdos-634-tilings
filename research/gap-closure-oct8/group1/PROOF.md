# Every scale at least v for the adjacent W and beta families

8 October 2026. Denis Paliy, research with ChatGPT assistance.
This is an internally verified constructive theorem, not a complete
classification of Erdős problem 634 and not a priority claim.

## Theorem

For every integer u>=2 put

    v=u+1,  a=uv,  b=2u+1,  c=v²,
    Q=u²+4u+2=2v²-u²,  P=2u²+6u+3=3v²-u².

For **every integer M>=v**, the following targets have tilings by the
single fixed primitive tile (a,b,c):

| Target sides | Tile count |
|---|---:|
| M(v³,uQ,vb) | QM² |
| M(v³,v³,uP) | PM² |

Thus the entire sufficient scale tail begins at v=u+1 for every adjacent
parameter pair, uniformly in u. No impossibility is asserted for M<v;
the theorem is not an exact necessary-and-sufficient scale criterion.

The W target is not similar to the tile. Its sides satisfy
vb<v³<uQ, because uQ-v³=u²-u-1>0. The tile sides satisfy b<uv<v².
Their smallest-to-middle ratios are respectively b/v² and b/(uv), which
differ. The beta target is isosceles and the primitive tile is scalene.

## 1. A finite interval of scales closes the infinite quantifier

The existing [six-block cap theorem](../../w-beta-caps/PROOF.md) extends
any W or beta tiling from scale T to T+u whenever T>=v-u. Here v-u=1.
Therefore it suffices to construct one seed in every residue modulo u:

    M=v+t,  0<=t<=u-1.

The scale t=0 is Beeson's existing triquadratic seed. The scale t=1 was
constructed in the previous
[adjacent-parameter theorem](../../universal-closure-oct8/group1-adjacent/PROOF.md).
For u=2 these two seeds already cover all residues. The new work below
constructs **every remaining seed** 2<=t<=u-1 for arbitrary u>=3.

For any prescribed M>=v, choose

    t=(M-v) mod u,  0<=t<u,
    k=(M-v-t)/u >=0.

Start from the corresponding seed v+t and attach k ordinary +u caps.
Every attachment satisfies the cutoff T>=1. This proves the all-M
quantifier without a finite-extrapolation argument.

## 2. Exact oblique coordinates

Let D=4v²-u² and z=(-u+sqrt(-D))/(2v). Use the oblique basis vE,vF,
where E=z^(-2), F=z. The physical squared norm of a coordinate vector is

    G(x,y)=v²(x²+y²)+[u(3v²-u²)/v]xy.

The two coordinate triangles

    A: (0,0),(u,0),(0,v),
    B: (0,0),(v,0),(0,u)

both have physical sides a,b,c. Their half-turns are also permitted.
Ordinary triangular grids and axis-parallel rectangles in these two
orientations give all the unit tiles used below.

Fix 2<=t<=u-1 and m=v+t. In this basis, set

    O=(u m v³/b, -u² m v²/b), X=(0,0),
    A=(-uvm,u²m), C=(-uvm,v²m), V=(-u²m,uvm),
    U=(-u²m+t v²,uv²), R=(-u²v+b(t-1),uv²),
    S=(ub-u²t,uvt), Q0=(ub,0),
    P0=Q0+(ut v³/b,-u²t v²/b),
    R0=S+(tu v²/b,-tu²v/b),
    T0=U+((u-t)v³/b,-(u-t)uv²/b).

The target is triangle O,A,C. Four ordinary grid regions are:

| Polygon | Outer grid scale | Removed corner scale |
|---|---:|---:|
| O,X,Q0,P0 | um | ut |
| P0,Q0,S,R0 | vt | t |
| R0,R,U,T0 | b-t | u-t |
| T0,V,C | m | 0 |

The first and third have horizontal c-bases; the second and fourth have
horizontal a-bases in physical coordinates. Each removed corner is an
integral homothetic grid subtriangle. All retained regions are positive:
their scale differences are uv,ut,v,m, respectively.

The four macros leave the eight-vertex polygon

    X,A,C,V,U,R,S,Q0.

Their metric identities, containment/disjointness together with the
remaining partition, and all counts are proved symbolically by the
independent checker described below.

## 3. The residual polygon has a complete horizontal-layer dissection

The complete elementary proof is
[`../group1-helper/ADJACENT_ALL_SCALES.md`](../group1-helper/ADJACENT_ALL_SCALES.md).
Its ingredients are summarized here to make the logical dependency clear.

Cut at y=uvt and y=uv². The lower trapezoid splits into t layers of
height uv. Layer j has a B-grid triangle of scale v at the left, an
A-grid triangle of scale u at the right, and a rectangle of width

    uv+bj = ju+(u+j)v.

Use j columns of A rectangles and u+j columns of B rectangles. Their
height uv is divisible by both u and v, so every column is an integral
grid. The lower count is bt(2u+t).

The central strip consists of v-t parallelograms of height uv and width
b(u+t). Each has two B-grid triangles of scale v and a rectangle of width

    b(u+t)-v² = (t-1)u+(u+t-1)v.

The same column construction applies. The central count is
2b(u+t)(v-t).

Translate the upper pentagon by -V. Above y=0 it is an A-grid triangle
of scale m. Its first negative layer consists of an A rectangle and a
B-grid triangle of scale v. Its second layer is an ordinary complete
parallelogram with one B-grid corner of scale t removed from a B-grid
triangle of scale v. This is a positive annulus because t<v. Every
subsequent layer is a full parallelogram. The mixed rectangle widths are

    bm-v² = tu+(u+t)v.

The corner removal matches the target's left kink exactly:

    v²-bm+vt=-um,  uv+ut=um,
    uv<um<2uv.

Thus it removes only the portion outside the target, without a hidden
overlap or a negative-weight region. The upper count is 2bmt.

The residual count is consequently

    bt(2u+t)+2b(u+t)(v-t)+2bmt
      = b(2uv+4vt+t²).

Adding the four outside grid counts gives exactly Qm².

## 4. Independent universal verification

`check_all_adjacent_symbolic.py` uses elementary exact polynomial
arithmetic in two variables p,q, with

    u=p+q+3,  t=q+2,  p,q>=0.

This substitution is exactly the entire parameter range
u>=3, 2<=t<=u-1. The checker verifies:

* Primitive A/B tile metric identities and positive-definite Gram form.
* Every outside macro side length and annular homothety identity.
* The generic horizontal cell and expanding lower layer, including their
  positive width representations by u and v.
* Convexity and nonnegative area of 13 fixed macroregions covering the
  whole W target; the final zero-height region is omitted when t=2.
* Exact **positioned** boundary equality with the W triangle, retaining
  supporting lines and all polynomial endpoints.
* The complete area and tile-count identities.

All geometric sign checks have nonnegative coefficients in p,q. Thus they
hold throughout the parameter cone, rather than just for tested values.
The boundary event list cancels identically in Z[p,q]. On each supporting
line this implies zero signed interval coverage. Hence the difference
between the sum of macroregion indicators and the target indicator has
zero distributional boundary and compact support, so it is zero. Because
all region weights are nonnegative, the coverage multiplicity is exactly
one inside and zero outside. This proves a genuine dissection without
assuming absence of overlap beforehand.

The symbolic report is `all_adjacent_symbolic_verified.json`.
`all_adjacent_formula.py` independently generates every unit tile without
a solver. The frozen independent checker
[`verify_general_geometry.py`](../../universal-closure-oct8/group1/verify_general_geometry.py)
checks its exported integer-coordinate certificates for congruence,
containment, area equality and pairwise disjoint interiors.

The solver-free formula passed these full unit checks:

| u | t | Count | Exact pair checks |
|---:|---:|---:|---:|
| 3 | 2 | 828 | 342,378 |
| 4 | 2 | 1666 | 1,386,945 |
| 4 | 3 | 2176 | 2,366,400 |
| 5 | 4 | 4700 | 11,042,650 |

These are implementation controls, separate from the universal polynomial
proof. The larger certificate checks over eleven million triangle pairs;
it does not replace any missing quantifier in the theorem.

## 5. Beta transfer, attribution and limits

The existing W-to-beta transfer attaches an ordinary tile triangle at
integer scale vM. It adds v²M² unit tiles to the W count QM², yielding
PM² and target sides M(v³,v³,uP). Thus the same all-M statement follows
for the fixed-tile beta family.

Beeson's scale-v seed, the previous scale-v+1 construction and the earlier
+u cap are inputs. The new theorem supplies every intervening seed residue
through the uniform horizontal-layer partition. Individual counts may
already have other known realizations; no claim of a new global count is
made merely from a new fixed-tile construction.

The omitted scales M<v are not classified here. Parameters with v-u>1
are also outside this theorem. The all-primes candidate and its disputed
geometric inductions are not premises.

Reproduction from the repository root:

```sh
python research/gap-closure-oct8/group1/check_all_adjacent_symbolic.py
python research/gap-closure-oct8/group1/all_adjacent_formula.py --u 4 --t 3 --output /tmp/W2176.json
python research/universal-closure-oct8/group1/verify_general_geometry.py /tmp/W2176.json
```

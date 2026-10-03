# Flexible corner constructions for reversed F4 and F2/F3

Research note, 3 October 2026. This is a sufficient construction theorem, not a complete solution of Erdős 634. It extends the reflected-corner shave in [PROOF.md](PROOF.md) by allowing the width of its low rectangle to vary independently of the target multiplier. The proof below includes the exact partition, transfer to three target families, and the arithmetic criterion for this construction.

Let positive integers a>b satisfy c²=a²+ab+b², and put t=a−b. Suppose positive integers m,k satisfy

    kc ≥ mt,
    rₖ = mbc−a²k ∈ <a,b> = {Aa+Bb: A,B are nonnegative integers}.

Then there are tilings by the (a,b,c) tile of all three triangles:

| Family | Target sides | Number of unit tiles |
| --- | --- | --- |
| reversed F4 | m(ac, b(2a+b), c(a+b)) | (2a+b)(a+b)m² |
| F2 | m(a(a+2b), b(2a+b), c²) | (a+2b)(2a+b)m² |
| F3 | m(c², c(a+2b), 3b(a+b)) | 3(a+b)(a+2b)m² |

In particular, **if a>b and 3c≥4a, every multiplier m≥2 is constructible in all three branches**. This is equivalent to

    1 < a/b ≤ (9+sqrt(333))/14 ≈ 1.9463062565.

The preceding narrower result b<a≤4b/3 is included. No assertion about primitive multiplier one follows.

## Exact reflected-corner partition with a free rectangle width

Use complex coordinates x+yρ, with ρ=exp(iπ/3), and let z=(a+bρ)/c, so |z|=1. The following coordinates already include the target multiplier m:

    F=0, O=mat, A=mc², B=mac z, C=mtc z,
    E=akc, D=E+C,
    U=C+a²kz, V=E+a(mc−ak)z.

The triangle FAB is mcR, where R has sides (a,b,c). The triangle FOC is mtR, reflected at the common β corner F. Their difference is the quadrilateral Q=OABC.

Since rₖ≥0, we have a²k≤mbc<mac and therefore ak<mc. The separate positivity condition mc−ak>0 is automatic. The rectangle-fit condition kc≥mt says that E lies on OA. The identities

    V=A+((mc−ak)/(mc))(B−A),
    B−U=rₖ z,
    V−D=rₖ z,
    D−E=mtc z,
    U−C=a²kz

place V on AB, U on CB, and D on EV. They give the interior-disjoint partition

    OEDC: parallelogram FEDC with its corner triangle FOC deleted;
    CDU: an akR triangle;
    EAV: an (mc−ak)R triangle;
    UDVB: a parallelogram with side lengths abk and rₖ and angles 60°,120°.

Indeed,

    D−U=ak(c−az),  |c−az|=b,
    Re(conjugate(z)(c−az))=b/2.

The parallelogram FEDC is a kc-by-mt array of two-tile parallelograms with adjacent sides a,c and included angle β. Because kc≥mt, its F-corner triangle FOC is exactly an mt-grid corner; deleting it removes whole unit tiles. The retained region therefore has 2kcm t−m²t² tiles. CDU and EAV have (ak)² and (mc−ak)² tiles in their ordinary quadratic grids.

Write rₖ=Aa+Bb. Split the rₖ side of UDVB into A intervals of length a and B intervals of length b. Its other side abk is divisible by both a and b. Pair an a-width strip with ak steps of length b, and a b-width strip with bk steps of length a. Every resulting small parallelogram splits into two R triangles along its long diagonal. The total in UDVB is 2k rₖ. Thus Q has

    2kcm t−m²t² + (ak)² + (mc−ak)² + 2k(mbc−a²k)
      = m²(c²−t²)
      = 3abm²

unit tiles.

Equality is allowed in both hypotheses. If kc=mt, then O=E and the low quadrilateral is a triangle; the same grid deletion remains valid. If rₖ=0, then U=B and D=V, and the zero-area high parallelogram is omitted. The two ordinary grid triangles always have strictly positive integer scales. The uniform family proved below has both fit and width strict.

Taking k=m recovers the earlier sufficient condition m(bc−a²)∈<a,b>. Allowing k to differ from m is essential: for (a,b,c)=(5,3,7), bc−a²=−4, yet k=1 works at both m=2 and m=3.

## Identification with the missing F4 quadrilateral

Put u=b+aρ. In the [existing F4 notation](../group2-f4/PROOF.md) let

    O₀=0, A₀=bc, B₀=cu, F₀=bc(1+ρ),
    C₀=b(2a+b)u/c,
    D₀=(a+b)c, E₀=bc+ab u/c.

The isometry

    w ↦ m c u − (u/c)w

maps the canonical scaled vertices (O,A,B,C) to (mC₀,mO₀,mA₀,mF₀), respectively. For the third vertex the identity used is

    (b+aρ)(a+bρ)=c²ρ.

Hence it tiles exactly the quadrilateral O₀A₀F₀C₀ at multiplier m. Attach the standard triangles A₀D₀E₀, D₀C₀E₀, F₀A₀E₀ of scales ma,ma,mb. For a>b the order along the collinear edge is C₀,F₀,E₀, so the successive unions have boundaries O₀A₀E₀C₀, O₀D₀E₀C₀, O₀D₀C₀. All pieces have disjoint interiors. The count becomes

    (3ab+2a²+b²)m²=(2a+b)(a+b)m².

## The F2 reflection bridge

The corner construction also supplies F2 at the same multiplier. For this paragraph write Z=a+bρ, S=c², h=a+2b, and k=2a+b. All displayed coordinates are first unscaled and then multiplied by m. Set

    X=0, Y=S, I=aZ, J=Z², T=(ah/S)Z².

The target XYT has sides S, ah, bk. The two triangles XYI and XIJ are cR triangles. The point J lies strictly between X and T since ah−S=b(a−b)>0. The incenter I has the positive barycentric expression

    I=(b/h)X+(a/k)Y+(S/(hk))T.

Thus the two triangles have disjoint interiors within the target and leave the quadrilateral whose vertices are Y,I,J,T (listed clockwise).

This quadrilateral is isometric to the canonical corner remainder. Reflect across the line joining canonical A=S and B=aZ, using

    R(w)=S+v² conjugate(w−S),
    v²=(−(a+b)+aρ)²/S=(bk−ahρ)/S.

The reflection fixes canonical A,B and sends canonical C=tZ to J=Z² and canonical O=at to T=(ah/S)Z². For the first identity, conjugate(C−S)=−bh−btρ; multiplying by v² gives (−bh,bk) in Eisenstein coordinates. For the second,

    S²−b²k²=(S−bk)(S+bk)=a(a−b)(a+b)h=ah(a²−b²).

At multiplier m the reflection is w↦mS+v² conjugate(w−mS). The already constructed corner grid therefore fills the residual quadrilateral. The total is

    (2c²+3ab)m²=(a+2b)(2a+b)m²=hk m².

This explicit bridge is sufficient whenever the free-k criterion holds; it makes no assertion that an arbitrary F2 tiling must admit this decomposition.

## The F3 attachment

In the preceding notation put K=(h/S)Z³. Then

    K−T=(h/k)(T−Y),
    |XT|=ah, |TK|=bh, |XK|=ch.

For the vector identity, use conjugate(Z²)=ah−bkρ and Z² conjugate(Z²)=S². Thus T lies between Y and K, and the triangle XTK is hR. Adding its standard grid to XYT gives the triangle XYK, with sides

    S, ch, 3b(a+b).

At multiplier m the attached grid has h²m² tiles. The total is

    (hk+h²)m²=3(a+b)(a+2b)m².

This is the standard F2-to-F3 (Harries V-to-II) one-patch transfer, included here with explicit coordinates. Attaching along the other appropriate F2 side gives its a↔b counterpart. Since the F2 target is unchanged up to reflection when a,b are interchanged, both F3 orientations are obtained from the same balanced F2 result.

## Exact arithmetic criterion for the free-k construction

Assume gcd(a,b)=1. For a fixed positive integer k,

    mbc−a²k=Aa+Bb

has a nonnegative solution if and only if there is an integer ℓ with

    ak/b ≤ ℓ ≤ mc/a.

Indeed, reduction modulo b forces A=ℓb−ak, and then B=mc−aℓ. Consequently, set

    k₀ = ceil(m(a−b)/c),   L = floor(mc/a).

There is an admissible free-k construction **if and only if**

    a k₀ ≤ b L.

The lower rectangle-fit bound forces k≥k₀, and the arithmetic upper bound only becomes harder as k increases. Thus k₀ is optimal. This equivalence classifies this explicit construction, not arbitrary tilings of Q or the target triangles.

For m=1, k₀=1 because 0<a−b<c. However a/b>1 forces ℓ≥2, while c/a<sqrt(3)<2. Therefore no primitive norm triple admits multiplier one by this construction. Geometrically, any possible k would satisfy k< c/a<2, hence k=1; increasing k cannot avoid this barrier.

For nonprimitive a,b the integer-ℓ characterization is not asserted. The generator checks membership in <a,b> directly by modular arithmetic and tries each integer k in the finite interval

    ceil(m(a−b)/c) ≤ k ≤ floor(mbc/a²).

This interval and semigroup test are necessary and sufficient for the stated free-k construction for arbitrary positive integer norm triples. Nonprimitive triples can pass at m=1; for example (16,14,26) does.

For comparison, fixing k=m in the primitive case gives the former criterion

    ma/b ≤ ℓ ≤ mc/a.

## Every multiplier at least two when 3c≥4a

Suppose a>b and 3c≥4a. This implies a<2b: if a≥2b, then c²≤7a²/4, which gives 3c<4a. Two valid (m,k) seeds are

    (m,k)=(2,1):  rₖ=(2b−a)a+2(c−a)b,
    (m,k)=(3,2):  rₖ=(4b−2a)a+(3c−4a)b.

All displayed coefficients are nonnegative, and both widths are positive. Their rectangle-fit inequalities follow from c>a and a<2b:

    c>2(a−b),   2c>3(a−b).

Every m≥2 can be written as m=2u+3v with u,v nonnegative integers. Set k=u+2v. Both the rectangle-fit inequality and the semigroup witness add linearly:

    kc−mt = u[c−2t] + v[2c−3t] > 0,
    mbc−a²k = u(2bc−a²) + v(3bc−2a²) ∈ <a,b>.

The single free-k partition therefore constructs Q at multiplier m. No operation gluing differently sized Q regions is needed. One explicit choice is k=ceil(m/2), using v=0 for even m and v=1 for odd m. The F4, F2, and F3 transfers then complete the claimed tilings. Primitivity is unnecessary for this sufficient theorem.

For primitive triples, this is the exact domain in which the free-k method supplies **every** m≥2. At m=2 it succeeds exactly when a≤2b: the k=1, ℓ=2 witness works throughout that range; if a>2b, then floor(2c/a)≤2 but ceil(ak/b)≥3 for every k≥1. At m=3 it succeeds exactly when 3c≥4a. Sufficiency was just shown. If 3c<4a, then a>9b/5 (substitute a/b≤9/5 into 9c²−16a²=−7a²+9ab+9b²). Hence 3t>4a/3>c, forcing k≥2. But then ak/b>18/5>3 while floor(3c/a)≤3, so the primitive arithmetic criterion fails. This limitation concerns the method alone.

## Expanded verification

The original fixed-width `construct_reversed.py` implements the canonical partition, both parallelogram grids, the exact isometry, and the three additional F4 grids. `verify_reversed.py` is the existing independent unit-certificate checker from `research/group2-f4/verify.py`, with only the theorem-domain comparison changed from a<b to a>b. Its geometric checks do not import the constructor.

For (8,7,13), multiplier 2 gives 1,380 unit triangles: all 951,510 tile pairs were checked, with 3,212 requiring rational polygon clipping. Multiplier 3 gives 3,105 unit triangles: all 4,818,960 tile pairs were checked, with 7,446 requiring clipping. Both certificates pass exact congruence, target containment, pairwise interior disjointness, and total-area checks.

The symbolic partition and the semigroup expressions provide the general proof; these two expanded checks are examples and implementation checks, not the basis for extrapolation.

The frozen unit certificates are `certificates/f4_reversed_8_7_13_m2.json` and `certificates/f4_reversed_8_7_13_m3.json`; `check_balanced_f4.py` regenerates and verifies them.

The F2 reflection is independently expanded at (8,7,13), m=2 into 2,024 unit triangles. `verify_f2.py` checks the same exact unit geometry with the F2 target/count formulas. `check_target_bridges.py` separately checks the explicit F2/F3 macro partitions on every primitive norm triple with 1≤b<a≤400, at multipliers 1 and 2: 70 triples, 140 instances. Its m=1 checks assert only the partition and reflected Q identity, not tileability of Q.

The separate `construct_free_k.py` implements the flexible width and chooses an admissible k automatically, or accepts an explicit `--k`. It leaves the original generator and its regression certificates unchanged. `check_free_k.py` regenerates and independently verifies full F4 unit certificates for (5,3,7) at m=2 and m=3: 416 and 936 triangles. Both pass even though the original fixed-width condition fails at every positive multiplier. A further 572-tile F2 unit check verifies the free-width reflection implementation. The campaign also checks the optimized primitive criterion, the two universal seeds, multiplier-one rejection within this method, and the prescribed degenerate cases. Results are recorded in `free_k_verification.json`.

The independent symbolic and exact-coordinate audit is recorded in `FREE_K_AUDIT.md`. These internal checks do not constitute external peer review or a complete classification of Erdős 634.

# Parity, primitive scales, and constructive spectra for triangle tilings

**Denis Paliy — research with ChatGPT assistance — 30 September 2026**

## Status and attribution

This note proves necessary scale restrictions, constructive sufficient bounds, and an exact example. It does **not** classify all admissible integers in Erdős problem 634. The arguments have been checked within this project, not by an external referee or a proof assistant. No priority claim is made.

The signed-direction framework is due to the existing source corpus, including Vico Bonfioli's manuscript [B]. In particular, the isosceles and F1 necessary spectra below already appear in its theorem labelled `thm:spectrum`; the half-difference proof here is a shorter derivation, not a claim to have discovered those spectra first. Zhang's trapezoid construction [Z] supplies the geometric building blocks. We replace its general Frobenius sufficient bound by an exact residue calculation for the particular base lengths used in that construction. The source comparison is to the explicitly inspected version 4, not a claim about every subsequent revision.

All tilings below are finite, their interiors are disjoint, reflections are permitted, and edge-to-edge incidence is **not** assumed. T-junctions are permitted throughout. The universal proofs do not depend on our earlier N=105 certificates or the candidate prime-classification manuscript.

## 1. Two boundary characters and one parity constraint

Let a nondegenerate tile have integer sides a,b,c, corresponding angles alpha,beta,gamma, and gamma equal to 60 or 120 degrees. Assume gcd(a,b,c)=1 and alpha/pi is irrational. Put one external target side horizontally.

Every directed tile edge then has direction

    theta = n alpha + j pi/3,   n in Z, j in Z/6Z.

Indeed the graph connecting tiles which share a positive-length boundary segment is connected: connect two interior points by a path through the target avoiding the finitely many vertices. Across an edge adjacency, all new directions differ by integer combinations of tile angles. For either value of gamma, these are integer combinations of alpha and pi/3. Irrationality makes n and j unique modulo the stated conventions.

Define

    f(theta)=(-1)^j,            g(theta)=(-1)^(n+j).

Both change sign under theta -> theta+pi. For a directed polygonal boundary let its f-value be the sum of edge length times f(direction), and define its g-value similarly. These values add under dissection: split longer edges at T-junctions and cancel the oppositely oriented internal segments. No integer subdivision lengths are needed in this cancellation.

A rotation multiplies a reference tile's value by a sign. A reflection also multiplies it by a sign: the direction is negated and the boundary traversal is reversed. Thus, after dividing the target's two values by the nonzero reference tile values, a tiling by N pieces gives integers U,V such that

    U ≡ V ≡ N (mod 2).                                      (1)

Consequently (U+V)/2 and (U−V)/2 are integers. This parity observation is the key simplification.

A reference tile is traversed counterclockwise with its c-edge in direction 0. For gamma=120 degrees its a,b directions are alpha+2pi/3 and alpha+pi, giving values

    X=c+a−b,      Y=c+b−a,       XY=3ab.                     (2)

For gamma=60 degrees its a,b directions are alpha+pi/3 and alpha+pi, giving values −A,B where

    A=a+b−c,      B=a+b+c,       AB=3ab.                     (3)

The length norm is c²=a²+ab+b² in (2), and c²=a²−ab+b² in (3). Each norm equation and primitivity imply pairwise coprimality of a,b,c: a prime dividing two would divide the third.

## 2. Equilateral targets: the primitive side is ab

**Theorem 1.** For an equilateral target of side S tiled by the specified primitive tile, in either angle case,

    S=ab m,       N=ab m²,       m a positive integer.        (4)

**Proof.** The external side is a concatenation of whole integer-length tile edges, so S is an integer. The three counterclockwise target directions are 0,2pi/3,4pi/3. Both target values are 3S.

For gamma=120 degrees, U=3S/X and V=3S/Y. By (1) and (2),

    (U+V)/2 = 3S(X+Y)/(2XY) = Sc/(ab) is an integer.

Since gcd(c,ab)=1, ab divides S.

For gamma=60 degrees use u=−U=3S/A and v=V=3S/B. Negating U does not change its parity. Equations (1),(3) give

    (u+v)/2 = S(a+b)/(ab) is an integer.

Since gcd(a+b,ab)=1, ab divides S again. In either case the area ratio is N=S²/(ab), proving (4). □

**Exact scope.** This is necessary for a geometric tiling. Conversely, S=ab m passes both of these invariant tests: their values are mX,mY or −mB,mA. Reducing the norm equation modulo 2 gives c≡a+b+ab, so these values have the parity of ab m². Thus (4) is precisely the arithmetic spectrum of these two tests, **not by itself a tiling-existence theorem**.

This proves the divisibility assertion stated as Conjecture 1 in [Z, v4], and the divisibility component of its 60-degree extension. It does not prove its conjectured sharp lower cutoff.

**Example.** For (a,b,c)=(5,16,19), X=8,Y=30. Integrality alone allows S=40h. But then U=15h and V=4h must have the same parity, forcing h even. Hence S is a multiple of 80, not merely 40. The argument does not assume that a and b are squarefree.

## 3. Two non-equilateral 120-degree spectra, by half-differences

Here c²=a²+ab+b². The primitive side triples are (a,c,a+b) for F1 and (c,c,a+2b) for the isosceles target with base angle alpha. Their scale lambda is an integer, by whole boundary lengths and Bezout.

For the second triple, gcd(c,a+2b)=1: a common prime would divide 3b², and 3 cannot divide c in a primitive 120-degree triple. To see the latter, c divisible by 3 implies a=b modulo 3; writing a=b+3h makes c²=3b² modulo 9, forcing 3|b, contrary to primitivity.

For F1, a counterclockwise boundary has sides lambda(a+b),lambda a,lambda c at directions 0,2pi/3,pi+alpha. Its normalized values are

    U=lambda(2a+b−c)/X = lambda(c−a)/b,
    V=lambda(2a+b+c)/Y = lambda(c+a)/b.

Therefore

    (V−U)/2=lambda a/b is an integer.

Coprimality forces b|lambda. Thus every such tiling has

    N=b(a+b)m²,       m>=1.                                (5)

For the isosceles target, the directed sides have directions 0,pi−alpha,pi+alpha. The normalized values are

    U=lambda(a+2b−2c)/X = lambda(c−a−b)/b,
    V=lambda(a+2b+2c)/Y = lambda(c+a+b)/b.

Their half-difference is lambda(a+b)/b, forcing b|lambda. Hence

    N=b(a+2b)m²,      m>=1.                                (6)

All displayed identities follow on multiplying out and substituting the norm equation. At lambda=bm, parity (1) follows from c≡a+b+ab modulo 2, so (5),(6) are also exact invariant-admissible spectra. As noted above, these two spectra are already in [B]; this proof removes the separate prime-adic and exceptional 2-adic analysis.

## 4. An exact replacement for a coarse Frobenius cutoff

Interchange a,b if necessary so that a>b>1. Write

    a=qb+r,     q>=1, 1<=r<b,     L=ab.

An ideal trapezoid will mean an isosceles trapezoid with acute angles 60 degrees, **shorter base x, legs h, and longer base x+h**. This explicit convention avoids ambiguity between the base and leg notation in [Z].

For a 120-degree tile, the basic ideal trapezoid has shorter base

    K=a²+b²,

legs L and longer base c²=K+L. It is partitioned into three original-tile triangles at integer scales a,b,c. For a 60-degree tile, K=c²=a²+b²−L and the same scales give the basic trapezoid with longer base a²+b².

A parallelogram with angles 60/120 degrees, one side L and the other side R=na*a+nb*b, na,nb nonnegative integers, is tiled by the original tile. Split the R side into na strips of width a and nb strips of width b; in each, split the L side respectively into lengths b or a. Each resulting cell is cut by the appropriate diagonal into two original tiles. There are exactly 2R tiles. The correct diagonal differs between the 60- and 120-degree cases.

**Residue lemma.** Define

    k0=q+2  (120 degrees),      k0=q+1  (60 degrees).

For an integer k>=0, the number kL−K is a nonnegative combination of a,b **if and only if k>=k0**.

For 120 degrees, a coefficient x of a must satisfy x≡−a≡b−r modulo b, so its minimum is b−r. The corresponding coefficient of b is

    y=a(k−q−1)−b.

If k<=q+1 then y<0; increasing x by b only decreases y by a. If k>=q+2 then y>=a−b>0. Thus

    kab−a²−b² = a(b−r)+b[a(k−q−1)−b]                       (7)

is the required explicit representation. For 60 degrees replace k by k+1 in the same calculation. □

Consequently an ideal trapezoid of shorter base kL and legs nL is tiled whenever k>=k0 and n>=1. Cut it into n bands with legs L and shorter bases kL,(k+1)L,...,(k+n−1)L. Each band is its basic three-triangle trapezoid plus the parallelogram from (7). This is a sufficient construction for that shape; no necessity for arbitrary trapezoid tilings is asserted.

## 5. A uniform constructive bound

**Theorem 2.** With a>b>1 as above, every equilateral triangle of side ab m is tileable when

    m >= M* = 3(floor(a/b)+2)      for a 120-degree tile;
    m >= M* = 3(floor(a/b)+1)      for a 60-degree tile.       (8)

Together with Theorem 1, this determines the equilateral fixed-tile spectrum outside the finite interval 1<=m<M*.

**Proof.** Take integers r0,s0,t0>=k0 with r0+s0+t0=m. In coordinates (x,y) representing the physical point (x+y/2,sqrt(3)y/2), put

    A=(0,0), B=(mL,0), C=(0,mL),
    D=(s0 L,t0 L), E=((s0+r0)L,t0 L),
    F=(0,(s0+t0)L), G=(s0 L,0).

The ideal trapezoids GBED, AGDF and ECFD have respective (shorter base,leg) pairs (r0 L,t0 L), (t0 L,s0 L), (s0 L,r0 L). They partition ABC with disjoint interiors, as follows directly from these coordinates. The preceding band construction tiles each. One can choose r0=s0=k0 and t0=m−2k0 for every m>=3k0. □

For a 120-degree tile, attaching one bm-fold original triangle to a side of this equilateral target gives the F1 target with sides (abm,bcm,b(a+b)m) and count b(a+b)m². Attaching a second bm-fold original triangle to an adjacent side, with its 120-degree corner at the opposite equilateral endpoint, gives the isosceles target (bcm,bcm,b(a+2b)m) and count b(a+2b)m². The straightening angles are 60+120=180 degrees. These are the transfers in [Z, Propositions 8–9]. They give existence for (5),(6) at every m>=M*; smaller m remain separate questions.

The bound (8) improves or equals the displayed Frobenius-based bound in [Z]. Indeed, the normalized 120-degree expression there is

    (c²−a−b)/(ab)=q+1+(r−1)/b+(b−1)/a,

strictly between q+1 and q+3. Its ceiling is q+2 or q+3. The 60-degree expression is exactly one less. Thus (8) improves that bound by either zero or three. No optimality of M* is claimed.

## 6. An explicit example below the displayed conjectural cutoff

Take the primitive 120-degree tile (a,b,c)=(45,32,67). Then

    L=1440, K=3049, q=1, r=13, M*=9.

The older displayed bound in [Z, Theorem 4] is

    M=3 ceil((4489−45−32)/1440)=12.

Our m=9 construction has equilateral side 12960 and

    N=1440*9²=116640 tiles.

The three large ideal trapezoids have shorter base and legs both 4320. Each splits into three bands with shorter bases 4320,5760,7200 and legs 1440. The strip remainders are exactly

    4320−3049=1271=19*45+13*32,
    5760−3049=2711=19*45+58*32,
    7200−3049=4151=19*45+103*32.

Each basic trapezoid contributes 45²+32²+67²=7538 tiles. The total is

    9*7538 + 3*2*(1271+2711+4151) = 116640.

This contradicts the assertion that m>=M is **necessary**, as literally written in Conjecture 2 of the inspected v4, already on its equilateral specialization. It does not contradict Theorem 4's sufficient construction or the divisibility conjecture. It also does not claim a new globally admissible integer: the result concerns this fixed tile and target.

For independent reproduction, the standard basic 120-degree trapezoid has

    A=(0,0), B=(K+L,0), C=(K,L), D=(0,L), E=(a²,L).

Its three triangles are AED, ABE, EBC at scales a,c,b. In a band with shorter base x, the remaining parallelogram is B,(x+L,0),(x,L),C. Rotations by 120 degrees are (x,y)->(−x−y,x), so all macroregion coordinates are integers in the chosen basis. `construction_116640.json` lists all 36 macroregions. Every small tile can be expanded explicitly; its coordinates are rational in this basis.

## 7. What was actually verified

`verify_certificate.py` does not import the generator. It verifies the target, every macroregion's geometry, all 630 macroregion pair intersections by exact rational polygon clipping, and equality of the covered area. Its hierarchical coverage argument uses ordinary n² subdivisions in triangle blocks and explicit strip-cell partitions in parallelograms.

The expanded run also generated and checked all 116640 small triangles: all three squared side lengths, the oriented area and containment in both their block and target. Their coordinates are included in `tiles_116640.jsonl.gz`. We did **not** test all O(N²) small-tile pairs: internal disjointness follows from the stated standard partitions, combined with the checked macroregion disjointness. This distinction is explicit in the report.

Supplementary tests cover 102 primitive triples with a<=250, 4887 equilateral scale checks, 8948 ratio-family scale checks, and 52 macro constructions (51996 exact pair intersections). Seven altered certificates were rejected. These finite checks supplement the general proofs and are not extrapolated to untested parameters.

Run:

    python verify_certificate.py construction_116640.json --expand
    python check_general_formulas.py

The scripts use the Python standard library. Their checks do not depend on `assert`, so optimized execution does not silently disable them.

## 8. Remaining obligation for the full Erdős problem

For each fixed tile covered here, all large admissible multipliers are now supplied by (8), while the exact set of smaller multipliers is not determined by these proofs. The primitive tiles themselves range over infinitely many triples. Other classified angular families must also be included. A finite exception interval **for each fixed tile** is therefore not a finite global exception list and not an all-N classification.

The complete answer to Erdős problem 634 has not been obtained in this note. In particular, neither passing both direction tests nor being below a published sufficient cutoff decides realizability in the unresolved small-scale range.

## Sources inspected

[Z] Yan X Zhang, *Tiling Triangles with 2pi/3 Angles*, arXiv:2512.22696v4, submitted 4 April 2026, manuscript dated 7 April 2026. Lemmas 1–4, Theorems 4–5, Conjectures 1–3, Propositions 8–9. https://arxiv.org/pdf/2512.22696v4

[B] Vico Bonfioli, *A signed-direction invariant for triangle tilings, and the exclusion of primes congruent to 3 modulo 4*, source `paper/erdos-634.tex`, repository `ElVec1o/erdos_634_proof`, inspected 30 September 2026, content blob SHA `b7a471881297a7cb0e44dc80ae3f65df60e8e076`. We use the two-character framework and the specific spectrum theorem, not the repository's broader or conditional prime claims. https://github.com/ElVec1o/erdos_634_proof/blob/main/paper/erdos-634.tex

[R] Michael Beeson and Yan X Zhang, *Rationality of certain triangle tilings*, arXiv:2604.01314v1, Theorem 1.2. This supplies context for why primitive rational tiles are important in the wider classification; it is not required once our fixed-tile hypotheses are imposed. https://arxiv.org/html/2604.01314v1

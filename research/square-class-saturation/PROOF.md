# Constructive saturation of quadratic-norm square classes

**Erdős problem 634 — Denis Paliy, research with ChatGPT assistance**  
**1 October 2026 — a quantitative constructive continuation, not a full solution**

## 0. Status, attribution, and dependency boundary

Let \(\mathcal S\) be the positive integers N such that some nondegenerate Euclidean triangle has a dissection into N congruent nondegenerate triangles. Reflections and arbitrary T-junctions are allowed.

This note combines an exact strip threshold with a previously established annular construction and classical quadratic-norm arithmetic. It proves a linear, kernel-dependent sufficient threshold for two infinite collections of square classes. On a W-only congruence sector it gives an exact membership criterion above that threshold, uniformly over **all** possible tiles. It does not classify every integer N, or every small multiplier. In particular, it does not decide 154.

The underlying norm criterion for \(2v^2-u^2\), the triquadratic seed, and the annular motif are **not new discoveries claimed here**. The first is already in Beeson [B, Lemmas 44–45], the seed is in [B, Theorem 11], and the annular motif was proved in the project's 29 September note [A]. Elementary norm arithmetic is written out below to make the quantifiers and exceptional cases explicit. The contribution recorded here is the exact mixed-strip cutoff, its uniform linear bound, the explicit fewer-than-v-step construction, and their integration into square-class statements.

The positive theorem can be read directly from the geometric constructions in this note. The global negative implication in Section 7 uses the published angular/rationality classification and the earlier necessary spectra, specifically their modulo-16 consequence. It does **not** use the later density-zero theorem, long-seam inequalities, theta-base obstruction, proposed all-primes proof, or proposed W/beta scale-one exclusions. No withdrawn necessity such as \(v\mid t\) is assumed.

The proofs and checkers are project-internal work, not external referee acceptance or a formalization in a proof assistant. Research priority has not been established. The two implementations (generator and geometric checker) are separate code paths, not independent human reviews. The repository input is pinned at `50d7459bd1d3f41352630323f1c55a92e8d9b64e`. No remote repository is changed by creating or running this package.

## 1. Statements

For coprime integers \(0<u<v\), set
\[
a=uv,\quad b=v^2-u^2,\quad c=v^2,\quad Q=b+c,\quad P=b+2c.
\]
The primitive triangle with sides (a,b,c) has angles \((\alpha,\beta,\gamma)\) opposite those sides, with \(3\alpha+2\beta=\pi\). Its W target at scale m has sides
\[
m(v^3,uQ,vb),\qquad N=Qm^2,
\]
and its beta-isosceles target has sides
\[
m(v^3,v^3,uP),\qquad N=Pm^2.
\]

Define
\[
R=\left\lceil c/b\right\rceil,\qquad
H=\left\lceil\frac{b+c(R-1)}u\right\rceil,
\]
\[
S_0=v\left\lceil H/v\right\rceil,\qquad
C(u,v)=S_0+(u-1)(v-1).
\tag{1.1}
\]

**Theorem 1 (quantitative fixed-tile construction).** For either target, every integer scale \(m\ge C(u,v)\) is tileable by the primitive tile. There is an explicit description using a seed at a multiple of v and at most v−1 exterior annuli. Moreover
\[
\boxed{C(u,v)<2Q<2P.}\tag{1.2}
\]
Every positive scale divisible by v is also constructible, whether or not it is below C. None of these sufficient thresholds is asserted to be the minimum scale for actual tilings.

Call a positive squarefree d **2-compatible** when every odd prime divisor is 1 or 7 modulo 8. Call it **3-negative-compatible** when
\[
\begin{gathered}
p\mid d,\ p>3\quad\Longrightarrow\quad p\equiv1\text{ or }11\pmod{12},\\
3\nmid d\ \Longrightarrow\ d\equiv2\pmod3,\qquad
3\mid d\ \Longrightarrow\ d/3\equiv1\pmod3.
\end{gathered}\tag{1.3}
\]
These names only abbreviate the displayed arithmetic tests.

**Theorem 2 (square-class saturation).**

* For every 2-compatible squarefree \(d>2\), there is a single primitive tile and W target shape that construct \(dm^2\) for every integer \(m\ge2d\).
* For every 3-negative-compatible squarefree \(d\notin\{2,3\}\), the same assertion holds with a beta-isosceles target.

The actual sufficient threshold is the least C(u,v) among the finitely many primitive solutions of Q=d or P=d, respectively, and is strictly less than 2d. The exceptional kernels 1,2,3 have classical constructions at every multiplier. Kernel 6 is also classical, separately from the two norm tests.

**Theorem 3 (exact tail in a W-only sector).** Let d be squarefree with
\[
d\equiv14\pmod{16},\qquad3\nmid d.
\]
If \(\gcd(m,6)=1\) and \(m\ge2d\), then
\[
\boxed{dm^2\in\mathcal S\quad\Longleftrightarrow\quad
        p\equiv1\text{ or }7\pmod8\text{ for every odd }p\mid d.}\tag{1.4}
\]
If the right side fails, the negative answer holds for **every** m coprime to 6, without a size restriction. If it holds, the positive answer holds for every m at or above the sharper computable threshold C, with no restriction on divisibility by 2 or 3. The restrictions in the global negative assertion must not be omitted.

## 2. Exact threshold for the existing apex annulus

Write \(\Theta_T\) for the theta-isosceles triangle of equal sides bvT and base ubT. Its apex angle is alpha, and \(\cos\alpha=Q/(2c)\). The construction [A, Section 3] makes the region between apex-centered copies at scales T and T+u from three tile-shaped triangular blocks of integral scales a,c,b and an alpha-parallelogram with side lengths bc and
\[
L=ubT-a^2-b^2.\tag{2.1}
\]
The following argument replaces only the coarse Frobenius sufficient bound in that construction. It does not classify all possible tilings of this trapezoid.

A mixed-strip filling of the parallelogram is available if
\[
L=xb+yc,\qquad x,y\in\mathbb Z_{\ge0}.\tag{2.2}
\]
An x-part is split into b-wide strips and c-step subdivisions along its bc side; a y-part uses c-wide strips and b-step subdivisions. Each cell is a b-by-c parallelogram with angle alpha or its supplement; its appropriate diagonal has length a. Splitting cells produces congruent copies of the original tile. Interfaces between filled blocks need not be edge-to-edge.

Here \(\gcd(b,c)=1\), and \(a^2=c(c-b)\). Reducing (2.2) modulo b gives \(y\equiv-c\pmod b\). With \(R=\lceil c/b\rceil\), the smallest nonnegative such y is
\[
y_0=bR-c,\qquad0<y_0<b.
\]
(The endpoints cannot occur because b>1 and gcd(b,c)=1.) Substitution gives
\[
x_0=uT-b-c(R-1).\tag{2.3}
\]
All other nonnegative choices of y have the form y_0+kb for k≥0, and decrease x by kc. Thus
\[
\boxed{L\in b\mathbb Z_{\ge0}+c\mathbb Z_{\ge0}
       \quad\Longleftrightarrow\quad T\ge H.}\tag{2.4}
\]
This is an exact equivalence for the mixed-strip recipe, **not a necessary cutoff for arbitrary geometric tilings**.

For clarity, the annulus coordinates are included. Pairs (x,y) represent physical points \((x,\sqrt D\,y)\), where \(D=4v^2-u^2>0\). Put
\[
\begin{aligned}
A&=(0,0),&C&=(ub(T+u),0),\\
B&=(u^2b/2,ub/2),&E&=B+(ubT,0),\\
J&=B+(a^2,0),&K&=(c^2,0),&F&=E-(b^2,0).
\end{aligned}
\]
The outer trapezoid is ACEB. Its pieces are ABJ, AJK, FEC, and KJFC. The triangular scales are a,c,b. The last region is the parallelogram of (2.1), since
\[
J-K=F-C=(-bQ/2,ub/2),\qquad |J-K|=bc,
\]
and its horizontal side has length L. Nonnegativity in (2.2) guarantees the boundary orders A,K,C and B,J,F,E, with a zero-width part simply omitted. Therefore these are actual disjoint pieces, not merely a sum of areas.

The number of tiles added to the theta target is
\[
a^2+b^2+c^2+2L=b\bigl((T+u)^2-T^2\bigr).\tag{2.5}
\]

## 3. Seeds and the lift to W and beta

### 3.1 A complete seed at every positive multiple of v

The W seed at scale v is the triquadratic construction [B, Theorem 11]. An explicit version, also contained as the first four blocks in the project's QP construction, is recalled so that sufficiency is geometric.

In the same metric coordinates set
\[
O=(0,0),\quad A=(b^2,0),\quad C=(-u^2b/2,ub/2),
\]
\[
D_1=(-u^2b/2,-ub/2),\quad
E=(-u^2Q/2,-u^3/2),\quad B=D_1+E.
\]
Triangle ABC has sides \((v^4,uvQ,v^2b)\), the scale-v W sides. It is partitioned into triangles OAC, OAD_1, OCE and parallelogram OD_1BE. Indeed
\[
D_1=A+(b/c)(B-A),\qquad E=C+(c/Q)(B-C),
\]
so D_1 and E are strictly inside the indicated sides. O has positive barycentric coordinates
\[
(u^2/c,\ b/Q,\ b^2/(cQ))
\]
with respect to (A,C,B); these sum to one. Drawing the segments from O thus gives the claimed disjoint partition. The four-vertex region is a genuine parallelogram because B=D_1+E.

The three triangular blocks have scales b,b,a. The parallelogram step vectors D_1/b and E/u² have lengths a and c, and their difference has length b. A b-by-u² grid split along that diagonal supplies 2bu² tiles. The full count is
\[
2b^2+a^2+2bu^2=cQ=v^2Q.\tag{3.1}
\]
Multiplying every coordinate by r and every grid subdivision count by r supplies a W seed at scale rv, for every positive integer r.

### 3.2 Why an arbitrary W or beta tiling can be extended

The geometrical decompositions of the targets used in [A] are especially transparent in the following canonical coordinates, with apex at zero:
\[
f=(-bv,0),\quad z=(-vQ/2,-uv/2),\quad
w=(-bQ/(2v),ub/(2v)),
\]
\[
z_2=z+(P/Q)(w-z).
\tag{3.2}
\]
One has \(f=z+(c/Q)(w-z)\) and \(w=z+(Q/P)(z_2-z)\). Thus f is strictly between z and w, and w is strictly between z and z_2. Direct metric calculation gives:

* (0,f,w) is the scale-one theta target;
* (0,f,z) is a v-scaled copy of the original tile;
* (0,w,z_2) is another v-scaled copy of the original tile;
* (0,z,w) is the scale-one W target;
* (0,z,z_2) is the scale-one beta target.

Consequently W is a theta region plus one tile-shaped region, and beta is a theta region plus two tile-shaped regions, with common apex. The beta seed follows by adding a v²-scaled original-tile triangle to the scale-v W seed. Scaling by r supplies every positive multiple rv for beta as well.

Apply homothety about the common apex. Between scales T and T+u, the theta component has exactly the annulus of Section 2. Each tile-shaped component has an ordinary triangular-grid annulus between integer scales vT and v(T+u). Such an annulus always has a tiling: if a reference tile has vectors e,f, and the two scales are k and k+h, use the triangle
\[
(ke,(k+h)e,ke+hf)
\]
and the parallelogram
\[
(ke,kf,(k+h)f,ke+hf).
\]
The first is a scale-h original tile; the second is a k-by-h cell grid whose difference diagonal is the third tile side. The two pieces fill the annulus, and their count is h²+2kh.

The entire annulus is outside the existing scale-T target. Therefore this extension does not assume that an arbitrary tiling of that target contains the particular theta decomposition. We have proved, for either family,
\[
T\ge H,\quad T\text{ realized}\quad\Longrightarrow\quad T+u\text{ realized}.
\tag{3.3}
\]
For W the added count is Q((T+u)²−T²), and for beta it is P((T+u)²−T²). This is the prior annular lift with the sharper exact threshold (2.4).

## 4. A finite construction for every scale beyond C, and a linear bound

For \(m\ge C=S_0+(u-1)(v-1)\), choose the unique i with
\[
0\le i<v,\qquad iu\equiv m\pmod v.
\]
Then \(m-S_0-iu\) is divisible by v and is at least −(v−1), hence is nonnegative. Write it as jv. Start from the known seed at scale \(S_0+jv\), and apply i annuli of increment u. All starting scales are at least H. This constructs m with fewer than v annuli. This argument explicitly handles the quantifier over every large integer scale; it does not assume that a finite collection of computed tilings fills a tail.

It remains to bound C in terms of the count coefficient. If u=1, then b=c−1, R=2, and H=b+c=Q. If u≥2, then
\[
ub-c=(u-1)v^2-u^3\ge u^2-u-1>0.
\]
Also \(R-1\le(c-1)/b\), and
\[
b^2+c(c-1)<bc+c^2=cQ\le ubQ.
\]
It follows that \(b+c(R-1)\le uQ\), so H≤Q. Finally,
\[
\begin{aligned}
C&=v\lceil H/v\rceil+(u-1)(v-1)\\
 &\le H+(v-1)+(u-1)(v-1)\\
 &=H+uv-u\\
 &\le Q+uv-u<2Q.
\end{aligned}\tag{4.1}
\]
The last strict inequality uses uv<v²<Q. Since P>Q, Theorem 1 follows. This bound is not claimed sharp.

## 5. Which squarefree kernels have a reduced W or beta representative?

This section is elementary norm theory; it is not a novel norm-solvability claim. In the W case the relevant criterion and a positive-cone reduction already appear in [B, Lemmas 44–45]. The proof here also records the sign restriction for the beta case.

**Lemma 5.1.** For squarefree d>2, there exist coprime integers 0<u<v with
\[
d=2v^2-u^2
\]
if and only if d is 2-compatible. For squarefree \(d\notin\{2,3\}\), such a representation
\[
d=3v^2-u^2
\]
exists if and only if d is 3-negative-compatible.

**Proof of norm existence.** For k=2 or 3, the ring \(\mathbb Z[\sqrt k]\) is norm-Euclidean. Given a quotient x+y√k in its fraction field, round x,y to nearest integers. For the residual coordinates |x|,|y|≤1/2,
\[
|x^2-ky^2|\le k/4<1.
\]
This supplies the Euclidean algorithm for the absolute norm. In particular every ideal is principal. If an odd prime p not dividing k has k as a quadratic residue, the ideal generated by p and r−√k, with r²≡k modp, has index p. Its generator therefore has norm ±p. If k is a nonresidue, p dividing x²−ky² forces p to divide both coordinates, so p² divides the norm. A squarefree norm cannot contain such an inert prime.

For k=2, 1+√2 is a unit of norm −1; the sign of any norm can therefore be reversed. The ramified prime 2 is represented by √2, of norm −2. For an odd p, the condition (2/p)=1 is exactly p≡1 or7 mod8. Multiplying generators for the primes of d and choosing the sign with that unit gives norm −d precisely under 2-compatibility.

For k=3, the split odd primes p>3 are exactly p≡1 or11 mod12. Their norm sign is fixed by reduction modulo3: the norm must be 1 modulo3, so a generator has norm +p for p≡1 mod3 and −p for p≡2 mod3. The prime 2 is represented by 1+√3 with norm −2; prime3 is represented by √3 with norm −3. Multiplying these elements gives norm −d exactly under the sign conditions (1.3). These conditions are also necessary: if 3∤d, x²−3y²=−d forces d≡2 mod3; if 3|d, squarefreeness forces x=3z and 3∤y, so d/3=y²−3z²≡1 mod3. Thus no sign ambiguity is being suppressed.

**Reduction to the required cone.** Suppose \(x^2-ky^2=-d\). Change signs so the real embedding \(x+y\sqrt k\) is positive and its conjugate negative, and write
\[
x=\sqrt d\sinh s,\qquad y=\sqrt{d/k}\cosh s.
\]
Multiplication by a positive norm-one unit shifts s by its logarithm. Use \(\varepsilon_2=3+2\sqrt2\), or \(\varepsilon_3=2+\sqrt3\). Choose a power so \(|s|\le\tfrac12\log\varepsilon_k\), then change the sign of x if necessary. The identity
\[
\sqrt k\tanh\bigl(\tfrac12\log\varepsilon_k\bigr)=1
\]
gives 0≤x≤y. Every operation preserves integral coordinates and norm −d. Squarefreeness makes gcd(x,y)=1. The endpoint x=0 implies d=k and y=1; the endpoint x=y implies d=k−1 and y=1. These are exactly the excluded degenerate kernels. Hence u=x, v=y satisfy 0<u<v in all other cases. ∎

The arithmetic reduction is finite in the ordinary integers:
\[
Q=d\quad\Longrightarrow\quad v^2<d,
\qquad P=d\quad\Longrightarrow\quad 2v^2<d.
\tag{5.1}
\]
One can enumerate v in these bounded intervals, test whether 2v²−d or3v²−d is a positive square, and retain primitive 0<u<v. The norm lemma proves that the search succeeds under the stated conditions; success is not inferred from a bounded experiment. This supplies the parameters effectively.

## 6. Square-class saturation

For a 2-compatible squarefree d>2 choose a reduced representative Q=d from Lemma 5.1. Theorem 1 gives an actual W tiling at every m≥C(u,v), and C<2Q=2d. For a 3-negative-compatible kernel choose P=d and use the beta version; again C<2Q<2P=2d. The tile is fixed once d and the chosen representative are fixed; it does not vary with m. This proves Theorem 2.

Some representatives and sufficient bounds are:

| Family | Kernel d | (u,v) | Primitive tile | H | C |
|---|---:|---|---|---:|---:|
| W | 14 | (2,3) | (6,5,9) | 7 | 11 |
| W | 46 | (2,5) | (10,21,25) | 23 | 29 |
| W | 62 | (6,7) | (42,13,49) | 27 | 58 |
| W | 94 | (2,7) | (14,45,49) | 47 | 55 |
| W | 142 | (10,11) | (110,21,121) | 63 | 156 |
| beta | 122 | (5,7) | (35,24,49) | 25 | 52 |

Kernel122 is not 2-compatible (61≡5 mod8), but it is 3-negative-compatible. It illustrates that the beta positive theorem is not merely a second name for the W theorem. These are sufficient bounds and are not claimed minimal.

For d=14,m=11, the construction starts from W_9 and adds one u=2 annulus. Its tile is (6,5,9), target sides are (297,308,165), and the count is 1694. The compressed certificate has eleven convex grid blocks. No claim of first discovery of this numerical count is made.

## 7. From a branch construction to a global exact sector

The following is the earlier modulo-16 consequence of the exhaustive necessary spectrum [U, Sections 2–3]:
\[
3\nmid N,\quad N\equiv14\pmod{16}
\quad\Longrightarrow\quad\text{every possible tiling is in W.}\tag{7.1}
\]
For auditability, here is its arithmetic content. Separate the classical similar/right/commensurable-angle cases using the published classification and rationality input [BZ]. Primitive Group1 counts are Qt², Pt², bt², bQt², QPt², and the double-angle count is another bt². The b coefficients are either odd or divisible by8. Squares modulo16 show that only Q among these coefficients can be 14 modulo16. As N has 2-adic valuation one, every multiplier t is odd and does not change this even residue.

In primitive 60°/120° norm triples c²=a²±ab+b², if a,b are both odd then ab≡1 or7 modulo8, respectively. If one is even it is divisible by8. Substitution into the seven necessary coefficients
\[
ab\ (\text{both signs}),\ b(a+b),\ b(a+2b),\
(a+2b)(2a+b),\ 3(a+2b)(a+b),\ (2a+b)(a+b)
\]
shows that none is 6 modulo8 except possibly the row with an explicit factor3. That row is excluded by 3∤N. Classical sums of two squares and twice a square cannot have residue6 modulo8; other exceptional classical forms are divisible by3. This proves the collapse (7.1), conditional on precisely the published exhaustive classification and earlier integer-scale derivations, not on a proposed prime-case proof.

Now let d,m satisfy the sector hypotheses in Theorem3. Then N=dm² also satisfies (7.1). In a W tiling write
\[
dm^2=(2v^2-u^2)t^2.
\]
If an odd inert prime p divides d, it occurs to an odd exponent in N and therefore also to an odd exponent in 2v²−u². But an inert prime dividing that primitive form would force p|u,v, a contradiction. Thus 2-compatibility is globally necessary for every such m.

Conversely, 2-compatibility supplies Q=d and a fixed tile. The construction in Theorem2 realizes every m≥2d, indeed every m≥C for the selected pair, without needing the sector's restrictions on m. This proves both directions of (1.4). ∎

For example, 110≡14 mod16 is squarefree and has inert primes5 and11. Hence 110m² is impossible for every m coprime to6. This is an application of the previously known W-only norm obstruction, not a new negative family invented here. What this continuation adds in that sector is the uniform constructive tail on the complementary arithmetic classes. The conclusions cannot be silently extended to m divisible by3; the code deliberately returns UNKNOWN on 990 rather than applying this negative test.

## 8. Certificate format and the exact finite checks

`generate.py` produces a complete list of convex macroregions covering the target. Each region records either a triangular grid or a parallelogram grid, with integer subdivision counts and a selected diagonal. Rational coordinates use the metric diag(1,4v²−u²). The recorded very large tile counts are represented by these finite grid formulas, not by claiming to have enumerated each tile.

`verify_geometry.py` imports neither the generator nor the arithmetic classifier. It checks the primitive tile, target side lengths, every grid cell's three squared lengths, positive integer grid dimensions, containment, exact areas, total count, and every pair of macroregions by rational convex clipping. All macroregion interiors are disjoint. Since the finite union is closed, contained in the triangular target, and has its full area, it covers the target including its boundary. This is a full positive geometric certificate in compressed form.

Run:

```text
python run_checks.py
python saturation.py 1694 38686 215822 342698 13310 154
python saturation.py 1694 --certificates output
```

The default regression has independent forward parameter enumeration and inverse arithmetic tests on all squarefree d≤20,000, strip-coin checks near the exact threshold, all primitive (u,v) with v≤80 for the quantitative bound and consecutive constructive plans, and complete geometric macrochecks on a smaller parameter range plus selected larger examples. Seven corrupted certificates and five invalid inputs are rejected. Exact counts, examples and scope are recorded in `verification.json`; those finite counts are not a proof of the universal theorems.

`YES` means a classical construction or an explicit scheme with a checked certificate in the CLI. `NO` is used only for the global inert-prime obstruction with all W-only sector hypotheses. `UNKNOWN` means this module does not decide the input, not that the input has no tiling or is unknown to the literature. This is a new complementary module, not a replacement for earlier QP/classical/exact-sector programs. In particular no previously known positive result is withdrawn by this module returning UNKNOWN.

## 9. What this does and does not finish

This continuation crosses a specific infinite-parameter gap: within either compatible norm class it selects a primitive tile directly from the kernel, gives a proved finite search bound for that tile, and constructs every sufficiently large multiplier with a uniform linear threshold. In the W-only sector it completes the positive direction matching the arithmetic obstruction, so the tail has an exact all-tile criterion.

It does not decide all small multipliers in these classes, the complete set of odd multipliers in other even square classes, or all remaining 60°/120° cases. 154 is outside the W-only sector and is not settled. A finite exception set for each d is not a single finite global exception list. No percentage of completion is inferred from these results.

The earlier statement that all large multipliers in odd square classes, and all large even multipliers in even square classes, are constructible was already in [A, Section7]. It is not relabeled as a new theorem here. Similarly, norm solvability by itself is never treated as a small-scale tiling construction.

## References and provenance

[B] Michael Beeson, *Triangle Tiling: The case 3α+2β=π*, arXiv:1206.2229v4, 25 September2026. Theorem11 for the triquadratic seed; Lemmas44–45 for the W norm criterion and cone reduction. Only the stated valid construction and arithmetic claims are used. https://arxiv.org/html/1206.2229v4

[BZ] Michael Beeson and Yan X Zhang, *Rationality of certain triangle tilings*, arXiv:2604.01314v1. Table1 and Theorem1.2, including the angular classification attributed to Laczkovich. https://arxiv.org/html/2604.01314v1

[A] Denis Paliy, research with ChatGPT assistance, *Two annuli settle all five rational families at sufficiently large scales*, 29 September2026, `docs/universal-rational-scales.md`, and `docs/scale-spectra.md`, pinned project commit. Existing annuli, seed propagation and previous square-class consequences. https://github.com/DenisUkranian/erdos-634-tilings/tree/50d7459bd1d3f41352630323f1c55a92e8d9b64e

[U] Previous project note, *Uniform arithmetic sectors and asymptotic concentration for congruent triangle dissections*, 1 October2026, Sections2–3, copied unchanged as `dependencies/UNIFORM_SECTORS_PROOF.md`. The required earlier necessary count table and modulo16 collapse are restated in Section7. Its density results are not inputs here.

The geometrical motifs have antecedents in Laczkovich's rational trapezoid constructions, as credited by [A]. The independent explicit seed-coordinate calculation above is a verification of an existing construction, not a priority claim. The archive contains only this continuation and the specifically needed previous proof, not a purported archive of every project artifact.

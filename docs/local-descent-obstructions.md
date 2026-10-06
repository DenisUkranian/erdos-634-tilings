# Local descent obstructions for every odd multiplier

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026**

Let \(\mathcal S\) be the triangle-tiling counts used throughout this repository. This note excludes **every odd multiplier** in two infinite families of square classes. The main family permits arbitrarily many prime factors in the squarefree kernel. The obstruction does not require a rank computation, and some of the excluded odd sectors belong to curves of positive rank.

The geometric inputs are the existing exhaustive shape classification and integral necessary coefficient spectra. The arithmetic arguments below are elementary local arguments on explicit quartic equations. They do not classify small even multipliers or solve all of Erdős problem 634. External priority and referee acceptance have not been established.

## 1. Main statements

**Theorem 1.1.** Let \(R>1\) be squarefree and have an even number of prime factors, each satisfying

\[
\ell\equiv7\pmod{24}.
\]

Then

\[
\boxed{6R m^2\notin\mathcal S\qquad\text{for every odd positive integer }m.}
\tag{1.1}
\]

There is no bound on the number of prime factors of \(R\). For example, taking \(R=7p\), where \(p\ne7\) is any prime congruent to 7 modulo 24, gives infinitely many squarefree kernels by Dirichlet's theorem.

**Theorem 1.2.** Let \(p\) be a prime such that

\[
p\equiv13\pmod{24},\qquad
3^{(p-1)/4}\equiv5^{(p-1)/2}\pmod p.
\tag{1.2}
\]

Then

\[
\boxed{30p m^2\notin\mathcal S\qquad\text{for every odd positive integer }m.}
\tag{1.3}
\]

Condition (1.2) is a finite modular-exponentiation test. It holds, for example, at \(p=37,109,157,181,229\). Appendix A proves that infinitely many primes satisfy it. That infinitude argument is separate from the elementary exclusion for any given prime.

The distinction from a rank-zero obstruction is concrete:

- The first family contains \(d=1302\), with an explicit primitive F3 coefficient witness whose square multiplier is even.
- The second contains \(d=4710\), whose associated F3 elliptic curve has a directly verifiable nontorsion rational point.

Section 6 gives the exact certificates. Positive rank can therefore coexist with the absence of **all** odd-multiplier counts.

## 2. Reduction to three coefficient rows

We use the residue reduction proved in [elliptic square classes, Theorem 4.1](elliptic-square-classes.md), together with the necessary spectra in the [uniform-reduction proof](../research/uniform-reduction/PROOF.md). Only the row reduction is used; no rank-zero hypothesis is assumed here.

If \(d>6\) is squarefree, \(d\equiv6\pmod{16}\), and \(m\) is odd, a putative tiling of count \(dm^2\) must have a primitive coefficient

\[
D=ds^2,\qquad s\mid m,
\tag{2.1}
\]

in one of the following three rows:

| Row | Primitive coefficient | Parameters |
|---|---|---|
| Group-1 alpha | \(bQ\) | \(b=v^2-u^2,\ Q=2v^2-u^2\) |
| Group-1 QP | \(QP\) | \(Q=2v^2-u^2,\ P=3v^2-u^2\) |
| 120-degree F3 | \(3(a+2b)(a+b)\) | \(c^2=a^2+ab+b^2\) |

The Group-1 parameters satisfy \(0<u<v\), \(\gcd(u,v)=1\); the F3 parameters are positive integers with \(\gcd(a,b)=1\). In particular,

\[
\gcd(b,Q)=\gcd(Q,P)=1.
\tag{2.2}
\]

For completeness, the residue argument excludes the two difference-of-squares rows at 2-adic valuation one, W modulo 16, beta modulo 8, and every primitive norm row except F3 modulo 8. The classical forms in this residue sector have only the exceptional squarefree kernel \(d=6\), which is excluded by \(d>6\). The full residue table and its proof are in the cited note.

Both Group-1 survivors have \(Q\) even. Indeed, if \(u\) is odd and \(v\) even, both factors are odd. If both are odd, alpha has \(v_2(b)\ge3\), while QP is 2 modulo 8. Neither gives \(D\equiv6\pmod{16}\). Thus \(u\) is even and \(v\) odd. For alpha, the stronger residue forces

\[
u\equiv2\pmod4,\qquad Q/2\equiv7\pmod8.
\tag{2.3}
\]

Because every scale in (2.1) is integral, excluding odd \(s\) excludes every odd \(m\), including multipliers divisible by 3 or by primes outside the squarefree kernel.

## 3. A necessary local-cover test for F3

Put \(k=\operatorname{sf}(3d)\), where \(\operatorname{sf}\) denotes the squarefree kernel. In the applications below \(k\) is even. Consider

\[
E'_k:\quad y^2=x^3+6kx^2-3k^2x.
\tag{3.1}
\]

### From an odd F3 coefficient to an even square class

An odd F3 coefficient multiplier gives a rational point on (3.1) with

\[
v_2(x)=1.
\tag{3.2}
\]

This is the necessary direction of [F3 odd multipliers, Theorem 1.1](f3-odd-multipliers.md), and can be checked directly. Set

\[
A=a+2b,\quad B=a+b,\quad
T=A/B=kz^2,\quad w=c/B.
\]

Then \(w^2=T^2-3T+3\). For even \(d\) and odd \(s\), the primitive plus-norm parity rules give \(a\) even, \(b\) odd, \(8\mid a\). Hence \(v_2(A)=1\), \(B,c\) are odd, and \(z,w\) are 2-adic units. The formulas

\[
x=k(2w+2T-3),\qquad y=2kxz
\tag{3.3}
\]

satisfy (3.1) by substitution, and the parenthesis in (3.3) is a 2-adic unit. This proves (3.2). No converse or density argument is needed for the exclusions below.

**Lemma 3.1 — necessary descent cover.** A rational point satisfying (3.2) gives an even signed squarefree integer \(e\), supported on the primes dividing \(3k\), and coprime integers \(u,v\) satisfying

\[
Z^2=e u^4+6ku^2v^2-\frac{3k^2}{e}v^4,
\qquad Z\in\mathbb Z.
\tag{3.4}
\]

**Proof.** Let \(e\) represent the square class of \(x\). At a prime \(q\nmid3k\), an odd positive valuation of \(x\) makes the linear term in (3.1) uniquely minimal, contradicting the even valuation of \(y^2\). Any negative valuation of \(x\) is even, because the cubic term is uniquely minimal. Thus \(e\) has the asserted support; (3.2) makes it even.

Write \(x=e(u/v)^2\) with \(\gcd(u,v)=1\). Substitution yields (3.4), with \(Z=yv^3/(eu)\). Its right side is an integer, since \(e\mid3k^2\); a rational number whose square is an integer is an integer. The exceptional points \(O\) and \((0,0)\) do not satisfy (3.2). ∎

Equation (3.4) is the standard 2-isogeny descent cover, recorded in [ALP, §2]. The proof above supplies all the necessity used here. We do **not** assume that local solubility implies a rational point.

### Three local rules

**Lemma 3.2.** The following are necessary conditions for a primitive solution of (3.4).

1. If \(k\equiv2\pmod{16}\) and \(e\) is even, then
   \[
   e\equiv6\pmod8.
   \tag{3.5}
   \]
2. If \(3\nmid k\), then
   \[
   3\nmid e\ \Longrightarrow\ e\equiv1\pmod3,
   \qquad
   e=3\delta\ \Longrightarrow\ \delta\equiv2\pmod3.
   \tag{3.6}
   \]
3. Let \(\ell>3\) be a prime dividing \(k\).
   - If \(\ell\nmid e\), the cover is impossible when
     \[
     (e/\ell)=(-3e/\ell)=-1.
     \tag{3.7}
     \]
   - If \(e=\ell\delta\), \(k=\ell\kappa\), the cover requires a root of
     \[
     t^2+6t-3=0\pmod\ell
     \tag{3.8}
     \]
     with quadratic character \((\delta\kappa/\ell)\). In particular, \((3/\ell)=-1\) excludes the cover.

Here \((\cdot/\ell)\) is the Legendre symbol.

**Proof.** For (3.5), write \(k=2h\), \(h\equiv1\pmod8\), and \(e=2\delta\). If exactly one of \(u,v\) is odd, the right side of (3.4) has valuation one. If both are odd, it is

\[
2\delta+12-6\delta^{-1}
\equiv12-4\delta\pmod{16},
\]

using \(h^2\equiv1\pmod{16}\) and \(\delta^{-1}\equiv\delta\pmod8\). For \(\delta\equiv1\pmod4\), this is the nonsquare 8 modulo 16. Thus \(\delta\equiv3\pmod4\).

For (3.6), if \(3\nmid e\) and \(u\) is a unit, reduction modulo 3 forces \(e\equiv1\). If \(3\mid u\), the last term has valuation one, impossible. If \(e=3\delta\) and \(v\) is a unit, the last term modulo 3 forces \(-\delta\) to be a square, hence \(\delta\equiv2\). If \(3\mid v\), the first term has valuation one.

For (3.7), a unit \(u\) makes the first term a nonsquare modulo \(\ell\). Otherwise \(v\) is a unit, \(\ell\mid Z\), and division by \(\ell^2\) gives the nonsquare \(-3(k/\ell)^2/e\) modulo \(\ell\).

Finally suppose \(\ell\mid e\). If exactly one of \(u,v\) is a unit, the right side has valuation one. If both are units, the coefficient of \(\ell\) must vanish modulo \(\ell\):

\[
\delta u^4+6\kappa u^2v^2-\frac{3\kappa^2}{\delta}v^4=0.
\]

Dividing by \(\kappa^2v^4/\delta\) gives (3.8), with
\(t=\delta u^2/(\kappa v^2)\). Its character is \((\delta\kappa/\ell)\), and its discriminant is \(48\), whose character is \((3/\ell)\). ∎

## 4. Proof of the family with unbounded prime support

Let \(R\) satisfy Theorem 1.1 and put \(d=6R\), \(k=2R\). An even number of prime factors congruent to 7 modulo 8 gives

\[
R\equiv1\pmod8,\qquad k\equiv2\pmod{16},\qquad d\equiv6\pmod{16}.
\]

Also \(d>6\), so Section 2 applies.

**F3.** Every even cover class \(e\) containing a prime \(\ell\mid R\) is excluded by Lemma 3.2, since \((3/\ell)=-1\). The only remaining possibilities are \(e=\pm2,\pm6\). Rule (3.5) excludes \(2,-6\). At any \(\ell\mid R\),

\[
(-2/\ell)=(6/\ell)=-1,\qquad(-3/\ell)=1.
\]

Thus (3.7) excludes \(-2,6\) as well. There is no odd F3 coefficient multiplier.

**Alpha.** Suppose \(bQ=6R s^2\), with \(s\) odd. The prime 3 cannot divide \(Q=2v^2-u^2\), since 2 is a nonresidue modulo 3 and \(u,v\) are coprime. Consequently \(3\mid b\). Coprimality of \(b,Q\) and evenness of \(Q\) give

\[
Q=2A x^2,\qquad A\mid R,
\]

for an integer \(x\) prime to 3. Every prime of \(A\) is 1 modulo 3, so \(Q\equiv2\pmod3\). But \(3\mid b=v^2-u^2\) forces \(Q\equiv v^2\equiv1\pmod3\), a contradiction.

**QP.** Suppose \(QP=6R s^2\). No prime \(\ell\mid R\) can divide \(P=3v^2-u^2\), since \((3/\ell)=-1\). As above, \(3\nmid Q\). Their coprimality therefore forces

\[
Q=2R x^2,\qquad P=3y^2.
\tag{4.1}
\]

Choose any \(\ell\mid R\). Since \(\ell\mid Q\), we have \(u^2\equiv2v^2\pmod\ell\), with \(v\) a unit. Hence

\[
P=3v^2-u^2\equiv v^2\pmod\ell
\]

is a nonzero square. Equation (4.1) says it is a nonsquare, because \((3/\ell)=-1\) and \(\ell\nmid y\). This final contradiction eliminates QP.

All three possible rows are absent. This proves Theorem 1.1. ∎

## 5. Proof of the modular-power family

Assume (1.2), and put \(d=30p\), \(k=10p\). Since \(p\equiv5\pmod8\), again \(d\equiv6\pmod{16}\), \(k\equiv2\pmod{16}\).

**F3.** The even signed squarefree classes are supported on \(2,3,5,p\). Rule (3.5) leaves

\[
-2,\ 6,\ -10,\ 30,\ -2p,\ 6p,\ -10p,\ 30p.
\]

Since \(p\equiv1\pmod3\), rule (3.6) leaves only

\[
-2,\ 6,\ -2p,\ 6p.
\tag{5.1}
\]

At \(\ell=p\), the first two are excluded by (3.7), because
\((-2/p)=(6/p)=-1\) and \((-3/p)=1\).

For the remaining two, choose \(r\) with \(r^2\equiv3\pmod p\). The two roots in (3.8) are \(-3\pm2r\); they have the same character because their product is \(-3\), a quadratic residue. For \(e=-2p\) or \(6p\), the required character \((\delta\kappa/p)\) is respectively \((-20/p)\) or \((60/p)\), both equal to \((5/p)\).

The identity

\[
-3+2r=\frac{r(r-1)^2}{2}
\tag{5.2}
\]

holds modulo \(p\). Its factors are nonzero. Since \((2/p)=-1\), its character is \(-(r/p)\). On the other hand,

\[
(r/p)\equiv r^{(p-1)/2}
\equiv3^{(p-1)/4}
\equiv5^{(p-1)/2}\equiv(5/p)\pmod p.
\]

Both characters are \(\pm1\), so they are equal as integers. Thus both roots in (3.8) have character \(-(5/p)\), opposite to the required one. This excludes the last two classes in (5.1).

**Alpha.** Its even factor has the form \(Q=2A x^2\), with \(A\mid15p\), and (2.3) requires \(A\equiv7\pmod8\). Every odd prime dividing \(Q\) must have \((2/\ell)=1\). But each of \(3,5,p\) has \((2/\ell)=-1\). Thus \(A=1\), a contradiction. This is also the alpha obstruction of [elliptic square classes, §3](elliptic-square-classes.md).

**QP.** The prime 5 divides its coefficient. Yet \((2/5)=(3/5)=-1\), so neither \(Q=2v^2-u^2\) nor \(P=3v^2-u^2\) can be divisible by 5 for coprime \(u,v\). This is impossible.

All three rows are excluded, proving Theorem 1.2. ∎

## 6. Positive-rank controls and the even-multiplier limitation

For \(R=7\cdot31\), Theorem 1.1 excludes every odd multiplier in square class \(d=1302\). Nevertheless,

\[
(a,b,c)=(159711,13889,167089)
\]

is a positive primitive plus-norm triple, with

\[
\begin{aligned}
\gcd(a,b)&=1,\\
c^2&=a^2+ab+b^2,\\
3(a+2b)(a+b)&=1302\cdot8660^2.
\end{aligned}
\tag{6.1}
\]

The multiplier 8660 is even. One way to obtain (6.1) is the rational point
\((-1200,51960)\in E'_{434}(\mathbb Q)\); its quartic coordinates are

\[
T=\frac{187489}{173600},\qquad
w=-\frac{167089}{173600}.
\]

The inverse formulas in [F3 odd multipliers, §2](f3-odd-multipliers.md) give (6.1), using \(|w|\). The [elliptic-rank theorem](elliptic-square-classes.md) therefore proves positive rank. This is a coefficient witness: actual tilings follow at the permitted sufficiently large geometric scales from the existing F3 construction. We do not assert that the unscaled coefficient in (6.1) is itself attained.

For Theorem 1.2, take \(p=157\), \(d=4710\), \(k=1570\). Direct substitution verifies

\[
P=(-471,73947)\in E'_{1570}(\mathbb Q).
\]

It is nontorsion by [F3 odd multipliers, Corollary 1.2 and its torsion proof](f3-odd-multipliers.md): for squarefree \(k\ne1\), the rational torsion consists only of \(O,(0,0)\). An independent check is also short. The tangent slope at \(P\) is \(-211/2\), so \(x(2P)=10609/4\). The integral short-Weierstrass change \(X=x+2k\) gives

\[
y^2=X^3-15k^2X+22k^3,
\qquad X(2P)=23169/4.
\]

Nagell–Lutz excludes torsion because this coordinate is nonintegral.

These controls show why positive rank alone cannot settle odd-multiplier existence. Conversely, the local cover test is only an obstruction: if some covers survive, no global point or tiling follows without further work. The results above leave prescribed small even multipliers undecided and do not complete the global classification in problem 634.

## 7. An effective eventual parity classification

**Corollary 7.1.** For each squarefree kernel \(d\) in either Theorem 1.1 or Theorem 1.2, one can compute an integer \(T(d)\) such that

\[
\boxed{m\ge2T(d)\quad\Longrightarrow\quad
\bigl(dm^2\in\mathcal S\ \Longleftrightarrow\ 2\mid m\bigr).}
\tag{7.1}
\]

**Proof.** Since \(d\) is even, the integers

\[
u=d-1,\qquad v=d+1
\]

are positive and coprime. Their Group-1 theta coefficient is

\[
b=v^2-u^2=4d.
\]

The existing [explicit theta seed bounds](explicit-theta-seeds.md), together with the [universal rational-scale theorem](universal-rational-scales.md), compute a threshold \(C_\theta(u,v)\) such that every integer theta scale \(t\ge C_\theta(u,v)\) is attained. Set

\[
T(d)=C_\theta(d-1,d+1).
\]

These constructions therefore realize every count

\[
4dt^2=d(2t)^2,\qquad t\ge T(d).
\]

This proves membership for every even \(m\ge2T(d)\). The corresponding theorem above excludes every odd \(m\), with no size restriction, proving (7.1). ∎

This corollary combines the new arithmetic exclusions with an existing geometric construction; it introduces no new dissection. The threshold is effective and deliberately conservative. The corollary does not decide the finitely many even multipliers below \(2T(d)\), so it is an eventual classification rather than a complete classification of each square class.

## Appendix A. Infinitely many primes satisfy (1.2)

This appendix uses Chebotarev's theorem; the proofs of the individual exclusions do not.

Let

\[
F=\mathbb Q(i,\sqrt2,\sqrt3,\sqrt5),\qquad
L=F(\alpha),\quad\alpha=\sqrt[4]3.
\]

The independent rational square classes \(-1,2,3,5\) give \([F:\mathbb Q]=16\). The field \(\mathbb Q(\alpha)\) is a real quartic field with nonreal conjugates and is not normal. It cannot be a subfield of the abelian extension \(F/\mathbb Q\). Thus \([L:F]=2\) and \([L:\mathbb Q]=32\). The field \(L\) is Galois over \(\mathbb Q\), since it contains all roots of \(X^4-3\).

A prime \(p\equiv13\pmod{24}\) has Frobenius fixing \(i,\sqrt3\) and negating \(\sqrt2\). Write \(\varepsilon\) for its sign on \(\sqrt5\), and \(\eta\) for its sign on \(\alpha\). Since \(\alpha^2=\sqrt3\) is fixed, these signs are \(\pm1\), and reduction at an unramified prime gives

\[
\varepsilon=(5/p),\qquad
\eta\equiv3^{(p-1)/4}\pmod p.
\]

For each \(\varepsilon\), the corresponding automorphism of \(F\) has two lifts to \(L\), one for each \(\eta\). Condition (1.2) selects \(\eta=\varepsilon\), giving two automorphisms. Each is central: automorphisms commute on the abelian field \(F\), and any automorphism sends \(\alpha\) to \(\pm\alpha\) or \(\pm i\alpha\); the selected automorphisms fix \(i\), so they commute there too. Thus each is a singleton Frobenius conjugacy class. Chebotarev supplies infinitely many rational primes in these classes, proving the claim. A precise statement of the theorem is [M, Theorem 8.31].

## Sources and dependencies

- **[ALP]** J. Aguirre, Á. Lozano-Robledo, J. C. Peral, *Elliptic curves of maximal rank*, [author PDF](https://alozano.clas.uconn.edu/wp-content/uploads/sites/490/2014/01/ALP-2-23-07.pdf), §2, pp. 3–4. This records the standard 2-isogeny descent covers and their supported square classes. Our necessary-cover and local-obstruction proofs are included above.
- **[M]** J. S. Milne, *Algebraic Number Theory*, [author notes](https://www.jmilne.org/math/CourseNotes/ANTc.pdf), Theorem 8.31, for the optional Chebotarev infinitude argument.
- The [uniform-reduction proof](../research/uniform-reduction/PROOF.md), [uniform-sector proof](../research/uniform-sectors/PROOF.md), and [elliptic square classes](elliptic-square-classes.md), §4, supply the exhaustive necessary rows and the residue reduction. Those geometric inputs are not replaced by local descent.
- [F3 odd multipliers](f3-odd-multipliers.md) supplies the full parity correspondence and torsion discussion; only its necessary direction is used in the exclusion proofs and is reproduced here. [Square-class tails](square-class-tails.md), Appendix A, records the existing F3 geometric construction used to interpret coefficient witnesses.

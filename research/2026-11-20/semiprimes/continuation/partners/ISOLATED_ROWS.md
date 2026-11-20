# An explicit progression of primes with no distinct tiling partner

Write $T(n)$ when some triangle tiles with $n$ congruent triangles, allowing reflections and T-junctions. For every prime $P$ congruent to $19$ modulo $2184$ and every prime $Q$,
$$
T(PQ)\quad\Longleftrightarrow\quad Q=P.
$$
For example the only prime partner of 19 is 19. The conclusion uses the project's [older necessary overlist](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md) and [small-factor rules](../SIMULTANEOUS.md). It is independent of the two later moving-bank exclusions and of any scale-one decision for a residual F2 board.

In fact, let $P$ be *any* prime congruent to $19$ modulo $24$. The same conclusion holds whenever both positive integers
$$
A(P)=(P^2+6P+1)/4,\qquad B(P)=(3P^2+6P-1)/4
$$
are composite. This gives a sufficient test for a complete isolated row without enumerating partners.

**Proof.** Such a prime is 3 modulo 4. Its square occurs by the square grid; the small-factor rules exclude 2 and 3 as partners. The classical families produce no distinct prime partner. Any mixed-residue nonclassical partner would require 3 to be a square modulo $P$ by the [F2 matching theorem](PARTNERS.md). For a pair of primes both 3 modulo 4 with ratio strictly below 2, the only nonclassical option in the overlist has endpoints $2v^2-u^2$ and $3v^2-u^2$. If one of these equals $P$, reduction modulo $P$ forces 2 or 3, respectively, to be a quadratic residue: if $P$ divided $v$ it would also divide $u$, and its square would divide the endpoint. Quadratic reciprocity gives $(2/P)=(3/P)=-1$ for $P\equiv19\pmod{24}$.

Write $s<t$ for the remaining pair with $t>2s$, both primes 3 modulo 4. When $s=P$, the older overlist gives $t=A(P),B(P)$ or $(P^2+6P-3)/4$. The third is even and exceeds two. When $t=P$, the same three equations require, respectively,
$$
P+2=((s+3)/2)^2,\qquad P+1=3((s+1)/2)^2,\qquad P+3=((s+3)/2)^2 .
$$
The first and third are impossible modulo 8 (the residues are 5 and 6), and the middle equality is impossible modulo 3. This proves the test.

Finally $2184=24\cdot7\cdot13$. If $P\equiv19\pmod{2184}$ then $A(P)$ is divisible by 7 and $B(P)$ by 13, since $A(19)=119$ and $B(19)=299$. Both exceed these divisors for all $P\ge19$. The progression is coprime to its modulus, so Dirichlet's theorem gives infinitely many such primes. The same argument applies after independently choosing either root of the numerator of $A$ modulo 7 and either root of the numerator of $B$ modulo 13, while retaining $P\equiv19\pmod{24}$ and $P\ge19$.

A second immediate family covers prime endpoints $P\equiv5\pmod{12}$. For such a prime $T(PQ)$ holds precisely when $Q=2$ or $Q\equiv1\pmod4$. Indeed $P\equiv1\pmod4$ and 3 is a quadratic nonresidue, excluding F2. The sum-of-two-squares construction gives all the stated positive cases, and the small-factor rule handles $Q=3$.

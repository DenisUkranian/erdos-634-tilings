# A path structure for the constructible Paliy prime pairs

Direct an edge from the smaller prime $p$ to the larger prime $q$ if $p=2v^2-u^2$ and $q=3v^2-u^2$ for positive integers $0<u<v$. These are the prime pairs realized by the Paliy construction. The directed graph has indegree and outdegree at most one at every odd prime greater than 3, so on these vertices it is a disjoint union of paths and isolated vertices. Paths can in principle be infinite toward larger primes. In the interval $3<p<q<2p$, the [previously established prime-pair reduction](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md) shows that every nonclassical prime-product tiling lies on these paths or in the arithmetic F2 matching. Thus after removing pairs of primes both 1 modulo 4, the graph of actual tilings restricted to this ratio interval has maximum degree three.

**Proof.** For $d=2$ consider the smaller prime $P=2v^2-u^2$. For $d=3$ consider the larger prime $P=3v^2-u^2$. In both cases $z=u+v\sqrt d$ has norm $-P$ and positive first embedding. Since $u/v$ lies strictly between 0 and 1,
$$
1 < \frac z{\sqrt P}
  =\sqrt{\frac{\sqrt d+u/v}{\sqrt d-u/v}}
  <\sqrt{E_d},\qquad
E_2=3+2\sqrt2,\quad E_3=2+\sqrt3 .
$$
These are the smallest norm-one units above 1 in $\mathbb Z[\sqrt d]$. For $d=3$ this follows from the solution $2^2-3=1$. For $d=2$ the coefficient of $\sqrt2$ cannot be 1, and at coefficient 2 the solution is $3^2-2\cdot 2^2=1$. A positive norm-one unit has positive conjugate, so these observations also rule out units strictly between $1/E_d$ and 1.

For any two putative solutions $z_1,z_2$, each $v_i$ is invertible modulo $P$, since otherwise $P$ divides $u_i$ and $P^2$ divides the norm. The residues $u_i/v_i$ are square roots of $d$ modulo $P$. If the residues agree, $z_1\bar z_2$ has both coefficients divisible by $P$. Hence $z_1/z_2$ is an integral norm-one unit. It lies strictly between $1/E_d$ and $E_d$, so $z_1=z_2$. If the roots are opposite, $z_1z_2/P$ is an integral positive norm-one unit strictly between 1 and $E_d$, which is impossible. Thus a prime has at most one outgoing and at most one incoming edge. All edges increase, and their ratios exceed $3/2$, giving the path assertion. The degree bound uses the [separate F2 matching theorem](PARTNERS.md).

A prime can actually have two Paliy neighbors: $(u,v)=(1,4)$ gives $31\to47$, and $(u,v)=(5,6)$ gives $47\to83$. The F2 matching also has the arithmetic edge $47\leftrightarrow73$, whose geometric status is unresolved here. Thus the union of the Paliy paths and the arithmetic matching can have degree exactly three, even before any decision on that unit board.

The degree bound is sharp for **actual tilings** as well. The prime 1031 has Paliy neighbors 631 and 1607, from $(u,v)=(13,20)$ and $(11,24)$ respectively. Its F2 neighbor 1009 comes from $(a,b,c)=(351,329,589)$, since $351+2\cdot329=1009$ and $2\cdot351+329=1031$. The staircase parameters $(u,v,g)=(20,7,1)$ satisfy the [sharp constructive range](https://github.com/DenisUkranian/erdos-634-tilings/blob/ea420d780718a9e4a1801dfcb66c8f8975e48863/research/2026-11-20/semiprimes/staircase/SHARP_STAIRCASE.md). All three positive neighbors follow from constructions. All are strictly within the ratio interval, and all four displayed integers are primes by trial division through their square roots.

**Removing the ratio restriction under the recorded geometric inputs.** Section 5 of the [project's I120 theorem](https://github.com/DenisUkranian/erdos-634-tilings/blob/ea420d780718a9e4a1801dfcb66c8f8975e48863/research/2026-11-20/semiprimes/continuation/counting/inputs/I120_THEOREM.md) excludes the remaining same-residue nonclassical pairs with $q>2p$ using the unit isosceles and the adjacent BQ manuscript theorems. For mixed residues the prime-pair reduction already requires F2, hence $q<2p$. With these inputs the degree-three theorem and the complete three-partner list at 1031 hold over *all* distinct primes above 3. The original geometric inputs are internal research proofs; the norm and unit argument here is elementary and the interval version does not require either of those two moving-bank proofs.

Finally $1031\equiv3\pmod4$, so the [small-prime rules](https://github.com/DenisUkranian/erdos-634-tilings/blob/ea420d780718a9e4a1801dfcb66c8f8975e48863/research/2026-11-20/semiprimes/continuation/SIMULTANEOUS.md) exclude $2\cdot1031$ and $3\cdot1031$. Its own square is realized by a grid. With the stated inputs this yields the all-prime row
$$
T(1031r)\quad\Longleftrightarrow\quad r\in\{631,1009,1031,1607\}\qquad(r\text{ prime}).
$$

### A short independent check of the distant partners of 1031

For this particular row, the two moving-bank inputs in the preceding paragraph can be dispensed with. Section 2 of the [prime-product reduction](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md) gives a necessary arithmetic list when the larger prime exceeds twice the smaller. For odd primes $s<t$ with $s>3$ the three expressions for $4t$ are $s^2+6s+1$, $3s^2+6s-1$ and $s^2+6s-3$. At $s=1031$, the three proposed partners factor respectively as $137\cdot1951$, $23\cdot34729$ and $2\cdot107\cdot1249$. At $t=1031$, the three equations would require respectively $4132$, $1376$ or $4136$ to be squares. The first and third lie strictly between $64^2$ and $65^2$. The middle one lies strictly between $37^2$ and $38^2$. Thus the all-prime row for 1031 follows from the earlier arithmetic overlist, the proven constructions, and the small-prime rules alone. The argument does not use an impossibility claim for any unresolved F2 board.

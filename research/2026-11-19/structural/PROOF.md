# A large prime factor and delayed tilings in square classes

Write $G(N)$ when at least one nondegenerate Euclidean triangle admits a dissection into $N$ congruent triangles. Reflections and T-junctions are allowed. All statements below concern actual tilings. The proofs use the necessary count forms of Denis Paliy's reduction and two geometric boundary obstructions of Vico Bonfioli. This is a research note prepared with AI assistance. Its deductions have been checked internally. No external refereeing or Lean replay of its inputs is claimed.

## 1. An exact test in a sector of positive density

**Theorem 1.** Suppose $p\ge19$ is a prime congruent to $5$ or $19$ modulo $24$, $v_p(N)$ is odd, and $5N<9p^2$. Then
$$
 G(N)\quad\Longleftrightarrow\quad N=x^2+y^2\quad(x,y\in\mathbb Z).
$$
In particular, for $p\equiv19\bmod24$ every such input has a negative answer. The test on the right is equivalent to even multiplicity for every prime $3\bmod4$. No squarefreeness of $N$ or $N/p$ is required.

The subsection $p>\sqrt N$ of this test has natural density $(\log 2)/4$ amongst **all** positive integers $N$. Its $p\equiv19\bmod24$ part alone has density $(\log 2)/8$. These are densities of the stated input sets. Some were already covered by earlier results. The previous large-prime test in this project used $4p>3h^2+6h-1$ for $N=hp$. In the two stated residue classes the new interval includes all $1\le h<p$ and extends beyond it. [Previous test, §3](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/2026-11-19/continuation/RESULTS.md#3-большой-простой-делитель-при-произвольном-втором-множителе).

**Inputs and notation.** Outside the classical possibilities (sums of two squares including a zero square, $3t^2$, $6t^2$), the necessary form is $N=Dt^2$ with an integer $t\ge1$. For coprime $0<e<f$ set $b_0=f^2-e^2,\ Q=2f^2-e^2,\ P=3f^2-e^2$. The group with $3\alpha+2\beta=\pi$ gives $Q,P,b_0,b_0Q,QP$. The double-angle isosceles case gives $b_0$ with $f<2e$. The two $b_0$ rows have $t\ge2$. For coprime positive $a,b$ the minus norm $c^2=a^2-ab+b^2$ gives $ab$. The plus norm $c^2=a^2+ab+b^2$ gives
$$
 ab,\quad b(a+b),\quad b(a+2b),\quad (a+2b)(2a+b),\quad 3(a+b)(a+2b),\quad(a+b)(2a+b).
$$
Here $c$ is an integer and both orders of $a,b$ are allowed. Every sum of two squares occurs by the classical construction. [Paliy, §§1–4, including the attribution of the geometric inputs](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/uniform-reduction/PROOF.md) · [Beeson and Zhang, Table 1 and Theorem 1.2](https://arxiv.org/html/2604.01314v1).

**The two difference-of-squares rows.** Put $U=f-e,\ V=f+e$. In the double-angle row $t>\lceil e/U\rceil$ by Bonfioli's side obstruction. Since $0<U<e$, this gives $t\ge3,\ tU\ge f$. In the theta row, the word on the base gives nonnegative integers $x,y,z$ with $teb_0=xef+yb_0+zf^2$ and $z\ge f$. Reducing modulo $f$ shows $te-y=kf$ with $k\ge0$ and $k\le te/f$. Then $kb_0=xe+zf$, so $x\equiv kU\bmod f$. If $kU<f$, nonnegativity implies $x\ge kU$ and $z\le kU<f$, a contradiction. Therefore $teU\ge f^2$. In particular $t\ge4$ (since $4eU\le f^2$) and $tU\ge f$. These are necessary inequalities for the original geometric configurations. [Bonfioli, theta base-word proposition](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_primes_and_N200.tex#L255-L259) · [Bonfioli, double-angle obstruction D′ and its hypotheses](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v5_supplement.tex#L13-L19).

For either row and **any** prime $p\mid b_0$, one has $p\le V$ and $V=2f-U\le(2t-1)U$. Hence
$$
 N=t^2UV\ \ge\ \frac{t^2}{2t-1}\,p^2\ \ge\ \frac95p^2.
$$
The last inequality follows by factoring $5t^2-18t+9=(t-3)(5t-3)$.

**The norm rows.** For the specified residues both $2$ and $3$ are quadratic nonresidues modulo $p$. Primitivity implies $p\nmid QP$: if $p$ divides either factor then $p\nmid f$ and $(e/f)^2$ is $2$ or $3$ in $\mathbb F_p$. Thus $Q,P,QP$ cannot supply the odd valuation. For $D=b_0Q$ we must have $p\mid b_0$, whence $b_0\ge p$, $2f>p$, and $D>p^3/4$.

**The seven Eisenstein rows.** Write $A=\max(a,b)$, $B=\min(a,b)$ and $\sigma=\pm1$ for the sign in $c^2=A^2+\sigma AB+B^2$. All seven coefficients satisfy $D\ge AB$. In the plus case $p$ cannot divide $a+2b$ or $2a+b$ since either congruence forces $c^2$ to be $3$ times a nonzero square modulo $p$. The prefactor $3$ is coprime to $p$. Thus $p\mid D$ forces $p\mid A$, $p\mid B$, or (only in the plus case) $p\mid A+B$.

Take the reduced fraction $u/v=(c-A)/B$, with $v>0$. In the minus case $-1/2<u/v\le0$, and in the plus case $1/2<u/v<3/4$. These bounds follow by comparing the norm with $(A-B/2)^2,A^2$ or $(A+B/2)^2,(A+3B/4)^2$, respectively, using $B\le A$. Substitution and $\gcd(A,B)=1$ give
$$
 gA=v^2-u^2,\qquad gB=v(2u-\sigma v),\qquad
 g=\gcd(v^2-u^2,v(2u-\sigma v)).
$$
As $\gcd(g,v)=1$, $g$ divides $2u-\sigma v$. The identity $4(v^2-u^2)+(2u-\sigma v)(2u+\sigma v)=3v^2$ shows $g\mid3$. Therefore $A>v^2/8$ and $B\ge v$. The possible factor products are $(v-u)(v+u)$ for $gA$, $v(2u-\sigma v)$ for $gB$, and $u(2v-u)$ for $g(A+B)$ when $\sigma=+1$. Every factor in a relevant positive product has absolute value less than $2v$. It follows that $p<2v$ and
$$
                     D\ge AB>v^3/8>p^3/64 .
$$

**Conclusion and small primes.** An odd $v_p(N)$ forces an odd $v_p(D)$. For $p\ge116$, the preceding bounds exclude all nonclassical rows under $5N<9p^2$. The remaining primes in the theorem are $19,29,43,53,67,101$. The two difference rows and the two single norms are already excluded without a finite check. For each of the nine other rows it suffices to inspect $D\le\lfloor9p^2/5\rfloor$. In the first two product rows $f^2\le D$. In the seven norm rows $ab\le D$, so enumerate $1\le B\le\sqrt D$, $B\le A\le D/B$, reduce to coprime pairs, and check the norm by an integer square root. In the order above the six inspections cover respectively 76, 114, 178, 229, 294, 450 primitive ordered records. None has odd $p$-valuation. [Exact finite verification](verify.py) · [Recorded output](verification.json).

Finally $3t^2$ and $6t^2$ have even valuation at $p$. This proves the equivalence. For the density count, if $p>\sqrt N$ then $N=hp$ with $h<p$ and $p$ uniquely determined. Among $N\le X$ the count from $p\le\sqrt X$ is $O(X/\log X)$. For $p>\sqrt X$ the count, up to $O(X/\log X)$ from floors, is $X\sum_{\sqrt X<p\le X}1/p$ in the selected residue classes. The prime number theorem in arithmetic progressions and partial summation give $(\log2)/8$ per class after division by $X$. [Prime number theorem in progressions, Theorem 4.12](https://kskedlaya.org/ant/chap-primes-in-ap.html).

## 2. How late the first tiling can appear

**Corollary.** For every prime $p\equiv19\bmod24$, the first $m$ with $G(pm^2)$ satisfies $m>\sqrt{9p/5}$. Nevertheless $G(pm^2)$ holds for every sufficiently large $m$ for each fixed $p$. Odd $p$-valuation persists for every multiplier and $p>5$, so equality $5m^2=9p$ is impossible. Eventual existence follows from the known theta construction in each odd square class. Equivalently, one may take $(e,f)=((p-1)/2,(p+1)/2)$, for which $f^2-e^2=p$. [Square-class tail constructions](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/docs/square-class-tails.md).

**Theorem 2.** Let $0<\gamma<1/2$ be fixed. Among the odd squarefree positive integers $d$, the lower relative density of those satisfying
$$
                  \neg G(dm^2)\quad\text{for every integer }1\le m\le d^\gamma
$$
is at least $\log(2/(1+2\gamma))$. Each fixed odd squarefree $d$ eventually has a tiling at every sufficiently large multiplier.

**Proof.** Fix $1/2+\gamma<\alpha<\beta<1$. Write $d=hp\le X$ with $X^\alpha<p\le X^\beta$ prime, $h$ odd squarefree, and $h$ divisible by some prime $\ell\equiv19\bmod24$. Since $p>\sqrt X$, these choices are unique and $p\nmid h$. Almost every odd squarefree $h$ has such a divisor. For a finite set of these primes the density of odd squarefree integers avoiding them is $(4/\pi^2)\prod_\ell(1+1/\ell)^{-1}$ by the squarefree sieve. This tends to zero since their reciprocal sum diverges. The resulting asymptotic for $h\le X/p$ is uniform since $X/p\ge X^{1-\beta}$. Summing over $p$ and applying partial summation gives $(4/\pi^2)X\log(\beta/\alpha)+o(X)$ such $d$.

For every $m$ the odd valuation at $\ell$ excludes the classical cases and both single norm rows. For $m\le d^\gamma$ put $Y=X^{1+2\gamma}$. Now $p^2>Y$ for $X>1$, so neither difference row can give $dm^2\le Y$ by the bound of §1, applicable at every prime divisor of $b_0$. It remains possible to choose one of the nine product rows. Each such occurrence requires a $D\le Y$ with squarefree part exactly $d$, since $dm^2=Dt^2$.

There are $O(\sqrt Y)$ primitive product records in total. For $b_0Q$ write $\Delta=f-e$ and note $b_0Q\ge f^3\Delta$. For $QP$ one has $QP\ge f^4$. For the seven norm rows use the parameters above with $\Delta=2u-\sigma v$. Here $1\le\Delta\le v$, and $AB>v^3\Delta/24$. For fixed $v,\Delta,\sigma$, there is at most one $u$ and a bounded number of orderings and row labels. For both $b_0Q$ and the seven rows the count is thus bounded by a constant times $\sum_{v\ge1}\min(v,24Y/v^3)=O(\sqrt Y)$, splitting at $Y^{1/4}$. For $QP$ sum $f$ up to $Y^{1/4}$. This is Paliy's earlier product-row counting bound, with the short parametrization proof included to specify what is counted. [Paliy, Lemmas 5.1–5.2](https://github.com/DenisUkranian/erdos-634-tilings/blob/c18097f56242dd43aebb11e54f5a56cf6eeca49b/research/uniform-sectors/PROOF.md).

Discarding the squarefree parts of all these $D$ eliminates at most $O(X^{1/2+\gamma})=o(X)$ kernels at once, for every allowed $m$. Divide the surviving count by $(4/\pi^2)X+o(X)$ and let $\alpha\downarrow1/2+\gamma$ and $\beta\uparrow1$. This proves the claim. For example $\gamma=1/4$ gives a lower relative density of $\log(4/3)$.

Theorem 2 disproves an absolute bound on the number of initial multipliers requiring attention, even when restricted to odd kernels with a positive tail. The remaining structural question for arbitrary $N=dm^2$ is which small or intermediate multipliers actually occur as the primitive shape varies. A finite residual range for each primitive shape alone gives no globally finite set of exceptions.

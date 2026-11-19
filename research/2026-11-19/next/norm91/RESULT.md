# What a fixed square factor decides for every sufficiently large prime

Denote triangular tilability by $G(N)$. All targets allow reflections and arbitrary T-junctions. The conclusions use Bonfioli’s run and construction theorems and the [fixed rational rotations](../global/NORM_ROTATION.md). The fixed scale 91 below was chosen to work in both real quadratic fields.

**Prime statement.** For every prime $p>2197$,
$$G(91^2 p)\quad\Longleftrightarrow\quad p\not\equiv19\pmod{24}.$$
In fact every prime outside the class $19\bmod24$ works at every size. Inside that class, $p=19$ works and 40 smaller prime inputs are still undecided by the tests recorded here. The accompanying [exact list](prime_row.json) includes their possible geometric parameters. This finite remainder is specific to this one prime row.

**Positive direction.** The cases $2,3$ and $p\equiv1\bmod4$ have classical tilings. Among the remaining primes outside $19\bmod24$, primes $7,23\bmod24$ are norms $2v^2-u^2$ and primes $11\bmod24$ are norms $3v^2-u^2$. This follows from the quadratic residue and sign conditions in the [norm proof](../global/NORM_ROTATION.md). For the first norm use the denominator 7 rotation there with residual scale $91/7=13\ge11$. For the second use denominator 13 with $91/13=7\ge5$. Increasing the total and residual scales only enlarges the interval where the construction applies. For a primitive pair with $u=1$ or $v-u=1$, the interval inequalities force the scale to be at least $v$ and the earlier all-scales construction applies. A common divisor of transformed coordinates increases the available scale.

**A closed formula for the theta base-word test.** Let $e<f$ be positive coprime integers, $b=f^2-e^2$, and $t\ge1$. Bonfioli’s necessary base condition is the existence of nonnegative integers $x,y,z$ with
$$teb=xef+yb+zf^2,\qquad z\ge f.$$
It is equivalent, as an arithmetic condition, to
$$\left\lfloor\frac{te}{f}\right\rfloor\ge \left\lceil\frac{f}{f-e}\right\rceil.$$
To see this, reduce the equation modulo $f$. This gives $te-y=kf$ for a positive integer $k\le\lfloor te/f\rfloor$. Dividing by $f$ and reducing again gives $x=lf-ke$ and $z=kf-le$ for an integer $l$. If $k(f-e)<f$, then $x\ge0$ forces $l\ge k$ and $z\le k(f-e)<f$, a contradiction. Conversely choose $k=\lceil f/(f-e)\rceil$, $l=k-1$ and $y=te-kf$. Then $x=k(f-e)-f\ge0$ and $z=k(f-e)+e\ge f$. The word test is necessary for a tiling. Sufficiency established here concerns the integer equation only. [Bonfioli, Proposition “Word of the base of theta”](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_primes_and_N200.tex)

For every passing tuple $f/(f-e)\le te/f$, so $t(e/f)(1-e/f)\ge1$ and $t\ge4$. The least possible $k$ satisfies $k\le t-2$. Indeed $k\le t-1$, and $k=t-1$ would require both $f\le(t-1)(f-e)$ and $f\ge t(f-e)$. Consequently $(f+e)/(f-e)\le 2t-5$. The upper bound for the ratio is attained in the word equation at $e=t-3,\ f=t-2$ for every $t\ge4$. At scale four only $e/f=1/2$ is possible.

**Negative direction.** For $p\equiv19\bmod24$, $91^2p\equiv19\bmod24$. Paliy’s residue reduction permits only the theta and double-angle rows. Their counts are $t^2(f-e)(f+e)$, with $t\ge2$. Also $p$ is different from 7 and 13, so $t\in\{7,13,91\}$. In the theta row the ratio above is at most $2t-5$. In the double-angle row Bonfioli’s Theorem F implies $e\le(t-1)(f-e)$, hence the ratio is at most $2t-1$. The larger of the factors $f-e,f+e$ is at least $p$, and the smaller is at most $(91/t)^2$, since their product is $p(91/t)^2$. Therefore
$$p\le(2t-1)(91/t)^2\le13\cdot13^2=2197.$$
For $p=19$ the theta parameters $e=9,f=10,t=91$ exceed the explicit notch threshold 68. The code checks all divisors and records the 40 remaining primes. [Residue reduction, after Theorem A](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/uniform-reduction/PROOF.md) · [Bonfioli, Theorem F](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_primes_and_N200.tex) · [Notch threshold](../../nov19/powers/POWERS.md)

**Large prime factor, with arbitrary cofactor.** For any $h\ge1$ put $H=91^2h$ and $B(H)=(3H^2+6H-1)/4$. For every prime $p>B(H)$, the following gives an exact prime-factorization criterion for $G(91^2 hp)$. At least one of the following conditions on $n=hp$ must hold.

- All primes $3\bmod4$ have even valuation (a sum of two squares), or the squarefree kernel is 3 or 6.
- All odd primes inert in $\mathbb Q(\sqrt2)$ have even valuation.
- All odd unramified primes inert in $\mathbb Q(\sqrt3)$ have even valuation, and $(-1)^{v_3(n)+1}n/3^{v_3(n)}\equiv1\bmod3$.

For necessity, the [large-prime bound](../../continuation/RESULTS.md) removes every nonclassical geometric row except W and beta. A square multiplier preserves all the listed norm tests for these two fields, including the 3-adic sign condition. For sufficiency the local tests give an integral signed norm representation by the principal-ideal and unit argument in [the norm proof](../global/NORM_ROTATION.md), followed by the same two rotations at 91. The classical condition gives its usual construction. The proof uses only the stated size restriction on $p$.

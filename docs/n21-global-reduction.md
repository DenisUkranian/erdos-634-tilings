# An exhaustive reduction of N=21 to one exact geometric instance

29 September 2026. Computer-assisted theorem with an explicit source dependency ledger and a separate exact geometric replay. No external refereeing, proof-assistant formalization, or priority claim is made.

**Theorem.** No triangle can be dissected into 21 congruent triangles, allowing reflections and arbitrary T-junctions.

The argument below reduces every classified shape to the single instance with tile `(2,3,4)` and target `(12,12,21)`. The [391-state geometric certificate](alpha-21-obstruction.md), checked by a separate implementation, excludes that instance.

**Attribution.** This count was already reported excluded by Vico Bonfioli and Jan Philipp Harries. Beeson [1206.2229v4](https://arxiv.org/abs/1206.2229v4), §§14.3 and 15, records their computational reports; his conclusion explicitly leaves the result unendorsed pending verification. The present contribution is an independent compact certificate, its separate exact replay, and an explicit exhaustive reduction. It is not a claim to have first excluded 21.

**Proposition.** Suppose some triangle can be dissected into 21 congruent triangles. Under the exhaustive source classification listed in the repository's [source dependency ledger](prime-case-dependencies.md), and the two-character theta necessary form proved in [the theta note](theta-branch.md), the tiling must, after scaling, consist of 21 copies of the $(2,3,4)$ triangle inside the triangle with sides $(12,12,21)$.

The exact refutation of this instance supplies the final step. No W or beta scale-one geometric exclusion candidate is needed in this reduction.

## Exhaustive shape inputs

Use the same source classification as the prime dependency ledger:

- Laczkovich's triangle-shape classification and the equilateral classification;
- the reptiling classification;
- Beeson, `1206.1974v7`, Theorems 7.8 and 11.7 for a non-equilateral isosceles target with a right tile or with $\gamma=2\alpha$;
- Beeson, `1206.2229v4`, rationality and the five $3\alpha+2\beta=\pi$ shapes;
- the rationality of nonsimilar irrational-angle $120^\circ$ tiles (Beeson–Zhang, `2604.01314v1`, Theorem 1.1) and the four scalene target formulas;
- the equilateral rationality input of Beeson, `1812.07014v3`.

The [independent global audit](audits/n21-global.md) records the primary sources and theorems checked afresh, including the composite-safe right-tile and double-angle restrictions.

The exact direction characters used below are derived in [the equilateral invariant note](n105-partial-results.md) and [the 120-degree invariant note](isosceles-120-invariant.md); their internal-edge cancellation works at arbitrary T-junctions. The flux formulas are not an edge-to-edge assumption.

## 1. Classical and special isosceles branches

The count 21 is neither a square, three times a square, nor a sum of two integer squares. Thus it is not a reptiling count. For a rational-angle equilateral tiling, the possible count forms are a square or $2,3,6$ times a square; none equals 21.

A nonsimilar right tile in a non-equilateral isosceles target would force a square or an even count by Theorem 7.8. A $\gamma=2\alpha$ tile would force a nonsquarefree count by Theorem 11.7. Since 21 is odd, nonsquare, and squarefree, both branches disappear.

## 2. Equilateral targets with irrational angles

After rationality and primitive normalization, write the tile sides as $a,b,c$, with $c$ opposite the $60^\circ$ or $120^\circ$ angle, and the equilateral target side as $S$. The two signed direction characters give positive integers $s,t$ satisfying $st=3N=63$.

For a $60^\circ$ tile,

$$
s=\frac{3S}{a+b+c},\qquad t=\frac{3S}{a+b-c},
$$

and the rational quantity $2S(a-b)/(ab)$ has square

$$
(t-s)^2-4N.
$$

An integer which is a rational square is an integer square. Interchanging $a,b$ is immaterial; order $s\le t$. The only pairs $(s,t)$ are $(1,63),(3,21),(7,9)$, with radicands

$$
3760,\qquad240,\qquad-80.
$$

None is a square.

For a $120^\circ$ tile the analogous radicand is

$$
(t-s)^2+16N,
$$

giving

$$
4180,\qquad660,\qquad340.
$$

These lie strictly between $64^2$ and $65^2$, between $25^2$ and $26^2$, and between $18^2$ and $19^2$, respectively. Thus no equilateral branch survives. The finite list comes from factoring 63, not from a bounded enumeration of possible tile sides.

## 3. The five rational $3\alpha+2\beta=\pi$ shapes

Write

$$
(a,b,c)=(uv,v^2-u^2,v^2),\qquad0<u<v,\quad\gcd(u,v)=1,
$$

and $Q=2v^2-u^2$, $P=3v^2-u^2$.

- **Theta-isosceles.** The strengthened necessary form is $N=bT^2$ with $T$ integral. Since 21 is squarefree, $T=1$ and both equal sides have length $vb$. The apex angle $\alpha$ is covered by exactly one tile angle $\alpha$: irrationality and $3\alpha+2\beta=\pi$ exclude every other nonnegative combination of tile angles. That tile places a $b$-edge on one equal side. If $B$ is the number of boundary $b$-edges on that side, its length equation modulo $v$ gives $B\equiv0\pmod v$, since $a,c$ are divisible by $v$ and $\gcd(b,v)=1$. Thus $B\ge v$, already using the entire side length $vb$; the side consists only of $b$-edges. Each such edge has a $\gamma$-angle at one endpoint. No target corner can receive $\gamma$, and no straight boundary vertex can receive two copies of the obtuse angle $\gamma$. A side made of $B$ edges has only $B-1$ internal vertices, so its $B$ gamma angles cannot fit. This contradiction uses only this one-edge-type pigeonhole argument, not the stronger two-$c$-edge bound.
- **W.** Its count is $QT^2$, so $Q=21$. Under coprimality, $2v^2-u^2$ modulo 8 is one of $1,2,6,7$, never $5=21\pmod8$.
- **Beta-isosceles.** Its count is $PT^2$, so $P=21$. Since $P>2v^2$, only $v=2,3$ are possible. The coprime pairs $(u,v)=(1,2),(1,3),(2,3)$ give $P=11,26,23$.
- **Other scalene.** Its count is $QPK^2$. The smallest possible product is $7\cdot11=77$ at $(u,v)=(1,2)$; the factors increase with $v$ even at their minimum $u=v-1$. Thus the count exceeds 21.
- **Alpha-isosceles.** Its count is $bQK^2$, so $K=1$ and $bQ=21$. Here $b>1$, $Q>b$, and $\gcd(b,Q)=1$. Thus $(b,Q)=(3,7)$. The identities $v^2=Q-b$ and $u^2=Q-2b$ give $(u,v)=(1,2)$. The tile is $(2,3,4)$ and the target sides are $(bc,bc,bQ)=(12,12,21)$.

Only the claimed instance remains in this angle family.

## 4. Nonsimilar irrational 120-degree tiles on other targets

Normalize the tile to a primitive positive integer triple

$$
c^2=a^2+ab+b^2.
$$

It has pairwise coprime sides. First, $a+b\ge8$: direct enumeration of the finitely many positive pairs with sum at most 7 gives no primitive integer $c$ (this elementary bound is replayed exactly by the attached script).

### 4.1 Isosceles targets

Up to interchanging $a,b$, the primitive target sides are $k(c,c,a+2b)$, and

$$
21b=k^2(a+2b).
$$

Since $\gcd(b,a+2b)=1$, the positive integer $A=a+2b$ divides 21. Take $A\in\{1,3,7,21\}$ and $1\le b<A/2$, with $a=A-2b$. The condition $k^2=21b/A$ leaves only:

| $A$ | $a$ | $b$ | $k$ | $a^2+ab+b^2$ |
|---:|---:|---:|---:|---:|
| 7 | 1 | 3 | 3 | 13 |
| 21 | 19 | 1 | 1 | 381 |
| 21 | 13 | 4 | 2 | 237 |
| 21 | 3 | 9 | 3 | 117 |

No last-column entry is a square. Hence no isosceles target survives.

### 4.2 The four scalene targets

The primitive side proportions and integer-scale area formulas are reproduced in the prime dependency ledger. Three of the counts have the forms

$$
3\lambda^2(a+2b)(a+b),\qquad
\lambda^2(2a+b)(a+b),\qquad
\lambda^2(a+2b)(2a+b).
$$

Each exceeds 21 because $a+b\ge8$ and the other linear factors exceed $a+b$.

For the remaining F1 target the primitive side proportions are $(a,c,a+b)$, with integral scale $k$, and

$$
21b=k^2(a+b).
$$

Thus $a+b$ divides 21. Enumerate its four divisors and use $k^2=21b/(a+b)$ together with $c^2=a^2+ab+b^2$. The unique primitive structural candidate is

$$
(a,b,c;k)=(5,16,19;4).
$$

It fails the signed-direction integrality condition

$$
M_\alpha=\frac{k(2a+b-c)}{c+a-b}
        =\frac{4(10+16-19)}{19+5-16}
        =\frac{28}{8}\notin\mathbb Z.
$$

Therefore the last $120^\circ$ branch is excluded as well.

## 5. Exact replay and remaining dependency

[check_n21_reduction.py](../scripts/check_n21_reduction.py) checks the factor pairs, all finite side enumerations, the unique F1 candidate and its failed flux, the beta parameter list, and the unique alpha candidate. It uses integer arithmetic only and rejects optimized Python mode. Its output is [n21-reduction.json](../verification/n21-reduction.json).

The script is a replay of the finite arithmetic in this proof. Exhaustiveness comes from the cited shape classification and the proved formulas. The final geometric exclusion is supplied by [alpha-21-obstruction.md](alpha-21-obstruction.md) and [its independent audit](audits/alpha21.md). The checker confirms every branch by exact rational arithmetic. The theorem depends on the stated published shape and rationality inputs; the two new universal scale-one candidates used elsewhere in this repository are not dependencies.

From the repository root:

```bash
python3 scripts/check_n21_reduction.py
python3 scripts/verify_alpha21.py
```

The first command checks the finite arithmetic; the second checks the complete geometric refutation. Neither command is a formal verification of the cited classification theorems.

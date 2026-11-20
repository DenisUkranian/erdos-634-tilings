# Three consecutive tiling scales imply a signed tiling at scale one

Let $T$ be a nondegenerate triangle and $K$ a fixed tile. Indicator identities below hold almost everywhere. An **integral signed tiling** is an expression of a region's indicator as a finite sum of indicators of admissible placements of $K$ with integer coefficients. Coefficients may be negative. Admissible placements must be closed under translations. They may allow reflections or have restricted orientations.

**Theorem.** If $nT,(n+1)T,(n+2)T$ admit integral signed tilings for one integer $n\ge1$, then every positive integer dilate of $T$ admits an integral signed tiling. In particular, three ordinary tilings at consecutive scales suffice.

Translate the vertices of $T$ to $0,u,v$. Write $X,Y$ for translation of indicator functions by $u,v$. Let $D$ be the triangle with vertices $u,v,u+v$. For integer $j\ge0$, put

$$
H_j=\sum_{i,k\ge0,\ i+k\le j}X^iY^k,\qquad H_j=0\quad(j<0).
$$

The usual grid in $mT$ gives

$$
S_m=\mathbf 1_{mT}=H_{m-1}\mathbf 1_T+H_{m-2}\mathbf 1_D \qquad(m\ge1).
$$

At scale two this gives three translates of $T$ and one copy of $D$. The generating function of the translation operators is

$$
\sum_{j\ge0}H_j t^j=\frac1{(1-t)(1-Xt)(1-Yt)}.
$$

Comparing coefficients yields the indicator identity

$$
 S_{m+3}=(1+X+Y)S_{m+2}-(X+Y+XY)S_{m+1}+XY S_m\qquad(m\ge1).
$$

All these translations commute and have inverses. Finite integral signed sums of permitted tile indicators form a translation-invariant additive subgroup. Any three consecutive $S$'s in this subgroup yield the preceding $S$ by applying the inverse translation $(XY)^{-1}$. They yield the next $S$ directly. Induction proves the theorem for every positive integer scale.

**Application to mixed semiprimes.** For primitive $a,b,c>0$ with $c^2=a^2+ab+b^2$, let $K$ have sides $a,b,c$. The F2 target $T$ has sides $a(a+2b),b(2a+b),c^2$. Eventual ordinary tiling for the same triangle and tile at all sufficiently large integer scales supplies the three-scale hypothesis. Thus every scale-one board in the residual F2 branch has an integral signed tiling, including the boards of area $3431$ and $5063$ in tile units. This application uses the scale and side conventions of the [prime-product reduction](../../README.md) and [Zhang, Theorem 7](https://arxiv.org/pdf/2512.22696). If the large tilings use directions outside a prescribed band, this argument only gives the unrestricted conclusion.

**Consequence for obstructions.** Every additive homomorphism on the group of polygon indicators up to measure zero with values in any abelian group that vanishes on every admissible tile placement also vanishes on $T$. The homomorphism itself need not be translation invariant. Its values may depend on position or be taken modulo a prime. The same applies to an additive boundary operator respecting these indicator identities. Thus an unrestricted linear inconsistency for translated and reflected tile indicators cannot exclude either target. Nonnegativity, confinement to the unit triangle or additional nonlinear conditions can still give obstructions. Ordinary tileability at scale one remains undecided by this argument. For a restricted collection of tile orientations one must verify the three-scale hypothesis with that restriction.

## Exact three-scale certificates for 3431 and 5063

For both boards one may take $n=2$. Write $T$ with vertices $0,u,v$, where in axial coordinates $u=(b(2a+b),0)$ and $v=(0,a(a+2b))$. A compressed certificate for $\mathbf1_T$ consists of seven translated large boards:

| Scale | Coefficient | Translations of the corresponding board |
|---:|---:|---|
| 4 | $+1$ | $-u-v$ |
| 3 | $-1$ | $-u-v,-v,-u$ |
| 2 | $+1$ | $-v,-u,0$ |

These entries are the $m=1$ recurrence solved for $S_1$. Use the ordinary [scale-two coordinates](../../controls) and the [scale-three and scale-four generators](../../controls/dilation.py). Reference boards keep the same tile and the same normalization of $u,v$ at all three scales. The checker verifies their coordinates, counts and congruence with the independent [grid checker](../../controls/verify_grids.py). It verifies the seven translated board indicators separately on every up and down cell of the unit triangular grid.

| Unit board | Scale 2 | Scale 3 | Scale 4 | Positive tile copies | Negative tile copies | Difference |
|---:|---:|---:|---:|---:|---:|---:|
| 3431 | 13,724 | 30,879 | 54,896 | 96,068 | 92,637 | 3,431 |
| 5063 | 20,252 | 45,567 | 81,008 | 141,764 | 136,701 | 5,063 |

Counts include multiplicities before any cancellation between coincident opposite-sign placements. Run the checker with assertions enabled from any directory:

~~~sh
python3 check_signed.py
~~~

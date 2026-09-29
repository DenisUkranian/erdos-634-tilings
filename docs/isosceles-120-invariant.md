# The isosceles 120° branch: a prime-count obstruction

29 September 2026. This note records the signed-direction argument attributed to Vico Bonfioli, with the elementary arithmetic written out. It is a component of the [global prime-case deduction](prime-case-dependencies.md), not a solution of the full composite-count problem. T-junctions and reflected tiles are allowed.

## Source ledger

- Beeson, *Tilings of an Isosceles Triangle*, [arXiv:1206.1974v7](https://arxiv.org/abs/1206.1974v7), Theorem 12.5 for rationality in the isosceles 120° branch.
- Beeson–Zhang, *Rationality of certain triangle tilings*, [arXiv:2604.01314v1](https://arxiv.org/abs/2604.01314v1), Theorem 1.1, supplying the current independent rationality input.
- Vico Bonfioli, *A signed-direction invariant for triangle tilings*, [repository commit 4bb61193bafa4471f7ba3a35324ae0f70bd2177c](https://github.com/ElVec1o/erdos_634_proof/tree/4bb61193bafa4471f7ba3a35324ae0f70bd2177c), [Zenodo v3.2](https://doi.org/10.5281/zenodo.22721069). The argument reproduced below is credited to this source; its broad prime claims are not used as inputs.

## Proof

Let the primitive integer tile be `(a,b,c)` with angles `(α,β,2π/3)` and α/π irrational. Rationality follows from the cited Beeson–Zhang theorem; the isosceles specialization is also recorded in the cited Beeson manuscript. Thus

$$
c^2=a^2+ab+b^2,
$$

and a,b,c are pairwise coprime. Also `3∤c`: otherwise reduction modulo3 gives `a≡b mod3`; writing `a=b+3h` gives `c²=3b²+9bh+9h²`, whence `3|b`, contrary to primitiveness. Any prime dividing both c and a+2b would, by substitution into the cosine equation, divide `3b²`, and hence be 3. Thus `gcd(c,a+2b)=1`. The possible isosceles base angle is α or β; swap a,b and α,β to take α. Its side proportions are `(c,c,a+2b)`, now seen to be primitive, so the actual target sides are `k(c,c,a+2b)` with positive integer k: every target side is an integer sum of tile edges. Area gives

$$
N=\frac{k^2(a+2b)}b.
$$

Since `gcd(a+2b,b)=1`, the integer `k²/b` multiplies `a+2b>1` to give the prime N. Hence `k²=b` and `N=a+2b`.

All directed tile-edge directions, after fixing a reference edge, lie in `G=Z·π/3+Z·α`, modulo `2π`. Irrationality makes

$$
f(j\pi/3+\ell\alpha)=(-1)^j
$$

well-defined. Give an oriented segment of length L the weight `L f(direction)`. Reversing direction negates the weight. Subdividing all edges at all intersections and T-junctions makes each interior subsegment cancel with its opposite orientation. Thus the sum of tile boundary weights equals the target boundary weight. Each tile contributes `±(c+a−b)`. The target contributes `k(a+2b−2c)`. Consequently

$$
\frac{k(a+2b-2c)}{c+a-b}=\frac{c-a-b}{k}\in\mathbb Z,
$$

where the equality uses `k²=b` and the cosine equation. Therefore `k | (a+b−c)`.

But `a<c<a+k²`, so this divisibility would imply `c=a+kr` with `1≤r≤k−1`. Substitution gives

$$
a(2r-k)=k(k-r)(k+r).
$$

As `gcd(a,k)=1`, we have `k|2r`. Its only possible value in `2≤2r≤2k−2` is `2r=k`. The displayed equation would then have zero left side and positive right side, a contradiction. (For k=1 there is no integer r at all.) This proves the branch exclusion while explicitly permitting T-junctions.


## Scope

Rationality and the possible target angles are external classification inputs. The cancellation and arithmetic argument are reproduced here for inspection. This is an internal exposition of the credited invariant, not a claim of novelty, independent referee acceptance, or formal proof-assistant verification.

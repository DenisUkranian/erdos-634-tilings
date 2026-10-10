# An exact one-candidate reduction for every count `N=2p`, `p≡7 (mod 8)`

**Erdős Problem 634 — research note, 9 October 2026**  
Research directed by Denis Paliy, with ChatGPT assistance.  
**Status:** mathematical derivation based on the published angular/rationality classification and the existing two-whole-long-edge lemma. Internal arithmetic regressions are not external peer review. The general Erdős 634 problem is not solved. **No priority claim** is made.

## Theorem A (global one-candidate reduction)

Let `p` be a prime with `p≡7 (mod 8)`, and let `N=2p`. After the standard published angular classification, rationality normalization, and necessary integer scales, *every* tiling with count `N`, if one exists, must be of the Group-1 W type at residual scale 1, by a **uniquely determined primitive pair** `0<u<v`. The pair is the unique solution of

```
2v²−u² = 2p,   gcd(u,v)=1, 0<u<v,
```

and necessarily `u=2x` is even, `v` is odd, and

```
v²−2x² = p,  0<x<v/2.
```

There is exactly one such pair for every prime `p≡7 (mod 8)`. Consequently the global existence decision for `N=2p` is equivalent to one specific primitive scale-one W tiling problem; no other classified shape or tile can realize the same count. This does **not** decide whether that W tiling exists in general.

### Proof: isolation among all angular branches

`N≡14 (mod 16)` and `3∤N`. The exhaustive 13-branch residue audit in [F3 global overlap, Theorem 1.1](https://github.com/DenisUkranian/erdos-634-tilings/blob/main/docs/f3-global-overlap.md) leaves only Group-1 W and F3 at residue 14 modulo 16. F3 coefficients are all divisible by 3 and are therefore excluded. Classical counts are excluded by the same modular audit. Thus W is mandatory. Every W count has form `(2v²−u²)m²` with coprime `0<u<v` and positive integer `m`. Squarefreeness of `N=2p` forces `m=1`.

Now `2v²−u²=2p≡2 (mod 8)`. Primitivity forces `v` odd and `u` even. Writing `u=2x` gives the positive Pell-type norm equation displayed above. Conversely every solution `v²−2x²=p` with `0<x<v/2` gives a primitive W candidate: a common divisor of `v` and `2x` would have square dividing the prime `p`.

### Proof: uniqueness and existence of the reduced norm representation

Work in the norm-Euclidean ring `R=Z[√2]`, with norm `Norm(v+x√2)=v²−2x²`. One elementary reason `R` is norm-Euclidean is that coefficient-wise rounding of an element of `Q(√2)` to its nearest integral coefficients gives a difference `r+s√2` with `|r|,|s|≤1/2`, hence `|r²−2s²|≤1/2<1`. Therefore `R` has unique factorization. Its positive norm-one units are powers of `ε=3+2√2=(1+√2)²`. (The smallest norm-one unit above 1 is `ε`, and division by powers of `ε` reduces any such unit to 1.)

Because `p≡7 (mod 8)`, the supplementary law for 2 gives `(2/p)=1`; hence the ideal `(p)` splits into two conjugate prime ideals in `R`. As `R` is principal, this provides an algebraic integer of norm `±p`. Multiplying by the norm-minus-one unit `1+√2` if needed gives norm `p`. Changing the overall sign if necessary makes both real embeddings positive.

Let `α=v+x√2` have norm `p`. The inequalities `x>0, v>2x` are equivalent to

```
1 < α/√p < √ε = 1+√2.
```

Indeed, `α·conj(α)=p`; the ratio is `sqrt((v+√2x)/(v−√2x))` and `0<x/v<1/2` is precisely the stated interval. Given any totally positive generator of norm `p`, multiply it by `ε^j` to place `α/√p` between 1 and `ε`. If it lies above `√ε`, replace it by `ε·conj(α)`, whose ratio is `ε/(α/√p)`; this lies between 1 and `√ε`. Equality at an endpoint would force a prime `p` to be a square, so cannot occur. Hence at least one reduced representation exists.

For uniqueness, suppose two reduced generators `α₁,α₂` have norm `p`. Since `p` is prime and `R` is a UFD, either `α₁=ε^jα₂` or `α₁=ε^j conj(α₂)`. In the first case their ratio is strictly between `1/√ε` and `√ε`, so `j=0` and they are equal. In the second case

```
1 < α₁α₂/p < ε,
```

but `α₁α₂/p=ε^j`, impossible because no integral power of `ε>1` is smaller than `ε`. Thus the reduced representation, and so `(u,v)`, is unique. QED.

## Theorem B (an explicit parametric global exclusion)

**For every integer `k≥1` such that `p=8k²−1` is prime,**

```
N=16k²−2
```

**cannot be the number of congruent triangles in a dissection of any triangle.**

**Proof.** Set `v=4k−1`, `u=4k−2`; then `0<u<v`, the pair is coprime, and

```
2v²−u² = 16k²−2 = 2p.
```

Theorem A proves that this is the **only** possible tile/target branch and pair, with scale one. The previously proved [two-whole-long-edge boundary theorem](https://github.com/DenisUkranian/erdos-634-tilings/blob/main/research/group1-continuation/PROOF.md) says that every exterior side of any primitive W target must contain at least two whole edges of length `c=v²`. But for this pair `u=v−1`, the W side `vb=v(v²−u²)=v(2v−1)=2v²−v` is **strictly shorter than `2c=2v²`**. Hence this unique W target is impossible. All classified alternatives were excluded in Theorem A. QED.

The theorem is conditional on primality of `8k²−1`; **infinitude of such primes is not proved here**, and therefore no unconditional infinitude claim for these excluded counts is made.

## Illustrative unconditional numerical consequences

The following members have a directly checkable prime `p=8k²−1`:

| k | p | N=2p | unique W (u,v) |
|---:|---:|---:|---|
| 1 | 7 | 14 | (2,3) |
| 2 | 31 | 62 | (6,7) |
| 3 | 71 | 142 | (10,11) |
| 4 | 127 | 254 | (14,15) |
| 5 | 199 | 398 | (18,19) |
| 9 | 647 | 1294 | (34,35) |

Other members are tested by `verify_prime_sector.py`. The numerical program independently enumerates all primitive coefficient representations in this restricted class and checks primality. Its finite PASS is a regression, not the justification for the universal quantifiers.

## What this does and does not solve

- **Closes a family of global negative counts**, contingent on an explicit, decidable primality condition; each displayed example is unconditional. Their nonexistence concerns all permitted triangle shapes and tilings, not just a selected W geometry.
- **Reduces every `N=2p` with prime `p≡7 (mod 8)` to exactly one W scale-one instance.** Some of these remaining instances (e.g. `p=23`, `N=46`, with `(u,v)=(2,5)`) survive the two-long-edge obstruction; Theorem A does not decide them.
- **Does not establish infinitely many excluded counts through Theorem B**, because infinitude of primes of the form `8k²−1` is not known from this argument.
- **Does not use** the unreviewed scale-one W/β candidate, an all-primes claim, or a negative inference from a timed-out solver.

For a complete Erdős 634 classification one still needs genuine geometric existence or impossibility criteria for the unbounded primitive parameter families, including this uniquely reduced prime sector and F3 cases such as 14430.

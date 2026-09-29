# Independent verification of odd theta tilings and the resulting scale theorem

29 September 2026. Internal mathematical audit, with an exact geometric replay independent of the construction generator. No claim of priority, external refereeing, or a solution of all of Erdős problem 634.

The two-c-edge proof and small-case exclusions are given in [the theta-branch report](../theta-branch.md). This audit verifies the odd constructions and the subsequent stronger conclusion.

**Subsequent update, same date.** This audit records the earlier 147/243
stage. The [75-tile construction](../theta-75-construction.md) has since
passed the same separate checker on all 2,775 pairs. The exception at
`t=5` below is therefore resolved: the complete fixed-tile spectrum is
`N=3t²` for every integer `t>=4`. The [two-character argument and eventual
theorem](../eventual-rational-families.md) also establish the necessary
form `N=bT²` without assuming b squarefree. The earlier audit is retained
below to show which arguments were checked at that stage.

## 1. Accepted results

The explicit constructions with tile `(2,3,4)` and theta-isosceles targets pass this audit:

| Tile count | Target sides | Coloring number M | Scale µ=X/c |
|---:|---|---:|---:|
| 147 | (21,42,42) | 7 | 21/2 |
| 243 | (27,54,54) | 9 | 27/2 |

Here X is either equal target side. The apex is α and the base angles are `θ=α+β`. Indeed the target apex has cosine `1−(1/2)²/2=7/8`, which is also the cosine of the tile angle opposite its side 2.

Consequently:

1. **Lemma 55 of Beeson `arXiv:1206.2229v4`, as printed, has a concrete counterexample.** This is stronger than the previously identified unsupported proof step.
2. For this fixed tile and target shape, **every count `3t²` with integer `t≥4`, except possibly `t=5`, is realized**.
3. The earlier area and boundary arguments exclude every other count except `N=75`: the only unresolved instance of this fixed branch is target `(15,30,30)` tiled by 75 copies of `(2,3,4)`.
4. A general mixed-strip construction gives the explicit eventual bound in Section 6 for all primitive tiles satisfying a stated geometric inequality.

None of these statements classifies all target shapes for this tile, all primitive tiles in the theta branch, or all integers in the original problem.

## 2. Exact independent replay

The script `scripts/verify_theta_odd.py` reads the stored certificates directly. It does not import or call the author's generator or its separating-axis verifier. Coordinates `(x,y)` in the certificates represent `(x/d, y√15/d)` in the Euclidean plane, with denominator d=8.

The replay uses rational polygon clipping over `fractions.Fraction` for every pair of tiles. It independently checks:

- exactly the claimed number of triangles;
- positive orientation and the exact squared side lengths 4, 9 and 16 for every tile;
- the exact target side lengths;
- all tile vertices inside the convex target;
- equality of the sum of tile areas and target area;
- zero positive intersection area for every tile pair;
- cancellation of every internal atomic edge, splitting at all certificate vertices so that T-junctions are included.

| Certificate | Pairs checked | Positive-area overlaps | Internal atomic edges | Boundary atomic edges |
|---|---:|---:|---:|---:|
| `data/theta-147.json` | 10,731 | 0 | 217 | 33 |
| `data/theta-243.json` | 29,403 | 0 | 359 | 42 |

Both return **PASS**. Full results, including the exact file hashes, are in `verification/theta-odd.json`.

The public certificate hashes replayed for this report are:

```text
147: 4a38b3b03bffcc9668a414d11c2edefe2467ceed4d0f93fef9c31b7521e68cf1
243: 90423a5b35e094f1e9c7983a03bc848b0515a2b667c4ee81d55eba762bd8e7ca
```

The original deterministic research files had hashes `986e0aad007ca534b8812e5297c8a2579fabd630c431c0fa4550388daa6fa748` (147) and `ffef97c63d5e3751db1bc5cd0d9e57bd4a75f85002cc616db312f7950e030044` (243). The public files revise provenance metadata and omit the generator's embedded verification report; they preserve exactly the same geometry. This audit reran the independent checker on the public bytes, rather than transferring a hash-based verdict from the earlier files.

Containment, pairwise disjoint interiors, and equal total area imply that the closed triangles fill the target. The atomic-edge check supplies a separate consistency check of the boundary and every seam. This is a verification of finite constructions, not a formal verification of any nonexistence theorem.

## 3. The exact contradiction to Lemma 55

The source's hypotheses require primitive integer sides, b squarefree, and b coprime to c−a, for a theta-isosceles target. For `(a,b,c)=(2,3,4)`, these conditions hold:

$$
\gcd(2,3,4)=1,\qquad b=3\text{ is squarefree},\qquad\gcd(3,4-2)=1.
$$

Its conclusion asserts that `k=gcd(a,c)=2` divides M and that µ is an integer. In the verified 147-tiling,

$$
\mu=\frac{X}{c}=\frac{42}{4}=\frac{21}{2},
$$

which is not an integer. The standard coloring equation also yields `M=(2X−Y)/(a+b+c)=(84−21)/9=7`, so `2∤M`. The nonintegral geometric µ alone contradicts the printed conclusion.

The 243-tiling gives a second instance with `µ=27/2` and M=9.

The printed proof of Lemma 55 invokes `k|M` for an enlarged beta-isosceles tiling through Theorem 18. The current Theorem 18 explicitly retracts that divisibility condition in footnote 3. Thus the counterexample agrees with the identified dependency failure. This audit concerns the exact version `1206.2229v4`; it makes no assertion about future corrections.

## 4. Why the odd constructions work

They use the macrogeometry of Beeson's Theorem 24 but remove an unnecessary integrality restriction on one auxiliary strip count. For tile `(2,3,4)`, let the desired count be `3T²`, put `µ=3T/2`, and choose green scale p=4. The five triangular regions have integer scales

$$
4,\quad6,\quad2(T-4),\quad2,\quad T-4.
$$

The first gamma-angle parallelogram has side lengths `L=3T−16` and 6. Although its former parameter `r=L/2` is not integral when T is odd, the parallelogram itself can still be tiled. Express `L=2x+3y`. A band of horizontal width 2 uses cells with horizontal side 2 and slanted side 3; a band of width 3 uses cells with horizontal side 3 and slanted side 2. Since 6 is divisible by both 2 and 3, both band types end at the same far boundary. Each cell has included angle γ and divides into two tiles.

For T=7, take `L=5=2+3`; for T=9, take `L=11=4·2+3`. The final parallelogram has horizontal side `3(T−4)` and slanted side `26−2T`, the latter an even positive integer in both cases. It is tiled by ordinary 3-by-2 cells.

The tile total is

$$
16+36+4(T-4)^2+4+(T-4)^2+2(3T-16)+(T-4)(26-2T)=3T^2.
$$

The exact replays above verify all macroregion interfaces and every individual tile for the two values used as seeds. No parity assumption about an arbitrary hypothetical tiling is used.

## 5. Closure covers every t≥4 except 5

Use a theta-isosceles unit triangle `T₀=conv(0,p,q)` with `|p|=|q|=6` and included angle α. Its area is three tile areas. If the scales m and n of this triangle are tiled, then scale m+n is the union of their translates and the parallelogram

$$
R=\operatorname{conv}(0,np,np+mq,mq).
$$

The translated triangles are `np+mT₀` and `mq+nT₀`. Their common corner `np+mq` lies on the large triangle's opposite side, so these three regions partition `(m+n)T₀` with disjoint interiors.

The parallelogram has side lengths 6n and 6m and included angle α. If either m or n is even, orient its cells so that the corresponding even-scale side is divided into steps of length c=4, and the other side into steps of length b=3. Both counts are integers. These b,c cells split into two original tiles, adding `6mn` tiles and giving total `3(m+n)²`.

The known 48- and 108-tile seeds supply t=4 and t=6. Repeated addition of 4 supplies all even t≥4. The new seeds give t=7 and t=9; repeated addition of 4 supplies both odd residue classes for every odd t≥7. Thus every integer t≥4 other than 5 is realized.

The earlier independently checked two-c-edge proof excludes t=1,2,3. Area gives the necessary form `N=3t²`. Therefore t=5, namely N=75, is the sole unresolved value for this fixed tile and theta target shape. It is not permissible to infer its impossibility from the absence of a current construction.

## 6. General mixed-strip eventual construction

The following formula in [the theta-branch report](../theta-branch.md), Section 7, passes this algebraic and geometric audit. Let

$$
a=uv,\quad b=v^2-u^2,\quad c=v^2,\quad
\Delta=b(a^2+b^2)-a^2c>0,\quad F=(a-1)(b-1).
$$

Then every integer

$$
T\ge\left\lceil\frac{(a^2c+F)(a^2+b^2)}{u\Delta}\right\rceil
$$

has a theta-isosceles construction with exactly `N=bT²` tiles, equal sides `bvT`, and base `ubT`.

To see this, choose an integer J in

$$
\frac{uT}{a^2+b^2}\le J\le\frac{ubT-F}{a^2c}.
$$

The interval length is

$$
\frac{uT\Delta-F(a^2+b^2)}{a^2c(a^2+b^2)},
$$

which is at least 1 under the stated bound. J is positive. Use target scale `µ=bT/v` and green scale `p=a²J`. The five triangular scales of the Theorem 24 macrogeometry become

$$
a^2J,\quad abJ,\quad vT-acJ,\quad au^2J,\quad uT-a^2J.
$$

They are all integers. The upper bound on J gives `ubT>a²cJ`; since c>b, this implies `T>avJ`, and hence both the yellow scale `vT−acJ` and pink scale `uT−a²J` are positive.

The first parallelogram has horizontal length

$$
L=ubT-a^2cJ\ge F
$$

and slanted length `H=abu²J`, a multiple of both a and b. Since `gcd(a,b)=1`, every integer at least F is a nonnegative combination `xa+yb`. Split L into such bands. Across H, an a-band is divided into b-steps and a b-band into a-steps. Every cell splits into two original tiles. The auxiliary value `r=L/a` need not be integral.

The final parallelogram has horizontal length `b(uT−a²J)` and slanted length

$$
a\bigl((a^2+b^2)J-uT\bigr).
$$

The latter is a nonnegative integer multiple of a by the lower bound on J; the former is a positive integer multiple of b. This is an ordinary b-by-a grid. Zero final width is allowed and simply removes this last region.

The triangle/parallelogram interfaces use only the exact side identities of the macrogeometry. Positivity of the first parallelogram length, nonnegativity of the final width, and the positive triangular scales are precisely what makes its regions fit. In particular, integer r was a condition for a chosen uniform grid, not a geometric condition on the dissection. Area now gives

$$
\frac{(bvT)^2}{bc}=bT^2
$$

tiles, as claimed.

For `(2,3,4)`, this bound is `T≥11`; the explicit seeds and additive closure improve it to every T≥4 except possibly 5. If b is squarefree, the area equation permits exactly the count forms `bT²`, so the general construction settles all sufficiently large scales for that fixed tile. If b is not squarefree, it covers only this sufficient subfamily. No conclusion is drawn for the complementary geometric range `Δ<0`.

## Files and reproducibility

Run from the repository root:

```bash
python3 scripts/verify_theta_odd.py
```

The deterministic certificates and replay are enough to check both counterexamples without executing the author generator. The general scale-addition and eventual-construction statements are supplied as ordinary mathematical proofs, separately from those finite certificates.

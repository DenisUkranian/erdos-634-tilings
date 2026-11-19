# Powers in Erdős Problem 634

19 November 2026. Let T(N) mean that at least one nondegenerate triangle can be tiled with N congruent triangles. Reflections and arbitrary T-junctions are allowed. Bases and exponents are positive integers throughout. When the problem is stated for N>1, omit N=1.

## 1. Every fifth power is attainable

**Claim.** T(nᵏ) holds for every n and every k≥4.

**Input theorem.** In Vico Bonfioli’s manuscript, the *Notch seed family* theorem in *Isosceles targets with base angles α+β* gives T(bt²) for coprime 1≤e<f, b=f²−e², and all integers t≥t₀. The tile sides are (ef,b,f²) and the outer sides are (tbf,tbf,tbe). The explicit sufficient threshold is

    h = ceil(e/(f−e)),  j = ceil(he/b),
    M = max(ceil(fh/e), h+ceil(eh/f)),  t₀ = fj+M.

The source also cites Denis Paliy’s earlier construction for all sufficiently large scales of a fixed tile. Here the quantitative threshold is essential. Bonfioli’s declaration and the threshold definition were checked against the linked source versions. No fresh Lean build was run in this study.

**Odd n≥3.** Set e=(n−1)/2 and f=e+1. Then b=n, h=e, j=ceil(e/2) and M=2e. The last equality follows from ceil(e²/(e+1))=e. For j, use e²/(2e+1)=e/2−e/(4e+2), with the subtracted term strictly between 0 and 1/4. Hence t₀=(e+1)ceil(e/2)+2e≤(e+1)e+2e≤(2e+1)²=n². Take t=n² to obtain bt²=n⁵.

**Even n≥4.** Set e=n−1 and f=n+1. These are coprime because they are odd and differ by 2. Now b=4n, h=n/2, j=ceil((n−1)/8), M=n. Indeed fh/e≤n and eh/f=n/2−n/(n+1), so h+ceil(eh/f)=n. The required scale is t=n²/2. For n≥6 we have

    2t₀ ≤ (n+1)(n+6)/4 + 2n = (n²+15n+6)/4 ≤ n²,

using ceil((n−1)/8)≤(n+6)/8 and 3n²−15n−6≥0. Then bt²=4n(n²/2)²=n⁵. For n=4 use a square subdivision into 32² pieces. For n=2 bisect an isosceles triangle and subdivide each half into 4² pieces. The case n=1 is immediate.

**All exponents k≥4.** For even k, nᵏ is a square. For odd k≥5, subdivide each of the n⁵ tiles by a triangular grid into (n^((k−5)/2))² congruent triangles. This proves the claim.

## 2. Bounds for intermediate scales

The construction also gives T(dm²) for odd d≥3 whenever m≥d+floor(d²/8). For even e=(d−1)/2 the sufficient threshold is t₀=(e²+5e)/2. For odd e≥3 Bonfioli’s *Odd e* corollary gives (e²+5e+2)/2. For e=1, t₀=4. Substitution gives the stated bound for odd e and one less for even e. For even d≥4 take e=d−1 and f=d+1. This gives T(dm²) for every **even** m≥2(d+1)ceil((d−1)/8)+2d. These sufficient bounds can substantially exceed the threshold, even for classical d.

**Cubes of products.** Write n=xy with odd coprime 3≤x<y. If y≤4x²(x−2), then T(n³). In particular y≤x³ suffices. Take e=(y−x)/2 and f=(y+x)/2. A common divisor of e,f divides x,y, so it is 1. We have b=xy, h=ceil(e/x)≤e and h<f/x. Thus j<y/(4x²)+1 because fe=(y²−x²)/4. Both terms defining M are at most y: the first is at most f and the second at most 2e. Since f≤y, t₀<y²/(4x²)+2y≤xy=n. At t=n this gives n³. For x=19,y=43 we get e=12,f=31,b=817,h=1,j=1,M=3,t₀=34. Thus every 817m² with m≥34 is attainable.

## 3. Remaining prime powers

For k=1 the Beeson–Roșu prime classification gives 2, 3 and the primes congruent to 1 modulo 4. Their square multiples are also attainable. For prime p>3 congruent to 3 modulo 4 in classes 7, 11 or 23 modulo 24, p³ is attainable:

* For residues 7 and 23 modulo 24 use a primitive representation p=2v²−u² with 0<u<v.
* For residue 11 modulo 24 use a primitive representation p=3v²−u² with 0<u<v.

Lemma 5.1 of Paliy’s square-class saturation note gives these representations with references on norm forms. At scale t=p use W in the first case and β in the second. For D=2 or 3 write p=Dv²−u²=(Dv−u)v+(v−u)u. Enlarge the seed tiling of scale v by a grid factor Dv−u, then add v−u collars of scale u. This uses only the seed and the specified admissible increment. Paliy’s theorem on all scales t≥v gives the same conclusion. The tile count is p·p². The only possible exceptions left among prime powers are cubes with p congruent to 19 modulo 24.

For such p, p³ is 19 modulo 24. Section 5, *Without squarefreeness*, of Paliy’s geometric reduction leaves θ and the isosceles double-angle case. Both have b=v²−u² and p³=bt² with t≥2. Thus t=p, b=p and (v−u)(v+u)=p, giving u=(p−1)/2, v=(p+1)/2. There are **two** specific target/tile shape pairs for each p. For example, p=19 gives N=6859:

| Target | Tile | Target sides |
|---|---|---|
| θ | (90,19,100) | (3610,3610,3249) |
| Double angle | (81,19,90) | (3249,3249,3610) |

**Verified limit of the method.** For θ with f=e+1, condition (a) in Bonfioli’s *Band theorem* forces n≥e and M≥f. Condition (d) gives k≥enf/(2e+1)≥e²(e+1)/(2e+1). The target scale M+k=2e+1 requires k≤e, impossible for e≥2. For example, when e=9 these two conditions alone require M+k≥53, whereas 19³ needs scale 19. This rules out this particular use of the band theorem. This work leaves the existence of both candidate tilings for 6859 undecided.

## Attribution and verification

The result on n⁵, the bounds and the two reductions are deductions from the sources below. Priority has not been established. This text has not undergone independent human review or a new machine formalization. The script check_powers.py replays the integer arithmetic. The proof for arbitrary n is given above.

- [Vico Bonfioli, manuscript v6, section on θ](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/paper/erdos634_v6_main.tex).
- [Threshold t₀ in Lean](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/lean/Erdos634/Draft/ThetaNotch3Gen.lean), [thetaTiled_all and tileCount_all](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/lean/Erdos634/Draft/ThetaNotch4Rho.lean), [odd e](https://github.com/ElVec1o/erdos634_primes_and_N200/blob/752005605ca4e607d2a08f57bdc2445dd5558dbb/lean/Erdos634/Draft/ThetaOddEFinal.lean).
- [Denis Paliy, earlier square-class tail result](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/docs/square-class-tails.md), [norms and W, β constructions](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/square-class-saturation/PROOF.md), [all scales from v](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/updates-2026-10-10/w-beta/UNRESTRICTED_CONSTRUCTION.md), [residue reductions and angles](https://github.com/DenisUkranian/erdos-634-tilings/blob/0f7935b71fd958bd764bccf079e1e70bc68ce351/research/uniform-reduction/PROOF.md).
- [Michael Beeson and Grigore Roșu, prime theorem, v4](https://arxiv.org/abs/2607.23453v4).

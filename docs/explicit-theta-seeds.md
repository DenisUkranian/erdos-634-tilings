# Explicit theta seeds and computable bounds for all five rational shapes

29 September 2026. Research note by Denis Paliy, who directed the
investigation; ChatGPT assisted with construction, drafting, and exact
checks. The negative-Delta construction below received a separate
internal symbolic audit. External review and priority have not been
established. This is not a complete solution of Erdős problem 634.

This note makes the rational-trapezoid step in Laczkovich's construction
fully effective. It supplies a deliberately coarse seed, not an optimal
tiling. The five-triangle layout is the one reproduced in Beeson's
Figure24 and Theorem23. The horizontal strip decomposition is an
integral specialization of Laczkovich's Lemma2.2(ii).

Throughout,

$$
a=uv,\quad b=v^2-u^2,\quad c=v^2,\quad
0<u<v,\quad\gcd(u,v)=1,
$$

$$
\Delta=b(a^2+b^2)-a^2c<0,
\qquad F=(b-1)(c-1),\qquad S=a^2+b^2.
$$

Define positive integers

$$
n=\left\lceil\frac{F-a^2\Delta}{b^3c^2}\right\rceil,
\qquad \rho=ab^2cn,
\qquad s=ucnS.
$$

**Proposition.** The theta target at scale `s`, of sides
`(bvs,bvs,ubs)`, has a tiling by the primitive tile. Thus this is a
computable seed for every negative-Delta tile.

## The five-triangle layout

Set `D=4v²-u²`; coordinates `(x,y)` mean Euclidean `(x,y sqrt(D))`.
Let

$$
\mu=bs/v=\rho S/(bc),\qquad
A=(0,0),\quad C=(\mu a,0),\quad B=(\mu a/2,\mu v/2).
$$

The following vectors have Euclidean length one:

$$
e_- =(-u/(2v),-1/(2v)),\quad
e_+ =(u/(2v),-1/(2v)),
$$

$$
e_\alpha=((2c-u^2)/(2c),u/(2c)).
$$

Define

$$
 K=B+b\rho e_-,\qquad L=B+c\rho e_+,
$$

$$
 H=\frac{a^3\rho}{bc}e_\alpha,\qquad
 I=\frac{-\rho\Delta}{ab}e_\alpha,
$$

$$
 J=C+\frac{-\rho\Delta}{bc}(-u/(2v),1/(2v)).
$$

The five tile-shaped triangles and their integer scales are

| Triangle | Scale |
|---|---:|
| `BKL` | `rho = a b² c n` |
| `KHL` | `a rho/c = a² b² n` |
| `AKH` | `a² rho/(bc) = a³ b n` |
| `HLJ` | `b rho/c = a b³ n` |
| `HIJ` | `b rho/a = b³ c n` |

Their side lengths can be checked directly from the displayed
coordinates. The corresponding edge relations are

$$
BK=b\rho,\ BL=c\rho,\ KL=a\rho,
$$

$$
KH=a^2\rho/c,\ HL=ab\rho/c,\ AK=a^2\rho/b,
$$

$$
AH=a^3\rho/(bc),\ LJ=b^2\rho/c,
\ HJ=b\rho,\ HI=b^2\rho/a,\ IJ=bc\rho/a.
$$

The boundary orders are `A,K,B`, `B,L,J,C`, and `A,I,H`. In fact

$$
AI=-\rho\Delta/(ab)>0,\qquad
JC=-\rho\Delta/(bc)>0,
$$

and all the other listed segments have positive lengths. To locate `H`
without relying on a drawing, its barycentric coordinates in `ABC` are

$$
\left(\frac{b^2}{S},\frac{a^2u^2}{cS},\frac{a^2b}{cS}\right),
$$

and in `AKL` they are

$$
\left(\frac{b^2}{c^2},\frac{u^2b}{c^2},\frac{u^2}{c}\right).
$$

All are positive and sum to one. The remaining quadrilateral `AHJC`
is convex: `HL` is horizontal, so removing `BKL`, `AKH`, and `KHL`
first leaves the trapezoid `AHLC`; removing `HLJ` leaves `AHJC`.
The edge `AH` points at angle `alpha` above the horizontal, `HJ` at
angle `beta` below it, and `JC` at angle `theta` below it. Its partition
by `IJ` consists of triangle `HIJ` and the trapezoid `AIJC`.
These orders and the interior placement of `H` give the asserted
disjoint partition of `ABC` into the five triangles and `AIJC`.

The lower and upper horizontal bases of the red trapezoid are `AC`
and `IJ`, with

$$
IJ=\rho bc/a,\quad AI=-\rho\Delta/(ab),\quad
JC=-\rho\Delta/(bc),\quad AC-IJ=AI.
$$

## Filling the red trapezoid

Divide both slant sides into `n` equal parts, and join corresponding
points horizontally. Every strip has left and right legs of lengths

$$
\ell=AI/n=bc(-\Delta),\qquad
r=JC/n=ab(-\Delta).
$$

For one strip, label its vertices `A',B',C',D'` from the lower left,
lower right, upper right, upper left. Its lower corner angles are
`alpha,theta`. Set `r_1=r/b=a(-Delta)`. On the upper base choose `E'`
at distance `a r_1` to the left of `C'`, and put

$$
G'=E'-(D'-A').
$$

Then `B'C'E'` is a tile-shaped triangle at scale `r_1=-a Delta`,
and `B'E'G'` is a tile-shaped triangle at scale
`r_2=ell/b=-c Delta`. The leftover `A'D'E'G'` is an alpha-
parallelogram of slant length `ell=bc(-Delta)`.

Counting strips downward from the top, its other side has length

$$
W_j=b^3c^2n+a^2\Delta+jbc(-\Delta),\qquad 0\le j<n.
$$

By the definition of `n`, every `W_j>=F`. Because `gcd(b,c)=1`, write
`W_j=x_j b+y_j c` with nonnegative integers. The slant length is a
multiple of both `b` and `c`, so mixed strips of the two orientations of
the `b`-by-`c` alpha-parallelogram tile the remainder.

Every triangular scale in both the five-block layout and these strips
is an integer. Quadratic subdivision therefore turns the full macro
partition into a tiling by congruent copies of the original tile.

## Reproducibility and conservative scale

[`check_explicit_theta_seed.py`](../scripts/check_explicit_theta_seed.py) checks all side lengths, containment,
pairwise intersections of the six main convex regions, each strip
partition, and the exact total count `b s²`, using rational arithmetic.
All 67 negative-Delta coprime pairs with `v<=25` pass. The largest
tested strip count is 1624; individual tiles, whose numbers can be
enormous, are not expanded.

| Tile | `n` | Seed scale `s` | Tile count `b s²` |
|---|---:|---:|---:|
| `(6,5,9)` | 1 | 1098 | 6028020 |
| `(12,7,16)` | 2 | 18528 | 2403007488 |
| `(90,19,100)` | 77 | 586347300 | 6532259968128510000 |

These are upper bounds, not minimal scales or claims of small tilings.
With the [two shell lemmas](universal-rational-scales.md), one may take

$$
H_u=\left\lceil\frac{a^2+b^2+F}{ub}\right\rceil,
\quad S_0=s\lceil H_u/s\rceil,
\quad C_\theta=S_0+(u-1)(v-1).
$$

Every theta scale `T>=C_theta` then exists, as does every alpha scale
`K>=ceil(C_theta/v)`. This turns the qualitative eventual theorem into
an explicit, although very coarse, bound throughout the negative-
Delta range.


## The positive sign and a complete table of explicit bounds

The two signs exhaust all primitive parameters. Indeed,

$$
\Delta=b^3-cu^4,
$$

and $\gcd(b,c)=1$. If $\Delta=0$, then $c$ divides $b^3$, forcing
$c=1$; this contradicts $c=v^2$ and $v\ge2$.

When $\Delta>0$, the earlier
[eventual-family construction](eventual-rational-families.md)
supplies every theta scale at least

$$
B_+=\left\lceil
\frac{(a^2c+(a-1)(b-1))(a^2+b^2)}{u\Delta}
\right\rceil.
$$

Thus $s=B_+$ is an explicit seed, and the stronger direct threshold
$C_\theta=B_+$ can be used in this sign. In the negative sign use the
seed $s$ proved above and the displayed threshold $C_\theta$.
For both signs define

$$
C_{W,\beta}=v\left\lceil\frac{H_u}{v}\right\rceil
 +(u-1)(v-1),\qquad Q=b+c,\quad P=b+2c.
$$

The [universal annulus theorem](universal-rational-scales.md) and the
[complete other-scalene construction](two-piece-construction.md) give:

| Target | Necessary count form | Explicit sufficient scales |
|---|---|---|
| W | $QT^2$ | $T\ge C_{W,\beta}$ |
| Beta-isosceles | $PT^2$ | $T\ge C_{W,\beta}$ |
| Theta-isosceles | $bT^2$ | $T\ge C_\theta$ |
| Alpha-isosceles | $bQK^2$ | $K\ge\lceil C_\theta/v\rceil$ |
| Other scalene | $QPK^2$ | $K\ge1$ |

Every bound in this table is now computed directly from $(u,v)$.
The bounds are sufficient and intentionally conservative; they do not
identify the exceptional scales below them.

## Reproduce the checks

From the repository root:

```sh
python scripts/check_explicit_theta_seed.py
```

The script uses only the Python standard library, refuses optimized
Python (`-O`), writes no files by default, and prints deterministic JSON.
The committed [verification output](../verification/explicit-theta-seeds.json)
uses the default `--max-v 25`: 67 negative-Delta geometric checks and
132 positive-Delta interval checks, covering 199 primitive parameter
pairs. The positive-Delta geometry is checked separately by
[`check_eventual_families.py`](../scripts/check_eventual_families.py).
Finite checks corroborate the uniform proof; they do not substitute for it.

## Sources and attribution

- Miklós Laczkovich, [*Tilings of triangles*](https://doi.org/10.1016/0012-365X(93)E0176-5),
  Discrete Mathematics 140 (1995), 79–94, Lemma 2.2(ii): rational
  trapezoid dissection into two tile-shaped triangles and a parallelogram.
- Michael Beeson, [*Triangle Tiling: The Case $3\alpha+2\beta=\pi$*](https://arxiv.org/abs/1206.2229),
  version 4, Figure 24 and Theorem 23: the five-triangle layout and its
  negative-Delta parameter range. The complementary construction is
  Theorem 24 and Corollary 5.
- This appendix specifies integral block scales, mixed strips, and an
  explicit denominator-clearing bound. Its
  [separate internal check](audits/explicit-theta-seeds.md)
  covered the two barycentric formulas, boundary orders, convexity,
  red-strip widths, and the Frobenius bound. The audit of the main
  annulus theorem should not be read as an external audit of this appendix.

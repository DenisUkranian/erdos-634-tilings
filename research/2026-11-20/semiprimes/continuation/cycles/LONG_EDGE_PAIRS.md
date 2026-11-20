# A uniform whole-board lower bound for triangles without a long-edge parallelogram mate

Let $a>b$ be positive odd primitive F2 sides, $c^2=a^2+ab+b^2$,
$p=a+2b$, $q=2a+b$, $d=a-b$. In any tiling of the complete unit triangle
$T=(O,B,C)=(0,c^2,apz^2)$ by $N=pq$ congruent triangles, let $U$ count
tiles whose neighbor across the whole side of length $c$ is not their
half-turn mate. A mate and its tile form a parallelogram with sides $a,b$.
This includes in $U$ a tile with a partial long-edge contact or with a
neighbor forming a different quadrilateral. Every tile has only one long
edge, so all existing half-turn pairs can be removed simultaneously.

**Theorem.** For every such board $U\ge N/c$. If $a\ge2b$, then
$$
 \boxed{U\ \ge\ 4c-2(a-b)+1.}
$$
This includes every odd mixed semiprime parameter remaining beyond the
unit staircase. Its parameter reduction gives $u/v\ge6$, hence
$a/b=(u^2-v^2)/(v(2u+v))\ge35/13>2$. Neither primality nor a height
gap is used in the proof. Tile reflections and arbitrary T-junctions are
allowed. The proof uses the two whole-edge cuts of the [earlier whole-board
path theorem](../paths/TWO_PATHS.md). It prescribes no pair of corner
patches and no inner boundary.

| $N$ | $(a,b,c)$ | Proved lower bound for $U$ |
|---:|---:|---:|
| 3,431 | (33,7,37) | 97 |
| 5,063 | (35,13,43) | 129 |
| 19,367 | (85,11,91) | 217 |
| 60,023 | (143,25,157) | 393 |
| 64,367 | (161,15,169) | 385 |
| 271,151 | (323,37,343) | 801 |
| 641,591 | (533,27,547) | 1,177 |

These are proved lower bounds. A tiling attaining any entry is unknown
here. A complementary [two-modulus bound](WHOLE_BOARD_PAIRS.md) survives
when the chosen parallelograms may also be formed along a shorter side.

## Whole-edge paths survive pair cancellation

Use $\rho=e^{i\pi/3}$, $z=(a+b\rho)/c$. A direction $\rho^jz^h$ has
height $h$. The short sides of a tile have the same height; its long
side has height one higher or one lower. At threshold $k=0,1$ the
whole-edge cut is an oriented chain of long edges with endpoints $B-O$.
Its steps go from the $\beta$ endpoint to the $\alpha$ endpoint. A
long edge at height $k$ has its short-height-$(k+1)$ tile on its left;
a long edge at height $k+1$ has its short-height-$k$ tile on its right.
If tiles form a parallelogram across $c$, their two contributions to
the unique threshold they cross are precisely the same segment with
opposite orientations. Erase every such pair in the directed chains.
The unchanged endpoint boundary gives a vertex-simple $O$ to $B$ path
in each chain, now using only tiles counted in $U$. The paths use
disjoint tiles, as a tile crosses only one threshold. All their edges
belong to the original tiling. In particular the upper path still
bounds a tiled region against the base, by the geometric simplicity
and open-base argument in the [path theorem](../paths/TWO_PATHS.md).

The lower path has at least $c$ edges by Euclidean distance. None of
its tiles has an edge of height 2. Write $L$ for the upper path length
in whole $c$-edges. For a directed edge of height 2 and length $s$
define its signed weight as $(-1)^j s$. Opposite directed edges cancel
and subdivision at T-junctions preserves the weight. On any one tile
the absolute height-2 weight is at most $c$: a long edge contributes
$c$, while its two short edges together contribute $d$ in absolute
value if they are at height 2. A half-turn pair contributes zero.
The board weight at height 2 is $-(ap+bq)=-(c^2+3ab)$. This alone,
plus the $c$ lower-path tiles of weight zero, gives $U\ge N/c$.

## The upper path and the remaining boundary weight

Let $J$ and $K$ be the alternating signed *counts* $\sum(-1)^j$ of
the upper steps in the height-1 and height-2 alphabets respectively.
Thus $L\ge |J|+|K|$ and $L\ge c$. The two boundary characters on the
region between the path and the base give
$$
 J+K\equiv d\pmod{c-d},\qquad J-K\equiv d\pmod{c+d}.
$$
For completeness, its CCW boundary is the base followed by the reversed
path. Its total alternating weights, without and with the factor
$(-1)^h$, are $c^2-c(J+K)$ and $c^2+c(J-K)$. The tile divisors are
$d-c$ and $d+c$ respectively, and $c$ is coprime to $d$. See the
[full-board character calculation](../../FULL_BOARD.md).

A height-1 step with unit direction $e=\rho^j$ on the upper path has its
tile on the left. The two directed short axes on that tile are $-e$ and
$\rho^2e$ in the height-2 frame, with lengths $a,b$, respectively.
Its height-2 weight is $-d(-1)^j$. A height-2 step has its tile on the
right, so the CCW long edge gives $-c(-1)^j$. The tiles not in either
path must therefore provide weight $-(c^2+3ab)+dJ+cK$. Half-turn pairs
supply zero. It follows that
$$
 U\ \ge\ c+L+\frac{|c^2+3ab-dJ-cK|}{c}. \tag{1}
$$
Write the two congruences as $J+K=d+(c-d)i$, $J-K=d+(c+d)j$. Since
$c\pm d$ are odd, $i-j=2t$ for an integer $t$. Substitution gives
$$
 J=d+cj+(c-d)t,\qquad K=(c-d)t-dj,\qquad
 dJ+cK=d^2+3ab\,t.
$$
The last term in (1) equals $3ab|t-2|/c$.

## Proof of the uniform inequality

Assume $a\ge2b$. We prove $L+3ab|t-2|/c\ge3c-2d$. Use
$3ab=c^2-d^2$, $0<d<c$ and $3d\ge c$ (since $3d\ge a+b>c$).

* For $t\le0$, $L+3ab|t-2|/c\ge c+6ab/c=3c-2d^2/c\ge3c-2d$.
  For $t\ge3$, $cL\ge dJ+cK=d^2+3ab\,t$. Adding the remaining term
  gives at least $(d^2+12ab)/c=4c-3d^2/c\ge3c-2d$, since
  $(c-d)(c+3d)>0$.
* For $t=2$, $J=2c-d+cj$ and $K=2(c-d)-dj$. At $j=-1$ their absolute
  values sum to $3c-2d$. For $j\ge0$ the sum is at least its value
  $4c-3d$ at zero: $J$ increases by $c$ while $|K|$ can decrease by
  at most $d$ per step. For $j\le-2$ both absolute values increase as
  $j$ decreases, from $2c+d\ge3c-2d$ at $-2$.
* For $t=1$, $J=c(1+j)$ and $K=c-d-dj$. At $j\ge0$ the same argument
  bounds $L$ below by $2c-d$, and at $j\le-2$ by $2c+d$. Adding
  $3ab/c=c-d^2/c$ yields the claim. Only $j=-1$ remains.

In that last case $J=0$, $K=c$. Work in the height-2 frame, dividing
physical coordinates by $cz^2$. For axial coordinates $(x,y)$ use the
linear functional $F=x-y$. The endpoint is
$B/(cz^2)=(ap/c,-bq/c)$, so its functional value is $c+3ab/c$.
For a height-2 step of positive character the maximum of $F$ is 1;
for one of negative character it is 2. If there are $n$ negative steps
of this alphabet, there are $n+c$ positive ones. For the middle
alphabet the directions are $\bar z\rho^j$; the corresponding maxima
are $p/c$ and $q/c$. This follows directly from the three axial
numerators $p,-d,-q$ for $j=0,1,2$ and their negatives at $j+3$.
Since $J=0$, the $m$ middle steps have equal counts of the two signs.
As $L-c=m+2n$ we obtain
$$
 \frac{3ab}{c}\le \frac{p+q}{2c}m+3n
 \le \frac{3(a+b)}{2c}(L-c),
 \qquad L-c\ge\frac{2ab}{a+b}.
$$
This exceeds $(c-d)^2/c$ when $a\ge2b$. Indeed $c<a+2b/3$ and
$c\ge\sqrt7\,b>5b/2$, so $(c-d)^2/c<10b/9$, whereas
$2ab/(a+b)\ge4b/3$. Thus $L+3ab/c\ge3c-2d$ in the final case as well.
Equation (1) gives $U\ge4c-2d$. The board has an odd tile count and
pairs remove two at a time, proving the stated $+1$.

There is a stronger conditional estimate after the half-turn pairs are
erased. If an upper path then uses only height 1, its endpoint character
is $J=d$ by the [middle-path population proof](CYCLES.md), and $K=0$.
The signed axis counts equal the reference $a$ forward and $b$ downward
steps, so $L\ge a+b$. Equation (1) gives at least 115 unpaired tiles
for $3431$ and 155 for $5063$, after rounding to odd integers. The
hypothesis concerns a path in the reduced chain.

[Exact arithmetic and independent inventory calculation on the seven controls](check_long_pairs.py).

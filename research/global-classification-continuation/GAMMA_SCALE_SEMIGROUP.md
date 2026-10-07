# A sharper constructive scale spectrum for the gamma corner

7 October 2026. This is a sufficient F3 construction, with an exact test
for its common-rectangle subconstruction. It is not a necessary condition
for general tilings and does not decide 4830 or 154. The subsequent
[common-staircase improvement](GAMMA_STAIRCASE.md) supersedes its tail
for 4830: every m>=2 is now positive, including19320.

## 1. The scaled rectangle condition

Let positive integers `a>b` satisfy `c²=a²+ab+b²`, and put

    h=a+2b, delta=a-b,
    F=-a³+2a²b+ab²+b³.

The reflected-gamma-hole lemma in
[the gamma-corner proof](../group2-gamma-corners/PROOF.md) works inside
an `L`-scaled tile triangle after removing a `t`-scaled reflected tile
triangle whenever there are nonnegative integers p,q with

    t <= min(ap,bq),          bp+aq <= L.                (1)

Its common parallelogram has side lengths `abp` and `abq`: either
the original grid or the grid with a and b interchanged tiles it.
The removed reflected corner lies in the second grid. The first
grid outside the parallelogram and the second grid inside it, less
the reflected corner, therefore tile the remainder.

For the F3 macro partition at multiplier m, the scales are

    L=mh,        t=m*delta.

For fixed m, condition (1) has an integer solution exactly when

    G(m):=b*ceil(m*delta/a)+a*ceil(m*delta/b)-mh <= 0.  (2)

Indeed the smallest eligible p,q are the two displayed ceilings,
and increasing either only makes the second inequality harder.
When (2) holds, the three other macro triangles each have scale mc.
Consequently their total unit-tile count, including the gamma
remainder, is

    3(mc)²+(mh)²-(m*delta)²
      =3(a+b)(a+2b)m².                               (3)

Thus (2) proves an actual ordered F3 tiling. The enclosing macro
partition is the one already established in the cited proof,
scaled uniformly by m. Rectangle feasibility implies that the
reflected hole is contained in its outer triangle, so the
construction makes no assumption that a/b<=2.

For completeness, the only additional order condition in that macro
partition is `delta*a<h*b`: this places its point J' strictly before K.
It follows directly from (1), since
`m*delta*a<=abq < b(bp+aq)<=m*h*b` (here p>0). The other intercept
inequality `delta*b<h*a` holds automatically for a>b. Thus the old
coordinate partition does extend to every instance of (2), rather
than requiring its earlier convenient hypothesis a<=2b.

## 2. A closed sufficient tail and an exact model spectrum

Since `ceil(x)<x+1`,

    G(m) < a+b-m*F/(ab).                             (4)

If F>0, every integer

    m >= C_gamma := ceil(ab(a+b)/F)                  (5)

satisfies (2). When `b<a<=2b`, the original unit-scale construction
already gives all m>=1, and this is stronger than (5) when its
ceiling is greater than one.

Conversely, `ceil(x)>=x` gives `G(m)>=-mF/(ab)`. There is no
positive rational root of `r³-2r²-r-1`: the rational-root test leaves
only r=1, which is not a root. Hence F is never zero for positive
integers a,b. If F<0, condition (2) fails at every positive m.

Equivalently, this rectangle construction succeeds at some scale
if and only if

    1 < a/b < sigma,

where sigma is the unique positive root of `r³-2r²-r-1=0`.
Uniqueness follows because the polynomial is strictly increasing
for r>2 and is negative on [1,2]. This describes this construction,
not all gamma-remainder tilings or all F3 tilings.

There is also an exact finite arithmetic description of its scales.
The ceiling inequality is subadditive, so

    G(m+n) <= G(m)+G(n).

Thus its successful nonnegative scales form an additive submonoid.
For every integer m,

    G(m+ab)=G(m)-F.                                  (6)

For F>0, write a positive m uniquely as `s+k*ab` with
`1<=s<=ab` and k>=0. Then (2) is equivalent to

    k >= max(0,ceil(G(s)/F)).                         (7)

This is an exact numerical-semigroup description of the
common-rectangle scales. Formula (5) often gives a more efficient
tail bound than enumerating its ab residue classes.

## 3. Two uniform ratio domains

The semigroup property sharpens the simple ceiling bound:

* If `b<a<=7b/3`, every multiplier m>=3 is constructive.
* If `b<a<=12b/5`, every multiplier m>=4 is constructive.

For the first assertion, use these explicit rectangle choices:

| m | p | q |
| --- | --- | --- |
| 3 | 2 | 4 |
| 4 | 3 | 6 |
| 5 | 3 | 7 |

Substitution in (1), with L=mh and t=m*delta, proves each inequality
throughout `b<a<=7b/3`. Since every integer at least 3 is a sum of
3,4,5, subadditivity gives the assertion. For the second assertion,
use the choices for m=4,5 above and add `(m,p,q)=(6,4,9),(7,5,10)`.
These four choices work throughout `b<a<=12b/5`; the integers
4,5,6,7 generate every integer at least 4.

For the range `2b<a<=7b/3` the first result is the **exact** spectrum
of this rectangle model: neither m=1 nor m=2 works. At m=1 the
minimum cost is `b+2a>h`. At m=2 it is `2b+3a>2h`, since
`2<2(a-b)/b<=8/3` and `1<2(a-b)/a<2`. Therefore its nonnegative
scale semigroup in that whole range is `<3,4,5>`.

These exact model failures remain insufficient for exclusions of
arbitrary tilings.

## 4. The class 4830

For `(a,b,c)=(24,11,31)`, one has `h=46`, `delta=13`, and

    F=3083,       ab(a+b)=9240,
    C_gamma=ceil(9240/3083)=3.

At m=1 the smallest rectangle costs `11+2*24=59>46`.
At m=2 it costs `2*11+3*24=94>92`.
At every m>=3, (4) and (5) prove feasibility. Its exact
nonnegative scale semigroup is therefore

    {0,3,4,5,6,...}=<3,4,5>.

In particular,

    4830*m² is a tiling count for every integer m>=3.  (8)

At m=3, choose p=2,q=4; then the common rectangle has cost
`2*11+4*24=118<=138`, and the removed corner has scale 39,
which is at most both `2*24=48` and `4*11=44`.
The outer and inner gamma triangles contribute `138²-39²=17523`
tiles; the other three contribute `3*93²=25947`, totalling 43470.

This improves the earlier sufficient threshold 6 for this tile to 3.
Failure at m=1,2 is failure of this particular construction. In
particular this note supplies no nonexistence proof for 4830 or 19320.
Thus this rectangle argument leaves at most two exceptions in the
square class `4830*m²`; the subsequent staircase resolves19320, leaving
only4830. The
existing exhaustive candidate enumerator leaves just `(24,11,31)`
in F3 at scales 1 and 2, respectively, for these two integers; a
same-count replacement by another classified tile does not settle
either one.

## 5. Verification scope

`check_gamma_scale_semigroup.py` checks exact integers and ceilings,
the scale-count identity, the tail inequality, and the residue
recurrence for primitive norm triples in a stated finite range.
The proof above supplies the universal statements. The checker does
not enumerate unit triangles for the 43470 construction and is not
an independent geometric verifier for that many tiles.

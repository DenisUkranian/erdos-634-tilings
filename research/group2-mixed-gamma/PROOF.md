# A staircase interchange for reflected gamma corners

This is a sufficient constructive theorem, not an all-N classification.
The new result is an ordered F3 tiling for every `b<a<=5b/2` at every
integer multiplier `m>=2`, including **19320** for `(a,b,c,m)=(24,11,31,2)`.
The multiplier-one target 4830 remains unresolved. The directory name
records the mixed-direction research route: the staircase itself has one
short-direction class in the gamma remainder.

## 1. The common-cell staircase lemma

Let integer sides `a>b>0` meet at 120 degrees in a triangle R. In physical
unit coordinates along those two axes, take the outer triangle

```
O=(0,0), A=(La,0), B=(0,Lb).
```

The proposed reflected triangular hole has vertices

```
O=(0,0), C=(tb,0), D=(0,ta),
```

where L,t are positive integers. A sufficient condition for tiling the
complement by `L²-t²` congruent copies of R is

```
L >= b+a*ceil(t/b).                                      (1)
```

Partition the first quadrant into the common parallelogram cells

```
P(i,j)=[iab,(i+1)ab] x [jab,(j+1)ab],  i,j>=0.
```

Both the original grid (axis steps a,b) and the reflected grid (axis
steps b,a) tile every such cell, using respectively a `b by a` and an
`a by b` array of paired triangles. The interiors of the cells are
disjoint; switching any selection of whole cells therefore introduces
no overlap or incomplete tile.

Choose exactly the finite staircase

```
S={ (i,j)>=0 : ai+bj<t }.
```

A cell meets the interior of the reflected hole exactly when its lower
left corner satisfies `ai+bj<t`. Indeed the hole equation is
`x/b+y/a<=t`. Thus this staircase covers the entire hole; boundary-only
contacts with unselected cells do not matter. Its common-cell lines are
also lines of the reflected unit grid, so the hole comprises exactly
`t²` entire reflected unit triangles.

The outer triangle contains a whole selected cell if and only if its
upper right vertex lies inside, namely

```
b(i+1)+a(j+1)<=L.
```

The maximum left-hand side over S is exactly `b+a*ceil(t/b)`. To prove
this, put `q=ceil(t/b)`. Since `a>b`, the selection condition implies
`i+j<=q-1`. Consequently

```
b(i+1)+a(j+1)
 = b+a+a(i+j)+(b-a)i
 <= b+aq.
```

Equality occurs at `(i,j)=(0,q-1)`, which belongs to S. This proves
both (1) and its exactness **for this particular common-cell recipe**.
It is not a necessity theorem for arbitrary corner tilings.

Start with the ordinary L-fold grid, replace every selected cell by its
reflected grid, then remove the `t²` hole triangles. This proves the lemma.

## 2. Application to the ordered F3 target

Suppose also `c²=a²+ab+b²`. Set

```
h=a+2b, delta=a-b, L=mh, t=m*delta.
```

If

```
m(a+2b) >= b+a*ceil(m(a-b)/b),                         (2)
```

the canonical F3 triangle of sides

```
m(c², c(a+2b), 3b(a+b))
```

has a tiling by `3(a+b)(a+2b)m²` original triangles. Use the three `mcR`
triangles and the gamma remainder of the previously proved
[F3 macro partition](../group2-gamma-corners/PROOF.md), filling that
remainder by the staircase lemma. Its count is

```
3m²c²+L²-t² = 3(a+b)(a+2b)m².
```

The staircase containment implies `ta<Lb`; hence the reflected corner
is contained and this macro partition is positive. Explicitly, (2)
implies `m[(a+2b)b-a(a-b)]>=b²>0`.

No primitivity is required. The theorem applies to the displayed ordered
F3 target only; it does not automatically apply after exchanging a,b,
nor to F2 or F4.

## 3. Two useful uniform consequences

Write `E=2ab+2b²-a²`. Whenever `E>0`, every multiplier

```
m >= ceil(b(a+b)/E)                                    (3)
```

satisfies (2). This follows from

```
b+a*ceil(m(a-b)/b) < b+a+ma(a-b)/b
```

and `mE>=b(a+b)`. Smaller multipliers can additionally be checked by (2).

More sharply, **if `b<a<=5b/2`, every integer `m>=2` works**. For `a<=2b`
this already follows by subdividing the established multiplier-one
construction. For `2<a/b<=5/2`, put `r=a/b` and `K=ceil(3m/2)`; then

```
ceil(m(r-1))<=K,
m(r+2)-[1+r*ceil(m(r-1))]
 >= 2m-r(K-m)-1
 >= (9m-5K)/2-1.
```

For `m=2k`, the last expression is `3k/2-1>=0`. For `m=2k+1`, it is
`3(k-1)/2>=0`, since odd m>=2 means k>=1. This proves (2) throughout
the claimed interval.

## 4. The explicit 19320 tiling

For `(a,b,c)=(24,11,31)` and m=2, take `L=92`, `t=26`. The staircase is

```
(0,0), (0,1), (0,2), (1,0).
```

Their required outer scales are respectively 35,59,83,46, all at most
92. The staircase swaps `4*2ab=2112` triangles, after which the hole
removes `26²=676`. The gamma remainder has `92²-26²=7788` triangles;
the three other macro triangles contribute `3*62²=11532`. The total
is **19320**, with target sides **1922,2310,2852**.

The deterministic gzip certificate `f3-19320.json.gz` lists all 19320
unit triangles in exact rational Eisenstein coordinates. Its independent
checker imports no construction code. It verifies every tile's lengths,
target containment, total area, and interior nonoverlap using a complete
rational spatial filter followed by exact separating-axis tests. Every
pair with overlapping interiors must share a spatial bucket, so rejecting
all candidate overlaps covers all 186,621,540 possible pairs without
looping over each pair. The report records actual candidate and SAT counts.

This is internal independent verification, not external peer review.
At multiplier one (2) fails: its cost is `11+24*ceil(13/11)=59>46`.
That failure excludes only this recipe and does not prove 4830 impossible.

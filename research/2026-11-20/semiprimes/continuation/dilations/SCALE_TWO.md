# The exact scale-two cutoff in the exceptional mobile staircase

Let $u\ge4$ satisfy $u=1\pmod3$. Set $a=(u^2-1)/3$, $b=(2u+1)/3$,
$c=(u^2+u+1)/3$ and $q=2a+b=2c-1$. Then $a>b$ and $c^2=a^2+ab+b^2$.
The unit F2 board has sides $a(a+2b),bq,c^2$.
Its dilation by two has a mobile staircase tiling for **every**
$u=4,7,10,13,16,19,22,25$. For **every $u\ge28$** in the progression
even the following relaxation of that staircase fails. This last
statement concerns a construction class. It leaves other dissections of
the doubled board, and all unresolved unit boards, open.

Use nonnegative integer horizontal/vertical advances $r,s$,
depths $D,D'$ and an arbitrary signed integer bridge size $t$ satisfying
$r\le D'b$, $s\le Da$, $a(r-(D'-D)b)-bs=ct$.
The lower anchor starts at $(b(2q-D_0c),0)$ and its transition is
$(-cr+at,cs+bt)$. Its two coordinates must be nonnegative and its
second increment must be nonnegative. At the end, of depth $D_f$,
its coordinates are $(0,a(2(a+2b)-D_f c))$.
The upper bank starts with advance $D_0 b$, ends with $D_f a$,
and its two total advances are $2c$ each. These conditions include mobile
staircases with signed bridge triangles, backtracking of the lower
horizontal coordinate and arbitrary depth changes. They do not cover
arbitrary lower vertical backtracking or changes of the underlying grid
directions.

## Positive constructions

For $u=4$, use depth 2 throughout and two steps
$(r,s)=(c-b,c-a)$. For $u=7$, use eleven $(3,2)$ steps at depth 1. For $10\le u\le25$ put $K=(u-7)/3$. Start at
depth 3. Use $u+4$ steps taking $m=4$ for the first $K$ and $m=1$
thereafter. Drop from depth 3 to 1 on precisely the last $m=4$ step.
If $\delta$ is the change of depth on a step, put
$$ r=(1+(u+1)m)/3+\delta b,\qquad s=(u-m)/3. $$
These formulas specify all eight finite certificates. The accompanying
program builds the actual triangles and parallelogram grids and invokes
the separate exact verifier on each. It checks side lengths, convex
containment, every pair of block interiors and total area. In particular
it constructs 77,468 tiles for $(85,11,91)$ and 257,468 for $(161,15,169)$.
The underlying unit products are $19367$ and $64367$
respectively (the counts are four times the corresponding unit counts).
The 13,724-tile result at $u=10$ previously had a different staircase.

## Excluding every profile above the cutoff

The following proof assumes $u\ge28$. For cumulative global upper
coordinates $I,J$ including the initial $D_0b$, the lower horizontal
coordinate divided by $b$ is
$$ 2q-[(a+b)I+aJ+D a^2]/c . $$
This follows from the start and the transition identities.
Since $I,J\ge0$, it gives $D\le 2qc/a^2<5$:
$q<2c$ and $c/a=1+(u+2)/(u^2-1)\le1+30/783$. At the end
$D_fa\le2c$, so $D_f\le2$. A terminal zero depth can be removed.
Indeed on the final entrance to zero, $r=0$, $ct=b(Da-s)\ge0$,
and $x'=x+at$ is zero. Thus $x=t=0$ and $s=Da$. This is exactly the final
vertical advance at depth $D$. Any subsequent constant-zero moves are
empty. We may assume $D_f=1$ or 2.

Let $r'=r-(D'-D)b$. The integral coordinates $n,m$ of each move obey
$$
3r'=n+(u+1)m,\quad 3s=un-m,\quad n=[r'+(u+1)s]/c,\quad m\equiv n\pmod3.
$$
For integrality, the displayed lattice ($n=m\pmod3$) has determinant
$a$ in $(s,t)$ coordinates, $3t=um-n$. Its image is contained in
$bs+ct=0\pmod a$, of index $a$ since $\gcd(a,b)=1$. Hence the two
lattices agree. Setting $f=(un+(u+1)m)/3$, the lower horizontal
coordinate divided by $b$ after any prefix equals $2q-Dc-\sum f$.
Its height increment divided by $a$ is $[(u+1)n+m]/3$. In particular
$n\ge0$ by $r'\ge-4b$, $s\ge0$ and $4b<c$. If $n=0$ then $m=0$
by $s\ge0$ and the nonnegative lower height increment.
The upper totals give
$$ \sum n=(2-D_f)u+4,\qquad \sum m=2u-(2+D_f). $$
Write $S=\sum(m-n)$ for a prefix or other group. Over the full path
$S\ge u-7$. Since $r'\le Db$, every move with $n>0$ satisfies $m<2D$
when $D\ge1$. At depth zero $m\le0$. Thus moves starting at depth
at most 2 have $m-n\le0$, by $m=n\pmod3$; those starting at depth 3
have $m-n\le3$, those at depth 4 have $m-n\le6$.

Choose the last vertex of depth at least 3. Such a vertex must exist
to supply positive total $S$, and is followed by a move. If its depth
is 4, its prefix has $\sum f\le2q-4c=-2$. The width formula gives
$S<0$ there; the remaining path can add at most 6, contradicting
$S\ge u-7$. Its depth is thus 3. The prefix before leaving this
last depth-3 vertex has $S\ge u-10$.

On this prefix, $S\le3\sum n$. If there are no depth-4 vertices this
holds move by move since $n>0$ on every positive-surplus move. Otherwise
group the entire initial part through the move out of its last depth-4
vertex into a single block. Immediately before this move $\sum f\le-2$,
so $\sum m\le-\sum n$, and $\sum n\ge1$ since zero-$n$ moves
have $m=0$. The exiting move has $n\ge1$ (its effective $r'$ is positive)
and adds at most 6 to $S$. Thus the block has $S\le4$, $\sum n\ge2$.
Every subsequent move of the prefix starts at depth at most 3.
This proves the asserted bound even for repeated changes of depth.

Finally $3\sum f=(2u+1)\sum n+(u+1)S\ge(5u+4)S/3$. At the last
depth-3 vertex, nonnegative horizontal coordinate gives
$$ (5u+4)(u-10)\le9(2q-3c)=9(c-2)=3(u^2+u-5). $$
Equivalently $(2u+1)(u-25)\le0$, a contradiction.

## A smaller construction problem beyond the cutoff

The simplest depth-2 load that would supply positive surplus is
$(n,m)=(1,4)$. Its effective width is $2b+1$, exactly one unit too large.
In the formal signed grid the excess is an oppositely oriented corner
tile in the adjacent standard triangle of side scale $t=(4u-1)/3=2b-1$.
In the wedge coordinates with unit directions $1$ and $(a+b\rho)/c$,
the correction is the difference between the triangle with intercepts
$(ta,tc)$ and the corner triangle with intercepts $(c,a)$.
Its short straight remnants have lengths $ta-c=b(2a-u)$ and
$tc-a=b(2c-u)$; they pass the scalar side-sum tests. This smaller region
has $t^2-1$ tiles by area, of order $u^2$, compared with order $u^4$ for
the original target. No tiling of this notched triangle is certified here.

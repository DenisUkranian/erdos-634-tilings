# A side obstruction for scale-one notches in the v=1 family

**Statement.** Let $u\ge 4$, $g=\gcd(3,u-1)$,
$a=(u^2-1)/g$, $b=(2u+1)/g$, $c=(u^2+u+1)/g$, with $a>b>0$,
and let $\rho=e^{i\pi/3}$, $z=(a+b\rho)/c$. Take positive integers
$t,k$ for which the triangle with intercepts $(kc,ka)$ on the rays
$(1,z)$ lies strictly inside the triangle with intercepts $(ta,tc)$,
apart from their shared corner and rays: $kc<ta$, $ka<tc$. Delete
the smaller triangle. The resulting convex quadrilateral has successive
vertices $A=ta$, $B=tc z$, $C=ka z$, $D=kc$. If
$$
 BC=tc-ka=h b,\qquad 0<h<a,
$$
it cannot be tiled by congruent $(a,b,c)$ triangles. Reflections and
partial contacts are allowed. This is a theorem about the prescribed
quadrilateral. General unit F2 tilings may avoid it.

The geometric input is the project's 120-degree adaptation of the
stopped-run argument of Beeson and Roşu, §11, Lemmas 32–34
([version 4](https://arxiv.org/html/2607.23453v4#S11)). The published
lemmas concern an exterior side of a particular triangular target.
The short explanation below specifies the hypotheses needed for this
application; the reduction to a single long side does not use formal
verification of the new adaptation.

## Arithmetic and angular data

Write $K=\lfloor a/u\rfloor$. We have $a+c=ub$, $K<u$, $K<b$,
$K<a/u$ (since $u$ cannot divide $a$), and the sides are pairwise
coprime. Any decomposition of $nb$ with $n\le K$ into a sum of whole
sides is pure $b$: after removing matching $b$'s, in
$mb=Xa+Zc$ both $X,Z<b$, so reducing modulo $b$ gives $X=Z$,
forcing $m=uX$ if positive. For $m c=Xa+Yb$ with $m\le K$,
$m+X\equiv0\pmod b$ implies $X\ge b-m$. Thus
$mu b=m(a+c)\ge ab$, contrary to $m\le K<a/u$.
For $m a=Zc+Yb$ the same calculation requires $mu\ge c$.
After cancellation of like summands, these three tests establish purity
of all multiples $na,nb,nc$ up to $K$.

The angle opposite $c$ is $\gamma=120^\circ$; the opposite angles
$\alpha,\beta$ at $a,b$ have $\alpha+\beta=60^\circ$. The rational
$2\cos\beta=(2a+b)/c$ is strictly between 1 and 2, so $\beta/\pi$
is irrational by the root-of-unity algebraic-integer test. Thus acute
tile angles do not split and integer combinations of $\alpha,\beta$
are unique. The quadrilateral angles at $B,C$ are respectively
$\alpha$ and $60^\circ$; the incident outer and inner slants $BA,CD$
have lengths $tb,kb$. Indeed the reference triangles $0AB$ and $0DC$
have sizes $t,k$ and respective angles at $B,C$ equal to $\alpha$
and $\gamma$. At $C$ the complement angle is $\pi-\gamma$.

## Testing the actual side of the quadrilateral

Write its side $BC$ as $Xa+Yb+Zc$, counting the whole edges exposed
on that genuine supporting side. Both $X,Z<b$ since $hb<ab$ and
$c>a$. Reduction modulo $b$ gives $X=Z$, and hence $h=Y+uZ$.
Consequently $Z\le K$. Also $Z\le t-1$ since $BC<tc$.
Put $M=\min(K,t-1)$. At each end of $BC$ the angle is too small for
$\gamma$. Every exposed $a$ or $b$ edge carries $\gamma$ at one end.
Two such $\gamma$ angles cannot share an internal join. This already
excludes $Z=0$ (there would be more required joins than available).

Consider the successive maximal runs of $c$-edges. The gap-count proof
of §11 finds a doubly stopped run: at an interior stop the non-$c$
neighbor presents $\gamma$, and an exterior endpoint is a stop.
For detail, scan the list of non-$c$ edges in order and mark whether
each presents $\gamma$ on its left or right. Include a right-pointing
mark before the board and a left-pointing mark after it. A transition
from right to left needs a nonempty $c$ run between the marks. If it
touches an endpoint, this uses the fact that the first and last non-$c$
edges cannot put $\gamma$ at the board corners. If the entire side is a
$c$ run the two true ends are both stops. Its length $n$ is at most $M$.

The short-run obstruction applies here for the following reasons.

* At an internal $\alpha$ start next to a $\gamma$ stop, the remaining
  sector is just $\beta$, and its tile puts an $a$ or $c$ edge along
  the starting tile's $b$-ray. At $B$, whose full angle is $\alpha$,
  a starting $b$-ray lies on the true wall $BA$ of length $tb>Mb$.
  At $C$, if $kb\le Mb$, the true side $CD$ is pure $b$. Its end
  at $C$ then shows $\alpha$, since its other possible endpoint angle
  $\gamma$ does not fit. The next tile on $BC$ shows $\beta$; hence
  a $c$-tile on $BC$ showing $\alpha$ cannot start at this short
  wall. If $kb>Mb$, an $\alpha$ at the $60^\circ$ corner has an
  adjacent $\beta$ (and the true wall itself also continues past $Mb$).
* If both stops of the run show $\beta$, an internal switch shows
  $\alpha,\alpha$. Its complementary sector $\pi-2\alpha=
  \alpha+3\beta$ has no $\gamma$ and exactly one $\alpha$, so at
  least one of the two starts has an adjacent $\beta$. Scan from
  that protected $\alpha$ toward its stop, shortening the run if
  necessary. This is the change in the angle counts in Lemma 34.
* From a protected start the triangle and trapezoid inductions of
  Lemmas 32 and 33 use purity of $wa,wb,wc$ for $w\le n$ and the
  two sectors $\pi-\gamma=\alpha+\beta$ and
  $\pi-\alpha-\gamma=\beta$. Each is available here. Purity makes
  the starting wall continue through the end of the short grid when
  opposite to a distinct edge; a true continuous wall at $B$ works
  for all $w\le n$. Interior joints and internal stops are backed by
  the same side $BC$ throughout. If the induction terminates at a
  vertex of the quadrilateral, its angle is either $\alpha$ or
  $60^\circ$, both strictly larger than $\beta$. Thus the terminal
  diagonal has tiles on its other bank and is clamped at the vertex,
  as in the article at lines 952 and 975. The forced $\gamma$ there
  cannot fit. The internal-stop conclusion instead contradicts the
  adjacent $\gamma$, as in lines 950–951 and 974–981. A tile
  cannot overhang a true vertex across its incident side. No other
  corner enters this terminal argument.

Thus a doubly stopped run has length greater than $M$, contradicting
$Z\le M$. This argument also covers the formerly problematic case
$kb\le Kb$. It is important to check the tile on the short adjacent
side at $C$, and to distinguish a run starting there from one ending
there. The integer inventory alone is only an upper bound.

| Full-board count | Tile | $t,k$ | Notch count | $BC=h b$ | $K$ | $CD$ |
|---:|---|---|---:|---:|---:|---:|
| 3431 | 33,7,37 | 13,8 | 105 | 217 = 31·7 | 3 | 56 |
| 3431 | 33,7,37 | 26,23 | 147 | 203 = 29·7 | 3 | 161 |
| 5063 | 35,13,43 | 11,2 | 117 | 403 = 31·13 | 5 | 26 |
| 5063 | 35,13,43 | 22,17 | 195 | 351 = 27·13 | 5 | 221 |

For the 117 case in particular, $CD=2b$ has two $b$ edges and
$BA=11b>5b$. The maximum possible count of $c$ edges on $BC$ is
five, and the stopped-run proof requires at least six.

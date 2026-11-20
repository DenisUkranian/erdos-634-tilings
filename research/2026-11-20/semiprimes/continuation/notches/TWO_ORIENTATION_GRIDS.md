# Rigidity and enumeration at the first mixed scales

Use the two orientations $A,B$ and the tip coordinates of the
[notch theorem](TWO_ORIENTATION_NOTCH.md). In this note a tiling of
$tA$ may use any translates and half-turns of these two orientations.
No particular position, even at a corner, is prescribed in advance.
Two different partitions of the fixed triangle are counted separately.

If $t<a+c$ there is exactly one tiling, the ordinary $t^2$ grid.
If $t=a+c+d$ with $0\le d<a$, the exact number is
$$
 1+\binom{d+a+1}{a+1}+\binom{d+c+1}{c+1}-\binom{d+2}{2}.
$$
In particular the unique alternative at $t=a+c$ is exchanging the
entire $ac$ by $ac$ cell at the cone apex. At the next scale the total
number of tilings is $a+c+2$, including the ordinary tiling. The axes
are oblique in the physical metric.

## Proof

Remove the prescribed $t$ boundary half-tiles as in the notch theorem.
The remaining staircase has horizontal sections of widths multiple
of $a$ and vertical sections of heights multiple of $c$. Its unit
rectangles have sizes $a$ by $c$ (ordinary) or $c$ by $a$ (exchanged).
If there are no exchanged rectangles, the subdivision is unique. Every
horizontal line off the finitely many edges determines the starting
$x$ coordinates by measuring successive intervals of length $a$ from
zero. Vertical lines determine the $y$ coordinates in the same way.
Each rectangle's triangular subdivision is unique, as its slant
direction is prescribed.

On any generic horizontal line the number of exchanged rectangles is
a multiple of $a$, while on every generic vertical line it is a
multiple of $c$. Thus each occupied section contains length at least
$ac$ of exchanged rectangles, in either slicing direction. In the whole
triangle the available height is $c(t-x/a)$ and the available width is
$a(t-y/c)$. Hence the exchanged rectangles lie within
$$ 0\le x\le a(t-a),\qquad 0\le y\le c(t-c). $$
If any such rectangle occurs, a horizontal slice through it already
requires $ac\le a(t-a)$, proving rigidity at every $t<a+c$.

In the stated range $0\le d<a<c$, both bounds in this display are
strictly less than $2ac$. Thus each nonempty horizontal slice meets
exactly $a$ exchanged rectangles, and each nonempty vertical slice
exactly $c$. Begin at the leftmost exchanged rectangle. All $c$
rectangles there start at the same horizontal coordinate (the generic
section just to the right meets $c$), and all have width $c$. No further
rectangle can enter before these $c$ end simultaneously. Repeat after
their end, ignoring any intervening empty interval. This partitions
the entire exchanged $x$ support into $m$ intervals of width $c$,
with every exchanged rectangle starting at a left endpoint. In $y$
there are similarly $n$ elementary intervals of width $a$. Counting
these rectangles gives $mc=na$; by the horizontal upper bound $m<2a$.
Since $\gcd(a,c)=1$, necessarily $m=a,n=c$.

Each occupied row therefore meets every exchanged $x$ interval, so
the exchanged union is the Cartesian product of the $a$ intervals in
$x$ with the $c$ intervals in $y$. Along a generic occupied row, the
initial empty space and all gaps between the $x$ intervals consist of
ordinary rectangles of widths $a$, hence have widths divisible by $a$.
Similarly the initial and internal $y$ gaps have heights divisible by
$c$. Count $X$ units of $a$ in the horizontal gaps and $Y$ units of $c$
in the vertical ones (always excluding trailing space). Since the
product's top right corner lies in $tA$,
$$ (ac+aX)/a+(ac+cY)/c\le t,\qquad X+Y\le d. $$

There cannot be internal gaps in both directions. Suppose an internal
$x$ gap follows $m_0$ exchanged columns, $0<m_0<a$, and an internal
$y$ gap follows $n_0$ exchanged rows, $0<n_0<c$. Pick a generic $x$
strictly inside that $x$ gap. The vertical line there is all ordinary
and its rectangle ends occur only at multiples of $c$. The bottom
level of the $y$ gap is $n_0a$ modulo $c$, nonzero. Thus a single ordinary
rectangle through that $x$ crosses the bottom of the $y$ gap. On its
lower side an occupied row forces this rectangle's $x$ phase to be
$m_0c$ modulo $a$, since $m_0$ exchanged rectangles occur to its left.
On its upper side an all-ordinary row forces phase zero. Coprimality
makes these requirements inconsistent. The enclosing staircase contains
the full box up to the top right of the exchanged support since the
staircase is coordinatewise downward closed.

Conversely, if the internal gaps occur only in $x$, take an $A$-grid
aligned bounding rectangle of height $ac$ and width $ac$ plus all
internal gap widths. Translate it by the chosen initial offsets,
multiples of $a$ in $x$ and of $c$ in $y$. The budget $X+Y\le d$
puts its top right corner in $tA$, so the aligned rectangle is a union
of full ordinary cells. In it tile the designated width-$c$ columns by
exchanged rectangles and the gaps by ordinary rectangles. Outside it
use the ordinary grid. The case of internal gaps only in $y$ is symmetric.
Given these gaps the ordinary subdivision also is unique: at any
generic row each ordinary interval is partitioned from its left end
in steps of $a$, and at each generic column in steps of $c$.

With no internal $y$ gaps, there are $a-1$ internal $x$ gaps and
two initial offsets, subject to the budget $d$. This gives
$\binom{d+a+1}{a+1}$ solutions. With no internal $x$ gaps there are
$\binom{d+c+1}{c+1}$; exactly $\binom{d+2}{2}$ solutions use only
initial offsets and occur in both counts. Add the single ordinary grid
with no exchanged rectangles.

## Arithmetic checks

The independent `check_near_threshold.py` fills the rectangle staircase
from its lowest leftmost available unit cell and counts all covers by the
two allowed rectangle sizes, using integral column heights. For the
physical $(a,b,c)=(5,3,7)$ tile it compares the formula with direct
counts. Several other small coprime pairs $a,c$ check the rectangular
enumeration separately. The proof itself allows arbitrary translations.

## Number of actual notch fillings in this range

At $t=a+c+d$, $0\le d<a$, with a prescribed nonzero exchanged corner
$kB$, the same argument counts all allowed tilings of the remaining
notch exactly. For $1\le k\le a$ the answer is
$$
 \binom{d+a-k}{a-k}+\binom{d+c-k}{c-k}-1 .
$$
For $k>a$ it is zero by the sharp threshold. Indeed completion with
the fixed $B$ grid in $kB$ forces both initial offsets to vanish and
the first $k$ exchanged columns and first $k$ exchanged rows to touch
without gaps. This follows by looking arbitrarily close to the two
cone axes, where the inserted triangle occupies widths approaching
$kc$ and $ka$, respectively. Conversely these contiguous initial
bands put $kB$ exactly on its $B$ grid with a supported slant. The
internal slots left in the horizontal and vertical cases are therefore
$a-k$ and $c-k$, respectively. Only the pattern with no gaps occurs
in both counts.

## Arbitrary triangle angles and irrational side ratios

The threshold, rigidity and enumerative proofs use only the two unequal
incident lengths and an exchange by reflection in their bisector.
Consequently they hold for a triangle with **any** nondegenerate
angle at the chosen corner and any ratio of its incident side lengths.
For a rational ratio, normalize the two lengths to relatively prime
integers $a<c$ and use the formulas above. The other side need not
be rational. The descriptions $a$ by $c$ always mean lengths in the
two unit cone directions, not a requirement on their physical angle.

If the incident lengths have irrational ratio, take any of the same
integer homotheties $t$. At a generic horizontal section the total
staircase width is a multiple of the first length. Any positive number
of exchanged rectangles would express a nonzero multiple of the other
length as an integer multiple of the first. Hence the exchanged
orientation is impossible throughout, and the ordinary grid is the
unique tiling in the two permitted classes for all $t$.

If unequal incident rational lengths meet at any vertex of a given
triangle, the rational case therefore supplies an explicit nonstandard
tiling of its integer homotheties starting at the sum of the coprime
numerator and denominator of that side ratio. It classifies only the
two chosen classes and their half-turns. The identification with all
boundary-direction tiles in the notch theorem was proved separately for
the specified 120-degree tiles.

## Prior rhombus exchange

Beeson already exhibited the local rhombus flip in the case of
commensurate sides $3a=2b$, with an interior version leaving the
boundary unchanged. See [Triangle Tiling I, Figure 14 and the paragraph
before Section 6](https://www.michaelbeeson.com/research/papers/TriangleTiling1.pdf).
The simple flip itself is prior work. The sharp exclusions and
enumeration above concern what all tilings in the specified orientation
classes can do.

# Round 3: an elementary squarefree exclusion in the third target branch

29 September 2026. This note proves a new-to-this-session necessary condition for
isosceles targets with base angles alpha+beta. It does not solve all composite
cases of Erdős 634. No claim of priority or external review is made.

## 1. Setup and theorem

Let a primitive rational tile have sides

    a=uv, b=v²-u², c=v², 0<u<v, gcd(u,v)=1,

and opposite angles alpha,beta,gamma. Then 3alpha+2beta=pi and

gamma=2alpha+beta>pi/2. Consider an isosceles triangle with apex angle
alpha and base angles theta=alpha+beta, tiled by N congruent copies of this
tile, allowing arbitrary T-junctions and reflections. Write

    b=q h²,

where q is squarefree and h is a positive integer.

**Theorem.** Necessarily N=q t² for a positive integer t, and

    q h(t-h) >= v.

In particular t>h, N>b, and **N is not squarefree**.

The proof below is independent of the newly proposed beta and W scale-one
exclusions. For an initially unspecified tile with 3alpha+2beta=pi, the
published rationality theorem (Beeson, arXiv:1206.2229v4, Theorem 9) reduces
it to the displayed primitive rational form.

## 2. Elementary boundary lemma

Suppose an obtuse triangular tile has obtuse angle gamma and opposite side c,
and a tiled polygon has all its corner angles strictly less than gamma. Then
**every side of the polygon contains at least one whole c edge**.

Indeed, the tile edges lying on a fixed polygon side form a finite partition of
that side into whole tile edges. If there are n edges and none has type c, each
has exactly one endpoint where its tile contributes gamma. No polygon corner
can carry such an endpoint. There are only n-1 interior junctions of the boundary
partition; at each, at most one tile can contribute gamma, because 2gamma>pi.
Thus n obtuse-angle endpoints would have to fit at n-1 points, a contradiction.

T-junctions in the interior do not affect this argument. Boundary tile edges
are whole edges: a tile edge on the supporting line cannot extend past a polygon
corner while the tile remains contained in the polygon. Two boundary edges
cannot overlap over a positive interval, since their tiles would overlap in an
open region on the polygon's interior side.

For the target of Section 1, alpha<gamma and theta=alpha+beta<gamma, so the
lemma applies to all three sides.

## 3. The apex is a single alpha corner

We have 2cos(alpha)=2-u²/v², a rational number strictly between 1 and 2.
If alpha/pi were rational, 2cos(alpha) would be a rational algebraic integer,
hence an integer, a contradiction. Thus alpha/pi is irrational.

If a fan at the target apex contains p alpha angles, r beta angles and s gamma
angles, then

    p alpha + r beta + s gamma = alpha.

Using beta=(pi-3alpha)/2 and gamma=(pi+alpha)/2 gives

    (2p-3r+s-2) alpha + (r+s) pi = 0.

Irrationality implies r+s=0 and p=1. Thus exactly one tile has its alpha
corner at the apex. Its incident sides are b and c, so at least one equal side
of the target contains a whole b edge starting at the apex.

## 4. Area plus one boundary congruence

Let X be the common length of the target's equal sides. Twice its area is
X² sin(alpha); twice the tile's area is b c sin(alpha). Consequently

    X²=Nbc=N b v².

The target side is partitioned into tile edges of integer lengths, so X is an
integer. Since v² divides X², v divides X. Hence (X/v)²=Nb is an integer
square. Comparing prime valuations with b=q h² gives N=q t² for an integer
t>0, and

    X=v q h t.

Choose the equal side containing the b edge forced in Section 3. Write its
whole-edge counts as A,B,C. Then

    X=Auv+B(v²-u²)+Cv².

Modulo v, gcd(b,v)=1 and v|X imply v|B. Since B>0, B>=v.
The boundary lemma gives C>=1 on this same side. Thus

    v q h t = X >= v b+c = v q h²+v².

Dividing by v yields the claimed inequality q h(t-h)>=v. In particular
t>=h+1, which rules out squarefree N (for which t=1).

An explicit count form of the same necessary condition is

    N >= q (h+ceil(v/(q h)))².

The weaker but especially simple consequence N>b is often enough.

## 5. An alternative geometric endpoint proof

For squarefree N the area identity gives b=N h² and X=Nvh. If h>=2,
one equal side cannot contain any b edge at all: the congruence requires at
least v such edges, whose length vb=Nvh² exceeds X. This contradicts the apex.
If h=1, those v b edges exhaust X, leaving no room for the mandatory c edge.
Again a contradiction.

Alternatively, in the h=1 case attach two quadratic tile-triangles of scale v
to the original isosceles triangle. The enlarged triangle has sides

    v³, v³, u(3v²-u²),

and 3v²-u² tiles, so the beta scale-one exclusion also rules it out. The direct
boundary proof above is shorter and avoids any dependence on that newer result.

## 6. Consequences and exact remaining scope

After combining this theorem with the current W and beta scale-one proof
candidates, squarefree counts are excluded in THREE of the five rational
3alpha+2beta=pi target shapes:

1. W shape (2alpha,beta,alpha+beta): by the separate W scale-one argument;
2. base-beta isosceles: by the separate beta scale-one argument;
3. base-(alpha+beta) isosceles: by the elementary proof here.

The remaining shapes are still real obstructions:

* scalene (2alpha,alpha,2beta), with necessary count
  N=k²(2v²-u²)(3v²-u²). The realized squarefree example 77 (u=1,v=2)
  prevents any claim that this branch also has no squarefree counts;
* base-alpha isosceles, with N(v-u)=j²(v+u)(2v²-u²). This note does not
  prove or disprove the squarefree members of this family.

The irrational 60-degree and 120-degree tile families also remain in the full
problem. In particular this result says nothing decisive about the independent
N=105 instances recorded in [the frontier note](n105-partial-results.md).

## 7. A useful exact reduction for the surviving base-alpha shape

The base-alpha isosceles target has equal side X and base Y=X(2v²-u²)/v².
Put A=2v²-u². Its area equation is

    A X² = N b v⁴.

Since gcd(A,v)=1, v² divides X. Write X=v²H; then

    A H²=Nb,   gcd(A,b)=1.

If N is squarefree, prime valuations imply A is squarefree and divides N.
Writing N=AD gives

    b=D h², H=Dh, X=v²Dh, Y=ADh.

The coloring divisibility in Beeson's Theorem 25 further requires

    v+u divides Dh.

These are exact necessary reductions, not a construction. For example
(u,v)=(1,2) gives (A,b,D,h,N)=(7,3,3,1,21), and (u,v)=(2,3) gives
(14,5,5,1,70). The new boundary bound in the previous sections does not transfer
to this target: its equal side is v²Dh, while the minimal positive number of
b edges is v, so their total length vb=vDh² is smaller than X because h<v.
Claiming the same contradiction here would therefore be false.

The base-alpha reduction does yield a simple squarefree necessary criterion:
A must be squarefree and the squarefree kernel D of b must be coprime to A;
the candidate count is uniquely N=A*sf(b) for each primitive pair (u,v),
subject to v+u|sf(b)*sqrt(b/sf(b)). The gcd is automatic from gcd(A,b)=1.
It remains a necessary arithmetic list, not a sufficiency theorem.

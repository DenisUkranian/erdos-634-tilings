# Independent audit: the c-side cap obstruction

29 September 2026. Separate internal audit of the proposed proof. Verdict: both cases pass. This is an internal mathematical
check, not external review or a formal proof-assistant certificate.

## Statement

Let u,v be coprime integers with 1<u<v, and let the tile have primitive sides

    a=uv, b=v²-u², c=v²

and corresponding angles alpha,beta,gamma, so 3alpha+2beta=pi and
gamma=2alpha+beta>pi/2. Set theta=alpha+beta=pi-gamma.

No convex polygon having a side AB of length c and interior angles gamma at A
and theta at B can be tiled by congruent copies of this tile.

## Short side-atom lemma

Each of a,b,c has exactly one representation as a nonnegative integer sum of
a,b,c: itself. Here coefficients count whole edges and at least one is positive.

For b: if a representation contains a b, it is exactly that b. Otherwise its
right-hand side is divisible by v whereas b is coprime to v.

For a: reduction modulo v shows the coefficient of b is a multiple of v.
But vb>a because b>u, so this coefficient is zero. Division by v then gives
u=A u+C v; since 0<u<v, only A=1,C=0 is possible.

For c: similarly the coefficient of b is a multiple of v. But
b>=2v-1>v, so vb>c; that coefficient is zero. Division by v gives
v=A u+C v. If C=0 then u divides v, contradicting u>1 and gcd(u,v)=1.
Thus C=1,A=0.

Consequently AB is exactly one whole c edge of a tile T0. Write R for T0's
third vertex; its angle there is gamma.

## Genuine endpoint argument

Whenever a side BR of T0 runs strictly inside the polygon's angle at B, the
opposite side of BR has a chain of whole tile edges starting at B. If a tile
edge of that chain crosses R, it is an actual edge with R in its relative
interior and the crossing tile contributes a straight angle pi at R.

If the opposite chain instead had an endpoint exactly at R, all its edges
would be wholly within BR, since no edge can extend backward past B by
convexity. Its edge lengths would therefore give a whole-edge representation
of |BR|. The side-atom lemma rules this out when its first edge has a type
different from BR.

Once R lies inside a crossing edge on the line BR, the extension of AR beyond
R enters the interior of that crossing tile. The extension of AR backward
past A leaves the convex polygon. Thus the opposite chain along AR has true
whole-edge endpoints at both A and R. It cannot be merely a chain truncated
at a T-junction. The side-atom lemma applies to this second chain.

These are the critical geometric facts. They remain true if the tiling has
other T-junctions or if the polygon has more than four sides.

## Case 1: T0 has alpha at A and beta at B

At B the remaining fan is alpha, necessarily one alpha corner. (Irrationality
of alpha/pi and beta=(pi-3alpha)/2, gamma=(pi+alpha)/2 give uniqueness.)
Its edge on BR has type b or c, whereas |BR|=a. The side-atom lemma forces
R to be in the interior of a crossing edge as described above.

Now |AR|=b and its opposite chain has true endpoints A,R. It is therefore
one whole b edge of a tile T1. At A the unfilled angle after T0 is
gamma-alpha=theta<gamma. The b-edge endpoint of T1 is either alpha or gamma;
hence it is alpha at A and gamma at R. At R, T0,T1 and the crossing tile have
disjoint interior sectors with total angle

    gamma+gamma+pi>2pi,

which is impossible.

## Case 2: T0 has beta at A and alpha at B

At B the remaining fan is beta, necessarily one beta corner. Its edge on BR
has type a or c whereas |BR|=b. Again R lies in a crossing edge.

The opposite chain along AR has length a and true endpoints A,R, so it is
one whole a edge of a tile T1. At A, after T0, the residual fan has angle

    gamma-beta=2alpha.

Irrationality implies that this fan consists of exactly two alpha corners.
But a tile incident through an a edge has beta or gamma at that endpoint,
never alpha. Contradiction.

## Scope

The proof genuinely establishes the stated arbitrary-convex-polygon cap
obstruction. In particular, any parallelogram with adjacent angles gamma and
theta and one side c is excluded, regardless of the other side's length.
It does not by itself show that a specified larger triangle contains such a
cap as an actual tiled subregion: that removal/forcing step must be proved
separately for every application. Nor does the proof immediately extend from
side c to a side n c with 1<n<u, since the longer boundary can consist of
several differently oriented c-edge tiles.

# The forced corner at Y in the 250-tile pentagon

**Proposition.** In the one-step pentagon for the tile $(a,b,c)=(35,13,43)$
and $(t,k,s,j)=(22,17,8,1)$, the tile at $Y$ has its $120^\circ$
angle there. Put $Y=(0,0)$ temporarily in the physical Eisenstein frame
$1,\rho$, $\rho=e^{i\pi/3}$. The unique prescribed tile is
$$ Y,\qquad Y+(0,-35),\qquad Y+(13,0). $$
The proof allows reflections and T-junctions, without a height palette.

**Data needed from the pentagon.** Its successive corners are
$X',Y,W,D,D'$. The true lengths at issue are
$X'Y=329$, $YW=39$, $X'D'=364$. The angles at $X',Y$ are
$\alpha,\gamma$, where $\alpha,\beta,\gamma$ are opposite $35,13,43$.
In particular $\gamma=120^\circ$ and $\alpha+\beta=60^\circ$.
Here $\alpha>\beta$. Also $2\cos\beta=83/43$ is rational and
nonintegral, which excludes a root of unity for $e^{i\beta}$.
Consequently the ratio $\alpha/\beta$ is irrational, and the numbers of
$\alpha$ and $\beta$ in any angle fan are forced after substituting
$\gamma=2\alpha+2\beta$. A fan in a true convex corner has a common
vertex there; no tile edge can pass straight through that corner.
Every true side is a concatenation of whole edges.

Assume the proposition fails. Since $39$ has only the edge decomposition
$3b$, the tile abutting $YW$ at $Y$ has angle $\alpha$ there:
its alternatives on a $b$ edge are $\alpha,\gamma$. At this corner
the presence of any $\gamma$ would exhaust the whole corner and
already prove the proposition. Neither $Y$ nor $X'$ can therefore
have a $\gamma$ under the contrary assumption.

**A short stopped run on $X'Y$.** The complete decompositions of
329 into lengths $35,13,43$, recorded as counts $(x,y,z)$, are
$(0,22,1),(1,16,2),(2,10,3),(3,4,4)$. In particular $z\le4$.
In addition, for $\ell=1,2,3,4$ each of $\ell a,\ell b,\ell c$
decomposes into whole tile edges only homogeneously. Both claims can
be verified by looping $0\le x\le L/35$, $0\le z\le(L-35x)/43$
and requiring $L-35x-43z\in13\mathbb Z_{\ge0}$.

Mark a non-$c$ edge on $X'Y$ by the endpoint at which it presents
$\gamma$. Two marks cannot face one another at a single point of the
side because $2\gamma>180^\circ$. Reading from $X'$ to $Y$, append a
right-pointing fictitious mark before the sequence, and a left-pointing
one after it. A right-to-left transition in this list gives a nonempty
run of $c$ edges. At an ordinary transition its two neighboring tile
edges present $\gamma$ towards the run. At a true endpoint the run
cannot be empty because that vertex carries no $\gamma$. Call either
such endpoint a stop. The run has length $nc$ with $1\le n\le4$.

Here is the local short-run argument used for this particular side.
It is the triangle/trapezoid induction of Beeson and Roşu,
[§11, Lemmas 32–34](https://arxiv.org/html/2607.23453v4#S11),
with the following input checks for the $120^\circ$ tile and this polygon.
At a stopped endpoint which shows $\alpha$ on its $c$ edge, the
$b$ ray entering the polygon must be protected, meaning that an $a$
or $c$ edge starts opposite it on that ray, or that it lies on a true
wall continuing farther than $4b$.

* If the stop is internal to $X'Y$, the $\gamma$ from its neighbor
  leaves $180^\circ-\gamma-\alpha=\beta$. This one $\beta$ tile gives
  an $a$ or $c$ edge on that ray.
* An $\alpha$ start at $X'$ uses its entire corner. Its $b$ ray is on
  $X'D'$, a continuing wall of length $364>4b$.
* If the $c$ edge shows $\alpha$ at $Y$, the $b$-edge tile on $YW$
  also shows $\alpha$ there. These tiles are distinct because a single
  corner tile filling both rays would have angle $\gamma$ at $Y$.
  The sector between their interior rays is $\gamma-2\alpha=2\beta$,
  consisting exactly of two $\beta$ angles. The first supplies $a$ or
  $c$ on the incoming $b$ ray. The short wall $YW=39<4b$ need not
  continue past the putative grid.
* If neither endpoint shows $\alpha$, the initial and final $c$
  edges show $\beta$ at their stops. There is an interior
  $\alpha$--$\alpha$ switch. Its complementary sector on the tiled side
  of the line is $180^\circ-2\alpha=\alpha+3\beta$. It has no
  $\gamma$ and only one $\alpha$. At least one of the two boundary
  $\alpha$ tiles consequently has an adjacent $\beta$. Start there
  on that protected side and proceed toward its corresponding true or
  internal stop. This is the $120^\circ$ angle-count adjustment to
  the starting choice in Lemma 34.

For clarity, the local induction has the following mechanism. With
the base given by the chosen sequence of $c$ edges, grow a standard
triangular grid from the protected $\alpha$ start. At grid width $w$
its starting bank is $wb$. If an opposite bank beginning with $a$ or
$c$ terminated there, $wb$ would have a forbidden decomposition.
A genuine starting wall works by continuing beyond $wb$. The other
diagonal is a clamped $wa$ bank: its far upper sector
$180^\circ-\gamma=\alpha+\beta$ permits no $\gamma$. By homogeneous
decomposition it has $w$ opposite $a$ edges. Each has one $\beta$
and one $\gamma$, and $2\gamma>180^\circ$ forces their ordering down
the diagonal. This puts $\gamma$ at its lower end. If a north-bank
tile diverges when extending a column, the trapezoid step of Lemma 32
uses a length $mc$ with $m<w$ containing a mismatched $b$ to force
an overhang. Its diagonal of length at most $wa$ is then clamped and
gives the same forced ordering. The surviving point sectors in these
two inductions are $\alpha,\beta,\alpha+\beta$, with acute angles
indivisible; those are the only sector properties used. Purity above
applies to every $w,m\le4$. All points in this argument are on the
chosen true side or inside the convex polygon. The true side provides
the same filled exterior half-plane as in the cited proof.

The terminal condition is important. At an internal stop a
$\gamma$ is already present outside the run, and the other forced
$\gamma$ cannot fit there. Equivalently, the terminal $\alpha$-sector
cannot furnish an $a$ edge on the clamped diagonal (Lemmas 32–33).
At an actual endpoint $X'$ or $Y$, its angle is strictly greater than
$\beta$, so there are tiles on the far side of the terminal diagonal.
It is clamped at the true vertex, as in §11 at the end of the
trapezoid induction and in the final triangle step. The forced
$\gamma$ cannot occur at $X'$ (angle $\alpha$) or at $Y$ (under the
contrary assumption). In particular the terminal $c$-edge tile has a
positive angle at that vertex. This endpoint check is only about
$X'Y$, with no use of the larger angle at $W$.

The induction is impossible at the stop, contradicting the assumed
tiling with no $\gamma$ at $Y$. With $\gamma$ at $Y$, the full corner
belongs to a single tile whose two incident edges are $a,b$; $YW$ is
pure $b$, forcing the coordinates in the statement.

This proposition prescribes one tile. A separate finite or geometric
argument is needed to decide whether the rest of the pentagon tiles.

# Two longest edges on each side of the (8,7,13) F1 target

> **Historical stage — 29 September 2026.** Its limited claims remain as written. The later [global N=105 proof](n105-global.md) supersedes statements here that the count is unresolved. These old partial certificates are retained as regression evidence, not as the new proof.

29 September 2026. Research directed by Denis Paliy, with ChatGPT assistance.
This is an internally checked geometric argument, not an externally refereed
result or a decision of N=105.

**Proposition.** If a triangle with sides $(105,56,91)$ is tiled by congruent
triangles with sides $(8,7,13)$, each outside side contains at least two whole
edges of length 13. Consequently its side of length 56 consists of exactly
two edges of each length 7, 8 and 13. Reflections and T-junctions are allowed.

## Proof

Write $a=8$, $b=7$, $c=13$. Let $\varepsilon$ and $\delta$ be the tile angles
opposite $a$ and $b$, respectively, and $\Gamma$ the angle opposite $c$.
Then $\Gamma=2\pi/3$, $\varepsilon+\delta=\pi/3$, and
$0<\delta<\varepsilon$. Also $2\cos\delta=23/13$, so $\delta/\pi$ is
irrational: a rational value of $2\cos$ at a rational multiple of $\pi$
would be an integer. By the cosine rule the target angles are
$\varepsilon$, $\varepsilon+\delta$, and $\varepsilon+2\delta$;
all are less than $\Gamma$.

A target side is a chain of whole tile edges. Each $a$-edge or $b$-edge in
that chain contributes a $\Gamma$ angle at one endpoint. No target corner
can accept $\Gamma$, and no internal junction along the side can accept
two such angles. A side with $m$ edges and no $c$-edge would therefore need
$m$ distinct internal junctions, but has only $m-1$. Thus it has a $c$-edge.

Suppose it has exactly one, $PQ$. Orient its tile $PQR$ so that the tile
angles at $P,Q,R$ are $\delta,\varepsilon,\Gamma$, respectively.
Thus $PR=a$ and $QR=b$. The other $m-1$ boundary edges now account for
exactly one $\Gamma$ at every internal junction. No additional tile can
have its $\Gamma$ angle at $P$ or $Q$ (whether they are junctions or target
corners).

If $Q$ is an internal junction, removing its existing $\Gamma$ and
$\varepsilon$ leaves an angle $\delta$. If $Q$ is a target corner, the
angle left beside $QR$ is $0$, $\delta$, or $2\delta$. An angle $k\delta$,
for $k=1,2$, can only be filled by $k$ tile angles $\delta$: substituting
$\varepsilon=\pi/3-\delta$ and $\Gamma=2\pi/3$ into any nonnegative
integer angle inventory and using irrationality proves this assertion.

If the remaining angle is zero, $QR$ is external and $R$ lies on the target
boundary. Otherwise the first tile across $QR$ has angle $\delta$ at $Q$.
Its edge along that ray has length $a$ or $c$, both greater than $b$.
Consequently $R$ lies in the relative interior of this edge, and that tile
occupies a straight angle at $R$. In either case no further tile can have
angle $\Gamma$ at $R$: either $2\Gamma>\pi$ on the target boundary, or
$\pi+2\Gamma>2\pi$ at the crossing tile.

The edge $PR$ is internal. If it were external, the target angle at $P$
would be $\delta$, which is absent from the target's three angles.
On the opposite side of $PR$ there is a chain of whole tile edges with
total length $a$. Here is why no edge can overrun an endpoint: at $P$ an
overrun crosses the supporting line of the target boundary; at $R$ it
either crosses the target boundary or enters the interior of the tile
whose transverse edge contains $R$. These barriers also cover T-junctions.

No edge in this chain can have length $c>a$. An edge of length $a$ would
occupy the entire chain and place its $\Gamma$ endpoint at $P$ or $R$,
both impossible. All edges must therefore have length $b$. This would give
$8=7k$ for a positive integer $k$, a contradiction.

Finally let $A,B,C$ be the numbers of length-8, length-7, length-13 edges
on the side 56. They satisfy

$$8A+7B+13C=56,\qquad C\ge2.$$

For $C=2$, reduction modulo 7 gives $A=2$ and then $B=2$.
For $C=3$, $8A+7B=17$ has no nonnegative solution; for $C=4$, its
right side is 4; larger $C$ are impossible. This proves the proposition.

## What this does and does not settle

The short side has only $6!/(2!2!2!)=90$ edge-length orders. Each edge has
two inward reflected placements, so there are at most $90\cdot2^6=5760$
initial side configurations before geometric filtering. This is a finite
reduction for that side, not a proof that all configurations fail or extend.
The proposition does not decide the F1 target or the full problem.

The same argument works for primitive integer $120^\circ$ tiles with
$a>b>1$ and target angles $\varepsilon,\varepsilon+\delta,
\varepsilon+2\delta$: its last contradiction is $b\mid a$ versus
$\gcd(a,b)=1$. The explicit target above is the case used here.

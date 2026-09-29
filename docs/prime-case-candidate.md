# No scale-one triangle in either rational Group-1 family

29 September 2026. **Proof internally checked, not externally reviewed.** The reverse-apex argument and the scale-one W argument in the appendix received separate internal adversarial checks; no gap was found. A further reviewer, without the earlier discussion, independently reconstructed both geometric arguments and found no gap. These are internal mathematical reviews, not external refereeing, formal verification or a claim of research priority.

## Main theorem and its geometric idea

Let $0<u<v$, $\gcd(u,v)=1$, and put

$$
a=uv,\qquad b=v^2-u^2,\qquad c=v^2,\qquad
P=3v^2-u^2,\qquad Q=2v^2-u^2.
$$

Let the congruent tile have sides $(a,b,c)$ opposite angles $(\alpha,\beta,\gamma)$. Then $3\alpha+2\beta=\pi$ and $\gamma=2\alpha+\beta>\pi/2$.

**Theorem.** The isosceles triangle with sides $(v^3,v^3,uP)$ cannot be tiled by these tiles. Its area would require exactly $P$ tiles. The triangle with sides $(v^3,uQ,vb)$ cannot be tiled by these tiles either; its area would require $Q$ tiles.

The second assertion is the scale-one W theorem, proved in the appendix. The new argument reduces the first assertion to the second by an actual dissection: starting at the three-$\alpha$ apex, it forces a standard $v^2$-tile corner. Its complement is exactly the forbidden W triangle.

These are statements about the full scale-one families. They do not classify larger-scale composite tilings or by themselves solve every part of Erdős problem 634.

## Elementary angular and arithmetic facts

The number $\alpha/\pi$ is irrational: $2\cos\alpha=2-u^2/v^2$ is rational strictly between 1 and 2, whereas for a rational multiple of $\pi$ it would be a rational algebraic integer, hence an integer. Consequently the tile-angle inventories at a $\beta$ corner, an $\alpha$ sector, a $\theta=\alpha+\beta$ sector, and a $3\alpha$ apex are respectively one $\beta$, one $\alpha$, one $\alpha$ plus one $\beta$, and three $\alpha$ sectors.

We need three exact positive-chain facts. All coefficients count whole edges and are nonnegative integers.

$$
ib=Aa+Bb+Cc,\quad0<i<v
\ \Longrightarrow\ A=C=0,\ B=i. \tag{1}
$$

Indeed $B\equiv i\pmod v$ and $0\le B\le i$.

$$
ia=Aa+Bb+Cc,\quad0<i<v
\ \Longrightarrow\ B=C=0,\ A=i. \tag{2}
$$

Write $B=v\ell$ and $\ell v+C=T u$; division of the length equation gives $i=A+(T-\ell)v+\ell(v-u)$. If $\ell+C>0$, then $Tu=\ell v+C>\ell u$, so $T>\ell$ and $i\ge v$, impossible.

$$
nc=Aa+Bb+Cc,\quad0<n<v
\ \Longrightarrow\ B=0,\ A=vh,\ C=n-uh
\quad\text{for an integer }h\ge0. \tag{3}
$$

To prove (3), write $B=v\ell$ and $d=v-u$. The equation gives

$$
A=vh-d\ell,\qquad n=C+uh+d\ell.
$$

If $\ell>0$, nonnegativity of $A$ forces $h\ge1$, and then $n\ge u+d=v$. Thus $\ell=0$. In particular, when $n<u$, (3) also forces $A=0$ and $C=n$.

The distinction is crucial: below height $u$ a pure-$c$ seam has only $c$ opposite it; below height $v$ it may have $a$ opposite it, but it has **no $b$ opposite it**. The downward apex induction needs the latter, stronger range.

Throughout the proof the tiling is fixed. A collinear component means a connected union of actual whole tile edges on one supporting line. An internal maximal component has a complete chain on each side: an edge cannot end inside an edge on the other side without another collinear edge continuing the remaining straight sector. Nor can a supplied next edge be swallowed by a tile at a junction. Maximality prevents an endpoint from lying inside any constituent edge. When the proof instead uses a subsegment, it separately establishes endpoints for both chains, using external supporting lines or the starting edge of an actual tile. Thus none of the length lemmas is applied to a chain of merely partial edges.

## Equal-side boundary fact and coordinates

No corner of the isosceles target contains a $\gamma$ sector: its two base corners contain one $\beta$ each, and its apex contains exactly three $\alpha$ sectors. This remains true when the total apex angle $3\alpha$ exceeds $\gamma$.

Every $a$- or $b$-edge on a target side contributes a $\gamma$ endpoint, and two such endpoints cannot coincide at a straight boundary junction because $2\gamma>\pi$. A side consisting of $n$ edges has only $n-1$ internal junctions. Hence every side contains at least one $c$-edge.

An equal side has length $v^3=vc$. Reduction modulo $v$ makes its $b$-count a multiple of $v$. If it had at least $v$ $b$-edges, removing $v$ of them would leave a positive whole-edge decomposition of

$$
vc-vb=u a.
$$

Since $u<v$, (2) makes every remaining edge an $a$-edge, contradicting the presence of a $c$-edge. Therefore **both equal sides have no $b$-edge**.

Place the target at $A=0$, $B=vq$, $C=uP$, where $p=a$ is horizontal, $q=ce^{i\beta}$, and $q-p=be^{i\theta}$. Put $Z(i,t)=ip+tq$. Use

$$
D(i,t)=\operatorname{conv}(Z(i,t),Z(i+1,t),Z(i,t+1)),
$$
$$
U(i,t)=\operatorname{conv}(Z(i+1,t),Z(i,t+1),Z(i+1,t+1)).
$$

Their angles at the listed vertices are respectively $(\beta,\gamma,\alpha)$ and $(\alpha,\gamma,\beta)$.

The apex has exactly three $\alpha$ tiles. Its two outer edges are $c$, because the equal sides have no $b$. Each $\alpha$ tile has incident sides $b,c$, so its two inner radial seams comprise one $b/b$ seam and one $b/c$ seam. Choose the reflected labeling so the latter is next to the left outer tile $D(0,v-1)$.

## Reverse-apex state

Write $V_m=Z(m,v-m)$ for $0\le m\le v$. Let $T(m,t)$ be the actual standard truncated corner region consisting of:

- all $D(i,s)$ with $0\le i<m$, $s\ge t$, and $i+s\le v-1$;
- all $U(i,s)$ with $0\le i<m$, $s\ge t$, and $i+s\le v-2$.

Geometrically this is the standard subdivision of the polygon with oblique coordinates

$$
(0,t),\quad(m,t),\quad(m,v-m),\quad(0,v),
$$

when $t\le v-m$, with zero-height edges allowed.

For each $m=1,\ldots,v-1$, the apex diagonal $b$-chain $B=V_0,V_1,\ldots,V_m$ will be actual. Its opposite chain starts at $B$ with the central apex $c$-edge. Since $m<v$, short $b$ purity implies that $V_m$ is in the relative interior of an actual opposite edge. Thus the positive $q$-ray from $V_m$ enters that opposite tile's interior.

Let $M_m$ be the actual maximal collinear component from $V_m$ in direction $-q$. Its upper end is $V_m$, by the preceding crossing. We prove:

1. Its whole left side is a chain of normal $c$-edges of $U$ tiles.
2. If its lower endpoint is $Z(m,r)$, then $T(m,r)$ is actual; more generally every reached integer height $t$ supplies $T(m,t)$.
3. Its opposite side has no $b$-edge.

These statements are proved in increasing $m$; within each column, the continuation goes downward. Earlier columns may terminate earlier, but whenever a newly supplied $U$ extends one of them downward, its already proved conditional completion statement applies. No assumption is made that any column reaches the base.

## Reverse horizontal cap

The first outer apex tile is $D(0,v-1)$. Its $b$-edge is $BV_1$, and the opposite central $c$-edge starts at $B$ and overruns $V_1$ since $c>b$.

More generally, suppose the diagonal has just reached $V_m$, where $m<v$, and $T(m-1,v-m)$ is known. For $m=1$, the old region $T(0,v-1)$ is empty and the new tile $D(0,v-1)$ is the outer apex tile. The new $D(m-1,v-m)$ gives, together with the old region, a horizontal chain of $m$ $a$-edges from $(v-m)q$ to $V_m$.

Its negative extension at the outer side leaves the convex target. Its positive extension at $V_m$ enters the crossing opposite tile. Thus the opposite chain is a complete chain of total length $ma$, hence exactly $m$ $a$-edges.

At $V_m$ the already placed $D$ contributes $\gamma$ and the crossing tile a straight sector $\pi$, so the remaining sector is $\theta=\alpha+\beta<\gamma$. Consequently the opposite $a$-tile has $\beta$, not $\gamma$, at $V_m$; it is $U(m-1,v-m-1)$. Propagating left, every successive opposite $a$-tile must also be a normal $U$: a reversed one would put two $\gamma$ sectors in the same lower half-plane at a shared junction.

At the outer boundary point $(v-m)q$, the old $D$ contributes $\beta$ and the new $U$ contributes $\gamma$, leaving $\alpha$. The next boundary edge is $c$, since that equal side has no $b$; this gives $D(0,v-m-1)$.

At each interior grid point $Z(i,v-m)$, where $1\le i<m$, the existing upper row and the two new $U$ tiles leave exactly one $\alpha$ sector. The new left $U$ supplies an actual downward $c$-edge in the earlier column $M_i$, connected to its upper component through the old actual region. Its already proved no-opposite-$b$ property excludes $b$ on the right of that $q$-edge. Hence its $\alpha$ tile uses $c$ and is $D(i,v-m-1)$.

Explicitly, at a reached height $t$, the old region contains the collinear $c$-edges of $U(i-1,s)$ for $t\le s\le v-i-1$, joining $Z(i,t)$ to $V_i$. The new edge of $U(i-1,t-1)$ attaches to this very component. If it extended below an earlier claimed endpoint, that would contradict the already established maximality; it would not create a different column. The same connectivity applies in the downward continuation below.

This supplies $T(m,v-m-1)$ and the first complete $c$-edge of $M_m$.

## Downward column completion

Assume $T(m,t)$ is actual, with $t\le v-m-1$, and the real component $M_m$ continues downward from $X=Z(m,t)$. Its old left-side normal tiles $D(m-1,t)$ and $U(m-1,t)$ contribute $\gamma+\alpha=\pi-\beta$. The actual downward $q$-ray therefore leaves one $\beta$ tile on its left.

That $\beta$ tile has either $a$ or $c$ on the downward $q$-ray. If it had $a$, its other incident side would be a $c$-edge from $X$ horizontally to the left. But the actual upper horizontal chain from $tq$ to $X$ consists of $m$ $a$-edges. Starting at $X$ with this $c$-edge, the opposite chain must cover the whole upper chain: at a T-junction inside an upper edge a straight sector forces continuation, and an upper-chain grid endpoint cannot let the actual next upper edge be swallowed by a tile. At $tq$ the external side prevents overrun. Hence the lower chain would be a complete positive chain of length $ma$ containing a $c$-edge, contrary to short $a$ purity, since $m<v$.

Thus the $\beta$ tile has $c$ on the $q$-ray and is $U(m-1,t-1)$. Its top $a$-edge starts a whole lower chain along the existing upper chain of length $ma$. Short $a$ purity makes the lower chain exactly $m$ $a$-edges. Starting at $X$, the same two-$\gamma$ argument forces all these lower tiles to be normal $U(i,t-1)$.

At $tq$, the old $D(0,t)$ contributes $\beta$ and $U(0,t-1)$ contributes $\gamma$, leaving $\alpha$, so absence of boundary $b$ gives $D(0,t-1)$. At each inner point $Z(i,t)$, where $1\le i<m$, exactly one $\alpha$ remains. The new actual downward $c$-edge is on the earlier column $M_i$; its no-opposite-$b$ property makes that $\alpha$ tile $D(i,t-1)$. Therefore $T(m,t-1)$ is actual.

Every actual continuation adds one complete normal $c$-edge. Since the target is bounded, the component ends at some grid height $r\ge0$. Its length is $nc$, where

$$
n=(v-m)-r,\qquad 0<n\le v-m<v.
$$

Arithmetic fact (3) gives no $b$-edge on the opposite side. This closes the induction for $M_m$.

## Advancing the apex diagonal

At $V_m$ the crossing opposite tile, the old $D(m-1,v-m)$, and the first $U(m-1,v-m-1)$ leave one $\alpha$ sector immediately on the right of the downward $q$-ray. Its $q$-side cannot be $b$ by $M_m$'s just established no-opposite-$b$ property. It is therefore $c$, and the tile is $D(m,v-m-1)$. Its $b$-edge extends the actual diagonal to $V_{m+1}$.

For $m+1<v$, short $b$ purity again says that this endpoint lies inside an actual opposite edge. The reverse horizontal cap then initializes the next column. For $m=v-1$ the same forcing gives $D(v-1,0)$ and reaches $V_v=vp$ on the base; no short $b$ statement with index $v$ is used.

The column $M_{v-1}$ starts at height $1$ and its initialization reaches height $0$. Its completion statement gives $T(v-1,0)$. Adding $D(v-1,0)$ gives the entire standard

$$
K_v=\operatorname{conv}(0,vp,vq),
$$

with its $v^2$ tiles.

In particular the base begins at $A$ with $v$ consecutive $a$-edges, of total length $L=va=uc$.

## The complement is a forbidden W triangle

Let $L=vp$. The forced $K_v$ has vertices $A,B,L$, consists of $v^2$ whole tiles, and is a genuine corner of the target. Its diagonal $BL$ is the actual chain of $v$ $b$-edges. Thus removing its tiles leaves a tiling of the triangle $BLC$.

But

$$
BC=v^3,\qquad BL=vb,\qquad
LC=uP-va=u(2v^2-u^2)=uQ.
$$

The remaining tile count is $P-v^2=Q$. Hence the complement is exactly the scale-one W triangle excluded below. This proves the isosceles assertion. No base-edge count, two-$c$ boundary lemma or assumption about an ordering of the base edges is needed. $\square$

# Appendix: complete scale-one W exclusion

The following proof is reproduced to make the result self-contained. It uses a different orientation of coordinates, reset in its statement. The arithmetic facts called $S_b,S_a,S_c$ below are respectively (1), (2), and the $n<u$ consequence of (3).

## Statement and coordinate convention

Let $0<u<v$, $\gcd(u,v)=1$, and put

$$
a=uv,\quad b=v^2-u^2,\quad c=v^2,\quad Q=2v^2-u^2.
$$

The theorem is that the triangle with side lengths

$$
(v^3,\;uQ,\;vb)
$$

cannot be tiled by $Q$ congruent copies of $(a,b,c)$. Its angles are $(\beta,2\alpha,\alpha+\beta)$, where $3\alpha+2\beta=\pi$.

Name the β corner $O$. Direct $OA$ horizontally to the right, with $|OA|=v^3$. The other side $OC$ has length $u(b+c)=uQ$ and makes angle β with $OA$. Put

$$
p=a,\quad q=ce^{i\beta},\quad O=0,\quad A=v^3,\quad
C=\frac{u(b+c)}{c}q,\quad Z_{i,t}=ip+tq.
$$

Thus $q-p=be^{i\theta}$, where $\theta=\alpha+\beta$. The $q$ direction is along the side $OC$, whose edge counts will be $(0,u,u)$. It is **not** assumed to be a pure $c$-grid initially.

The two adjacent side lengths satisfy the strict inequalities

$$
|OA|=v^3>u a=u^2v,\qquad |OC|=u(b+c)>u c.
\tag{L}
$$

Consequently every corner front of index $j\le u$ has both endpoints strictly inside the two external sides, so its opposite side is an internal chord. This excludes the degenerate situation in which a purported front is already the outer third side of the target.

Use the standard actual triangles

$$
D_{i,t}=\operatorname{conv}(Z_{i,t},Z_{i+1,t},Z_{i,t+1}),\quad
U_{i,t}=\operatorname{conv}(Z_{i+1,t},Z_{i,t+1},Z_{i+1,t+1}).
$$

The angles of $D$ at its listed vertices are $(\beta,\gamma,\alpha)$; those of $U$ are $(\alpha,\gamma,\beta)$. Let $R(m,n)$ denote the actual rectangle of all such tiles for $0\le i<m$, $0\le t<n$.

## 1. Boundary counts, corner, and short-chain arithmetic

Every target angle is less than γ. Thus no boundary corner can contain a γ sector. Each boundary $a$- or $b$-edge contributes a γ endpoint. Two γ sectors cannot share a straight boundary junction. Consequently every target side has at least one $c$-edge.

On $OC$, write its counts as $(A_0,B_0,C_0)$, with $C_0\ge1$. The length equation is

$$
A_0uv+B_0(v^2-u^2)+C_0v^2=u(2v^2-u^2).
$$

Reduction modulo $v$ gives $B_0=u+vk$, $k\ge0$. Write $C_0=u\ell-vk$; then $A_0=uk+v(1-\ell)$. For $k\ge1$, $C_0\ge1$ requires $\ell\ge k+1$, but $A_0\ge0$ requires $\ell\le k$. Hence $k=0$, and positivity gives $\ell=1$. Therefore

$$
\boxed{(A_0,B_0,C_0)=(0,u,u).}
\tag{B}
$$

At $O$, the unique β tile has incident sides $a,c$. Since $OC$ has no $a$-edge, its first edge is $c$ and $OA$ starts with $a$. Thus $D_{0,0}$ is present.

We use $S_b$, $S_a$ and $S_c$ for the positive-chain facts (1), (2), and the $n<u$ consequence of (3), proved above. The exact angle inventories and irrationality of $\alpha/\pi$ were also established above.

## 2. First column: actual c-only strip, then no right a-edge

The internal $b$-edge of $D_{0,0}$ is the chord joining $p$ and $q$. Both endpoints are on the outer boundary. Its opposite chain consists of a single $b$-edge by $S_b$. The opposite tile is $U_{0,0}$: the other orientation would put two γ sectors at the boundary point $p$.

Let $L_1$ be the actual maximal connected collinear component of tile boundaries from $p$ in direction $q$. Its negative extension leaves the target across $OA$. Its left side starts with the $c$-edge of $U_{0,0}$.

The distance from this line to the supporting line $OC$ is $a\sin\beta=h_c$, the tile altitude to $c$. A tile attached on the left with an $a$- or $b$-edge would have larger altitude and cross the external supporting line. Hence **every complete edge on the entire left of $L_1$ has length $c$**, even at arbitrary T-junctions.

The component is finite. Maximality means its left edges form a complete chain starting at $p$ and ending at $p+nq$, for some integer $n\ge1$. There is no possibility of ending inside one of these edges, because that edge would extend the component.

For each left $c$-edge from $p+iq$ to $p+(i+1)q$, its opposite vertex lies on the supporting line $OC$, since its altitude equals the strip width. The two possible vertex positions are

$$
(i+1)q,\qquad(i+\lambda)q,
\qquad \lambda=2\frac ac\cos\beta
=\frac{u^2(3v^2-u^2)}{v^4}.
$$

The second point has signed distance

$$
(i+\lambda)c=iv^2+\frac{u^2(3v^2-u^2)}{v^2}
$$

from $O$, which is nonintegral because $\gcd(u,v)=1$. An actual tile vertex on $OC$ must be a boundary junction, and every boundary-junction distance is an integer sum of tile-edge lengths. Thus the second point is impossible. All left tiles are the normal $U_{0,i}$.

The spaces between consecutive $U$ tiles and $OC$ are the triangles $D_{0,i}$. They are bounded by actual tile edges and the external boundary and each has exactly one tile's area. They must therefore be single tiles, so $R(1,n)$ is present. Equivalently, this can be checked by successive boundary angle fans. The original $D_{0,0}$ is already present.

At $nq$ the tiles $D_{0,n-1}$ and $U_{0,n-1}$ contribute α and γ, leaving β in the target boundary half-plane. This point cannot be $C$: its two existing angles already total $\alpha+\gamma>\alpha+\beta$, the target angle at $C$. It cannot lie beyond $C$ either. Hence it is an internal boundary junction, and its next boundary edge belongs to a β tile. That edge is $a$ or $c$; by (B), it is $c$. Therefore the existing first $n$ boundary $c$-edges require one additional $c$-edge, giving

$$
\boxed{n<u.}
\tag{H}
$$

The opposite side of $L_1$ is a complete edge chain of length $nc$. By $S_c$, every edge on it is also $c$. In particular, there is **no right $a$-edge on $L_1$**.

The same argument gives the first-column rectangular completion property: whenever this actual component reaches height $t$, $R(1,t)$ is present. If $u=1$, (H) contradicts $n\ge1$ already; hence that case is excluded at this point.

## 3. Horizontal cap without a pre-assumed c-grid

Suppose $R(i,t)$ and $D_{i,t-1}$ are present, $0<i<v$, and an actual $\theta$-directed edge contains $X=Z_{i,t}$ in its relative interior, with its tile on the lower/right side.

The rectangle supplies a horizontal chain of $i$ lower $a$-edges from $tq$ to $X$. The negative extension at $tq$ leaves the target across $OC$, and the positive extension at $X$ enters the crossing tile's interior. Hence this is the entire actual horizontal component. Its complete upper chain has length $ia$, so $S_a$ makes it exactly $i$ $a$-edges.

At $tq$ the existing α and γ sectors leave β. The point is an internal point of $OC$ for the same reason as in (H). Since $OC$ has no $a$-edges, its next actual edge must be $c$, giving $D_{0,t}$. At every later upper-chain junction, the preceding normal $D$ contributes γ. The remaining upper angle is θ, and $\gamma>\theta$. The next upper $a$-tile must therefore have β at that junction, so it is normal. This forces $D_{i-1,t}$.

Thus the earlier horizontal-cap lemma works here: every needed local $c$-boundary continuation is forced by the actual rectangle and (B), rather than assumed globally.

## 4. Diagonal-chain obstruction

**Diagonal-chain lemma.** Assume $1\le j<v$, the actual $R(j-1,n+1)$ and $D_{j-1,n}$ are present, and every column with index $<j$ already has the following conditional rectangular completion property: whenever its actual component connected to the base reaches $Z_{i,t}$, the whole $R(i,t)$ is present. There cannot be an actual $a$- or $c$-edge from $V=Z_{j,n}$ in direction $e^{i\theta}$ toward $OC$, with its tile on the lower/right side.

**Proof.** Set

$$
X_k=Z_{j-k,n+k},\qquad0\le k\le j.
$$

The supplied $D_{j-1,n}$ gives the first actual $b$-edge $X_0X_1$ on the upper/left side. The hypothesized $a$- or $c$-edge starts at $X_0$ on its other side.

Suppose the actual upper/left $b$-chain $X_0\cdots X_k$ has been supplied. Along each of its edges, the tiling on the opposite side supplies a collinear chain. If an opposite edge ends inside one of the existing $b$-edges, that $b$-tile has a straight sector there and forces the next actual collinear edge. Hence the opposite chain starts at $X_0$ and covers the entire segment $X_0X_k$.

If $X_k$ were the endpoint of an opposite edge too, both sides from $X_0$ to $X_k$ would be complete whole-edge chains of length $kb$. The opposite chain contains its initial $a$- or $c$-edge; because $k\le j<v$, this contradicts $S_b$. Therefore every intermediate $X_k$ lies strictly inside one actual opposite edge.

At $k=1$, put $i=j-1$ and $t=n+1$. The rectangle and additional tile required by the horizontal-cap lemma are exactly the supplied $R(j-1,n+1)$ and $D_{j-1,n}$. The lemma forces $D_{i-1,t}$, whose $b$-edge is $X_kX_{k+1}$.

For $i-1>0$, this newly forced tile also supplies a real $c$-edge in column $i-1$ from height $t$ to $t+1$. Its lower endpoint is already connected to the base through $R(i,t)$. The completion property of this strictly smaller column therefore supplies $R(i-1,t+1)$. The new $D_{i-1,t}$ is precisely the additional tile needed at the next crossing. Thus the cap can be applied successively. If any required tile leaves the target, this already contradicts the assumed tiling.

When $k=j$, the endpoint $X_j=Z_{0,n+j}$ lies on the supporting line $OC$. If it were beyond the side segment, an already supplied tile would have left the target. Otherwise the actual $b$-chain reaches the external side there. Its opposite chain cannot overrun outside the convex target, so both chains are complete from $X_0$ to $X_j$. Their length $jb$ contradicts $S_b$ once more. The case $j=1$ uses this final step immediately, without an intermediate cap. ∎

This proof permits intermediate endpoints and changes of the actual opposite tile. It requires neither $a>b$, nor a short-distance estimate, nor artificial continuation of the original $a$- or $c$-edge.

## 5. Strong column induction

Suppose $K_m=\operatorname{conv}(0,mp,mq)$, with its standard subdivision, is present and $m\le u<v$. By (L), its front from $mp$ to $mq$ is an internal chord. Its complete opposite edge chain is exactly $m$ $b$-edges by $S_b$. At $mp$ the old patch contributes γ, so the first opposite tile must have α there; another γ would exceed the boundary angle π. Reversing the orientation of a later opposite tile would put two γ sectors in the same half-plane at a shared endpoint. Hence every opposite tile is the normal $U$ tile. This complete opposite row, together with $K_m$, supplies $R(m,1)$.

For every actual column $L_m$ from $mp$ in direction $q$, establish:

1. its whole left side consists of normal $U$ tiles with complete $c$-edges;
2. if its connected prefix reaches height $t$, $R(m,t)$ is present;
3. it has no right $a$-edge.

Column one has already been proved. Assume every smaller column is established, and maintain an actual $R(m,n)$. If $L_m$ ends at $Z_{m,n}$, its completed normal left chain stops. Otherwise its actual upward $q$-ray exists.

At $nq$, the boundary α and γ sectors force a normal β tile $D_{0,n}$, using (B). Sweep across the top row. At each $Z_{i,n}$, $1\le i<m$, the old rectangle and preceding new $D$ leave the fan θ. In the following two cases the fan is read counterclockwise from the positive horizontal ray to the $\theta$ ray.

- The order α,β gives a real long $a$- or $c$-edge in the $\theta$ direction, on its lower/right side. The diagonal-chain obstruction applies with $j=i$; the preceding sweep has supplied its required rectangle and $D$ tile. Thus this order is impossible.
- In the order β,α, an actual upward $q$-ray is present and connected to column $i$ through the old rectangle. The β tile cannot use $a$ on that ray, by the no-right-$a$ property of this earlier column. Hence it is normal $D_{i,n}$. The α tile cannot use $b$ on the ray, by that earlier column's complete c-only left side. Hence it is normal $U_{i-1,n}$.

At the outer point $Z_{m,n}$, its actual continuation leaves an α fan on the left. If the α tile uses $b$ on the q-ray, its $c$-edge is a real forbidden diagonal; the just completed sweep supplies the hypotheses of the diagonal-chain obstruction with $j=m$. Thus it uses $c$, and is $U_{m-1,n}$. This gives $R(m,n+1)$.

Every real continuation therefore adds a whole normal $c$-edge. Since the target is bounded, continuation is finite and the full component has some integer height $n$ and the complete actual rectangle $R(m,n)$. Its boundary endpoint $nq$ again forces one additional boundary $c$-edge by (B), so $n<u$. The right chain of the component has length $nc$; $S_c$ makes it c-only. In particular it contains no right $a$-edge. This completes the induction using only earlier columns.

## 6. Forced fronts and contradiction

Start with $K_1=D_{0,0}$. Across its b-chord, the opposite tile is forced. The β gap at $q$ has its boundary edge on $OC$ and must use $c$ there by (B). The β gap at $p$ cannot switch to a right a-edge on $L_1$. Hence $K_2$ is forced whenever $u\ge2$.

Suppose $K_j$ is present for $j\le u<v$. By (L), its two front endpoints are strictly inside the external sides and its inner side is an actual internal chord. The complete opposite b-row is forced by $S_b$. Each remaining β notch admits the standard order of sides or an interchange of $a,c$. The notch on $OC$ must be standard because that side has no $a$-edge. Any other switched notch gives a right a-edge on the actual column connected to the base through $K_j$ and its real opposite b-row. Its column index is at most $j$, and all such columns have just been established from their contained $K_m$. Therefore no switch is possible and $K_{j+1}$ is forced.

Thus $K_{u+1}$ is forced. It supplies $u+1$ complete c-edges on $OC$, contradicting its exact count $u$ from (B). This concludes the proof.

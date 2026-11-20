# The seam from the 60-degree corner cannot meet either other corner seam at unit scale

Let $a>b>0$, $\gcd(a,b)=1$ and $c^2=a^2+ab+b^2$. Let $\alpha,\beta$ be the angles opposite $a,b$ in this tile. Write $p=a+2b,\ q=2a+b$; primality of $p,q$ is unnecessary. In the axial basis $1,\rho=e^{i\pi/3}$ put the F2 board vertices at $O=0$, $B=bq$, $C=ap\rho$. Their angles are $\pi/3,2\alpha,2\beta$. The positive integer scale $t$ multiplies the board lengths, leaving the tile unchanged.

Each board vertex has a unique seam issuing strictly into the board. Its **initial straight portion** is the maximal closed interval on its ray starting at that vertex and contained in tile edges. Collinear T-junctions and four-way crossings may occur along it. In the following statement a meeting may be at an endpoint of one or both straight portions or in their relative interiors.

**Theorem.** At unit scale, the initial straight portion from $O$ is disjoint from the initial straight portion from $B$ and from the one from $C$. Thus three unbroken corner seams cannot bound a central triangle or end in a cyclic arrangement of T-junctions. The two equal-angle bisectors from $B,C$ have an arithmetically permissible intersection with each other. No claim is made that they reach it.

At general positive integer scale $t$, these are necessary divisibilities for actual meetings:

| Angle made by the ray from $O$ with $OB$ | Meeting the ray from $B$ requires | Meeting the ray from $C$ requires |
|---|---:|---:|
| $\beta$ | $c\mid t$ | $c\mid t$ |
| $\alpha$ | $p\mid t$ | $q\mid t$ |

They are exact conditions for integrality of the two distances to the proposed meeting. They do not ensure continuation of either seam to that point. The [first-cut theorem](PROOF.md) studies straight chords ending on the outer boundary. Its [virtual-apex argument](VIRTUAL_APEX.md) studies chords in one specified complement. Here the collision is inside the whole board and neither participating segment has to reach its opposite board side. The result applies with unrestricted tile orientations and T-junctions.

### Integer offsets along a straight seam

Consider a fixed supporting line, with either unit coordinate. Each tile side on that line is a closed interval of integer length. Also include any outer side on the line, with the reverse boundary orientation; its length is an integer. In the sum of oriented interval indicators, their step functions total zero almost everywhere. This follows locally by cancellation of the two banks at points away from vertices. Both endpoints of every interval have the same coordinate modulo one.

Group the intervals by that residue. Every jump at a particular point $x$ lies in the single group $x\bmod 1$. Since the full step function has no jumps, each group has no jumps. A compactly supported step function without jumps is zero almost everywhere. On a positive-length overlap between two constituent intervals, a generic point has exactly the two opposite banks (one can be the exterior). Their residues must agree by the groupwise cancellation. Intervals touching at just one point share an endpoint, so their residues likewise agree. It follows along a finite chain of intersecting intervals that each connected component of their union has a single endpoint residue. A point in the interior of a whole edge need not itself have this residue unless it is also an endpoint of a side on the line.

The emitting board vertex is an endpoint of an actual tile side on the corner seam. At a meeting of two noncollinear seams inside the board, the meeting is an endpoint of a tile side **on each participating line**. Indeed, if there were no such endpoint on one line, continuity of the seam up to the point and finiteness of the tiling would give a side passing through the point on that line. On a neighboring generic interval on this side, the opposite bank is also a tile side. It too must pass through the point if there is no endpoint there. Their interiors would then occupy both half-disks in a sufficiently small neighborhood, precluding even a transverse terminating ray. This covers also the case where one bank passes through a T-junction and the other changes tile. Consequently the distance to the meeting from each of the two emitting corners is an integer. The proof imposes no integer condition on an arbitrarily chosen endpoint of a proper subsegment of a seam.

### The four distances

The angle $\beta/\pi$ is irrational: $2\cos\beta=q/c$ is rational strictly between one and two, whereas a rational multiple of $\pi$ would make this a rational algebraic integer. Since $\alpha+\beta=\pi/3$, the two angles $\alpha,\beta$ are rationally independent. The third tile angle is $2\alpha+2\beta$. Thus the only way to fill $2\alpha$ at $B$ is with two copies of $\alpha$, and the only way to fill $2\beta$ at $C$ is with two copies of $\beta$. At $O$ one copy of each is required. An interior point of a tile side cannot occupy a corner sector of the convex board because it contributes angle $\pi$. These counts prove the uniqueness of the outgoing seams locally.

Put $z=(a+b\rho)/c$. In axial coordinates their unit direction vectors are
$$
 d_O=(a,b)/c\ \text{or}\ (b,a)/c,\qquad d_B=(-(a+b),a)/c,\quad d_C=(b,-(a+b))/c .
$$
The first choice at $O$ makes angle $\beta$ with $OB$ and the second makes $\alpha$. At scale one a ray from $X=B$ or $C$ meets the supporting ray from $O$ at $O+\lambda d_O=X+\mu d_X$. Taking axial determinants gives $\lambda=\det(X,d_X)/\det(d_O,d_X)$. The analogous determinant gives $\mu$. All entries in the table are positive.

| $O$ direction | Other corner | Distance $\lambda$ from $O$ | Distance $\mu$ from the other corner |
|---|---:|---:|---:|
| $\beta$ | $B$ | $abq/c$ | $b^2q/c$ |
| $\beta$ | $C$ | $abp/c$ | $a^2p/c$ |
| $\alpha$ | $B$ | $bcq/p$ | $bcq/p$ |
| $\alpha$ | $C$ | $acp/q$ | $acp/q$ |

For reference the other two supporting rays meet at $(ab,ab)$, at distances $bc$ from $B$ and $ac$ from $C$. The area or tileability of a central region is not used.

The integers $a,b,c$ are pairwise coprime. If $3\mid c$, the norm implies $a\equiv b\pmod3$; then $a^2+ab+b^2\equiv3b^2\pmod9$, contradicting primitivity. The identities $4c^2-p^2=3a^2$ and $4c^2-q^2=3b^2$ give $\gcd(c,pq)=1$. Also $\gcd(p,b)=\gcd(q,a)=1$, while $\gcd(p,q)$ divides three by primitivity and cannot be three because $a\equiv b\bmod3$ would imply $3\mid c$. Thus all displayed distances are already in lowest terms. Dilation multiplies them by $t$. This proves the divisibility table and the unit obstruction.

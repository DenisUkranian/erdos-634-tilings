---
title: "Square-class obstructions and a uniform finite reduction for triangle tilings"
author: "Denis Paliy — research with ChatGPT assistance"
date: "30 September 2026"
fontsize: 11pt
geometry: margin=25mm
colorlinks: true
linkcolor: blue
urlcolor: blue
---

## Status and precise scope

This note gives universal necessary conditions and an explicit arithmetic reduction for congruent triangle dissections. It does **not** give a new full classification of all integers in Erdős problem 634. Its principal negative conclusions are:

**Theorem A.** No triangle is tiled by a squarefree number $N$ of congruent triangles if $N\equiv19\pmod{24}$ or $N\equiv35\pmod{120}$.

More generally, if $N$ is squarefree, $N\equiv3\pmod8$, and $3\nmid N$, then every such tiling must be a scale-one Group-1 beta-isosceles tiling, with
$$N=3v^2-u^2,\qquad 0<u<v,\qquad \gcd(u,v)=1.$$
In particular, $3$ must be a square modulo every prime divisor of $N$.

The conclusions use the published shape classification and rationality inputs specified below, not the project's unreviewed all-primes candidate. Reflections and arbitrary T-junctions are allowed. The squarefree qualification is essential.

A second result is the exact **invariant-admissible** scale in the double-angle isosceles branch: for the primitive tile $(u^2,v^2-u^2,uv)$ the count must be $(v^2-u^2)t^2$, and $t=1$ is geometrically impossible. This does not assert existence at every $t\ge2$.

Finally, an explicit Laurent identity shows why even the complete translation-invariant directed-edge signature cannot prove the two Group-1 scale-one obstructions: every candidate in those families has a formal orientation multiset of the correct size and boundary signature. A formal multiset is not a dissection.

All claims here received project-internal derivation and supplementary exact checks, not external refereeing or formal verification. Priority has not been established. The general signed-direction method and much of the branch framework predate this note. Computational decidability for fixed $N$ is already discussed by Beeson [I, Theorem 11.15 and Section 13; G, Section 15]; the explicit decision procedure below is not advertised as a new solution of Erdős's classification problem.

## 1. Definitions and outside inputs

A tiling consists of finitely many nondegenerate congruent closed triangles, with disjoint interiors and union a triangular target. A tile need not share a whole edge with its neighbor. A boundary vertex may lie strictly inside another tile's edge.

The external inputs are precisely:

* Laczkovich's exhaustive angular classification, as reproduced in [R, Table 1], with the isosceles specialization [I, Theorem 3.1].
* Rationality of the side ratios of a nonsimilar, nonright, incommensurable-angle tile [R, Theorem 1.2].
* The classical reptiling, commensurable-angle, and right-tile restrictions [S, Theorems 1, 3, 4; I, Theorem 7.10]. Their counts are contained in the explicitly realizable set
$$\mathcal C=\{r^2,\ r^2+s^2,\ 2r^2,\ 3r^2,\ 6r^2:r,s\in\mathbb Z_{>0}\}.$$
Twice a sum of two squares is itself a sum of two squares. A zero square causes no issue because perfect squares are already included.

No withdrawn packing lemma, necessity of a scale-divisibility assertion from [G], or blanket prime nonexistence claim is an input. Outside the classical cases, rationality permits primitive integer tile sides. An exterior side of the convex target is covered by **whole** tile edges: a tile edge lying on its supporting line cannot extend outside the target. All target side lengths are therefore integers in this normalization.

If the primitive integer side ratios of the target are $(r,s,t)$, its common scale is an integer. Indeed integers $x,y,z$ with $xr+ys+zt=1$ give the scale as an integer combination of the three actual exterior lengths.

## 2. Signed directions, parity, and T-junctions

Suppose every directed edge has direction $n\eta+j\pi$, where $\eta/\pi$ is irrational. The representations are unique with $n\in\mathbb Z$ and $j$ modulo $2$. Define
$$f(n\eta+j\pi)=(-1)^j,\qquad g(n\eta+j\pi)=(-1)^{n+j}.$$
For an oriented polygon take the sum of its edge lengths times $f$, or times $g$. Both sums are additive under dissection. To verify this with T-junctions, split all edges at every incident vertex and cancel oppositely oriented internal subsegments. No integrality of the subsegment lengths is used.

Each rotation of the reference tile multiplies its value by a sign. Reflection, followed by reversing the traversal to keep the boundary counterclockwise, does the same. Consequently, if the reference values are nonzero, division of the target values gives integers $U,V$ with
$$U\equiv V\equiv N\pmod2.\tag{1}$$
Both half-sum and half-difference are integers.

The direction group really is shared by all tiles: the graph of tiles joined by a positive-length common boundary segment is connected. A generic path between two tile interiors avoids the finitely many vertices. Crossing each shared segment propagates directions by integer combinations of the tile angles. Start from an exterior edge and rotate it to the horizontal.

The same argument works for the group $n\alpha+j\pi/3$ in the 60/120-degree branches, with $j$ modulo $6$ and characters $(-1)^j,(-1)^{n+j}$.

## 3. The double-angle isosceles branch

The tile angles are $(\alpha,\beta,2\alpha)$, where $3\alpha+\beta=\pi$ and $\alpha/\pi$ is irrational. Rational sides and the sine law give the primitive parametrization
$$a=u^2,\qquad b=v^2-u^2,\qquad c=uv,
\qquad \gcd(u,v)=1,\quad 0<u<v<2u.\tag{2}$$
For completeness, $c/a=2\cos\alpha=v/u$ in lowest terms and
$b/a=\sin(3\alpha)/\sin\alpha=(v^2-u^2)/u^2$, giving (2).
The target has base angles $\alpha$, hence primitive side ratios $(u,u,v)$. Write its sides as $(\lambda u,\lambda u,\lambda v)$, with $\lambda$ a positive integer. Area comparison gives
$$N=\lambda^2/b.\tag{3}$$

### Theorem B: the complete two-character scale restriction

Every such tiling has
$$\boxed{\lambda=bt,\qquad N=bt^2,\qquad t\in\mathbb Z_{>0}.}\tag{4}$$
Conversely, these scales pass the area equation and both character integrality/parity tests. This converse concerns the tests only.

**Proof.** Use $\eta=\alpha$. A counterclockwise reference tile with its $c$-edge horizontal has the other edge directions $3\alpha$ and $\pi+\alpha$. Its two values are
$$c+a-b=(2u-v)(u+v),\qquad c-a+b=(v+2u)(v-u).$$
The target boundary directions are $0,\pi-\alpha,\pi+\alpha$. The target values are $\lambda(v-2u)$ and $\lambda(v+2u)$. Thus
$$U=-\frac{\lambda}{u+v},\qquad V=\frac{\lambda}{v-u}.$$
Using (1),
$$\frac{U+V}{2}=\frac{\lambda u}{b}\in\mathbb Z,
\qquad \frac{V-U}{2}=\frac{\lambda v}{b}\in\mathbb Z.$$
Since $\gcd(u,v)=1$, Bezout gives $b\mid\lambda$, proving (4). At $\lambda=bt$, the normalized values are $-t(v-u)$ and $t(v+u)$; both have the parity of $bt^2$. $\square$

For example, the tile $(9,16,15)$ corresponds to $(u,v)=(3,5)$. The area equation at $\lambda=24$ gives the integer count $N=36$ but character values $-3$ and $12$ of different parity. Therefore the target $(72,72,120)$ cannot be tiled by this tile. The general exclusion is a parity theorem, not an extrapolation of this example.

### Lemma C: scale one is impossible

In (4), an actual tiling must have $t\ge2$.

**Proof.** The inventory at either base corner $\alpha$ is a single $\alpha$ tile. At the apex $\alpha+\beta=\pi-2\alpha$ it is exactly one $\alpha$ and one $\beta$, and no $2\alpha$. These statements follow by equating the rational and irrational parts of
$p\alpha+q\beta+r(2\alpha)$.

Choose the equal side incident to the apex's $\alpha$ tile. This side must contain a $b$-edge. Otherwise every boundary edge is $a$ or $c$ and has one endpoint presenting $\beta$. Neither endmost boundary tile presents $\beta$ at the outer endpoint, and a straight boundary junction contains exactly one $\beta$: the inventory equations are $q=1$, $p+2r=3$. Thus $k$ edges would require $k$ distinct internal junctions, although there are only $k-1$.

On this side, of length $\lambda u$, let the edge counts be $A,B,C$. Reduction of
$$\lambda u=A u^2+B(v^2-u^2)+Cuv$$
modulo $u$ gives $u\mid B$. If $t=1$, then $\lambda=b$, so $B\ge u$ consumes all of the available length $bu$. The side would consist entirely of $b$-edges.

Each $b$-edge has one $2\alpha$ endpoint. No target corner contains $2\alpha$, and the straight-vertex inventory $p+2r=3$ permits at most one such endpoint at an internal junction. The same counting contradiction excludes a pure-$b$ side. $\square$

This reproduces the squarefree consequence of [I, Theorem 11.7] and, together with (4), locates the obstruction at $t=1$ for nonsquarefree $b$ as well. No first-priority claim is made.

## 4. Rational Group 1 and the other necessary count forms

For $3\alpha+2\beta=\pi$, put
$$a=uv,\quad b=v^2-u^2,\quad c=v^2,\quad
Q=b+c,
\quad P=b+2c,\quad 0<u<v,\quad\gcd(u,v)=1.$$
The parametrization follows from $a^2=c(c-b)$ and primitive normalization. Use $\eta=\gamma=(\pi+\alpha)/2$. The reference tile's character values are
$$Q-a=(v-u)(2v+u),\qquad Q+a=(v+u)(2v-u).$$

For the theta-isosceles target, of primitive proportions $(v,v,u)$, the target values are $\lambda(u+2v)$ and $\lambda(u-2v)$. Thus
$$U=\lambda/(v-u),\qquad V=-\lambda/(v+u).$$
The same half-sum and half-difference force $b\mid\lambda$, and the count is $bt^2$. At its apex there is exactly one $\alpha$ tile, so one equal side contains a $b$-edge. Modulo $v$, the $b$-edge count on that side is divisible by $v$. At $t=1$ the side would be pure $b$; each such edge presents one obtuse $\gamma$ endpoint, no outer corner contains $\gamma$, and a straight junction contains at most one. Hence $t=1$ is impossible here too.

For the alpha-isosceles target of primitive proportions $(c,c,Q)$, the two normalized values are
$$U=\frac{\lambda(2v-u)}{v-u},\qquad
V=\frac{\lambda(2v+u)}{v+u}.$$
Their half-difference is $\lambda uv/b$. Since $\gcd(uv,b)=1$, $b\mid\lambda$. The count is consequently $bQt^2$.

The complete list needed here is:

| Group-1 target | Target sides at multiplier $t$ | Necessary $N$ |
|:--|:--|:--|
| W | $t(v^3,uQ,vb)$ | $Qt^2$ |
| beta-isosceles | $t(v^3,v^3,uP)$ | $Pt^2$ |
| theta-isosceles | $t(bv,bv,bu)$ | $bt^2$, $t\ge2$ |
| alpha-isosceles | $t(bc,bc,bQ)$ | $bQt^2$ |
| other scalene | $t(c^2,cQ,bP)$ | $QPt^2$ |

The W, beta, and other-scalene primitive side triples have greatest common divisor one; exterior integrality and area give the indicated scale directly. These derivations do not use a proposed W or beta scale-one nonexistence proof. The theta/alpha restrictions and these count forms also occur in the earlier project notes [P].

### The 60/120-degree families

For a primitive integer tile with $c^2=a^2\pm ab+b^2$, the sides are pairwise coprime. In the plus case, $3\nmid c$, and
$$\gcd(c,a+2b)=\gcd(c,2a+b)=\gcd(c,a+b)=1.$$
For example, if $3\mid c$ then $a\equiv b\pmod3$, and the norm is $3b^2\pmod9$, a contradiction to primitivity. The other gcd assertions follow by substituting the corresponding linear relation in the norm.

The two character argument in [P] is recalled briefly. In the plus case the reference values are $X=c+a-b,Y=c+b-a$, with $XY=3ab$. An equilateral side $S$ gives $U=3S/X,V=3S/Y$ and integer half-sum $Sc/(ab)$. Hence $ab\mid S$. In the minus case the values have magnitudes $a+b-c,a+b+c$, product $3ab$, and the relevant half-sum is $S(a+b)/(ab)$, again giving $ab\mid S$. Thus both equilateral branches require $N=abt^2$.

For the plus-case F1 and isosceles targets with primitive scale $\lambda$, the normalized values are respectively
$$\left(\lambda\frac{c-a}{b},\lambda\frac{c+a}{b}\right),\qquad
\left(\lambda\frac{c-a-b}{b},\lambda\frac{c+a+b}{b}\right).$$
Their half-differences force $b\mid\lambda$. The remaining rows follow from primitive side ratios and area:

| Branch | Target sides at multiplier $t$ | Necessary $N$ |
|:--|:--|:--|
| equilateral, either norm | $(abt,abt,abt)$ | $abt^2$ |
| F1 | $t(ab,bc,b(a+b))$ | $b(a+b)t^2$ |
| isosceles | $t(bc,bc,b(a+2b))$ | $b(a+2b)t^2$ |
| F3 | $t(c^2,c(a+2b),3b(a+b))$ | $3(a+2b)(a+b)t^2$ |
| F4 | $t(ac,b(2a+b),c(a+b))$ | $(2a+b)(a+b)t^2$ |
| F2 | $t(a(a+2b),b(2a+b),c^2)$ | $(a+2b)(2a+b)t^2$ |

F1, F2, F3, F4 are local labels; the displayed triples, not the label alone, identify each branch. The corresponding angular triples are, respectively,
$(\alpha,\alpha+\beta,\alpha+2\beta)$,
$(2\alpha,2\beta,\alpha+\beta)$,
$(\alpha,2\alpha,3\beta)$,
and $(\alpha,2\beta,2\alpha+\beta)$.
Both orders of $a,b$ are included. The equilateral minus norm has only its own equilateral row.

All entries are necessary conditions, not existence claims. The primitive triples and count identities can also be verified by the sine law or Heron's identity. The stronger F1/isosceles spectra are already present in Bonfioli's work as acknowledged in [P].

## 5. Proof of the global residue-class obstruction

Assume $N\equiv3\pmod8$ and $3\nmid N$. In every count $dt^2$ above, $t$ is odd and $t^2\equiv1\pmod8$. No classical count in $\mathcal C$ qualifies: a sum of two squares cannot be $3\pmod4$, an odd square is $1\pmod8$, and the remaining forms are even or divisible by $3$.

### A short, exhaustive residue calculation

For coprime $u,v$ the possible residues modulo $8$ are as follows. This table follows by separating the two opposite-parity cases and the case when both parameters are odd; each even square is $0$ or $4$ and each odd square is $1$.

| Group-1 coefficient | Possible residues modulo $8$ |
|:--|:--|
| $Q=2v^2-u^2$ | $1,2,6,7$ |
| $P=3v^2-u^2$ | $2,3,7$ |
| $bQ$ | $0,1,2,5,6$ |
| $QP$ | $1,2,5,6$ |

Thus only beta and theta remain from Group 1.

For a primitive plus-norm triple, if $a,b$ are odd, the norm modulo $8$ forces $ab\equiv7$; therefore $a+b\equiv0\pmod8$. If one of $a,b$ is even, it is divisible by $8$: valuation one gives a nonsquare modulo $4$, and valuation two gives $5\pmod8$. For the minus norm, the corresponding odd product is $ab\equiv1$, and again an even side is divisible by $8$.

Substitution gives:

| Coefficient | Possible residues modulo $8$ |
|:--|:--|
| $ab$, minus norm | $0,1$ |
| $ab$, plus norm | $0,7$ |
| $b(a+b)$ | $0,1$ |
| $b(a+2b)$ | $0,1,2$ |
| $(2a+b)(a+b)$ | $0,1,2$ |
| $(a+2b)(2a+b)$ | $2,7$ |
| $3(a+2b)(a+b)$ | $0,3,6$; always divisible by $3$ |

None qualifies. The only branches left are Group-1 beta, Group-1 theta, and double-angle isosceles.

If $N$ is squarefree, the last two require $N=bt^2$ and hence $t=1$, excluded in Sections 3–4. Thus every tiling under these hypotheses must be the beta instance
$$N=3v^2-u^2,\quad \gcd(u,v)=1,\quad 0<u<v.\tag{5}$$
If a prime $p\mid N$, then $p\nmid v$; otherwise (5) gives $p\mid u$. Hence $(u/v)^2\equiv3\pmod p$. This proves the more general assertion at the start of the note.

If in addition $N\equiv19\pmod{24}$, then $N\equiv1\pmod3$, whereas the right side of (5) is $0$ or $2\pmod3$. Contradiction.

If instead $N\equiv35\pmod{120}$, then $5\mid N$, but $3$ is not a square modulo $5$. Contradiction. This proves Theorem A. $\square$

**Without squarefreeness.** When $N\equiv19\pmod{24}$, the same argument still eliminates beta, leaving only theta and double-angle counts $bt^2$ with $t\ge2$. Since $N$ is coprime to $6$, so is $t$; thus $t\ge5$. No claim is made that all nonsquarefree numbers in this progression are impossible.

**Infinite composite families.** These conclusions are not confined to primes. To obtain infinitely many composite examples of the first kind, take $N=7q$, where $q\equiv13\pmod{24}$ is squarefree and $7\nmid q$. Among the first $M$ terms of that progression, the proportion ruled out by a prime square is at most $\sum_{j\ge5}j^{-2}+O(M^{-1/2})<0.24+O(M^{-1/2})$, and divisibility by $7$ rules out at most $1/7+O(M^{-1})$. A positive proportion remains. Similarly, $N=5q$ with squarefree $q\equiv7\pmod{24}$ and $5\nmid q$ gives infinitely many composite examples in the second progression. This elementary counting argument does not require a conjecture about primes in progressions.

Examples in the first family include $91,115,187,235,259$; in the second, $35,155,395,515$. These examples are not claimed to be previously unknown exclusions.

## 6. A finite candidate set for each arbitrary N

The preceding formulas give a uniform **finite overlist** without selecting an experimental tile-side cutoff. Let
$$D_N=\{d:d\mid N,\ N/d\text{ is a positive integer square}\}.$$
The program `candidates.py` does the following.

For theta and double-angle, factor $b=d$ as $(v-u)(v+u)$, test equal parity of the factors, reconstruct $u,v$, and test coprimality (and $v<2u$ for double-angle). The other Group-1 coefficients are at least $Q>v^2$, so it suffices to use $v\le\lfloor\sqrt N\rfloor$.

For the equilateral rows, factor $ab=d$ and test the norm square. For F1 and isosceles, factor $b(a+jb)=d$ for $j=1,2$. For F3 factor $d/3=(a+b)(a+2b)$; for F4 factor $d=(a+b)(2a+b)$; for F2 factor $d=(a+2b)(2a+b)$. The two linear factors recover $a,b$, so only finitely many integer pairs are involved. Every multiplier is then the determined value $\sqrt{N/d}$.

**Theorem D.** Subject to the stated published classification/rationality inputs, any tiling count outside $\mathcal C$ occurs among these fixed tile/target candidates. There are at most $13(N+1)^2$ candidates before symmetry identifications, and every primitive tile side is at most $(N+1)^2$.

**Proof.** Sections 1, 3, 4 exhaust the angular branches and impose the count formulas. For a difference-of-squares coefficient $b\le N$, write $r=v-u\ge1$, $s=v+u=b/r$, so $v\le(N+1)/2$. Other Group-1 rows have $v^2<N$. In the norm families all $a,b\le N$ and $c<a+b\le2N$. These give the side bound. Each of the thirteen parameterized rows has at most $(N+1)^2$ candidate pairs in these boxes, with one multiplier for each pair. The sharper divisor enumeration is equivalent to this coarse finite search. $\square$

An empty overlist excludes a nonclassical $N$. A nonempty overlist says neither that a tiling exists nor that it does not.

For $N=105$ the sieve independently regenerates exactly the four pairs from the earlier package: two equilateral targets with tiles $(5,21,19)$ and $(7,15,13)$, and the two F1 targets $(56,91,105)$ and $(80,95,105)$. This is a check of the arithmetic reduction only; the old four nonexistence certificates were not replayed in this continuation.

## 7. Exact finite geometric search and its limits

Let integer tile sides be $(a,b,c)$, and write
$$D=(a+b+c)(-a+b+c)(a-b+c)(a+b-c)=16\operatorname{Area}(T)^2>0.$$
Represent a point $(x,y)$ physically by $(x,\sqrt D\,y)$. A reference tile is
$$\left(0,0\right),\quad(c,0),\quad
\left(\frac{b^2+c^2-a^2}{2c},\frac1{2c}\right).$$
For a target with integer sides $(A,B,C)$ and area $N$ times the tile, replace $c,b,a,1$ by $C,B,A,N$ in this formula. All coordinates are rational in this basis. Rotation/reflection taking an integer-length tile edge to a known boundary ray stays in this rational plane.

At any finite partial placement, form the **actual** residual boundary by adding the outer boundary and reversed tile boundaries, splitting at all their endpoints and T-junctions, and canceling. A positive-area polygonal residual region has a convex boundary sector of angle strictly between $0$ and $\pi$. At a branch vertex, use an individual sector between consecutive incident rays, not the sum of several disconnected sectors.

In any completion, a tile adjacent to either boundary ray of such a sector must have a vertex at its tip. A tile edge passing through the tip would occupy a local angle $\pi$, which cannot fit. Choose the boundary-adjacent tile on one fixed ray: its corner type has three choices, and the incident side has two. This gives at most six rigid placements. Keep only placements contained in the target, lying in the chosen local cone, and not overlapping a placed tile in positive area. Every genuine completion contains one of them.

Iterate. The depth is at most $N$, and there are at most
$$1+6+6^2+\cdots+6^N=\frac{6^{N+1}-1}{5}$$
nodes before memoization. No denominator grid, packing lemma, collar order, or assumption of edge-to-edge incidence is involved. With $N$ contained disjoint congruent tiles and the correct area, coverage follows from closedness and equality of area.

This proves finiteness and completeness of the abstract search. It does not make the worst-case bound practical. The supplied research program uses exact fractions and optional resource limits. A limit or recursion-resource stop returns `INCOMPLETE`; an unexpected geometric invariant raises an error rather than becoming a contradiction. In particular, the retained run on the $N=154$ candidate is incomplete.

Combining this finite search with Theorem D gives an in-principle total membership procedure. This is not a new resolution of the structural classification question: the per-$N$ finite-search principle is already in [I, G]. We supply an explicit elementary overlist, a rational-coordinate branching proof, and tested code, not a claim that every large outstanding computation has been executed.

## 8. Why more translation-invariant edge weights do not close W or beta

There is a concrete algebraic obstruction to trying to finish the prime candidate solely by adding more such invariants.

For Group 1 use $\gamma=(\pi+\alpha)/2$ and represent a directed edge of length $L$ and direction $n\gamma+j\pi$ by the formal term $(-1)^j Lz^n$. This is the full odd-under-reversal directed-edge signature in $\mathbb Z[z,z^{-1}]$; evaluating it by any linear map includes all length-linear, translation-invariant signed-direction edge tests.

The reference tile signature is
$$p(z)=v^2+bz^2-uvz^3=(v-uz)\,d(z),\qquad d(z)=vz^2+uz+v.$$
The two oriented target signatures, with a suitable exterior side horizontal, are
$$h_W(z)=uQ+vbz-v^3z^{-3},$$
$$h_\beta(z)=uP-v^3(z^3+z^{-3}).$$
A reflected tile, with an optional half-turn, has signature $\pm z^k p(z^{-1})$; an unreflected tile has $\pm z^k p(z)$.

**Theorem E: a formal orientation witness for every scale-one candidate.** The identities
$$\boxed{h_W(z)=v(z^{-1}-z^{-3})p(z)+uz^2p(z^{-1})}$$
and
$$\boxed{h_\beta(z)=v(z^{-1}-z^{-3})p(z)
 +(uz^2-vz^3)p(z^{-1})}$$
hold for all $0<u<v$. Their expanded numbers of tile orientations are $2v+u$ and $3v+u$. They can be increased to exactly $Q$ and $P$, respectively, by adding half-turn pairs with zero signature.

**Proof.** Multiply the first identity by $z^3$ and cancel $d(z)$. It becomes
$$uvz-v^2+bz^2=v(z^2-1)(v-uz)+uz^2(vz-u),$$
an immediate polynomial identity using $b=v^2-u^2$. Subtract $vz^3p(z^{-1})$ for the second identity. The differences
$$Q-(2v+u)=2v(v-1)-u(u+1),$$
$$P-(3v+u)=3v(v-1)-u(u+1)$$
are nonnegative even integers, since $u\le v-1$. A tile and its half-turn have opposite directed-edge signatures and contribute two copies, so padding is possible. $\square$

Thus all these edge signatures, together with the correct tile count and total area, are compatible with **every** W/beta scale-one instance. The formal orientations may overlap or fail to form a target when actual positions are assigned. No assertion about their spatial placement is made.

A particularly small illustration is the theta target at $t=1$. Its signature is
$$h_\theta(z)=b\bigl(u+v(z+z^{-1})\bigr)
 =vz^{-1}p(z)+uz^2p(z^{-1}).$$
The orientation count $u+v$ pads to $b=(v-u)(v+u)$. Yet Section 4 proves every such actual tiling impossible. For $(u,v)=(1,2)$ this gives a three-orientation signature witness for target $(6,6,3)$ and tile $(2,3,4)$, which has no real tiling. This is an explicit separation of boundary-signature feasibility from geometric realizability.

The conclusion is limited to this class of translation-invariant, length-linear directed-edge functionals. It says nothing against position-sensitive invariants, geometric forcing, nonlinear constraints, or a different global classification argument.

## 9. Reproduction and unresolved work

Run from this directory:

```text
python verify_all.py
python candidates.py 105
python exact_search.py 154 --seconds 8 --max-nodes 1000
```

The supplementary arithmetic tests compare the divisor sieve with an independently written bounded parameter sweep for every $N\le300$, cover 61,652 parameter trials and 374 candidate instances, and check 719 positive-area instances. Twenty-one algebraic identities, including the formal signature identities, are checked coefficientwise as polynomials rather than on sample values. They also check 460,844 character integrality/parity instances, the complete residue tables modulo $8$, and the negative progressions up to 6,000. These finite tests supplement, rather than establish, the universal proofs.

A different geometric implementation, based on exact polygon clipping, verifies 18 positive subdivision certificates and the existing 75-tile construction, including all 2,775 tile pairs in the latter. Its 25 T-junction vertices are retained. Eighteen subsets of that known tiling test 274 convex-corner choices, including 53 residual branch-vertex occurrences: a true completing tile remains available in every case. Five corrupted positive certificates are rejected. Node/time-limit controls return `INCOMPLETE`.

The small negative search controls are execution records, not independently replayed proof-tree certificates. No new global exclusion is inferred merely from a stored string `EXHAUSTED`. Theorem A instead has the written symbolic proof in Section 5. A previous long attempt on 154 was externally interrupted and yielded no certificate; the retained bounded retry explicitly reports `INCOMPLETE`.

The full Erdős problem is **not** resolved here. The simplest concrete survivor of the new sieve among the recorded frontier examples is the $N=154$ pair
$$\text{tile }(8,7,13),\qquad\text{target }(91,91,154).$$
This note neither constructs it nor excludes it. The same distinction applies to small scales in the infinitely many other primitive families. Fixed-$N$ decidability, universal necessary spectra, and eventual existence for each fixed tile must not be confused with a finished classification of all counts. The new results do not validate the separate all-primes candidate.

## References and provenance

[R] Michael Beeson and Yan X Zhang, *Rationality of certain triangle tilings*, arXiv:2604.01314v1. Table 1 and Theorem 1.2. <https://arxiv.org/html/2604.01314v1>

[I] Michael Beeson, *Tilings of an Isosceles Triangle*, arXiv:1206.1974v7. Theorems 3.1, 7.10, 11.7, 11.15, and Section 13. <https://arxiv.org/html/1206.1974v7>

[S] Michael Beeson, *No triangle can be cut into seven congruent triangles*, arXiv:1811.09723v5. Theorems 1, 3, 4 and the underlying Laczkovich/Snover–Waiveris–Williams references. We use the classical restrictions, not its larger unproved prime assertions. <https://arxiv.org/html/1811.09723v5>

[G] Michael Beeson, *Triangle Tiling: The case $3\alpha+2\beta=\pi$*, arXiv:1206.2229v4, 25 September 2026. Section 15 is cited for the existing finite-search perspective, not as a source of the withdrawn divisibility necessity or the two open scale-one obstructions. <https://arxiv.org/html/1206.2229v4>

[P] Denis Paliy project notes, *Parity, primitive scales, and constructive spectra for triangle tilings* and *No triangle can be dissected into 105 congruent triangles*, 30 September 2026; and `docs/universal-rational-scales.md` in `DenisUkranian/erdos-634-tilings`. The first note credits Vico Bonfioli's two-character/spectrum framework and Yan X Zhang's constructions. The current proofs rederive the character identities they use. Older numerical certificates are not silently treated as new computations.

No emails or GitHub edits were made in preparing this continuation.

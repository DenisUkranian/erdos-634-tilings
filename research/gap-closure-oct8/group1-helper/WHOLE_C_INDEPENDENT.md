# Independent proof of the whole-c boundary theorem

Let `(a,b,c)` be a primitive positive integral triangle with
`c^2=a^2+ab+b^2`. Suppose a nonempty finite polygonal region is tiled by N
congruent copies, and its entire oriented boundary, including every hole,
can be represented by whole length-c segments whose directions all belong
to **one class modulo 60 degrees**. Equivalently, after rotation their
directions are powers of `rho=exp(i*pi/3)`. A formal integer chain of such
segments is enough; connectedness and absence of holes are unnecessary.

Then

```
c^2 divides N;
if ab is even, 2c^2 divides N;
in every case, N>=2c^2.
```

The common direction-class hypothesis is essential to the proof. Merely
saying that all boundary edges are long tile edges, while allowing several
height classes, does not meet it.

## Arithmetic and area

Primitivity implies pairwise coprimality of a,b,c. In particular c is odd
and `gcd(c,ab)=1`. Also 3 does not divide c: otherwise the norm identity
forces `a=b mod3`; if neither is divisible by3 its right-hand side has
3-adic valuation one, inconsistent with being c squared.

The boundary chain is balanced at its endpoints and decomposes into closed
walks of c-steps. Each walk's vertices lie in a translate of `c Z[rho]`.
Its signed area is an integer multiple of `c^2 sqrt(3)/4`, even if it
self-intersects. Summing the walks gives the region area. A tile has area
`ab sqrt(3)/4`, so `abN` is divisible by c squared, hence `c^2|N`.

## Boundary character

Relabel a,b so that a>b, and put

```
delta=a-b>0, D=c^2-delta^2=3ab, z=(a+b*rho)/c.
```

The equality a=b is impossible for positive integral a,b,c. The standard
direction-propagation lemma gives every tile edge a direction `rho^j z^h`
with integer h after anchoring one boundary direction. This can be done
in each positive-edge-contact component. Every component meets the boundary;
T-junctions preserve edge-direction propagation. The powers of z are distinct
modulo powers of rho: z lies strictly between the adjacent root-of-unity
directions and the only roots of unity in Q(rho) are powers of rho.

Give an oriented segment of direction `rho^j z^h` the additive character
`length*(-1)^j X^h`. Opposite orientations have opposite characters, so
every internal seam cancels, with arbitrary subdivisions and T-junctions.
For the twelve rotations/chiralities at a fixed height the tile characters
are signed monomials times either `delta-cX` or `delta-c/X`. Consequently
there exist integer Laurent polynomials U,V and an integer M such that

```
(delta-cX)U(X)+(delta-c/X)V(X)=cM.                 (1)
```

Each tile contributes exactly one signed monomial to U or V. Therefore,
with `S=U(1)+V(1)`,

```
|S|<=N,                 S=N mod2.               (2)
```

No restriction on positive or negative tile heights is used.

Since `gcd(c,D)=1`, set `s=delta*c^(-1) modD`. The identity
`delta^2=c^2-D` gives `s^2=1 modD`, so the evaluation of Laurent polynomials
at s is legitimate and both left factors of (1) vanish. Hence `D|M`.
Writing `M=Dk` and evaluating at X=1 gives

```
S=-c(c+delta)k.                                   (3)
```

If ab is even, delta is odd and c+delta is even. Thus S and N are even.
Since c is odd and `c^2|N`, this proves `2c^2|N`.

If ab is odd and N=c squared, then N is odd and delta is even. Equations
(2)-(3) force k odd and nonzero. They then imply

```
N >= |S| >= c(c+delta) > c^2,
```

a contradiction. The area divisibility excludes all other positive counts
below 2c squared. This proves the universal lower bound.

## Audit scope

This proof was derived independently of the structure-note author. It uses
the standard height-direction framework but neither a finite enumeration nor
an assumed pure-height interior. The conclusion applies to mixed heights,
holes, and multiple components under the stated common boundary class.

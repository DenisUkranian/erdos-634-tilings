# Exact two-long-edge arithmetic for a theta base

7 October 2026. This is a closed-form consequence of the already established
at-least-two-c-edge boundary theorem in `../../docs/theta-branch.md`, not a
new proof of that theorem and not a sufficient condition for a tiling. The
new longest-edge adjacency theorem gives a further ordering restriction.

Let a=uv, b=v²-u², c=v² with 0<u<v coprime. At theta scale t the base
length is L=utb. Put q=floor(ut/v) and r=ut-vq, so 0<=r<v.

**Exact side-count criterion.** There exist nonnegative counts A,B,C with
C>=2 and Aa+Bb+Cc=L if and only if

    b floor(ut/v) - 2v belongs to <u,v>.

Here <u,v> means nonnegative integer combinations of u and v. Necessity
of the exact side-count criterion for tilings follows from C>=2; the
criterion asserts only an edge-count representation, not placements.

Proof. Reduction modulo v, using gcd(b,v)=1, gives B=r+kv for k>=0.
Subtract rb and divide by v:

    bq = Au + Cv + kb.

Since b=(v-u)u+(v-u)v belongs to <u,v>, subtracting 2v shows necessity.
Conversely a representation bq-2v=Au+C'v supplies B=r and C=C'+2.
Equivalently, each group of v b-edges in any count solution may be
replaced at the arithmetic level by v-u a-edges and v-u c-edges:

    v b = (v-u)a + (v-u)c.

This substitution is about counts only, not about an actual boundary
replacement inside a tiling. QED.

In particular every actual theta tiling necessarily satisfies

    b floor(ut/v) >= 2v,
    t >= ceil( v*ceil(2v/b) / u ).

For u=1, v>=3 this simplifies to t>=v, since b=v²-1>=2v. For (u,v)=(1,2)
it gives t>=4, matching the existing exact spectrum's lower bound. For
u=v-1 it excludes t=2, but that exclusion was already supplied by the
known independent apex bound b(t-1)>=2v and is not newly claimed here.

## The semigroup test simplifies completely

Put d=v-u. If d>=2, then

    b-2v = d*u + (d-2)*v belongs to <u,v>.

Since b also belongs to this semigroup, every q>=1 works, while q=0
fails by negativity. If d=1, then b=2v-1, so b-2v=-1 fails, whereas

    2b-2v = 2(v-1) = 2u belongs to <u,v>.

Every q>=2 then works. Consequently the exact base-count condition is
simply

    t >= ceil(v/u)       if v-u>=2,
    t >= ceil(2v/u)      if v-u=1.

These are equivalent to the preceding nested-ceiling bound. For d>=2,
b>=2v; for d=1, v<=b<2v. This is an exact classification of **the base
length's whole-edge counts with C>=2**, not of actual theta tilings.
The explicit constructions of counts use B=(ut mod v), C=2+C', and
the displayed nonnegative (u,v)-semigroup expressions.

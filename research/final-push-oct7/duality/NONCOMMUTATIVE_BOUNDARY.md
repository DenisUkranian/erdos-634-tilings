# Ordered boundary words: prime-exponent quotients do not obstruct F3

Assume the previously established integer-atom theorem and take a
primitive plus-norm tile

    c^2 = a^2 + ab + b^2.

Put rho = exp(i*pi/3), z = (a+b*rho)/c. Let G be the group with symbols
`e(h,j)` for h in Z and j modulo 6, the reversal relation
`e(h,j+3)=e(h,j)^(-1)`, and the tile relations

    e(h,j)^a e(h,j+1)^b = e(h+1,j)^c,
    e(h,j)^a e(h,j-1)^b = e(h-1,j)^c.                 (1)

These are imposed for every h,j. The second family accounts for reflected
tiles. A unit directed segment of direction `z^h rho^j` is labeled by
`e(h,j)`. Subdivide integer-length sides into unit atoms. A genuine disk
tiling makes its ordered exterior word trivial in G: the face words
are defining relators and oppositely traversed interior atoms cancel
in a disk diagram. This uses only the usual elementary disk relation;
it makes no assertion that an arbitrary group identity has a positive
geometric realization.

For the canonical F3 target at scale m the exterior word is

    B_m = e(0,0)^(m c^2)
          e(2,1)^(3m b(a+b))
          e(3,0)^(-m c(a+2b)).                     (2)

## Proposition

For every prime p, every homomorphism from G to a group of exponent p
sends B_m to the identity, for every positive integer m. The receiving
group need not be abelian or finite.

**Proof.** Work modulo p in all exponents. Primitivity makes a,b,c
pairwise coprime, so at most one is zero modulo p.

First note a consequence of (1) and its half-turn (j replaced by j+3).
If `x=e(h,j), y=e(h,j+1), w=e(h+1,j)`, they give both

    x^a y^b = w^c,      y^b x^a = w^c.

Hence x^a and y^b commute.

If p does not divide abc, raising to each of a,b,c is invertible on
each cyclic subgroup. Thus x and y commute. The three independent
directions at every height commute pairwise. Equations (1), using the
unique c-th root `g -> g^(c^(-1))`, express the generators at adjacent
heights in the abelian subgroup at the current height. The full image
of G is therefore abelian. The F3 word is zero in the abelianization:
this is exactly the already verified integral full-signature identity
in `research/f3-descent-attempt/check_full_signature.py`. Consequently
B_m maps to the identity.

If p divides a, put `s=b/c` modulo p. The norm identity gives s^2=1.
Equations (1) imply

    e(h,j) = g(j+h)^(s^h),   g(j+3)=g(j)^(-1),

where `g(j)=e(0,j)`. No commutativity of the g(j) is needed. In (2),
`e(2,1)=g(0)^(-1)` and `e(3,0)=g(0)^(-s)`. The total exponent of
g(0) is

    m b^2 - 3m b^2 + 2m s b c = 0,

because s c=b. Thus B_m is trivial.

If p divides b, put s=a/c, again with s^2=1. Now
`e(h,j)=g(j)^(s^h)`. The middle factor in (2) vanishes, and the first
and third have total exponent `m c^2 - m s c a = 0`.

If p divides c, a and b are invertible. At any fixed height let
`x=e(h,j), y=e(h,j+1)`. The first relation and the reflected relation
with index j+1 give

    x^a y^b=1,       y^a x^b=1.

Therefore `y=x^(-a/b)` and `x^(b^2-a^2)=1`. The coefficient
`b^2-a^2` is nonzero modulo p: a=-b contradicts the norm equation,
whereas a=b would force p=3. The primitive plus-norm triple has
3 not dividing c (if a=b nonzero modulo 3, the norm is 3 modulo 9).
Thus x=1, and all generators at every height are trivial. This proves
the proposition.

## Finite-exponent extension and its limit

The first case works without primality: if a receiving group has finite
exponent E and `gcd(abc,E)=1`, the image of G is abelian, so B_m is
trivial. The roots used in the proof are unique because if `x^r=y`
and `r q=1 mod E`, then `x=y^q`.

One cannot extend the *commutativity conclusion* to all finite p-groups.
When p divides a, the construction
`e(h,j)=g(j+h)^(s^h)` above satisfies every relation for arbitrary
g(0),g(1),g(2) in any exponent-p group. For the tile (24,11,31) and
p=3, take two noncommuting generators of the order-27 Heisenberg group
as g(0),g(1), and take g(2)=1. This is a genuine nonabelian quotient;
nevertheless every F3 boundary word still vanishes in it.

Nothing here decides quotients whose exponent contains higher prime
powers dividing abc, arbitrary finite groups, or G itself. Most
importantly, even triviality of B_m in G would only produce a group
diagram; positivity and geometric completion would still need proof.

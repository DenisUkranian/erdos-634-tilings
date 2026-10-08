# Scope audit: quadratic tilings and the theta nonsquarefree obstruction

8 October 2026. This is a fresh mathematical and terminology audit, not a
new theorem, external review, or priority claim.

## Distinguish the shapes explicitly

The phrase "quadratic shape" is not a sufficiently precise name to identify
one of the five nonsimilar Group-1 targets. In Beeson's
[isosceles paper, version 7](https://arxiv.org/html/1206.1974v7), Section 1
defines a *quadratic tiling* to be the ordinary subdivision into n squared
congruent similar triangles. Theorem 2.1, attributed there to Snover,
Waiveris, and Williams, says that a nonsquare reptiling count requires a
right triangle. Therefore, in the similar-tile case for an obtuse Group-1
tile, N is a square; for a nontrivial tiling it is nonsquarefree. This is
an established result, not the project's added theta argument.

The project result in
[`docs/theta-squarefree-obstruction.md`](../theta-squarefree-obstruction.md)
concerns precisely the isosceles target with angles

```
(alpha, alpha+beta, alpha+beta),    3 alpha+2 beta=pi.
```

It does not concern the base-beta isosceles target or the W target.
Beeson's [Group-1 paper, version 4](https://arxiv.org/html/1206.2229v4),
Theorem 22, already proves non-primality for the theta target. The
project's short proof gives the stronger nonsquarefree restriction and a
quantitative lower bound, without claiming external novelty.

The other scalene target `(2 alpha, alpha, 2 beta)` must also be kept
separate. Source Theorem 16 proves non-primality there, but nonsquarefree
is false: its constructed example N=77 with tile `(2,3,4)` is squarefree
(source Theorem 15 and Table 3; also the project's two-piece construction).

## Fresh check of the theta proof

Normalize the rational tile to

```
a=uv, b=v^2-u^2, c=v^2, 0<u<v, gcd(u,v)=1.
```

The published Group-1 rationality theorem is the external input. No
scale-one exclusion is used. The following steps have been checked anew.

1. Every outer side is a concatenation of whole integer-length tile
   edges. A supporting-line tile edge cannot extend beyond an outer
   corner while staying inside the convex target; positive overlaps of
   two such boundary edges would overlap tile interiors.
2. Every outer side contains a c-edge. Otherwise each of its n boundary
   tiles contributes its obtuse gamma angle at one endpoint. The two
   outer corners have angles less than gamma, and the n-1 internal
   junctions accommodate at most one gamma angle each, since 2 gamma>pi.
   This contradicts n>n-1. The same pigeonhole observation is already
   present in the proof of source Theorem 22; it is not a new general
   boundary lemma claimed without attribution.
3. The identity `2 cos(alpha)=2-u^2/v^2` is rational and strictly between
   1 and 2. If alpha/pi were rational it would be a rational algebraic
   integer, impossible. At the alpha apex, a fan with counts p,r,s has
   `(2p-3r+s-2) alpha+(r+s) pi=0`. Thus r=s=0 and p=1. The unique apex
   tile contributes a whole b-edge to one of the equal target sides.
4. If X is the common equal-side length, area gives `X^2=N b v^2`.
   Since X is integral, v divides X. Writing `b=q h^2` with q squarefree
   then gives `N=q t^2` and `X=v q h t`, with positive integers h,t.
5. On the equal side selected at the apex write
   `X=Auv+B(v^2-u^2)+Cv^2`. Modulo v, `gcd(b,v)=1` implies v divides B.
   Since B>0, B>=v; step 2 gives C>=1. Therefore

```
v q h t >= v q h^2+v^2,
q h(t-h) >= v.
```

In particular t>h>=1, so N=q t squared is not squarefree. This remains
valid with arbitrary interior T-junctions and reflections: the argument
uses only the convex exterior sides and the apex fan.

The optional attachment argument in Section 5 of the old note is not
used. Neither the W candidate, the base-beta candidate, nor an asserted
classification of all prime counts is required anywhere in this proof.
The old prime-case dependency file remains a conditional dependency audit;
its historical wording does not establish either candidate geometric lemma.

## Unambiguous correspondence wording

One can state the result without interpreting an informal shape name:

> To be precise, the separate nonsquarefree statement I meant concerns
> the isosceles target with angles (alpha, alpha+beta, alpha+beta), for a
> tile satisfying 3 alpha+2 beta=pi. I have a short boundary-and-area
> argument for that statement, independent of the proposed W and
> base-beta exclusions. I recognize that non-primality for this shape
> is already your Theorem 22; I am not claiming a new quadratic-reptiling
> theorem.

If the intended target is instead `(2 alpha, alpha, 2 beta)`, explicitly
state that only non-primality is asserted; its 77-tile construction rules
out a nonsquarefree claim.

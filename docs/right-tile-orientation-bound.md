# A parity argument and orientation bound for the right-tile branch

4 October 2026, Kyiv. Research directed by Denis Paliy, with ChatGPT assistance.
The argument below addresses the parity step identified in the
[orientation audit](orientation-reduction-audit.md). It was checked
separately within this investigation; no external acceptance or priority
is asserted. The parity theorem is independent. The fixed-pair orientation
corollary additionally uses the shape classification and Beeson,
*Tilings of an Isosceles Triangle*, Lemma 7.5. Neither invokes Theorems
7.8 or 7.10. The universal orientation conjecture and Erdős problem 634
remain unresolved.

## Imported boundary lemma

Suppose a non-equilateral isosceles target has base angles beta and is tiled by the right tile with angles (alpha,beta,pi/2), where alpha/pi is irrational. Put lambda=sqrt(N/2), normalize the tile hypotenuse to 1, and suppose lambda is irrational. Beeson Lemma 7.5 states:

* both legs are rational multiples of lambda, hence their ratio is rational;
* the base of the target consists solely of hypotenuses, and its equal sides contain no hypotenuses.

Source: https://arxiv.org/html/1206.1974v7, Lemma 7.5; also https://michaelbeeson.com/research/papers/IsoscelesTilings.pdf (January 4, 2026), printed pp.14–16.

This lemma is a published dependency of the fixed-pair corollary, not of
the parity theorem below. Its statement is separate from the invalid
sine/tangent step in Theorem 7.8. We do not claim to have replaced its
entire c-edge-graph proof here.

## Boundary arithmetic leaves only one parity obstruction

Scale the right tile to primitive integral legs r,s, with gcd(r,s)=1, hypotenuse c=sqrt(d), d=r²+s², and alpha=atan(r/s). Take the target apex to have angle 2alpha. Its equal sides have length lambda c; its base has length 2lambda r. The imported lemma gives integers M,K with

    lambda c = M,
    2lambda r = K c.

Thus 2Mr=Kd. Since gcd(r,d)=1, d divides 2M. Write 2M=kd. Then

    lambda = k c/2,
    K = kr,
    N = k² d/2.

If k is even, say k=2m, each half of the target has the usual biquadratic tiling with grid scales mr and ms. These are exactly the original tile and target; the four grids use N=2m²(r²+s²) tiles. There are at most eight rigid orientations.

If k is odd, integrality of N forces d even, hence r and s both odd. Since odd squares are 1 modulo 8, d is 2 modulo 8 and then N=k²d/2 is odd. The next theorem rules this out for irrational alpha/pi. Thus k must be even. The case r=s=1 is the similar right-isosceles case, already covered separately.

## Independent parity theorem for arbitrary irrational-angle right tiles

Let a right tile have acute angles alpha,beta with alpha+beta=pi/2 and alpha/pi irrational. If it tiles an isosceles target with base angles beta, then the number N of tiles is even.

This theorem needs neither rational leg ratios nor the imported Lemma 7.5.

### Coordinates and integer direction heights

Normalize the tile's hypotenuse to 1, and put

    lambda = sqrt(N/2),
    z = exp(i alpha).

The target's equal sides have length lambda. In complex coordinates place its apex and base corners at

    O=0, B=lambda, C=lambda z².

The target is positively oriented O,B,C. Its equal sides have directions 0 and 2alpha; its base BC has direction alpha+pi/2.

If lambda is rational, write lambda=h/k in lowest terms. From N=2h²/k² follows k² divides 2, hence k=1. Therefore N=2h² is even. It remains to assume lambda irrational.

Starting with a tile with an edge on OB, and passing through the connected graph of positive-length tile contacts, every tile-edge direction has the form

    h alpha + j pi/2

for integers h,j. This is because the reference triangle's edge directions differ by integer combinations of alpha and pi/2. A generic path between tile interiors avoids the finite vertex set, which proves that the contact graph is connected even with T-junctions.

Irrationality of alpha/pi makes h unique modulo the quarter-turn term: if h alpha+j pi/2=h' alpha+j' pi/2 modulo 2pi, then h=h'. Call h the height of the direction. Both leg directions of each tile have the same height; its hypotenuse height differs from that height by one.

### A finite directed graph of whole hypotenuses

Select every tile whose leg height and hypotenuse height are the two values 0 and 1, **in either order**. Direct its whole hypotenuse from its alpha endpoint to its beta endpoint. Vertices of this finite directed multigraph are geometric endpoints of selected hypotenuses. An edge passing through another graph vertex is not split there; only its own endpoints count for incidence. Coincident tile edges remain distinct graph edges.

At any tiling vertex other than O,B,C, examine the tile sectors counterclockwise. An alpha corner raises ray height by one, a beta corner lowers it by one, and a right-angle corner leaves it unchanged. A tile whose edge passes through the point occupies a straight angle, which also leaves the height unchanged. The initial and final heights agree, at interior vertices and at straight points of the target boundary alike.

Therefore upward crossings of the cut between heights 0 and 1 balance downward crossings. These crossings are exactly the alpha and beta endpoints of selected tiles. Thus every noncorner graph vertex has equal indegree and outdegree.

At O the interior angle runs counterclockwise from height 0 to height 2, giving net outdegree minus indegree 1. At B it runs from height 1 to height 0, giving net indegree minus outdegree 1. At C it runs from height 2 to height 1 and does not cross this cut. Hence O is the only source and B the only sink.

The graph has a directed path from O to B. Otherwise the set reachable from O excludes B and has total outdegree minus indegree 1, although no edge leaves that set, an impossibility.

### A Gaussian-integer norm forces N even

Selected hypotenuses have length 1 and direction height either 0 or 1. Each path displacement is one of

    ±1, ±i, ±z, ±iz.

Summing along the path gives

    lambda = U + V z,       U,V in Z[i].

Since lambda is irrational, V is nonzero. Since |z|=1,

    |V|² = |lambda-U|²
          = lambda² - 2lambda Re(U) + |U|².

The quantities |V|² and |U|² are integers, and lambda²=N/2 is rational. Irrationality of lambda therefore forces Re(U)=0. Consequently

    lambda² = |V|² - |U|²

is an integer. Thus N=2lambda² is even, completing the proof.

This argument permits every orientation and arbitrary T-junctions. It invokes no mixed-area functional, coordinate rationality, hypotenuse-pairing assumption, or classification of all tilings.

## Resulting fixed-pair bound

Combining the imported Lemma 7.5 with the parity theorem and boundary arithmetic proves the following:

* For a non-similar isosceles target tiled by a right tile with irrational acute angles, the same target has a tiling by the same tile with at most **eight** rigid orientations: double quadratic if lambda is integral, or double biquadratic otherwise.
* Rational-angle pairs have the bound **24** proved in the [orientation audit](orientation-reduction-audit.md), under its stated shape-classification input.
* Similar tile/target pairs have the bound **six** from the fixed-pair classification cited in that audit.

Thus the classical branches have an absolute bound 24, with explicit dependencies on the usual shape classification, similar-pair theorem, and Lemma 7.5. This settles the previously isolated classical source-audit obstruction. It does not prove the orientation conjecture for the nonclassical rational-side branches or prove the stronger finite-block conjecture.

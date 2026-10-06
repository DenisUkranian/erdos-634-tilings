# Complete odd-multiplier criterion in square class 110

**Research directed by Denis Paliy, with ChatGPT assistance — 6 October 2026**

Let \(\mathcal S\) be the set of positive integers that count congruent
nondegenerate triangles in a dissection of a nondegenerate triangle.
Reflections and arbitrary T-junctions are allowed.

**Theorem.** For every positive odd integer \(m\),

\[
\boxed{110m^2\in\mathcal S\quad\Longleftrightarrow\quad3\mid m.}
\]

This settles every odd multiplier in this square class. It does not
classify the even multipliers, the other square classes, or all of
Erdős problem 634. The new positive input is the verified primitive
F3 tiling with 990 tiles; the branch-isolation theorem and integral
necessary spectra are prior project inputs.

## Necessity

If m is odd, its square is 1 or 9 modulo 16. Since \(110\equiv14\pmod{16}\),
both possibilities give

\[
110m^2\equiv14\pmod{16}.
\]

The prime 5 has odd valuation:

\[
v_5(110m^2)=1+2v_5(m).
\]

The [F3 isolation theorem](f3-global-overlap.md), Theorem 1.1,
therefore forces any realization of \(110m^2\) into the 120-degree
F3 branch. That theorem uses the exhaustive angular classification,
rationality and the integral primitive spectra recorded in the
[uniform-reduction proof](../research/uniform-reduction/PROOF.md).
It excludes all other classified branches, including the classical
ones, under these two arithmetic conditions.

Every F3 count has the necessary form

\[
N=3(a+2b)(a+b)t^2,
\qquad c^2=a^2+ab+b^2,
\]

with positive integers \(a,b,c,t\), after primitive normalization.
In particular \(3\mid N\). Since 3 does not divide 110, this forces
\(3\mid m^2\), equivalently \(3\mid m\). This is a global negative
argument, not a failure of a particular construction.

## Sufficiency

The [nested-corner construction](../research/group2-nested-corners/PROOF.md)
now supplies the primitive F3 tiling

\[
(a,b,c)=(8,7,13),\qquad
N=3(8+2\cdot7)(8+7)=990,
\]

whose target has sides \((169,286,315)\). Its explicit arithmetic
construction parameters include the rectangle width k=1, with

\[
kc=13\ge a-b=1,\qquad
bc-a^2=91-64=27=2b+c\in\langle a,b,c\rangle.
\]

The nested-corner theorem turns these conditions into an actual
positive partition. The resulting
[990-tile coordinate certificate](../research/group2-nested-corners/f3-990.json)
was independently checked in exact rational arithmetic for congruence,
target containment, all 489,555 tile pairs, and equality of total area.
Its [geometric report](../research/group2-nested-corners/f3-990-geometric-report.json)
records these checks. A separate
[coordinate-free disk certificate](../research/group2-nested-corners/disk-990.json)
also passed exact development and degree-one nonoverlap verification;
the [disk report](../research/group2-nested-corners/f3-990-disk-report.json)
records 100 genuine interior T-junctions.

Now write \(m=3k\), where k is a positive integer. Scale the certified
target by k and subdivide each enlarged tile by the ordinary parallel
grid into \(k^2\) congruent copies of the original tile. This gives

\[
990k^2=110(3k)^2=110m^2
\]

tiles. Hence every multiplier divisible by 3 is admissible. In fact
this positive direction also holds for even m divisible by 3; the
necessity proved above is asserted only for odd m.

## Scope and change from the earlier reduction

Previously, the old balanced construction covered the odd multipliers
divisible by 3 from m=9 onward, leaving the single primitive count 990.
The new 990 certificate removes that last gap. No elliptic-rank
assumption, finite-search extrapolation, proposed all-primes theorem,
or retracted divisibility condition enters the criterion.

The result has internal symbolic and exact computational verification.
External peer review and formal proof-assistant verification are not
claimed.

# A universal lower bound for a boundary in one long-edge lattice

8 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

This is a necessary theorem for actual tilings. It does not classify F3,
exclude 14430, or prove a normal form for arbitrary tilings.

## Statement and scope

Let `(a,b,c)` be a primitive positive integral triangle satisfying

\[
c^2=a^2+ab+b^2.
\]

Its angle opposite `c` is 120 degrees. Write

\[
\rho=e^{i\pi/3},\qquad z=(a+b\rho)/c.
\]

Suppose a bounded polygonal region of positive area is tiled by `n`
congruent copies of this triangle, including reflected copies. Holes,
nonconvex boundary, and T-junctions are allowed. Assume that, for one fixed
integer `k`, every directed boundary segment is an integer multiple of
one of

\[
c\rho^jz^k\quad (j=0,\ldots,5).
\tag{1}
\]

Assume the tiles and boundary have a common direction normalization:
every short edge has direction `rho^j z^h` for integers `j,h`. This is
automatic for a connected positive-length contact component after one
edge direction is fixed. For multiple components the hypothesis is
required for each component, with the same boundary class, or the
conclusion may be applied separately to each component. Different
boundary loops need not have the same translational lattice phase.

Then

\[
\boxed{c^2\mid n,\qquad n\ge 2c^2.}
\tag{2}
\]

If `ab` is even, the stronger divisibility holds:

\[
\boxed{2c^2\mid n.}
\tag{3}
\]

No restriction is placed on the number of interior direction classes.
In particular, this is not a pure-tiling or convex-island theorem. The
boundary condition (1) concerns one class of directions modulo 60
degrees; a boundary using two such classes does not satisfy it.

## Primitive arithmetic and direction notation

Primitivity implies the pairwise coprimality of `a,b,c`. Indeed, a prime
dividing two of them divides the third by the norm equation. Also `c` is
odd: reduction modulo 2 rules out even `c` unless both `a,b` are even.
One has `3` not dividing `c`. If `3` divided `c`, the norm equation
modulo 3 would imply `a=b (mod 3)`; when neither is divisible by 3 its
left norm is 3 modulo 9, a contradiction. Consequently, on putting
`d=a-b`,

\[
\gcd(c,ab)=\gcd(c,d)=1,\qquad
(c-d)(c+d)=3ab.
\tag{4}
\]

For the second coprimality, a common prime divisor of `c,d` must divide
`3b^2`, so it can only be 3. Also `a` and `b` are unequal, since otherwise
`c^2=3a^2` is impossible for positive integers.

The short height of a tile is the common class `h` of its two short
edges. Its long edge has height `h-1` or `h+1`. These heights are unique:
if a nonzero power of `z` were a sixth root of unity, `z` would be a root
of unity in `Q(sqrt(-3))`, hence itself a sixth root of unity; its
argument is strictly between 0 and 60 degrees. Common direction
normalization propagates across positive-length contacts. Splitting a
contact at a T-junction does not change its direction.

## Area divisibility, with holes and winding

Each oriented boundary loop is a closed walk whose steps belong to
`c z^k Z[rho]`. After translating its first vertex to zero, its vertices
belong to that lattice. The fundamental parallelogram has area
`c^2 sqrt(3)/2`; the shoelace formula therefore gives signed loop area
in `c^2 sqrt(3)/4` times the integers. Apply this to every loop, with
inner loops oppositely oriented. If a polygonal boundary touches itself,
decompose its oriented chain into closed walks; signed area remains
additive. No common translation between different loops is needed.

The sum of these signed areas is the area of the region, namely
`n ab sqrt(3)/4`. Therefore `c^2` divides `n ab`. Equation (4) gives
`c^2 | n`.

## A character of the full directional current

Use the two counterclockwise reference triangles

\[
T_A=(0,a,b\rho^2),\qquad T_B=(0,b,a\rho^2).
\]

For each height `h`, let `A_h,B_h` be signed three-vectors: the count
at rotation `j+3` is subtracted from that at rotation `j`, for `j=0,1,2`.
Let `R` be rotation by 60 degrees on these vectors. Then

\[
R^2(v_0,v_1,v_2)=(-v_1,-v_2,v_0).
\]

The counterclockwise directional current at height `h` is

\[
J_h=(aI-bR^2)A_h+(bI-aR^2)B_h-cA_{h+1}+cR^2B_{h-1}.
\tag{5}
\]

This is an identity of length currents after discarding positions. In
an actual tiling, internal contacts cancel after atomization, including
arbitrary T-junctions. Thus `J_h` equals the exterior boundary current.
The edge convention and (5) are also documented in
[the directional-current derivation](../../closure-position-oct7/dual/DIRECTIONAL_SUPPORT.md).

Define the integer character

\[
\chi(v_0,v_1,v_2)=v_0-v_1+v_2.
\]

It satisfies `chi(R^2 v)=chi(v)`. Set `u_h=chi(A_h)` and
`v_h=chi(B_h)`. The scalar version of (5) is

\[
S_h=d(u_h-v_h)-cu_{h+1}+cv_{h-1}.
\tag{6}
\]

Condition (1) says `S_h=0` for `h!=k`, while `S_k=cM` for an integer
`M`. More concretely, an oriented boundary step `ell*c*rho^j*z^k`
contributes `ell*(-1)^j` to `M`. Reversing the step changes this sign,
so the definition is independent of the chosen directed representative.

All sums below are finite. Put

\[
D=\sum_h(v_h-u_h),\qquad
D_*=\sum_h(-1)^h(v_h-u_h).
\]

Each tile contributes either `1` or `-1` to each of these two integers.
Consequently

\[
|D|,|D_*|\le n,\qquad D\equiv D_*\equiv n\pmod2.
\tag{7}
\]

Summing (6), first normally and then with alternating signs, gives

\[
cM=(c-d)D,\qquad
(-1)^k cM=-(c+d)D_*.
\tag{8}
\]

## The resulting divisibility and size obstruction

Write `s=c-d`, `t=c+d`. Both are positive, `st=3ab`, and
`gcd(c,s)=gcd(c,t)=1`.

If `ab` is odd, `d` is even and `s,t` are odd and coprime. Equations
(8) force `M=st*r=3ab*r` for an integer `r`, and

\[
D=ct r,\qquad D_*=-(-1)^k cs r.
\tag{9}
\]

Here `c,s,t` are odd, so (7) gives `r=n (mod 2)`.

If `ab` is even, `d,c` are odd. The integers `s/2,t/2` are coprime,
have opposite parity, and sum to the odd number `c`. Equations (8)
first force `M=(st/2)q` for an integer `q`. They then give
`D=c(t/2)q` and `D_*=-(-1)^k c(s/2)q`. Their equal parity in (7)
forces `q` even. Again `M=st*r` and (9) hold. In this case both `D`
and `D_*` are even, so `n` is even. Together with `c^2 | n` and odd
`c`, this proves (3).

In both cases, (7) and (9) yield the additional quantitative bound

\[
M=3ab r,\qquad
c\bigl(c+|a-b|\bigr)|r|\le n.
\tag{10}
\]

Suppose now `n=c^2`. If `ab` is even, (3) already rules it out. If
`ab` is odd, then `n` is odd and `r` must be odd, hence nonzero.
But (10) would imply

\[
c^2\ge c\bigl(c+|a-b|\bigr)>c^2,
\]

a contradiction. Since `n` is a positive multiple of `c^2`, (2)
follows.

## Application to a separating height gap

Consider a tiling of a convex polygon, and an empty short height `k`.
Separate a nonempty upper tail of tiles of short height greater than
`k` from the lower tiles. Assume the tail does not touch an exterior
boundary segment of height greater than `k`; exterior segments of
height `k` are permitted if they have length an integer multiple of
`c`.

At a positive-length interface of the upper and lower tile sets, the
only possible common edge height is `k`. Since no short edge has that
height, both incident edges are long edges of length `c`. On a maximal
straight seam, the partitions into whole `c`-edges on its two sides
have the same endpoints and therefore coincide. Convexity of the
original target ensures that an endpoint on the exterior cannot leave
one side of this straight seam continuing outside the region. The same
argument holds at an interior seam endpoint. Thus the tail boundary
consists of whole `c`-edges of height `k`, including in the presence of
T-junctions elsewhere. Apply (2) and (3) to every positive-area contact
component of that tail. The lower-tail statement follows by reflection.

For the canonical scale-one F3 triangle

\[
P=\operatorname{conv}\{0,c^2,c(a+2b)z^3\},\qquad
N=3(a+b)(a+2b),
\]

the boundary heights are `0,2,3`; the sides at heights `0` and `3`
have lengths divisible by `c`. Hence the preceding application holds
for an upper separating gap `k>=3` or a lower separating gap `k<=0`.
It says nothing by itself about gaps at heights `1,2`.

In particular, if `ab` is even and `N<4c^2`, every such nonempty tail
has exactly `2c^2` tiles. There can be only one positive-area contact
component. It has no hole: the tiles filling a hole themselves have
a one-class whole-`c` boundary and require at least another `2c^2`
tiles, contradicting `N<4c^2`. This statement concerns an empty height;
it does not bound a consecutive occupied interval.

For `(a,b,c)=(56,9,61)` one has `N=14430<4c^2=14884`, so every such
separated tail would have exactly `7442` tiles. This is a necessary
restriction, not a proof that 14430 is impossible. The positive 4830
example with `(24,11,31)` has `4830>4*31^2`, so the last small-area
specialization does not apply to it.

## What is not asserted

The stronger divisibility `2c^2 | n` is only proved here when `ab` is
even. For arbitrary odd `ab`, the result is `c^2 | n` and the strict
exclusion of the first positive multiple. Nor does the theorem say
that a mixed-height region can be replaced by a pure tiling, that a
separated tail is convex, or that three direction classes suffice for
every F3 tiling. Those would be additional geometric assertions.

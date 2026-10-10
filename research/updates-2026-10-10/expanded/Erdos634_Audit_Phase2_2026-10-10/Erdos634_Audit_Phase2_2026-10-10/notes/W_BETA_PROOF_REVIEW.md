# Universal W/beta construction: proof-level review and independent checks

10 October 2026. Audit for Denis Paliy, with ChatGPT assistance.
This note reorganizes the existing 9 October unrestricted construction.
It claims no new sufficient range, necessity result, priority, or outside review.
The original 483-line proof is retained unchanged in `inputs`.

## 1. Exact claim and the short dependency chain

For coprime integers 0<u<v, let

    a=uv, b=v^2-u^2, c=v^2, d=v-u,
    Q=2v^2-u^2, P=3v^2-u^2.

The SAME fixed tile (a,b,c) tiles W of sides M(v^3,uQ,vb), and beta of
sides M(v^3,v^3,uP), for every integer M>=v. Counts are QM^2 and PM^2.
The claim allows reflection and T-junctions. It neither excludes M<v nor
validates the reverse-apex/prime candidate.

The proof uses exactly three constructive steps: a known scale-v seed,
new seeds at v+t for 1<=t<u, and an exterior +u collar. The W-to-beta
attachment is a single ordinary scaled tile triangle. No hypothetical tiling
is presumed to contain any removable collar.

For any M>=v let t=(M-v) mod u. Start at v+t and attach (M-v-t)/u collars.
Every intermediate scale T is at least v, so satisfies the collar condition
T>=v-u. For u=1 there are no new residue seeds and the old +1 collar suffices.
This proves the all-integer quantifier once the next sections are checked.

## 2. The three-macro residue seed, in a consistent metric

For 1<=t<u put m=v+t, w=u+t, K=vm-uw=d(u+v+t)>0. The rational coordinates
carry the positive-definite metric

    G(x,y)=v^2(x^2+y^2)+(uP/v)xy,
    det(Gram)=b^2(4v^2-u^2)/(4v^2)>0.

The grid triangles [0,(u,0),(0,v)] and [0,(v,0),(0,u)] have sides (a,b,c).
A rectangle of height uv and width xu+yv, x,y nonnegative integers, is filled
by columns of these two grids, with exactly 2(xu+yv) tiles. Different edge
subdivisions on common interfaces are permitted.

Define

    e=(v^3/b,-uv^2/b), s=(b/v,0),
    s2=(-u,v), e2=(u/v)e.

The triangles [0,s,e], [0,s2,e2] are also congruent to the same tile, since

    |s|=b, |e|=c, |e-s|=a,
    |s2|=b, |e2|=a, |e2-s2|=c.

Set X=0, O=um e, A=(-uvm,u^2m), C=(-uvm,v^2m), and

    Q0=(ub,0), S=Q0+ut s2, P0=Q0+ut e,
    R0=S+dt e2, V=(-u^2w,uvw).

The target OAC has sides m(uQ,v^3,vb). The three outside pieces are:

* OXQ0P0: an um-grid at X in (s,e) with a ut-grid corner removed;
* P0Q0SR0: a vt-grid at Q0 in (s2,e2) with a dt-grid corner removed;
* R0VC: a full K-grid at V in (s2,e2).

Removed corners are whole subgrids, not fractions of tiles. Both outer-minus-
inner scales are positive: uv and ut. The exact joins are

    C=V+K s2, R0=V+K e2, S=V+b e2,
    O-P0=uv(e-s), P0-R0=ut(e2-s2), R0-C=K(e2-s2).

The two last edge directions are positively parallel, so O,P0,R0,C are in
this order on OC. X is on OA. The remaining positioned boundary is H=XACVSQ0.

## 3. Fill H rather than inferring tileability from its area

At height y the left endpoint of H is

    l(y)=-(v/u)y, 0<=y<=u^2m;
         -uvm,   u^2m<=y<=v^2m.

The right endpoint is

    r(y)=ub-(u/v)y,  0<=y<=uvt;
         bw-(v/u)y,  uvt<=y<=uvw;
         -(u/v)y,    uvw<=y<=v^2m.

The breakpoints have the strict order

    0<uvt<u^2m<uvw<v^2m.

For the first nontrivial inequality,
uv-(v-u)t >= uv-(v-u)(u-1) = u^2+v-u >0.
The next two differences are udt>0 and vK>0. These explicit inequalities
remove any reliance on a picture or a numerical aspect-ratio assumption.

### Lower layers

For 0<=j<t, take one v-grid triangle on the left slope and one u-grid triangle
on the right slope. Between them lies a height-uv rectangle of width

    ub+bj-u^2 = u(v+qj)+v qj,
    qj=(d-1)u+dj>=0.

The elementary rectangle rule fills it. These pieces are disjoint by their
horizontal cross-sections.

### Middle layers before the vertical kink

For t<=j<w, a full slant cell has bottom-left (-v^2j,uvj), width bw,
height uv and displacement (-v^2,uv). Its two ends are v-grid triangles;
the middle rectangle has width

    bw-v^2=u(v+q*)+v q*, q*=(d-1)u+d(t-1)>=0.

It is therefore filled with whole tiles.

### The one clipped layer

Let J=floor(um/v) and r=v(J+1)-um. Then 1<=r<=v and t<=J<w.
Indeed um/v=u+ut/v>=u>t and um/v<u+t=w.
The vertical line x=-uvm cuts only the left v-grid triangle in layer J:
its x-coordinate is between -v^2(J+1) and -v^2J. Remove the r-grid corner
based at F=(-v^2(J+1),uv(J+1)). The other two removed-corner vertices are

    F+(vr,0)=(-uvm,uv(J+1)),
    F+(vr,-ur)=(-uvm,u^2m)=A.

Thus exactly the portion outside the target side is removed, as a union of
r^2 WHOLE tiles. When r=v that entire left triangle is omitted. No cut tile
is retained. This possibility is relevant in nonprimitive controls.

### Above the kink

For J<j<w, the left triangle is wholly external and the rectangle begins at
x=-uvm. Its width is

    bw+uvm-v^2(j+1)=uK+v^2(w-1-j).

The coefficients in K*u+[v(w-1-j)]*v are nonnegative and K>0. Hence the
rectangle is tileable and the right triangle lies to the right of the
external vertical side. This identity is the actual reason no restriction
on v/u remains; it is not an appeal to a semigroup test succeeding often.

The upper remainder has vertices

    (-uvm,uvw), (-uvm,v^2m), (-u^2w,uvw).

Its legs have coordinate lengths vK,uK, so it is a K-grid triangle.
This completes H. Positioned cancellation of the positively oriented piece
boundaries proves a partition by the lemma in FOUNDATION_LEMMAS.md; the new
finite regression also checks containment and all macro intersections by
independent rational polygon clipping.

The area count is a consistency identity, not the existence argument:

    u^2(m^2-t^2)+t^2(v^2-d^2)+K^2
      + b[t^2+2t(u+v)+u^2+v^2]=Qm^2.

## 4. Prior seed: explicit geometry remains an input, not an unexplained citation

This construction is attributed in the earlier project to Michael Beeson.
In metric x^2+D y^2, D=4v^2-u^2, set

    O=0, A0=(b^2,0), C0=(-u^2b/2,ub/2),
    D0=(-u^2b/2,-ub/2), E0=(-u^2Q/2,-u^3/2), B0=D0+E0.

Triangle A0C0B0 splits into O A0 C0, O A0 D0, O C0 E0 and parallelogram
O D0 B0 E0. The triangles have integral scales b,b,a. The parallelogram has
b by u^2 cells with step vectors D0/b,E0/u^2; their lengths are a,c and their
difference has length b. The count is 2b^2+a^2+2bu^2=v^2Q.

For partition positivity, D0 lies at parameter b/c on A0B0 and E0 at c/Q on
C0B0; O has positive barycentric coefficients (u^2/c,b/Q,b^2/(cQ)) with
respect to A0,C0,B0. All are strict interior/side conditions. The target sides
are (v^4,uvQ,v^2b), exactly W at scale v. No scale-one nonexistence result is
used. The new checker recomputes its pieces, containment, cell metrics and
pairwise intersections for 49 parameter pairs.

## 5. Prior collar: why it extends ANY existing inner tiling

The full source is `research/w-beta-caps/PROOF.md`, Sections 2-4, pinned to
commit 3a0ad269f645850ed9fd01bbd76a08c9b456032e. It defines a positive six-block
trapezoid with short base L0=u(v-u)b, long base L0+u^2Q and slant legs ab,ac.
It contains u^4+2uvb tiles. Its two rectangular grid vectors satisfy the
required sum-diagonal metrics. The new code independently reconstructs all
six pieces from the source coordinates, rather than trusting their areas.

For T>=v-u, add a parallelogram of slant length ab and horizontal width

    L=uQT-L0 = a(vT)+b*u(T-v+u).

Both coefficients are nonnegative, so two cell types fill it with 2L tiles.
The assembled trapezoid has vertices

    0, (uQ(T+u),0), B+(uQT,0), B,
    B=(u^2b/2,ub/2).

Its legs meet at G=(ub(T+u)/2,b(T+u)/2). The upper base endpoints are the
homothetic images of the lower endpoints about G with ratio T/(T+u).
Thus it is EXACTLY the exterior difference of the two W triangles, not a
claim about the structure of the existing smaller tiling. The added count is

    u^4+2uvb+2L=Q((T+u)^2-T^2).

The new code checks all six cap pieces and the external attachment at
T=v-u, v, v+u for 49 parameter pairs (147 collars). These tests supplement
the displayed construction; they do not prove collar necessity.

## 6. Beta lift and normalization

In the residue coordinates, put B*=O+(P/Q)(A-O). A lies between O and B*.
The triangle A B* C is across AC from OAC and has sides vm(a,b,c). Filling
it with (vm)^2 tiles gives beta and the count (Q+v^2)m^2=Pm^2. This can be
performed after constructing any W scale.

If u=g u0,v=g v0, dividing lengths by g^2 changes M to gM in the primitive
model, so sufficient is gM>=v0, equivalently M>=ceil(v/g^2). This is only
normalization, not a new family of tile shapes. The main statement needs no
nonprimitive case to establish the claimed primitive range.

## 7. Audit verdict and limits

The piece geometry, parameter inequalities, residue-class step and direction
of the W-to-beta transfer have been reconstructed without finding a broken
implication. The written statement remains a sufficient construction theorem.
There is no deduction that M>=v is necessary, no extraction theorem for
arbitrary beta tilings, and no conclusion about F3/14430. This audit uses no
reverse-apex candidate. Its symbolic checks are exact identities; its 413
macro/collar parameter tests are finite regression controls, not formal
verification of an infinite theorem.

# A nonadjacent all-scale construction for W and beta

**Erdős problem 634 — Denis Paliy, research with ChatGPT assistance**  
**9 October 2026**

## Status and scope

This note gives a positive construction theorem, including an entire parameter cone and an additional exact sufficient arithmetic test. It does **not** give a necessary scale bound, classify all tile counts, or resolve the prime-case manuscript. In particular no assertion that every W or beta tiling has the present macrostructure is made. Reflections and T-junctions are allowed.

The new part is the explicit completion of **every seed residue** for nonadjacent parameters, using a correctly scaled four-macro partition and a clipped horizontal strip. The scale-v triquadratic seed attributed to Michael Beeson, and the existing +u external cap, are prior inputs, not new results of this note. Precise dependencies appear in Section 10. No priority or external referee acceptance is claimed. The written proof is accompanied by exact symbolic identities and a separately implemented geometric checker; this is not a proof-assistant formalization.

## 1. Statements

Let integers 0<u<v be coprime, and set

\[
a=uv,\quad b=v^2-u^2,\quad c=v^2,\quad
Q=2v^2-u^2,\quad P=3v^2-u^2,\quad d=v-u.
\]

The tile has side lengths (a,b,c) and angles satisfying 3 alpha + 2 beta = pi. The two target families and counts are

| Family | Target side lengths at scale M | Number of original congruent tiles |
|---|---|---|
| W | M(v^3,uQ,vb) | QM^2 |
| beta-isosceles | M(v^3,v^3,uP) | PM^2 |

Put

\[
\Delta=u^2+uv-v^2,\qquad
\Omega=uv+d(\Delta+u+v)
       =d\Delta+b+uv.
\]

### Theorem A — all scales from a single semigroup test

If u>=2 and

\[
\boxed{\Omega>0,\qquad \Omega\in\langle u,v\rangle,}
\tag{1}
\]

then **both fixed target families are tiled by the stated tile at every integer M>=v**. Here <u,v> denotes nonnegative integer combinations of u and v. For u=1, the same all-M conclusion already follows from the prior scale-v seed and +1 cap.

Condition (1) is sufficient, not necessary. Its failure gives no nonexistence conclusion about any target or count.

### Corollary B — a universal golden-ratio cone

For all coprime 0<u<v satisfying

\[
\boxed{v^2<u^2+uv,}
\tag{2}
\]

both families exist at **every integer M>=v**. Equivalently,

\[
1<\frac vu<\frac{1+\sqrt5}{2}.
\]

A slightly stronger directly checkable sufficient inequality is

\[
v^2\le u^2+uv+u+v.
\tag{3}
\]

**Arithmetic proof of the corollary from Theorem A.** Under (3), Omega>=uv. Choose the unique x in {0,...,v-1} with xu=Omega modulo v. Then y=(Omega-xu)/v is a nonnegative integer, since Omega-xu>=uv-u(v-1)=u>0. Thus Omega=xu+yv. Condition (2) implies (3). No inference from sampled parameter pairs is used.

### Consecutive Fibonacci parameters

If u=F_k, v=F_{k+1}, k>=3, then Delta=(-1)^(k+1). This follows inductively because replacing (u,v) by (v,u+v) negates Delta. Hence Delta+u+v>0, so (3) holds. Therefore both W and beta exist for all M>=v for **every consecutive Fibonacci parameter pair**. This includes pairs approaching the golden ratio from either side, not just from below.

## 2. Reduce the all-scale assertion to finitely many symbolic seed types

The prior cap theorem [C] extends an arbitrary W tiling at scale T to scale T+u whenever T>=v-u. The cap is wholly outside the smaller target. The prior triquadratic construction [C, Section 6] gives scale v.

It therefore suffices to construct

\[
m=v+t,\qquad 1\le t\le u-1.
\tag{4}
\]

Together with the old t=0 seed these are u consecutive scales, one in each residue class modulo u. For any M>=v, choose t=(M-v) mod u, m=v+t and k=(M-m)/u. Start with the corresponding seed and attach k caps. Every attachment satisfies T>=v>v-u.

The following is a single construction for the entire range (4). Its parameters are not a finite experimental list.

## 3. Exact metric and two ordinary grids

Use rational oblique coordinates with squared physical norm

\[
G(x,y)=v^2(x^2+y^2)+\frac{uP}{v}xy.
\tag{5}
\]

Its Gram determinant is

\[
\frac{b^2(4v^2-u^2)}{4v^2}>0,
\]

so this is a Euclidean coordinate system. The triangles

\[
A_0=\operatorname{conv}\{(0,0),(u,0),(0,v)\},\quad
B_0=\operatorname{conv}\{(0,0),(v,0),(0,u)\}
\]

are congruent physical (a,b,c) triangles. Their half-turns give ordinary rectangular grids. The ordinary coordinate area of one tile is uv/2.

A rectangle of coordinate height uv and width xu+yv, with x,y nonnegative integers, can be filled by x columns of width u and y columns of width v. A width-u column has u rows of A_0 cells; a width-v column has v rows of B_0 cells. Each rectangular cell splits into two original tiles. These are actual grid fillings, not only area equalities.

Also put

\[
s=(b/v,0),\quad e=(v^3/b,-uv^2/b),\quad
s_2=(-u,v),\quad e_2=(u/v)e.
\]

The lengths of s,e,e-s are b,c,a, and those of s_2,e_2,e_2-s_2 are b,a,c. Both grid determinants det(s,e) and det(s_2,e_2) equal -uv. Thus these are two more descriptions of ordinary grids of the same tile.

For vectors f,g of any original tile, define the grid annulus A(X;f,g;K,k) as

\[
\operatorname{conv}\{X,X+Kf,X+Kg\}
\setminus\operatorname{int}\operatorname{conv}
\{X+(K-k)f,X+Kf,X+(K-k)f+kg\},
\]

where 0<=k<K are integers. It contains K^2-k^2 whole tiles of the standard K-grid. It is the convex trapezoid with vertices

\[
X,\ X+(K-k)f,\ X+(K-k)f+kg,\ X+Kg.
\]

For k=0 it is the full triangle. No negative-weight region is used.

## 4. Corrected four-macro partition for arbitrary v-u

For m=v+t as in (4), define

\[
\begin{aligned}
X&=(0,0),&O&=um e,\\
A&=(-uvm,u^2m),&C&=(-uvm,v^2m),\\
V&=(-u^2m,uvm),&Q_0&=(ub,0),\\
S&=(ub-u^2t,uvt),&P_0&=Q_0+ut e,\\
R_0&=S+dt e_2,&R&=(-u^2v+b(t-d),uv^2),\\
U&=(-u^2v+bt,uv^2),&T_0&=V+dm e_2.
\end{aligned}
\]

The outer triangle is OAC. Substitution into (5) gives side lengths m(uQ,v^3,vb), exactly W.

Use four ordinary regions:

| Region | Grid description | Tile count |
|---|---|---:|
| O,X,Q_0,P_0 | A(X;s,e;um,ut) | u^2(m^2-t^2) |
| P_0,Q_0,S,R_0 | A(Q_0;s_2,e_2;vt,dt) | t^2(v^2-d^2) |
| R_0,R,U,T_0 | A(R;s,e;b-dt,d(u-t)) | (b-dt)^2-d^2(u-t)^2 |
| T_0,V,C | Full d m-grid on V,s_2,e_2 | d^2m^2 |

Every outer/inner scale is a nonnegative integer with strictly positive difference: uv,ut,dv and dm respectively. The exact joins are

\[
R_0=R+(b-dt)e,\qquad U-R=(bd,0),\qquad
T_0=U+d(u-t)e=V+dm e_2.
\tag{6}
\]

The factors d are essential. Merely substituting arbitrary u,v into the d=1 formulas would produce mismatched seams.

The remaining polygonal region has boundary

\[
H=[X,A,C,V,U,R,S,Q_0].
\tag{7}
\]

The oriented boundaries of the four regions and H sum exactly to the oriented boundary of OAC. Indeed O,X,A are collinear; O,P_0,R_0,T_0,C are collinear; S,R_0,R and U,T_0,V are collinear; every other interface cancels literally. These are positioned boundary identities, not identities discarding edge locations.

Section 5 proves that H is a positive region and gives an ordinary positive grid filling. The four grid annuli are already positive. Therefore the boundary equality establishes that these pieces constitute a genuine partition. An elementary justification is to take their sum of indicator functions minus the target indicator. It has no jumps across any open edge segment and is zero outside a bounded set, so it is zero everywhere off the edges. Positive multiplicities then give coverage exactly once; the closed boundaries follow by taking closure. This argument does not assume nonoverlap beforehand.

## 5. A clipped strip fills the whole remainder

Write y_j=uvj. The left boundary of H is

\[
\ell(y)=\begin{cases}
-(v/u)y,&0\le y\le u^2m,\\
-uvm,&u^2m\le y\le v^2m.
\end{cases}
\]

The right boundary is

\[
r(y)=\begin{cases}
ub-(u/v)y,&0\le y\le uvt,\\
b(u+t)-(v/u)y,&uvt\le y\le uv^2,\\
bm-(v/u)y,&uv^2\le y\le uvm,\\
-(u/v)y,&uvm\le y\le v^2m.
\end{cases}
\tag{8}
\]

At the y=uv^2 interface, the right boundary steps outward by bd. The inequalities t<u<v imply

\[
uvt<u^2m<uvm,
\]

so the change in the left boundary occurs after all the lower expanding layers and before the top triangle.

### 5.1. Lower expanding layers

For j=0,...,t-1 the layer has bottom endpoints

\[
L_j=(-v^2j,uvj),\qquad Q_j=(ub-u^2j,uvj).
\]

Fill its left slant by a v-fold B_0 triangle and its right slant by a u-fold A_0 triangle. The intervening rectangle has height uv and width

\[
W_j^{\rm low}=ub+bj-u^2.
\]

Put K_j=(d-1)u+dj>=0. Then

\[
W_j^{\rm low}=u(v+K_j)+vK_j.
\tag{9}
\]

Thus the rectangle is explicitly tiled by the grid columns from Section 3.

### 5.2. Full slant cells

A parallelogram with bottom-left (x,y), width K, height uv and displacement (-v^2,uv) from bottom to top is partitioned into two v-fold B_0 triangles and a rectangle of width K-v^2 and height uv.

The left triangle has vertices

\[
F=(x-v^2,y+uv),\quad F+(v^2,0),\quad F+(v^2,-uv),
\]

and the right triangle has vertices

\[
(x+K-v^2,y),\quad(x+K,y),\quad(x+K-v^2,y+uv).
\]

The rectangle lies between them. Their interiors are visibly disjoint.

For j=t,...,m-1 take x=-v^2j, y=uvj and

\[
K=K_j^*=\begin{cases}b(u+t),&j<v,\\bm,&j\ge v.\end{cases}
\]

The corresponding full rectangle widths have nonnegative representations:

\[
\begin{aligned}
b(u+t)-v^2&=u(v+K_1)+vK_1,
&K_1&=(d-1)u+d(t-1),\\
bm-v^2&=u(v+K_2)+vK_2,
&K_2&=dm-v.
\end{aligned}
\tag{10}
\]

Both K_1 and K_2 are nonnegative. Hence all full cells below the kink are filled.

### 5.3. The kink is not required to coincide with a strip boundary

This is the new completion step that removes adjacency and the earlier overly restrictive cutoff.

Let

\[
J=\left\lfloor\frac{um}{v}\right\rfloor,\qquad
r=v(J+1)-um,\qquad 1\le r\le v.
\tag{11}
\]

Then t<=J<m. In layer J, use the full slant cell but remove from its left v-grid triangle the r-grid corner with vertices

\[
F,\qquad F+(vr,0),\qquad F+(vr,-ur),
\quad F=(-v^2(J+1),uv(J+1)).
\tag{12}
\]

The last two vertices are exactly

\[
(-uvm,uv(J+1)),\qquad(-uvm,u^2m)=A.
\]

Thus the removed part is precisely the portion outside the vertical target side. It consists of r^2 whole B_0 tiles, not arbitrary fragments. Since r<=v, this is a legitimate subtriangle of the left v-grid; when r=v that left grid is omitted entirely. Nothing inside H is removed. Layers below J use full cells; above J the entire old left B_0 triangle is outside H and the rectangle starts at x=-uvm instead.

### 5.4. Every clipped rectangle has a nonnegative width representation

For j>J, retain the right v-grid triangle and use a rectangle with left side x=-uvm. Its width is

\[
W_j=K_j^*+uvm-v^2(j+1).
\]

Choose a nonnegative representation Omega=A_1 u+B_1 v from (1).

For j<v,

\[
\begin{aligned}
W_j
 &=\Omega+(t-1)(b+uv)+v^2(v-1-j)\\
 &=u\,[A_1+(t-1)(d+v)]
   +v\,[B_1+(t-1)d+v(v-1-j)].
\end{aligned}
\tag{13}
\]

Every coefficient is nonnegative. For j>=v,

\[
W_j=u(dm)+v\,[v(m-1-j)].
\tag{14}
\]

Again both coefficients are nonnegative. These formulas also prove positivity of the horizontal cross-sections in (8). In particular the smallest middle width equals Omega+(t-1)(b+uv)>0.

Above y=uvm, fill the remaining triangle

\[
\operatorname{conv}\{(-uvm,uvm),(-uvm,v^2m),(-u^2m,uvm)\}
\]

with an ordinary A_0 grid of scale dm. This finishes every part of H.

This construction works whether the kink lies in the middle strip or the upper strip. No guessed alignment with y=uv^2 is needed, and no finite sample stands in for that case distinction.

## 6. Exact count and beta extension

The normalized area of H, in unit-tile units, is

\[
b(2uv+4vt+t^2).
\]

Together with the four macro counts in Section 4, this gives the identity

\[
u^2(m^2-t^2)+t^2(v^2-d^2)
 +(b-dt)^2-d^2(u-t)^2+d^2m^2
 +b(2uv+4vt+t^2)=Qm^2.
\]

The area is a count check, not the argument for geometric coverage: that was proved by the positive strips and positioned-boundary equality.

To obtain beta, put

\[
B_*=O+\frac{P}{Q}(A-O).
\]

A lies strictly between O and B_*. The triangle AB_*C is an ordinary tile triangle of integer scale vm: its side lengths are vm(a,b,c). It lies across AC from the W triangle. Adding its (vm)^2 tiles gives the beta triangle OB_*C, with sides m(uP,v^3,v^3) and count (Q+v^2)m^2=Pm^2. This is a positive geometric attachment.

Section 2 now supplies every M>=v, completing Theorem A.

## 7. Nonprimitive parameters

There is no separate unknown family created by gcd(u,v)>1. If u=g u_0,v=g v_0, then the tile sides have common factor g^2. Dividing all lengths by g^2 converts the displayed target scale M to primitive scale gM:

\[
(2v^2-u^2)M^2=(2v_0^2-u_0^2)(gM)^2,
\]

and likewise for beta. The ratio condition is unchanged. Thus Corollary B extends to arbitrary positive integers u<v at M>=v, by the primitive theorem (indeed normalization often gives stronger scales). The formulas and code also permit nonprimitive integer inputs directly. Their successful checks do not represent new tile shapes.

## 8. Concrete exact constructions

### The first useful example beyond 11/7

For (u,v)=(5,8),

\[
(a,b,c)=(40,39,64),\quad Q=103,\quad P=167,\quad
\Delta=1,\quad \Omega=82=10\cdot5+4\cdot8.
\]

The theorem supplies both fixed target families for all M>=8. At m=9, t=1, it gives

\[
\begin{array}{lll}
W:&(4608,4635,2808),&N=8343,\\
\beta:&(4608,4608,7515),&N=13527.
\end{array}
\]

Their complete unit coordinates are included. The W outer macros contain 3936 tiles and H contains 4407. The kink is in layer J=5 and the removed B-corner has scale r=3.

### A pair outside the golden-ratio cone, admitted by the stronger test

For (u,v)=(6,11),

\[
\Delta=-19,\quad \Omega=56=2\cdot6+4\cdot11.
\]

Thus both families exist for all M>=11, even though 11/6 exceeds the golden ratio. The included W seed at M=13 has tile (66,85,121), target (17303,16068,12155), and N=34814.

Individual global counts may already have other constructions; no priority or first-ever realizability claim is inferred from a new fixed-tile certificate.

## 9. Verification performed and the remaining gap

`construct.py` is a solver-free exact rational constructor. It implements the new residue seeds, the prior triquadratic seed, the prior +u cap, and the beta lift. Thus it can export arbitrary supported M>=v, not merely the three retained examples.

`verify.py` imports no construction code. It checks integer-metric congruence, target sides, orientation, containment, exact area, and cancellation of every positioned boundary current. With nonnegative tile multiplicities this certifies coverage without overlap. Its optional second check visits every unordered tile pair and uses exact integer separating-axis tests, guarded against int64 determinant overflow.

The retained examples have these additional full pair checks:

| Count | Exact pairs checked |
|---:|---:|
| 8343 | 34,798,653 |
| 13527 | 91,483,101 |
| 34814 | 605,989,891 |

The wider 21-case regression checked 358,827 tiles across the examples and 5,770,147,225 unordered pairs. It includes all missing seed residues for (5,8) and (6,11), caps and repeated caps, the beta lift, and nonprimitive and kink-at-layer-end cases. It includes old constructions as controls, not new results.

`check_symbolic.py` verifies 39 symbolic identities, including the whole positioned boundary, the metric, macro joins, clipping endpoints, and each rectangle representation. Its separate bounded arithmetic regression used u<=100, v<=2u+2: 3257 accepted parameter pairs, 213005 seed parameter cases, and 1459167 critical rectangle checks. The finite regression is not the proof of the infinite quantifier; Sections 2–6 provide that proof. Deliberately duplicated, deformed and orientation-reversed tile certificates are rejected by the verifier.

The new positive theorem does not:

* prove that M>=v is necessary, or exclude any M<v;
* determine arbitrary W/beta scales when (1) fails;
* solve F3, including the separate candidate 14430;
* rely on or validate the disputed reverse-apex induction or all-primes conclusion.

The golden ratio is a uniform sufficient boundary for this method, not a boundary between possible and impossible tilings. If v/u tends to a fixed r>(1+sqrt(5))/2 along parameters of increasing size, then Omega/u^3 tends to (r-1)(1+r-r^2)<0. Thus this particular first-seed layout cannot supply a larger fixed cone by merely improving the coin-representation algorithm. This is a limitation of the layout, not a geometric nonexistence theorem.

## 10. Dependencies and comparison to prior material

All repository references below are pinned at the snapshot examined, commit `3a0ad269f645850ed9fd01bbd76a08c9b456032e` of `DenisUkranian/erdos-634-tilings`.

**[C] Prior six-block cap and the credited scale-v seed:**  
`research/w-beta-caps/PROOF.md`, especially Sections 3–6.  
https://github.com/DenisUkranian/erdos-634-tilings/blob/3a0ad269f645850ed9fd01bbd76a08c9b456032e/research/w-beta-caps/PROOF.md

Its prior guaranteed scale set is v+<u,v>, with sufficient conductor uv-u+1. Its +u cap extends an arbitrary existing target at T>=v-u. Its seed is attributed there to Michael Beeson's triquadratic construction. This note does not use the scale-one nonexistence arguments in that author's other work.

**[A] Prior adjacent all-scale construction:**  
`research/gap-closure-oct8/group1/PROOF.md` and `group1-helper/ADJACENT_ALL_SCALES.md`.  
https://github.com/DenisUkranian/erdos-634-tilings/blob/3a0ad269f645850ed9fd01bbd76a08c9b456032e/research/gap-closure-oct8/group1/PROOF.md

This proves all M>=v for v=u+1 and motivated the grid partition. The new formulas retain d=v-u in the annular scales and allow the outer-side kink in any relevant layer. They are not a direct substitution into the adjacent formulas.

**Scope of comparison.** This is an extension relative to the inspected repository snapshot. A quoted external-model summary mentioning a cone 11/7 was not used as a mathematical premise. No exhaustive literature-priority audit is claimed. The cone here contains and strictly extends that numerical range, regardless of the status of that earlier summary.

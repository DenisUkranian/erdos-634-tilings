# A six-block cap for every primitive W and beta tile

Denis Paliy, research with ChatGPT assistance. 3 October 2026.

This is a project-internal construction and proof, with separate exact
generation and verification. Priority and external referee acceptance have
not been established. It improves a sufficient construction threshold; it
does not solve Erdős problem 634 or assert a necessary scale condition.

## 1. The statement

Let integers `0 < u < v` be coprime, and put

\[
a=uv,\quad b=v^2-u^2,\quad c=v^2,\quad
Q=b+c,\quad P=b+2c,\quad D=4v^2-u^2.
\]

The primitive tile has sides `(a,b,c)`. The W triangle at integer scale
`m` has sides `m(v³,uQ,vb)` and area `Qm²` times the tile area. The
beta-isosceles target has sides `m(v³,v³,uP)` and area `Pm²` times that
area. These are the targets and scale conventions of
`../square-class-saturation/PROOF.md` and
`../../docs/universal-rational-scales.md`.

**Theorem.** For either fixed target family, every scale

\[
\boxed{m\in v+\langle u,v\rangle
       =\{v+iu+jv:i,j\ge0\}}
\]

has a dissection into congruent copies of the primitive tile. In
particular every integer

\[
\boxed{m\ge C(u,v):=uv-u+1}
\]

is realizable. More precisely, any existing W or beta tiling at scale
`T ≥ v−u` can be extended, without changing any of its tiles, to scale
`T+u`.

The numerical semigroup is a proved subset of the actual scale spectrum.
Neither its omitted scales nor its conductor are claimed to be necessary
for arbitrary tilings. Reflections and T-junctions are allowed.

## 2. Two elementary grids

Pairs `(x,y)` throughout represent physical coordinates `(x,y√D)`.
Thus the squared norm is `x²+Dy²`, and the sign of a determinant is
the usual orientation. Set

\[
p=(uv,0),\quad w=\left(-\frac{uP}{2v},\frac b{2v}\right),\quad
r=\left(\frac{uQ}{2v},\frac{u^2}{2v}\right),\quad
s=\left(-\frac{ub}{2v},\frac b{2v}\right).
\]

Direct algebra gives

\[
|p|=|r|=a,\quad |s|=|p+w|=b,\quad |w|=|r+s|=c,
\quad p+w=s,
\]

\[
\det(r,s)=\det(p,w)=\frac{ub}{2}>0.
\]

Consequently the parallelograms on `(r,s)` and on `(p,w)` each split
along their sum diagonal into two copies of the tile. An integral
`d×e` array gives `2de` tiles. Any integral `n`-scaled tile triangle
has the usual triangular-grid dissection into `n²` tiles. These facts
will fill every region below by actual congruent triangles.

## 3. The cap and its disjoint partition

Put

\[
k=uv,\quad h=u(v-u),\quad q=u^2,\quad L_0=hb,
\]

\[
\begin{aligned}
O&=(0,0),&K&=(uv^3,0),&R&=br=K+qw,\\
J&=h(r+s),&C&=K+hp,&E&=R+hs=C+kw,\\
B&=E-(L_0,0).&&&&
\end{aligned}
\]

The proposed cap is the quadrilateral `O,C,E,B`. Its useful boundary
identities are

\[
B=\left(\frac{u^2b}2,\frac{ub}2\right),\quad
C=(L_0+u^2Q,0),\quad E=B+(L_0,0).
\]

It is a strictly convex trapezoid: the two horizontal bases have
positive lengths `L₀+u²Q` and `L₀`, and its height is positive.
Its legs have lengths

\[
|OB|=uvb=ab,\qquad |CE|=uvc=ac.
\]

The points used to dissect it have strictly controlled locations:

\[
0<K_x<C_x,\qquad J=\frac v{v+u}B,
\]

and

\[
R=\frac{(v-u)b}{v^3}K+\frac uvE+
  \frac{u^2(v-u)}{v^3}O. \tag{3.1}
\]

The three coefficients in (3.1) are positive and sum to one. Thus `R`
is strictly inside triangle `O,K,E`, while `J` lies strictly on `O,B`.
Draw `OE` and `KE`, subdivide triangle `OKE` from its interior point `R`, and
subdivide triangle `OBE` from `J`. Merging adjacent subtriangles gives
exactly the following four regions with disjoint interiors:

| Region | Description | Tile count |
|---|---|---:|
| `O,K,R` | Tile triangle at scale `k` | `k²` |
| `J,B,E` | Tile triangle at scale `h` | `h²` |
| `O,R,E,J` | Grid in vectors `r,s` | `2bh−h²` |
| `K,C,E,R` | Grid in vectors `p,w` | `2hq+h²` |

For the first triangle, `K=cp` and `R=K+qw` give side lengths
`ac,ab,a²`, which are `k(c,b,a)`. For the second, `BE=hb`,
`JB=ha`, and `JE=hc`. The last two regions are not being justified
only by their areas: they have the following ordinary convex-grid
partitions. Define `X=hr` and `Y=C+qw`. Then

* `O,R,E,J` is triangle `O,X,J` of scale `h` and the
  `(b−h)×h` parallelogram `X,R,E,J` in `(r,s)`.
* `K,C,E,R` is the `h×q` parallelogram `K,C,Y,R` in `(p,w)`
  and triangle `R,Y,E` of scale `h`.

The corresponding coordinate polygons are respectively
`(0,0),(b,0),(b,h),(h,h)` and
`(0,0),(h,0),(h,k),(0,q)`; all are convex since
`b−h=v(v−u)>0` and `k=q+h`. The diagonals in these grids are
sum diagonals. The displayed subdivisions therefore give six ordinary
macroregions, avoiding any convention about partially retained cells.

The total number of primitive tiles is

\[
\begin{aligned}
N_{\rm cap}
 &=k^2+h^2+(2bh-h^2)+(2hq+h^2)\\
 &=\boxed{u^4+2uvb}. \tag{3.2}
\end{aligned}
\]

## 4. Attach mixed strips to obtain the W collar

Fix an integer `T ≥ v−u`, and let

\[
L=uQT-L_0.
\]

This length is nonnegative because it has the explicit representation

\[
\boxed{L=a(vT)+b\,u(T-v+u).} \tag{4.1}
\]

Both coefficients are nonnegative integers. Let `V=B`, of length
`ab`. Its angle with the positive horizontal has cosine `u/(2v)`.
Consequently a cell with horizontal side `a` and slant side `b`, or
horizontal side `b` and slant side `a`, has sum diagonal `c`, since

\[
a^2+b^2+2ab\frac u{2v}=c^2.
\]

Translate the cap to the right by `(L,0)`, and fill the adjacent
parallelogram with vertices `0,(L,0),(L,0)+V,V`. Use `vT` horizontal
strips of width `a`, with the slant side divided into `a` pieces of
length `b`; then use `u(T−v+u)` strips of width `b`, with the slant
side divided into `b` pieces of length `a`. Empty strip groups are
omitted. Each cell splits into two original tiles, and the added
parallelogram uses `2L` tiles. This construction permits T-junctions
at interfaces and needs no divisibility beyond (4.1).

In fact `T≥v−u` is the exact cutoff for this cap's mixed-strip recipe.
Since `gcd(a,b)=1`, any nonnegative representation `L=ax+by` requires
`x≡vT (mod b)`. If `1≤T<v−u`, then `0<vT<v(v−u)<b`, so the
least nonnegative `x` is `vT`; its corresponding coefficient is
`y=u(T−v+u)<0`. Increasing `x` only decreases `y`. Thus no other
nonnegative strip choice repairs this particular recipe below the
cutoff. This is not an obstruction to other collar tilings.

The resulting trapezoid has vertices

\[
0,\quad (uQ(T+u),0),\quad V+(uQT,0),\quad V. \tag{4.2}
\]

Its two nonparallel lines meet at

\[
G=\left(\frac{ub(T+u)}2,\frac{b(T+u)}2\right).
\]

The outer triangle with apex `G` and the lower base in (4.2) has
sides

\[
(T+u)(vb,v^3,uQ).
\]

The upper endpoints in (4.2) are the homothetic images of the lower
endpoints, with center `G` and ratio `T/(T+u)`. Thus the trapezoid is
exactly the region between `W_T` and `W_{T+u}`, with their angle-`2α`
apex fixed. It lies wholly outside the smaller triangle, regardless
of how that smaller triangle may already have been tiled.

The number of added tiles agrees with the whole collar area:

\[
N_{\rm cap}+2L=Q\big((T+u)^2-T^2\big).
\]

For reproducible canonical coordinates, the orientation-preserving
metric isometry

\[
(x,y)\longmapsto
\left(\frac{-ux+Dy}{2v},\frac{-x-uy}{2v}\right) \tag{4.3}
\]

applied after translation by `−G` sends the two outer vertices to
`(T+u)w₀` and `(T+u)z`, where

\[
z=\left(-\frac{vQ}2,-\frac{uv}2\right),\qquad
w_0=\left(-\frac{bQ}{2v},\frac{ub}{2v}\right).
\]

Hence the canonical W target used by the generator is `(0,mz,mw₀)`.

## 5. The beta lift

Define

\[
z_2=z+\frac P Q(w_0-z).
\]

Since `0<Q/P<1`, the point `w₀` lies strictly between `z` and `z₂`.
Metric calculation gives

\[
|z|=|z_2|=v^3,\quad |z-z_2|=uP,
\]

and the triangle `(0,w₀,z₂)` has sides `v(b,c,a)`. Therefore the
beta triangle `(0,mz,mz₂)` is the disjoint union of `W_m` and an
original-tile triangle at scale `vm`.

Between scales `T` and `T+u`, the first region has the collar just
constructed. The second has an ordinary triangular-grid annulus
between integer scales `k=vT` and `k+h= v(T+u)`. To be explicit,
if `e,f` are vectors for a primitive tile based at zero, this annulus
partitions into

\[
(ke,(k+h)e,ke+hf)
\]

and the parallelogram

\[
(ke,kf,(k+h)f,ke+hf).
\]

The first is a scale-`h` tile; the second is a `k×h` grid whose
difference diagonal is the third tile side. Both are outside the
inner tile triangle. Adding them gives the beta collar, with count

\[
P\big((T+u)^2-T^2\big).
\]

As in the W case, this argument extends an arbitrary existing beta
tiling. It makes no assumption about a decomposition inside it.

## 6. Seeds and the universal scale quantifier

The credited triquadratic construction gives W at scale `v`; here
are the coordinates, also reproduced in the preceding saturation
package, so that this note's positive conclusion is self-contained:

\[
\begin{aligned}
O&=(0,0),& A&=(b^2,0),& C_0&=(-u^2b/2,ub/2),\\
D_0&=(-u^2b/2,-ub/2),&E_0&=(-u^2Q/2,-u^3/2),&B_0&=D_0+E_0.
\end{aligned}
\]

Triangle `A,C₀,B₀` has sides `(v⁴,uvQ,v²b)`. It partitions into
triangles `O,A,C₀`, `O,A,D₀`, `O,C₀,E₀` and parallelogram
`O,D₀,B₀,E₀`. Indeed

\[
D_0=A+\frac bc(B_0-A),\qquad
E_0=C_0+\frac cQ(B_0-C_0),
\]

and `O` has strictly positive barycentric coefficients
`(u²/c,b/Q,b²/(cQ))` with respect to `(A,C₀,B₀)`.
The triangular scales are `b,b,a`; the parallelogram has `b×u²`
cells with step vectors `D₀/b,E₀/u²`, of lengths `a,c` and
difference length `b`. Their count is

\[
2b^2+a^2+2bu^2=v^2Q.
\]

Integer coordinate multiplication, with the corresponding finer
grids, supplies every seed scale `rv`, `r≥1`. Section 5 supplies the
beta seed at each such scale by adding a tile triangle of scale
`rv²`. These are existing seeds; this note claims the cap construction
and its consequences, not the discovery of the triquadratic seed.

Now let `m=v+iu+jv`, with `i,j≥0`. Start with the seed at
`(j+1)v`, then add `i` collars of increment `u`. Every starting
scale is at least `v>v−u`, so all collar hypotheses hold.

For an explicit plan using fewer than `v` collars, choose the unique
`0≤i<v` with `iu≡m (mod v)`, and set `s=m−iu`. A positive `m`
belongs to `v+⟨u,v⟩` if and only if `s≥v`; then `s/v` is its seed
factor. For every `m≥uv−u+1`,

\[
s\ge m-u(v-1)\ge1.
\]

Since `s` is divisible by `v`, it is at least `v`. This proves the
universal tail without extrapolating from finitely many examples.
Equivalently, the numerical semigroup conductor gives
`v+(u−1)(v−1)=uv−u+1`. For `u>1`, its preceding integer is absent
from this particular semigroup; that says nothing about other tilings.

## 7. Square-class consequences and the remaining gap

The explicit threshold satisfies

\[
Q-C=(v-u)(2v+u)+u-1>0,
\]

\[
P-2C=(v-u)(3v+u)+2u-2>0.
\]

Combining this with the reduced norm-representation lemma already
proved in `../square-class-saturation/PROOF.md`, Section 5, gives:

* If a squarefree `d>2` has all its odd prime factors `1` or `7`
  modulo `8`, choose a reduced primitive solution `Q=d`. A single
  fixed W tile realizes every `dm²` for `m≥C<d`, hence for `m≥d`.
* If squarefree `d∉{2,3}` has a reduced primitive solution `P=d`
  (equivalently the signed norm conditions in that cited lemma), a
  single fixed beta tile realizes every `dm²` for `m≥C<d/2`, hence
  for `m≥⌈d/2⌉`.

The norm-solvability lemma, the angular classification, and the
previous necessary count forms are not reproved or newly claimed here.
The main cap theorem needs none of the negative classification results.

For example, `(u,v)=(2,3)` gives tile `(6,5,9)` and constructs scales
`3,5,6,7,…` in both W and beta. The missing scale `4` is not ruled out
by this theorem. For `(u,v)=(1,v)`, every scale `m≥v` is constructed;
the special `v=2` spectrum was already known through Bonfioli's
construction. These conclusions do not classify all scales or all
possible tiles, and do not finish Erdős problem 634.

## 8. Verification and provenance

`generate.py` returns complete compressed certificates, using only
triangle grids and parallelogram grids. `verify.py` imports neither
the generator nor the symbolic checker. It independently checks every
unit-cell metric, integer grid dimensions, exact area and count,
containment, and every pair of macroregions by rational convex
clipping. Shell certificates additionally include the inner target,
which is checked as a disjoint complementary region. The contained
finite closed union has full target area; consequently it covers the
target, including its boundary.

`verify.py --expand` separately constructs every individual tile and
checks exact congruence, containment, and pairwise disjointness for
the small regression certificates. This is finite unit verification,
not the universal proof. `check_symbolic.py` verifies the identities
as exact Laurent polynomials over the rationals, using `laurent.py`;
no numerical parameter substitution and no external algebra package
are used. Positivity, partition topology, and quantifiers are proved
in the text above.

`run_checks.py` writes a reproducible report with its precise finite
scope, example certificates, and rejected corruptions. Its results
must not be read as proving that omitted scales are impossible.

The seed attribution is to Michael Beeson, *Triangle Tiling: The case
3α+2β=π*, Theorem 11, as used in the existing project's saturation
proof. The beta geometric transfer and integral triangular annuli are
also existing project ingredients. The cap emerged from extending
the small `(u,v)=(1,2),(1,3)` examples to the formula proved here;
this observation is motivation, not a finite-extrapolation argument.

# The uniform charged fan family cannot fit the target board

21 November 2026. **This is a restriction on one explicit family. It does
not exclude 3431, 5063, or all integer cylinder packings.**

The neighboring
[uniform charged cylinder construction](../integer3431/UNIFORM_CHARGED_CYLINDER_CONTROL.md)
places `c` copies of a three-triangle fan on one carrier line. With suitable
integer anchor spacings it gives a nonoverlapping plane packing of `3c`
triangles, signed charge `c`, and zero short cylinder endpoint current.
Its gate profile fails the required target congruences. The theorem below
adds a separate exact obstruction: this same-carrier family at height one
cannot be contained in the prescribed board, even after translating it
freely or rotating it by a multiple of 60 degrees.

## 1. Fan and carrier section

Let `a>b>0` be coprime integers with `a^2+ab+b^2=c^2`. Use the unit
triangular-lattice directions `U_j=rho^j`, where `rho=exp(i*pi/3)`.
At normalized anchor `q=(0,t)`, the fan consists of the three labels

```
(j,s) = (0,-1), (0,+1), (4,+1),
```

with triangle vertices `q`, `q-a U_j`, `q+b U_(j+s)`. The three triangles
have disjoint interiors. They occupy the three successive 120-degree
sectors about `q`.

On the carrier line `x=0`, their union has the interval

\[
\left[t-\frac{ab}{a+b},\ t+a\right],
\qquad
F:=a+\frac{ab}{a+b}
  =\frac{a(a+2b)}{a+b}.                              \tag{1}
\]

The lower endpoint comes from the side joining `(-a,t)` to `(b,t-b)`
of the `(0,-1)` triangle. The upper endpoint is `(0,t+a)` of the
`(4,+1)` triangle.

If two anchors are separated by `delta>0` and `delta<F`, the upper
fan's `(0,-1)` triangle overlaps the lower fan's `(4,+1)` triangle.
Indeed, at `x=0` the former has section
`[delta-ab/(a+b),delta]`, while the latter has section `[0,a]`.
Their interiors in the longitudinal coordinate overlap. The former
crosses the carrier, and the latter has interior immediately to its
right, so the intersection persists for sufficiently small `x>0`.
Thus nonoverlap requires `delta>=F`.

When the anchors have integer longitudinal coordinates, consecutive anchors
must therefore differ by at least `ceil(F)`. Any `c` such fans occupy a
segment on the common carrier of length at least

\[
L_{\rm fan}\ge(c-1)\lceil F\rceil+F.                   \tag{2}
\]

This is a necessary condition for disjointness, not an assumption that
bounding rectangles must be disjoint. In particular, using the smaller
spacing `c+1` would cause an actual triangle overlap at both targets.

## 2. Exact maximal chords of the board

The standard board has vertices

\[
(0,0),\quad(A,0),\quad(0,B),
\qquad A=b(2a+b),\quad B=a(a+2b).
\]

At height one put `z=(a+b*rho)/c`. Its three unoriented short-axis unit
directions have axial coordinates

\[
z=(a,b)/c,\quad z\rho=(-b,a+b)/c,
\quad z\rho^2=(-a-b,a)/c.
\]

The longest board chords parallel to these directions have lengths

\[
\begin{aligned}
L_0&=\frac{ABc}{Ba+Ab}=\frac{AB}{c(a+b)},\\
L_1&=\min\left\{\frac{Ac}{b},\frac{Bc}{a+b}\right\}
     =\frac{Bc}{a+b}=cF,\\
L_2&=\min\left\{\frac{Ac}{a+b},\frac{Bc}{a}\right\}
     =\frac{Ac}{a+b}.
\end{aligned}                                         \tag{3}
\]

For a direction with both coordinates positive, the longest segment starts
at `(0,0)` and ends on `BX+AY=AB`, giving the first formula. For a direction
with negative first coordinate and positive second coordinate, a segment
of length `ell` must have first-coordinate span `ell*|u|/c<=A` and
second-coordinate span `ell*v/c<=B`. Both conditions are sufficient: the
segment from `(ell*|u|/c,0)` to `(0,ell*v/c)` lies in the convex board.
This gives the two minimum formulas.

The simplified choices of the minima follow from `a>b>0`. Also

\[
\frac{L_0}{L_1}=\frac{A}{c^2}<1,
\qquad
\frac{L_2}{L_1}=\frac AB<1,
\]

because `c^2-A=a(a-b)>0` and `B-A=(a-b)(a+b)>0`.
Consequently `cF` is the largest available chord among all three
height-one short axes. Rotating the fan family by 60 degrees merely
permutes these axes.

## 3. Containment theorem

**Theorem.** A family of `c` nonoverlapping fans of the stated form, with
integer anchor coordinates on one common carrier, cannot fit in the
standard board at height one, after any common translation and any
rotation by a multiple of 60 degrees.

**Proof.** Since `gcd(a,b)=1`, also `gcd(a+b,b^2)=1`. The expression

\[
F=(a+b)-\frac{b^2}{a+b}
\]

is not an integer. Therefore (2) and (3) give

\[
L_{\rm fan}-\max(L_0,L_1,L_2)
\ \ge\ (c-1)(\lceil F\rceil-F)>0.                    \tag{4}
\]

If all triangles lay in the board, the extreme points of their carrier
sections would also lie in the board. By convexity the entire segment
between those extreme points would be a board chord. Equation (4) rules
this out. Common translation cannot change these lengths. The rotation
claim follows from the three-direction comparison. QED.

## 4. Exact target values and scope

| Target | `F` | Minimum integer spacing | Required carrier span | Maximum height-one chord | Excess |
|---|---:|---:|---:|---:|---:|
| 3431 | `1551/40` | 39 | `57711/40` | `57387/40` | `81/10` |
| 5063 | `2135/48` | 45 | `92855/48` | `91805/48` | `175/8` |

The [integer/rational verifier](verify_uniform_fan_obstruction.py) checks
these identities, the three chord formulas, the side metric, the carrier
intersection, and the actual adjacent-triangle overlap at spacing `c+1`.
Its [replay](UNIFORM_FAN_OBSTRUCTION_REPLAY.json) records the exact fractions.

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/global/verify_uniform_fan_obstruction.py
```

No claim is made that every `3c` charged cylinder kernel decomposes into
these fans, lies on one carrier, has integer anchor differences of this
form, or occurs at height one. The theorem therefore cannot exclude the
minimal 3431 mode, let alone all larger odd populations. It is a concrete
instance in which spatial nonoverlap and the prescribed board remove a
valid integer cylinder construction; the earlier cylinder and gate
distinctions remain essential.

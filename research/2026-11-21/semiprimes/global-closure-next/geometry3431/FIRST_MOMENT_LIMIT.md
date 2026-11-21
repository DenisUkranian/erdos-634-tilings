# Containment and first transverse moments do not close the 3431 relaxation

21 November 2026. This is an exact limitation of one proposed strengthening,
not a geometric construction or a nonexistence result. **3431 remains open.**

**Theorem.** The rational periodic witness at odd population 111 for the
3431 board lifts to a nonnegative rational weighted collection of contained
height-one placements satisfying:

* every periodic short-edge endpoint equation modulo `37R`;
* every first transverse moment of those endpoint equations, separately
  for the three short-edge axes;
* exactly the same signed gate currents, total population, sign populations,
  and positive gate capacities as the original witness.

In particular this stronger linear relaxation is still feasible at
`n_odd=111`, `n_+=74`, `n_-=37`, with native currents 22 and 15 and
zero remote currents. Thus a certificate using just these constraints
cannot exclude that profile. Integral placement multiplicities, exact
individual supporting lines, contact with real branch interiors, and
nonoverlap remain absent.

The result does **not** say that full supporting-line endpoint equations
are redundant. It addresses only the zeroth and first moments defined
below. It also makes no assertion about the feasibility of a model that
imposes area transport, common interfaces, or integer face coverage.

## 1. The known exact periodic input

Set

\[
 a=33,\quad b=7,\quad c=37,\quad
 \rho=e^{i\pi/3},\quad z=(a+b\rho)/c.
\]

The existing [rational projection theorem](../../global-invariant/N3431_PROFILE_LIMIT.md)
supplies strictly positive rational weights `x(q,j,s)` for every
`q in (Z/cZ)^2`, `j in {0,...,5}`, and `s in {-1,1}`. There are
`12c^2=16428` classes. It proves, by exact arithmetic and rigorous
inverse bounds, the claimed mass 111, sign masses 74 and 37, and
signed gate currents

\[
 Q_0^+=22,\qquad Q_0^-=15,\qquad
 Q_r^+=Q_r^-=0\quad(r\ne0).
\]

All positive gate masses are strictly less than 44. This input is a
rational solution of a relaxation, not an integer tiling.

The present proof works for *every* rational solution of the periodic
endpoint equations on these 16,428 classes. It need not expand or
approximate the exact rational inverse used by the earlier witness.

## 2. Precisely which positional constraints are added

Divide physical coordinates in the path frame by `z`. Every height-one
anchor is now `q=(x,y) in R`, and the two other tile vertices are

\[
 u=q-aU_j,\qquad w=q+bU_{j+s},\qquad U_j=\rho^j.
\]

For the three unoriented short-edge axes, take transverse coordinates

\[
 \tau_0(x,y)=y,\qquad
 \tau_1(x,y)=x,\qquad
 \tau_2(x,y)=x+y.
\]

Each is constant along its corresponding axis. A periodic endpoint
potential for axis `i` may be strengthened to

\[
 F_i(P\bmod cR)+\tau_i(P)H_i(P\bmod cR).                 \tag{1}
\]

This function is still periodic under translation by `cU_i` along
an individual line. Therefore a whole complementary long edge has
zero endpoint difference. Endpoint telescoping on partial contacts
continues to apply. Such functions retain each periodic endpoint
current and its first transverse moment.

For a counterclockwise tile, the two short sides have endpoint entries

\[
 +s\,[j,q]-s\,[j,u]+s\,[j+s,w]-s\,[j+s,q],              \tag{2}
\]

where axes are reduced modulo three and endpoint coordinates modulo
`cR`. On the `j` side both endpoints have transverse coordinate
`tau_j(q)`; on the `j+s` side both have `tau_(j+s)(q)`.
This fact gives the lifting identity below.

## 3. Four contained translations for each residue class

Use the common mean anchor

\[
 q_*=(1601/2,\;1/2).
\]

For a residue `r=(r_x,r_y)`, with `0<=r_x,r_y<c`, define

\[
 l_i=r_i+c\left\lfloor\frac{(q_*)_i-r_i}{c}\right\rfloor,
 \qquad d_i=2(q_*)_i-2l_i\in\{1,3,\ldots,73\}.
\]

The four integer anchors are

\[
 q_{\epsilon\eta}=(l_x+c\epsilon,l_y+c\eta),
 \qquad\epsilon,\eta\in\{0,1\}.
\]

Give the lower and upper choices of coordinate `i` the respective
probabilities `(2c-d_i)/(2c)` and `d_i/(2c)`, and use their products.
Every weight is a strictly positive rational number with denominator
`4c^2=5476`. Their sum is one, and

\[
 \sum_{\epsilon,\eta}w_{\epsilon\eta}q_{\epsilon\eta}=q_*.
 \tag{3}
\]

All four anchors retain the original residue class. The orientation,
hand, and sign of the tile are unchanged. Both gate residues are
unchanged because their defining expressions are integer linear
functions modulo `c`.

These are actual contained placements. In coordinates normalized by
`1/z` and then multiplied by `c`, the board vertices are

\[
 (0,0),\quad(c^2(a+b),-c^2b),\quad
 (a^2(a+2b),ab(a+2b)).                                  \tag{4}
\]

The independent checker constructs every one of the `65712` placements,
checks the tile determinant, and tests all three vertices against all
three closed half-planes in (4). All inequalities are strict. Their
smallest determinant is the positive integer `131089964`.
No floating containment tolerance is used.

## 4. Exact preservation of the endpoint moments

Replace the weight of a periodic column by its weight times the four
probabilities in Section 3. The ordinary periodic column is unchanged,
since all four translated columns have identical periodic endpoints.

Consider a first-moment row on axis `i`. Each contribution of a fixed
column in (2) is multiplied by the same transverse anchor coordinate
`tau_i(q)`. Averaging over the four lifts and using (3) therefore
multiplies that periodic contribution by `tau_i(q_*)`. This common
factor is independent of the residue, orientation, and hand. Hence

\[
 \text{lifted first-moment current on a row of axis }i
 =\tau_i(q_*)\times\text{original periodic current on that row}.
 \tag{5}
\]

Every original periodic current is zero, so every first-moment current
is zero as well. Gate currents, gate sign masses, and the total mass
are preserved column by column. The exact rational witness consequently
lifts to the stronger contained relaxation at mass 111.

The weights are fractional. Distinct lifted placements can overlap;
nothing in this construction tests or permits treating those overlaps
as a positive tiling. Containment alone does not impose coverage.

## 5. Reproduction and numerical attempts kept separate

Run the dependency-free exact checker:

```sh
python3 verify_first_moment_lift.py
```

It checks all 16,428 column identities, all 65,712 strict containment
claims, all probability sums and first moments, and all gate labels.
The output is [FIRST_MOMENT_LIFT_REPLAY.json](FIRST_MOMENT_LIFT_REPLAY.json).
The previous rational periodic theorem is a stated proof dependency;
the current checker verifies the universal linear lifting map itself.

The optional `line_moment_probe.py` is a numerical discovery tool. It
uses exact integer containment to reduce the 4,207,420 candidate anchors
to 160,177 convex-hull extreme columns: for a fixed residue and
orientation every zeroth/first-moment column is affine in the anchor.
The 8,288-row full first-moment optimization stopped at its 55-second
limit without a mathematical verdict. A weaker 518-row additive-field
probe returned numerical feasibility. These statuses are recorded in
[NUMERICAL_PROBES.json](NUMERICAL_PROBES.json); neither is a premise of
Sections 1–4. The exact lifting theorem resolves this particular
feasibility question without relying on either solver outcome.

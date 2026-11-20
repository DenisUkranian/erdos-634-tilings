# Exact capacity of a phase gate in one Euclidean tile class

21 November 2026. This is a global necessary inequality, with no position
box, finite placement catalogue, restriction on occupied heights, or
assumption that the whole tiling is native. It applies separately to an
individual Euclidean class of tiles. The application below excludes two
upper-median parameter values in a hypothetical `3c` odd population.
It does not exclude the remaining `3c` cases or either target board.

## 1. A single class and a selected gate

Let `R=Z[rho]`, `rho=exp(i*pi/3)`, `z=(a+b*rho)/c`, and
`c^2=a^2+ab+b^2`. Use the placement sign
`epsilon=s*(-1)^j` for a tile with short height `h` and long height
`h+s`.

Fix a Euclidean class

\[
 L=q_0+z^hR
\]

and let `n_+,n_-` be the actual numbers of positive and negative tiles
whose short height is `h` and whose vertices lie in `L`. The class
need not be connected. Other classes at this height and tiles at other
heights remain unrestricted.

For an upward tile in this class, let `u` be its beta endpoint, the
start of its long edge. Select the gate

\[
 u\in q_0+z^{h+1}R.                                  \tag{1}
\]

Inside `L`, this is the one-prime residue condition for the selected
child edge node. Choosing `q_0` elsewhere in the same class selects
any other such gate. Let `P_g` count the **positive** upward tiles
passing through this gate; it is not a signed count.

Assume that the endpoint weight defined below has zero total on the
outer boundary. In particular this holds whenever no outer side has
height `h`, so it holds at height 1 on every F2 board, in either
normalization used by the project.

**Gate-capacity theorem.**

\[
 \boxed{222P_g\le43n_++179n_-}
 \quad\text{for }(a,b,c)=(33,7,37),                   \tag{2}
\]
\[
 \boxed{43P_g\le8n_++35n_-}
 \quad\text{for }(a,b,c)=(35,13,43).                 \tag{3}
\]

For the positive control `(5,3,7)` the certified inequality is
`2P_g<=n_++n_-`.

The same coefficients apply to a downward gate
`u in q_0+z^(h-1)R`. For negative tiles, interchange `n_+` and
`n_-`. Each variant requires its corresponding transformed endpoint
weight to vanish on the exterior. Absence of outer sides at height `h`
suffices for all four variants simultaneously. Thus these are capacities
for either sign and either hand, with the class, gate, and relevant
exterior condition stated explicitly.
Counts obtained from several different classes or gates must not be
added as though their upper bounds described disjoint extra populations.

## 2. Endpoint weights and why the inequality is global

Divide coordinates relative to `q_0` by `z^h`. The selected class is
now `R`. For an integral point `p=x+y*rho`, put

\[
 \phi(p)=ay-bx\pmod c.                              \tag{4}
\]

The upward gate is `phi(u)=0`. Indeed

\[
 u/z=((a+b)x+by+(-bx+ay)\rho)/c,
\]

and the norm identity makes divisibility of the two numerators
equivalent modulo `c`.

The certificate supplies three integer tables `f_0,f_1,f_2`, each
indexed by `Z/cZ`. On an oriented segment of height `h` and axis
`j mod 3`, assign the endpoint difference

\[
 F_j(\text{end})-F_j(\text{start}),
 \qquad
 F_j(P)=
 \begin{cases}
 f_j(\phi((P-q_0)/z^h)),&P\in L,\\
 0,&P\notin L.
 \end{cases}                                         \tag{5}
\]

Segments at other heights receive zero. This assignment telescopes on
arbitrary subdivisions and reverses with orientation, even at partial
contacts or endpoints outside `L`.

Every complete long edge at height `h` has vector `c*z^h*rho^j`.
Its endpoints are either both in `L`, with the same residue in (4),
or both outside `L`. Its weight is therefore zero. A short-height-`h`
tile in a different Euclidean class also has zero weight on both
short edges. Consequently, summing over the entire tiling isolates
exactly the short-edge weights `W(T)` of the selected class:

\[
 \sum_{T\in L}W(T)=W(\partial\text{board})=0.          \tag{6}
\]

No claim that a finite selected catalogue contains all neighbors is
used. Equation (6) follows from the complete physical tiling and the
endpoint definition on all points.

For each orientation, hand, and integral translation, the finite tables
satisfy

\[
 D\,\mathbf1_{\{T\text{ positive, upward, gated}\}}
 \le W(T)+C_+\mathbf1_{\{\epsilon=+1\}}
             +C_-\mathbf1_{\{\epsilon=-1\}}.          \tag{7}
\]

The exact triples are

| Tile | `D` | `C_+` | `C_-` |
|---|---:|---:|---:|
| `(5,3,7)` | 2 | 1 | 1 |
| `(33,7,37)` | 222 | 43 | 179 |
| `(35,13,43)` | 43 | 8 | 35 |

All quantities in (7) depend only on the integral translation modulo
`c`, so this is an exhaustive finite residue check for all translated
tiles, rather than a finite geometric placement assumption. Summing
(7) and using (6) proves the theorem.

If the outer endpoint weight is not zero, the proof instead gives

\[
 DP_g\le C_+n_++C_-n_-+W(\partial\text{board}).        \tag{8}
\]

One must retain this term rather than applying a homogeneous bound at
an exterior-bearing height without checking it.

For the negative-sign version, rotate all local coordinates by 180
degrees: the gate is unchanged and the signs reverse. For the downward
version, use `w -> -conjugate(w)` in the normalized coordinates.
It maps `(j,s)` to `(3-j,-s)`, preserves `epsilon`, and exchanges
`R intersect zR` with `R intersect z^(-1)R`. Absence of an exterior
side at height `h` is preserved. If exterior sides of that height
are present, vanishing of one particular table weight does not imply
vanishing of its transformed version: check the latter separately or
retain its boundary term as in (8).

## 3. A bank-count consequence

Put `n_L=n_++n_-`, `G_L=n_+-n_-`, and

\[
 \beta=1-2C_+/D=
 \begin{cases}
 68/111,&(33,7,37),\\
 27/43,&(35,13,43).
 \end{cases}
\]

Suppose `m` distinct actual bank tiles from this class pass through
one gate and have signed sum `K`, and both relevant sign-specific
endpoint weights vanish on the outer boundary. Absence of outer sides
at height `h` suffices. Applying the positive and negative versions
to their two sign populations gives

\[
 \boxed{n_L\ge m+|K+\beta G_L|.}                     \tag{9}
\]

In particular, if their positive signed sum is `K>=0` and
`G_L>=0`, then `m>=K` implies

\[
 \boxed{n_L\ge2K+\beta G_L.}                         \tag{10}
\]

This is an actual population cost for a physical bank. It requires
that the specified bank tiles belong to the selected class and gate.
It does not count their neighbors a second time.

## 4. Consequence for the minimal odd-population mode

Use the path frame `O=0,B=c^2,C=a(a+2b)z^2`, where the total odd
charge is `+c`. The previously proved actual-median localization says
that a hypothetical tiling with `n_odd=3c` has only heights `0,1,2`,
all height-one tiles lie in `zR`, and their sign populations are
`n_+=2c,n_-=c`.

For any upper median path let `J,K` be its direction characters at
long heights 1 and 2. Its parameter `t` is 2. Set

\[
 n=j_0+2=G_{\rm even}(\text{lower region})/c.
\]

This integer `n` is a path parameter, not a tile population. The
character formulas become

\[
 J=cn-d,\qquad K=2c-dn.                              \tag{11}
\]

Every height-2 step is the long edge of a distinct height-one tile
on the lower bank. The path vertices lie in
`cz(R+zR)`, a sublattice of both `zR` and `z^2R`. These bank tiles
therefore pass through the particular upward gate `z^2R`.
Their signs equal their direction characters. In particular `P_g>=K`
when `K` is positive.

The elementary sign inventory first gives `-c<=K<=2c`, hence
`0<=n<=floor(3c/d)`. The gate-capacity theorem strengthens this to:

| Target | Exact upper bound for `P_g` | Integer bound | Excluded `n` | Remaining `n` | Corresponding remaining `K` |
|---:|---:|---:|---|---|---|
| 3431 | `265/6` | 44 | 0, 1 | 2, 3, 4 | 22, -4, -30 |
| 5063 | 51 | 51 | 0, 1 | 2, 3, 4, 5 | 42, 20, -2, -24 |

For example, `n=1` would require at least 48 positive gated tiles
at 3431 or 64 at 5063, exceeding 44 and 51. The saturated `n=0`
case is excluded as well. No canonical-path assumption is made.
The remaining rows are not excluded by this argument.

## 5. Exact certificate and positive controls

`gate_capacity_certificates.json` contains the three integer endpoint
tables and coefficients. `verify_gate_capacity.py` uses only the
Python standard library, reconstructs the CCW polygonal short edges
independently of the LP generator, and checks all `12c^2` translations
and shapes:

| Tile | Independently checked two-dimensional columns |
|---|---:|
| `(5,3,7)` | 588 |
| `(33,7,37)` | 16,428 |
| `(35,13,43)` | 22,188 |

Every scaled column slack is a nonnegative integer. The minimum is
zero in each case. The LP supplied candidate tables; the proof relies
on these exact checked inequalities, not on a numerical infeasibility
message.

The replay also transforms and checks the whole height-one population
of both previously verified complete positive 143 tilings:

| Complete 143 control | `(n_+,n_-)` | Positive native-up gated tiles | Exact gate bound | Sum of endpoint weights |
|---|---|---:|---:|---:|
| Repository certificate | `(56,49)` | 14 | `105/2` | 0 |
| Independent macro certificate | `(49,42)` | 14 | `91/2` | 0 |

Both controls pass. The 14 gated positive tiles are compatible with
their actual upper-path character `K=14`; neither control has the
hypothetical odd population `3c`.

Replay with

```sh
python3 verify_gate_capacity.py --continuation /path/to/continuation \
  --macro /path/to/macro143_certificate.json
```

The output is `GATE_CAPACITY_REPLAY.json`. The paths can be omitted in
the current scratch layout; an explicitly supplied macro certificate
makes a relocated replay unambiguous.

## 6. Scope retained

The theorem is global for its stated single-class gate and exterior
weight hypotheses, and it allows arbitrary other heights, phases,
reflections, and T-junctions. The two exclusions in Section 4 are
unconditional consequences within the hypothetical `3c` mode.
They do not establish `n_odd>=5c`, a terminal `c^2` lower bound,
or impossibility of 3431 or 5063.

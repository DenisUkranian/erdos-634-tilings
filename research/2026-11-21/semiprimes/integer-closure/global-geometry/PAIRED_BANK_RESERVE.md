# Independent audit: mandatory long banks and residual pair reserves

21 November 2026. **Neither 3431 nor 5063 is excluded by this note.**
This is an independent derivation and strengthening of the neighboring
[mandatory long-bank reconstruction](../long-banks/long_bank_completion.py).
Its hypotheses are exact physical placements, not fractional periodic
columns. The main decomposition below requires **the complete family of
all odd-short-height tiles** of a proposed full tiling.

## 1. What the reconstruction determines

Use the standard board and sign convention of
[SIGNED_PHASE_POPULATIONS](../../../../2026-11-20/semiprimes/continuation/vertex-phase/SIGNED_PHASE_POPULATIONS.md):
the board has exterior direction heights 0 and 2,
`epsilon=s*(-1)^j`, and its full odd and even charges are `-c` and
`-d`, where `d=a-b`.

Let `O` be its complete odd family. Every short edge of `O` has an odd
direction height. The other edges on such a line are long edges of even
tiles; no board side occurs there. On each actual supporting line and
each orbit of translation by a length-`c` vector, write `J_n` for the
short-edge endpoint current. A positive directed interval contributes
`+1` at its initial endpoint and `-1` at its final endpoint. If `k_n`
is the net even long-edge multiplicity of the segment from orbit position
`n` to `n+1`, endpoint cancellation says

\[
 J_n+k_n-k_{n-1}=0.
\]

There is a finite solution if and only if `sum J_n=0`; it is unique and
is given by

\[
 k_n=-\sum_{i\le n}J_i.                                      \tag{1}
\]

Uniqueness is a finite-support assertion. The difference of two solutions
is constant on the entire doubly infinite orbit and consequently zero.
An orbit having no short endpoints cannot carry a nonzero finite net
long-edge chain either.

Nonoverlap implies `k_n in {-1,0,1}`. Two actual triangles with their
interiors on the same side of a common positive-length portion of a
long side overlap in a small neighborhood of that portion. Thus the
nonzero same-sign segments cannot have intersecting relative interiors.
This condition must be checked also between different longitudinal
orbits of the same actual line.

For each signed nonzero segment, exactly two congruent triangles have
that CCW long side and their interiors on its left. They are the two
choices of which endpoint is adjacent to side `a`. Both must be checked;
replacing them by only a half-turn mate would lose an allowed placement.
Containment and intersection with `O` give unary exclusions. Intersections
between choices at different segments give binary exclusions. Selecting
one of two choices at every segment is therefore exactly a 2-SAT problem
for **the mandatory bank alone**. It does not fill the remaining board.

The implementation uses exact rational coordinates, exact convex
separation, and a strongly connected component test with explicit
implication paths in an inconsistent case. Its endpoint recurrence and
choice construction agree with (1).

## 2. A fixed long-side direction fixes the sign, not the short height

Write a positive directed long vector as `c*z^h*rho^j`. The two possible
triangles on its left have labels

\[
 (h+1,j,-1),\qquad (h-1,j+3,+1)
\]

at their respective obtuse vertices. In both cases

\[
 \epsilon=-(-1)^j.                                          \tag{2}
\]

The two short heights differ by two. Reversing the long vector reverses
the sign. Consequently a pair of even tiles on opposite sides of an
identical whole long segment has opposite signs. Such a pair can be a
half-turn pair at one short height, or can have short heights differing
by two. **It need not be a half-turn pair.**

Let `M` be any physically compatible mandatory-bank selection and let
`B=|M|`, equivalently the sum of the absolute values of the reconstructed
coefficients. In a complete tiling, every other even tile is paired with
exactly one opposite-side tile on its identical whole long side. Indeed,
after removing the net coefficient in (1), the remaining coefficient
of every whole segment is zero. There can be at most one triangle on
each side. There are no further finite nonzero orbit solutions.

Thus, for an integer `P>=0`,

\[
 \boxed{N=|O|+B+2P.}                                        \tag{3}
\]

Each of those `P` residual pairs contains one positive and one negative
even tile. There is no independent unbalanced even charge left to repair.

The ordinary short-edge character of `O` is `d G(O)`, while that of
the mandatory long bank is `-c G(M)`. Summing their equality gives

\[
 \boxed{G(M)=\frac dc G(O)=-d.}                            \tag{4}
\]

This charge does not depend on the 2-SAT assignment. Formula (4) is also
an exact consistency check of the reconstruction. A compatible bank is
not a complete tiling, even when (3)--(4) hold.

## 3. A sign-residue cost for the residual pairs

Fix either prime phase tree. Use any finite set `V` of even exact nodes
that are proved occupied in a completion, including every node met by
`M`. Always include the exceptional height-zero core. The set may also
include exterior-free even ancestors forced by the established
[no-vacant-ancestor theorem](../../../../2026-11-20/semiprimes/continuation/vertex-phase/NO_PHASE_GAPS.md).
That theorem does **not** permit declaring arbitrary exterior-containing
ancestors occupied.

At `v`, let `p_v,q_v` be the mandatory positive and negative counts.
At an ordinary node put `r_v^+=r_v^-=0`. At the core the residues are

\[
 (r_+,r_-)=
 \begin{cases}(19,8),&3431,\\(5,27),&5063.\end{cases}
\]

Take least nonnegative residues

\[
 \delta_v^+=(r_v^+-p_v)\bmod c,\qquad
 \delta_v^-=(r_v^--q_v)\bmod c,
 \quad
 D_+=\sum_v\delta_v^+,\quad D_-=\sum_v\delta_v^- .          \tag{5}
\]

The separately rounded counts are `pbar_v=p_v+delta_v^+` and
`qbar_v=q_v+delta_v^-`. For each required ordinary node define

\[
 t_v=\max\{0,\ 2-(\bar p_v+\bar q_v)/c\},
 \qquad t=\sum_{v\text{ ordinary}}t_v.                    \tag{6}
\]

This is an integer in `{0,1,2}`: a required empty node needs two further
blocks, and a one-sign node rounded to one block needs one more. It is
zero as soon as the rounded node has at least two blocks. No extra
two-block condition is imposed on the exceptional core.

Since every missing pair supplies exactly one tile of each sign,

\[
 \boxed{P\ \ge\ R_\tau(M):=
       \min_{0\le j\le t}
       \max\{D_++cj,\ D_-+c(t-j)\}.}                     \tag{7}
\]

Here `j` is an integer. Each of the extra `t` sign blocks may be positive
or negative. Any split of their total between the signs can be distributed
over the required nodes, so (7) is the exact minimum in this particular
relaxed sign-count problem. It does not assert that the missing pairs can
be placed in space or realize the chosen node allocations.

Because (4) holds and the core residue difference is `-d modulo c`,

\[
 D_+\equiv D_-\pmod c.
\]

Writing `q=|D_+-D_-|/c`, the minimum in (7) has the closed form

\[
 \boxed{R_\tau(M)=\max(D_+,D_-)
        +c\left\lceil\frac{(t-q)_+}{2}\right\rceil.}     \tag{8}
\]

The first `q` extra blocks can be assigned to the sign with smaller
deficit for free relative to the larger deficit; the remaining blocks
must be split as equally as possible. Equations (7) and (8) agree in the
finite independent arithmetic checks.

Use the maximum of the two prime-tree reserves. Adding them would count
the same missing tiles twice. Both reserves have the common residue

\[
 P\equiv r_+-\#\{T\in M:\epsilon(T)=+1\}\pmod c.          \tag{9}
\]

## 4. A separate height-transport cost

Index even short heights by `2r`, and let
`m_r=sum_(T in M,h(T)=2r) epsilon(T)`. Let `E_r` denote the unknown full
even charge at that height. The phase population theorem gives

\[
 E_r\equiv-d\,\mathbf1_{r=0}\pmod c.
\]

A residual pair at one height changes no height charge. A mixed-height
pair has its two short heights `2r,2r+2`, and transports one unit of
signed charge between these adjacent height positions. If

\[
 S_r=\sum_{i\le r}(E_i-m_i),
\]

then the number of mixed pairs crossing that height cut is at least
`|S_r|`. Every mixed pair crosses exactly one such cut, so

\[
 P\ge\sum_r|S_r|.
\]

The residue of `S_r` is fixed by `M`. Eliminating all the unknown
`E_r` gives the completely explicit lower bound

\[
 \boxed{P\ge H(M):=
  \sum_{r\in\mathbb Z}
  \operatorname{dist}\!\left(
       \sum_{i\le r}m_i+d\mathbf1_{r\ge0},\ c\mathbb Z
  \right).}                                               \tag{10}
\]

The sum is finite: below all occupied heights and the core it vanishes;
above them it vanishes because `sum m_i=-d`. Distance means the least
nonnegative absolute integer residue, at most `(c-1)/2`.

This is the sharp minimum for the projected charge-transport problem
with only the stated height congruences. Each prefix flow can independently
take its least-absolute residue; successive differences then reconstruct
height charges with the required residues. The actual placement and node
requirements can increase the cost.

The height cost and node costs concern the same residual pairs. Take
their maximum, **not their sum**. If `r` denotes the residue in (9), define
`ceil_r,c(x)` to be the least integer at least `x` that is `r modulo c`.
For the mandatory selection put

\[
 \mathcal P(M)=\operatorname{ceil}_{r,c}
      \max\{R_+(M),R_-(M),H(M)\}.                         \tag{11}
\]

Every full completion of `O` therefore satisfies

\[
 \boxed{N\ge |O|+B+2\min_{M\text{ compatible}}\mathcal P(M).} \tag{12}
\]

The compatible choices are exactly those of the mandatory-bank 2-SAT
system, optionally with justified additional unary exclusions. The
objective in (12) is not itself a plain 2-SAT objective; its minimum
still requires a correct finite optimization or a lower certificate.
No global exceedance of 3431 or 5063 is asserted here.

## 5. Cellwise use and scope boundaries

One complete odd joint Euclidean cell also has its own unique mandatory
bank. Different cells on an actual short line have disjoint unit-offset
classes, hence disjoint length-`c` endpoint orbits. Every reconstructed
segment belongs to a unique odd cell. The mandatory counts consequently
add across all complete odd cells.

However a **single** complete cell does not make all other even tiles
residual cancelling pairs: other odd cells can require their own banks.
The pair decomposition and height-transport theorem apply after every
odd cell is included. The same-side and two-triangle conflicts must also
be checked across cells. A finite subset of an odd cell is insufficient,
since omitted odd short edges could change (1).

For an even-height cell, an exterior side may occur on its short lines.
Its known exterior endpoint current must then be included explicitly.
The unmodified zero-exterior reconstruction must not be applied to such
a cell, even if its exterior length is divisible by `c`.

## 6. An explicit whole-board bound on odd charge variation

Write the charge of every odd joint cell as `G_L=c g_L`, and put

\[
 V=\sum_{L\text{ odd}}|g_L|.
\]

The full standard-frame charge is `sum g_L=-1`, so `V` is a positive
odd integer. By the cellwise character identity, the mandatory bank of
cell `L` has even charge `d g_L` and at least `d|g_L|` tiles. These
banks consist of distinct even tiles. In particular

\[
 n_{\rm even}\ge dV.                                      \tag{13}
\]

The positive and negative variations of the cell charges are respectively
`(V-1)/2` and `(V+1)/2`. The mandatory even positive population is at
least `d(V-1)/2`. The full even positive population has residue `r_+`
modulo `c`, and its negative population exceeds it by `d`. Therefore
the sharper explicit estimate is

\[
 \boxed{n_{\rm even}\ge E_{\min}(V):=
 2\operatorname{ceil}_{r_+,c}\!\left(\frac{d(V-1)}2\right)+d,
 \qquad N\ge n_{\rm odd}+E_{\min}(V).}                    \tag{14}
\]

At `V=1`, the even minima are the existing 64 and 32. For larger
variation this replaces those constant reserves by a growing cost of
distinct physical neighbors. It may be combined with the previous
[odd-node minority and occupancy bound](../../continued-rigidity/global/UNIT_CHARGE_CELL_MINORITY.md),
since odd and even tiles are disjoint populations. Using just
`n_odd>=cV` already gives

\[
 \boxed{V\le53\quad(3431),\qquad V\le77\quad(5063).}       \tag{15}
\]

For 5063, the endpoint `V=77` forces `n_odd=3311` and
`n_even=1752`: the two lower bounds sum exactly to 5063. Every odd
cell would then have to be monochromatic, since equality in
`n_odd>=cV` leaves no cell minority. This is a necessary description
of that extremal variation, not its exclusion or a construction.

## 7. Exact controls

[`verify_bank_pair_reserves.py`](verify_bank_pair_reserves.py) checks both
long-side choices and their sign/height labels in all six directions at
four odd long heights for the two targets and the positive 143 control.
It independently groups actual even long edges in both complete 143
certificates, verifies the exact mandatory-versus-paired decomposition,
the common-sign formula, both prime-node reserves and the height cost.
It also checks the closed form (8), and explicit nonzero height-transport
examples, using integers and rational coordinates.

The controls test formulas on the stated data. The universal geometric
argument is the written derivation above, relying on the cited established
phase statements. A compatible reconstructed bank is not a full tiling;
an obstruction for one proposed complete odd packing is not an obstruction
for every possible odd packing.

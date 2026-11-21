# A rigid support-line cost for a unit-charge Euclidean cell

21 November 2026. **Both original counts 3431 and 5063 remain open.**
This is a necessary geometric condition at an arbitrary ordinary
Euclidean phase cell. It does not assume a total odd population,
terminality, a native phase, or only three short heights.

## 1. Statement and physical hypotheses

Use the established placement convention

\[
 u=q-a\rho^j,\qquad w=q+b\rho^{j+s},\qquad
 \epsilon=s(-1)^j,\qquad \rho=e^{i\pi/3},
\]

after translating and rotating the chosen height and Euclidean cell.
The original triangles have positive area. The sign `epsilon` records
orientation data, not the sign of geometric area.

For one cell let `p` and `m` be its populations of the two signs,
with the majority called positive. Suppose its charge is one block:
`p-m=c`. We require the physical, line-by-line short-edge congruence
from the [joint-cell current theorem](../../../../2026-11-20/semiprimes/continuation/common-obstruction/joint/JOINT_CELLS.md):

\[
 aM_\ell-bL_\ell\equiv0\pmod c.                 \tag{1}
\]

Here `M_ell` is the number of positive length-`a` sides minus the
negative ones on the actual supporting line `ell`; `L_ell` is defined
using length `b`. Every complementary long side has length `c`.
Exterior contributions on that individual line must be multiples of
`c`. In particular (1) holds at every odd-height cell, at nonnative
ordinary cells, and whenever the cited ordinary-cell argument supplies
it. The exceptional core with a nonzero exterior residue is excluded.
Arbitrary partial edge contacts and T-junctions are allowed.

**Unit-charge minority theorem.** Under these hypotheses,

\[
\boxed{
\begin{array}{c|c|c}
 (a,b,c)&\min(p,m)&p+m\\ \hline
 (33,7,37)&\ge2&\ge41\\
 (35,13,43)&\ge5&\ge53
\end{array}}
\tag{2}
\]

The same conclusion holds for charge `-c`, by reversing every
orientation with a half-turn. It is an intrinsic line-incidence
argument and does not require the board to admit that half-turn as
a symmetry.

The 5063 statement strengthens the previous `m>=1` cell bound. It
therefore restricts the four-cell five-block parameter to `5<=x<=42`.
It does **not** assert that a 53-tile charged cell can be realized.

## 2. Why rigid triangles give a simple incidence graph

There are three unoriented short-edge axis families. Given an actual
length-`a` supporting line and a nonparallel length-`b` supporting
line, their intersection fixes the obtuse vertex. For a specified
sign there is exactly one placement with those two **ordered roles**.
Two copies of that placement would overlap, and hence cannot both
occur in the cell.

Consequently the positive triangles form a simple bipartite graph:
the source vertices are their actual length-`a` lines, the target
vertices their actual length-`b` lines, and an edge is one positive
triangle. A geometric line may appear in both vertex sets. Edges
between parallel axis families are forbidden. A pair of nonparallel
source and target lines carries at most one edge.

This is a necessary graph of a rigid packing, not an assertion that
every such abstract graph has geometric positions. In particular,
the intersection coordinates of three families of lines cannot be
chosen independently.

A related stronger fact is useful when retaining negative triangles:
a positive triangle with ordered roles `(a-line,b-line)=(ell,k)`
and a negative triangle with reversed roles `(k,ell)` have the same
open 120-degree sector at the intersection. Their interiors overlap
near that vertex. Thus, writing their indicators as `P_ell,k` and
`N_k,ell`,

\[
 P_{\ell,k}+N_{k,\ell}\le1.                       \tag{3}
\]

The exact local control enumerates all twelve `(j,s)` templates. It
finds six ordered role pairs for each sign, exactly one of each, and
checks the equal sectors in (3). The exclusion in Sections 3--5 only
needs the positive simple-graph condition. Section 7 explains why
(3) alone does not eliminate the next case either.

## 3. Complete line-type reduction at 5063 for `m<=5`

For `(35,13,43)`, (1) is

\[
 M_\ell+7L_\ell=43k_\ell,\qquad k_\ell\in\mathbb Z.
\tag{4}
\]

The full signed counts give `sum M=sum L=43`, so `sum k=8`.
Since `M,L>=-m`, when `m<=5` the left side is at least `-40`.
It follows that every `k>=0`.

A line with `k=0` has `(M,L)=(7h,-h)`. A negative `h` would
require at least seven negative length-`a` sides, impossible here.
Thus `h>=0`. Put `t=sum h` over these zero lines. Each consumes at
least `h` negative length-`b` sides, so `0<=t<=m`.

Let `r` be the number of positive-`k` lines, and let `r_M,r_L` be
the numbers of lines carrying at least one positive `a` or `b`
side. The complete bounds are

\[
 r_M\le r+t+m,\qquad r_L\le r+m-t.                \tag{5}
\]

For the first, the positive-`k` lines contribute at most `r`; the
zero lines with `h>0` at most `t`; any further line carrying a
positive `a` side has `M=0` and consumes a negative `a` side.
For the second, outside the positive-`k` lines a positive `b` side
consumes a negative `b` side beyond the already reserved `t`.

If a particular line has `k>=1`, then `r<=9-k`, because the other
positive-`k` lines each consume at least one of the eight units.
Its net counts satisfy `M<=r_L`, `L<=r_M`, by the ordered-role
incidence bound. Therefore

\[
 43k=M+7L
 \le8(9-k)+8m+6t
 \le72-8k+14m.
\]

For `m<=5`, this excludes `k>=3`. Combining `k=1,2`, the bounds
`M,L>=-m`, and (5) leaves exactly these candidates:

| Name | `k` | `M` | `L` |
|---|---:|---:|---:|
| A | 1 | 1 | 6 |
| B | 1 | 8 | 5 |
| D | 2 | 2 | 12 |
| E | 2 | 9 | 11 |
| F | 2 | -5 | 13 |

Type F is possible arithmetically only at `m=5`. It consumes all
five negative `a` sides. No other zero-net `M` line can then carry a
positive `a` side. There is at most one F line and
`r_M<=r-1+t<=7-1+5=11`, whereas F requires at least thirteen
positive `a` lines to supply its thirteen positive `b` sides.
This excludes F.

A zero line with `h>=2` would require at least fourteen positive
`b` lines to supply its positive `a` sides; (5) gives at most
thirteen. Thus every nonzero `h` equals one. There are exactly `t`
such lines, called **Z**, with `(M,L)=(7,-1)`.

Let `a_0,b_0,d_0,e_0` count types A, B, D, E, respectively. The
entire necessary type list is now described by

\[
 a_0+b_0+2d_0+2e_0=8,\qquad b_0+e_0+t=5,
 \qquad0\le t\le m.                               \tag{6}
\]

There are no unlisted nonzero-net line types in this reduction.
Zero-net lines can still carry both signs; their contributions are
retained by the allowances in the next section.

## 4. A finite maximum-flow obstruction retaining the tile count

Each A, B, D, E, Z line supplies a fixed baseline number of positive
`a` sides, namely `1,8,2,9,7`. Their sum is exactly 43. The additional
positive `a` sides are paired in the signed count with negative `a`
sides, of which there are exactly `m`. Replace these additional
sources by one unrestricted source of capacity `m`. This weakens
the geometry and is therefore safe for an impossibility proof.

Each A, B, D, E line requires a baseline positive `b` population
`6,5,12,11`. Their total is `43+t`. There remain exactly `m-t`
positive `b` sides above those baselines. Split each one into a
fresh auxiliary target line of capacity one, in the same axis
family as its original line. Splitting a target cannot invalidate
the image of a real incidence graph: move the edge supplying that
extra side to its new target. It only relaxes the geometric
coincidences and the uniqueness of the original line.

Thus every real cell with `m<=5` induces an integer flow of value
`43+m` in one of the following finite networks:

1. Assign every A, B, D, E, Z source/line to one of three axes.
2. Assign the `m-t` auxiliary unit targets to axes.
3. Give a baseline source its stated supply and a baseline target
   its stated demand. A source--target pair has capacity one when
   its axes differ, and zero otherwise.
4. The unrestricted source of supply `m` may feed any target.

The total source supply and target demand both equal `43+m`.
No nonnegative integer flow of that value means that even this
relaxed line inventory cannot come from the positive triangles.

For compactness the checker groups equal line types on the same
axis. A group of `u` source lines and `v` target lines has capacity
`uv` between them. Every real simple incidence graph projects to
this grouped network. Grouping therefore cannot invalidate the
necessary condition.

The verifier exhausts (6), all axis-count assignments up to
permutation of the three axis names, and all distributions of the
auxiliary unit targets. It first rejects impossible source degrees.
For the rest it runs integer augmenting paths and verifies an equal
capacity cut in the final residual graph. The resulting exact counts
are:

| `m` | Axis assignments after preliminary type bounds | Degree failures | Further flow/cut failures | Survivors |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 108 | 108 | 0 | 0 |
| 2 | 558 | 558 | 0 | 0 |
| 3 | 1,676 | 1,672 | 4 | 0 |
| 4 | 7,100 | 7,031 | 69 | 0 |
| 5 | 25,247 | 24,636 | 586 | 25 |

The initial type bounds are just (5) and the fact that a line with
both roles needs the required opposite-role lines **outside its own
axis**, including exclusion of itself. They are not numerical
optimization results.

Every `m<=4` is excluded, proving the 5063 part of (2).

## 5. A short independent view of the last 5063 cases

The flow calculation has the following direct explanation at `m=4`.
The earlier values follow by the same, stricter bounds.

An E line would force exactly one `k=2` line, `t=1`, `r_M=12`,
`r_L=10`, and three B lines. Its own axis contains exactly one
positive line of each role. The three B lines cannot occupy the
other two axes while each has eight distinct positive `b` lines
off its own axis. A D line similarly forces one `k=2` line, `t=2`,
`r_M=13`, `r_L=9`, and three B lines. Each B axis could have only
one positive `b` line, which cannot accommodate both three B
lines and the additional D line. Thus all eight positive-`k` lines
are A or B, with `b_0+t=5`.

At `t=0`, five B targets require 25 positive `b` incidences. Their
own B sources contribute at most 16 ordered cross-axis incidences;
the remaining positive `a` population is only seven. Hence at most
23 can reach them.

At `t=1`, four B lines occupy at most two axis families. The sole
Z line cannot lie in the B-free axis, because it needs seven
positive `b` lines off its axis. B-to-B incidences contribute at
most eight, A sources and all negative-`a` corrections at most
eight, and Z contributes at most three. The total is at most 19,
below the required 20.

At `t=2`, three B lines require exactly ten positive `b` lines and
split into one and two B lines on their two axes. Each of the two
B lines on the latter axis must meet every one of the other eight
positive `b` lines. There are two extra zero-net positive `b`
lines, each of population one because the remaining negative-`b`
budget is `m-t=2`. They cannot lie on that two-B axis, already
filled by its two B lines; outside it they would each receive at
least two B incidences, impossible.

At `t=3`, the two B lines require nine positive `b` lines and lie
on different axes, each containing only its one B line. The one
extra zero-net target line lies off both axes and would receive
two incidences despite capacity one. At `t=4`, the single B line
would require nine positive `b` lines, while (5) permits only eight.

The finite checker independently performs the full network accounting
instead of importing these case arguments.

## 6. The analogous 3431 bound

For `(33,7,37)`, the line equation is

\[
 M+11L=37k,\qquad\sum k=12.                       \tag{7}
\]

Suppose `m<=1`. Then all `k>=0`; zero lines have `(M,L)=(11h,-h)`
with `h>=0`, and `t=sum h<=m`. Bounds (5) hold with this `t` and
the present positive-`k` line count `r`. For a positive-`k` line,
`r<=13-k`, giving

\[
 37k\le12(13-k)+12m+10t\le156-12k+22m.
\]

Hence `k<=3`. The possible nonzero line types are
`A=(4,3), B=(8,6), C=(12,9), D=(1,10)` with respective
`k=1,2,3,3`. Other integer solutions violate `M,L>=-m` or the
role-line bounds. Summing `M` gives `d_0-t=1`, where `d_0`
counts type D.

If `t=1`, at least two D lines consume six `k` units, leaving at
most eight positive-`k` lines altogether. A zero line with `M=11`
would then require eleven positive `b` lines, whereas
`r_L<=r+m-t<=8`. Thus `t=0`, `d_0=1`.

The D target needs ten positive `a` lines off its axis. As D itself
has a positive `a` side, `r_M>=11`. With at most one negative
`a` side, this forces exactly nine A lines and one D line. It is
already impossible at `m=0`.

At `m=1`, the D demand forces all nine A lines off the D axis,
as well as the only possible additional positive `a` line. Each
A source sends one of its four edges to D and has three left.
The nine A lines occupy two axes; one axis contains at least five
of them. Those five sources must send at least fifteen edges to
the opposite A axis and to any extra positive `b` side. The other
axis has at most four A targets, of total capacity at most twelve;
the one negative `b` side adds at most one further target unit.
The maximum is thirteen, a contradiction.

The checker independently verifies all 85 axis assignments of this
last necessary network by exact maximum-flow/minimum-cut equality.
Therefore `m>=2`, proving the 3431 part of (2).

## 7. The next 5063 value is not excluded by line incidence alone

The checker exports all 25 surviving networks at `m=5`, with exact
flow witnesses, in
[`CELL_MINORITY_FRONTIER_5063.json`](CELL_MINORITY_FRONTIER_5063.json).
They are relaxed line networks, not placed triangles or solutions
of the endpoint-current equations.

The first survivor also has a fully integral **signed** incidence
control satisfying (3). Take eight A lines with axis counts `(0,2,6)`,
five Z lines all on axis zero, and five zero-net lines carrying one
positive and one negative `a` side: four on axis one and one on axis
two. Each Z sends positive incidences to all six axis-two A lines
and to one axis-one A line. The two axis-one A sources and four
axis-one zero-net sources fill the six remaining axis-two A slots.
The six axis-two A sources and the one axis-two zero-net source fill
the seven remaining axis-one A slots. The five negative incidences
join the five zero-net `a` lines to distinct Z `b` lines.

This has 48 positive and five negative abstract triangles. No
ordered pair is repeated, and no positive ordered pair reverses a
negative one. It satisfies all line signed counts. However no
supporting-line coordinates, rigid metric placements, endpoint
currents, or nonoverlap between different intersections are supplied.
It specifically prevents interpreting a surviving line graph as
either a tiling or a counterexample to a stronger geometric theorem.

## 8. A global signed population reserve

The local physical bound gives a closed-form necessary inequality for
the whole tiling, without fixing its odd population or height range.
Put `mu=2` for 3431 and `mu=5` for 5063. At an ordinary exact node
`v` in either prime tree, write its sign populations as `cp_v,cq_v`.
For its joint cells write `g_L=G_L/c` and define

\[
 P_v=\sum_{L\subset v}\max(g_L,0),\qquad
 Q_v=\sum_{L\subset v}\max(-g_L,0),\qquad
 U_v=\#\{L\subset v:|g_L|=1\}.
\]

The balanced reserve is exactly

\[
 E_v=\sum_{L\subset v}\min(n_L^+,n_L^-),\qquad
 cp_v=cP_v+E_v,\qquad cq_v=cQ_v+E_v.
\]

Thus `E_v` is a multiple of `c`. Theorem (2) gives `E_v>=mu U_v`,
and hence

\[
\boxed{
 n_v\ge c\sum_{L\subset v}|g_L|
       +2c\left\lceil\frac{\mu U_v}{c}\right\rceil.}
\tag{8}
\]

This strengthens the earlier unit-charge reserve, whose numerator
was only `U_v`. For example, nine unit-charge cells incident to one
5063 ordinary node now require two balanced sign blocks in that
node, instead of the one block obtained from the old bound. Their
additional cost is 86 actual tiles.

An occupied ordinary node also has at least two blocks, independently
of its charge. Thus its complete available bound is the maximum of
`2c` and the right side of (8); a balanced occupied node is not free.

For a whole tiling let

\[
 V=\sum_{h\text{ odd}}\sum_{L\text{ at }h}|g_L|,
\quad
 R_h=\max_{\tau\in\{\pi,\bar\pi\}}
       \sum_{v\text{ at height }h\text{ in tree }\tau}
           \left\lceil\frac{\mu U_v}{c}\right\rceil.
\]

The exact nodes at each height partition that height's actual
population. Both prime trees describe the same tiles, so take their
maximum at each height, never their sum. Summing (8) over the
disjoint odd heights gives

\[
\boxed{n_{\rm odd}\ge cV+2c\sum_{h\text{ odd}}R_h.}
\tag{9}
\]

The [signed phase identities](../../../../2026-11-20/semiprimes/continuation/vertex-phase/SIGNED_PHASE_POPULATIONS.md)
give minimum complete even populations 64 at 3431 and 32 at 5063.
For clarity, in the standard frame the core residues are `(19,8)`
and `(5,27)`. The even signed charge is `-d`. At 3431 the core
residue charge is 11 and one further negative block of 37 is
needed, costing at least `27+37=64`; at 5063 the residue charge
already equals -22 and costs 32. Extra nodes cannot reduce these
counts. Consequently the global bounds are

\[
\boxed{3431\ge64+37V+74\sum_hR_h,\qquad
       5063\ge32+43V+86\sum_hR_h.}                 \tag{10}
\]

Here `R_h` uses the appropriate `mu,c` for its target. The invariant
odd charge gives `sum g_L=+1` or `-1` according to frame, so the
variation `V` and the reserve concern the mandatory whole-board
imbalance. Equation (10) combines that imbalance, a rigid geometric
incidence obstruction, signed divisibility, and the available tile
count. It does not yet force a contradiction for every admissible
configuration; small numbers of unit-charge cells leave substantial
room. All larger-population regimes remain in scope of (9)--(10).

Retaining the two-block cost just noted gives the stronger version

\[
\boxed{
 N\ge b_e+c\sum_{h\text{ odd}}\max_{\tau}
 \sum_{v\text{ occupied at }h\text{ in tree }\tau}
 \max\left\{2,\ \sum_{L\subset v}|g_L|
              +2\left\lceil\frac{\mu U_v}{c}\right\rceil\right\},}
\tag{11}
\]

where `(b_e,c,mu)=(64,37,2)` or `(32,43,5)`. It counts actual
tiles once, including balanced occupied nodes, and needs no terminal
branch hypothesis. No exceedance of the target count has been
established for all possible joint-cell data.

## 9. Reproduction and provenance

Run from the repository root:

```sh
python3 research/2026-11-21/semiprimes/continued-rigidity/global/verify_cell_minority.py
```

The program uses only the Python standard library and integer
arithmetic. Its replay is
[`CELL_MINORITY_REPLAY.json`](CELL_MINORITY_REPLAY.json). It checks
the twelve local templates, finite type/axis networks, residual cuts,
and the signed next-case control. The geometric reduction to those
networks is the written proof above; the code is not a formal
proof-assistant verification.

The 5063 case argument was developed in the parallel cell study and
independently audited and replaced here by a complete finite network
check. No unsupported unsigned divisibility of Euclidean cell
populations is used. Larger cell populations and both original
whole-board counts remain open.

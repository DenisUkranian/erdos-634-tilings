# Independent audit of the native exceptional-core budget

21 November 2026. This audit checks the four certificates in
[`../core-budget/`](../core-budget/) and the physical reduction used by
`probe_core_budget.py`. **No original target is excluded by these bounds.**

## Verdict and exact scope

The four supplied inequalities and their integer population roundings pass
an independent exact check. The geometric projection is valid under the
stated hypotheses:

1. all short heights belong to `{0,1,2}`;
2. the entire odd family belongs to the single native class `zR` at height
   one;
3. the selected class is the native exceptional height-two class `z^2R`
   in the **path frame**.

Remote even classes may be occupied. The proof must retain the unique
odd-class hypothesis; it does not automatically apply to the two- and
four-cell alternatives at 5063 or to larger height support.

The precise ordinary/exceptional population residues are frame-dependent.
Here the exceptional core residues are `(8,19)` at 3431 and `(27,5)` at
5063. Using the standard-frame residues `(19,8)` or `(5,27)` here would
interchange the sign populations and give the wrong rounding.

## 1. Why the single/pair catalogue remains containing

For a height-two native-core tile, a long side of height three has no
neighboring short-height-three tile or exterior side. No height-four
short tile exists. Its maximal supporting run therefore has only
height-two long sides of length `c` on both banks. The equal-length
partitions coincide, and its actual whole half-turn mate is present.

A downward long side has height one. At the native gate it may contact
odd short sides, so all such columns remain available singly. At any
nonnative gate, the corresponding exact height-one node in the conjugate
tree has no odd tiles. It is exterior-free: the only exterior-containing
height-one ancestor is the native one in the established exterior-chain
classification. A height-zero tile furnishing a long side on that run
would be an occupied descendant of that absent exterior-free height-one
node. The occupied-ancestor theorem rules this out. Thus that run again
contains only height-two long sides, which pair whole-to-whole.

A whole mate of a native-core tile has all vertices in the same native
Euclidean class. Consequently all nonaccessible long sides of the core
are paired within the core. Remote even tiles elsewhere do not supply a
missing bank at one of these nonnative height-one gates.

This argument allows T-junctions globally. Whole pairing is deduced only
on runs where all available bank sides have equal length `c`, with no
short bank or exterior contribution. It must not be extended to a run
having neighboring short edges.

The native height-zero analogue is symmetric. Its only accessible long
sides are upward native-gate sides; the downward and nonnative upward
long sides pair. Its only exterior side at its own short height has length
`c^2`, so the periodic endpoint source is zero. The homogeneous single-gate
charge bound may therefore be used there, including when remote even
classes exist. Its parity/sign-population rounding remains necessary.

## 2. Direct derivation of the exceptional endpoint source

Write

\[
 A=b(2a+b),\qquad B=a(a+2b),\qquad z=(a+b\rho)/c.
\]

The path-frame board is `conv(0,c^2,Bz^2)`. Dividing by `z^2` gives the
counterclockwise vertices

\[
 O=(0,0),\qquad X=(B,-A),\qquad Y=(B,0).
\]

Indeed `c^2/z^2=(B,-A)` and its norm is `c^4`. The edge `O->X`
is not an axis of the height-two endpoint tables. The other two edges
are `X->Y` on axis one and `Y->O` on axis zero. With endpoint current
`delta_end-delta_start`, their source is exactly

\[
 \boxed{J_0=\delta_O-\delta_Y,\qquad
        J_1=\delta_Y-\delta_X,\qquad J_2=0.}
\]

The checker obtains this by inspecting the three actual polygon edges,
not by importing the generator's `rhs_nonzero` list. The resulting rows
agree with every supplied certificate.

Whole height-two long sides of odd neighboring tiles contribute zero to
these periodic endpoint tables, including when a board side is subdivided.
Endpoint telescoping therefore retains exactly this source for the native
height-two short tiles. Treating the exceptional source as zero would be
incorrect.

## 3. Independent column and rounding checks

The verifier constructs the CCW triangle polygon for each translated
orientation. It identifies the short-edge axes from the actual vectors,
computes `delta_end-delta_start`, and adds the specified charge weight.
It permits every downward native single and every whole half-turn pair.
The certificate denominator bounds the single score and twice that
bound dominates every pair score.

| Tile | Core charge | Singles checked | Pairs checked | Exact certified lower bound | Rounded core population |
|---|---:|---:|---:|---:|---:|
| `(33,7,37)` | -48 | 222 | 8,214 | `21064508116/100000001` | **212** |
| `(33,7,37)` | -85 | 222 | 8,214 | `35970666295/100000001` | **397** |
| `(33,7,37)` | -122 | 222 | 8,214 | `51093809348/100000001` | **582** |
| `(35,13,43)` | -107 | 258 | 11,094 | `67699999951/100000001` | **677** |

The population rounding independently solves

\[
 n_+=r_++ct_+,\quad n_-=r_-+ct_-,\quad
 t_+,t_-\in\mathbb Z_{\ge0},\quad n_+-n_-=G.
\]

For a fixed charge the allowed totals have step `2c`. The first totals
at or above the certified rational bounds have sign populations,
respectively, `(82,130)`, `(156,241)`, `(230,352)`, and `(285,392)`.
The immediately preceding congruent total violates the exact dual in
each case. Floating optimization values are not used for the rounding.

## 4. Complete 143 control

The existing complete 143 tiling was independently transformed to the
native path frame and then divided by `z^2`. Its entire exceptional
core has 38 tiles and charge two. Its exact source is the boxed boundary
current above. It decomposes into two accessible downward singles and
18 compulsory whole pairs, with actual, unreduced coordinates.

This checks the source signs and the physical single/pair reduction on a
genuine complete positive tiling. It does not apply the target-specific
numerical duals to the different control shape.

## Replay

```sh
python3 research/2026-11-21/semiprimes/full-closure-attempt/target5063/verify_core_budget_audit.py
```

The checker uses only Python integers and `Fraction`; it imports neither
the LP builder nor NumPy/SciPy. Output and input hashes are recorded in
[`CORE_BUDGET_INDEPENDENT_REPLAY.json`](CORE_BUDGET_INDEPENDENT_REPLAY.json).
This is an independent internal mathematical and implementation audit,
not external peer review or proof-assistant formalization.

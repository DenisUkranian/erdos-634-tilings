# Simultaneous ordered quotients determine a median path's position

21 November 2026. This note proves a positional necessary condition for
**every** upper median path in a complete tiling of either target. The
condition uses two ordered, nonabelian boundary quotients and actual
board containment. It does not force a negative face in a disk filling,
prove a lower bound `A(W)>N`, or decide either target.

**Theorem.** Let an upper median path be vertex-simple, oriented from
`O` to `B` in the path frame. No nonempty consecutive subpath has word
equal to the identity in both of the free products defined below.
Equivalently, all ordered pairs of prefix states in those two groups
are distinct. This holds for both 3431 and 5063.

The theorem concerns the actual whole-length-`c` path supplied by
[TWO_PATHS](../../paths/TWO_PATHS.md), without a restriction on other
tile heights, translations, or partial contacts in the complete board.

## 1. The two quotient maps are explicit

Let

\[
 R=\mathbb Z[\rho],\quad \rho=e^{i\pi/3},\quad
 z=(a+b\rho)/c,\quad c^2=a^2+ab+b^2.
\]

The primitive integers `a,b,c` are pairwise coprime. A directed unit
edge of heading `z^h rho^j` has generator `e(h,j)`, with
`e(h,j+3)=e(h,j)^(-1)`. Both hands of the tile give the relations

\[
 e(h,j)^a e(h,j+1)^b=e(h+1,j)^c,\qquad
 e(h,j)^a e(h,j-1)^b=e(h-1,j)^c.                 \tag{1}
\]

These are the ordered edge relations used in the existing
[noncommutative boundary note](../../../../../final-push-oct7/duality/NONCOMMUTATIVE_BOUNDARY.md).
They follow from unit subdivision and the disk relation; no assertion
about a positive geometric realization of an arbitrary group word is
needed here.

Put

\[
 \mathcal A=C_a*C_a*C_a=\langle X_0,X_1,X_2\mid X_i^a=1\rangle,
 \qquad s=bc^{-1}\pmod a,
\]
\[
 \mathcal B=C_b*C_b*C_b=\langle Y_0,Y_1,Y_2\mid Y_i^b=1\rangle,
 \qquad t=ac^{-1}\pmod b.
\]

Extend the generators by `X_(i+3)=X_i^(-1)` and
`Y_(i+3)=Y_i^(-1)`, with period six. The norm identity gives
`s^2=1 mod a` and `t^2=1 mod b`. Define

\[
 e(h,j)\longmapsto X_{j+h}^{s^h},\qquad
 e(h,j)\longmapsto Y_j^{t^h}.                  \tag{2}
\]

These are homomorphisms of the entire tile presentation. In the first,
the length-`a` side is trivial and the remaining exponents agree because
`cs=b mod a`; the reflected relation uses `s^(-1)=s`. In the second,
the length-`b` side is trivial and the other exponents agree because
`ct=a mod b`, again for both hands. This verifies the word-label
property rather than assuming it.

For a whole long-edge step `(h,j)`, its two labels are therefore

\[
 X_{j+h}^{c s^h},\qquad Y_j^{c t^h}.             \tag{3}
\]

An actual upper median path has `h=1` or `2`. Since the lower region
is tiled and its positive boundary is the base followed by the reversed
path, the whole path words are, respectively,

\[
 X_0^{c^2},\qquad Y_0^{c^2}.                    \tag{4}
\]

The quotient factors need not have prime order. In particular, the
orders `a=33` and `a=35` are retained in full.

## 2. Joint-null subpaths have an exact translation period

The following lemma also applies to any two consecutive long heights
`k,k+1`. It is independent of positivity or containment.

Define

\[
 \Lambda_0=cR+(a+b\rho)R=c(R+zR),\qquad
 L_k=z^k\Lambda_0.
\]

**Joint-null translation lemma.** If a word of whole-length-`c` steps
at heights `k,k+1` is trivial in both groups (2), its physical endpoint
displacement satisfies

\[
 \boxed{\Delta\in ab L_k.}                     \tag{5}
\]

To prove this, normalize the physical displacement by `z^k`, putting
`Delta'=z^(-k) Delta`. Every step is then `c rho^j` or
`(a+b rho)rho^j`, so `Delta'` belongs to `Lambda_0`.

Map `A` to the additive group `R/aR` by

\[
 X_i\longmapsto s^{-k}\rho^{i-k}.
\]

This is a well-defined homomorphism: the additive group has exponent
`a`, and `rho^(i+3)=-rho^i` respects reversal. For a lower-height
step its value is `c rho^j`; for an upper-height step it is
`cs rho^(j+1)=b rho^(j+1) mod a`, exactly the corresponding physical
step modulo `aR`. Triviality of the first word implies `Delta' in aR`.

Similarly map `B` to `R/bR` by `Y_i -> t^(-k) rho^i`.
The upper step maps to `ct rho^j=a rho^j mod b`, and the lower
one to `c rho^j`. Hence the second identity gives `Delta' in bR`.
Since `a` and `b` are coprime, `Delta' in abR`.

It remains to retain the sharper lattice `L_k`, rather than replacing
it by `z^kR`. In axial coordinates the exact index calculation is

\[
 \Lambda_0=
 \{x+y\rho\in R: ay-bx\equiv0\pmod c\},
 \qquad [R:\Lambda_0]=c.                        \tag{6}
\]

Indeed the four generators `c,c rho,a+b rho,-b+(a+b)rho`
satisfy the congruence. Modulo `c`, every solution is a multiple of
`(a,b)`, because `a` is a unit modulo `c`; the second rotated vector
satisfies the same relation by the norm equation. The congruence is
surjective, so its kernel has index `c`. This is the Smith-index
statement with invariant factors `1,c`.

For any integer `m` coprime to `c`,

\[
 \Lambda_0\cap mR=m\Lambda_0.
\]

For if `my` belongs to `Lambda_0`, multiplication by `m` is invertible
on the finite quotient `R/Lambda_0`, so `y` already belongs to
`Lambda_0`. Apply this with `m=ab` and multiply back by `z^k` to
obtain (5).

No existence of a jointly null interval has been inferred in this
argument. It only controls its displacement if such an interval occurs.

## 3. The target boards have no nonzero joint period as a chord

In the path frame the board is

\[
 T=\operatorname{conv}\{0,c^2,C\},\qquad
 C=Bz^2,\quad A=b(2a+b),\quad B=a(a+2b).
\]

Its side lengths are `A,B,c^2`; its diameter is `B` on both targets.
We need `k=1` in (5).

For these cases an explicit Eisenstein generator of `Lambda_0` is

| Tile | `pi` with `Lambda_0=pi R` | `Norm(pi)` |
|---|---|---:|
| `(5,3,7)` | `1+2 rho` | 7 |
| `(33,7,37)` | `3+4 rho` | 37 |
| `(35,13,43)` | `6+rho` | 43 |

Each generator satisfies (6) and has norm `c`; hence its principal
lattice has the same index `c` and equals `Lambda_0`. Thus
`abL_1=ab z pi R` is a triangular lattice with shortest nonzero length
`ab sqrt(c)`. Every nonunit Eisenstein integer has norm at least three:
its integer norm `x^2+xy+y^2` is never two. Consequently the next
possible length is at least `sqrt(3) ab sqrt(c)`.

### 5063: the first period already exceeds the diameter

\[
 (ab)^2c=455^2\cdot43=8,902,075
       > 2135^2=4,558,225.
\]

No nonzero joint period joins two points of this board.

### 3431: the exact orientation excludes the shortest six vectors

The minimum squared length is

\[
 231^2\cdot37=1,974,357 <1551^2=2,405,601,
\]

so the diameter alone is insufficient. The next shell has squared
length at least `5,923,071`, which exceeds the diameter squared.
Only the six unit multiples of

\[
 ab z\pi=(16401+41811\rho)/37
\]

could be board chords. Up to sign they are

\[
 (16401,41811)/37,\quad
 (-41811,58212)/37,\quad
 (-58212,16401)/37.                            \tag{7}
\]

The board has axial coordinate spans

\[
 0\le x\le1369,\qquad
 0\le y\le792561/1369.
\]

The first two vectors in (7) exceed the `y` span in absolute value.
The third exceeds the `x` span, since `58212>37*1369=50653`.
Their negatives fail the same tests. Thus this board also has no
nonzero joint period as a chord.

The checker additionally uses the exact difference body, not just
these necessary coordinate-span tests. For a displacement written
`v=r(c^2,0)+sC`, membership in `T-T` is precisely

\[
 |r|\le1,\quad |s|\le1,\quad |r+s|\le1.
\]

Combining this geometric exclusion with (5), a simultaneous-null
subpath inside either board must have zero displacement. A
vertex-simple upper path cannot repeat its endpoint, proving the
theorem stated at the start.

## 4. Controls and the precise obstruction still missing

The exact checker reads both complete positive 143 upper paths from
the previously verified
[actual-median replay](../../charge-transport/geometry/ACTUAL_MEDIAN_CHARGES.md).
It checks both ordered boundary identities, develops every prefix
by exact rational displacement, and checks the joint-period property
for any repeated pair of prefix states. Both complete controls pass.
Their current upper paths have no repeated joint prefix state.

The 143 board is not incorrectly excluded by the geometric theorem:
its shortest joint period has squared length `1575<55^2`, and some
of the shortest periods really are chords of its difference body.
The theorem's target-specific chord hypothesis therefore fails there.

There is a decisive limitation even on the targets. The canonical
words

\[
 (h=1,j=0)^a\,(h=1,j=5)^b
\]

have the correct physical endpoint `c^2`, satisfy both identities
(4), and have distinct joint prefix states. The checker verifies
these statements for both targets and the 143 control. Their two
coordinate reductions can be made noncrossing separately: the first
`a`-block vanishes in the first quotient and the last `b`-block in
the second. They provide no common-null interval. Completion of the
whole board above such a path is a separate problem.

Thus two noncrossing reductions do **not** by themselves force a
simultaneous-null subpath. An assertion of that kind would need
additional information from the actual tiled disk. Likewise, mere
simplicity of a path in the product Cayley graph does not bound its
length sufficiently to decide either target.

For upper steps, the two factor axes are `j+h mod 3` and `j mod 3`.
The six unoriented types form `K_(3,3)` with the three diagonal pairs
removed, a six-cycle. The unproved next step is to combine this
incidence pattern with the actual disk's two ordered reductions or
with a positional cost for their crossings. No such area lower
bound is claimed here.

### A single-quotient mixed reduction is locally realizable

The companion `check_mixed_syllable.py` prevents a false shortcut.
Take step types `(h,j)=(1,5)` and `(2,4)`. They belong to the same
factor in `A`. Three of each have exponent `3b+3c=4a` at 3431;
five of each have exponent `5b+5c=8a` at 5063. Both the one-switch
and alternating orders are simple path segments whose unique actual
bank triangles are pairwise interior-disjoint and can be translated
into the corresponding board. Exact rational coordinates are saved
in `MIXED_SYLLABLE_REPLAY.json`.

These controls are partial bank packings, not tiled lower regions
or complete board tilings. They show why adjacent-turn legality
cannot exclude these mixed torsion syllables. They are not jointly
null in the second quotient.

A blanket exclusion of supported mixed-height cycles would also
be false: the earlier
[balanced-strip controls](../../common-obstruction/boundary/UNMATCHED_NODES_AND_GATES.md)
have fully tiled interiors of `2c` tiles, actual mixed long-edge
cycles, and disjoint supporting banks inside both targets. A useful
extension of pure-cycle exclusion must therefore impose a further
global attachment or charge condition.

## 5. Exact reproduction

From this directory after inclusion in the continuation package:

```sh
python3 verify_joint_null.py \
  --known-replay ../../charge-transport/geometry/ACTUAL_MEDIAN_REPLAY.json \
  --out JOINT_NULL_REPLAY.json
python3 check_mixed_syllable.py --continuation ../.. \
  --known-replay ../../charge-transport/geometry/ACTUAL_MEDIAN_REPLAY.json \
  --out MIXED_SYLLABLE_REPLAY.json
```

The first checker uses only the Python standard library and exact
rational arithmetic. The second uses the project's exact placement
geometry for the finite local bank controls. Neither searches for
a target tiling or claims a minimum disk area. Both target existence
questions remain open.

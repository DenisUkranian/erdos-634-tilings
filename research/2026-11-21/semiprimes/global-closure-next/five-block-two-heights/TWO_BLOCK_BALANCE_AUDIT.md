# Independent audit of the one-height two-block balance theorem

21 November 2026. This audit concerns
[`TWO_BLOCK_BALANCE_5063.md`](../global-strengthening/TWO_BLOCK_BALANCE_5063.md),
whose reviewed SHA-256 is
`f8a5c064aaee603e2eb726cd92226e23368737329e6c3557f9fd15c8d9957bdd`.
It was performed independently of that theorem's author, after the
two-height profile exclusion had been completed.

**Result: PASS.** Under the stated hypothesis that all odd short heights
other than one are empty, every exact 86-tile height-one node of either
prime tree is balanced. No conclusion excluding a whole 215-tile layer
or the original count 5063 follows from this audit.

## Geometric checks

1. A monochromatic exact 86-tile node is one Euclidean cell. Signed cell
   divisibility makes each of its occupied cells a positive multiple of
   43; the existing one-block line theorem excludes a 43-tile cell.
2. The actual-line current isolates that cell by an endpoint potential
   supported on it. Short sides from other cells have both endpoint
   values zero. A whole complementary long side has normalized
   displacement `43 rho^j`, so its endpoint contribution is either zero
   or a multiple of 43. No exterior side has short height one. This
   justifies the separate congruence on each used supporting line,
   including separated runs and partial contacts.
3. For fixed sign and hand, two supporting lines in different axis
   families determine at most one allowed placement. With one short
   side on a fixed line, the other short side belongs to the axis family
   determined by that hand. These statements justify both the global
   pair-product bound and the per-line majority-hand bound.
4. Every child subtree has zero odd charge under the one-height
   hypothesis. Its exact parent current is therefore the applicable
   native offset plus `22e`, or simply `22e` at an exterior-free gate.
   These are currents of the entire exact parent node. The single-cell
   conclusion in item 1 is what permits the single-class gate capacity
   to bound them.
5. All tiles in this parent have one sign. Their signed gate count is
   thus their actual gate population, with no opposite-sign half-turn
   cancellation inside the parent. The parent tiles are partitioned by
   their hand and gate, so zero outward gate currents imply zero tiles
   of that hand, and native currents of magnitude one or two imply
   precisely that many outward-hand tiles.

## Independent arithmetic derivation

The line congruence

\[
35M-13L\equiv0\pmod{43}
\]

has the particularly short equivalent form

\[
M+7L=43k,\qquad k\in\mathbb Z_{>0}
\]

on every used line. Since both edge totals are 86, summation gives
`sum k=(86+7*86)/43=16`; hence there are at most 16 used lines.
This independently recovers the line bound without the original draft's
auxiliary variables `t,u`. The author subsequently incorporated this
shorter derivation into the reviewed version identified above.

If at least 84 tiles have one hand, direct enumeration of all ordered
axis-family triples with total at most 16 and pair-product sum at least
84 gives only permutations of `(4,6,6)` and `(5,5,6)`. Each family has
at most six lines. At most two minority tiles then give `M,L<=8` on
every line. Independent enumeration of the line congruence in that box
gives exactly `(1,6)` and `(8,5)`. The two totals 86 force six lines of
the first type and ten of the second. The ten lines with `M=8` require
at least 20 minority length-35 edges, contradicting a minority of at
most two tiles.

Independently enumerating the native residue classes in the interval
permitted by the one-sign gate bound reproduces:

| Native offset | Parent sign | Possible current |
|---:|:---:|---:|
| 86 | positive | none |
| 86 | negative | -2 |
| -43 | positive | 1 |
| -43 | negative | none |

At a remote gate, the only multiple of 22 in `[-16,16]` is zero.
Thus each alleged monochromatic two-block node contradicts the
independently checked incidence lemma.

## Replay and scope

The supplied `verify_two_block_balance.py` was run independently and
returned `finite_arithmetic: PASS`. A separate Cartesian calculation
also checked the alternative line identity, all six ordered family
triples, the line-pair set, and the four native residue cases.

The final implication from a balanced exact two-block node to zero
charge in each joint cell is the existing joint-cell reserve theorem.
The argument does not assume unsigned joint-cell divisibility, does
not delete balanced cells, and does not replace a whole-node current
by the current of a proper subcell. Those distinctions remain necessary
when studying the residual 215-tile layer.

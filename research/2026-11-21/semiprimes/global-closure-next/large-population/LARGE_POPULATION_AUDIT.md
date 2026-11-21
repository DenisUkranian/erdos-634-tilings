# Independent internal audit of the odd-branch budget

21 November 2026. This audit concerns the claims in
[GLOBAL_ODD_BRANCH_BUDGET.md](GLOBAL_ODD_BRANCH_BUDGET.md), not a
nonexistence theorem for 5063. Both original target counts remain open.

## Reviewed conclusion

The proof establishes the following necessary conditions at 5063:

1. An exterior-free odd exact node containing 86 positive tiles and no
   negative tiles requires at least 301 odd tiles globally. The analogous
   node containing 86 negative tiles requires at least 387 odd tiles.
2. If the entire height-one population is the native `zR` class with
   **86 positive and 43 negative** tiles, then the full tiling requires
   at least 387 odd tiles. The sign assumption is essential.
3. At total odd population 215, height-one population 129 is impossible.
   The remaining displayed five-block alternatives are not excluded.

I found no mathematical gap in these three deductions, conditional on
the explicitly cited earlier geometric and certificate inputs. This is
an internal review, not an independent proof-assistant formalization or
external peer review.

## 1. The one-sign 86-tile node

The reduction to one Euclidean class is valid without assuming unsigned
joint-cell divisibility. In a one-sign cell, population equals absolute
charge; signed cell divisibility makes it a positive multiple of 43.
The earlier line-incidence theorem excludes a monochromatic 43-tile
cell, so two cells cannot share the node's total population 86.

The terminal two-block balance theorem makes the node nonterminal.
For an occupied child subtree, physical bidirectional transport gives a
nonzero parent current. Every parent tile has the same sign, so this
current has that sign and its magnitude is the actual parent-gate tile
count. The gate capacity applies to the **whole** unique class, because
an odd short height carries no exterior side. It gives
`1 <= |Q| <= 16` for either hand and either sign.

For the even-root child subtree, the exact cut identity is
`Q=22e-43o`, so `Q=o (mod 22)`. Both charges are integers in units
of 43 because the whole subtree is exterior-free. No terminality of
that child is used.

The disjoint inventory argument is correct. With at most five odd
blocks and a positive two-block parent, the remaining inventory is
bounded by `(positive,negative)=(1,2)`. A child union cannot consist
of a single ordinary block; its possible signed charges are therefore
`o in {0,-1,-2}`. None has a representative in `[1,16]` modulo 22.
For a negative parent and at most seven blocks, the remaining inventory
is bounded by `(4,1)` and `o in {0,1,2,3,4}`. None has a representative
in `[-16,-1]`. The global odd-block parity gives the thresholds 7 and
9. The argument checks all charges below those thresholds, rather than
assuming a bounded height range or an arbitrary bound on `e`.

## 2. Transfer of the earlier finite-profile exclusion

The corrected hypothesis expressly states `G_1=43`, with signs `(86,43)`.
It is not inferred from `n_1=129` when other odd heights occur.

Every off-middle odd tile belongs to one upward or downward child
subtree of the native height-one class. The occupied-parent/ancestor
input excludes a different empty height-one ancestor. The two groups
are disjoint by physical height (`>=3` versus `<=-1`), so their charges
sum to zero. This use of both trees does not add overlapping populations.

For each even-root child subtree, retaining the exterior term gives

`Q=(d G_even-c G_odd-b(S))/c`.

Substitution of the even-core residue `d`, the native upper exterior
character `-(2c^2-d^2)`, and the native lower character `c^2` yields
exactly the two equations (7). If every off-middle odd subtree charge
is zero, these are the old integer gate equations. All other required
constraints transfer:

* 129 native height-one tiles, positive/negative populations 86 and 43;
* signed gate caps, aggregate positive/negative reserves, and integral
  neighboring charge variables;
* `sum e=0`, obtained by summing actual disjoint gate bins;
* zero periodic endpoint current, since there is no outer side of
  short height one and every complementary long side has length 43;
* every universal translated and dihedrally transformed column inequality.

Inspection of the existing enumerator shows that it uses those current
constraints. It does **not** use terminal branch populations, absence of
higher odd tiles, or whole-edge matching at zero-current gates. Thus
reusing its 65-certificate exclusion under the zero-subtree-charge
hypothesis is legitimate.

Nonzero balanced charges outside height one require at least four odd
blocks. At equality, they must be one `+2` two-block population and one
`-2` two-block population. Each contains a single odd exact node; its
physical height makes it exterior-free in the relevant outward tree.
The negative two-block node invokes the preceding 9-block theorem,
excluding the 7-block equality case. This gives the stated global
387-tile lower bound under the explicit native-layer hypothesis.

## 3. The five-block corollary

At `n_odd=215` and `n_1=129`, the existing five-block height theorem
leaves exactly one other odd height, -1 or 3, with 86 tiles. Its unique
outward exact node is exterior-free. Both monochromatic possibilities
are excluded by Section 1, so it is balanced and the height-one signs
are `(86,43)`.

The native phase still needs proof and is supplied in the note. Each
of the two odd heights lies entirely on one side of any actual upper
median path, by the two-block minimum on each side. Its lower-region
odd charge is consequently zero or 43, giving `t in {1,2}`. The exact
formula `K=(c-d)t-dj_0` rules out `K=0`, because `gcd(c,d)=1` and
`d=22` divides neither 1 nor 2. An actual height-two path step supplies
a height-one bank tile whose vertex lies in `zR`. Since the full
129-tile layer is a unique joint class, that one anchor proves the
native-class assertion for the entire layer. The previous conditional
387 bound then applies, contradicting 215.

## 4. Verification boundary

The geometric dependencies remain the published joint-cell, ordinary
node, physical-cut, gate-capacity, and median-path theorems, together
with the earlier exact 65-certificate finite proof. Arithmetic replay
can check the residues and finite inventories; it does not by itself
prove these geometric premises or decide any remaining five-block
alternative. The optional new replay must be read with that scope.

### Independent replay performed

I read `verify_odd_branch_budget.py` and independently ran it with Python
assertions enabled. It returned **PASS**. The first feasible arithmetic
block counts were 7 for the positive remote parent and 9 for the negative
remote parent. Its 3431 and 143 arithmetic controls retained possibilities
at five blocks, as required to avoid an unsupported transfer of the
5063 thresholds. The only zero-sum nonzero charge lists costing at most
four blocks were `(-2,+2)` and `(+2,-2)`.

The independent combinatorial count reproduced 34,672,599 profiles and
17,800,359 sign-reserve profiles. The script checked all 65 certificate
file hashes, the transformed-cut and enumerator hashes, and the saved
zero-survivor accounting. As its output correctly states, this short
replay **did not rerun** the earlier 1,442,220 individual column checks
or the complete C++ exhaustion; those are explicit existing dependencies.
The exact control output is [ODD_BRANCH_BUDGET_REPLAY.json](ODD_BRANCH_BUDGET_REPLAY.json).

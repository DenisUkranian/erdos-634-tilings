# Independent review of the exact 154 inventory dynamic program

7 October 2026. Separate internal mathematical and implementation review;
not external refereeing and not an exclusion of 154.

Reviewed:

* `../dual/INVENTORY_SUPPORT.md`;
* `../dual/check_inventory_supports.py`;
* the 75 exact-support records in `../dual/inventory_exact.json`.

**Outcome: PASS for the stated necessary inventory exclusions.** A small
endpoint sentence was corrected during review; it does not affect the
algorithm or the exclusions. The surviving formal inventories must not
be treated as geometric tilings.

## 1. The signature is necessary with T-junctions

Assign a directed edge of length ell, height h and rotation j the formal
quantity `ell*(-1)^j*X^h`. Reversal adds three to j and negates this value.
Splitting an edge into collinear atoms preserves it by length additivity.
Thus the signature cancels on every internal contact, with no edge-to-edge
assumption.

The reference triangle with counterclockwise vertices `0,8,8+7rho` has
boundary vectors `8,7rho,-13z`. Its signature is `P=1-13X`.
The reflected triangle, ordered counterclockwise, has signature
`-Q=-1+13X^(-1)`. Its opposite rotations supply the other two signs.
The actual target boundary vectors are

    154, 91*rho^2*z, -91*rho*z^(-1),

giving `F=154+91X+91X^(-1)`. Hence `PU+QV=F` is necessary and the stated
four unsigned groups cover all twelve rigid orientations at each height.

## 2. Completeness of the integer W parametrization

The displayed particular solution directly expands to F. Subtract it.
Over the rational Laurent polynomial ring, `P` and `Q` have different
roots, respectively 1/13 and 13, and are coprime. Therefore every
homogeneous solution has `Delta U=QW`, `Delta V=-PW` for a rational
Laurent polynomial W. Both P and Q are primitive integer Laurent
polynomials. Clearing Laurent monomials and applying Gauss's lemma makes
W integral. Conversely each integer W gives an integer solution.
The coefficient formulas used in the program are precisely these two
products.

For the least occupied W index q, `U_(q-1)=-13W_q`, apart from the
possible particular term -8 at q=1, which cannot cancel a nonzero
integer multiple of 13. Thus q>=L+1, giving W_(L-1)=W_L=0.
For a greatest W index q>=U, one has q>=0 because U>=0. The only possible
particular term in `V_(q+1)` is then -13 when q=0. This proves exactly
`W_U=0` for U>=1, `W_0=1` for U=0, and vanishing of every W above U.
The qualification q>=U avoids an irrelevant exceptional term at q=-1;
that term has no bearing on the endpoint conclusion.

Let M=max|W_h| and choose q attaining it. Then

    |U_(q-1)| >= 13M-M-8 = 12M-8.

Every coefficient |U_h| is bounded by its population and hence by 154,
even if h is outside the support (where it is zero). Therefore M<=13.
The checker's range [-13,13] is complete, not a search cutoff.

## 3. Population cost and padding are exact for these constraints

For given U,V, four nonnegative group counts with total n exist exactly
when `n>=|U|+|V|` and `n=U+V mod2`. The absolute values supply minimal
counts; any permitted excess is supplied by opposite-sign pairs.
The program rounds upward to the required positive population residue
modulo 13 and then adds 13 if needed to fix parity. This is the least
possible population at that height.

At height zero the required residue is 11; every other occupied height
has positive population divisible by 13. Summed populations thus have
residue 11 modulo 13. Evaluation of the Laurent identity at X=1 gives
`sum(U_h+V_h)=-28`, so their sum is even. Every total cost at most 154
therefore differs from 154 by a nonnegative multiple of 26. Adding this
difference at height zero preserves all signed counts, congruences and
the exact occupied support. Consequently a retained path really gives
an inventory of exactly 154, not merely a lower-area candidate.

## 4. Exhaustion and independent implementation

The program state is the pair `(W_(h-1),W_h)`. Its future costs depend
only on that pair and later W values. Keeping the least accumulated cost
at each state therefore discards no possible feasible continuation.
All costs are nonnegative, so discarding partial costs above 154 is safe.
The terminal rules are the endpoint conditions proved above.

An independent implementation ran the dynamic program **backward**, from
`(W_U,W_(U+1))=(1[U=0],0)` down to `(W_(L-1),W_L)=(0,0)`. It enumerated
the possible positive populations directly in steps of 13 and checked
parity, rather than using the producer's ceiling formula. On all 75
supports it obtained the identical status and, for each survivor, the
identical minimum total cost. The independent run evaluated 19,008 cached
integer local costs.

Result:

* all twelve width-11 intervals are excluded;
* the three width-10 intervals `[-9,1]`, `[-5,5]`, `[-1,9]` are excluded;
* each of the other sixty intervals has a formal witness.

Combined with the separately reviewed contiguous-support theorem and the
two-height obstruction, a 154 tiling therefore has height span between
2 and 10 and one of the sixty surviving exact intervals.

## 5. Safe use in geometric search

These are necessary conditions for a **completed** tiling. A partial
placement cannot generally be rejected because its current exact support
fails an exact-support test: future tiles may enlarge it. The simple
consequences here are safe: span exceeding 10 is impossible, and a hull
containing mandatory height zero that already equals one of the three
excluded width-10 intervals cannot be repaired by enlargement, since that
would exceed span 10. More general support filtering must allow every
compatible completion interval.

No claim is made that the current matrix is totally unimodular, that
formal inventories determine placements, or that all three-or-more-height
geometric cases are excluded.

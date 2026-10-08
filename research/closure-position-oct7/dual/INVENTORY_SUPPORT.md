# Exact finite inventory exclusions for the 154 candidate

7 October 2026. This does not decide whether 154 is realizable.

Assume an actual tiling of the triangle `(91,91,154)` by `(8,7,13)`.
Use `rho=exp(i*pi/3)`, `Z=8+7*rho`, and `z=Z/13`. A tile's short-edge
height is the exponent of z, modulo rotations by 60 degrees. This note
combines the existing height-population congruences with the complete
alternating signed chirality inventory. It does not retain positions.

## Laurent equation

For a directed edge of height h and rotation j, assign
`length*(-1)^j X^h`. Counterclockwise boundaries cancel on every atomic
contact, including T-junctions.

The reference counterclockwise tile `R=(0,8,Z)` has signature
`P=1-13X`. The counterclockwise reflected tile has signature
`-Q=-1+13X^(-1)`. Define U_h as the even-minus-odd rotation count of R,
and V_h as the odd-minus-even rotation count of the reflected tile.
Write U,V for their Laurent polynomials. The counterclockwise target
boundary has signature

    F = 154 + 91X + 91X^(-1),

because its directions are `(h,j)=(0,0),(1,2),(-1,4)`.
Consequently every tiling satisfies

    (1-13X)U + (1-13X^(-1))V = F.                    (1)

A particular integer solution is

    U*=-8,   V*=-7-13X.

The factors P and Q are coprime over the rational Laurent polynomial
ring: their distinct roots are 1/13 and 13. They are primitive integer
Laurent polynomials. Euclid's lemma followed by Gauss's lemma therefore
shows that every integer Laurent solution is uniquely of the form

    U = U* + QW,    V = V* - PW,                     (2)

where W is an integer Laurent polynomial. In coefficients this reads

    U_h = -8[ h=0 ] + W_h - 13W_(h+1),
    V_h = -7[ h=0 ] - 13[ h=1 ] - W_h + 13W_(h-1).  (3)

## Exact population cost

For prescribed signed counts U_h,V_h, an unsigned population n_h is
possible as a formal inventory exactly when

    n_h >= |U_h|+|V_h|,     n_h = U_h+V_h (mod 2).

Necessity follows by separating positive and negative counts.
Sufficiency follows by using `|U_h|` and `|V_h|` tiles with the stated
signs and adding pairs of opposite rotations to absorb the even excess.
This is sufficiency only for an inventory, not a geometric arrangement.

The existing height theorem adds

    n_0 = 11 (mod 13),     n_h = 0 (mod 13), h != 0.

For an occupied height require n_h>0. Let C_h(p,w,q) be the least positive
n_h meeting these congruences and the absolute-value bound when
`(W_(h-1),W_h,W_(h+1))=(p,w,q)`. The checker computes this integer directly:
round the absolute-value bound upward to the required residue modulo 13,
then add 13 if necessary to obtain the required parity.

## Complete finite bounds for W

Suppose all occupied heights are exactly the interval [L,U], where L<=0<=U.
Outside that interval the signed counts vanish.

If q is the least nonzero W index, U_(q-1)=-13W_q unless q-1=0, in
which case it is -8-13W_q and still nonzero. Hence q>=L+1, and

    W_h=0 for h<=L.

If the greatest nonzero W index q satisfies q>=U (and hence q>=0),
then V_(q+1)=13W_q, except at q=0, where V_1=-13+13W_0 can cancel.
It follows that

    W_h=0 for h>U;
    W_U=0 if U>=1;
    W_0=1 if U=0.

The last condition cancels the particular solution's V_1 outside the
support. The identically zero W also fits the stated conditions whenever
it can fit the interval; no nonzero endpoint is assumed by the checker.

Finally set M=max|W_h|. If M>0 and |W_q|=M, (3) gives

    |U_(q-1)| >= 13M-M-8 = 12M-8.

Since `|U_(q-1)|<=154`, one obtains M<=13. Thus every genuine solution
is represented by integer W_h in the finite range [-13,13]. This bound
uses only necessity and is deliberately loose.

## Exhaustive integer dynamic program

The state before processing height h is `(W_(h-1),W_h)` and the least
population cost through h-1. Start at `(0,0)` at h=L. Try every integer
W_(h+1) from -13 through 13, add `C_h`, and retain the least cost for each
new state. Discard costs greater than 154. At the final height impose the
upper endpoint conditions just proved. This exhausts all possible W;
discarding a more expensive path to the same state is valid because all
future costs depend only on that state and later W values.

Conversely every retained path gives a formal inventory with the
specified support. Its minimum cost has residue 11 modulo 13. Evaluating
(1) at X=1 gives `sum_h(U_h+V_h)=-28`, so its cost is even. Its deficit
from 154 is therefore a nonnegative multiple of 26. Add that deficit
at height zero as opposite-rotation pairs. The resulting formal inventory
has exactly 154 tiles and passes every condition used here. The program
independently replays all coefficients and population conditions of each
such witness using integers.

## Result

For the 75 intervals containing zero of lengths 3 through 12, the exact
dynamic program excludes precisely these 15:

* every interval of length 12;
* the intervals `[-9,1]`, `[-5,5]`, and `[-1,9]` of length 11.

Each of the remaining 60 intervals has an explicit, exactly replayed
formal inventory in `inventory_exact.json`. Therefore these particular
inventory conditions cannot reduce the remaining problem to two or three
heights. The witnesses are not tilings and do not refute any stronger
position-sensitive obstruction.

If combined with the separately proved fact that below c^2=169 the
occupied heights form an interval, and the existing population bound of
at most 12 occupied heights, this improves the bound for the 154 candidate
to at most 11 occupied heights and a height span of at most 10. It still
leaves 60 possible intervals after the two-height exclusions. The
interval/no-gap theorem is an external dependency of that geometric
conclusion, not a lemma proved in this note.

Reproduce with:

```sh
python research/closure-position-oct7/dual/check_inventory_supports.py
```

The auxiliary SciPy MILP independently finds the same 60 witnesses and
flags the same 15 exclusions, but solver infeasibility messages are not
used as proof. The integer dynamic program supplies the exhaustive check.

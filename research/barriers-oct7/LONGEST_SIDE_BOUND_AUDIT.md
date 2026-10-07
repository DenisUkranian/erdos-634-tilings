# Audit of the proposed longest-side-square bound

7 October 2026. This note does not prove the conjectured bound and does
not use it as a necessary condition in the classification.

The proposed statement is that a nonsimilar triangular tiling by a
primitive nonright integer-sided tile, with irrational angles in the
sense of the classification, must have N at least the square of its
longest side. Here c is the longest side in the plus-norm and Group-1
families. It is not necessarily the longest side in the minus-norm or
double-angle parametrizations.

## 1. It cannot remove any F3 arithmetic candidate

For the plus norm c^2=a^2+ab+b^2 the following exact identities hold:

    (a+2b)(2a+b) - c^2 = a^2+4ab+b^2,
    3(a+b)(a+2b) - c^2 = 2a^2+8ab+5b^2,
    (2a+b)(a+b) - c^2 = a^2+2ab.

Every right-hand side is strictly positive for positive a,b. Therefore
all necessary F2, F3 and F4 counts Dm^2 already exceed c^2 for every
positive integer m. Even a complete proof of the proposed geometric
bound would remove **no candidate in these rows**. In particular it
would not decide 4830 or any member of the squarefree primitive F3
frontier merely by this inequality.

At primitive scale the potentially relevant plus-norm differences are

    b(a+b)-c^2 = -a^2,
    b(a+2b)-c^2 = b^2-a^2,
    ab-c^2 = -a^2-b^2.

Thus a proof would exclude primitive F1 and equilateral targets and
I120 targets with a>b. It would in particular exclude the (8,7,13)
I120 candidate for N=154, since 154<169. These are **conditional
consequences**, not established nonexistence results.

## 2. Why scanning the known constructions is weak evidence

The known W semigroup starts at m=v for tile
(a,b,c)=(uv,v^2-u^2,v^2). Already at that scale

    N-c^2=(2v^2-u^2)v^2-v^4=v^2(v^2-u^2)>0.

Increasing m only increases N. The QP construction also automatically
exceeds c^2, since

    (2v^2-u^2)(3v^2-u^2)>2v^4>v^4.

The F2/F3/F4 identities above handle all their constructive subdomains,
including the staircase and nested-corner results, without checking a
single certificate. Several other construction recipes literally
contain a c-fold copy of the original tile, giving c^2 unit tiles in
that block alone. Such recipes cannot test whether all arbitrary
triangular tilings must satisfy the same lower bound.

No counterexample to the proposed statement was established by this
audit. This is not positive evidence strong enough to use it as a
lemma, and it is not an exhaustive scan of all possible tilings.

## 3. The existing area-cut proof has index c, not c^2

For a plus-norm tile use rho=exp(i*pi/3), Z=a+b*rho and z=Z/c.
At a median cut separating short-edge heights, the selected whole-long
edge vectors belong, after rotation, to the lattice

    M=c Z[rho]+Z Z[rho].

In the basis (1,rho), generators are the columns

    (c,0), (0,c), (a,b), (-b,a+b).

The gcd of all two-by-two minors is exactly c. Indeed they are c^2,
cb, c(a+b), -ca, cb and c^2 up to signs, and primitivity gives

    gcd(c,a,b)=1.

Thus the area argument supplies divisibility by c for a closed cut,
not by c^2. Replacing this lattice by c Z[rho] silently deletes the
allowed long edges in the adjacent direction class and is invalid.

For a pure all-long-edge island the stronger c^2 divisibility comes
from a single boundary direction class. The boundary of a general
mixed-height cut can contain the two adjacent classes. Nor does a
boundary-attached region meet the pure-island hypotheses. One therefore
cannot import the pure-island 2c^2 lower bound or the small-balanced-
polygon 2c rigidity theorem into the full triangular target without a
new extraction argument.

## 4. Status

The proposed bound remains unproved. It is not used to label 154,
W56, or any other surviving candidate impossible. Even if proved it
would leave the entire F3 frontier untouched, so it would be a partial
obstruction rather than a complete classification theorem.

Dependencies used here are the count formulas in
../../docs/global-gap-2026-10-07.md, the whole-edge lattice computation
in ../../research/f3-descent-attempt/SMALL_POLYGONS.md, and the W seeds
in ../w-beta-caps/PROOF.md. All displayed comparisons and lattice minors
are direct integer identities; no literature claim of the proposed
bound is being made.

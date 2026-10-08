# Independent arithmetic review of the extended F3 cone

The current `global/F3_UNIFORM_CONE.md` and its source checker were reviewed
independently of their author. No gap was found in the arithmetic argument.

For both possible orders of the coprime norm parametrization, the stated
identities for `t=p/q` give `p<(8/5)sqrt(b)`. Together with the exact Frobenius
formula this gives `F<(44/5)b^(3/2)`. The stated lower bound on `D-c` exceeds
this bound for every `b>=22500`, and monotonicity of the comparison function
is immediate. For `b<22500`, the strict parameter bound implies `p<240`,
so the finite enumeration `2<=p<=239,1<=q<p` is complete. The factor-three
normalization and the positive reduction proof of the Apéry formula were
also checked in their cited source.

All 710 positive certificates were independently checked by substitution.
The endpoint obstruction was independently verified by shortest paths in
the 1139 residue classes, using edges of weights 2725 and 3439. This checks
the minimum representative without using the Apéry formula. For the residue
of 75807 the minimum is 130479, confirming nonmembership.

Run `python3 research/universal-closure-oct8/e135/check_f3_endpoint_independent.py`.
The report is `f3_endpoint_independent_verified.json`. This audit concerns
the arithmetic sufficient criterion; the mixed-corner geometric construction
has its own proof and checks.

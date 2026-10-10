# Proof audit / self-check ledger

This is a separate written self-audit, not external or independently staffed
review. 9 October 2026.

## Coverage and dependencies

- **Nine versus thirteen rows:** addressed in PROOF Section 2. When d is odd,
  an existing theta tail settles the density. When d is even, even multipliers
  have their existing tail. In the remaining odd sector, W/beta/classical
  candidates force one of the easy cofinal conditions; theta/double-angle have
  the wrong 2-adic valuation. No row is silently discarded.
- **Conditional source chain:** the result uses the existing exhaustive
  classification, integer residual scale proofs, and genuine every-integer
  tails. These old universal geometric arguments were not all independently
  re-proved in this session. The candidate all-primes proof and disputed
  small W/beta extraction are not used.
- **Old versus new:** the cofinal arithmetic test already existed. The new
  claims are all-branch effective density and the positive-density complement,
  not a new discovery of that test or a better F3 power-saving exponent.

## Arithmetic pitfalls checked

- **F3 factor three:** both 3|d and 3 not dividing d are handled. In the latter
  case 3|s and the product kernel is 3d after writing s=3k. Using d/3 there
  would have been an error. The regression tests cover both cases.
- **F2 coprimality:** the gcd dividing 3 is excluded by the plus-norm equation
  modulo 9, not assumed from gcd(a,b)=1 alone.
- **Factor squares may share primes with the kernel:** the allocation
  L_i=d_i x_i² does not assume gcd(d_i,x_i)=1. The divisor inequality used
  does not require that extra coprimality.
- **Unbounded other short side when one is fixed:** counted by the exact
  positive-divisor identities; no bounding-box enumeration was used as an
  infinite proof or as a complete fixed-factor test.
- **Pell orbits:** assigning an element to an ideal does not make that
  assignment injective. The compact real intervals and the explicit minimum
  norm-one unit gaps bound the multiplicity by one. Ideal norm, not
  the norm of a rational integer's principal ideal, is used correctly.
- **Class number:** no class-number-one assumption is needed. Counting all
  integral ideals is an upper bound for the principal ideals that occur.
- **Ordered a,b:** the a+b fixed-factor bound uses
  `(2c-(a-b))(2c+(a-b))=3(a+b)^2` and retains both ordered divisor pairs,
  including a-b<0. It is not a Pell equation with a spurious coefficient
  three on (a-b)^2. The checker now tests this identity explicitly.
- **Reciprocal tail:** the integral has the factor two from u=sqrt(t), and
  P_4 has coefficients 1,4,12,24,24. The count is of distinct s bounded by
  the count of witnesses, never the reverse inequality.

## Density and geometry pitfalls checked

- **Relative odd density:** a finite odd divisibility generator has density
  1/s relative to odd integers. The tail's sharp density bound uses a second
  finite truncation before passing to infinity; simply dividing a uniform
  integer count by X/2 would otherwise introduce a factor two.
- **Coefficient is not a scale-one construction:** equality with the actual
  density uses only finite tail exceptions for finitely many retained
  coefficients and a summable remaining tail. No single exceptional count
  is reclassified on that argument.
- **Correlation:** different divisibility events are not independent.
  Section 6 proves the required positive association on independent prime
  valuations. The infinite product is a lower bound for the complement,
  not an asserted exact formula for its density.
- **Positive density is within a square class:** the normalizing variable
  is m. No claim of positive density among all tile counts N follows.
- **Effective versus efficient:** the constants and termination are explicit,
  but the requested cutoff may be huge. No numerical decimal for an infinite
  density is presented as certified merely from a finite lower estimate.

## Actual arithmetic results

The final replay checks 1539 forward/inverse witnesses, including every row;
2100 complete fixed-factor tests (seven kinds, L=1,...,300); 3000 divisor
majorant tests; and seven exact-period/correlation tests. All passed.

It completely enumerates coefficient multipliers at odd s<=3000 in classes
22,38,78,110,1302. Only class 110 contributes in that range: s=3, tile
(8,7,13), row F3, coefficient 990. Its finite union density is exactly 1/3.
The empty lists for other classes are strictly finite statements, not
infinite exclusions. In particular the pre-existing theorem gives actual
odd class-38 tilings beyond such finite search limits.

No full geometry search, new geometric certificate, formal proof assistant,
or external mathematical reviewer was run for this package.

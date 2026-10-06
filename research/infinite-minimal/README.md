# Finite arithmetic audit for infinitely many minimal multipliers

This package checks the explicit elliptic-orbit arithmetic used in
[the square-class-38 proof](../../docs/infinite-minimal-multipliers.md).
It uses only Python standard-library integer and `Fraction` arithmetic,
and imports no tiling construction or author-supplied arithmetic module.

From the repository root:

```sh
python research/infinite-minimal/verify_orbit.py
```

The default invocation is read-only. To regenerate the committed report:

```sh
python research/infinite-minimal/verify_orbit.py --report research/infinite-minimal/verification.json
```

The program refuses `-O`/`-OO`, because its checks use assertions.

For the curves

\[
E:Y^2=X^3+114^3,\qquad F:y^2=x^3+684x^2-38988x,
\]

it independently implements the group law and the displayed isogeny maps.
It checks:

- Curve membership of \(Q=(-110,388)\) and \(G=(54,216)\), the map signs,
  and the exceptional kernel points.
- \(\widehat\phi(-nG)=nQ\), both composition identities, and the rational
  square lift for every \(1\le n\le15\).
- Exact reduced-coordinate normalization and the multiplier
  \(s=3WC/\gcd(114,A)\); positive primitive F3 triples at indices
  \(7,9,10,12\).
- The local valuation implications at \(2,3,19\) and a finite set of
  additional primes, whenever the sampled point meets the specified
  neighborhood conditions.
- The complete small inverse checks for multipliers 1 and 3, the
  quadratic nonresidues 2 and 3 modulo 19, the alpha residue implication,
  and the arithmetic in the stated Lutz–Nagell certificate.

[verification.json](verification.json) contains compact counts and
valuation data, with a digest of the exact sample data rather than long
coordinate streams. The examples are regression checks, not the logical
basis of the infinitude theorem. In particular, this program does not
prove density of an elliptic orbit, simultaneous local avoidance, the
exhaustive geometric classification, or the existing F3 tiling tail. Those
arguments and dependencies are stated in the proof document. It neither
constructs a geometric tiling nor solves all of Erdős problem 634.

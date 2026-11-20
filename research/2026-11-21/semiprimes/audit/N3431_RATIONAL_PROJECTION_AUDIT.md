# Independent review of the rational 3431 projection witness

21 November 2026. I reviewed `../global-invariant/N3431_PROFILE_LIMIT.md`
and `verify_3431_rational_projection.py`, and independently replayed the
checker. The exact feasibility conclusion for the stated fractional
periodic model is sound. It proves neither a physical tiling nor
feasibility with integer individual tile multiplicities.

## Fourier range and normalization

The endpoint-column signs agree with the CCW short-edge convention.
Under the unitary two-coordinate transform, translating an endpoint by
`u` multiplies its coefficient by `zeta^(k dot u)`, giving the displayed
block entries. A one-coordinate gate transform produces a factor
`sqrt(c)` relative to the normalized input; dividing that output by
`sqrt(c)` produces the saved gate row. At frequency zero, the physical
gate totals and total population must all be divided by `c`, as stated.

Exactly the endpoint modes `k dot U_axis=0` are identically zero.
They account for `3c=111` omitted rows. Their target entries vanish.
Every other row belongs to one of the 1,369 supplied blocks. The
verified invertibility of each block Gram matrix establishes full row
rank for these blocks, not full row rank for the original redundant
matrix. Therefore the target belongs to the image of that original
matrix; this also places the correction residual in its image.

## Exact inverse bound

The rational Machin and Taylor estimates correctly enclose every root
component. Each endpoint block entry involves at most one root
difference, because the two short-edge axes of a tile are distinct.
Its coordinatewise absolute-sum error is at most `2/Q`, and both exact
and approximate entries have absolute-sum size below three. Twelve
products therefore contribute less than `200/Q` error to a Gram entry.
The saved integer residual estimate includes that entire error.

The Neumann-series calculation with residual norm below one half gives
the asserted inverse infinity-norm bound. Passing from this bound to
the spectral bound is legitimate because the exact inverse Gram matrix
is Hermitian. The output scalings all contract the original residual
norm. Thus the least-norm correction for the unscaled original matrix
satisfies `||M^dagger r||_2^2 <= 3||r||_2^2`.

The Moore--Penrose inverse of a rational matrix is rational: the
displayed full-rank rational factorization proves this directly. Taking
the real part of a Fourier solution, if needed, preserves the real
equations and cannot increase its norm. The explicit witness formula
therefore defines a rational real solution rather than only a complex
or approximate one.

## Positivity and capacities

The replay checked all 16,428 rational approximate coordinates and all
4,182 unscaled equations exactly. Its residual squared numerator is
988,020 and its minimum coordinate numerator is 346,672,370, with
point denominator `10^12`. The strict bound
`3*988020 < 346672370^2` proves positivity after correction.

Each positive gate bin contains `3c=111` variables. Bounding its change
by `111||M^dagger r||_2` is conservative and valid. The exact remaining
slack establishes every corrected positive gate population below 44.
The corrected population and signed gate sum give sign masses 74 and
37, and native charge units -2 and 2, with all remote currents zero.

The replay returned `K=3`, with block row counts 108 of size two,
1,189 of size three, and 72 of size four. Its certificate SHA-256 is
`1990dc1bc01af53e9e03b6d3e88621c5ff58b5da5af48944846a6e33087d04a1`.

Consequently additional valid linear dual cuts from this same full
periodic relaxation cannot exclude the displayed 3431 profile. The
conclusion does not apply to stronger conditions retaining real
supporting lines, integer individual tile counts, physical matching,
or nonoverlap. The note preserves these distinctions explicitly.

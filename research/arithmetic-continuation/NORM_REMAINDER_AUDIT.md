# Independent internal audit of the norm-family remainder estimate

6 October 2026. This is a project-internal mathematical and implementation
audit, not external refereeing or a proof-assistant verification.

**Conclusion:** the proof of `U_norm(X)=O(sqrt X)` in
[`NORM_GEOMETRIC_REMAINDER.md`](NORM_GEOMETRIC_REMAINDER.md) is sound,
conditional on its explicitly identified, already established constructive
tails. It counts subthreshold representations and their distinct counts;
it does not decide which members of that remainder admit tilings.

The seven thresholds were checked against Appendix A of
`docs/square-class-tails.md`. In particular F2 and F3 use `ceil(M/2)`,
while F4 still uses `M`; both ordered side assignments are retained.

The parameter estimates and the summation limits were independently
rederived as follows.

* With `h/k=(c-a)/b`, the plus-norm equation gives
  `a/b=(k²-h²)/(k(2h-k))`. Reduced positive parameters have `k/2<h<k`.
  Coprimality of h,k implies the gcd of the two numerators divides 3;
  the same divisor divides the c numerator. Thus the stated primitive
  formulas with `g in {1,3}` are correct and their reduced parameter is
  unique.
* For `d=k-h`, `e=2h-k`, and `delta=min(d,e)`, both side lengths lie
  between `k delta/g` and `k²/g`. Also
  `ab=kde(2k-d)/g² >= k³ delta/27` because
  `max(d,e)>=k/3`. At most two choices of (d,e) correspond to each
  fixed (k,delta). All positive parameters have k>=3.
* Every listed plus-row coefficient is at least ab, and all its
  sufficient thresholds are at most `3R+6<=9R`. The strict cutoff
  `t<T` therefore gives `delta*t<9k`, while `Dt²<=X` gives
  `delta*t²*k³<=27X`. The script implements the strict scale cutoff
  by `T-1` and the inclusive count cutoff by `isqrt(X//D)`.
* After ordering a>b, the minus-norm substitution `(A,B)=(a-b,b)`
  is one-to-one onto positive ordered primitive plus-norm pairs.
  Restoring the two original side orders accounts for precisely a
  factor two. Its coefficient `B(A+B)` is at least AB, and its
  threshold is at most `9R_plus`. Equality a=b contributes only the
  explicitly removed classical tile (1,1,1).
* For fixed t, the resulting sum over k is bounded by
  `2 sum min(9k/t,27X/(t²k³))`. Splitting at
  `K=(3X/t)^(1/4)` gives `O(sqrt X/t^(3/2))` with an absolute
  constant. The restriction `t<=sqrt X` follows from D>=1 and
  ensures K>=1 for X>=1. Extending the final t-sum to infinity is
  valid because its terms are nonnegative and `sum t^(-3/2)`
  converges.

## Implementation checks

`check_norm_remainder.py` now explicitly refuses optimized execution,
supports an optional `--report PATH`, and reports `full_solution: false`
and the compatible `full_Erdos634_solved: false`.
By default it writes only standard output. The frozen
[`norm-remainder-verification.json`](norm-remainder-verification.json)
was regenerated with this script; its numerical counts are unchanged.

In addition to the retained parameter regression through side bound 200,
an independent direct enumeration tested every positive coprime ordered
pair with `ab<=X`, checking the integer squares `a²+ab+b²` and
`a²-ab+b²` directly. It used none of the h/k parametrization or its
k-bound. All seven row counts and the distinct-count unions agreed:

| X | Subthreshold representations | Distinct counts |
|---:|---:|---:|
| 1,000 | 162 | 76 |
| 10,000 | 689 | 333 |

The default script output was checked byte-for-byte against the refreshed
frozen report. An actual `python -O` invocation exited unsuccessfully
with the required assertion-dependency message.

These finite checks test the implementation and the enumeration bounds.
The asymptotic conclusion rests on the written universal estimates above.

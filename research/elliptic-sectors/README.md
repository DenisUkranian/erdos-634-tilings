# Elliptic square classes and an exact class-number sector

The [main proof](../../docs/elliptic-square-classes.md) proves the F3
coefficient/rank equivalence and an exact odd-multiplier theorem. The
[odd-F3 theorem](../../docs/f3-odd-multipliers.md) identifies the additional
local condition on a full Mordell–Weil basis. The
[alpha correspondence](../../docs/alpha-congruent-numbers.md) connects that
branch to the classical congruent-number curve.

These are statements about whole parameter families. They do not settle
all small geometric scales or the full Erdős problem 634.

## Exact sector classifier

```bash
python research/elliptic-sectors/sector.py 22 1 2 248599631
```

For odd `m`, the tool certifies the hypotheses

- `d` positive squarefree and `d = 22 mod 48`;
- `3` does not divide the imaginary quadratic class number `h(-4d)`;
- the finite necessary alpha-allocation sieve is empty.

It then returns `YES` or `NO` using complete QP prime allocation. Its
class-number certificate lists every primitive reduced binary quadratic
form, with the complete bound `a <= sqrt(4d/3)`. The implication to elliptic
rank zero uses the cited Stoll theorem as stated by Chang; software does
not prove that external theorem.

For even `m`, the tool tests for an existing oriented F4 coefficient `4d`
with `a < b`. A seed gives `YES` by the previously proved construction.
Every failure of these sufficient scope tests returns `NOT_COVERED`, never
`NO`. A class number divisible by 3 does not prove positive rank; a surviving
alpha allocation does not prove an alpha tiling. In particular, the old
unresolved `(d,m)=(110,3)` is not excluded.

The large class-22 positive multiplier is a regression for an old example,
not a new count claim. Trial division and form enumeration are exact but
not optimized for arbitrarily large input.

## Constructive elliptic arithmetic

`elliptic.py` provides exact `Fraction` arithmetic on `E_K: Y²=X³+K³`:

- `forward_f3(d,a,b,c)` and `reverse_f3(d,point)` implement the proved
  correspondence, including primitive normalization.
- `f3_from_generator(d,point,max_steps)` examines successive even multiples
  of a supplied rational non-torsion point. Success returns a coefficient
  witness; exhaustion returns `INCOMPLETE`, not a nonexistence verdict.
- `dual_isogeny(K,point)` checks the map from
  `y²=x³+6Kx²−3K²x` to `E_K`.

No general rank algorithm, Mordell–Weil basis computation, or geometric
small-scale search is implemented here. A coefficient witness only gives
actual tilings after applying an existing sufficient construction.

## Verification

```bash
python research/elliptic-sectors/run_checks.py
python research/elliptic-sectors/check_alpha_maps.py
```

Use ordinary Python 3.11+, without optimization. Checks are read-only
unless `--report FILE` is explicitly supplied to `run_checks.py`.
[verification.json](verification.json) retains the finite report.

The tests compare complete reduced-form sets with a separately ordered
enumeration, check elliptic maps and primitive round trips, compare QP
inversion with independently bounded forward enumeration, retain alpha
witnesses divisible by 3, and compare with the prior complete class-22
classifier. Scope controls reject false exclusions outside the theorem.
The alpha checker verifies rational-function identities by coefficient
arithmetic. These finite checks complement the universal written proofs;
they are not external refereeing or proof-assistant formalization.

Primary references and exactly inspected source boundaries are retained
in [sources.json](sources.json).

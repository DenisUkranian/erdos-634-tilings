# Finite tests for square-class tails and prime-power rays

The [proof and source ledger](../../docs/square-class-tails.md) give two finite arithmetic criteria for Erdős 634:

- whether every sufficiently large multiplier in a square class `d*m²` is admissible;
- whether an odd-prime-power ray `d*q^(2k)` contains any admissible count.

Here `d` is positive and squarefree, and `q` is an odd prime. The first criterion includes all odd `d` by the earlier theta construction. The new finite reduction concerns even `d`. These tests do not classify arbitrary individual tile counts.

## Use

From the repository root, with Python 3.11 or newer and no third-party dependencies:

```bash
python research/square-class-tails/classify.py 14 22 70
python research/square-class-tails/classify.py 22 --prime 3
python research/square-class-tails/classify.py 14 --prime 7
```

| Output | Exact meaning |
|---|---|
| `COFINITE_TAIL` | Every multiplier at or above the displayed sufficient bound has a construction. The bound is not claimed minimal. |
| `NOT_COFINITE` | Infinitely many odd multipliers fail. In particular, all prime-power multipliers with base `q>2d` fail. Other individual composite multipliers are not decided. |
| `EMPTY_RAY` | No exponent `k>=0` on this specified odd-prime-power ray is admissible. |
| `NONEMPTY_RAY` | All exponents at or above the displayed sufficient bound are admissible. Earlier exponents are not classified by this output. |

The program returns primitive coefficient witnesses and sufficient construction thresholds. It does not generate new geometric coordinate certificates; their correctness uses the cited, previously proved constructions. The implementation uses exact integer factorization and square tests. Trial division terminates but can be slow for large inputs.

## Reproduce the finite checks

```bash
python research/square-class-tails/run_checks.py
python research/square-class-tails/verify_22.py
```

Ordinary verification is read-only. Both commands accept `--report PATH` to save a new report and reject optimized Python because their checks use assertions. `classify.py` uses explicit validation and runtime checks.

`run_checks.py` compares the production inverse-factor enumerator with a separately written forward Group-1 and conic-parameter enumerator on coefficients through 5000. It also checks exceptional kernels, representative positive outputs, invalid-input rejection, and the implementation of the class-22 ray exclusion. The report is [verification.json](verification.json).

`verify_22.py` independently checks all nine product rows at the 17 coefficients `22*s²` with `s=1` or an odd prime power below 44. It finds no witnesses, using two independent enumerations. Their explicit completeness bounds and the old positive witness's arithmetic are recorded in [verified22.json](verified22.json).

The infinite theorem has a written proof. The exclusion of **every** `22*q^(2k)` for odd prime `q` also has a direct short proof, so it does not depend on extrapolating these finite checks. The previously certified positive count at multiplier `248599631=7*3089*11497` is compatible with the exclusion: its multiplier has several distinct prime factors.

Separate internal proof and implementation reviews found no gaps. This is not external refereeing or a proof-assistant formalization. Full Erdős 634 remains unresolved.

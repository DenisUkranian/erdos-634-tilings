# Composite multipliers, fixed prime support, and the complete class 22

Read the [fixed-support theorem](../../docs/fixed-prime-support.md) and the
[complete square-class-22 criterion](../../docs/square-class-22.md).
The unrestricted Erdős problem 634 remains open in this work.

## Complete classification of the square class 22

```bash
python research/composite-support/classify22.py 1 2 21 27 248599631
```

For every positive multiplier `m`, this returns `YES` or `NO` for `22*m*m`.
Even multipliers use the previously published 88-tile F4 construction and
quadratic refinement. Odd multipliers use an exhaustive allocation of prime
powers and the exact QP inverse-square tests. A `YES` includes the primitive
tile and target parameters. The exclusion of the remaining F3 row uses the
elliptic rank-zero input proved/cited in the note; this is not a finite scan
standing in for that theorem. The large positive example was already known
in the uniform-sectors package and is not a new count here.

## Other even nonsaturated kernels

```bash
python research/composite-support/allocate.py 110 3
```

This separate tool requires even squarefree `d` failing the previous cofinal
tail test, and positive odd `m`. It enumerates `s|m`, assigns each full prime
power of `D=d*s*s` to one of two coprime factors, and inverts all nine product
rows. In F3 it first removes the coefficient's factor 3. No parameter-height
cutoff or refactorization of the potentially much larger `D` is used.

- `YES`: an existing construction applies at the actual multiplier.
- `NO`: the exhaustive coefficient list is empty.
- `UNKNOWN`: coefficient witnesses remain below their sufficient geometric
  thresholds. This does not assert nonexistence.

For example, `(d,m)=(110,3)` is retained as `UNKNOWN`; the code does not turn
the new class-22 argument into an unsupported claim about other kernels.

Trial division factors the input integers exactly; this is not optimized
for arbitrary cryptographic-size input. Prime-power allocation has finitely
many states determined by the input factorization.

## What the fixed-support theorem adds

For any fixed squarefree `d` and finite prime set `H`, effective unit-equation
theory gives a finite arithmetic divisibility basis valid beyond a computable
threshold. A finite geometric remainder then gives an exact basis for every
multiplier supported on `H`. **This package does not implement or run the
general unit-equation solver or that geometric campaign.** Its executable
allocation tool handles individual inputs; the quantified finiteness theorem
is a separate written deduction.

## Reproduction and verification boundary

Python 3.11 or later; standard library only. Run from the repository root:

```bash
python research/composite-support/run_checks.py
python research/composite-support/check_quartics.py
python research/composite-support/verify_rank22.py
```

Verifiers are read-only unless an explicit `--report FILE` is supplied, and
reject optimized Python execution. Frozen reports are [checks.json](checks.json),
[verification.json](verification.json), and [rank22.json](rank22.json).

The suite checks all nine homogeneous quartic discriminants and both conic
identities, compares prime allocation with an independently implemented
forward enumeration for coefficients 1 through 5000, exercises all three
general-tool statuses, and freshly replays the old 88-tile geometric
certificate. It checks class-22 interfaces and the old positive QP witness,
including its odd refinement by 3.

The elliptic checker independently proves `L(E,1)>0` by exact interval
arithmetic, 500 Euler coefficients computed from finite-field point counts,
and a proved bound on the infinite tail. It **cites**, rather than recomputes,
the conductor, additive reduction primes, and root number. The implication
from nonzero `L(E,1)` to rank zero is an established unconditional theorem;
the code is not a proof-assistant implementation of that theorem. The
[source record](sources.json) identifies the independently checked primary
curve data. No BSD conjecture, floating-point rank guess, or bounded
rational-point search is used.

These are internal mathematical and computational checks, not external
referee acceptance or a claim of first priority.

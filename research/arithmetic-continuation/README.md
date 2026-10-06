# Arithmetic continuation, 6 October 2026

This package narrows the unresolved tiling problem. It does not solve
Erdős 634 or decide the primitive F3 counts 990 and 4830. The constructive
geometry is supplied by the earlier theorems identified in each proof.

| Result | Proof and independent audit |
|---|---|
| All-branch finite list and eventual criterion for even squarefree d, odd m, and fixed joint split part H; complementary prime support is unrestricted | [Global theorem](GLOBAL_FIXED_SPLIT_PART.md), [audit](GLOBAL_FIXED_SPLIT_PART_AUDIT.md) |
| Explicit split-part cutoffs for I120, F2, F3 and F4 | [Four-row theorem](OTHER_SPLIT_BRANCHES.md) |
| Sharper F3 cutoffs and global exclusion of odd class-38 multipliers supported on 3 and primes 5,7,17,19 modulo 24 | [F3 theorem](F3_SPLIT_PART_REDUCTION.md), [audit](F3_SPLIT_PART_AUDIT.md) |
| Only O(sqrt X) representations below the seven norm-family constructive tails | [Counting theorem](NORM_GEOMETRIC_REMAINDER.md), [audit](NORM_REMAINDER_AUDIT.md) |

## Scoped membership tool

From the repository root:

```sh
python research/arithmetic-continuation/classify_global_sector.py 38 3
python research/arithmetic-continuation/classify_global_sector.py 110 3
python research/arithmetic-continuation/classify_global_sector.py 110 15
```

The inputs are an even squarefree kernel d and an odd positive multiplier
m; the count is N=dm². The three examples return NO, UNRESOLVED_SMALL_SCALE
and YES, respectively. YES uses an identified existing construction;
NO requires absence of every necessary witness in the complete sector
list. An arithmetic witness below its construction threshold is never
reported as NO. UNRESOLVED describes this tool's methods, and may include
counts already settled by a sharper construction elsewhere in the project.

The program reports the list and its cutoff C(d,H). Its deliberately
coarse finite enumeration is not intended for huge dH². It writes only
standard output. The proof, rather than these example calls, establishes
the completeness of the list and the all-branch implications.

## Finite verification

```sh
python research/arithmetic-continuation/check_norm_remainder.py
python research/arithmetic-continuation/check_split_part.py
python research/arithmetic-continuation/check_other_split_branches.py
python research/arithmetic-continuation/check_global_split_part.py
python research/arithmetic-continuation/check_global_sector_cli.py
```

All checks use exact integer arithmetic and the standard library. They
reject optimized Python execution, print fresh reports, and accept an
optional `--report PATH`. Frozen reports in this directory retain their
scope and explicitly mark the full problem unsolved. The coefficient
comparisons, status controls and independent mathematical audits have
different purposes; none is a formal verification of the entire project.

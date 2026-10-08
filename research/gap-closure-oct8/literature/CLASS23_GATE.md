# Square class 23: source audit, exact gates, and engine results

8 October 2026. The existing constructions give every `23m²` with
`m>=3`. This note records the remaining arithmetic and computational
checks. **It does not declare a newly certified global exclusion of23
or a complete classification of the square class.** A separate complete
refutation trace is not included in the present checkpoint.

## 1. Complete arithmetic gates

The exhaustive angular classification, rationality and integral-scale
spectra are the inputs of
[`uniform-reduction/PROOF.md`](../../uniform-reduction/PROOF.md).
The complete candidate enumerator gives:

| Count | Branch | Primitive tile | Target | Multiplier |
| ---: | --- | --- | --- | ---: |
| 23 | W | (12,7,16) | (64,69,28) | 1 |
| 23 | beta | (6,5,9) | (27,27,46) | 1 |
| 92 | W | (12,7,16) | (128,138,56) | 2 |
| 92 | beta | (6,5,9) | (54,54,92) | 2 |
| 92 | theta | (132,23,144) | (552,552,506) | 2 |
| 92 | double-angle | (121,23,132) | (506,506,552) | 2 |

The classical forms do not contain23 or92. The last two92 candidates
are separately excluded by the
[proved long-seam inequalities](../../../docs/long-seams-density.md):
`23*2<11*12` for theta and `23*2<11²` for double-angle.
Thus precisely the two displayed W/beta targets remain to decide92.
`candidate_checks.json` preserves the full initial lists; the inequalities
are elementary substitutions, not search outcomes.

## 2. Why the current external global23 claim needs a dependency check

Bonfioli's main manuscript at commit
[`4bb61193bafa4471f7ba3a35324ae0f70bd2177c`](https://github.com/ElVec1o/erdos_634_proof/tree/4bb61193bafa4471f7ba3a35324ae0f70bd2177c)
lists23 among excluded primes and reports19,677 exhaustive nodes for its
beta target. However, its general W-prime exclusion cites the old
`K|N` necessity in `rem:b3prime` (main source lines404–409).
The same repository's
[`lean/PAPER_MAP.md`](https://github.com/ElVec1o/erdos_634_proof/blob/4bb61193bafa4471f7ba3a35324ae0f70bd2177c/lean/PAPER_MAP.md)
explicitly flags that input as unsupported and the prime-to-beta
reduction as conditional. Its blob is
`5f116df80cd71151e9e1c011013c25daee8bb966`.

The present audit found the beta23 search but no separately exposed
W23 refutation in the inspected manuscript. Accordingly the beta
exhaustion and the global23 sentence must not be conflated. We do not
infer that no valid prior proof exists; this is the precise dependency
gap in the inspected source chain.

## 3. Fresh complete-engine outcomes

We independently supplied **both** surviving23 instances to the
unmodified optimized exact C++ engine from that immutable source.
It was compiled with `QD_CROSSCHECK`, which repeats every fast arithmetic
operation in GMP and aborts upon disagreement. Fresh serial runs used
MRV selection, no direction restriction, no walk filter and no checkpoint:

| Input | Engine result | Nodes | Maximum depth | Arithmetic comparisons |
| --- | --- | ---: | ---: | ---: |
| W23.txt | EXHAUSTED_NO_TILING | 123 | 16 | 3,562,041 |
| beta23.txt | EXHAUSTED_NO_TILING | 387 | 18 | 14,302,137 |

Every arithmetic comparison agreed. Both runs ended below their100,000
node cap. MRV changes the explored ordering, explaining why the beta
node count differs from the source's original run.

The corner-search principle is complete: at a convex residual corner,
the first tile in angular order has a vertex there and one incident
edge along the chosen boundary ray. Three tile corners and two choices
of incident side exhaust the possibilities, with exact containment
and polygon subtraction permitting T-junctions. Necessary area and
convex-ended boundary-semigroup filters do not impose an arbitrary
lattice. The prior detailed engine review is
[`BONFIOLI_56_AUDIT.md`](../../universal-closure-oct8/overlap-literature/BONFIOLI_56_AUDIT.md).

Nevertheless these saved outputs are **computational engine results**,
not a separately exported and independently replayed complete search
trace. The GMP comparison checks arithmetic, not all control-flow and
geometric logic. This distinction is why this checkpoint does not
promote23 to a newly certified project nonexistence theorem.

The unmodified engine and W-input generator are retained in `vendor/`
with their MIT license and attribution to Vico Bonfioli. Input and source
hashes, exact outcomes and commands are in `class23_replay_checked.json`.
With a C++17 compiler and GMP development libraries, reproduce with:

```sh
g++ -O2 -std=c++17 -DQD_CROSSCHECK vendor/cengine_c2.cpp -o cengine_c2_crosscheck -lgmpxx -lgmp
CENGINE_MRV=1 CENGINE_THREADS=1 ./cengine_c2_crosscheck FILE:W23.txt 100000
CENGINE_MRV=1 CENGINE_THREADS=1 ./cengine_c2_crosscheck FILE:beta23.txt 100000
```

## 4. The92 probe is incomplete

A short single-thread W92 probe visited4,519 nodes at its last logged
checkpoint, maximum depth59, and was manually stopped. Its estimated
progress percentage is an engine heuristic, not a certificate. The
beta92 input was prepared but its search was not run. Neither92 target
has been declared impossible or possible by this audit. No process
from this audit remains running.

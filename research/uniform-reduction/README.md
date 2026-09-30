# Triangle tilings: square-class obstructions and a finite candidate reduction

Denis Paliy, research with ChatGPT assistance. 30 September 2026.

Read **PROOF.md** or **paper.pdf** for the theorems, hypotheses, external
classification inputs, exact scope and remaining obligations. This is a new
partial research continuation, not a claimed full solution of Erdős 634.

The two simple global conclusions exclude every squarefree count congruent to
19 modulo 24 or 35 modulo 120. A stronger local norm condition is also proved.
The note derives the necessary double-angle scale and shows explicitly why all
translation-invariant directed-edge signatures still fail to decide the
Group-1 scale-one geometric problems.

## Replay

Python 3.10 or newer, standard library only:

```bash
python verify_all.py
python candidates.py 105
python exact_search.py 154 --max-nodes 1000 --seconds 8
```

`verify_all.py` regenerates the supplementary JSON reports. Runtime measurements
can change. `MANIFEST.sha256` records the distributed snapshot, not the timing
fields of a future rerun. `EXHAUSTED` is a completed execution of the supplied
search; its small negative-control records are not separately checked proof-tree
certificates. `INCOMPLETE` is never a nonexistence conclusion.

The unlimited abstract search is finite, but the prototype has practical
resource limitations. The stored N=154 run is **INCOMPLETE**. Neither
arithmetic candidates nor formal orientation witnesses are actual tilings.

`verify_positive.py` independently uses exact polygon clipping instead of the
searcher's separating-axis predicate. It checks the positive controls. The
75-tile T-junction construction is an existing project result, not found anew;
its source and original SHA-256 are in `positive75.json`.

`check_symbolic.py` uses a small integer-polynomial implementation to check 21
identities coefficient by coefficient. `check_reduction.py` independently
compares a direct parameter-box sweep with the divisor sieve and tests the
complete residue tables. Finite numerical tests do not prove the universal
geometry or replace the written arguments.

No external peer review or research priority is claimed. No GitHub edits or
emails accompanied this continuation. The prepared N=105 material and the
separate prime-count candidate are not silently treated as inputs to the new
global negative theorem.

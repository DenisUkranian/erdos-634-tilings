# A complete constructive half of the F4 branch

For positive integer sides `0<a<b` with `c²=a²+ab+b²`, the target with sides
`(ac, b(2a+b), c(a+b))` has an explicit `(2a+b)(a+b)`-tiling by `(a,b,c)`.
Every positive integer multiplier is therefore realized for this orientation.

Read [PROOF.md](PROOF.md) for the symbolic four-region dissection, exact grid
removal, attribution to Harries's 88-tile example, and the remaining `a>b` gap.
This does not solve Erdős 634 in full.

```bash
python run_checks.py
python construct.py 3 5 7 --output /tmp/f4-88.json
python verify.py /tmp/f4-88.json
```

The generator emits only positive unit triangles. The separate verifier reads
their coordinates without importing the generator. It checks shapes, target
sides, containment, all tile pairs and total area with exact rational arithmetic.
The frozen [report](VERIFIED_RESULTS.json) records finite regression coverage;
the all-parameter conclusion follows from the written proof.

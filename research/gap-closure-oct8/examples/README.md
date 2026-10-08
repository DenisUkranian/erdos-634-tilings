# A complete 5022-tile example

The all-adjacent theorem with `u=6,v=7,t=2,m=9` gives a tiling of the
triangle with sides `(3087,3348,819)` by **5022** copies of `(42,13,49)`.

`W5022.json` contains every unit triangle in integer coordinates for the
metric `(dx²+160dy²)/98²`. `check_5022.py` imports neither the generator
nor a search engine. It verifies congruence of all tiles, positive
orientation, target containment, exact area, and exact positioned
boundary cancellation on all 568 supporting lines. The boundary-current
argument in the general proof then gives multiplicity one everywhere
off the finitely many edges, excluding overlaps and gaps.

The report `W5022_checked.json` is PASS and binds the coordinate file by
SHA-256 `cd4cf660f7275393d90f3ab89539e19d31ae08da45e5a7e19b3539f9be73aa80`.

The same general construction gives **7502** at `m=11,t=4`, with target
`(3773,4092,1001)`. A separate full unit expansion for 7502 is not claimed.

The frozen `W5022_candidates.json` and `W7502_candidates.json` are outputs
of the existing complete arithmetic overlist with all scale-one rows
retained. Each count has exactly one candidate, this W tile and scale,
and no classical witness. The completeness assumptions are those of
[`uniform-reduction/PROOF.md`](../../uniform-reduction/PROOF.md).
The arithmetic calculation is not the positive proof; the construction is.

```sh
python research/gap-closure-oct8/examples/check_5022.py
python research/uniform-reduction/candidates.py 5022 --keep-scale-one
python research/uniform-reduction/candidates.py 7502 --keep-scale-one
```

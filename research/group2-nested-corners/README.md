# Nested reflected corners

The [proof](PROOF.md) enlarges the sufficient free-width condition from
`mbc-a²k in <a,b>` to **`mbc-a²k in <a,b,c>`**, with
`kc>=m(a-b)`. The coefficient of `c` increases the low rectangle's height;
the deleted corner keeps its original size.

Consequently reversed F4, F2 and F3 are constructible at every positive
integer multiplier when `a>b` and `c<=2b`. The
[ternary semigroup theorem](../f3-descent-attempt/TERNARY_SEMIGROUP_TAIL.md) extends the uniform
primitive range to **`1<a/b<=7/5`**, with no size restriction, including
both F3 orientations. Its general estimate and complete 240-witness finite
replay together prove this interval. The three-generator condition also
applies to some triples beyond this interval.

The primitive F3 count **990** is now positive, with tile `(8,7,13)` and
target sides `(169,286,315)`. Its complete unit certificate passes two
independent exact geometric routes. This does not solve the remaining
F3 scales or the whole Erdős problem.

Reproduce the construction and checks from the repository root:

```bash
python research/group2-nested-corners/construct.py 8 7 13 --family F3 --output /tmp/f3-990.json
python research/group2-nested-corners/verify.py /tmp/f3-990.json
python research/disk-certificates/verify_disk.py research/group2-nested-corners/disk-990.json
python research/group2-nested-corners/check_balanced_7_5_small.py
```

The general constructor also accepts `--family F2` or `--family F4`, a
positive `--multiplier`, and an explicit `--k` and `--q`. With no explicit
parameters it searches only the finite arithmetic witness range, then
emits positive triangular and parallelogram grids. It does not search
for arbitrary tilings.

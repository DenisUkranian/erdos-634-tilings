# F3 from a reflected 120-degree corner

The [general proof](PROOF.md) constructs the ordered F3 family

```
N=3(a+b)(a+2b)m²
```

for **every positive integer m** whenever `b<a<=2b` and
`c²=a²+ab+b²`. It replaces a reflected 120-degree corner by transposing
an actual parallelogram grid. It does not depend on the earlier
beta-corner semigroup condition.

The primitive `(5,3,7)` example gives a fully certified 264-tile triangle
at multiplier one, even though `bc-a²=-4`. The coordinate certificate
and a coordinate-free disk certificate both pass independent checks.

From the repository root:

```bash
python research/group2-gamma-corners/construct.py 5 3 7 --output /tmp/f3-264.json
python research/group2-nested-corners/verify.py /tmp/f3-264.json
python research/disk-certificates/verify_disk.py research/group2-gamma-corners/disk-264.json
python research/group2-gamma-corners/run_checks.py --report research/group2-gamma-corners/VERIFIED_RESULTS.json
```

The statement is ordered: exchanging a,b gives a different F3 target,
which is not automatically covered by this proof. For primitive triples
at multiplier one, the same gamma remainder cannot be filled using a
single short-edge direction class when a>2b. This includes all six
60-degree rotations and both reflections in that class: its boundary
would require `2ab+2b²-a²` to belong to `<a,b>`, which it does not.
The proof establishes this restriction directly from a boundary side.

For `(24,11,31)`, a hypothetical filler must introduce additional short
direction classes; the 4830-tile F3 target remains unresolved here.
The restriction concerns this macro partition, not arbitrary F3 tilings
or the complete Erdős classification.

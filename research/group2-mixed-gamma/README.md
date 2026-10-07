# Staircase gamma-corner continuation

The [proof](PROOF.md) gives a sufficient F3 construction under
`m(a+2b)>=b+a*ceil(m(a-b)/b)`. In particular, every `b<a<=5b/2` works at
every integer multiplier `m>=2`. The primitive target 4830 is still
unresolved; its multiplier-two target **19320** now has an explicit
19320-triangle certificate and exact independent verification.

The directory retains the research route's name, but the finished
staircase uses one short-direction class in its gamma remainder.

From the repository root:

```bash
python research/group2-mixed-gamma/run_checks.py
python research/group2-mixed-gamma/verify_spatial.py research/group2-mixed-gamma/f3-19320.json.gz
```

To regenerate the deterministic compressed unit certificate:

```bash
python research/group2-mixed-gamma/construct_staircase.py 24 11 31 --multiplier 2 --output research/group2-mixed-gamma/f3-19320.json.gz
```

The spatial checker checks lengths, containment, area, and all possible
overlaps through complete rational bounding-box buckets and exact separating
axes. The replay compares a small positive control with the older independent
quadratic checker and rejects duplicates, missing tiles, a wrong target,
and a moved tile vertex. No full classification or external review is claimed.

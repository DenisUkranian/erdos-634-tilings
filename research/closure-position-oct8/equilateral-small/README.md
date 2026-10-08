# Smaller equilateral tilings by (3,5,7)

**Established result in this package:** an equilateral triangle of side
`15m` has a tiling by `15m²` congruent `(3,5,7)` triangles for every
integer `m>=6`. The formerly conjectured-impossible sides 105 and 120
are included; side 90 also works.

* [Proof and attribution](CONSTRUCTIONS.md).
* Full unit coordinates: [540 tiles](equilateral_540.json),
  [735 tiles](equilateral_735.json), [960 tiles](equilateral_960.json).
* [The 315-tile intermediate trapezoid](T30_45_315.json).
* [180-tile seed](../equilateral-position/cpsat/T30_30_0-1_certificate.json).
* [Independent exact geometric audit](../equilateral-audit/).
* [Earlier route and unsuccessful restricted searches](REDUCTION.md).

From this directory regenerate the complete constructions with:

```
python construct_new.py
```

This uses only Python's standard library and the supplied 180-tile seed.
It creates all unit coordinates using exact fractions; no search or
optimization package is needed to reproduce the positive constructions.

The result does not establish minimum size, resolve 154 or 4830, or
classify all of Erdős 634. External priority and peer review are not
claimed.

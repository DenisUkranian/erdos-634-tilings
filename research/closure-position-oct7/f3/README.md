# Direct constructive attack on 4830

7 October 2026. **No positive 4830 certificate and no unrestricted
negative proof were obtained.** These files are exploratory construction
searches. They do not alter the project's UNKNOWN status for 4830.

The ordered primitive F3 tile remains `(24,11,31)` at multiplier one.
The older arithmetic reduction excludes transferring this count to an
easier primitive tile. The established constructions at every integer
multiplier at least two do not construct multiplier one.

## A mixed construction route, rather than another all-grid search

The already proved good F4 construction, with its labels ordered as
`(11,24,31)`, has target sides

```
341, 1104, 1085
```

and uses `(2*11+24)*(11+24)=1610` copies of the same original tile.
Consequently `4830=3*1610` suggests using those positive F4 triangles as
macro pieces. Three such pieces alone cannot work: write alpha for the
original angle opposite 24 and beta for the angle opposite 11. The F3
target has an alpha corner. The good F4 angles are beta, 2*alpha, and
60 degrees + beta. Since alpha+beta=60 degrees and beta/pi is irrational,
no nonnegative sum of those three angle types is alpha.

The mixed route is less restrictive: combine one or two already tiled
1610-tile F4 pieces with ordinary integer-scaled original triangles.
The exact remaining area is 3220 or 1610, respectively. For example,

```
3220 = 36^2+32^2+30^2 = 40^2+36^2+18^2
     = 48^2+30^2+4^2 = 50^2+24^2+12^2.
```

These are area identities only. The new `mixed_macro_probe.py` checks
actual positions, exact containment, and exact interior nonoverlap by
the pre-existing rational advancing-corner engine. It also rejects an
exposed interval on the outer target boundary unless its length belongs
to `<11,24,31>`.

The run allowing at most five macro pieces and requiring at least one
F4 piece exhausted 3,020 search states without finding a construction.
The report is `mixed_macro_five_report.json`. This is a recipe-search
report, not an independently certified impossibility theorem.

The seven-piece run visited 24,287 states in 240 seconds and stopped
with `INCOMPLETE`, at a maximum of six placed macro pieces. Its report
is `mixed_macro_seven_report.json`. The timeout is not a negative result.

## The reflected-corner route

The old sufficient quadrilateral

```
[(312,0),(961,0),(576,264),(312,143)]
```

in Eisenstein coordinates needs 792 original tiles. The fresh six-grid
probe ran for 240 seconds, visited 29,372 states, and stopped with
`INCOMPLETE`, having placed at most five macros. Its report is
`q792_six_probe.json`; it uses the unchanged old
`research/final-synthesis-oct7/f3/probe_beta_quad.py`.

The four-piece impossibility theorem from the previous synthesis does
not exclude six or more grid pieces, arbitrary unit fillings, or another
F3 dissection. Likewise, the failure of the mixed F4 search is not a
necessity theorem for F3.

## Reproduction and scope

From the repository root:

```bash
python research/closure-position-oct7/f3/mixed_macro_probe.py --max-macros 5 --seconds 180
python research/closure-position-oct7/f3/mixed_macro_probe.py --max-macros 7 --seconds 240
python research/final-synthesis-oct7/f3/probe_beta_quad.py --max-macros 6 --seconds 240
```

The script reuses the proved F4 shape as a positive building block. A
future successful run would still need its macro pieces expanded to
unit coordinates and checked by a separate geometry implementation.
No mere area decomposition, timeout, or failed restricted recipe is
promoted to a result about unrestricted 4830-tilings.

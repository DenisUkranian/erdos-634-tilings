# I120 and orientation-height continuation

7 October 2026. Research directed by Denis Paliy, with ChatGPT assistance.

The [written theorem](HEIGHT_LEVELS.md) proves a common c-divisibility
law for actual short-edge orientation-level populations in equilateral,
F1, I120, F2, and F3 tilings. There is one explicitly identified possible
exceptional level. Arbitrary T-junctions are covered by the whole-edge
chain identity; an orientation component need not have its own c-edges
on its boundary.

The theorem does not decide 154 or 4830 and does not classify all N.
A 14-tile parallelogram shows why positivity and a closed whole-c-step
boundary alone do not improve the conclusion from c to c squared.

Replay the algebra and actual-construction checks with:

```sh
python research/i120-global-oct7/check_height_levels.py
```

The default replay writes no files. Use `--report PATH` to retain a new
JSON report explicitly.

The regression checks include 87 primitive norm triples, an equilateral
construction, its I120 extension, three existing F2/F3 certificates with
their canonical target normalizations, and all 91 pairs in the small
parallelogram. The retained report is `height-level-checks.json`.

## A bounded search probe for 154

The new [probe](probe_154_integer_seams.py) adapts the preserved n105
corner-fan engine to the target `(91,91,154)`. It adds two necessary
integer-seam tests to its existing adjacency, arc-consistency and binary
implication rules:

1. Every remaining boundary segment has integer length. Its endpoints
   are original tile vertices or target corners, and any completion
   divides it into positive integer atoms.
2. Whenever one placed tile has a vertex on another placed tile's side,
   its distance from that side's endpoint is integral. This checks also
   contacts that later disappear from the remaining region's boundary.

Both use the existing [integer-atom theorem](../../docs/exact-seam-certificates.md).
No artificial diagonal or unconstrained point is treated as a seam.
All 489,555 pairs of the existing 990-tiling pass the new pair test;
they include 300 tested vertex-on-edge incidences.

```sh
python research/i120-global-oct7/probe_154_integer_seams.py --seconds 300
```

The retained run visited 2,674 states, reaching 97 placed tiles, and
ended **INCOMPLETE** at its 300-second limit. It checked 26,498
vertex-on-edge incidences and found only two incompatible tile pairs
with noninteger seam offsets. No state was rejected by the additional
residual-boundary length test. These figures show limited extra pruning,
not a nonexistence proof. The retained report is
`probe-154-integer-seams-report.json`. Rerunning with an unchanged budget
is not expected to resolve the open branch.

The search code is not an independent refutation checker. Even a future
exhaustion requires its own complete certificate and independent replay
before it can be reported as a computer-assisted exclusion.

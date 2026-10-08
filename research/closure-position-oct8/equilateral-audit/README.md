# Independent exact audit of the 180, 315, 540, 735 and 960 tile certificates

8 October 2026. Internal independent implementation; no external review or novelty determination is asserted here.

All five explicit certificates pass `independent_geometry.py`, written without importing the constructor, solver, current matrix, or the other new verifier.

| Target | Unit tiles | Pairwise interior-disjointness checks | Result |
|---|---:|---:|---|
| T(30,30) trapezoid | 180 | 16,110 | PASS |
| T(30,45) trapezoid | 315 | 49,455 | PASS |
| Equilateral triangle, side 90 | 540 | 145,530 | PASS |
| Equilateral triangle, side 105 | 735 | 269,745 | PASS |
| Equilateral triangle, side 120 | 960 | 460,320 | PASS |

Every tile has sides `(3,5,7)`. The certificates supply every unit triangle; these results do not rely on a claimed macroregion expansion. In particular, the three full equilateral certificates are actual congruent-triangle tilings.

## Exact checks and why they suffice

An integer pair `(x,y)` represents `(x+y rho)/7`, with `rho=exp(i*pi/3)`. Squared length in these coordinates is `(x*x+x*y+y*y)/49`. The checker recomputes the three squared side lengths of every triangle and obtains exactly `9,25,49`.

After normalizing polygon orientation, each target edge defines a closed half-plane. Every tile vertex lies in all target half-planes. Convexity therefore puts the whole tile inside the target.

For each pair of triangles the checker first tries separation of their intervals on either affine coordinate axis. If that fails, it checks the oriented edge half-planes of both triangles. Two convex polygons have disjoint interiors exactly when one of their edge-normal projection intervals separates them, with equality allowed. Thus shared edges, isolated contacts and T-junctions are accepted, and positive-area overlap is rejected. All arithmetic uses Python integers; there is no numerical tolerance.

Finally, shoelace determinant areas add to the exact determinant area of the target. Containment, pairwise disjoint interiors and area equality establish full coverage. Indeed a missed point of the target's interior would have a positive-area neighborhood missed by the finite closed union; a missed boundary point contradicts closure of that union after the interior is covered.

## Reproduce

From the repository root:

```sh
python research/closure-position-oct8/equilateral-audit/independent_geometry.py research/closure-position-oct8/equilateral-position/cpsat/T30_30_0-1_certificate.json
python research/closure-position-oct8/equilateral-audit/independent_geometry.py research/closure-position-oct8/equilateral-small/T30_45_315.json
python research/closure-position-oct8/equilateral-audit/independent_geometry.py research/closure-position-oct8/equilateral-small/equilateral_540.json
python research/closure-position-oct8/equilateral-audit/independent_geometry.py research/closure-position-oct8/equilateral-small/equilateral_735.json
python research/closure-position-oct8/equilateral-audit/independent_geometry.py research/closure-position-oct8/equilateral-small/equilateral_960.json
```

The recorded `*_independent.json` files pin the exact certificate bytes with SHA-256. `check_negative_controls.py` separately verifies that an altered side, an area-preserving duplicated tile, and a rigidly displaced tiling are rejected for the appropriate geometric reasons.

This audit proves the supplied tilings. It does not classify all equilateral counts, prove a smallest-count statement, resolve 154 or 4830, or establish publication priority.

## Independent review of the infinite extension

The symbolic part of `../equilateral-small/CONSTRUCTIONS.md` was also checked. For `k>=3`, the identity `15k-34=3(5k-13)+5` has nonnegative coefficients and supplies the claimed auxiliary horizontal strips. Stacking `T(60,15(n-2))` below a translated `T(30,30)` gives exactly `T(30,15n)` for every `n>=2`.

For the cyclic assembly, the common interior point is `(15s,15t)` and the three boundary junctions are `(15s,0)`, `(15(s+r),15t)` and `(0,15(s+t))`. They lie on the three distinct sides of the equilateral triangle of side `15(r+s+t)`. The three segments from the interior point to these junctions partition the target into precisely the three displayed rotated trapezoids. Thus their containment and nonoverlap hold for all positive parameters, not only for the three numerical controls.

Choosing `(r,s,t)=(2,2,m-4)` therefore proves the stated construction for every integer `m>=6`, once the independently checked 180-tile seed is supplied. This verifies the extension's geometry; its literature attribution and novelty are outside this audit.

# The central height has at least 24 tiles in the 154 candidate

8 October 2026. This is a necessary condition, not an impossibility proof for 154.

Let the target be the isosceles triangle `(91,91,154)`, tiled by congruent
`(8,7,13)` triangles. Normalize the base to the positive real axis and use
the established short-edge heights with `rho=exp(i*pi/3)` and
`z=(8+7rho)/13`. Then

**Theorem.** The central population satisfies `n_0 >= 24`.

The known congruence is `n_0 = 11 (mod 13)`. We exclude `n_0=11` by
retaining the affine supporting line of each short edge. All statements
below allow arbitrary T-junctions.

## Common character and supporting lines

Write the two counterclockwise reference tile types as

```
A_j: (0,8 rho^j,7 rho^(j+2)),
B_j: (0,7 rho^j,8 rho^(j+2)),   j=0,...,5.
```

At height zero their signed short-direction current, reduced modulo 13,
is `(11,0,0)`. Apply the alternating character `J0-J1+J2`. Each `A_j`
contributes `(-1)^j`, and each `B_j` contributes `-(-1)^j`. If there are
11 tiles, the character is an odd integer between -11 and 11 congruent
to 11 modulo 13. Thus it equals 11. Only the six orientations

```
A0, A2, A4, B1, B3, B5
```

can occur. Their 8-edges point in even directions and their 7-edges in
odd directions.

On every complete affine supporting line except the exterior base,
the signed total of these short edges is divisible by 13. The other
edges on that line are complete long edges of length 13 from heights
`-1` or `1`; no other exterior side has a height-zero direction.
Whole-line integration of oriented boundary cancellation proves this
regardless of how individual edges meet or are subdivided.

If a line contains `m` 8-edges and `n` 7-edges, its residue condition is
`8m-7n=0 (mod 13)`, after possibly reversing its orientation. Here
`m+n<=11`. Every nonempty such pair is one of

```
(9,1), (5,2), (1,3), (6,5), (2,6).
```

The program permits the larger list valid through population 13, which
also includes `(13,0),(0,13),(3,9)`; none of these three can occur under
the present total bound. Every actual partition into supporting lines
is a sum of these pairs. Exact finite dynamic programming finds the
maximum number of nonempty lines for any required total `(M,N)`.

## The exterior base requires three 8-edges

Every tile edge on the exterior base is directed positively, because
all tiles lie above it and the tile boundary is oriented
counterclockwise. No height-zero 7-edge can lie there: all such edges
parallel to the base point negatively. Consequently the base has `m`
8-edges and `k` long edges of length 13, and

```
8m+13k=154,     0<=m<=11.
```

It follows that `m=3`, `k=10`. All three of these 8-edges lie on the
same supporting line, the exterior base. If the total pair in the
base direction is `(M0,N0)`, its maximum possible number of supporting
lines is therefore

```
L0 = 1 + max_lines(M0-3,N0).
```

The other two direction families have bounds
`L1=max_lines(M1,N1)` and `L2=max_lines(M2,N2)`.

A gamma vertex is the intersection of the supporting lines of its two
short edges. Thus an orientation using direction families `r,s` can
occur at most `Lr*Ls` times: any additional occurrence would have the
same gamma vertex and orientation as another tile, giving coincident
interiors.

There is also a sharper bound specifically on the base. Its 8-edges
belong only to orientations `A0` and `B1`. The other short edge of `A0`
uses direction family 2, and that of `B1` uses family 1. Therefore the
number of available 8-edges on the base is at most

```
min(number of A0,L2) + min(number of B1,L1).
```

This upper bound must be at least 3.

## Complete finite check

Enumerate weak compositions of 11 among the six allowed orientations
and retain precisely those whose direction-current residues are
`(11,0,0)`. There are exactly 28 inventories. The exact checker excludes:

* 10 inventories having fewer than three positive 8-edges in the base direction;
* 10 inventories whose base gamma-vertex capacity is at most two;
* 8 inventories having a repeated orientation exceeding its gamma-vertex capacity.

All 28 inventories and their individual contradictions appear in
`central_eleven_verified.json`. The generator and verifier are
`check_central_eleven.py`; they use the supporting-line arithmetic from
`closure-position-oct7/oct8-structural/check_no_thirteen_height.py`.

Run from the repository root:

```sh
python research/closure-position-oct8/central/check_central_eleven.py
```

This exhausts the finite orientation inventories; it is not a search
limited by time or by a chosen geometric grid. Since `n_0=11` is
impossible and `n_0` is positive and congruent to 11 modulo 13, the next
possibility is 24, proving the theorem.

The argument does not exclude `n_0=24` or assert that any surviving
orientation inventory can be placed geometrically.

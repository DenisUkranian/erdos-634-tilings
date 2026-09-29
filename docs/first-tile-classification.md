# Complete count classification for the fixed tile (2,3,4)

29 September 2026. This classifies **all triangular targets for one prescribed tile**. It does not classify all integers in Erdős problem 634, whose tile may also vary. The proofs have internal review and exact certificate replays; no external acceptance or priority claim is made.

Let $T$ be the triangle with sides $(2,3,4)$, with opposite angles $\alpha,\beta,\gamma$. Then a triangle can be tiled by $N$ congruent copies of $T$ if and only if $N$ appears in the following table.

| Target shape | Target side lengths in units of $T$ | Exact counts | Permitted integer scales |
|---|---|---|---|
| Similar to $T$ | $(2t,3t,4t)$ | $t^2$ | $t\ge1$ |
| W, angles $(2\alpha,\beta,\alpha+\beta)$ | $(6t,7t,8t)$ | $7t^2$ | $t\ge2$ |
| Beta-isosceles | $(8t,8t,11t)$ | $11t^2$ | $t\ge2$ |
| Theta-isosceles | $(6t,6t,3t)$ | $3t^2$ | $t\ge4$ |
| Alpha-isosceles | $(12t,12t,21t)$ | $21t^2$ | $t\ge2$ |
| Other scalene, angles $(2\alpha,\alpha,2\beta)$ | $(16t,28t,33t)$ | $77t^2$ | $t\ge1$ |

Equivalently, the squarefree part of $N$ must be one of

$$
1,\ 3,\ 7,\ 11,\ 21,\ 77,
$$

and its square multiplier must meet the corresponding threshold in the table. These six square classes are disjoint.

## Why the list is exhaustive

The tile satisfies

$$
3\alpha+2\beta=\pi,\qquad
\cos\alpha=\frac78,\quad \cos\beta=\frac{11}{16},\quad\cos\gamma=-\frac14.
$$

Its angles are irrational multiples of $\pi$. For example, if $\alpha/\pi$ were rational, then $2\cos\alpha=7/4$ would be a rational algebraic integer and hence an integer, a contradiction; the displayed angle relation then gives irrationality of the others.

The Laczkovich–Beeson shape classification, with the exact source versions in [the dependency ledger](prime-case-dependencies.md), permits precisely the five listed nonsimilar target shapes for this tile. The tile has neither a right angle nor a $60^\circ$ or $120^\circ$ angle and is not in the separate double-angle family: $\cos(2\alpha)=17/32$ and $\cos(2\beta)=-7/128$ equal none of the other tile-angle cosines, while $2\gamma>\pi$. Similar targets give the sixth row.

The [integer-scale formulas](eventual-rational-families.md), specialized to $(u,v)=(1,2)$, give the necessary count forms

$$
Qt^2=7t^2,\quad Pt^2=11t^2,\quad bt^2=3t^2,
\quad bQt^2=21t^2,\quad QPt^2=77t^2.
$$

For a similar target with scale $t$, its side lengths $2t,3t,4t$ are integers because every outer side is a union of whole integer-length tile edges. Therefore $t=3t-2t$ is an integer and the area ratio is $N=t^2$. Conversely, ordinary parallel subdivisions construct every such square count.

## Matching constructions and exclusions

**W and beta.** The [scale-spectrum note](scale-spectra.md) proves the exact spectra $7t^2$ and $11t^2$ for $t\ge2$, using constructions and exclusions already present in Vico Bonfioli's work. These complete fixed-shape spectra are credited inputs, not claimed discoveries here.

**Theta.** The [theta proof](theta-branch.md) excludes scales $1,2,3$. Its four seeds at scales $4,5,6,7$, followed by addition of scale $4$, construct every larger scale. The missing seed at scale $5$ is the [ten-piece construction of 75 tiles](theta-75-construction.md), with exact coordinate verification.

**Alpha.** The [separately replayed 21-tile refutation](alpha-21-obstruction.md) excludes scale $1$. For every $t\ge2$, cut off a $3t$-scaled copy of the tile: it contributes $9t^2$ tiles and leaves a theta target at scale $2t\ge4$, which contributes $12t^2$ tiles. Their sum is $21t^2$. Thus no search for each subsequent alpha scale is required.

**Other scalene.** The [two-piece construction](two-piece-construction.md) realizes $77t^2$ for every $t\ge1$; its general count-form theorem supplies necessity.

These six matching necessity-and-construction arguments prove the table. The new global [exclusion of count 21](n21-global-reduction.md) also checks that no different tile can realize that count; this stronger statement about 21 is not needed to classify the prescribed tile.

## Scope and attribution

This synthesis combines published shape classification, known constructions and fixed-shape spectra, this project's complete theta construction, and a compact independent exact refutation of the last alpha instance. Earlier exclusions of 21 were reported by Bonfioli and Harries; the present certificate is an independently checked reproduction, not a first-discovery claim.

The project was directed by Denis Paliy. ChatGPT assisted with proof exploration, writing, implementation, and exact checks. Neither this finite-tile classification nor successful code replay constitutes a solution of the unrestricted all-tile Erdős problem.

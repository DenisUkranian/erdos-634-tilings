# Six interacting corners exclude the third fixed N=105 collar

29 September 2026. Research directed by Denis Paliy, with ChatGPT assistance
in exploration, proof writing, and exact verification. This is an internal
computer-assisted proof, not external refereeing or a global exclusion of 105.

**Theorem.** The particular 45-tile collar in
[n105-local-fan-collar-5-21-19.json](../data/n105-local-fan-collar-5-21-19.json)
cannot extend to a complete tiling of the side-105 equilateral triangle by
copies of the tile $(5,21,19)$.

The preceding [local-fan note](n105-local-fan-frontier.md) correctly verified
that each of its 18 convex residual corners can be filled separately. The
obstruction is compatibility: six of those corners already have no mutually
compatible choice of their local fillings.

## Why the local lists are exhaustive

Let $(\alpha,\beta,\gamma)$ be opposite $(5,21,19)$. Then
$\gamma=\pi/3$, $\alpha+\beta=2\pi/3$, and
$2\cos\alpha=37/19$. Thus $\alpha/\pi$ is irrational: otherwise
$2\cos\alpha$ would be a rational algebraic integer and hence an integer.

At a convex residual corner every incident unplaced tile has an actual vertex
there; a tile edge passing through the corner would require a straight angle,
which does not fit. Start with the tile adjacent to the first boundary ray,
and list the incident tile angles in their circular order. Irrationality and
$\beta=2\gamma-\alpha$ give exactly the following inventories for the three
sector types used in this certificate:

| Residual sector | All possible angle inventories |
|---|---|
| $\alpha+\gamma$ | one $\alpha$ and one $\gamma$ |
| $2\gamma$ | two $\gamma$, or one $\alpha$ and one $\beta$ |
| $\beta$ | one $\beta$ |

For every inventory the checker enumerates all angle orders and both orders
of the incident edge lengths. The fixed vertex and first ray determine each
placement exactly. It rejects only a tile outside the target or an interior
overlap with the collar or another tile in the same fan. This includes
reflected tiles and allows T-junctions; no coordinate lattice is assumed.

The six selected sectors, labelled $1,2,6,9,10,13$ in the certificate, have
exactly two admissible full fans each, labelled 0 and 1. Across the six sectors
there are 44 raw angle/order choices. The full rational coordinates, sector
rays, and retained fans are in the
[six-corner certificate](../data/n105-six-corner-refutation.json).

## A six-step contradiction

A complete tiling would choose one of the two fans at each of these six
corners. Two fans cannot both occur if different triangles in them overlap in
positive area. Identical triangles shared by two corner descriptions are
permitted and are not counted as a conflict.

The following eliminations use only such geometric conflicts:

| Step | Remove this choice | It conflicts with every remaining choice at |
|---|---|---|
| 1 | corner 1, option 1 | corner 6: options 0 and 1 |
| 2 | corner 2, option 0 | corner 1: option 0 |
| 3 | corner 9, option 0 | corner 13: options 0 and 1 |
| 4 | corner 10, option 0 | corner 2: option 1 |
| 5 | corner 6, option 0 | corner 9: option 1 |
| 6 | corner 6, option 1 | corner 10: option 1 |

Corner 6 has no remaining option, a contradiction. This is an exhaustive
local incompatibility argument without branching, not a failed attempt to
complete one selected collection of fans.

## Exact replay and scope

Run from the repository root:

```sh
python3 scripts/verify_n105_joint_fans.py
```

The [checker](../scripts/verify_n105_joint_fans.py) imports only existing
independent verification helpers, not search or construction code. It first
rechecks the retained collar and its individual positive witnesses. It then
reconstructs the six actual empty sectors directly from incident tiles,
re-enumerates every possible fan, and checks all eight required conflicts by
rational polygon clipping. For each conflict it also records an exact point
strictly inside both conflicting triangles. Finally it replays the six
eliminations. The deterministic [report](../verification/n105-joint-fans.json)
returns `PASS_FIXED_COLLAR_SIX_CORNER_INCOMPATIBILITY`.

The program uses the standard library, writes only to standard output, and
refuses optimized Python. An optional argument selects another data directory.

This proves nonextendability of this one collar. It does not exhaust all
boundary collars, does not rule out the tile globally, and does not decide
N=105. The earlier two [fixed-collar obstructions](n105-fixed-collar-obstructions.md)
remain separate valid results. Successful individual corner tests and global
geometric compatibility are different statements.

# Independent audit of the two-gate population certificates

21 November 2026. This audit checks the unrestricted projection of a
complete **two-tree spine-class** tiling and the two exact integer
certificates. It does not assume a finite geometric placement catalogue.
No optimization or tiling search was performed during the audit.

| Reviewed file | SHA256 |
|---|---|
| `both_gate_torus.py` | `36c9ab8b158262744dfefd1b29372b69cb93f2ac8b745be40a736684aa801f38` |
| `BOTH_GATE_MIN_37.json` | `cf36b59d1a94cfbb23f8068a947b2663dbd481edae96e9d16214cc91cc9c842d` |
| `BOTH_GATE_MIN_43.json` | `e4aaef1bb4d87a8f738c3afb56342f9238fc3ea995f06e294714761e3315c15c` |

**Assessment:** the two certificates rigorously imply `n_1>=5c` in
the path frame for every complete spine-class tiling of either target.
The model and the inequalities were independently checked without
importing the model builder, SciPy, or its sparse matrix.

## 1. Exact projection and the two gates

The previously audited spine classification becomes `R,zR,z^2R`
at path-frame short heights `0,1,2`. Dividing all coordinates by `z`
makes every height-one vertex integral in `R`. Write its obtuse vertex
as `q=(x,y)` and its long endpoints as

`u=q-a*rho^j`, `w=q+b*rho^(j+s)`.

For the up hand, native height-two membership is `u/z in R`.
Since

`1/z=((a+b)-b*rho)/c`,

the two numerator coordinates are `(a+b)u_x+b*u_y` and
`-b*u_x+a*u_y`. Modulo `c` the second vanishes precisely when
both do, using the norm relation and coprimality. The native gate
condition is therefore

`phi(u)=a*u_y-b*u_x=0 mod c`.

For the down hand, native height-zero membership is `u*z in R`.
The corresponding numerator coordinates are
`a*u_x-b*u_y` and `b*u_x+(a+b)*u_y`, giving

`psi(u)=a*u_x-b*u_y=0 mod c`.

The other long endpoint has the same gate: dividing an up long
vector by `z`, or multiplying a down long vector by `z`, gives
an integral length-`c` unit vector. The independent check verifies
these equivalences directly at both endpoints for every residue and
orientation.

Every nonnative gate is closed under the full spine hypothesis.
The already audited closed-gate theorem supplies its actual whole
half-turn mate. Thus the height-one tiles partition into open singles
and closed pairs. An open tile which also has a mate can be represented
by two singles; no forced unmatchedness is assumed at open gates.

Taking `q` modulo `cR` preserves both gates and every endpoint row.
It does not require `q` to be in a bounded physical box. There are
`12c` open single columns. Each closed pair has one representative
with `j` in `0,1,2`, giving `6c(c-1)` pair columns.

## 2. Why the torus endpoint equations hold in the real tiling

Use one potential table for each unoriented height-one axis. At an
integral normalized point, use the table entry modulo `cR`; at a
point outside `R`, assign zero. The endpoint difference reverses
under orientation reversal and telescopes under every subdivision.

A whole long side of physical height one has normalized vector
`c*rho^j`. If one endpoint is integral, both are integral with the
same residue; if one is nonintegral, both are nonintegral. Its total
potential difference is therefore zero in either case. This remains
true when partial contacts subdivide that side at additional points.

There is no exterior side of height one. Summing the real oriented
boundary currents consequently gives zero for all the height-one
short-edge endpoint rows on the torus. Actual long-side positions
off the native height-one lattice do not invalidate the projection.

The short-side signs in the implementation agree with direct CCW
triangles: use vertices `u,q,w` for `s=+1` and `u,w,q` for `s=-1`.
The two short edges then give the displayed row coefficients.

## 3. Independent exact certificate verification

The audit reconstructed the two short-edge weights directly from
those CCW polygons, identified their unoriented axes from their
integer displacement vectors, and evaluated the supplied integer
tables. Closed-pair weights were reconstructed from the actual mate
apex `u+w-q` and rotation `j+3`. This was independent of the matrix
construction in `both_gate_torus.py`.

Let `F(column)` be the endpoint weight, `g(column)` the signed
population, and `m(column)` its population, one or two. Every column
was checked against

`F(column)+t*g(column) <= D*m(column)`.

| Target | Open singles checked | Closed pairs checked | `D` | `c*t` |
|---:|---:|---:|---:|---:|
| 3431 | 444 | 7992 | 1,000,001 | 140,035,861 |
| 5063 | 516 | 10,836 | 1,000,001 | 194,218,014 |

For both certificates, the largest single score is exactly `D` and
the largest pair score exactly `2D`; every inequality passes with
integer arithmetic. Every actual projected tiling is a nonnegative
integer sum of these columns. Summing the inequalities uses zero
endpoint weight and the path-frame signed height-one charge `G_1=c`,
and yields

\[
 n_1\ge\frac{140035861}{1000001}\quad(c=37),\qquad
 n_1\ge\frac{194218014}{1000001}\quad(c=43).
\]

Both bounds strictly exceed `3c`. The height-one sign populations
are separately divisible by `c`; since their difference is `c`,
`n_1/c` is an odd integer. Hence `n_1>=5c` on both targets.
Floating optimizer status is unnecessary for this conclusion once
the exact finite column inequalities have been verified.

## 4. Scope and positive-control interpretation

The theorem applies to every full tiling in the classified spine
branch, including all placements and partial contacts in that branch.
The existing 143 complete control is preserved by the projection;
it is not being subjected to a target certificate with different
parameters.

The closed-pair condition cannot be transferred unchanged to the
other global branch. A nonnative height-zero or height-two node may
then be occupied and supply a genuine unpaired contact. Extending the
`5c` conclusion to every tiling requires an additional argument for
those active gates. The audited certificates by themselves neither
exclude the complete spine class nor decide either target.

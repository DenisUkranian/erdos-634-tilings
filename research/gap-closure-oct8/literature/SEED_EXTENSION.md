# Every W/beta seed extends by v: an improved adjacent-parameter conductor

8 October 2026. The beta addition law is already stated by Bonfioli in
[the companion manuscript](https://github.com/ElVec1o/erdos_634_proof/blob/4bb61193bafa4471f7ba3a35324ae0f70bd2177c/paper/erdos-634-companion.tex),
Theorem `thm:addlaw`: two available scales can be added when one is
divisible by v. Below we specialize it using the old Beeson scale-v
seed and give the same elementary partition for W, also an application
of Harries' multiplier-addition argument. The useful new deduction
combines these old mechanisms with the project's new adjacent seed to
improve the sufficient conductor. No external priority claim is made.

**Later in the same turn:** the separately audited
[all-adjacent-scale theorem](../group1-helper/ADJACENT_ALL_SCALES.md)
constructs every scale `m>=v`, superseding Theorem2 below as the best
adjacent bound. Theorem1 still applies to every coprime pair `u<v`.
Theorem2 remains the exact conductor of its explicitly stated sufficient
set and is retained to document the deduction, not as the current best
geometric threshold.

Let `0<u<v` be coprime integers, and set

```
a=uv, b=v²−u², c=v², Q=2v²−u², P=3v²−u².
```

The W target at scale T has sides `T*(v³,uQ,vb)` and count `QT²`.
The beta target has sides `T*(v³,v³,uP)` and count `PT²`.

**Theorem 1.** For either of these fixed targets, if scale T is tiled,
then scale `T+v` is tiled, for every positive integer T. Consequently,
if `T>=v−u` is tiled, then every scale in `T+<u,v>` is tiled.

This is a sufficient extension, not a necessary scale condition.

## 1. The exact addition partition

Let a triangle Delta have vertices `O=0,A,B`. For positive integers r,s,
the triangle `(r+s)Delta` is the disjoint union of

```
triangle(0,rA,rB),
rA + triangle(0,sA,sB),
parallelogram(rA,rB,(r+s)B,rA+sB).
```

The first two pieces are r- and s-scaled copies of Delta. The two
adjacent side lengths of the parallelogram are `r|B−A|` and `s|B|`;
their included angle is the angle of Delta at B or its supplement.
If these lengths are integer multiples of two adjacent tile sides
meeting at that angle, the parallelogram has a grid of two-tile cells.

In the W target, choose B to be the beta corner. Its adjacent lengths
at scale one are `uQ` and `v³`; the original tile has adjacent lengths
`a=uv` and `c=v²` there. Take `r=v`, `s=T`, and put `|B−A|=uQ`,
`|B|=v³`. The numbers of grid cells in the two directions are exactly

```
(v*uQ)/(uv)=Q,       (T*v³)/v²=Tv.
```

Every cell splits into two congruent original tiles by SAS. The old
Beeson construction supplies the W triangle at scale v. The other
triangle uses the assumed scale-T tiling. The resulting count is

```
Qv² + QT² + 2QTv = Q(T+v)².
```

For the beta target, take either beta base corner: its adjacent lengths
are `uP` and `v³`. Replace Q by P throughout. Its scale-v seed is the
old W seed plus the usual triangular attachment. Thus the same proof
gives beta at `T+v`.

The [existing cap theorem](../../w-beta-caps/PROOF.md) extends any
scale `T>=v−u` to `T+u`. All later scales remain above that cutoff.
Applying these two extensions in either order proves `T+<u,v>`.
In particular the extension applies to **arbitrary** scale-T tilings;
it imposes no normal form on their interiors.

## 2. Adjacent parameters

Now let `u>=2`, `v=u+1`. The old seed has scale `u+1`, and the
[new adjacent construction](../../universal-closure-oct8/group1-adjacent/PROOF.md)
has scale `u+2`. Subdivide either seed, then apply Theorem 1 and the
old cap. This constructs every scale in

```
A_u={p(u+2)+q(u+1)+ru : p,q,r>=0, p+q>=1}.             (1)
```

To justify mixtures explicitly: when p>0, subdivision first supplies
`p(u+2)` and the +v extension supplies the q copies of `u+1`; when
p=0, subdivision supplies `q(u+1)`. The +u cap then adds ru. Every
starting scale is at least `v−u=1`.

**Theorem 2.** The exact conductor of the sufficient set (1) is

```
C_u = u*ceil(u/2)+1.
```

Thus every W and every beta scale `m>=C_u` is constructed for every
adjacent pair `(u,u+1)`. This does not declare smaller omitted scales
impossible.

**Proof.** For a residue j modulo u, with `1<=j<u`, its smallest
member of (1) is

```
w_j=u*ceil(j/2)+j,
```

obtained from `p=floor(j/2)` and `q=j mod 2`. The least positive
member of residue zero is

```
w_0=u*ceil(u/2)+u.
```

Indeed put `k=2p+q>=1`. For a fixed k the least possible p+q is
`ceil(k/2)`, so the least value is `u*ceil(k/2)+k`. This expression
strictly increases with k. Choose the smallest positive k in the
required residue: k=j for j>0 and k=u for j=0. Adding ru then gives
every larger integer in that residue. The largest w_j is w_0, so the
largest missing integer is `w_0−u=u*ceil(u/2)`. This proves the
conductor formula. ∎

| u | Previous two-seed sufficient conductor | Improved conductor |
| ---: | ---: | ---: |
| 2 | 3 | 3 |
| 3 | 10 | 7 |
| 4 | 12 | 9 |
| 5 | 26 | 16 |
| 6 | 30 | 19 |

At u=3 the newly filled scale is **9**: take the new scale5 seed and
add v=4. Scales7 and8 already follow from the previous constructions;
the +u cap then fills the tail from7. At u=4 the newly filled scale11
is the new scale6 seed plus v=5. Thus not every point of the improved
tail is itself a newly constructed scale.

## 3. Limits and verification

The extension does not change the primitive tile or remove small-scale
questions. For u=2 it supplies the fixed W/beta tails from scale3;
the global counts14,56 and23,92 require separate all-branch decisions.
The new class15 theorem supplies no cross-tile identification with these
W/beta targets. The literature audit in `README.md` gives the precise
remaining scope.

`check_seed_extension.py` checks exact rational macrogeometry, tile-side
ratios, area identities and the claimed conductor against direct
generation. The general proof is the partition and residue argument
above, not an extrapolation from these finite checks.

# Full-solution attempt: what was proved and what remains

3 October 2026. Denis Paliy, research with ChatGPT assistance.

The requested objective is a necessary-and-sufficient characterization for
every positive tile count in Erdős 634. **That objective was not reached.**
The constructions below have proofs and exact finite checks; they do not
supply the missing necessity statements. This continuation follows the
[archive reconciliation](research-2026-10-03.md).

## Confirmed general constructions

* [Oriented F4](../../research/group2-f4/PROOF.md): every multiplier for
  `c²=a²+ab+b²` and `a<b`.
* [W/beta cap](../../research/w-beta-caps/PROOF.md): every scale in
  `v+<u,v>`, hence every scale at least `uv-u+1`, for every primitive
  `0<u<v`. The construction extends an arbitrary existing tiling; it does
  not require that tiling to contain a prescribed internal cut.
* [120-degree trapezoids](../../research/group2-trapezoids/PROOF.md):
  smaller general seeds, a parameterized reflected-corner construction,
  and the sufficient equilateral bound `m>=3 ceil(c/min(a,b))`.
* [Balanced F4, F2 and F3](../../research/group2-trapezoids/BALANCED_F4.md):
  the corner construction with a free integer parameter and its transfers
  supply all `m>=2` when `b<a` and `3c>=4a`. They leave the primitive
  scale-one cases open. The exact criterion stated for this construction
  is not a necessary condition for arbitrary tilings.

These are separate sufficient theorems. Their proofs, generators and
verification scopes are in the linked packages. External referee
acceptance and a complete classification are not asserted.

## Why the proposed converses do not follow

**W/beta semigroup necessity.** Whole-edge arithmetic alone cannot force
membership in `v+<u,v>`. For every `v>=4`, set `u=v-1` and use the usual
`a=uv,b=v²-u²,c=v²`. Then

```
(2v+1)c = (v-2)a + 2v b + v c.
```

Every coefficient on the right is positive, even the c coefficient is
a multiple of v, but `2v+1` is outside `v+<v-1,v>`: its offset `v+1`
is neither generator and is smaller than twice the smaller generator.
This is a counterexample to the proposed arithmetic implication, not a
tiling or a counterexample to the geometric spectrum conjecture.

**Rescaling the cap.** Theorem 1 of Abrams and Pommersheim,
[arXiv:2301.03475v2](https://arxiv.org/html/2301.03475v2), applies to
arbitrary trapezoid dissections. With tile area normalized to one, any
rational diagonal-triangle area must be an integer. A step-k W/beta cap
with top length m has small diagonal area `km/u` in tile units. Thus
the new step-u cap cannot simply be rescaled to step one for `u>1`:
its new top length is `(v-u)b`, coprime to u. This rules out the entire
rescaled cap, including alternative fillings of it. It does not rule
out differently shaped collars or arbitrary triangular tilings.

**A finite pair of trapezoid seeds is not an exact spectrum.** The
trapezoid package gives a checked counterexample to the candidate set
`{K-bd,K-ad}+<a,b>`, where `K=a²+b²,d=a+b-c`. Its general parameterized
construction can go below both seeds. A necessity theorem cannot be
inferred from their success for the smallest tile.

**Pairing triangles into parallelograms.** A weighted Hall argument
gives a matching covering all white tiles under the appropriate
checkerboard hypotheses, including T-junctions. The stronger geometric
pairing is impossible for a non-similar triangular target: cancellation
of half-turn pairs, together with perimeter equality, would force every
unmatched tile to have precisely the target's three edge directions.
The [complete argument](../checkerboard-matching-limit.md) explains why
the direct lozenge/parallelogram analogy cannot provide the desired
normal form.

**Boundary inventories and long seams.** Consecutive-parameter theta
and double-angle targets remain a serious test. Exact edge inventories
and short lists of possible long-seam relations do not establish
nonoverlap or force a standard triangular grid. In particular, a unique
angle at a seam junction need not fix the assignment of its two side
lengths. Swapping them can overrun a shorter supporting edge. Any proof
that uses a forced grid must exclude that actual geometric option.

The proposed strict scalar width bound also fails even after placing valid
fans at all three corners. An [exact partial configuration](../../research/attempt-obstructions/THETA_CHORD.md)
has an avoiding long chord and unfilled-side width exceeding that bound.
This does not make the chord an actual tiled seam or show that a swapped
tile fits: its full footprint and edge-partition constraints remain
additional requirements.

## Computational limits

Positive discovery was used to identify general motifs and then followed
by separate exact verification. Limited searches of other caps, the
reversed scale-one F4 target and isosceles targets produced no complete
classification. An exhaustion reported by a discovery engine without an
independently replayed certificate is not promoted here to a negative
theorem. A timeout or checkpoint is not an exclusion.

The remaining task is still to prove a necessary geometric criterion and
a matching positive construction across the unresolved, infinitely many
primitive parameters. Neither the finite search procedure nor another
sufficient tail replaces that implication. The repository continues to
record `full_Erdos634_solved = false`.

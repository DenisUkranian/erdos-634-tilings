# W/beta final synthesis: two precise boundary limitations

7 October 2026. No new tiling or complete scale criterion is claimed.

- [Uniform side-word barrier](BOUNDARY_FILTER_BARRIER.md): every W and
  beta scale m>=2 satisfies whole-side arithmetic, adjacent c-edges,
  corner inventories, and abstract straight-angle completions. At m=1
  the same witnesses work whenever u>=2 and v-u>=2. These are formal
  boundary words, not joint geometric collars or disk certificates.
- [Full formal direction inventory](FORMAL_DIRECTION_BARRIER.md): an
  all-scale restatement of the existing uniform-reduction Theorem E.
  Every W/beta target has a direction inventory with exactly the required
  positive number of tile copies. This was already proved at scale one
  and extends immediately to every scale; it is not new progress.

The existing positive cap constructs v+<u,v>. The actual c/a exchange
uc=va prevents extending short-chain purity past its sharp threshold.
The W56 local escape and universal nine-tile short-side collar show why
local forcing alone has not settled the missing cases. None of the
present formal witnesses removes the need for positional compatibility
or a global construction/descent theorem.

Fresh checks:

    python research/final-synthesis-oct7/w-beta/check_boundary_filter.py
    python research/final-synthesis-oct7/w-beta/check_formal_direction.py

Their aggregate report is `verification.json`. The symbolic direction
identities are coefficientwise; the parameter-loop results are finite
implementation regressions. Neither checker claims nonoverlap.

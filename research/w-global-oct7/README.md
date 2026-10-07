# Group-1 boundary continuation, 7 October 2026

The full problem is not solved. W56 remains unresolved.

- `ADJACENT_C_EDGES.md`: every side of every W, beta-isosceles and
  theta-isosceles tiling contains two consecutive c-edges. All primitive
  pairs and T-junctions are covered. This strengthens the existing
  at-least-two-c-edge result.
- For u=v-1, v>=3, W at scale2 has the unique short-side word c,c,a,a.
  For W56 the correct word runs from (46,20) to (56,0), with two exact
  four-tile orientation roots in `W56-boundary-roots.json`.
- `THETA_BASE_RESIDUES.md`: the old two-c condition on a theta base has
  the exact arithmetic criterion floor(ut/v)>=1 if v-u>=2, and >=2 if
  v-u=1. This is an edge-count criterion, not tiling sufficiency.
- The new rooted W56 searches stopped INCOMPLETE at depths47 and48;
  no negative decision is claimed.

Reproduce the fast arithmetic check:

    python research/w-global-oct7/check_theta_base.py

Reproduce the complete boundary roots without starting a search:

    python research/w-global-oct7/w56_boundary_search.py --seconds 0

Optional bounded runs, whose timeouts mean INCOMPLETE:

    python research/w-global-oct7/w56_boundary_search.py --seconds 240
    python research/w-global-oct7/w56_boundary_search.py --root 1 --seconds 60

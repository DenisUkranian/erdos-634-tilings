# Central height and boundary conditions for the 154 candidate

All computations use exact integers or rational numbers and allow
T-junctions. None claims a complete solution of N=154 or Erdős 634.

* `CENTRAL_HEIGHT.md`: proof that `n_0>=24`. The 28-case finite certificate
  is reproduced by `check_central_eleven.py` and saved in
  `central_eleven_verified.json`. Independent mathematical review by the
  parallel layer-geometry agent found no gap; this is not external review.
* `BASE_BOUNDARY.md`: the complete 2561 base-edge profiles and the stronger
  base-junction angle-fan inventory condition. `check_base_profiles.py`
  independently checks the geometric predicates by rational polygon
  clipping, and `check_fans.py` checks the full ray enumeration against
  independent angle-word counts.
* `probe_central_24.py` and `central24_probe.json`: exhaustive necessary
  supporting-line screen of the 221819 modular inventories of population
  24; 161932 survive. This does not prove a floor of 37.
* `boundary_fan_inventory.py`: an additional exact necessary search for
  one supplied complete unsigned inventory. The `[0,4]` control fails;
  the `[-1,3]` and `[-2,2]` controls pass the relaxation. A timeout is
  explicitly `INCOMPLETE`. These are controls, not a classification of
  the corresponding supports.

No existing proof or frozen prior certificate was modified.

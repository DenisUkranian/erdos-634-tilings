# Compact geometric checkpoints

These files record incomplete unrestricted searches. **No target is
excluded and no full target tiling is represented.** A JSON status value
`solver-inconclusive`, `resource-limit`, or a column cap is not UNSAT.

`INDEX.json` gives each compressed geometric source, its decompressed
SHA-256, and the hash and candidate count of the original full formula
snapshot. The full semantic reports in `../audit/` explicitly name the
original snapshots they checked. An audit of one snapshot must not be
transferred to another by matching only its target number.

`compact_checkpoint.py` retains complete physical rows, queried whole
banks and vertex fans, exact overlap pairs, and supported-cycle witnesses.
It stores only placements referenced by those geometric sources and
renumbers their indices. Regeneration recovers additional candidates from
the complete local catalogues. Original solver assertions, generated-only
columns, and temporary population allocations are omitted.

Consequently a restarted model is a newly generated necessary model,
not a byte-for-byte copy of the old formula. Its own full snapshot must
pass `../audit/verify_snapshot.py` before a purported refutation can be
used. The original root assumptions are never imported by this path.

Example, from the repository root:

```sh
python3 research/2026-11-21/semiprimes/through-contact-closure/spatial/area_search.py \
  --allocation joint 35 13 43 --out /tmp/restarted-5063 \
  --model-checkpoint research/2026-11-21/semiprimes/through-contact-closure/checkpoints/5063_population_area_restart.json.gz
```

The earlier `3431_phase-whole` search loaded the weaker 46-node cap before
the 45-node strengthening was applied. Its recorded status remains valid
as a weaker necessary-model experiment. New target runs and restarts use
45 and 58. The archived intermediate phase audit names its own hash and
does not certify the different final 3431 phase snapshot.

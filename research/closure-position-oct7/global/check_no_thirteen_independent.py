#!/usr/bin/env python3
"""Independent exact finite part of the nonzero-height population-13 obstruction.

Edges are derived from rational coordinates by the earlier independent model.
We do not import the producer's inventory list, orbit table or line bounds.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import check_full_inventory_backward as geometry

HERE = Path(__file__).resolve().parent


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total+1):
        for tail in compositions(total-first, length-1):
            yield (first,)+tail


def main():
    types = []
    for tile_type in range(2):
        for rotation in range(6):
            short = [edge for edge in geometry.EDGES[tile_type][rotation] if edge[0] == 0]
            character = sum(length*(-1)**axis for _, axis, length in short)
            assert abs(character) == 1
            if character == 1:
                e8 = next(edge for edge in short if edge[2] == 8)
                e7 = next(edge for edge in short if edge[2] == 7)
                assert e8[1] % 2 == 0 and e7[1] % 2 == 1
                types.append((tile_type, rotation, e8[1] % 3, e7[1] % 3))
    assert len(types) == 6
    assert {t[2:] for t in types} == {(a, b) for a in range(3) for b in range(3) if a != b}
    pairs = [(a, b) for a in range(14) for b in range(14-a)
             if a+b and (8*a-7*b) % 13 == 0]

    @lru_cache(maxsize=None)
    def max_lines(a, b):
        if a == b == 0:
            return 0
        maximum = -1  # No exact decomposition.
        for x, y in pairs:
            if x <= a and y <= b:
                rest = max_lines(a-x, b-y)
                if rest >= 0:
                    maximum = max(maximum, rest+1)
        return maximum

    records = []
    full_inventories = set()
    enumerated = 0
    for counts in compositions(13, 6):
        enumerated += 1
        eight_totals = [0]*3
        seven_totals = [0]*3
        for count, (_, _, a, b) in zip(counts, types):
            eight_totals[a] += count
            seven_totals[b] += count
        if any((8*a-7*b) % 13 for a, b in zip(eight_totals, seven_totals)):
            continue
        bounds = [max_lines(a, b) for a, b in zip(eight_totals, seven_totals)]
        assert all(bound >= 0 for bound in bounds)
        contradictions = []
        for index, (count, (tile_type, rotation, a, b)) in enumerate(zip(counts, types)):
            if count > bounds[a]*bounds[b]:
                contradictions.append({'type': tile_type, 'rotation': rotation,
                                       'tile_count': count, 'point_bound': bounds[a]*bounds[b]})
        assert contradictions, (counts, eight_totals, seven_totals, bounds)
        record = {'counts_at_positive_character_types': counts,
                  'eight_edge_totals': eight_totals, 'seven_edge_totals': seven_totals,
                  'maximum_line_counts': bounds, 'pigeonhole_contradictions': contradictions}
        records.append(record)
        for half_turn in (0, 3):
            inventory = [0]*12
            for count, (tile_type, rotation, _, _) in zip(counts, types):
                inventory[6*tile_type+(rotation+half_turn) % 6] = count
            full_inventories.add(tuple(inventory))
    assert enumerated == 8568 and len(records) == 54 and len(full_inventories) == 108

    def transform(inventory, rotation, reflect):
        result = [0]*12
        for tile_type in range(2):
            for j in range(6):
                t, k = (1-tile_type, -j-2) if reflect else (tile_type, j)
                result[6*t+(k+rotation) % 6] = inventory[6*tile_type+j]
        return tuple(result)

    unseen = set(full_inventories)
    orbit_sizes = []
    while unseen:
        seed = min(unseen)
        orbit = {transform(seed, rotation, reflection)
                 for rotation in range(6) for reflection in (False, True)}
        assert orbit <= full_inventories
        assert len(orbit) == 12
        unseen -= orbit
        orbit_sizes.append(len(orbit))
    assert len(orbit_sizes) == 9
    report = {'status': 'PASS', 'full_Erdos634_solved': False, 'N154_solved': False,
              'scope': 'Independent exact finite arithmetic plus line-count pigeonhole; geometric line-divisibility lemma is a written input',
              'compositions_tested': enumerated, 'inventories_one_character': len(records),
              'inventories_both_characters': len(full_inventories),
              'dihedral_orbit_sizes': orbit_sizes, 'allowed_nonempty_line_pairs': pairs,
              'geometry_derived_positive_character_types': types,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'geometry_source_sha256': hashlib.sha256(Path(geometry.__file__).read_bytes()).hexdigest(),
              'records': records}
    (HERE/'no_thirteen_independent.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('status', 'compositions_tested', 'inventories_one_character', 'inventories_both_characters', 'dihedral_orbit_sizes')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O so exact assertions execute.')
    main()

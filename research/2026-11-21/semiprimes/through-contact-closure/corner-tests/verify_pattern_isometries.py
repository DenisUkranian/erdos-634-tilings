#!/usr/bin/env python3
"""Independent exact geometry and completeness controls for pattern reuse.

The independent matcher derives its affine multiplier from labelled physical
vertices, then compares Fraction vertex triples. It does not use the native
height/phase transform formulas or the production matching routine.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import copy
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'owned'))
from legacy import core, ROOT
from pattern_isometries import pattern_isometries, pattern_key, transform_area_witness
from verify_long_cycles import U,add,sub,scale,det,norm,mul,power,point,reconstruct
from verify_area_cycles import check_physical,check_witness
from area_cycles import selected_skeleton_faces


def conjugate(p):
    return p[0]+p[1],-p[1]


def labelled(g,tile):
    q,h,j,s = tile
    q = point(g,q)
    rotation = power((F(g.a,g.c),F(g.b,g.c)),h)
    return (add(q,scale(-g.a,mul(rotation,U[j]))),q,
            add(q,scale(g.b,mul(rotation,U[(j+s)%6]))))


def map_fraction(p,source,target,unit,reflected):
    delta = sub(p,source)
    return add(target,mul(unit,conjugate(delta) if reflected else delta))


def native(g,p):
    exponent,denominator = 0,1
    while denominator%p[0].denominator or denominator%p[1].denominator:
        denominator *= g.c
        exponent += 1
    return int(p[0]*denominator),int(p[1]*denominator),exponent


def independent_copy(g,pattern,H,J,reflected,target):
    source = point(g,pattern[0][0])
    unit = mul(power((F(g.a,g.c),F(g.b,g.c)),H),U[J])
    answer = []
    sign = -1 if reflected else 1
    for q,h,j,s in pattern:
        mapped = map_fraction(point(g,q),source,target,unit,reflected)
        tile = native(g,mapped),H+sign*h,(J+sign*j)%6,sign*s
        reconstruct(g,tile)  # Independent metric and board containment.
        answer.append(tile)
    return answer


def independent_occurrences(g,tiles,pattern_indices,anchor=0):
    all_vertices = [labelled(g,tile) for tile in tiles]
    lookup = {vertices:i for i,vertices in enumerate(all_vertices)}
    assert len(lookup) == len(tiles)
    pattern = [all_vertices[i] for i in pattern_indices]
    beta0,q0,alpha0 = pattern[anchor]
    orientation0 = det(sub(beta0,q0),sub(alpha0,q0))
    expected = set()
    for beta,q,alpha in all_vertices:
        reflected = orientation0*det(sub(beta,q),sub(alpha,q)) < 0
        source_vector = sub(beta0,q0)
        if reflected:
            source_vector = conjugate(source_vector)
        unit = scale(F(1,norm(source_vector)),mul(sub(beta,q),conjugate(source_vector)))
        assert norm(unit) == 1
        images = []
        for triangle in pattern:
            mapped = tuple(map_fraction(v,q0,q,unit,reflected) for v in triangle)
            if mapped not in lookup:
                break
            images.append(lookup[mapped])
        else:
            expected.add(tuple(sorted(images)))
    return expected


def check_occurrence(g,tiles,occurrence):
    transform = occurrence['transform']
    source = point(g,transform['source_anchor'])
    target = point(g,transform['target_anchor'])
    unit = mul(power((F(g.a,g.c),F(g.b,g.c)),transform['unit_height']),
               U[transform['unit_direction']])
    assert norm(unit) == 1
    assert sorted(occurrence['image_indices']) == occurrence['indices']
    for before,after in zip(occurrence['pattern_indices'],occurrence['image_indices']):
        first,last = labelled(g,tiles[before]),labelled(g,tiles[after])
        mapped = tuple(map_fraction(v,source,target,unit,transform['reflected']) for v in first)
        # The beta/obtuse/alpha labels are checked separately. A reflected
        # CCW order cannot accidentally pass as a direct labelled mapping.
        assert mapped == last
        assert all(norm(sub(mapped[i],mapped[j])) == norm(sub(first[i],first[j]))
                   for i,j in ((0,1),(1,2),(0,2)))


def benchmark_snapshot(path,source_patterns):
    """Time native matching; independently check every returned occurrence."""
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1<<20),b''):
            digest.update(block)
    with path.open() as stream:
        data = json.load(stream)
    assert data['sides'] == source_patterns['sides']
    g = core.Geometry(*data['sides'])
    tiles = [(tuple(t[0]),*t[1:]) for t in data['tiles']]
    index = {tile:i for i,tile in enumerate(tiles)}
    assert len(index) == len(tiles)
    report = []
    for pattern in source_patterns['patterns']:
        source = [(tuple(t[0]),*t[1:]) for t in pattern['tiles']]
        indices = [index[tile] for tile in source]
        witness = copy.deepcopy(pattern['witness'])
        witness['indices'] = sorted(indices)
        for edge in witness['edges']:
            edge['representative'] = indices[edge['representative']]
            edge['selected_owners'] = [indices[i] for i in edge['selected_owners']]
        start = time.perf_counter()
        occurrences = pattern_isometries(g,tiles,index,indices)
        seconds = time.perf_counter()-start
        for occurrence in occurrences:
            check_occurrence(g,tiles,occurrence)
            expanded = transform_area_witness(g,witness,occurrence)
            check_witness(g,tiles,occurrence['indices'],expanded)
        item = dict(pattern_id=pattern['id'],supporting_tiles=len(indices),
                    tile_area_ratio=witness['tile_area_ratio'],occurrences=len(occurrences),
                    seconds=round(seconds,6),
                    direct=sum(not o['transform']['reflected'] for o in occurrences),
                    reflected=sum(o['transform']['reflected'] for o in occurrences),
                    all_returned_labelled_isometries_checked=True,
                    all_expanded_polygon_witnesses_checked=True)
        print('BENCHMARK',json.dumps(item,sort_keys=True),flush=True)
        report.append(item)
    return dict(status='PASS',source_snapshot_sha256=digest.hexdigest(),candidate_count=len(tiles),
                patterns=report,total_scan_seconds=round(sum(r['seconds'] for r in report),6),
                new_placements_inserted=0,full_target_excluded=False,
                timing_scope='Native occurrence enumeration only; independent checking is outside this timing.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot',type=Path,
                        help='Optional existing 5063 snapshot for the full catalogue benchmark.')
    parser.add_argument('--benchmark-out',type=Path,
                        default=HERE/'PATTERN_ISOMETRY_BENCHMARK.json')
    args = parser.parse_args()
    data = json.loads((HERE/'ISOMETRY_SOURCE_PATTERNS_5063.json').read_text())
    additional = json.loads((HERE/'ISOMETRY_SOURCE_PATTERNS_3431.json').read_text())
    source_records = [(data['sides'],record) for record in data['patterns']]
    source_records += [(additional['sides'],record) for record in additional['patterns']]
    reports = []
    cases = [(False,0,0),(False,0,1),(False,-5,2),(False,7,5),
             (True,0,0),(True,-5,2),(True,7,5),(True,1,3)]
    for sides,record in source_records:
        g = core.Geometry(*sides)
        pattern = [(tuple(t[0]),*t[1:]) for t in record['tiles']]
        source_indices = list(range(len(pattern)))
        check_physical(g,pattern,source_indices)
        check_witness(g,pattern,source_indices,record['witness'])
        tiles = list(pattern)
        for k,(reflected,H,J) in enumerate(cases):
            target = F(g.A//3+3*k),F(g.B//3+5*k)
            for tile in independent_copy(g,pattern,H,J,reflected,target):
                if tile not in tiles:
                    tiles.append(tile)
        index = {tile:i for i,tile in enumerate(tiles)}
        before = len(tiles),len(index)
        occurrences = pattern_isometries(g,tiles,index,source_indices)
        assert (len(tiles),len(index)) == before
        expected = independent_occurrences(g,tiles,source_indices)
        assert {tuple(o['indices']) for o in occurrences} == expected
        other_anchor = pattern_isometries(g,tiles,index,source_indices,anchor=len(pattern)-1)
        assert {tuple(o['indices']) for o in other_anchor} == expected
        key = pattern_key(g,tiles,source_indices)
        for occurrence in occurrences:
            check_occurrence(g,tiles,occurrence)
            assert pattern_key(g,tiles,occurrence['indices']) == key
            expanded = transform_area_witness(g,record['witness'],occurrence)
            check_witness(g,tiles,occurrence['indices'],expanded)
            assert expanded['tile_area_ratio'] == record['witness']['tile_area_ratio']
        broken = copy.deepcopy(occurrences[0])
        broken['transform']['reflected'] = not broken['transform']['reflected']
        try:
            check_occurrence(g,tiles,broken)
        except AssertionError:
            pass
        else:
            raise AssertionError('An incorrect reflection witness was accepted.')
        partial_copy = independent_copy(g,pattern,2,4,True,(F(g.A//3),F(g.B//3)))
        incomplete = pattern+partial_copy[:-1]
        incomplete_index = {tile:i for i,tile in enumerate(incomplete)}
        missing = pattern_isometries(g,incomplete,incomplete_index,source_indices)
        assert {tuple(o['indices']) for o in missing} == {tuple(source_indices)}
        reports.append(dict(N=g.N,id=record['id'],source_support_size=len(pattern),
                            test_catalogue_size=len(tiles),occurrences=len(occurrences),
                            independent_complete_enumeration=True,
                            direct=any(not o['transform']['reflected'] for o in occurrences),
                            reflected=any(o['transform']['reflected'] for o in occurrences),
                            rotations_and_heights=[-5,0,1,7],anchor_choice_invariant=True,
                            exact_labelled_vertices_and_side_support=True,
                            missing_member_not_inserted=True,bad_reflection_rejected=True))

    seeds = []
    for N in (3431,5063):
        seed = json.loads((HERE/f'ISOMETRY_SEEDS_{N}.json').read_text())
        geometry = core.Geometry(*seed['sides'])
        tiles = [(tuple(t[0]),*t[1:]) for t in seed['tiles']]
        keys = set()
        for witness in seed['general_area_cycle_cuts']:
            check_physical(geometry,tiles,witness['indices'])
            check_witness(geometry,tiles,witness['indices'],witness)
            assert witness['budget']['violations']
            key = pattern_key(geometry,tiles,witness['indices'])
            assert key not in keys
            keys.add(key)
        seeds.append(dict(N=N,candidate_tiles=len(tiles),noncongruent_patterns=len(keys),
                          sha256=hashlib.sha256((HERE/f'ISOMETRY_SEEDS_{N}.json').read_bytes()).hexdigest()))

    control = json.loads((ROOT/'research/2026-11-21/semiprimes/continued-rigidity/physical/CONTROL_143.json').read_text())
    geometry = core.Geometry(*control['sides'])
    tiles = [(tuple(t[0]),*t[1:]) for t in control['tiles']]
    index = {tile:i for i,tile in enumerate(tiles)}
    occurrences = pattern_isometries(geometry,tiles,index,[0])
    assert len(occurrences) == 143
    for occurrence in occurrences:
        check_occurrence(geometry,tiles,occurrence)
    valid = next(selected_skeleton_faces(geometry,tiles,[0]))
    assert not valid['budget']['violations']
    try:
        transform_area_witness(geometry,valid,occurrences[0])
    except ValueError:
        pass
    else:
        raise AssertionError('A compatible polygon was promoted into a no-good.')
    report = dict(status='PASS',source_patterns=reports,seeds=seeds,
                  control143=dict(actual_triangle_images=143,all_labelled_isometries_valid=True,
                                  valid_source_cannot_be_promoted_to_no_good=True,rejected=False),
                  full_target_excluded=False,
                  scope='Exact local obstruction reuse. No target or complete corner-root exclusion.')
    (HERE/'PATTERN_ISOMETRY_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if args.snapshot:
        benchmark = benchmark_snapshot(args.snapshot,data)
        args.benchmark_out.write_text(json.dumps(benchmark,indent=2)+'\n')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O: exact assertions are required.')
    main()

#!/usr/bin/env python3
"""Exact controls of mandatory-bank pair, node, and height reserves.

No target tiling decision is made. Uses two complete positive 143 controls,
all local long-side choices, and independent integer reserve checks.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CONT = ROOT / 'research/2026-11-20/semiprimes/continuation'
sys.path[:0] = [str(CONT / 'global-endpoints/integer'),
                str(CONT / 'vertex-phase')]
from global_core_sat import Geometry
from phase_budget import PhaseBudget


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bank = load('audited_long_bank', HERE.parent / 'long-banks/long_bank_completion.py')
control = load('existing_contact_control', ROOT / 'research/2026-11-21/semiprimes/global-closure-next/contact-budget/verify_contact_budget.py')


def epsilon(tile):
    return tile[3] * (-1 if tile[2] % 2 else 1)


def point(g, p):
    return F(p[0], g.c ** p[2]), F(p[1], g.c ** p[2])


def native_point(g, p):
    exponent = 0
    while (p[0] * g.c ** exponent).denominator != 1 or (p[1] * g.c ** exponent).denominator != 1:
        exponent += 1
        assert exponent <= 20
    return g.point(int(p[0] * g.c ** exponent), int(p[1] * g.c ** exponent), exponent)


def identify(g, polygon, heights):
    vertices = {native_point(g, p) for p in polygon}
    matches = []
    for q in vertices:
        for h in heights:
            for j in range(6):
                for s in (-1, 1):
                    tile = q, h, j, s
                    if set(g.vertices(tile)) == vertices:
                        matches.append(tile)
    assert len(matches) == 1, matches
    return matches[0]


def node_reserve(c, rows):
    """Rows: (mandatory+, mandatory-, residue+, residue-, ordinary_required)."""
    dplus = dminus = extra_blocks = 0
    for positive, negative, rplus, rminus, ordinary in rows:
        assert positive >= 0 and negative >= 0
        dp, dn = (rplus-positive) % c, (rminus-negative) % c
        dplus += dp
        dminus += dn
        if ordinary:
            assert rplus == rminus == 0
            rounded = positive+negative+dp+dn
            assert rounded % c == 0
            extra_blocks += max(0, 2-rounded//c)
    assert (dplus-dminus) % c == 0
    direct = min(max(dplus+c*j, dminus+c*(extra_blocks-j))
                 for j in range(extra_blocks+1))
    difference = abs(dplus-dminus)//c
    closed = max(dplus,dminus) + c*((max(0,extra_blocks-difference)+1)//2)
    assert direct == closed
    return dict(positive_deficit=dplus, negative_deficit=dminus,
                extra_blocks=extra_blocks, minimum_pairs=closed,
                pair_residue=closed % c)


def height_reserve(c, d, mandatory):
    """Keys are even short heights divided by two; standard-frame charge."""
    assert sum(mandatory.values()) == -d
    lower = min([0, *mandatory])
    upper = max([0, *mandatory])
    prefix = 0
    score = 0
    flows = {}
    for h in range(lower, upper+1):
        prefix += mandatory.get(h, 0)
        residue = (-d*(h >= 0)-prefix) % c
        nearest = residue if 2*residue <= c else residue-c
        flows[h] = nearest
        score += abs(nearest)
    assert flows[upper] == 0
    full_charge = {}
    previous = 0
    for h in range(lower, upper+1):
        full_charge[h] = mandatory.get(h,0)+flows[h]-previous
        assert (full_charge[h]+d*(h == 0)) % c == 0
        previous = flows[h]
    assert sum(full_charge.values()) == -d
    return dict(minimum_pairs=score, least_prefix_flows=flows,
                congruent_full_height_charges=full_charge)


def local_choices():
    counts = []
    for a,b,c in ((5,3,7),(33,7,37),(35,13,43)):
        g = Geometry(a,b,c)
        checked = 0
        for long_height in (-3,-1,1,3):
            for j in range(6):
                # This tile has positive CCW long direction at (long_height,j).
                original = g.point(0,0,0), long_height+1, j, -1
                poly = tuple(point(g,p) for p in g.vertices(original))
                long_edges = [(p,q) for p,q in zip(poly,poly[1:]+poly[:1])
                              if bank.norm(bank.sub(q,p)) == c*c]
                assert len(long_edges) == 1
                p,q = long_edges[0]
                for coefficient in (1,-1):
                    segment = dict(p=p,q=q,coefficient=coefficient)
                    choices = bank.triangle_choices(segment,a,b,c)
                    labels = [identify(g,triangle,(long_height-1,long_height+1))
                              for triangle in choices]
                    assert {t[1] for t in labels} == {long_height-1,long_height+1}
                    assert {epsilon(t) for t in labels} == {coefficient*epsilon(original)}
                    if coefficient == 1:
                        assert frozenset(poly) in {frozenset(t) for t in choices}
                    checked += 2
        counts.append(dict(tile=[a,b,c], choices_checked=checked))
    return counts


def full_control(which):
    g = Geometry(5,3,7)
    tiles, source = control.read_tiles(g,which)
    polys, _, _, _, _ = control.check_full_tiling(g,tiles)
    odd_ids = [i for i,t in enumerate(tiles) if t[1] % 2]
    even_ids = [i for i,t in enumerate(tiles) if not t[1] % 2]
    segments,residual = bank.reconstruct([polys[i] for i in odd_ids],g.a,g.b,g.c)
    assert not residual and not bank.capacity_conflicts(segments)
    mandatory = {tuple(sorted((s['p'],s['q']))): s for s in segments}
    assert len(mandatory) == len(segments)
    groups = defaultdict(list)
    for i in even_ids:
        poly = tuple(polys[i])
        edge = [(p,q) for p,q in zip(poly,poly[1:]+poly[:1])
                if bank.norm(bank.sub(q,p)) == g.c*g.c]
        assert len(edge) == 1
        p,q = edge[0]
        groups[tuple(sorted((p,q)))].append((i,p,q))
    selected = []
    pairs = []
    for endpoints, members in groups.items():
        assert len(members) in (1,2)
        if len(members) == 2:
            (i,p,q),(j,u,v) = members
            assert (p,q) == (v,u)
            assert epsilon(tiles[i])+epsilon(tiles[j]) == 0
            assert abs(tiles[i][1]-tiles[j][1]) in (0,2)
            assert endpoints not in mandatory
            pairs.append((i,j))
        else:
            i,p,q = members[0]
            segment = mandatory[endpoints]
            required = (segment['p'],segment['q'])
            if segment['coefficient'] == -1:
                required = required[::-1]
            assert (p,q) == required
            assert frozenset(polys[i]) in {
                frozenset(t) for t in bank.triangle_choices(segment,g.a,g.b,g.c)}
            selected.append(i)
    assert len(selected) == len(segments)
    assert len(even_ids) == len(segments)+2*len(pairs)
    assert sum(epsilon(tiles[i]) for i in selected) == -(g.a-g.b)
    assert sum(epsilon(tiles[i]) for i in odd_ids) == -g.c
    reports = []
    rplus = (g.N-g.a+g.b)*pow(2,-1,g.c) % g.c
    rminus = (g.N+g.a-g.b)*pow(2,-1,g.c) % g.c
    for tree in (-1,1):
        phase = PhaseBudget(g,tree)
        core = phase.node(g.point(0,0,0),0)
        counts = defaultdict(lambda:[0,0])
        counts[core]
        for i in selected:
            tile = tiles[i]
            counts[phase.node(tile[0],tree*tile[1])][epsilon(tile)<0] += 1
        rows = [(p,q,rplus if v == core else 0,rminus if v == core else 0,v != core)
                for v,(p,q) in counts.items()]
        result = node_reserve(g.c,rows)
        assert result['minimum_pairs'] <= len(pairs)
        assert len(pairs) % g.c == result['pair_residue']
        reports.append(dict(tree=tree, **result))
    m = Counter()
    full = Counter()
    for i in selected:
        m[tiles[i][1]//2] += epsilon(tiles[i])
    for i in even_ids:
        full[tiles[i][1]//2] += epsilon(tiles[i])
    height = height_reserve(g.c,g.a-g.b,m)
    assert height['minimum_pairs'] <= len(pairs)
    cross_pairs = [(i,j) for i,j in pairs if tiles[i][1] != tiles[j][1]]
    lower,upper = min([0,*m,*full]),max([0,*m,*full])
    flow = 0
    actual_cost = 0
    for h in range(lower,upper+1):
        flow += full[h]-m[h]
        crossing = [(i,j) for i,j in cross_pairs
                    if min(tiles[i][1],tiles[j][1])//2 <= h < max(tiles[i][1],tiles[j][1])//2]
        assert abs(flow) <= len(crossing)
        actual_cost += abs(flow)
    assert flow == 0 and actual_cost <= len(cross_pairs) <= len(pairs)
    return dict(control=which, source=source, odd_tiles=len(odd_ids),
                mandatory_even_tiles=len(segments), residual_even_pairs=len(pairs),
                mandatory_even_charge=sum(epsilon(tiles[i]) for i in selected),
                exact_total=len(odd_ids)+len(segments)+2*len(pairs),
                prime_tree_reserves=reports, height_transport=height)


def arithmetic_controls():
    tested = 0
    for c in (7,37,43):
        for residue in range(c):
            for bp in range(8):
                for bn in range(8):
                    dplus,dminus = residue+c*bp,residue+c*bn
                    for t in range(13):
                        direct = min(max(dplus+c*j,dminus+c*(t-j)) for j in range(t+1))
                        closed = max(dplus,dminus)+c*((max(0,t-abs(bp-bn))+1)//2)
                        assert direct == closed
                        assert direct % c == residue
                        tested += 1
    # Required but as yet empty nodes contribute two full sign blocks.
    examples = []
    for c,rplus,rminus,d in ((37,19,8,26),(43,5,27,22)):
        rows = [(0,d,rplus,rminus,False),(0,0,0,0,True)]
        example = node_reserve(c,rows)
        assert example['extra_blocks'] == 2
        examples.append(dict(c=c, required_empty_node=example))
    heights = []
    for c,d,m in ((37,26,{-2:17,0:-43}),
                  (37,26,{-1:20,0:-46}),
                  (43,22,{-2:21,0:-43})):
        result = height_reserve(c,d,m)
        heights.append(dict(c=c, mandatory_charge_by_half_height=m, **result))
    assert [e['minimum_pairs'] for e in heights] == [34,17,42]
    variations = []
    for N,c,d,rplus,expected in ((3431,37,26,19,53),(5063,43,22,5,77)):
        surviving = []
        for variation in range(1,N//c+1,2):
            required_positive = d*(variation-1)//2
            rounded_positive = rplus+c*((required_positive-rplus+c-1)//c)
            assert rounded_positive >= required_positive
            assert rounded_positive-c < required_positive
            even_minimum = 2*rounded_positive+d
            assert even_minimum >= d*variation
            if c*variation+even_minimum <= N:
                surviving.append(dict(variation=variation,
                                      odd_minimum=c*variation,
                                      even_minimum=even_minimum,
                                      remaining_tiles=N-c*variation-even_minimum))
        assert surviving[-1]['variation'] == expected
        if N == 5063:
            assert surviving[-1] == dict(variation=77,odd_minimum=3311,
                                         even_minimum=1752,remaining_tiles=0)
        variations.append(dict(target=N,largest_allowed_variation=expected,
                               extremal_budget=surviving[-1]))
    return dict(closed_form_cases=tested, empty_node_examples=examples,
                nonzero_height_examples=heights,charge_variation_bounds=variations)


if __name__ == '__main__':
    report = dict(status='PASS', target_status='Both original target counts remain OPEN',
                  local_choices=local_choices(),
                  positive_controls=[full_control('known'),full_control('macro')],
                  arithmetic=arithmetic_controls(),
                  scope='Exact local and positive-control checks of a necessary complete-odd bank theorem; no enumeration of all odd packings.')
    (HERE/'BANK_PAIR_RESERVE_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

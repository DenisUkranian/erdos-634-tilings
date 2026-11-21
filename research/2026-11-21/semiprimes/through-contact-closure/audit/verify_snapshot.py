#!/usr/bin/env python3
"""Independently regenerate the finite owned-through model's necessary clauses.

This verifier imports no search geometry, inverse placement enumeration,
corner oracle, SMT solver, or candidate generator.  Geometric catalogues are
reconstructed from exact side lengths, dot products and determinants.
The mathematical orientation/integer-offset theorems remain explicit inputs
to this finite audit; see README.md.  A PASS is not an UNSAT result.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import gzip
from itertools import combinations
import json
from math import gcd,isqrt
from pathlib import Path
import sys
import time

from proof_cnf import parse
from through_geometry import ExactGeometry, add, sub, scale, det, norm, canonical, overlap_open, interior, common_vertex_interior

ROOT = Path(__file__).resolve().parents[5]


def freeze(value):
    return tuple(freeze(x) for x in value) if isinstance(value, list) else value


def read_snapshot_bytes(path):
    raw = Path(path).read_bytes()
    return gzip.decompress(raw) if raw.startswith(b'\x1f\x8b') else raw


def normalized(node):
    """Only elementary, independently valid Boolean syntactic identities."""
    if isinstance(node, str):
        return node
    op, *args = node
    args = [normalized(x) for x in args]
    if isinstance(op, tuple):
        if op[1] == 'pble':
            assert len(op) == len(args)+3
            # A weight belongs to its literal. Reordering only the literals
            # would silently change a weighted inequality's meaning.
            pairs = tuple(sorted(((int(w),a) for w,a in zip(op[3:],args)),key=repr))
            return 'weighted-pble',int(op[2]),pairs
        return op, tuple(sorted(args, key=repr))
    if op == 'not':
        assert len(args) == 1
        if args[0] in ('true', 'false'):
            return 'false' if args[0] == 'true' else 'true'
        if isinstance(args[0], tuple) and args[0][0] == 'not':
            return args[0][1]
        return op, args[0]
    if op in ('and', 'or'):
        identity, zero = ('true', 'false') if op == 'and' else ('false', 'true')
        flat = []
        for value in args:
            if value == zero:
                return zero
            if value == identity:
                continue
            if isinstance(value, tuple) and value[0] == op:
                flat.extend(value[1:])
            else:
                flat.append(value)
        flat = tuple(sorted(set(flat), key=repr))
        return identity if not flat else flat[0] if len(flat) == 1 else (op, *flat)
    if op == '=':
        return op, *sorted(args, key=repr)
    return op, *args


def logical(source):
    return normalized(parse(source))


def combine(op, terms):
    terms = list(dict.fromkeys(terms))
    identity, zero = ('true', 'false') if op == 'and' else ('false', 'true')
    if zero in terms:
        return zero
    terms = [x for x in terms if x != identity]
    return identity if not terms else terms[0] if len(terms) == 1 else '(' + op + ' ' + ' '.join(terms) + ')'


def atmost(bound, terms):
    terms = list(terms)
    if bound >= len(terms):
        return 'true'
    if bound < 0:
        return 'false'
    if not bound:
        return '(not (or ' + ' '.join(terms) + '))'
    return f'((_ at-most {bound}) ' + ' '.join(terms) + ')'


def equal(bound, terms):
    terms = list(terms)
    if not terms:
        return 'true' if not bound else 'false'
    if not 0 <= bound <= len(terms):
        return 'false'
    if not bound:
        return atmost(0, terms)
    if bound == len(terms):
        return '(and ' + ' '.join(terms) + ')'
    return f'((_ pbeq {bound}' + ' 1' * len(terms) + ') ' + ' '.join(terms) + ')'


def weighted_atmost(bound,weights,terms):
    weights,terms = list(weights),list(terms)
    assert len(weights) == len(terms) and all(w>0 for w in weights)
    if not terms or sum(weights) <= bound:
        return 'true'
    if bound < 0:
        return 'false'
    return f'((_ pble {bound} '+ ' '.join(map(str,weights))+') '+ ' '.join(terms)+')'


def advance(ray, aa, bb):
    h, j = ray
    return h - aa + bb, (j + aa) % 6


def ccw(polygon):
    return polygon if det(sub(polygon[1], polygon[0]), sub(polygon[2], polygon[0])) > 0 else polygon[::-1]


class IndependentPhase:
    """Residue classes from exhaustive unique digit lifting, no search import."""
    def __init__(self,g,sign):
        self.g,self.sign,self.c = g,sign,g.c
        assert sign in (-1,1)
        roots = [r for r in range(g.c) if (r*r-r+1)%g.c == 0]
        positive, = [r for r in roots if (g.a+g.b*r)%g.c == 0]
        negative, = [r for r in roots if r != positive]
        self.lifts = {1:positive if sign==1 else negative}
        self.outer = (((0,0,0),0),((g.A,0,0),2*sign),((0,g.B,0),0))

    def root(self,precision):
        while len(self.lifts)<precision:
            n = len(self.lifts)
            modulus = self.c**n
            choices = [self.lifts[n]+digit*modulus for digit in range(self.c)
                       if ((self.lifts[n]+digit*modulus)**2-(self.lifts[n]+digit*modulus)+1)%(modulus*self.c)==0]
            assert len(choices) == 1
            self.lifts[n+1] = choices[0]
        return self.lifts[precision]

    @lru_cache(None)
    def node(self,point,level):
        x,y,e = point
        precision = e+level
        if precision <= 0:
            return level,0,0
        value = (x+y*self.root(precision))%(self.c**precision)
        while e and value%self.c == 0:
            value //= self.c
            e -= 1
        return level,value,e

    def exterior_free(self,node):
        level = node[0]
        return all(level>h or self.node(p,level)!=node for p,h in self.outer)

    @lru_cache(None)
    def required(self,tile):
        p,h,_,_ = tile
        start = min(1-p[2],1+min(hh for _,hh in self.outer))
        return tuple(at for level in range(start,self.sign*h+1)
                     if self.exterior_free(at:=self.node(p,level)))


class SnapshotAudit:
    def __init__(self, model):
        self.model = model
        self.g = ExactGeometry(*model['sides'])
        assert model['N'] == self.g.N
        assert model['unrestricted_heights'] is True
        assert model['fixed_odd_population'] is None
        assert model['temporary_row_equations'] is False
        self.tiles = [freeze(t) for t in model['tiles']]
        assert len(set(self.tiles)) == len(self.tiles), 'Duplicate encoded tile variables'
        self.polygons = [self.g.polygon(t) for t in self.tiles]
        self.polygon_keys = [canonical(p) for p in self.polygons]
        self.index = {p: i for i,p in enumerate(self.polygon_keys)}
        assert len(self.index) == len(self.tiles), 'Duplicate physical triangle variables'
        assert all(self.g.admissible_polygon(p) for p in self.polygons), 'Inadmissible placement'
        self.expected = set()
        self.stats = Counter(tiles=len(self.tiles))
        self.phase_caps = []
        self.population_caps = []
        self.fans = {}
        for record in model['fan_paths']:
            key = self.g.point(record['point']), tuple(record['start']), tuple(record['target'])
            assert key not in self.fans, 'Duplicate fan state'
            self.fans[key] = record

    def add_clause(self, source):
        value = logical(source)
        if value != 'true':
            self.expected.add(value)

    def ids(self, polygons, label):
        missing = {p for p in polygons if p not in self.index}
        assert not missing, f'Incomplete {label}: {len(missing)} missing whole tiles'
        return {self.index[p] for p in polygons}

    @lru_cache(None)
    def endpoint_ids(self, p, ray):
        return frozenset(self.ids(self.g.endpoint_candidates(p, ray), 'endpoint catalogue'))

    def boundary(self):
        assert self.model['boundary_complete'] is True
        O, X, Y = self.g.board
        for start, end, length, ray in ((O,X,self.g.A,(0,0)), (X,Y,self.g.c**2,(2,1)), (Y,O,self.g.B,(0,4))):
            unit = scale(F(1,length), sub(end,start))
            assert unit == self.g.unit(*ray)
            banks = [set() for _ in range(length)]
            for k in range(length+1):
                if not (self.g.coin[k] and self.g.coin[length-k]):
                    continue
                p = add(start,scale(k,unit))
                for i in self.endpoint_ids(p,ray):
                    offsets = []
                    for vertex in self.polygons[i]:
                        delta = sub(vertex,start)
                        if det(unit,delta) == 0:
                            t = delta[0]/unit[0] if unit[0] else delta[1]/unit[1]
                            assert t.denominator == 1
                            offsets.append(int(t))
                    assert len(offsets) == 2
                    lo, hi = sorted(offsets)
                    if lo == k:
                        for t in range(lo,hi):
                            banks[t].add(i)
            for bank in banks:
                self.add_clause(equal(1, (f'x{i}' for i in sorted(bank))))
            self.stats['boundary_unit_intervals'] += length

    def rows(self):
        O,X,Y = self.g.board
        needs = Counter()
        for start,end,ray in ((O,X,(0,0)),(X,Y,(2,1)),(Y,O,(0,1))):
            needs[start,*ray] -= 1
            needs[end,*ray] += 1
        seen = set()
        for encoded,h,j in self.model['complete_rows']:
            assert j in (0,1,2)
            p, ray = self.g.point(encoded), (h,j)
            key = p,h,j
            assert key not in seen
            seen.add(key)
            positives,negatives = [],[]
            wedges = defaultdict(list)
            u = self.g.unit(*ray)
            for i in self.endpoint_ids(p,ray):
                polygon = self.polygons[i]
                assert p in polygon
                coefficient = None
                for a,b in zip(polygon,polygon[1:]+polygon[:1]):
                    if p not in (a,b) or det(sub(b,a),u):
                        continue
                    assert coefficient is None
                    coefficient = -1 if p == a else 1
                    other = b if p == a else a
                    third, = [v for v in polygon if v not in (p,other)]
                    delta = sub(other,p)
                    along = delta[0]/u[0] if u[0] else delta[1]/u[1]
                    across = det(u,sub(third,p))
                    assert along and across
                    wedges[along>0,across>0].append(i)
                assert coefficient in (-1,1)
                (positives if coefficient == 1 else negatives).append(i)
            positives,negatives = tuple(sorted(positives)),tuple(sorted(negatives))
            target = needs[key]
            if not target and negatives < positives:
                positives,negatives = negatives,positives
            self.add_clause(equal(len(negatives)+target,
                [f'x{i}' for i in positives]+[f'(not x{i})' for i in negatives]))
            for indices in wedges.values():
                self.add_clause(atmost(1,(f'x{i}' for i in sorted(indices))))
            self.stats['complete_endpoint_rows'] += 1

    @lru_cache(None)
    def outgoing(self,p,ray):
        result = []
        u = self.g.unit(*ray)
        for raw in self.g.endpoint_candidates(p,ray):
            polygon = ccw(raw)
            k = polygon.index(p)
            first,second = sub(polygon[(k+1)%3],p),sub(polygon[(k+2)%3],p)
            if det(u,first):
                continue
            length = first[0]/u[0] if u[0] else first[1]/u[1]
            if length <= 0:
                continue
            assert length in (self.g.a,self.g.b,self.g.c)
            other, = [v for v in (self.g.a,self.g.b,self.g.c) if v*v == norm(second)]
            pair = frozenset((int(length),other))
            angle = (1,0) if pair == frozenset((self.g.b,self.g.c)) else (0,1) if pair == frozenset((self.g.a,self.g.c)) else (2,2)
            assert second == scale(other,self.g.unit(*advance(ray,*angle)))
            result.append((raw,angle))
        assert len(result) <= 6
        return tuple(result)

    def fan_term(self,p,start,target):
        key = p,start,target
        assert key in self.fans, ('Missing fan subproblem',key)
        return self.fans[key]['term']

    def fan_definitions(self):
        symbols = set()
        for (p,start,target),record in self.fans.items():
            A,B = target
            assert 0 <= A <= 6 and 0 <= B <= 6
            terms = []
            if (A,B) == (0,0):
                expression = 'true'
            else:
                for polygon,(aa,bb) in self.outgoing(p,start):
                    if aa>A or bb>B:
                        continue
                    child = self.fan_term(p,advance(start,aa,bb),(A-aa,B-bb))
                    if child != 'false':
                        assert polygon in self.index, 'Missing viable fan tile'
                        terms.append(combine('and',(f'x{self.index[polygon]}',child)))
                expression = combine('or',terms)
            assert logical(record['expression']) == logical(expression), 'Incorrect full fan recursion'
            term = record['term']
            if term.startswith('cf'):
                assert term not in symbols
                symbols.add(term)
                self.add_clause(f'(= {term} {expression})')
            else:
                assert logical(term) == logical(expression), 'Incorrect inline fan expression'
        self.stats['fan_states'] = len(self.fans)
        self.stats['fan_auxiliaries'] = len(symbols)

    def board_sector(self,p):
        O,X,Y = self.g.board
        if p == O: return (0,0),(1,1)
        if p == X: return (2,1),(2,0)
        if p == Y: return (0,4),(0,2)
        x,y = p
        if y == 0: return (0,0),(3,3)
        if x == 0: return (0,4),(3,3)
        if self.g.B*x+self.g.A*y == self.g.A*self.g.B: return (2,1),(3,3)
        return None

    def tile_sector(self,i,p):
        polygon = self.polygons[i]
        assert p in polygon
        k = polygon.index(p)
        delta = sub(polygon[(k+1)%3],p)
        h = self.tiles[i][1]
        matches = [(H,j) for H in range(h-1,h+2) for j in range(6)
                   if any(delta == scale(length,self.g.unit(H,j)) for length in (self.g.a,self.g.b,self.g.c))]
        assert len(matches) == 1
        start, = matches
        angles = [angle for raw,angle in self.outgoing(p,start) if self.index.get(raw) == i]
        assert len(angles) == 1
        return start,angles[0]

    def owners_and_corner_roots(self):
        catalogues = {}
        for record in self.model['owner_catalogues']:
            p,ray = self.g.point(record['point']),tuple(record['ray'])
            key = p,ray
            assert key not in catalogues
            expected = self.ids(self.g.owners(p,ray),'through-owner catalogue')
            indices = record['indices']
            assert len(set(indices)) == len(indices) and set(indices) == expected
            catalogues[key] = indices
        for record in self.model['owner_cliques']:
            key = self.g.point(record['point']),tuple(record['ray'])
            assert key in catalogues and set(record['indices']) == set(catalogues[key])
            self.add_clause(atmost(1,(f'x{i}' for i in record['indices'])))
        for record in self.model['corner_roots']:
            i,p = record['tile'],self.g.point(record['point'])
            start,(aa,bb) = self.tile_sector(i,p)
            end = advance(start,aa,bb)
            boundary = self.board_sector(p)
            alternatives = []
            if boundary is not None:
                wall,(A,B) = boundary
                for x in range(A-aa+1):
                    for y in range(B-bb+1):
                        if advance(wall,x,y) == start:
                            alternatives.append(combine('and',(
                                self.fan_term(p,wall,(x,y)),
                                self.fan_term(p,end,(A-aa-x,B-bb-y)))))
            else:
                alternatives.append(self.fan_term(p,end,(6-aa,6-bb)))
                for x in range(4-aa):
                    for y in range(4-bb):
                        ray = advance(start,-x,-y)
                        if not self.g.owners(p,ray):
                            continue
                        left = self.fan_term(p,ray,(x,y))
                        right = self.fan_term(p,end,(3-aa-x,3-bb-y))
                        if 'false' in (left,right):
                            continue
                        assert (p,ray) in catalogues, 'Missing viable half-fan owner catalogue'
                        owner = combine('or',(f'x{k}' for k in catalogues[p,ray]))
                        alternatives.append(combine('and',(left,right,owner)))
            clause = f'(=> x{i} {combine("or",alternatives)})'
            assert logical(record['clause']) == logical(clause), 'Incorrect owned corner implication'
            self.add_clause(clause)
        self.stats['owned_corner_roots'] = len(self.model['corner_roots'])
        self.stats['complete_owner_catalogues'] = len(catalogues)

    def exclusion_cliques(self):
        for record in self.model['angular_cliques']:
            p,indices = self.g.point(record['point']),record['indices']
            assert len(set(indices)) == len(indices)
            assert all(p in self.polygons[i] for i in indices)
            # A common open cone is sufficient for pairwise interior overlap,
            # independently of the production angular-cell sweep.
            assert common_vertex_interior(p,[self.polygons[i] for i in indices])
            self.add_clause(atmost(1,(f'x{i}' for i in indices)))
        for i,j in self.model['overlap_pairs']:
            assert i != j and overlap_open(self.polygons[i],self.polygons[j])
            self.add_clause(f'(not (and x{i} x{j}))')
        for record in self.model.get('interior_point_cliques',[]):
            p,indices = tuple(map(F,record['point'])),record['indices']
            assert len(set(indices)) == len(indices)
            assert all(interior(p,self.polygons[i]) for i in indices), 'Invalid strict-interior point clique'
            self.add_clause(atmost(1,(f'x{i}' for i in indices)))
        self.stats['angular_cliques'] = len(self.model['angular_cliques'])
        self.stats['overlap_pairs'] = len(self.model['overlap_pairs'])
        self.stats['interior_point_cliques'] = len(self.model.get('interior_point_cliques',[]))

    def whole_edges(self):
        if 'whole_edge_extension' not in self.model:
            return
        assert self.model['whole_edge_extension'] == 'complete-opposite-bank-v1'
        catalogues = {}
        for record in self.model['whole_edge_catalogues']:
            p,ray,length = self.g.point(record['start']),tuple(record['ray']),record['length']
            key = p,ray,length
            assert key not in catalogues
            metric = self.g.edge_bank(p,ray,length)
            expected = self.ids(metric.keys(),'whole-edge opposite bank')
            indices = record['indices']
            assert len(set(indices)) == len(indices) and set(indices) == expected
            assert len(record['spans']) == len(indices)
            spans = {i:metric[self.polygon_keys[i]] for i in indices}
            assert all(tuple(span) == spans[i]
                       for i,span in zip(indices,record['spans']))
            intervals = [{i for i in indices if spans[i][0] <= k < spans[i][1]} for k in range(length)]
            assert len(record['intervals']) == length
            assert all(len(set(supplied)) == len(supplied) and set(supplied) == expected
                       for supplied,expected in zip(record['intervals'],intervals))
            catalogues[key] = record
        obligations = set()
        for record in self.model['whole_edge_obligations']:
            i,k = record['tile'],record['edge_index']
            assert k in (0,1,2) and (i,k) not in obligations
            obligations.add((i,k))
            polygon = self.polygons[i]
            p,q = polygon[k],polygon[(k+1)%3]
            assert self.g.point(record['start']) == p and self.g.point(record['end']) == q
            ray,length = tuple(record['ray']),record['length']
            assert length in (self.g.a,self.g.b,self.g.c)
            assert sub(q,p) == scale(length,self.g.unit(*ray))
            def faces(v):
                x,y = v
                return x==0,y==0,self.g.B*x+self.g.A*y==self.g.A*self.g.B
            boundary = any(a and b for a,b in zip(faces(p),faces(q)))
            assert record['boundary'] == boundary
            if boundary:
                assert not record['neighbors'] and not record['intervals'] and not record['clauses']
                continue
            bank = catalogues[p,ray,length]
            assert record['neighbors'] == bank['indices'] and record['intervals'] == bank['intervals']
            clauses = [f'(=> x{i} {combine("or",(f"x{j}" for j in group))})'
                       for group in bank['intervals']]
            assert list(map(logical,record['clauses'])) == list(map(logical,clauses))
            for clause in clauses:
                self.add_clause(clause)
            self.stats['whole_edge_unit_obligations'] += length
        for record in self.model['whole_edge_bank_cliques']:
            key = self.g.point(record['start']),tuple(record['ray']),record['length']
            group = catalogues[key]['intervals'][record['unit']]
            assert record['indices'] == group
            self.add_clause(atmost(1,(f'x{i}' for i in group)))
        complete = self.model.get('whole_edge_complete_tiles',[])
        assert len(set(complete)) == len(complete)
        assert all((i,k) in obligations for i in complete for k in range(3))
        self.stats['whole_edge_catalogues'] = len(catalogues)
        self.stats['whole_edge_obligations'] = len(obligations)
        self.stats['whole_edge_bank_cliques'] = len(self.model['whole_edge_bank_cliques'])

    def root_and_budgets(self):
        indices = self.model['root_indices']
        assert sorted(set(indices)) == indices
        assert self.model['root_assumptions'] == [f'x{i}' for i in indices]
        root = self.model['root']
        if root is None:
            assert not indices
        else:
            source = Path(root['source'])
            if not source.is_absolute():
                source = ROOT/source
            raw = source.read_bytes()
            assert hashlib.sha256(raw).hexdigest() == root['sha256']
            data = json.loads(raw)
            assert data['sides'] == self.model['sides']
            records = [r for r in data['surviving_roots'] if r['id'] == root['id']]
            assert len(records) == 1
            polygons = {canonical(self.g.polygon(freeze(t))) for t in records[0]['tiles']}
            assert {canonical(self.polygons[i]) for i in indices} == polygons
            # This establishes which explicit branch is being tested. Exhaustive
            # root coverage is checked separately by verify_corner_roots.py.
        for i in indices:
            self.add_clause(f'x{i}')
        total = atmost(self.g.N,(f'x{i}' for i in range(len(self.tiles))))
        assert logical(self.model['total_count_bound']) == logical(total)
        reserves = {}
        for record in self.model['charge_reserves']:
            sigma,tau = record['sigma'],record['tau']
            assert sigma in (-1,1) and tau in (-1,1)
            assert (sigma,tau) not in reserves
            wanted = [i for i,(_,h,j,s) in enumerate(self.tiles)
                      if s*(-1 if j%2 else 1) == (-sigma if h%2 else -tau)]
            bound = (self.g.N+sigma*self.g.c+tau*(self.g.a-self.g.b))//2
            assert record['indices'] == wanted and record['bound'] == bound
            term = atmost(bound,(f'x{i}' for i in wanted))
            if 'term' in record:
                assert logical(record['term']) == logical(term)
            reserves[sigma,tau] = term
        assert set(reserves) == {(-1,-1),(-1,1),(1,-1),(1,1)}
        query = combine('and',[total]+list(reserves.values())+self.phase_caps+self.population_caps)
        assert logical(self.model['query_count_bound']) == logical(query)
        self.stats['global_charge_reserves'] = 4
        self.stats['root_assumptions'] = len(indices)

    def phase_budgets(self):
        record = self.model.get('ordinary_phase_budget')
        if record is None:
            return
        assert record['costs_of_trees_are_not_added'] is True
        enabled = tuple(self.model['sides']) in ((33,7,37),(35,13,43))
        assert record['enabled'] == enabled
        c = self.g.c
        core_minimum = self.g.N%c
        assert record['core_minimum'] == core_minimum
        assert record['ordinary_node_minimum'] == 2*c
        loose = (self.g.N-core_minimum)//(2*c)
        strong = (self.g.N-core_minimum-c)//(2*c)
        limit = record['limit_per_tree']
        assert limit in (loose,strong), 'Unjustified ordinary-node population cap'
        additional = record.get('additional_odd_sign_block',0)
        assert additional in (0,c)
        assert limit == (self.g.N-core_minimum-additional)//(2*c)
        if not enabled:
            assert not record['tile_implications']
            assert all(not tree['nodes'] for tree in record['trees'])
            return
        roots = [r for r in range(c) if (r*r-r+1)%c == 0]
        assert len(roots) == 2
        positive, = [r for r in roots if (self.g.a+self.g.b*r)%c == 0]
        negative, = [r for r in roots if r != positive]
        expected_flags = defaultdict(list)
        all_symbols = set()
        assert len(record['trees']) == 2
        for sign,first,tree in zip((1,-1),(positive,negative),record['trees']):
            assert tree['sign'] == sign
            lifted = {1:first}
            def root(precision):
                # Independent digit enumeration instead of the production
                # Newton/Hensel update formula.
                while len(lifted) < precision:
                    n = len(lifted)
                    modulus = c**n
                    choices = [lifted[n]+digit*modulus for digit in range(c)
                               if ((lifted[n]+digit*modulus)**2-(lifted[n]+digit*modulus)+1)%(modulus*c)==0]
                    assert len(choices) == 1
                    lifted[n+1] = choices[0]
                return lifted[precision]
            @lru_cache(None)
            def node(point,level):
                x,y,e = point
                precision = e+level
                if precision <= 0:
                    return level,0,0
                value = (x+y*root(precision))%(c**precision)
                while e and value%c == 0:
                    value //= c
                    e -= 1
                return level,value,e
            outer = (((0,0,0),0),((self.g.A,0,0),2*sign),((0,self.g.B,0),0))
            catalogue = {tuple(n['key']):n['symbol'] for n in tree['nodes']}
            assert len(catalogue) == len(tree['nodes'])
            assert (0,0,0) not in catalogue
            assert len(set(catalogue.values())) == len(catalogue)
            assert not all_symbols.intersection(catalogue.values())
            assert all(symbol.startswith('pn'+str(0 if sign==1 else 1)+'_')
                       and symbol.split('_')[1].isdigit() for symbol in catalogue.values())
            all_symbols.update(catalogue.values())
            used = set()
            for i,(p,h,j,s) in enumerate(self.tiles):
                height = sign*h
                needed = set()
                own = node(p,height)
                if own != (0,0,0):
                    needed.add(own)
                start = min(1-p[2],1+min(H for _,H in outer))
                for level in range(start,height+1):
                    at = node(p,level)
                    if all(level>H or node(q,level)!=at for q,H in outer):
                        needed.add(at)
                assert (0,0,0) not in needed
                assert all(n in catalogue for n in needed), 'Missing required ordinary phase node'
                used.update(needed)
                expected_flags[i].extend(catalogue[n] for n in sorted(needed))
            assert used == catalogue.keys(), 'Unreferenced ordinary-node flag'
            self.phase_caps.append(atmost(limit,catalogue.values()))
            self.stats[f'ordinary_phase_nodes_sign_{sign}'] = len(catalogue)
        implications = {r['tile']:r['clause'] for r in record['tile_implications']}
        assert len(implications) == len(record['tile_implications'])
        expected = {i:f'(=> x{i} {combine("and",flags)})' for i,flags in expected_flags.items() if flags}
        assert implications.keys() == expected.keys()
        for i,clause in expected.items():
            assert logical(implications[i]) == logical(clause), 'Incorrect required-node implication'
            self.add_clause(clause)
        self.stats['ordinary_phase_tile_implications'] = len(expected)
        self.stats['ordinary_phase_cap_per_tree'] = limit
        self.stats['ordinary_phase_additional_odd_sign_block'] = additional

    def supported_long_cycles(self):
        records = self.model.get('supported_long_cycle_cuts',[])
        if not records:
            return
        assert tuple(self.model['sides']) in ((33,7,37),(35,13,43)), 'Unsupported cycle theorem shape'
        for record in records:
            height = record['height']
            vertices = [self.g.point(p) for p in record['vertices']]
            indices = record['indices']
            assert len(vertices) >= 4 and vertices[0] == vertices[-1]
            assert len(set(vertices[:-1])) == len(vertices)-1
            assert len(indices) == len(set(indices)) == len(vertices)-1
            assert len(record['edges']) == len(indices)
            for p,q,i,edge in zip(vertices,vertices[1:],indices,record['edges']):
                assert edge['representative'] == i
                assert self.g.point(edge['from']) == p and self.g.point(edge['to']) == q
                assert i in edge['selected_owners']
                assert norm(sub(q,p)) == self.g.c**2
                assert any(sub(q,p) == scale(self.g.c,self.g.unit(height,j)) for j in range(6))
                for owner in edge['selected_owners']:
                    anchor,h,j,s = self.tiles[owner]
                    assert h+s == height
                    long_endpoints = {sub(self.g.point(anchor),scale(self.g.a,self.g.unit(h,j))),
                                      add(self.g.point(anchor),scale(self.g.b,self.g.unit(h,j+s)))}
                    assert long_endpoints == {p,q}
            # The inherited target-specific supported pure-c-cycle theorem
            # forbids this exact single-height embedded triangular-lattice
            # cycle at every rotation/translation. Its board-width/area
            # arithmetic is replayed by the package's separate pure-cycle check.
            self.add_clause('(not (and '+' '.join(f'x{i}' for i in sorted(indices))+'))')
        self.stats['supported_long_cycle_cuts'] = len(records)

    def population_allocations(self):
        data = self.model.get('phase_population_allocation')
        if data is None:
            return
        assert data['enabled'] is True
        assert data['allocation_caps_are_current_pool_normalizations'] is True
        assert data['query_caps_are_permanent'] is False
        assert data['costs_of_trees_are_not_added'] is True
        c,residue = self.g.c,self.g.N%self.g.c
        assert self.g.a%2 == self.g.b%2 == 1 and gcd(self.g.a,self.g.b) == 1
        assert c>=3 and all(c%d for d in range(2,isqrt(c)+1))
        assert 0<residue<c
        cap = (self.g.N-residue)//c
        width = cap.bit_length()
        assert data['hypotenuse'] == c and data['core_residue'] == residue
        assert data['block_cap_per_tree'] == cap and data['bit_width'] == width
        strict = tuple(self.model['sides']) in ((33,7,37),(35,13,43))
        assert data['strict_no_empty_ancestor'] == strict
        allowance = 0 if strict else 1
        assert data['empty_ancestor_allowance_per_tree'] == allowance
        assert len(data['trees']) == 2
        variables = set()
        tile_clauses = defaultdict(list)
        query_clauses = []
        for tree_index,(sign,tree) in enumerate(zip((1,-1),data['trees'])):
            assert tree['sign'] == sign
            phase = IndependentPhase(self.g,sign)
            nodes = {tuple(record['key']):record for record in tree['nodes']}
            assert len(nodes) == len(tree['nodes'])
            expected_own = defaultdict(list)
            required_by_tile = {}
            used = {(0,0,0)}
            for i,tile in enumerate(self.tiles):
                own = phase.node(tile[0],sign*tile[1])
                expected_own[own].append(i)
                required = phase.required(tile)
                required_by_tile[i] = required
                used.add(own)
                used.update(required)
            assert used == nodes.keys(), 'Incomplete or extraneous population-node catalogue'
            all_weights,all_bits,flags,excuses = [],[],[],[]
            for key,record in nodes.items():
                core = key == (0,0,0)
                assert record['core'] == core
                bits = record['bits']
                assert len(bits) == len(set(bits)) == width
                assert all(isinstance(bit,str) and bit.startswith(f'pn{tree_index}_')
                           and bit.endswith(f'_b{k}') for k,bit in enumerate(bits))
                assert not variables.intersection(bits)
                variables.update(bits)
                higher = combine('or',bits[1:])
                assert logical(record['higher']) == logical(higher)
                own = expected_own[key]
                assert record['own'] == own
                permanent = []
                if not core:
                    permanent.append(f'(=> {bits[0]} {higher})')
                exterior_free = phase.exterior_free(key)
                flag,excuse = record['flag'],record['excuse']
                if exterior_free:
                    assert not core
                    prefix = bits[0][:-3]
                    assert flag == prefix+'_f' and excuse == prefix+'_e'
                    assert flag not in variables and excuse not in variables
                    variables.update((flag,excuse))
                    flags.append(flag)
                    excuses.append(excuse)
                    permanent.extend((f'(=> {flag} (or {higher} {excuse}))',
                                      f'(=> {excuse} {flag})',
                                      f'(=> {excuse} (not {combine("or",bits)}))'))
                else:
                    assert flag is None and excuse is None
                assert list(map(logical,record['permanent_source_clauses'])) == list(map(logical,permanent))
                for clause in permanent:
                    self.add_clause(clause)
                all_weights.extend(1<<k for k in range(width))
                all_bits.extend(bits)
                allocation_cap = ((max(0,len(own)-residue)+c-1)//c if core
                                  else max(2,(len(own)+c-1)//c))
                allocation_cap = min(allocation_cap,cap)
                if not core and allocation_cap == 2:
                    forbidden = [bits[0]]+bits[2:]
                    if forbidden:
                        query_clauses.append('(not '+combine('or',forbidden)+')')
                elif allocation_cap == 0:
                    query_clauses.append('(not '+combine('or',bits)+')')
                elif allocation_cap<cap:
                    query_clauses.append(weighted_atmost(allocation_cap,[1<<k for k in range(width)],bits))
                if len(own)>(residue if core else 2*c):
                    weights = [1]*len(own)+[c*(1<<k) for k in range(width)]
                    terms = [f'x{i}' for i in own]+[f'(not {bit})' for bit in bits]
                    bound = c*((1<<width)-1)+(residue if core else 0)
                    query_clauses.append(weighted_atmost(bound,weights,terms))
            for i,tile in enumerate(self.tiles):
                own = phase.node(tile[0],sign*tile[1])
                record = nodes[own]
                if not record['core']:
                    tile_clauses[i].append(f'(=> x{i} {record["higher"]})')
                required_flags = [nodes[node]['flag'] for node in required_by_tile[i]]
                assert all(required_flags)
                if required_flags:
                    tile_clauses[i].append(f'(=> x{i} (and '+ ' '.join(required_flags)+'))')
            query_clauses.extend((weighted_atmost(cap,all_weights,all_bits),
                                  atmost(allowance,excuses),atmost(cap//2+allowance,flags)))
            self.stats[f'population_nodes_sign_{sign}'] = len(nodes)
        supplied = {record['tile']:record['clauses'] for record in data['tile_sources']}
        assert len(supplied) == len(data['tile_sources']) == len(self.tiles)
        assert set(supplied) == set(range(len(self.tiles)))
        for i in range(len(self.tiles)):
            expected = tile_clauses[i]
            assert list(map(logical,supplied[i])) == list(map(logical,expected))
            for clause in expected:
                self.add_clause(clause)
        assert len(data['variables']) == len(set(data['variables']))
        assert variables == set(data['variables'])
        other_symbols = {f'x{i}' for i in range(len(self.tiles))}
        other_symbols.update(r['term'] for r in self.model['fan_paths'] if r['term'].startswith('cf'))
        for tree in self.model.get('ordinary_phase_budget',{}).get('trees',[]):
            other_symbols.update(n['symbol'] for n in tree['nodes'])
        assert not variables.intersection(other_symbols), 'Population variables alias physical/fan/phase variables'
        assert list(map(logical,data['query_source_clauses'])) == list(map(logical,query_clauses))
        self.population_caps = query_clauses
        self.stats['population_allocation_variables'] = len(variables)
        self.stats['population_allocation_query_clauses'] = len(query_clauses)

    def general_area_cycles(self):
        if 'general_area_cycle_cuts' not in self.model:
            assert 'general_area_cycle_rule' not in self.model
            return
        assert self.model['general_area_cycle_rule'] == 'integral-tile-area-and-two-signed-characters-v1'
        def on_segment(p,a,b):
            return det(sub(b,a),sub(p,a)) == 0 and all(min(x,y)<=v<=max(x,y) for v,x,y in zip(p,a,b))
        def intersects(a,b,c,d):
            x,y = det(sub(b,a),sub(c,a)),det(sub(b,a),sub(d,a))
            u,v = det(sub(d,c),sub(a,c)),det(sub(d,c),sub(b,c))
            return (x*y<0 and u*v<0) or any((cross==0 and on_segment(point,first,last))
                for cross,point,first,last in ((x,c,a,b),(y,d,a,b),(u,a,c,d),(v,b,c,d)))
        for record in self.model['general_area_cycle_cuts']:
            vertices = [self.g.point(p) for p in record['vertices']]
            assert len(vertices)>=4 and vertices[0] == vertices[-1]
            polygon = vertices[:-1]
            n = len(polygon)
            assert len(set(polygon)) == n
            sides = list(zip(vertices,vertices[1:]))
            for i,(a,b) in enumerate(sides):
                c = polygon[(i+2)%n]
                first,second = sub(b,a),sub(c,b)
                assert det(first,second) != 0 or sum(x*y for x,y in zip(first,second))>0
                for j in range(i+1,n):
                    if j == i+1 or (i==0 and j==n-1):
                        continue
                    assert not intersects(a,b,*sides[j]), 'Supported polygon is not simple'
            area2 = sum(det(p,q) for p,q in sides)
            assert area2>0
            area = area2/(self.g.a*self.g.b)
            assert F(record['twice_axial_area']) == area2 and F(record['tile_area_ratio']) == area
            assert len(record['edges']) == n
            W0 = W1 = F(0)
            representatives = set()
            for (p,q),edge in zip(sides,record['edges']):
                assert self.g.point(edge['start']) == p and self.g.point(edge['end']) == q
                i,k = edge['representative'],edge['side']
                assert k in (0,1,2)
                representatives.add(i)
                triangle = self.polygons[i]
                a,b = triangle[k],triangle[(k+1)%3]
                assert on_segment(p,a,b) and on_segment(q,a,b)
                h = self.tiles[i][1]
                possibilities = [(H,j,L) for H in range(h-1,h+2) for j in range(6)
                                 for L in (self.g.a,self.g.b,self.g.c)
                                 if sub(b,a) == scale(L,self.g.unit(H,j))]
                assert len(possibilities) == 1
                H,j,L = possibilities[0]
                axis = 0 if a[0]!=b[0] else 1
                signed_length = L*(q[axis]-p[axis])/(b[axis]-a[axis])
                assert signed_length and F(edge['length']) == abs(signed_length)
                assert edge['direction'] == [H,j if signed_length>0 else (j+3)%6]
                assert i in edge['selected_owners']
                for owner in edge['selected_owners']:
                    tile = self.polygons[owner]
                    assert any(on_segment(p,a,b) and on_segment(q,a,b)
                               for a,b in zip(tile,tile[1:]+tile[:1]))
                W0 += signed_length*(-1 if j%2 else 1)
                W1 += signed_length*(-1 if (H+j)%2 else 1)
            assert record['indices'] == sorted(representatives)
            assert all(not overlap_open(self.polygons[i],self.polygons[j])
                       for i,j in combinations(representatives,2))
            d = self.g.a-self.g.b
            E0,E1 = W0/(d-self.g.c),W1/(d+self.g.c)
            even,odd = (E0+E1)/2,(E0-E1)/2
            failures = []
            if area.denominator != 1: failures.append('nonintegral_area')
            if even.denominator != 1: failures.append('nonintegral_even_charge')
            if odd.denominator != 1: failures.append('nonintegral_odd_charge')
            if area.denominator == even.denominator == odd.denominator == 1:
                if area < abs(even)+abs(odd): failures.append('insufficient_area_for_signed_population')
                if (area-even-odd)%2: failures.append('incompatible_population_parity')
            budget = record['budget']
            assert F(budget['W0']) == W0 and F(budget['W1']) == W1
            assert F(budget['even_charge']) == even and F(budget['odd_charge']) == odd
            assert failures and budget['violations'] == failures, 'Supported polygon has no demonstrated obstruction'
            self.add_clause('(not (and '+' '.join(f'x{i}' for i in sorted(representatives))+'))')
        self.stats['general_area_cycle_cuts'] = len(self.model['general_area_cycle_cuts'])

    def signed_joint_allocations(self):
        data = self.model.get('signed_phase_population_allocation')
        if data is None:
            return
        assert data['enabled'] is True and data['joint_physical_heights_enabled'] is True
        assert data['allocation_caps_are_current_pool_normalizations'] is True
        assert data['query_caps_are_permanent'] is False
        assert data['tree_populations_are_not_added'] is True
        assert data['sign_index_epsilon'] == [1,-1]
        c,d,N = self.g.c,self.g.a-self.g.b,self.g.N
        assert self.g.a%2 == self.g.b%2 == c%2 == 1 and gcd(self.g.a,self.g.b) == 1
        assert all(c%p for p in range(2,isqrt(c)+1))
        # Independent closed formulas, using G_core=-d (mod c).
        residues = [((N-d)*pow(2,-1,c))%c,((N+d)*pow(2,-1,c))%c]
        totals = [(N-c-d)//2,(N+c+d)//2]
        assert all((total-residue)%c == 0 for total,residue in zip(totals,residues))
        caps = [(total-residue)//c for total,residue in zip(totals,residues)]
        widths = [cap.bit_length() for cap in caps]
        delta,rem = divmod(d+residues[0]-residues[1],c)
        assert rem == 0 and delta in (0,1) and caps[1] == caps[0]+delta+1
        assert data['hypotenuse'] == c and data['core_residues'] == residues
        assert data['signed_totals'] == totals and data['block_caps'] == caps
        assert data['bit_widths'] == widths and data['even_delta'] == delta
        assert min(widths)>=2
        strict = tuple(self.model['sides']) in ((33,7,37),(35,13,43))
        allowance = 0 if strict else 1
        assert data['strict_no_empty_ancestor'] == strict
        assert data['empty_ancestor_allowance_per_tree'] == allowance
        assert len(data['trees']) == 2
        variables = set()
        tile_clauses = defaultdict(list)
        uncoupled,joint_clauses,tree_records = [],[],[]
        needed_heights = set()
        specs = [((0,0),(0,1),caps[0]),((1,0),(1,1),caps[1]),
                 ((0,0),(1,1),caps[0]+1),((1,0),(0,1),caps[0]+delta)]
        for tree_index,(tree_sign,tree) in enumerate(zip((1,-1),data['trees'])):
            assert tree['sign'] == tree_sign
            phase = IndependentPhase(self.g,tree_sign)
            nodes = {tuple(r['key']):r for r in tree['nodes']}
            assert len(nodes) == len(tree['nodes'])
            expected_own = defaultdict(lambda:[[],[]])
            required_by_tile = {}
            used = {(0,0,0)}
            for i,tile in enumerate(self.tiles):
                epsilon_index = 0 if tile[3]*(-1 if tile[2]%2 else 1)==1 else 1
                own = phase.node(tile[0],tree_sign*tile[1])
                expected_own[own][epsilon_index].append(i)
                required = phase.required(tile)
                required_by_tile[i] = required
                used.add(own)
                used.update(required)
            assert used == nodes.keys(), 'Incorrect signed population-node catalogue'
            groups = {(sign,parity):([],[]) for sign in range(2) for parity in range(2)}
            flags,excuses = [],[]
            for key,record in nodes.items():
                core = key == (0,0,0)
                assert record['core'] == core and record['own'] == expected_own[key]
                bits = record['bits']
                assert len(bits) == 2
                for sign,group in enumerate(bits):
                    assert len(group) == len(set(group)) == widths[sign]
                    assert all(bit.startswith(f'spn{tree_index}_') and bit.endswith(f'_s{sign}_b{k}')
                               for k,bit in enumerate(group))
                    assert not variables.intersection(group)
                    variables.update(group)
                higher = combine('or',bits[0][1:]+bits[1][1:])
                positive = combine('or',[higher,f'(and {bits[0][0]} {bits[1][0]})'])
                present = [combine('or',group) for group in bits]
                assert logical(record['positive']) == logical(positive)
                assert list(map(logical,record['present'])) == list(map(logical,present))
                permanent = []
                if not core:
                    permanent.extend((f'(=> {bits[0][0]} (or {higher} {bits[1][0]}))',
                                      f'(=> {bits[1][0]} (or {higher} {bits[0][0]}))'))
                flag,excuse = record['flag'],record['excuse']
                if phase.exterior_free(key):
                    assert not core
                    prefix = bits[0][0][:-6]
                    assert flag == prefix+'_f' and excuse == prefix+'_e'
                    assert flag not in variables and excuse not in variables
                    variables.update((flag,excuse))
                    flags.append(flag)
                    excuses.append(excuse)
                    permanent.extend((f'(=> {flag} (or {positive} {excuse}))',
                                      f'(=> {excuse} {flag})',
                                      f'(=> {excuse} (not {combine("or",bits[0]+bits[1])}))'))
                else:
                    assert flag is None and excuse is None
                assert list(map(logical,record['permanent_source_clauses'])) == list(map(logical,permanent))
                for clause in permanent:
                    self.add_clause(clause)
                needed_heights.add(tree_sign*key[0])
                for sign in range(2):
                    group = bits[sign]
                    width = widths[sign]
                    own = record['own'][sign]
                    residue = residues[sign] if core else 0
                    gw,gb = groups[sign,key[0]%2]
                    gw.extend(1<<k for k in range(width))
                    gb.extend(group)
                    if len(own)>(residue if core else c):
                        terms = [f'x{i}' for i in own]+[f'(not {bit})' for bit in group]
                        weights = [1]*len(own)+[c*(1<<k) for k in range(width)]
                        uncoupled.append(weighted_atmost(c*((1<<width)-1)+residue,weights,terms))
                    local_cap = ((max(0,len(own)-residue)+c-1)//c if core
                                 else max(2,(len(own)+c-1)//c))
                    local_cap = min(local_cap,caps[sign])
                    if local_cap == 0:
                        uncoupled.append('(not '+combine('or',group)+')')
                    elif local_cap == 1:
                        uncoupled.append('(not '+combine('or',group[1:])+')')
                    elif local_cap == 2:
                        if group[2:]:
                            uncoupled.append('(not '+combine('or',group[2:])+')')
                        uncoupled.append(atmost(1,group[:2]))
                    elif local_cap<caps[sign]:
                        uncoupled.append(weighted_atmost(local_cap,[1<<k for k in range(width)],group))
            for i,tile in enumerate(self.tiles):
                sign = 0 if tile[3]*(-1 if tile[2]%2 else 1)==1 else 1
                own = phase.node(tile[0],tree_sign*tile[1])
                record = nodes[own]
                if not record['core']:
                    tile_clauses[i].extend((f'(=> x{i} {record["present"][sign]})',
                                           f'(=> x{i} {record["positive"]})'))
                required_flags = [nodes[node]['flag'] for node in required_by_tile[i]]
                assert all(required_flags)
                if required_flags:
                    tile_clauses[i].append(f'(=> x{i} (and '+ ' '.join(required_flags)+'))')
            for first,second,bound in specs:
                w0,b0 = groups[first]
                w1,b1 = groups[second]
                uncoupled.append(weighted_atmost(bound,w0+w1,b0+b1))
            uncoupled.extend((atmost(allowance,excuses),atmost((sum(caps)-1)//2+allowance,flags)))
            tree_records.append((tree_sign,nodes))
            self.stats[f'signed_population_nodes_sign_{tree_sign}'] = len(nodes)
        supplied = {r['tile']:r['clauses'] for r in data['tile_sources']}
        assert len(supplied) == len(data['tile_sources']) == len(self.tiles)
        assert set(supplied) == set(range(len(self.tiles)))
        for i in range(len(self.tiles)):
            assert list(map(logical,supplied[i])) == list(map(logical,tile_clauses[i]))
            for clause in tile_clauses[i]:
                self.add_clause(clause)
        heights = {r['height']:r['bits'] for r in data['joint_heights']}
        assert len(heights) == len(data['joint_heights']) and needed_heights == heights.keys()
        for h,bits in heights.items():
            assert len(bits) == 2
            for sign,group in enumerate(bits):
                assert len(group) == len(set(group)) == widths[sign]
                assert all(bit.startswith('jh') and bit.endswith(f'_s{sign}_b{k}') for k,bit in enumerate(group))
                assert not variables.intersection(group)
                variables.update(group)
        for tree_sign,nodes in tree_records:
            groups = {}
            for key,record in nodes.items():
                physical_height = tree_sign*key[0]
                for sign in range(2):
                    weights,terms = groups.setdefault((physical_height,sign),([],[]))
                    weights.extend(1<<k for k in range(widths[sign]))
                    terms.extend(record['bits'][sign])
            for (h,sign),(weights,terms) in groups.items():
                bits = heights[h][sign]
                width = widths[sign]
                joint_clauses.append(weighted_atmost((1<<width)-1,
                    weights+[1<<k for k in range(width)],terms+[f'(not {bit})' for bit in bits]))
        groups = {(sign,parity):([],[]) for sign in range(2) for parity in range(2)}
        for h,bits in heights.items():
            for sign,group in enumerate(bits):
                weights,terms = groups[sign,h%2]
                weights.extend(1<<k for k in range(widths[sign]))
                terms.extend(group)
        for first,second,bound in specs:
            w0,b0 = groups[first]
            w1,b1 = groups[second]
            joint_clauses.append(weighted_atmost(bound,w0+w1,b0+b1))
        assert len(data['variables']) == len(set(data['variables'])) and variables == set(data['variables'])
        assert not variables.intersection({f'x{i}' for i in range(len(self.tiles))})
        assert list(map(logical,data['uncoupled_query_source_clauses'])) == list(map(logical,uncoupled))
        assert list(map(logical,data['joint_query_source_clauses'])) == list(map(logical,joint_clauses))
        complete = uncoupled+joint_clauses
        assert list(map(logical,data['query_source_clauses'])) == list(map(logical,complete))
        self.population_caps.extend(complete)
        self.stats['signed_population_variables'] = len(variables)
        self.stats['signed_population_query_clauses'] = len(complete)
        self.stats['joint_physical_heights'] = len(heights)

    def run(self,verbose=False):
        for method in (self.boundary,self.rows,self.fan_definitions,self.owners_and_corner_roots,
                       self.exclusion_cliques,self.whole_edges,self.supported_long_cycles,
                       self.general_area_cycles,self.phase_budgets,self.population_allocations,
                       self.signed_joint_allocations,self.root_and_budgets):
            stamp = time.monotonic()
            if verbose:
                print('Auditing '+method.__name__,file=sys.stderr,flush=True)
            method()
            if verbose:
                print(f'  checked in {time.monotonic()-stamp:.3f}s',file=sys.stderr,flush=True)
        supplied = {logical(s) for s in self.model['permanent_assertions']}
        supplied.discard('true')
        extra = supplied-self.expected
        missing = self.expected-supplied
        assert not extra, f'{len(extra)} unverified permanent assertions: {list(map(repr,list(extra)[:2]))}'
        assert not missing, f'{len(missing)} expected permanent assertions missing: {list(map(repr,list(missing)[:2]))}'
        self.stats['verified_permanent_assertions'] = len(supplied)
        self.stats['raw_permanent_assertions'] = len(self.model['permanent_assertions'])
        return dict(status='PASS',counts=dict(self.stats),root=self.model['root'],
                    recognized_optional_fields=[field for field in (
                        'interior_point_cliques','whole_edge_extension','supported_long_cycle_cuts',
                        'general_area_cycle_cuts','ordinary_phase_budget','phase_population_allocation',
                        'signed_phase_population_allocation')
                        if field in self.model],
                    scope='Independent exact regeneration of all supported finite geometric/Boolean clauses; no target refutation.')


def audit_file(path,verbose=False):
    started = time.monotonic()
    raw = read_snapshot_bytes(path)
    report = SnapshotAudit(json.loads(raw)).run(verbose)
    report.update(model_sha256=hashlib.sha256(raw).hexdigest(),seconds=round(time.monotonic()-started,3))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model',type=Path)
    parser.add_argument('--report',type=Path)
    parser.add_argument('--verbose',action='store_true')
    args = parser.parse_args()
    report = audit_file(args.model,args.verbose)
    text = json.dumps(report,indent=2)+'\n'
    if args.report:
        args.report.write_text(text)
    print(text,end='')


if __name__ == '__main__':
    main()

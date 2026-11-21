#!/usr/bin/env python3
"""Exact regional minority/contact certificates and a charged143 hole control.

No solver, search cutoff, or target exclusion is used. The production bank
catalogue is compared to an independent rational metric construction.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations,product
import json
from pathlib import Path
import sys

PACKAGE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(PACKAGE/'owned'),str(PACKAGE/'whole-edges'),
             str(PACKAGE/'corner-tests'),str(PACKAGE/'audit')]
from legacy import core,ROOT
from whole_edge_oracle import WholeEdgeOracle
from verify_owned_controls import exact_physical_control
from verify_area_cycles import independent_simple
from through_geometry import ExactGeometry,canonical,overlap_open,det,sub


def ceiling(value):
    return -((-value.numerator)//value.denominator)


def certificate(rows,costs,weights,rhs=None,cliques=(),multipliers=(),capacities=None):
    """Check every shared-owner column; return the rounded finite lower bound."""
    assert len(rows)==len(weights)
    rhs=[1]*len(rows) if rhs is None else rhs
    capacities=[1]*len(cliques) if capacities is None else capacities
    assert len(rhs)==len(rows)
    assert len(cliques)==len(multipliers)==len(capacities)
    assert all(isinstance(w,(int,F)) for w in [*weights,*multipliers])
    assert all(value in (0,1) for value in [*rhs,*capacities])
    assert all(mu>=0 for mu in multipliers)
    assert all(cost in (0,1) for cost in costs.values())
    assert all(set(row)<=set(costs) for row in [*rows,*cliques])
    for owner,cost in costs.items():
        load=sum((weight for row,weight in zip(rows,weights) if owner in row),F(0))
        load-=sum((mu for group,mu in zip(cliques,multipliers) if owner in group),F(0))
        assert load<=cost,('A shared whole owner was overcharged',owner,load,cost)
    bound=sum((w*r for w,r in zip(weights,rhs)),F(0))
    bound-=sum((mu*b for mu,b in zip(multipliers,capacities)),F(0))
    return bound,max(0,ceiling(bound))


def enumerated_certificate_control(rows,costs,weights,rhs=None,cliques=(),multipliers=(),capacities=None):
    bound,rounded=certificate(rows,costs,weights,rhs,cliques,multipliers,capacities)
    rhs=[1]*len(rows) if rhs is None else rhs
    capacities=[1]*len(cliques) if capacities is None else capacities
    owners=list(costs)
    feasible=[]
    for bits in product((0,1),repeat=len(owners)):
        assignment=dict(zip(owners,bits))
        if any(sum(assignment[q] for q in row)!=r for row,r in zip(rows,rhs)):continue
        if any(sum(assignment[q] for q in group)>cap for group,cap in zip(cliques,capacities)):continue
        value=sum(costs[q]*assignment[q] for q in owners)
        assert value>=bound and value>=rounded
        feasible.append(value)
    assert feasible
    return dict(feasible_assignments=len(feasible),exact_bound=str(bound),
                integer_bound=rounded,attained_minimum=min(feasible))


def finite_controls():
    # Every contact here has a majority candidate. Nonnegative contact
    # weights alone give zero; weights (1,-1,1) prove one minority.
    signed=enumerated_certificate_control(
        [{'a','b'},{'a','c'},{'c','d'}],{'a':0,'b':1,'c':0,'d':1},
        [F(1),F(-1),F(1)])
    assert signed['attained_minimum']==signed['integer_bound']==1
    clique=enumerated_certificate_control(
        [{'a','b'},{'c','d'}],{'a':0,'b':1,'c':0,'d':1},[F(1),F(1)],
        cliques=[{'a','c'}],multipliers=[F(1)])
    assert clique['attained_minimum']==clique['integer_bound']==1
    rounded=enumerated_certificate_control([{'a','b'}],{'a':1,'b':1},[F(1,2)])
    assert rounded['integer_bound']==1
    known=enumerated_certificate_control(
        [{'a','b'},{'a'}],{'a':0,'b':1},[F(1),F(-1)],rhs=[1,0])
    assert known['integer_bound']==1
    return dict(signed_contact_correlation=signed,spatial_clique=clique,
                integer_rounding=rounded,known_owner_residual=known)


def charge(tiles):
    return tuple(sum(t[3]*(-1 if t[2]%2 else 1) for t in tiles if t[1]%2==parity)
                 for parity in (0,1))


def minority(tile,alpha):
    return int(tile[3]*(-1 if tile[2]%2 else 1)==-alpha[tile[1]%2])


def main():
    source=ROOT/'research/2026-11-21/semiprimes/continued-rigidity/physical/CONTROL_143.json'
    data=json.loads(source.read_text())
    assert data['sides']==[5,3,7] and data['N']==143
    tiles=tuple((tuple(t[0]),*t[1:]) for t in data['tiles'])
    g=core.Geometry(5,3,7)
    exact_physical_control(g,tiles)
    independent=ExactGeometry(5,3,7)
    polygons=[independent.polygon(t) for t in tiles]
    assert all(independent.admissible_polygon(p) for p in polygons)
    assert all(not overlap_open(polygons[i],polygons[j]) for i,j in combinations(range(143),2))
    raw_vertices=[(151,15,1),(25,0,0),(200,15,1),(225,30,1),
                  (176,30,1),(171,27,1),(156,18,1)]
    vertices=list(map(independent.point,raw_vertices))
    independent_simple(vertices)
    assert all(det(sub(vertices[(i+1)%7],vertices[i]),
                   sub(vertices[(i+2)%7],vertices[(i+1)%7]))>=0 for i in range(7))
    def contained(polygon):
        return all(det(sub(b,a),sub(v,a))>=0 for a,b in zip(vertices,vertices[1:]+vertices[:1])
                   for v in polygon)
    assert {i for i,p in enumerate(polygons) if contained(p)}=={1,2,3}
    area2=sum(det(a,b) for a,b in zip(vertices,vertices[1:]+vertices[:1]))
    assert area2==45 and area2/(g.a*g.b)==3
    supports=[(0,0),(5,1),(7,1),(4,2),(15,0),(13,0),(11,0)]
    support_ids=sorted({i for i,k in supports})
    assert support_ids==[0,4,5,7,11,13,15]
    whole=WholeEdgeOracle(g)
    W0=W1=F(0)
    verified_units=0
    selected_contacts=[]
    exclusion_counts=[]
    all_catalogues=0
    for edge_number,(owner,side) in enumerate(supports):
        first,last=vertices[edge_number],vertices[(edge_number+1)%7]
        description=whole.edge(tiles[owner],side)
        p,q=independent.point(description.start),independent.point(description.end)
        u=independent.unit(*description.ray)
        assert sub(q,p)==tuple(description.length*v for v in u)
        assert all(det(sub(last,first),sub(v,first))<=0 for v in polygons[owner])
        assert all(det(sub(q,p),sub(v,p))==0 for v in (first,last))
        axis=0 if u[0] else 1
        offsets=[(v[axis]-p[axis])/u[axis] for v in (first,last)]
        assert all(t.denominator==1 and 0<=t<=description.length for t in offsets)
        signed_length=offsets[1]-offsets[0]
        h,j=description.ray
        W0+=signed_length*(-1 if j%2 else 1)
        W1+=signed_length*(-1 if (h+j)%2 else 1)
        catalogue=whole.catalogue(description.start,description.ray,description.length)
        reference=independent.edge_bank(p,description.ray,description.length)
        actual={canonical(independent.polygon(t)):span for t,span in zip(catalogue.tiles,catalogue.spans)}
        assert actual==reference,'The complete six-shape bank catalogues disagree.'
        all_catalogues+=1
        lo,hi=sorted(map(int,offsets))
        for k in range(lo,hi):
            production={canonical(independent.polygon(catalogue.tiles[i])):catalogue.tiles[i]
                        for i in catalogue.intervals[k]}
            complete={polygon for polygon,(lo,hi) in reference.items() if lo<=k<hi}
            assert set(production)==complete
            surviving={polygon for polygon in complete if contained(polygon)}
            nonoverlap={polygon for polygon in complete
                        if all(polygon==canonical(polygons[i]) or not overlap_open(polygon,polygons[i])
                               for i in support_ids)}
            assert surviving==nonoverlap,'A purported boundary crossing lacks an overlap witness.'
            assert surviving
            verified_units+=1
            actual_owner=canonical(polygons[2])
            if surviving=={actual_owner}:
                assert production[actual_owner]==tiles[2]
                selected_contacts.append(dict(source_tile=owner,source_side=side,unit=k,
                    raw_candidate_count=len(complete),surviving_owner_tile=2,weight='1/5'))
                exclusion_counts.append(len(complete)-1)
    assert W0==-5 and W1==-9
    total=W0/(g.a-g.b-g.c)
    alternating=W1/(g.a-g.b+g.c)
    G=((total+alternating)/2,(total-alternating)/2)
    assert G==(0,1)==charge([tiles[i] for i in (1,2,3)])
    assert len(selected_contacts)==5
    assert sorted({row['source_tile'] for row in selected_contacts})==[11,13,15]
    first,last=independent.point((176,30,1)),independent.point((151,15,1))
    for encoded,offset in (((171,27,1),1),((156,18,1),4)):
        point=independent.point(encoded)
        assert det(sub(last,first),sub(point,first))==0
        fraction=(point[0]-first[0])/(last[0]-first[0])
        assert fraction==F(offset,5) and 0<fraction<1
    alpha=(-1,1)
    assert minority(tiles[2],alpha)==1
    rows=[{2} for _ in selected_contacts]
    bound,rounded=certificate(rows,{2:1},[F(1,5)]*5)
    assert bound==rounded==1
    base=sum(a*value for a,value in zip(alpha,G))
    assert base==1 and base+2*rounded==3
    assert sum(minority(tiles[i],alpha) for i in (1,2,3))==1
    try:certificate(rows,{2:1},[F(1)]*5)
    except AssertionError:pass
    else:raise AssertionError('The fivefold shared-owner overcount was accepted.')
    # Complement bookkeeping, first for this hole, then for this hole and
    # a distinct actual unit-tile region. The full selected complement
    # attains the global identity for all four alpha choices.
    global_G=charge(tiles)
    assert global_G==(-2,-7)
    complement_checks=0
    for regions in ([{1,2,3}],[{1,2,3},{140}]):
        removed=set().union(*regions)
        assert sum(map(len,regions))==len(removed)
        local_G=[charge([tiles[i] for i in indices]) for indices in regions]
        rest=[t for i,t in enumerate(tiles) if i not in removed]
        residual=tuple(global_G[p]-sum(Gp[p] for Gp in local_G) for p in (0,1))
        assert residual==charge(rest)
        for signs in product((-1,1),repeat=2):
            minority_count=sum(minority(t,signs) for t in rest)
            lower=len(removed)+sum(a*v for a,v in zip(signs,residual))+2*minority_count
            assert lower==143
            complement_checks+=1
    report=dict(status='PASS',physical143_control=True,
        hole=dict(removed_tiles=[1,2,3],supporting_tiles=support_ids,vertices=raw_vertices,
                  tile_area=3,W0=str(W0),W1=str(W1),even_charge=0,odd_charge=1,
                  scalar_charge_lower_bound=1,contact_charge_lower_bound=3,
                  unique_negative_odd_owner=tiles[2],unit_contacts=selected_contacts,
                  raw_candidates_excluded_per_contact=exclusion_counts,
                  shared_owner_count=1,T_junctions_on_shared_owner=2,
                  fivefold_overcount_rejected=True,positive_completion_preserved=True),
        independent_full_bank_catalogues=all_catalogues,unit_catalogues_compared=verified_units,
        finite_incidence_controls=finite_controls(),complement_identity_controls=complement_checks,
        full_target_excluded=False)
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O: exact assertions are required.')
    main()

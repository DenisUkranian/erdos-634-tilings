#!/usr/bin/env python3
"""Exact mandatory long-edge reconstruction from a complete odd packing.

This is a necessary completion test, not a tiling solver.  All coordinates
are rational axial coordinates, with squared norm x*x+x*y+y*y.  The input
must contain every odd-height tile of the proposed full tiling.  No height
cutoff, phase envelope, or longitudinal period is silently imposed.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as F
from math import gcd, isqrt, lcm


def add(p, q):
    return p[0]+q[0], p[1]+q[1]


def sub(p, q):
    return p[0]-q[0], p[1]-q[1]


def scale(k, p):
    return k*p[0], k*p[1]


def det(p, q):
    return p[0]*q[1]-p[1]*q[0]


def norm(p):
    return p[0]*p[0]+p[0]*p[1]+p[1]*p[1]


def ccw(poly):
    poly=tuple((F(x), F(y)) for x,y in poly)
    area=det(sub(poly[1],poly[0]),sub(poly[2],poly[0]))
    assert area
    return poly if area>0 else poly[::-1]


def overlaps(A, B):
    """Strict interior intersection; both convex polygons are CCW."""
    for first, second in ((A,B),(B,A)):
        for p,q in zip(first,first[1:]+first[:1]):
            if max(det(sub(q,p),sub(r,p)) for r in second)<=0:
                return False
    return True


def contained(poly, board):
    return all(det(sub(q,p),sub(r,p))>=0
               for p,q in zip(board,board[1:]+board[:1]) for r in poly)


def line_data(p, q, c):
    """A rational line and a vector of physical length c along it."""
    dx,dy=sub(q,p)
    denominator=lcm(dx.denominator,dy.denominator)
    ix,iy=int(dx*denominator),int(dy*denominator)
    common=gcd(abs(ix),abs(iy)); ix//=common;iy//=common
    if (ix,iy)<(0,0): ix,iy=-ix,-iy
    size2=ix*ix+ix*iy+iy*iy
    size=isqrt(size2)
    if size*size!=size2:
        raise ValueError('Edge is not a rational unit direction in the placement framework')
    direction=(F(c*ix,size),F(c*iy,size))
    line=(ix,iy,F(ix*p[1]-iy*p[0]))
    coordinate=0 if ix else 1
    t=p[coordinate]/direction[coordinate]
    origin=sub(p,scale(t,direction))
    return line,direction,origin,t


def reconstruct(polygons, a, b, c):
    """Invert 1-X on every actual c-step orbit of every short support line.

    A signed positive segment goes from P to P+direction.  Its endpoint
    current is +1 at P and -1 at P+direction.  The returned segments have
    current equal to minus the complete input short-edge current.
    """
    assert a*a+a*b+b*b==c*c and a>b>0
    lines={};events=defaultdict(Counter)
    for raw in polygons:
        poly=ccw(raw)
        lengths=sorted(norm(sub(q,p)) for p,q in zip(poly,poly[1:]+poly[:1]))
        assert lengths==sorted((a*a,b*b,c*c))
        for p,q in zip(poly,poly[1:]+poly[:1]):
            if norm(sub(q,p))==c*c: continue
            line,direction,origin,t=line_data(p,q,c)
            lines[line]=(direction,origin)
            coordinate=0 if direction[0] else 1
            end=q[coordinate]/direction[coordinate]
            events[line][t]+=1;events[line][end]-=1
    segments=[];residual=[]
    for line,table in sorted(events.items()):
        orbits=defaultdict(Counter)
        for t,value in table.items():
            if value:
                integer=t.numerator//t.denominator
                orbits[t-integer][integer]+=value
        direction,origin=lines[line]
        for residue,orbit in sorted(orbits.items()):
            if sum(orbit.values()):
                residual.append((line,residue,sum(orbit.values())))
                continue
            coefficient=0
            for n in range(min(orbit),max(orbit)+1):
                coefficient-=orbit[n]
                if coefficient:
                    p=add(origin,scale(residue+n,direction));q=add(p,direction)
                    segments.append(dict(line=line,t=residue+n,
                                         p=p,q=q,coefficient=coefficient))
            assert coefficient==0
    # Direct unreduced endpoint identity, independent of the prefix code.
    check=Counter()
    for line,table in events.items():
        direction,origin=lines[line]
        for t,value in table.items():
            if value:check[line,add(origin,scale(t,direction))]+=value
    for segment in segments:
        line,p,q,k=(segment[key] for key in ('line','p','q','coefficient'))
        check[line,p]+=k;check[line,q]-=k
    assert bool(any(check.values()))==bool(residual)
    return segments,residual


def capacity_conflicts(segments):
    failures=[]
    groups=defaultdict(list)
    for i,S in enumerate(segments):
        k=S['coefficient']
        if abs(k)>1:failures.append(('multiplicity',i,k))
        groups[S['line'],k>0].append((S['t'],i))
    for group in groups.values():
        group.sort()
        for (t,i),(u,j) in zip(group,group[1:]):
            if u<t+1:failures.append(('same_side_overlap',i,j))
    return failures


def triangle_choices(segment, a, b, c):
    p,q=segment['p'],segment['q']
    assert abs(segment['coefficient'])==1
    if segment['coefficient']<0:p,q=q,p
    v=sub(q,p);perpendicular=(-v[0]-2*v[1],2*v[0]+v[1])
    result=[]
    for r,s in ((a,b),(b,a)):
        t=F(r*r+c*c-s*s,2*c*c)
        apex=add(p,add(scale(t,v),scale(F(a*b,2*c*c),perpendicular)))
        poly=ccw((p,q,apex))
        assert norm(sub(apex,p))==r*r and norm(sub(apex,q))==s*s
        assert det(sub(q,p),sub(apex,p))==a*b
        result.append(poly)
    assert result[0]!=result[1]
    return tuple(result)


def solve_2sat(count, forbidden, pairs):
    """Choice i is encoded by vertex 2*i+choice; return a checked witness.

    A forbidden choice x implies its complement.  A conflicting pair x,y
    gives x -> not y and y -> not x.  SCCs decide satisfiability exactly.
    """
    size=2*count;graph=[[] for _ in range(size)];reverse=[[] for _ in range(size)]
    def edge(u,v):graph[u].append(v);reverse[v].append(u)
    for u in forbidden:edge(u,u^1)
    for u,v in pairs:edge(u,v^1);edge(v,u^1)
    seen=set();order=[]
    for first in range(size):
        if first in seen:continue
        seen.add(first);stack=[(first,0)]
        while stack:
            u,k=stack[-1]
            if k<len(graph[u]):
                v=graph[u][k];stack[-1]=(u,k+1)
                if v not in seen:seen.add(v);stack.append((v,0))
            else:order.append(u);stack.pop()
    component=[-1]*size;next_id=0
    for first in reversed(order):
        if component[first]>=0:continue
        component[first]=next_id;stack=[first]
        while stack:
            u=stack.pop()
            for v in reverse[u]:
                if component[v]<0:component[v]=next_id;stack.append(v)
        next_id+=1
    for i in range(count):
        if component[2*i]==component[2*i+1]:
            return dict(satisfiable=False,contradictory_variable=i,
                        component=component,graph=graph)
    chosen={2*i+(component[2*i+1]>component[2*i]) for i in range(count)}
    assert not chosen.intersection(forbidden)
    assert all(not (u in chosen and v in chosen) for u,v in pairs)
    return dict(satisfiable=True,chosen=sorted(chosen),components=len(set(component)))


def complete_bank(polygons, a, b, c, board=None, pair_checks=True):
    """Exact necessary neighboring-bank test for a complete odd subfamily."""
    polygons=[ccw(p) for p in polygons]
    assert all(not overlaps(p,q) for i,p in enumerate(polygons) for q in polygons[:i])
    if board is not None:
        board=ccw(board)
        assert all(contained(p,board) for p in polygons)
    segments,residual=reconstruct(polygons,a,b,c)
    report=dict(odd_tiles=len(polygons),cylinder_residual_orbits=len(residual),
                mandatory_long_segments=len(segments),
                mandatory_long_multiplicity=sum(abs(s['coefficient']) for s in segments))
    if residual:
        report.update(status='cylinder_obstruction',first_residual=residual[0]);return report
    conflicts=capacity_conflicts(segments)
    report['line_capacity_conflicts']=len(conflicts)
    if conflicts:
        report.update(status='line_capacity_obstruction',first_conflict=conflicts[0]);return report
    candidates=[poly for segment in segments for poly in triangle_choices(segment,a,b,c)]
    forbidden=set();reason=Counter()
    for i,poly in enumerate(candidates):
        if board is not None and not contained(poly,board):
            forbidden.add(i);reason['outside_board']+=1
        elif any(overlaps(poly,q) for q in polygons):
            forbidden.add(i);reason['overlaps_odd_tile']+=1
    pairs=[]
    if pair_checks:
        for i,poly in enumerate(candidates):
            if i in forbidden:continue
            for j,q in enumerate(candidates[:i]):
                if j not in forbidden and i//2!=j//2 and overlaps(poly,q):pairs.append((i,j))
    report.update(forbidden_choices=len(forbidden),forbidden_reasons=dict(reason),
                  conflicting_choice_pairs=len(pairs))
    if not pair_checks:
        report['status']='pair_checks_omitted';return report
    solution=solve_2sat(len(segments),forbidden,pairs)
    if solution['satisfiable']:
        chosen=[candidates[i] for i in solution['chosen']]
        assert all(not overlaps(p,q) for i,p in enumerate(chosen) for q in chosen[:i])
        report.update(status='compatible_mandatory_bank',choice_indices=solution['chosen'])
    else:
        # Explicit reachability in both directions certifies the SCC conflict.
        root=2*solution['contradictory_variable'];graph=solution['graph']
        paths=[]
        for first,last in ((root,root^1),(root^1,root)):
            parents={first:None};todo=[first]
            for u in todo:
                if last in parents:break
                for v in graph[u]:
                    if v not in parents:parents[v]=u;todo.append(v)
            assert last in parents
            path=[last]
            while path[-1]!=first:path.append(parents[path[-1]])
            path.reverse();assert all(v in graph[u] for u,v in zip(path,path[1:]));paths.append(path)
        report.update(status='mandatory_bank_2sat_obstruction',implication_paths=paths)
    return report

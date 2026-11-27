"""Rooted population bounds, native cuts, and coordinate checks for the controls."""
from collections import Counter
from itertools import product
import json

import numpy as np
from layers import Layers
from remote_sectors import minimum
from rooted import branch_bounds


def native(model, N, costs):
    c, d, A, D = model.c, model.d, model.A, model.D
    evens, odds = model.ranges
    odd = np.array(odds)
    # Axes are the odd charges of C, T and the remaining outward forest.
    oC, oT, oR = odd[:, None, None], odd[None, :, None], odd[None, None, :]
    k = 1-oC-oT-oR
    odd_ok = abs(oC)+abs(oT)+abs(oR)+abs(k) <= model.V
    signed = c*k
    core = {e: np.array([model.side(e,o,True,costs) for o in odds]) for e in evens}
    slant = {e: np.array([model.side(e,o,False,costs) for o in odds]) for e in evens}
    other = {e: np.array([costs[0,e,o] for o in odds]) for e in evens}
    survivors = 0
    maxima = np.zeros(3,dtype=int)
    for eC, eT in product(evens, repeat=2):
        eR = -eC-eT
        if eR not in evens or abs(eC)+abs(eT)+abs(eR)>model.W:
            continue
        q = d*eC-c*oC+2*c
        r = d*eT-c*oT-c
        h = d*eR-c*oR
        lower = abs(q)+abs(r)+abs(h)
        for bank in (q,r):
            aligned = np.where(bank >= 0, signed, -signed)
            lower = np.maximum(lower, (2*D*abs(bank)+(D-2*A)*aligned+D-1)//D)
        blocks = (lower+c-1)//c
        blocks += (k-blocks)%2
        blocks += 2*((blocks==1) | ((c==43) & (blocks==2) & (abs(k)==2)))
        total = (c*blocks + core[eC][:,None,None] + slant[eT][None,:,None]
                 + other[eR][None,None,:])
        indices = np.nonzero(odd_ok & (total<=N))
        survivors += len(indices[0])
        if len(indices[0]):
            for i, e in enumerate((eC,eT,eR)):
                maxima[i] = max(maxima[i], max(abs(e-odd[indices[i]])))
    return dict(surviving_charge_quintuples=survivors,
                max_abs_even_minus_odd_C_T_other=maxima.tolist())


def run(c, d, A, D, N, W, V, allowance):
    model = Layers(c,d,A,D,W,V,allowance)
    trees, forests, iterations = branch_bounds(model,N)
    # Check the resulting inequalities by independent finite structural induction.
    from forest_review import review
    review(model,N,trees,forests)
    def lookup(table,p,x,y):
        return c*int(table[p][x-model.ranges[p].start,y-model.ranges[1-p].start])
    costs = {(p,x,y):lookup(forests,p,x,y) for p in (0,1)
             for x in model.ranges[p] for y in model.ranges[1-p]}
    remote = {}
    for p in (0,1):
        remaining = []
        for e,o in product(*model.ranges):
            x,y = (o,e) if p else (e,o)
            bank = d*x-c*y
            inside = lookup(trees,p,x,y) if x or y else 0
            outside = (minimum(c,A,D,d-c*e,bank if p else 0,True,allowance)
                       + minimum(c,A,D,c-c*o,0 if p else bank,False,0))
            if inside+outside <= N:
                remaining.append((e,o))
        remote[['even','odd'][p]] = dict(surviving_charge_pairs=len(remaining),
                max_abs_even_minus_odd=max(abs(e-o) for e,o in remaining))
    samples = [(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2),(2,-2)]
    return dict(iterations=iterations, sample_forest_blocks=[
        [x,y,costs[0,x,y]//c,costs[1,x,y]//c] for x,y in samples],
        remote=remote, native=native(model,N,costs))


def controls(name):
    from verify import branch, cell, geom, reconstruct, step
    g = geom.Geometry(5,3,7)
    tiles,_ = geom.read_tiles(g,name)
    polys,centroids,centre,*_ = geom.check_full_tiling(g,tiles)
    matched,_ = geom.long_pairs(g,tiles,polys,centroids,centre)
    lifts,T = reconstruct(g,tiles,polys)
    C,B = T[:1],T[:-1]
    charge, population, owners = Counter(),Counter(),Counter()
    native_edges = {key:[] for key in ((B,C),(C,B),(B,T),(T,B))}
    unmatched = Counter()
    for i,tile in enumerate(tiles):
        v = lifts[i]
        long = step(v,cell(g,tile[1]+tile[3],g.vertices(tile)[-1]))
        sign = -geom.eps(tile)
        charge[v] += sign
        population[v] += 1
        owners[v,long] += sign
        if (v,long) in native_edges:
            native_edges[v,long].append((polys[i][-1],polys[i][0]))
            unmatched[v,long] += i not in matched
    vertices = set(population)|{C,B,T}
    tree = {v[:i] for v in vertices for i in range(1,len(v)+1)}
    def net(nodes,parity):
        raw = sum(charge[v] for v in nodes if v[-1][0]%2==parity)
        corrected = raw - (g.a-g.b)*(C in nodes and parity==0)
        assert corrected%g.c==0
        return corrected//g.c
    groups = [{v for v in tree if v!=B and branch(B,v)==root} for root in (C,T)]
    remaining = tree - {B} - groups[0] - groups[1]
    groups.append(remaining)
    currents = []
    for nodes,root in zip(groups,(C,T,None)):
        e,o = net(nodes,0),net(nodes,1)
        gate = sum(owners[B,v] for v in nodes)
        assert gate==(g.a-g.b)*e-g.c*o+(2*g.c if root==C else -g.c if root==T else 0)
        currents.append(gate)
        if root is not None:
            z = net(nodes-{root},0)
            inward = owners[root,B]
            assert inward==g.c*e-(g.a-g.b)*o+(g.a-g.b)*(root==C)
            outward = sum(owners[root,v] for v in nodes)
            assert outward==(g.a-g.b)*o-g.c*z
            assert abs(inward)+abs(outward)<=population[root]
    assert sum(currents)==charge[B] and sum(map(abs,currents))<=population[B]
    assert sum(population[v] for nodes in groups for v in nodes)+population[B]==len(tiles)
    # Rebuild the slant-side cut as a chain in standard physical coordinates.
    # The scalar signed populations above use the reflected path convention.
    slant_chord = ((g.A,0),(0,g.B))
    for gate,inside,outside,nodes in ((C,B,C,tree-groups[0]),(T,T,B,groups[1])):
        edges = [slant_chord]+native_edges[inside,outside]
        edges += [(s,r) for r,s in native_edges[outside,inside]]
        ends = Counter()
        for r,s in edges:
            ends[r] -= 1
            ends[s] += 1
        assert not any(ends.values())
        area = sum(geom.det(r,s) for r,s in edges)
        m = sum(population[v] for v in nodes)
        assert area==g.a*g.b*m
        if not unmatched[B,gate]:
            assert m==g.c**2
    assert not population[B] or unmatched[B,C]+unmatched[B,T]>0
    # Every exterior-free edge, including edges strictly inside the two native sectors.
    remote = 0
    for v in tree-{C,B,T}:
        parent = branch(v,B)
        nodes = {w for w in tree if w==v or branch(v,w)!=parent}
        p = v[-1][0]%2
        x,y = net(nodes,p),net(nodes,1-p)
        assert owners[v,parent]==g.c*x-(g.a-g.b)*y
        assert owners[parent,v]==(g.a-g.b)*x-g.c*y
        remote += 1
    return dict(tiles=len(tiles),native_C_T_other=currents,middle_population=population[B],
                middle_unmatched_C_T=[unmatched[B,C],unmatched[B,T]],
                sector_populations=[sum(population[v] for v in nodes) for nodes in groups],
                exterior_free_edges_checked=remote)


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    records = {'original_counts':{'3431':'OPEN','5063':'OPEN'},
               'controls_143':{s:controls(s) for s in ('known','macro')}}
    for row in ((37,26,43,222,3431,38,39,424),(43,22,8,43,5063,58,59,88)):
        records[str(row[4])] = run(*row)
    print(json.dumps(records,indent=2))

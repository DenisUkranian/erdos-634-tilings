#!/usr/bin/env python3
"""Exact support-line relaxation for charge43 cells with minority <=5.

The written proof establishes that every actual ordinary Euclidean cell
with populations(43+m,m), m<=5, induces one of these finite networks.
This checker uses only integer maximum flow. It supplies no placements.
"""
from collections import deque
from itertools import product, permutations
import json
from pathlib import Path


def triples(n):
    return [(i,j,n-i-j) for i in range(n+1) for j in range(n-i+1)]


def maxflow(n,edges,source,sink,with_witness=False):
    graph=[[] for _ in range(n)]
    forward=[]
    for u,v,c in edges:
        forward.append((u,len(graph[u])))
        graph[u].append([v,c,len(graph[v])])
        graph[v].append([u,0,len(graph[u])-1])
    answer=0
    while True:
        parent=[None]*n; parent[source]=(-1,-1)
        todo=deque([source])
        while todo and parent[sink] is None:
            u=todo.popleft()
            for k,(v,c,_) in enumerate(graph[u]):
                if c and parent[v] is None:
                    parent[v]=(u,k); todo.append(v)
                    if v==sink:break
        if parent[sink] is None:break
        delta=10**9; v=sink
        while v!=source:
            u,k=parent[v]; delta=min(delta,graph[u][k][1]); v=u
        v=sink
        while v!=source:
            u,k=parent[v]; edge=graph[u][k]
            edge[1]-=delta; graph[v][edge[2]][1]+=delta; v=u
        answer+=delta
    reached={source}; todo=[source]
    for u in todo:
        for v,c,_ in graph[u]:
            if c and v not in reached:reached.add(v);todo.append(v)
    cut=sum(c for u,v,c in edges if u in reached and v not in reached)
    assert cut==answer
    flow=[c-graph[u][k][1] for (u,v,c),(_,k) in zip(edges,forward)]
    balance=[0]*n
    for (u,v,c),f in zip(edges,flow):
        assert 0<=f<=c
        balance[u]-=f;balance[v]+=f
    assert balance[source]==-answer and balance[sink]==answer
    assert all(x==0 for i,x in enumerate(balance) if i not in (source,sink))
    if with_witness:
        return answer,{'edges_with_flow':[[u,v,c,f] for (u,v,c),f in zip(edges,flow) if f],
                       'source':source,'sink':sink,'cut_capacity':cut}
    return answer


def flow_for(groups,m,with_witness=False):
    # A,B,D,E,Z,free unit targets. Z has no baseline b target.
    net=((1,6),(8,5),(2,12),(9,11),(7,0),(0,1))
    sources=[];targets=[]
    for g,counts in enumerate(groups):
        M,L=net[g]
        for axis,count in enumerate(counts):
            if not count:continue
            if M:sources.append((axis,count,M))
            if L:targets.append((axis,count,L))
    ls=len(sources);lt=len(targets)
    source=ls+lt; free=source+1;sink=free+1
    edges=[]
    for i,(axis,count,M) in enumerate(sources):
        edges.append((source,i,count*M))
        for j,(other,num,L) in enumerate(targets):
            if axis!=other:edges.append((i,ls+j,count*num))
    for j,(axis,count,L) in enumerate(targets):
        edges.append((ls+j,sink,count*L))
        edges.append((free,ls+j,count*L))
    edges.append((source,free,m))
    assert sum(c*M for _,c,M in sources)==43
    assert sum(c*L for _,c,L in targets)==43+m
    result=maxflow(sink+1,edges,source,sink,with_witness)
    if with_witness:
        result[1]['source_groups']=sources;result[1]['target_groups']=targets
    return result


def canonical(groups):
    key=tuple(groups)
    return all(key<=tuple(tuple(g[k] for k in perm) for g in groups)
               for perm in permutations(range(3)))


def verify(m):
    count_cases=0;count_axes=0;degree_rejected=0;flow_rejected=0;survivors=[]
    for d in range(5):
      for e in range(5-d):
        for b in range(9-2*d-2*e):
            a=8-b-2*d-2*e;t=5-b-e
            if not 0<=t<=m:continue
            r=a+b+d+e
            rM=r+t+m;rL=r+m-t
            if (a and rM<7) or (b and rL<9) or (d and rM<13) or (e and (rM<12 or rL<10)):
                continue
            count_cases+=1
            for groups in product(*(triples(n) for n in (a,b,d,e,t,m-t))):
                if not canonical(groups):continue
                count_axes+=1
                target_counts=tuple(sum(groups[g][j] for g in (0,1,2,3,5)) for j in range(3))
                total_targets=sum(target_counts)
                if any(groups[g][j] and M>total_targets-target_counts[j]
                       for g,M in ((0,1),(1,8),(2,2),(3,9),(4,7)) for j in range(3)):
                    degree_rejected+=1;continue
                value=flow_for(groups,m)
                if value<43+m:flow_rejected+=1
                else:
                    _,witness=flow_for(groups,m,True)
                    survivors.append({'types':[a,b,d,e],'zero_lines':t,'groups':groups,'flow':value,'witness':witness})
    return {'minority':m,'net_type_cases':count_cases,'axis_assignments':count_axes,
            'degree_rejected':degree_rejected,'flow_rejected':flow_rejected,
            'surviving_patterns':len(survivors),'first_survivor':survivors[:1]},survivors


def local_role_checks():
    U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
    positive={};negative={}
    for j in range(6):
      for s in (-1,1):
        key=(j%3,(j+s)%3)
        rays=tuple(sorted(((-U[j][0],-U[j][1]),U[(j+s)%6])))
        dest=positive if s*(-1)**j==1 else negative
        assert key not in dest
        dest[key]=rays
    assert len(positive)==len(negative)==6
    assert set(positive)=={(i,j) for i in range(3) for j in range(3) if i!=j}
    assert all(positive[i,j]==negative[j,i] for i,j in positive)
    return {'positive_ordered_role_pairs':6,'negative_ordered_role_pairs':6,
            'opposite_role_opposite_sign_sectors_overlap':True}


def verify_3431_one_minority():
    # The written reduction leaves A=(4,3) nine times and D=(1,10)
    # once as the only case at m=1. At m=0 degree already fails.
    tested=0;rejected=0
    for A,D,E in product(triples(9),triples(1),triples(1)):
        groups=(A,D,E)
        if not canonical(groups):continue
        tested+=1
        sources=[];targets=[]
        for g,(M,L) in enumerate(((4,3),(1,10),(0,1))):
          for axis,count in enumerate(groups[g]):
            if not count:continue
            if M:sources.append((axis,count,M))
            if L:targets.append((axis,count,L))
        ls=len(sources);lt=len(targets);source=ls+lt;free=source+1;sink=free+1;edges=[]
        for i,(axis,count,M) in enumerate(sources):
            edges.append((source,i,count*M))
            for j,(other,num,L) in enumerate(targets):
                if axis!=other:edges.append((i,ls+j,count*num))
        for j,(axis,count,L) in enumerate(targets):
            edges.append((ls+j,sink,count*L));edges.append((free,ls+j,count*L))
        edges.append((source,free,1))
        value=maxflow(sink+1,edges,source,sink)
        assert value<38
        rejected+=1
    return {'minority':1,'axis_assignments':tested,'flow_rejected':rejected,'proved_minority_lower_bound':2}


def signed_frontier_control():
    A1=[('A1',i) for i in range(2)]
    A2=[('A2',i) for i in range(6)]
    Z=[('Z',i) for i in range(5)]
    O1=[('O1',i) for i in range(4)]
    O2=[('O2',0)]
    axis={line:ax for lines,ax in ((A1,1),(A2,2),(Z,0),(O1,1),(O2,2)) for line in lines}
    positive=[(z,a) for z in Z for a in A2]
    positive.extend((z,A1[i%2]) for i,z in enumerate(Z))
    positive.extend(zip(A1+O1,A2))
    positive.extend((a,A1[0 if i<3 else 1]) for i,a in enumerate(A2+O2))
    negative=list(zip(O1+O2,Z))
    assert len(positive)==len(set(positive))==48
    assert len(negative)==len(set(negative))==5
    assert all(axis[a]!=axis[b] for a,b in positive+negative)
    assert not set(positive)&{(b,a) for a,b in negative}
    rows={line:[0,0,0,0] for line in axis}
    for a,b in positive:rows[a][0]+=1;rows[b][2]+=1
    for a,b in negative:rows[a][1]+=1;rows[b][3]+=1
    for line,(Mp,Mn,Lp,Ln) in rows.items():
        assert (Mp-Mn+7*(Lp-Ln))%43==0
        if line in A1+A2:assert (Mp,Mn,Lp,Ln)==(1,0,6,0)
        elif line in Z:assert (Mp,Mn,Lp,Ln)==(7,0,0,1)
        else:assert (Mp,Mn,Lp,Ln)==(1,1,0,0)
    control={'scope':'Abstract signed supporting-line incidence only. No coordinates or nonoverlapping placements supplied.',
             'positive':positive,'negative':negative,
             'lines':[{'name':line,'axis':axis[line],'counts_Mplus_Mminus_Lplus_Lminus':rows[line]} for line in axis]}
    Path(__file__).with_name('SIGNED_LINE_FRONTIER_5063.json').write_text(json.dumps(control,indent=2)+'\n')
    return {'positive':48,'negative':5,'lines':len(axis),
            'all_line_congruences':True,'all_ordered_pair_capacities':True,
            'all_opposite_role_sector_conflicts_avoided':True,
            'physical_realization_asserted':False}


def main():
    rows=[];frontier=[]
    for m in range(6):
        row,survivors=verify(m);rows.append(row)
        if m==5:frontier=survivors
    result={'scope':__doc__,'local_rigid_role_controls':local_role_checks(),
            'results':rows,'3431':verify_3431_one_minority(),
            'signed_next_case_control':signed_frontier_control()}
    assert all(row['surviving_patterns']==0 for row in result['results'][:5])
    result['proved_minority_lower_bound']=5
    result['actual_tiling_or_cell_constructed']=False
    assert len(frontier)==25
    Path(__file__).with_name('CELL_MINORITY_FRONTIER_5063.json').write_text(json.dumps({
        'scope':'Necessary relaxed support-line networks only; no actual positions, endpoint-current solution or packing is asserted.',
        'minority':5,'group_order':['A','B','D','E','Z','extra_unit_targets'],
        'patterns':frontier},indent=2)+'\n')
    Path(__file__).with_name('CELL_MINORITY_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

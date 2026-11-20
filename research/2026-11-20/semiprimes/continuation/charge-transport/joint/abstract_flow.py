#!/usr/bin/env python3
"""Exact phase/axis/contact-port countermodels. These are NOT geometric tilings.

The port graph retains side labels, whole fixed mates, axis directions, phase
nodes, full boundary ports and connectivity. It has no common vertex coordinates,
per-supporting-line identity, planar sector embedding, nonoverlap or coverage.
"""
from collections import Counter,defaultdict
from pathlib import Path
import argparse,json,random,sys

U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def make_case(a,b,c,K,base,seed=634):
    assert a>b>0 and a%2==b%2==c%2==1 and c*c==a*a+a*b+b*b
    N=(a+2*b)*(2*a+b);A=b*(2*a+b);H=a*(a+2*b);d=a-b
    assert K>=3 and K%2==1
    t=(K-3)*c//2;m=(N-K*c-d)//2
    assert t>=0 and m>=0 and 2*m+K*c+d==N
    base=Path(base);sys.path[:0]=[str(base/'global-endpoints/integer'),str(base/'vertex-phase')]
    from global_core_sat import Geometry
    from phase_budget import PhaseBudget
    g=Geometry(a,b,c);pb=[PhaseBudget(g,s)for s in(1,-1)]
    cells={'core':((0,0,0),0),'closed':((0,0,0),1),'middle':((0,H,0),1),'outer':((A,0,0),2)}
    node={name:tuple(p.node(q,p.sign*h)for p in pb)for name,(q,h)in cells.items()}
    # The ordinary short cell lies on the exterior-containing spine in both trees.
    assert all(not p.exterior_free(node['middle'][i])for i,p in enumerate(pb))
    assert pb[0].exterior_free(node['closed'][0])
    assert node['middle'][0]!=node['closed'][0]
    assert node['middle'][1]==node['closed'][1]
    assert all(node['core'][i]==(0,0,0)for i in(0,1))
    for own,long in [('core','closed'),('core','middle'),('middle','core'),('middle','outer')]:
        for tree,p in enumerate(pb):
            q,h=cells[own];r,k=cells[long];l=p.sign*h;n=p.sign*k
            assert abs(l-n)==1
            if l<n:assert p.node(r,l)==p.node(q,l)
            else:assert p.node(q,n)==p.node(r,n)
    # One exact type realization (not containment) for every orientation/cell edge.
    def type_membership(own,long,j,s):
        h=cells[own][1];u=(0,0,0)if long=='closed' else(0,H,0)
        if own=='middle'and long=='core':u=(0,H,0)
        if long=='outer':u=(0,H,0)
        q=g.add(u,g.scale(a,g.unit(h,j)));tile=q,h,j,s
        vertices=g.vertices(tile)
        for i,p in enumerate(pb):
            assert p.node(q,p.sign*h)==node[own][i]
            assert all(p.node(v,p.sign*h)==node[own][i]for v in vertices)
            assert p.node(u,p.sign*(h+s))==node[long][i]
        assert not any(p.required(tile)for p in pb)
    types=[('core_plus','core','closed',0,1,m),('core_minus','core','closed',3,1,m),
           ('core_source','core','middle',3,1,d),
           ('middle_down_base0','middle','core',0,-1,c),
           ('middle_down_pair0','middle','core',0,-1,t),
           ('middle_down_pair3','middle','core',3,-1,t),
           ('middle_down_base4','middle','core',4,-1,c),
           ('middle_up_boundary','middle','outer',4,1,c)]
    for _,own,long,j,s,count in types:
        if count:type_membership(own,long,j,s)
    # Tile IDs are just combinatorial copies. Distinct geometric placements are not supplied.
    tiles=[];tag_ids={};ports=[];tile_ports=[]
    currents=Counter();pop=defaultdict(Counter);flow=defaultdict(Counter)
    for tag,own,long,j,s,count in types:
        tag_ids[tag]=[];h=cells[own][1];eps=s*(-1)**j
        for _ in range(count):
            tile_id=len(tiles);tiles.append((own,long,h,j,s,eps));tag_ids[tag].append(tile_id)
            pop[own][eps]+=1;flow[own,long][eps]+=1
            ps=[]
            for side,cell,J,L,sgn in [('a',own,j,a,s),('b',own,(j+s)%6,b,s),('c',long,j,c,-s)]:
                axis=J%3;direction=sgn*(1 if J<3 else-1)
                port_id=len(ports);ports.append((tile_id,side,cell,axis,direction,L));ps.append(port_id)
                currents[cell,axis]+=direction*L
            tile_ports.append(ps)
    assert len(tiles)==N
    boundary={('core',0):A,('core',1):-H,('outer',1):c*c}
    assert {k:v for k,v in currents.items()if v}==boundary
    assert sum(v[5]for v in tiles if v[2]%2)==-c
    assert sum(v[5]for v in tiles if v[2]%2==0)==-d
    assert pop['middle'][1]==(K-1)*c//2 and pop['middle'][-1]==(K+1)*c//2
    # Exact signed populations, joint-cell reserve, and node budgets in both prime trees.
    tree_reports=[]
    for tree,p in enumerate(pb):
        by=defaultdict(Counter);joint_by=defaultdict(list)
        for cell,count in pop.items():
            by[node[cell][tree]].update(count);joint_by[node[cell][tree]].append(count)
        for key,count in by.items():
            if key==(0,0,0):continue
            assert count[1]%c==count[-1]%c==0 and sum(count.values())>=2*c
            charges=[(x[1]-x[-1])//c for x in joint_by[key]]
            assert all((x[1]-x[-1])%c==0 for x in joint_by[key])
            P=sum(max(q,0)for q in charges);Q=sum(max(-q,0)for q in charges)
            unit=sum(abs(q)==1 for q in charges);reserve=(unit+c-1)//c
            assert count[1]//c>=P+reserve and count[-1]//c>=Q+reserve
        ordinary=[key for key in by if key!=(0,0,0)]
        assert len(ordinary)==1
        j=N%c;rp=((j-d)*pow(2,-1,c))%c;rm=((j+d)*pow(2,-1,c))%c
        assert by[0,0,0][1]%c==rp and by[0,0,0][-1]%c==rm
        tree_reports.append({'sign':p.sign,'occupied_ordinary_nodes':1,'core_sign_counts':[by[0,0,0][1],by[0,0,0][-1]],'ordinary_sign_counts':[pop['middle'][1],pop['middle'][-1]],'required_exterior_free_nodes':0})
    # Match designated whole long sides first. This is the closed-gate condition.
    parent=list(range(N+1));size=[1]*(N+1);internal=list(range(N));internal_size=[1]*N;outside=N;used=set();locked_pairs=0;boundary_tiles=set()
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def internal_find(x):
        while internal[x]!=x:internal[x]=internal[internal[x]];x=internal[x]
        return x
    def union(x,y):
        if x<N and y<N:
            ix=internal_find(x);iy=internal_find(y)
            if ix!=iy:
                if internal_size[ix]<internal_size[iy]:ix,iy=iy,ix
                internal[iy]=ix;internal_size[ix]+=internal_size[iy]
        x=find(x);y=find(y)
        if x==y:return
        if size[x]<size[y]:x,y=y,x
        parent[y]=x;size[x]+=size[y]
    def lock_pair(i,j):
        nonlocal locked_pairs
        pi,pj=tile_ports[i][2],tile_ports[j][2];x,y=ports[pi],ports[pj]
        assert pi not in used and pj not in used
        assert x[2:4]==y[2:4]and x[4]==-y[4]and x[5]==y[5]==c
        assert tiles[i][2:5]==(tiles[j][2],(tiles[j][3]+3)%6,tiles[j][4])
        assert tiles[i][5]==-tiles[j][5]
        used.update((pi,pj));union(i,j);locked_pairs+=1
    for left,right in [('core_plus','core_minus'),('middle_down_pair0','middle_down_pair3')]:
        for i,j in zip(tag_ids[left],tag_ids[right]):lock_pair(i,j)
    # Cover each outer side by complete tile-side ports, with at least one c side.
    def partition(length,small):
        for nc in range(1,c+1):
            rest=length-nc*c
            if rest>=0 and rest%small==0:return rest//small,nc
        raise AssertionError('No requested two-length boundary partition')
    ra,sx=partition(A,a);rb,sy=partition(H,b)
    assert ra<=m and rb<=m and sx<=c and sy<=c
    consumed=Counter()
    def use_boundary(ids,side,length,cell,axis,sign):
        for i in ids:
            port=tile_ports[i][side];data=ports[port]
            assert port not in used and data[2:]==(cell,axis,sign,length)
            used.add(port);union(i,outside);boundary_tiles.add(i);consumed[cell,axis]+=sign*length
    use_boundary(tag_ids['core_plus'][:ra],0,a,'core',0,1)
    use_boundary(tag_ids['middle_down_base0'][:sx],2,c,'core',0,1)
    use_boundary(tag_ids['core_minus'][:rb],1,b,'core',1,-1)
    use_boundary(tag_ids['middle_down_base4'][:sy],2,c,'core',1,-1)
    use_boundary(tag_ids['middle_up_boundary'],2,c,'outer',1,1)
    assert dict(consumed)==boundary
    # Unit-length ports permit T contacts. Matching never supplies Euclidean coordinates.
    groups=defaultdict(lambda:[[],[]])
    for pid,(i,side,cell,axis,sgn,length)in enumerate(ports):
        if pid not in used:groups[cell,axis][0 if sgn==1 else 1].extend([i]*length)
    rng=random.Random(seed);unit_contacts=0
    for (cell,axis),(positive,negative)in sorted(groups.items()):
        assert len(positive)==len(negative)
        rng.shuffle(negative)
        for i,j in zip(positive,negative):
            assert i!=j and abs(tiles[i][2]-tiles[j][2])<=2
            union(i,j);unit_contacts+=1
    connected=len({find(i)for i in range(N+1)})==1
    tile_components=len({internal_find(i)for i in range(N)})
    assert connected and tile_components==1
    return {'format':'joint-axis-port-countermodel-v1','tile':[a,b,c],'N':N,'K':K,'m':m,'t':t,
            'scope':'Exact abstract population/phase/axis/contact-port network. No common coordinates, supporting-line placement, planar sector embedding, nonoverlap or tiling are asserted.',
            'inventory':[{'tag':tag,'short_cell':own,'long_cell':long,'h':cells[own][1],'j':j,'s':s,'count':count}for tag,own,long,j,s,count in types],
            'joint_cells':{name:{'h':h,'anchor':q,'prime_nodes':node[name]}for name,(q,h)in cells.items()},
            'signed_flows':[{'source':v,'target':w,'positive':n[1],'negative':n[-1],'net':n[1]-n[-1]}for(v,w),n in sorted(flow.items())],
            'node_populations':{v:{'positive':n[1],'negative':n[-1],'total':sum(n.values()),'G':n[1]-n[-1]}for v,n in sorted(pop.items())},
            'axis_boundary':[[cell,axis,value]for(cell,axis),value in sorted(boundary.items())],
            'height_totals':{'G_even':-d,'G_odd':-c,'n0':N-K*c,'n1':K*c},'prime_tree_checks':tree_reports,
            'boundary_partitions':{'A':[ra,'a',sx,'c'],'H':[rb,'b',sy,'c'],'c_squared':[c,'c']},
            'contact_port_graph':{'whole_halfturn_pairs':locked_pairs,'unpaired_long_tiles':N-2*locked_pairs,'boundary_tiles':len(boundary_tiles),'remaining_unit_contacts':unit_contacts,'connected_to_exterior':connected,'tile_contact_components':tile_components,'random_matching_seed':seed},
            'target_status':'OPEN'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--base',default=Path(__file__).resolve().parents[2]);p.add_argument('--out');args=p.parse_args()
    records=[make_case(*abc,K,args.base)for abc,K in[((33,7,37),15),((35,13,43),17),((5,3,7),15)]]
    for r in records:print(json.dumps({k:r[k]for k in('tile','N','m','t','height_totals','boundary_partitions','contact_port_graph')}),flush=True)
    if args.out:Path(args.out).write_text(json.dumps({'scope':'Abstract necessary-condition countermodels, not geometric tilings.','cases':records},indent=2)+'\n')

"""Exact relaxed census of all charge placements with at most five excess blocks."""
from itertools import product
from collections import Counter
import json

from reserve import HERE, UNITS, subtract, scale, multiply, gate


def support(a,b,c):
    # Directly name the actual hand and gate of a tile from an acute endpoint.
    template=[]
    for x,y,j,h in product(range(c),range(c),range(6),(-1,1)):
        q=(x,y)
        u=subtract(q,scale(a,UNITS[j]))
        dx,dy=scale(b,UNITS[(j+h)%6])
        w=(x+dx,y+dy)
        gate=(c if h==1 else 0)+multiply((a+b,-b) if h==1 else (a,b),u)[0]%c
        sign=h*(-1)**j
        if sign>0 and gate!=c:
            continue
        entries=[(j,q,h),(j,u,-h),(j+h,w,h),(j+h,q,-h)]
        template.append((sign,gate,[(k%3,p[0]%c,p[1]%c,n) for k,p,n in entries]))
    remaining=[]
    for extra in range(2*c):
        if extra in (0,c):
            continue
        cols=[row for row in template if row[0]>0 or row[1] in (0,extra)]
        while cols:
            positive,negative=set(),set()
            for _,_,col in cols:
                for k,x,y,n in col:
                    (positive if n>0 else negative).add((k,x,y))
            shared=positive & negative
            more=[item for item in cols if all((k,x,y) in shared for k,x,y,n in item[2])]
            if len(more)==len(cols):
                break
            cols=more
        assert all(g!=0 for _,g,_ in cols)
        if cols:
            remaining.append([extra,len(cols)])
    return remaining


def initial_profiles(c,d):
    alpha,den=(43,222) if c==37 else (8,43)
    ratio,scale_den=(3810,1002) if c==37 else (4304,1001)
    survivors=[]
    for k in range(4):
        for attachment in (range(3) if k else (0,)):
            # Vertex order C,B,T, followed by charged off-spine vertices from the spine.
            n=3+k
            neighbors=[[] for _ in range(n)]
            edges=[(0,1),(1,2)]
            if k:
                edges.extend([(attachment,3)]+[(i,i+1) for i in range(3,n-1)])
            for i,j in edges:
                neighbors[i].append(j)
                neighbors[j].append(i)
            def far(v,parent):
                return [v]+[u for nbr in neighbors[v] if nbr!=parent for u in far(nbr,v)]
            cuts=[[far(j,i) for j in row] for i,row in enumerate(neighbors)]
            for extra in product(range(6),repeat=n-1):
                if sum(extra)>5 or max(extra)<3 or (k and extra[-1]<3) or 0 in extra[2:]:
                    continue
                sizes=(0,)+tuple(2+h for h in extra)
                for ordinary in product(*(range(2-size,size,2) for size in sizes[1:])):
                    if 0 in ordinary[2:]:
                        continue
                    for tail in product((0,1),repeat=k):
                        parity=(0,1,0)+tail
                        if sum(g for g,p in zip(ordinary,parity[1:]) if p)!=1:
                            continue
                        core=-sum(g for g,p in zip(ordinary,parity[1:]) if not p)
                        charges=(core,)+ordinary
                        currents=[]
                        for i in range(1,n):
                            q=[]
                            for side in cuts[i]:
                                e=sum(charges[t] for t in side if not parity[t])
                                o=sum(charges[t] for t in side if parity[t])
                                C,T=int(0 in side),int(2 in side)
                                q.append(d*e-c*o+2*c*C-c*T if parity[i] else d*o-c*e-d*C)
                            assert sum(q)==charges[i]*c
                            plus=(sizes[i]+charges[i])*c//2
                            minus=(sizes[i]-charges[i])*c//2
                            if sum(max(0,x) for x in q)>plus or sum(max(0,-x) for x in q)>minus:
                                break
                            if any(x*den>alpha*plus+(den-alpha)*minus or
                                   -x*den>alpha*minus+(den-alpha)*plus for x in q):
                                break
                            if sum(x!=0 for x in q)==1 and sizes[i]*scale_den<abs(charges[i])*ratio:
                                break
                            if i==1 and not any(q[2:]):
                                if q[:2]==[2*c,-c] and sizes[i]<9:
                                    break
                                if q[:2]==[c,-c] and sizes[i]<6:
                                    break
                            currents.append(q)
                        else:
                            survivors.append((sizes,currents))
    return survivors


def check():
    tables=json.loads((HERE/'short-tree-duals.json').read_text())
    data={}
    for a,b,c in ((33,7,37),(35,13,43)):
        cert=tables[str(c)]['balanced']
        first,other,D=gate(a,b,c,cert)
        assert c*(first-other)>4*c*D
        remaining=support(a,b,c)
        if c==37:
            assert len(tables['37']['split'])==c
            for k,cert in enumerate(tables['37']['split'],1):
                first,_,D=gate(a,b,c,cert)
                assert 48*first+26*cert['table'][3*c+k]>4*c*D
        survivors=initial_profiles(c,a-b)
        classified=Counter()
        for sizes,qs in survivors:
            if sizes[1]==4 and tuple(qs[0]) in ((2*c,-2*c),(2*c,-c,-c)):
                classified['sign-exhausted native gates']+=1
            elif c==37 and any(n==4 and sorted(q)==[26,48] for n,q in zip(sizes[1:],qs)):
                classified['two positive currents at a four-block lift']+=1
            else:
                raise AssertionError((sizes,qs))
        data[str(c)]=dict(survivors_after_budget_filters=len(survivors),exclusions=classified,
                          nonempty_peeled_supports_without_slant=remaining)
    return data


if __name__=='__main__':
    if not __debug__:
        raise SystemExit("Enable Python assertions.")
    print(json.dumps(check(),indent=2))

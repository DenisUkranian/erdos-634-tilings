"""A unit alternating charge with exactly one wrong-sign owner."""
from tempfile import TemporaryDirectory
import json
from saturation import letters,triples,maximum
from triangle import cap
from charged import compile_at,evaluate

def prefixes(a,b,c,j):
    # The exceptional last letter is minus moves[j].
    length=c+a-b+1
    moves,_=letters(a,b,c,a)
    dx,dy=moves[j]
    for low in range(length+1):
        high={(c*(k-s),c*(i-k)):(i,s,k) for i,s,k in triples(length-low)}
        for i,s,k in triples(low):
            x,y=i-s,s-k
            h=high.get((dx-(a+b)*x-b*y,dy+b*x-a*y))
            if h is None:
                continue
            v=(i,h[0],s,h[1],k,h[2])
            for q in (a,b):
                _,proj=letters(a,b,c,q)
                totals=[0]*3
                for n,(f,e) in zip(v,proj):
                    totals[f]+=n*e
                f,e=proj[j]
                totals[f]-=e
                if any(t%q for t in totals): break
            else:
                yield v

def mate(v,j):
    return tuple(v[(1-k)%6] for k in range(6)),1-j

def run(tmp):
    scalar=compile_at(tmp,'scalar','inventory.cpp')
    bin11=compile_at(tmp,'q11','affine.cpp',['-DFIELD_SIZE=11'])
    bin29=compile_at(tmp,'q29','affine.cpp',['-DFIELD_SIZE=29'])
    out={}
    for N,a,b,c in [(3431,33,7,37),(5063,35,13,43)]:
        table={}
        index={}
        for j in (0,1):
            for v in prefixes(a,b,c,j):
                scores=[evaluate(scalar,a,b,c,q,*v) for q in (a,b)]
                if c==43:
                    # Independent top-down parsing with a specified final factor.
                    assert [maximum(a,b,c,v,q,j) for q in (a,b)]==scores
                bound=min(scores)
                test=None
                # It is sufficient to certify one member of each mirror pair.
                if c==43 and j==0 and bound>=59*c*a*b:
                    for binary,p in [(bin11,11),(bin29,29)]:
                        for params in [(1,1,0),(2,1,2)]:
                            val=evaluate(binary,a,b,c,b,*v,*params,j)
                            if val<bound:
                                bound=val
                                test=dict(field=p,params=params,upper=val)
                            if bound<59*c*a*b: break
                        if bound<59*c*a*b: break
                row=dict(exception_axis=j,prefix=v,area_maxima=scores)
                if test: row['quotient']=test
                table[v,j]=row
                index[v,j]=bound
        upper=cap(N,a*b,c*(c+a-b+2))
        max_tiles=0
        for (v,j),row in table.items():
            bound=min(index[v,j],index[mate(v,j)])
            k=int(min(upper/c,bound//(a*b*c)))
            tiles=c*(k-(k+1)%2)
            row['cap']=tiles
            max_tiles=max(max_tiles,tiles)
        out[N]=dict(physical_cap=str(upper),prefix_count=len(table),maximum=max_tiles,
                    profiles=list(table.values()))
    return out

if __name__=='__main__':
    with TemporaryDirectory() as tmp:
        print(json.dumps(run(tmp),indent=2))

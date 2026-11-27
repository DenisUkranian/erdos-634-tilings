"""Verify all signed inventories, both scalar parsers, and joint quotient bounds."""
from itertools import combinations
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from saturation import inventories,letters

HERE=Path(__file__).resolve().parent
SCALAR=json.loads((HERE/'SATURATION.json').read_text())

def normalize(v):
    return min(v[h:]+v[:h] for h in (0,2,4))
def mirror(v):
    return normalize(tuple(v[(3-j)%6] for j in range(6)))

def compile_at(tmp,name,src,flags=()):
    path=str(Path(tmp)/name)
    subprocess.run(['c++','-std=c++17','-O3',*flags,str(HERE/src),'-o',path],check=True)
    return path

def evaluate(bin,*args):
    return int(subprocess.check_output([bin,*map(str,args)]))

def review_field(binary):
    # An open, monotone two-heading test with the 143 tile parameters.
    # Primary product is identity for all orders of these fifteen letters.
    # Compose explicit permutations in reverse order on the point zero.
    a,b,c,p=5,3,7,11
    v=(5,0,0,10,0,0)
    moves,proj=letters(a,b,c,a)
    g=next(i for i in range(2,p) if pow(i,a,p)==1)
    perm={}
    for j in (0,3):
        f,e=proj[j]
        center=(0,1,2)[f]
        perm[j]=[(center+pow(g,e%a,p)*(x-center))%p for x in range(p)]
    scores=[]
    for positions in combinations(range(15),5):
        word=[3]*15
        for j in positions: word[j]=0
        z=0
        for j in reversed(word): z=perm[j][z]
        if z: continue
        x=y=area=0
        for j in word:
            u,w=moves[j]
            area+=x*w-y*u
            x,y=x+u,y+w
        scores.append(area)
    result=evaluate(binary,a,b,c,b,*v,1,1,2)
    assert 0<len(scores)<3003 and result==max(scores)
    return dict(accepted=len(scores),area=result)

def run(tmp):
    scalar=compile_at(tmp,'scalar','inventory.cpp')
    settings={37:((5,12,12,9,9,16),67,(4,3,2)),
              43:((3,16,9,10,10,17),11,(1,1,0))}
    out={}
    for a,b,c in [(33,7,37),(35,13,43)]:
        caps={}
        rows=SCALAR[str(c)]
        assert [list(v) for v in inventories(a,b,c)]==[r['inventory'] for r in rows]
        for row in rows:
            v=tuple(row['inventory'])
            vals=[evaluate(scalar,a,b,c,q,*v) for q in (a,b)]
            assert vals==row['area_maxima']
            units=min(vals)//(a*b*c)
            caps[v]=c*(units-(units+1)%2)
            assert caps[v]==row['population_cap']
        v,field,params=settings[c]
        binary=compile_at(tmp,'affine'+str(c),'affine.cpp',[f'-DFIELD_SIZE={field}'])
        upper=evaluate(binary,a,b,c,b,*v,*params)
        assert 0<=upper<=next(r['area_maxima'][1] for r in rows if tuple(r['inventory'])==v)
        units=upper//(a*b*c)
        cap=c*(units-(units+1)%2)
        for w in (v,mirror(v)): caps[w]=min(caps[w],cap)
        by_low={}
        for w,size in caps.items():
            low=sum(w[::2])
            by_low[low]=max(by_low.get(low,0),size)
        out[c]=dict(affine_field=field,parameters=params,inventory=v,mirrored=mirror(v),
                    joint_area_upper=upper,corrected_cap=cap,by_low=by_low,
                    maximum=max(caps.values()))
    test_bin=compile_at(tmp,'review','affine.cpp',['-DFIELD_SIZE=11'])
    out['direct_action_check']=review_field(test_bin)
    return out

if __name__=='__main__':
    with TemporaryDirectory() as tmp:
        print(json.dumps(run(tmp),indent=2))

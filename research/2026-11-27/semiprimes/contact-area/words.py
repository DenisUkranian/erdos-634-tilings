"""Replay the scalar word bound and the boundary populations at small budgets."""
import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from reserve import table
from saturation import UNITS

HERE=Path(__file__).resolve().parent

def grammar(binary,a,b,c,order,limit,saturated=0):
    output=subprocess.check_output([binary,*map(str,(a,b,c,order,limit,saturated))],text=True)
    return {(n,l):v for n,l,v in (map(int,row.split()) for row in output.splitlines())}

def direct(a,b,c,q,depth=4):
    # Literal group stacks, meet in the middle. Translate the second half to
    # the origin and reverse its steps. Closing cancels the cross determinant.
    moves=[]
    for j,(x,y) in enumerate(UNITS):
        u,v=UNITS[j-1]
        for low in (True,False):
            h=(j-1)%6 if low and q==a else j
            power=((b if q==a else a) if low else c)*(1 if h<3 else -1)
            dx,dy=(a*x+b*u,a*y+b*v) if low else (c*x,c*y)
            moves.append((dx,dy,h%3,power))
    layers=[]
    def visit(x,y,s,stack,left):
        key=(x,y,stack)
        best=layers[depth-left]
        lo,hi=best.get(key,(s,s))
        best[key]=(min(lo,s),max(hi,s))
        if left:
            for u,v,f,e in moves:
                z=stack
                if z and z[-1][0]==f:
                    e+=z[-1][1]
                    z=z[:-1]
                if e%q:
                    z+=((f,e%q),)
                visit(x+u,y+v,s+x*v-y*u,z,left-1)
    layers=[{} for _ in range(depth+1)]
    visit(0,0,0,(),depth)
    return {2*d:max(hi-lo for lo,hi in layers[d].values()) for d in range(1,depth+1)}

def run(binary):
    out={}
    for a,b,c,limit in [(33,7,37,42),(35,13,43,22)]:
        circ=grammar(binary,a,b,c,a,limit)
        for q in (a,b):
            small=grammar(binary,a,b,c,q,8)
            assert direct(a,b,c,q)=={n:small[n,0] for n in (2,4,6,8)}
        # Below c+d every individual circuit has zero alternating charge,
        # an even length and positive area in units of 2c. Bound the sum of
        # all positive interiors, permitting any even partition.
        cap={0:0}
        min_length=10 if c==37 else 12
        for m in range(2,limit+1,2):
            cap[m]=max([0]+[cap[m-k]+(2*c)*(circ[k,0]//(2*c*a*b))
                             for k in range(min_length,m+1,2) if (k,0) in circ])
        determinant=table(a,b,c,limit)
        bounds={m:min(cap[m],row['population_cap']) for m,row in determinant.items()}
        two=max((v+bounds[j] for i,v in bounds.items() for j in bounds if i+j<=limit),default=None)
        out[c]=dict(circuit_max_area={n:v for (n,_),v in circ.items() if n%2==0},
                    neutral_branch_caps=bounds,one=max(bounds.values()),two_disjoint=two)
    return out

if __name__=='__main__':
    with TemporaryDirectory() as tmp:
        binary=str(Path(tmp)/'word-area')
        subprocess.run(['c++','-O3','-std=c++17',str(HERE/'word_area.cpp'),'-o',binary],check=True)
        print(json.dumps(run(binary),indent=2))

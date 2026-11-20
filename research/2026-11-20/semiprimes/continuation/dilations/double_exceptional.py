"""Eight exact doubled F2 constructions in the exceptional v=1 progression."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from controls.profiles import make
from controls.verify_grids import check


def doubled(u):
    if u not in range(4,26,3):
        raise ValueError('supported parameters are 4,7,...,25')
    a,b,c=(u*u-1)//3,(2*u+1)//3,(u*u+u+1)//3
    if u == 7:
        return make(a,b,c,2,1,[(3,2,1)]*11)
    if u == 4:
        return make(a,b,c,2,2,[(c-b,c-a,2)]*2)
    high=(u-7)//3
    steps=[]
    for i in range(u+4):
        m=4 if i<high else 1
        r=(1+(u+1)*m)//3-(2*b if i==high-1 else 0)
        s=(u-m)//3
        steps.append((r,s,3 if i<high-1 else 1))
    return make(a,b,c,2,3,steps)


if __name__=='__main__':
    for u in range(4,26,3):
        witness=doubled(u)
        print(u,witness['tile'],check(witness))

"""Exclude an 86-tile layer between two nested saturated ordinary mixed gates."""
from itertools import permutations, product
from pathlib import Path
import base64
import json
import zlib
from two_current import U

C,A,B=43,35,13
P=-A*pow(B,-1,C)%C
M=-B*pow(A,-1,C)%C
TRIPLES=sorted({t for seed in [(0,8,13),(1,6,14),(7,7,7)] for t in permutations(seed)})

def projected(w,slope):
    assert len(w)==3*C and all(type(x)==int for x in w)
    table={}
    for t,j,h in product(range(C),range(6),(-1,1)):
        def residue(v):return (v[0]+slope*v[1])%C
        u=(t-A*residue(U[j]))%C
        k=(j+h)%6
        v=(t+B*residue(U[k]))%C
        score=h*(w[(j%3)*C+t]-w[(j%3)*C+u]+w[(k%3)*C+v]-w[(k%3)*C+t])
        table[t,j,h]=score,u,(u+v-t)%C
    return table

def limits(w,slope):
    table=projected(w,slope)
    pairs=max(s+table[m,(j+3)%6,h][0] for (t,j,h),(s,u,m) in table.items())
    return table,pairs

def check():
    blob=Path(__file__).with_name('SHELL.duals').read_bytes().strip()
    tables=json.loads(zlib.decompress(base64.b85decode(blob)))
    opposite=tables.pop('opposite')
    reps={min(k*pow(P-1,e,C)%C for e in range(3)) for k in range(1,C)}
    assert set(map(int,tables))==reps
    for label,ws in tables.items():
        todo=set(product(TRIPLES,repeat=2))
        for w in ws:
            tab,pm=limits(w,P)
            banks=[[s for j in range(i,6,2) for t in range(C)
                    for s,u,_ in [tab[t,j,1]] if u==g] for i,g in enumerate((0,int(label)))]
            assert all(len(s)==3 for s in banks)
            todo={(x,y) for x,y in todo if 22*pm+sum(n*s for n,s in zip(x+y,banks[0]+banks[1]))>=0}
        assert not todo
    pos,neg=projected(opposite[:3*C],P),projected(opposite[3*C:],M)
    pm=-10**20
    banks=[-10**20,-10**20]
    for t,r,j,h in product(range(C),range(C),range(6),(-1,1)):
        x,u,m=pos[t,j,h]
        y,v,n=neg[r,j,h]
        pm=max(pm,x+y+pos[m,(j+3)%6,h][0]+neg[n,(j+3)%6,h][0])
        if j%2==0 and (u if h==1 else v)==0:
            i=int(h==-1)
            banks[i]=max(banks[i],x+y)
    bound=22*pm+21*sum(banks)
    assert bound<0
    return dict(same_hand_offsets=42,rotation_classes=len(reps),inventory_pairs=len(TRIPLES)**2,
                opposite_hand_pair_max=pm,opposite_hand_single_max=banks,opposite_hand_total_upper=bound)

if __name__=='__main__':
    print(json.dumps(check(),indent=2))

"""All signed population possibilities for the 224-tile quadrilateral."""
from itertools import product

a,b,c=35,13,43
N=224
boundary={-1:-172,0:143,1:575}
def enumerate_profiles():
    out=[]
    for lo in range(-2,1):
      for hi in range(1,3):
        levels=list(range(lo,hi+1))
        options=[]
        for h in levels:
            residue={0:1,1:8}.get(h,0)
            options.append([(n,g) for n in range(residue,N+1,43) if not(n==43 and h not in (0,1)) and not (not n and (h< -1 or h>1)) for g in range(-n,n+1,2) if (22*g-boundary.get(h,0))%43==0])
        for row in product(*options):
            if sum(n for n,g in row)!=N:continue
            rr=dict(zip(levels,row))
            if sum(g for n,g in row)!=-26 or sum((-1 if h%2 else 1)*g for h,(n,g) in rr.items())!=-4:continue
            # Permit a nonoccupied exterior height (−1), but do not count it twice.
            if lo==-1 and rr[lo][0]==0:continue
            if hi>1 and rr[hi][0]==0:continue
            chir={};old=0
            for z in range(lo-1,hi+2):
                n,g=rr.get(z,(0,0));x=22*g-boundary.get(z,0)
                if x%43:break
                down=x//43-old
                if z+1 in rr:
                    n2,g2=rr[z+1];up=g2-down
                    if abs(up)+abs(down)>n2:break
                    chir[z+1]=(up,down)
                elif down:break
                old=chir.get(z,(0,0))[0]
            else:out.append({h:(n,g,*chir[h]) for h,(n,g) in rr.items() if n})
    return out

if __name__=="__main__":
    profiles=enumerate_profiles()
    for row in profiles:print(row)
    assert len(profiles)==6

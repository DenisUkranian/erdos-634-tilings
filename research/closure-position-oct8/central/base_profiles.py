#!/usr/bin/env python3
"""Complete exact packing profiles of tile edges along the base of length154.
This is a necessary boundary condition, not a tiling certificate.
"""
from collections import defaultdict
import json,time
T=((0,0),(2002,0),(637,728))
# Name, height, orientation index, base length, apex in coordinates scaled13.
DATA=(('A0',0,0,8,(-91,91)),('B1',0,7,8,(104,91)),
      ('B0',0,6,7,(-104,104)),('A1',0,1,7,(91,104)),
      ('A3',1,3,13,(64,56)),('B4',-1,10,13,(49,56)))
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def triangle(k,x):
    d=DATA[k];s=13*x
    return ((s,0),(s+13*d[3],0),(s+d[4][0],d[4][1]))
def inside(t):return all(cross(T[k],T[(k+1)%3],p)>=0 for p in t for k in range(3))
def apart(a,b):
    return any(all(cross(t[k],t[(k+1)%3],p)<=0 for p in other) for t,other in ((a,b),(b,a)) for k in range(3))
OK={(x,k):inside(triangle(k,x)) for x in range(155) for k in range(6) if x+DATA[k][3]<=154}
PAIR={(a,b):apart(triangle(a,0),triangle(b,DATA[a][3])) for a in range(6) for b in range(6)}
TRIPLE={(a,b,c):apart(triangle(a,0),triangle(c,DATA[a][3]+DATA[b][3])) for a in range(6) for b in range(6) for c in range(6)}
def run():
    start=time.time()
    layers=[set() for _ in range(155)];layers[0].add(((0,)*6,-1,-1))
    record=[]
    for x in range(154):
      for counts,prev2,prev in layers[x]:
        for k,d in enumerate(DATA):
            nx=x+d[3]
            if nx>154 or not OK[x,k]:continue
            if x==0 and k not in (3,5):continue
            if nx==154 and k not in (2,4):continue
            if prev!=-1 and not PAIR[prev,k]:continue
            if prev2!=-1 and not TRIPLE[prev2,prev,k]:continue
            new=list(counts);new[k]+=1
            layers[nx].add((tuple(new),prev,k))
      if layers[x]:record.append((x,len(layers[x])))
      layers[x].clear()
    profiles=sorted({q[0] for q in layers[154]})
    return {'status':'EXHAUSTIVE_NECESSARY_BOUNDARY_PROFILES','N154_solved':False,'profiles':profiles,'profile_order':[d[:4] for d in DATA],'final_states':len(layers[154]),'count_profiles':len(profiles),'state_counts':record,'seconds':time.time()-start}
if __name__=='__main__':print(json.dumps(run(),indent=2))

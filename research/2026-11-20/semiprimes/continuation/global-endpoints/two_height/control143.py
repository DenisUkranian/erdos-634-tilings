from pathlib import Path
import json
from fractions import Fraction as F
root=Path(__file__).resolve().parent
src=root/'certificate_143.json'
d=json.loads(src.read_text())
def add(p,q):return p[0]+q[0],p[1]+q[1]
def sub(p,q):return p[0]-q[0],p[1]-q[1]
def mul(p,q):
 x,y=p;u,v=q;return x*u-y*v,x*v+y*u+y*v

def scale(n,p):return n*p[0],n*p[1]
tri=[]
for block in d['blocks']:
 pts=[tuple(F(v,d['coordinate_denominator']) for v in p) for p in block['points']]
 if block['kind']=='triangle':
  A,B,C=pts;n=block['scale'];u=scale(F(1,n),sub(B,A));v=scale(F(1,n),sub(C,A))
  for i in range(n):
   for j in range(n-i):
    p=add(A,add(scale(i,u),scale(j,v)))
    tri.append((p,add(p,u),add(p,v)))
    if i+j<n-1:tri.append((add(p,u),add(p,v),add(p,add(u,v))))
 else:
  A,B,C,D=pts;r,s=block['rows'],block['cols'];u=scale(F(1,r),sub(B,A));v=scale(F(1,s),sub(D,A))
  for i in range(r):
   for j in range(s):
    p=add(A,add(scale(i,u),scale(j,v)));pu=add(p,u);pv=add(p,v);puv=add(p,add(u,v))
    tri.extend([(p,pu,puv),(p,pv,puv)] if block['diagonal']=='sum' else [(p,pu,pv),(pu,pv,puv)])
assert len(tri)==143
vals=list(map(int,(root/'board143.in').read_text().split()));T=vals[1];offset=2+6
models=[tuple(tuple(vals[offset+6*i+2*j:offset+6*i+2*j+2]) for j in range(3)) for i in range(T)]
rows=[]
for t in tri:
 points=[mul(p,(3,-2)) for p in t]
 assert all(int(v)==v for p in points for v in p)
 points=[tuple(map(int,p)) for p in points]
 found=[]
 for p in points:
  norm={sub(q,p) for q in points}
  for i,model in enumerate(models):
   if norm==set(model):found.append((i,*p))
 assert len(found)==1,(points,found)
 rows.append(' '.join(map(str,found[0])))
(root/'board143.known').write_text('\n'.join(rows)+'\n')
print('143 exact tile coordinates expanded and matched')

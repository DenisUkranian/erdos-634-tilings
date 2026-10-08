from pathlib import Path
import json,sys

def prod(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def power(a,n):
 r=(1,0)
 for _ in range(n):r=prod(r,a)
 return r
def rot(a):return(-a[1],a[0]+a[1])
def mul(a,n):return(a[0]*n,a[1]*n)
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
prefix=Path(sys.argv[1]);r=json.loads(prefix.with_suffix('.json').read_text());L,U=r['L'],r['U'];R=r['basis_rotation'];invg=prod(power((5,1),-L),power((6,-1),U))
for _ in range(R):invg=rot(invg)
P=[prod(invg,v)for v in((0,0),(649,0),(264,264),(0,143))]
inside=lambda p:all(cross(sub(P[(i+1)%4],P[i]),sub(p,P[i]))>=0 for i in range(4))
o=0;seeds=[]
for h in range(L,U+1):
 u=prod(power((5,1),h-L),power((6,-1),U-h))
 for _ in range(R):u=rot(u)
 for order in range(2):
  a,b=mul(u,11 if order else 24),mul(rot(rot(u)),24 if order else 11)
  for j in range(6):
   tip=a if order else b;anchor=sub(P[1],tip);T=[anchor,add(anchor,a),add(anchor,b)]
   if all(inside(p)for p in T):seeds.append((o,*anchor))
   o+=1;a,b=rot(a),rot(b)
for i,s in enumerate(seeds):prefix.with_name(prefix.name+f'.seed{i}.txt').write_text('1\n'+' '.join(map(str,s))+'\n')
print(json.dumps({'L':L,'U':U,'corner_seeds':seeds}))

#!/usr/bin/env python3
"""Reconstruct theta tilings48,75,108,147,243,300 by explicit macrodissections.
Coordinates (x,y) mean physical (x,y*sqrt(15)). Exact rational generation.
"""
from fractions import Fraction as F
from math import lcm
import json
from pathlib import Path
from generate_tiling import grid,ccw,verify

if not __debug__:
 raise SystemExit("Verification requires assertions: do not run Python with -O or PYTHONOPTIMIZE.")
P=lambda x,y:(F(x),F(y))
add=lambda a,b:(a[0]+b[0],a[1]+b[1])
sub=lambda a,b:(a[0]-b[0],a[1]-b[1])
scale=lambda a,s:(a[0]*s,a[1]*s)
def parallelogram(origin,e,f,m,n):
 out=[]
 for i in range(m):
  for j in range(n):
   z=add(origin,add(scale(e,i),scale(f,j)))
   # e,f meet at gamma; the difference diagonal has length c.
   out.extend((ccw((z,add(z,e),add(z,f))),ccw((add(z,e),add(z,add(e,f)),add(z,f)))))
 return out

def seed(mu,p):
 mu=F(mu); q=F(3*p,2);t=F(p,2);r=mu-2*p;u=F(4,3)*(mu-q);v=u/2;h=3*q-2*v
 assert all(x.denominator==1 for x in (q,t,u,v,h))
 q,t,u,v,h=map(int,(q,t,u,v,h)); assert r>=0
 A=P(0,0);B=P(mu,mu);C=P(2*mu,0);P0=P(4*p,0)
 G=P(F(21*p,8),F(3*p,8));K=P(q,q);L=P(mu+u,mu-u)
 Q=P(F(29*p,8),F(3*p,8));R=P(2*mu-F(3*p,8),F(3*p,8));V=P(q+F(v,2),q-F(v,2))
 tiles=[];blocks=[]
 for name,verts,n in [('green',(A,P0,G),p),('blue',(A,G,K),q),('yellow',(B,K,L),u),('red',(P0,G,Q),t),('pink',(K,L,V),v)]:
  out=grid(verts,n);blocks.append({'name':name,'first':len(tiles),'count':len(out)});tiles+=out
 # First gamma parallelogram: both cell orientations are allowed.
 # Horizontal length L=2r; slanted H=3t. Use L=2x+3y.
 L0=2*r; assert L0.denominator==1; L0=int(L0)
 y0=0 if L0%2==0 else 1; x0=(L0-3*y0)//2; assert x0>=0
 out=parallelogram(P0,P(2,0),P(F(-3,4),F(3,4)),x0,t)
 if y0:
  assert(3*t)%2==0
  out+=parallelogram(add(P0,P(2*x0,0)),P(3,0),P(F(-1,2),F(1,2)),y0,3*t//2)
 blocks.append({'name':'base_parallelogram','first':len(tiles),'count':len(out)});tiles+=out
 # Last gamma parallelogram: horizontal side is 3v and the other is h.
 # Split h=2x+3y: (x,y)=(1,1) for48; (7,0) for108.
 y=0 if h%2==0 else 1; x=(h-3*y)//2; assert x>=0
 assert 2*x+3*y==h
 base=G
 out=parallelogram(base,P(3,0),P(F(-1,2),F(1,2)),v,x)
 blocks.append({'name':'cap_a_strips','first':len(tiles),'count':len(out)});tiles+=out
 base=add(base,P(F(-x,2),F(x,2)))
 assert y==0 or (3*v)%2==0
 out=parallelogram(base,P(2,0),P(F(-3,4),F(3,4)),3*v//2,y)
 blocks.append({'name':'cap_b_strips','first':len(tiles),'count':len(out)});tiles+=out
 return {'target':ccw((A,B,C)),'tiles':tiles,'components':blocks,'N':len(tiles),'seed_parameters':{'mu':mu,'p':p,'q':q,'t':t,'r':r,'u':u,'v':v,'h':h}}

def alpha_frame(obj):
 # Put theta apex at0, equal rays p=(12,0), q=(21/2,3/2).
 # For seed48 mu6 scale2 and seed108 mu9 scale3.
 mu=obj['seed_parameters']['mu']; B=P(mu,mu)
 # Map left down ray (-mu,-mu) to(+4mu,0): metric-orthogonal rotation.
 def f(point):
  x,y=sub(point,B)
  return P((-x-15*y)/4,(x-y)/4)
 return {'target':ccw(tuple(f(p) for p in obj['target'])),'tiles':[ccw(tuple(f(p) for p in tri)) for tri in obj['tiles']]}

def add_seeds(s2,s3):
 # p and q are vectors of theta unit target(12,12,6); angle atorigin alpha.
 p=P(12,0);q=P(F(21,2),F(3,2));m,n=2,3
 a2=alpha_frame(s2);a3=alpha_frame(s3)
 # The rotation puts the second equal ray at(+10.5,+1.5).
 flip=lambda z:P(z[0],z[1])
 t2=[ccw(tuple(flip(z) for z in tri)) for tri in a2['tiles']]
 t3=[ccw(tuple(flip(z) for z in tri)) for tri in a3['tiles']]
 first=[ccw(tuple(add(z,scale(p,n)) for z in tri)) for tri in t2]
 second=[ccw(tuple(add(z,scale(q,m)) for z in tri)) for tri in t3]
 # Alpha cell edges b and c; difference diagonal has side a.
 bridge=[];e=scale(p,F(1,4));f=scale(q,F(1,3))
 for i in range(n*4):
  for j in range(m*3):
   z=add(scale(e,i),scale(f,j))
   bridge.extend((ccw((z,add(z,e),add(z,f))),ccw((add(z,e),add(z,add(e,f)),add(z,f)))))
 return {'target':ccw((P(0,0),scale(p,m+n),scale(q,m+n))),'tiles':first+second+bridge,'N':12*(m+n)**2,'components':[{'name':'seed48','first':0,'count':48},{'name':'seed108','first':48,'count':108},{'name':'bridge','first':156,'count':144}]}

def pack(obj):
 den=lcm(*(x.denominator for tri in [obj['target']]+obj['tiles'] for p in tri for x in p))
 conv=lambda tri:[[int(x*den) for x in p] for p in tri]
 obj=dict(obj)
 if 'seed_parameters' in obj:
  obj['seed_parameters']={k:(int(v) if isinstance(v,F) and v.denominator==1 else str(v) if isinstance(v,F) else v) for k,v in obj['seed_parameters'].items()}
 return {**obj,'target':conv(obj['target']),'tiles':[conv(t) for t in obj['tiles']],'denominator':den,'D':15,'a':2,'b':3,'c':4,'u':1,'v':2,'source':('Beeson Figure21/Theorem24' if obj['N'] in(48,108) else 'mixed-strip extension of Beeson Theorem24' if obj['N'] in(147,243) else 'scale-addition construction')}
def para75(origin,e,f,m,n,diagonal):
 out=[]
 for i in range(m):
  for j in range(n):
   z=add(origin,add(scale(e,i),scale(f,j)));ze=add(z,e);zf=add(z,f);zef=add(ze,f)
   if diagonal=='sum':out.extend((ccw((z,ze,zef)),ccw((z,zf,zef))))
   else:out.extend((ccw((z,ze,zf)),ccw((ze,zef,zf))))
 return out

def construct75():
 A=P(0,0);B=P(F(15,2),F(15,2));C=P(15,0)
 P0=P(8,0);G=P(F(21,4),F(3,4));K=P(3,3);L=P(F(27,2),F(3,2))
 U=P(4,2);V=P(10,2);W=P(F(19,4),F(5,4));Z=P(F(43,4),F(5,4))
 R=P(F(45,4),F(3,4));S=P(12,0);H=P(F(37,4),F(3,4));J=P(F(21,2),F(3,2))
 pieces=[('green_square',grid((A,P0,G),2)),('blue_square',grid((A,G,K),3)),('yellow_square',grid((B,K,L),6)),
 ('patch_square',grid((K,U,V),2)),
 ('upper_strip',para75(U,P(2,0),P(F(3,4),F(-3,4)),3,1,'sum')),
 ('middle_strip',para75(W,P(3,0),P(F(1,2),F(-1,2)),2,1,'sum')),
 ('lower_strip',para75(G,P(4,0),P(F(11,8),F(-3,8)),1,2,'difference')),
 ('lower_single',[ccw((H,R,S))]),('right_single',[ccw((V,L,J))]),
 ('right_strip',para75(J,P(3,0),P(F(1,2),F(-1,2)),1,3,'sum'))]
 tiles=[];components=[]
 for name,batch in pieces:
  components.append({'name':name,'first':len(tiles),'count':len(batch)});tiles+=batch
 conv=lambda t:[[int(8*x) for x in p] for p in t]
 return {'a':2,'b':3,'c':4,'u':1,'v':2,'D':15,'N':75,'denominator':8,'target':conv(ccw((A,B,C))),'tiles':[conv(t) for t in tiles],'components':components,'source':'Explicit ten-piece dissection: four quadratic triangle blocks, four ordinary parallelogram grids, two individual tiles. Found in this project,2026-09-29; not a new globally admissible count.'}

def certificates():
 s2=seed(6,2);s3=seed(9,4)
 return [pack(s2),construct75(),pack(s3),pack(seed(F(21,2),4)),pack(seed(F(27,2),4)),pack(add_seeds(s2,s3))]

def main():
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 mode=parser.add_mutually_exclusive_group()
 mode.add_argument('--check',action='store_true',help='Regenerate, compare, and verify the six stored certificates (default).')
 mode.add_argument('--write',action='store_true',help='Verify and write the six deterministic certificates.')
 args=parser.parse_args()
 directory=Path(__file__).resolve().parents[1]/'data'
 for obj in certificates():
  path=directory/('theta-%d.json'%obj['N'])
  if args.write:
   result=verify(obj)
   path.write_text(json.dumps(obj,separators=(',',':'))+'\n',encoding='utf-8')
  else:
   stored=json.loads(path.read_text(encoding='utf-8'))
   if stored!=obj:
    raise ValueError('Certificate differs from deterministic reconstruction: '+str(path))
   result=verify(stored)
  print(json.dumps({'certificate':path.name,**result},sort_keys=True))

if __name__=='__main__':
 main()

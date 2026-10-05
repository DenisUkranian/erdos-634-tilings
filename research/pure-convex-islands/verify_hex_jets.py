"""Exact first-jet / core-boundary checks. Standard library only.
Independent integer-cell enumeration; cyclotomic arithmetic, no floats.
The accompanying note contains the general proof, not inferred from tests.
"""
import json
from pathlib import Path
from functools import lru_cache

def trim(p):
 while len(p)>1 and p[-1]==0:p.pop()
 return p

def divide(p,q):
 p=p.copy();out=[0]*max(1,len(p)-len(q)+1)
 while len(p)>=len(q) and any(p):
  d=len(p)-len(q);c=p[-1]//q[-1];assert c*q[-1]==p[-1]
  out[d]=c
  for i,v in enumerate(q):p[d+i]-=c*v
  trim(p)
 return trim(out),trim(p)
@lru_cache(None)
def cyclo(n):
 p=[-1]+[0]*(n-1)+[1]
 for d in range(1,n):
  if n%d==0:p,r=divide(p,list(cyclo(d)));assert not any(r)
 return tuple(p)

class Ring:
 def __init__(self,n,k,l):self.n=n;self.k=k;self.l=l
 def add(self,x,y):
  z=x.copy()
  for i,v in y.items():z[i]=z.get(i,0)+v
  return{i:v for i,v in z.items()if v}
 def neg(self,x):return{i:-v for i,v in x.items()}
 def sub(self,x,y):return self.add(x,self.neg(y))
 def scale(self,x,k):return{i:v*k for i,v in x.items()if v*k}
 def mul(self,x,y):
  z={}
  for i,a in x.items():
   for j,b in y.items():e=(i+j)%self.n;z[e]=z.get(e,0)+a*b
  return{i:v for i,v in z.items()if v}
 def red(self,x):
  p=[0]*self.n
  for i,v in x.items():p[i%self.n]+=v
  return divide(trim(p),list(cyclo(self.n)))[1]
 def zero(self,x):return not any(self.red(x))
 def mon(self,i,j):return{(self.k*i+self.l*j)%self.n:1}
 def const(self,c):return({0:c}if c else {},{}, {})
 def var(self,i,j):
  m=self.mon(i,j);return(m,self.scale(m,i),self.scale(m,j))
 def da(self,x,y):return tuple(self.add(a,b)for a,b in zip(x,y))
 def ds(self,x,y):return tuple(self.sub(a,b)for a,b in zip(x,y))
 def dm(self,x,y):
  return(self.mul(x[0],y[0]),self.add(self.mul(x[1],y[0]),self.mul(x[0],y[1])),self.add(self.mul(x[2],y[0]),self.mul(x[0],y[2])))
 def sn(self,n,z):
  out=self.const(0);v=self.const(1)
  for _ in range(n):out=self.da(out,v);v=self.dm(v,z)
  return out

def sub(p,q):return(p[0]-q[0],p[1]-q[1])
def add(p,q):return(p[0]+q[0],p[1]+q[1])
def mul(k,p):return(k*p[0],k*p[1])
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def inside3(p,poly):return all(det(sub(poly[(i+1)%len(poly)],v),sub(p,mul(3,v)))>=0 for i,v in enumerate(poly))
def overlap(p,q):
 for r in(p,q):
  for i,v in enumerate(r):
   d=sub(r[(i+1)%len(r)],v);n=(-d[1],d[0]);a=[n[0]*v[0]+n[1]*v[1]for v in p];b=[n[0]*v[0]+n[1]*v[1]for v in q]
   if max(a)<=min(b)or max(b)<=min(a):return False
 return True

def cells(poly,holes=()):
 out=[[],[]]
 for i in range(min(p[0]for p in poly)-1,max(p[0]for p in poly)+1):
  for j in range(min(p[1]for p in poly)-1,max(p[1]for p in poly)+1):
   for k in(1,2):
    p=(3*i+k,3*j+k)
    if inside3(p,poly)and not any(inside3(p,h)for h in holes):out[k-1].append((i,j))
 return out

def core(a,b,X,Y):
 u=(a+b,-b);w=(b,a);U=mul(X,u);V=mul(Y,w);P=[(0,0),U,add(U,V),V];rows=[]
 for start,step,apex,n in[((0,0),u,(a,0),X),(U,w,(0,a),Y),(add(U,V),mul(-1,u),(-a,0),X),(V,mul(-1,w),(0,-a),Y)]:
  for j in range(n):
   z=add(start,mul(j,step));rows.append([z,add(z,step),add(z,apex)])
 assert all(inside3(mul(3,z),P)for t in rows for z in t)
 assert all(not overlap(t,s)for i,t in enumerate(rows)for s in rows[:i])
 cc=cells(P,rows);assert sum(map(len,cc))==2*(a*a+a*b+b*b)*X*Y-2*(X+Y)*a*b
 return cc

def inventory(R,cc):
 out=[]
 for layer in cc:
  v=R.const(0)
  for i,j in layer:v=R.da(v,R.var(i,j))
  out.append(v)
 return out

def formulas(R,a,b,X,Y):
 q=R.var(a+b,-b);r=R.var(b,a)
 F=R.dm(R.dm(R.var(0,-1),R.sn(b,R.var(1,-1))),R.dm(R.sn(X,q),R.ds(R.var(b*Y,a*Y),R.var(a,0))))
 G=R.dm(R.sn(a,R.var(0,1)),R.dm(R.sn(Y,r),R.ds(R.var(b,0),R.var((a+b)*X,-b*X))))
 return F,G

def jet(R,U,D,kind):
 x=R.mon(1,0);y=R.mon(0,1);one={0:1}
 if kind=='a':return R.add(R.mul(R.sub(y,one),R.sub(U[1],R.mul(x,D[1]))),R.mul(R.sub(y,x),R.sub(U[2],D[2])))
 return R.add(R.mul(R.sub(x,y),R.sub(U[1],D[1])),R.mul(R.sub(x,one),R.sub(U[2],R.mul(y,D[2]))))


def hexcells(a,b,X,Y,Z):
 u=(a+b,-b);w=(b,a);v=sub(w,u);Xu=mul(X,u);Yw=mul(Y,w);Zv=mul(Z,v)
 P=[(0,0),Xu,add(Xu,Yw),add(add(Xu,Yw),Zv),add(Yw,Zv),Zv]
 dirs=[u,w,v,mul(-1,u),mul(-1,w),mul(-1,v)];rows=[];apex=(a,0)
 for j,(start,step,n)in enumerate(zip(P,dirs,[X,Y,Z,X,Y,Z])):
  for k in range(n):
   z=add(start,mul(k,step));rows.append([z,add(z,step),add(z,apex)])
  apex=(-apex[1],apex[0]+apex[1])
 assert all(inside3(mul(3,z),P)for t in rows for z in t)
 assert all(not overlap(t,s)for i,t in enumerate(rows)for s in rows[:i])
 cc=cells(P,rows);assert sum(map(len,cc))==2*(a*a+a*b+b*b)*(X*Y+X*Z+Y*Z)-2*(X+Y+Z)*a*b
 return cc

def prod(R,*zs):
 v=R.const(1)
 for z in zs:v=R.dm(v,z)
 return v

def hexformulas(R,a,b,X,Y,Z):
 q=R.var(a+b,-b);r=R.var(b,a);s=R.var(-a,a+b)
 F=R.da(prod(R,R.var(0,-1),R.sn(b,R.var(1,-1)),R.sn(X,q),R.ds(R.var(b*Y-a*Z,a*Y+(a+b)*Z),R.var(a,0))),prod(R,R.var(-a,a-1),R.sn(a,R.var(1,-1)),R.sn(Z,s),R.ds(R.var((a+b)*X+b*Y,-b*X+a*Y),R.var(0,b))))
 G=R.da(prod(R,R.sn(a,R.var(0,1)),R.sn(Y,r),R.ds(R.var(b-a*Z,(a+b)*Z),R.var((a+b)*X,-b*X))),prod(R,R.sn(b,R.var(0,1)),R.sn(Z,s),R.ds(R.const(1),R.var(-a+(a+b)*X+b*Y,a-b*X+a*Y))))
 return F,G

def reduced_jet(R,a,b,X,Y,Z):
 one={0:1};A=R.mon((a+b)*X,-b*X);B=R.mon(b*Y,a*Y);C=R.mon(-a*Z,(a+b)*Z);AB=R.mul(A,B);BC=R.mul(B,C)
 J=R.scale(R.mul(A,R.sub(BC,one)),b*X)
 J=R.add(J,R.scale(R.mul(R.sub(one,A),BC),a*Y+(a+b)*Z))
 J=R.sub(J,R.scale(R.mul(C,R.sub(one,AB)),a*Z))
 J=R.add(J,R.scale(R.mul(R.sub(one,C),AB),(a+b)*X+b*Y))
 return J

out=[]
for a,b,X,Y,Z in[(3,5,1,1,1),(8,7,2,2,3)]:
 cc=hexcells(a,b,X,Y,Z);row={'a':a,'b':b,'X':X,'Y':Y,'Z':Z,'up':len(cc[0]),'down':len(cc[1]),'checks':[]}
 for n,k,l,kind in[(31,2,5,None),(a,1,2,'a'),(a,2,1,'a')]:
  R=Ring(n,k,l);U,D=inventory(R,cc);F,G=hexformulas(R,a,b,X,Y,Z)
  FF=R.ds(U,D);GG=R.ds(U,R.dm(R.var(1,0),D));assert all(R.zero(R.sub(c,d))for c,d in zip(F,FF));assert all(R.zero(R.sub(c,d))for c,d in zip(G,GG))
  rec={'order':n,'x_power':k,'y_power':l,'HF_HG_values_and_first_derivatives':'exact PASS'}
  if kind:
   allzero=R.zero(U[0])and R.zero(D[0]);J=jet(R,U,D,'a');rec['core_zero_order_vanishes']=allzero;rec['jet']=R.red(J)
   if allzero:assert R.zero(R.sub(J,reduced_jet(R,a,b,X,Y,Z)));rec['reduced_jet_K']='exact PASS'
   assert not(R.zero(U[0])and R.zero(D[0])and R.zero(J))
  row['checks'].append(rec)
 out.append(row);print(json.dumps(row),flush=True)
# Exact tests of all four algebraic branches, including even a.
for a,b,X,Y,Z in[(3,5,3,1,3),(3,5,3,3,1),(3,5,1,3,3),(3,5,1,1,1),(8,7,8,1,8),(8,7,8,8,1),(8,7,1,8,8),(8,7,2,2,3)]:
 R=Ring(a,1,2);F,G=hexformulas(R,a,b,X,Y,Z);assert R.zero(F[0])and R.zero(G[0]);one={0:1};x=R.mon(1,0);y=R.mon(0,1)
 J=R.add(R.mul(R.sub(y,one),G[1]),R.mul(R.sub(y,x),F[2]));assert R.zero(R.sub(J,reduced_jet(R,a,b,X,Y,Z)))and not R.zero(J)
Path(__file__).with_name('hex_jets_verified.json').open('w').write(json.dumps({'arithmetic':'exact integer cyclotomic remainder','independent_hex_core_cells':True,'four_branch_algebra_including_even_a':'PASS','results':out},indent=2)+'\n')

#!/usr/bin/env python3
"""Replay row-cited Boolean identifications and verify the full reduced model."""
import argparse,json,math
from pathlib import Path
from collections import defaultdict

def need(ok,msg):
 if not ok:raise RuntimeError(msg)
class Equivalence:
 def __init__(self,n):self.parent=list(range(n));self.flip=[0]*n;self.fixed=[None]*n
 def locate(self,x):
  if self.parent[x]==x:return x,0
  r,q=self.locate(self.parent[x]);self.flip[x]^=q;self.parent[x]=r;return r,self.flip[x]
 def fix(self,x,v):
  r,p=self.locate(x);v^=p;need(self.fixed[r]in(None,v),'conflicting fixed assignment');self.fixed[r]=v
 def join(self,x,y,q):
  r,p=self.locate(x);s,t=self.locate(y);q^=p^t
  if r==s:need(q==0,'conflicting equivalence');return
  if r>s:r,s=s,r
  self.parent[s]=r;self.flip[s]=q
  if self.fixed[s]is not None:self.fix(r,self.fixed[s]^q)

def reduced(row,eq,conditions=()):
 coeff=defaultdict(int);b=row[0];forced={}
 for x,v in conditions:
  r,p=eq.locate(x);v^=p
  if r in forced and forced[r]!=v:return None
  if eq.fixed[r]is not None and eq.fixed[r]!=v:return None
  forced[r]=v
 for lit in row[1]:
  sign=1 if lit>0 else -1;r,p=eq.locate(abs(lit)-1);value=forced.get(r,eq.fixed[r])
  if value is not None:b-=sign*(value^p)
  elif p:b-=sign;coeff[r]-=sign
  else:coeff[r]+=sign
 return {x:a for x,a in coeff.items()if a},b

def impossible(state):
 if state is None:return True
 c,b=state;lo=sum(min(a,0)for a in c.values());hi=sum(max(a,0)for a in c.values())
 if not lo<=b<=hi:return True
 g=math.gcd(*c.values())if c else 0
 if g and b%g:return True
 if len(c)<=2:
  values={0}
  for a in c.values():values|={v+a for v in list(values)}
  return b not in values
 return False

def parse(path):
 with open(path)as f:
  n,s=map(int,next(f).split());meta=[tuple(map(int,next(f).split()))for _ in range(n+s)];rows=[]
  for line in f:
   b,k,*lits=map(int,line.split());need(k==len(lits)and all(1<=abs(x)<=n for x in lits),'bad model row');rows.append((b,lits))
 return n,s,meta,rows

def canonical(coeff,b):
 coeff={x:a for x,a in coeff.items()if a}
 if not coeff and b==0:return None
 g=math.gcd(*coeff.values())if coeff else 0
 if g>1 and b%g==0:b//=g;coeff={x:a//g for x,a in coeff.items()}
 lits=tuple((x+1 if a>0 else -x-1)for x,a in sorted(coeff.items())for _ in range(abs(a)))
 if lits and lits[0]<0:b=-b;lits=tuple(-v for v in lits)
 return b,lits

def main():
 ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('prefix');ap.add_argument('output');a=ap.parse_args()
 n,selected,metadata,rows=parse(a.source);need(selected==0,'selected source unsupported');eq=Equivalence(n);steps=0;units=0;merges=0;conflict=False
 with open(a.prefix+'.trace.txt')as f:
  for line in f:
   kind,*numbers=line.split();numbers=list(map(int,numbers));ri=numbers[0];need(0<=ri<len(rows),'source row index')
   if kind=='u':
    _,x,v=numbers;x-=1;need(0<=x<n and v in(0,1),'unit format');need(impossible(reduced(rows[ri],eq,[(x,1-v)])),'unit not implied by row');eq.fix(x,v);units+=1
   elif kind=='m':
    _,x,y,q=numbers;x-=1;y-=1;need(0<=x<n and 0<=y<n and q in(0,1),'merge format')
    for vx in(0,1):need(impossible(reduced(rows[ri],eq,[(x,vx),(y,vx^(1-q))])),'merge not implied by row')
    eq.join(x,y,q);merges+=1
   elif kind=='c':need(impossible(reduced(rows[ri],eq)),'conflict not implied');conflict=True
   else:raise RuntimeError('unknown trace step')
   steps+=1
 nn,ss,newmeta,newrows=parse(a.prefix+'.model.txt');need(ss==0,'selected reduced unsupported');free={}
 need(len(newmeta)==nn and {m[0]for m in newmeta}==set(range(nn)),'reduced variable indices incomplete or duplicated')
 for index,original,mirror,height in newmeta:
  need(0<=index<nn and 1<=original<=n,'new metadata');root,p=eq.locate(original-1)
  need(eq.fixed[root]is None and root not in free,'new variable is fixed/duplicate');free[root]=(index,p)
 expected_free={eq.locate(x)[0]for x in range(n)if eq.fixed[eq.locate(x)[0]]is None}
 need(set(free)==expected_free,'free-variable coverage')
 with open(a.prefix+'.map.txt')as f:
  need(int(next(f))==n,'map header')
  for i,line in enumerate(f):
   variable,root,p,value=map(int,line.split());need(variable==i+1 and 1<=root<=n and p in(0,1)and value in(-1,0,1),'map entry invalid');r,u=eq.locate(i);s,v=eq.locate(root-1)
   need(r==s and u^v==p,'map equivalence wrong');actual=-1 if eq.fixed[r]is None else eq.fixed[r]^u;need(value==actual,'map value wrong')
  need(i+1==n,'map incomplete')
 expected=set()
 for row in rows:
  coeff,b=reduced(row,eq);newcoeff=defaultdict(int)
  for root,c in coeff.items():
   index,p=free[root]
   if p:b-=c;c=-c
   newcoeff[index]+=c
  result=canonical(newcoeff,b)
  if result is not None:expected.add(result)
 if conflict:expected.add((1,()))
 actual={(b,tuple(lits))for b,lits in newrows}
 need(actual==expected and len(actual)==len(newrows),'reduced row set differs')
 out=dict(status='PASS',original_variables=n,original_rows=len(rows),reduced_variables=nn,reduced_rows=len(newrows),verified_trace_steps=steps,verified_units=units,verified_equivalences=merges,conflict=conflict,all_reduced_rows_independently_reconstructed=True)
 Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()

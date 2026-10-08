#!/usr/bin/env python3
"""Exact DSU current rows and original-tile count in native OPB format."""
import argparse,json,hashlib
from collections import defaultdict
from pathlib import Path

def need(ok,message):
 if not ok:raise RuntimeError(message)
def main():
 p=argparse.ArgumentParser();p.add_argument('prefix');p.add_argument('output');p.add_argument('--count',type=int,default=135);a=p.parse_args()
 with open(a.prefix+'.model.txt')as f:
  n,s=map(int,next(f).split());need(s==0,'selected reduced unsupported');roots={}
  for _ in range(n):
   index,original,mirror,height=map(int,next(f).split());need(original not in roots and 0<=index<n,'duplicate metadata');roots[original]=index+1
  rows=[]
  for line in f:
   rhs,k,*lits=map(int,line.split());need(k==len(lits),'row size');c=defaultdict(int)
   for lit in lits:need(1<=abs(lit)<=n,'literal range');c[abs(lit)]+=1 if lit>0 else -1
   rows.append((rhs,dict(c)))
 weights=defaultdict(int);constant=0
 with open(a.prefix+'.map.txt')as f:
  original_n=int(next(f));seen=0
  for line in f:
   i,root,parity,value=map(int,line.split());need(i==seen+1 and parity in(0,1)and value in(-1,0,1),'mapping entry');seen+=1
   if value>=0:constant+=value
   else:
    need(root in roots,'unknown free representative');weights[roots[root]]+=1 if parity==0 else -1;constant+=parity
  need(seen==original_n,'mapping incomplete')
 rows.append((a.count-constant,dict(weights)))
 with open(a.output,'w')as f:
  f.write(f'* #variable= {n} #constraint= {len(rows)} #equal= {len(rows)} intsize= 32\n')
  for rhs,coeff in rows:
   f.write(' '.join(f'{c:+d} x{x}'for x,c in sorted(coeff.items())if c)+f' = {rhs} ;\n')
 out=dict(variables=n,equalities=len(rows),original_tile_count=a.count,count_constant=constant,weighted_count_terms=len(weights),original_variables=original_n,opb_sha256=hashlib.sha256(Path(a.output).read_bytes()).hexdigest())
 Path(a.output+'.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()

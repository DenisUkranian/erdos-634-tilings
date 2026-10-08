#!/usr/bin/env python3
"""Cross-check the actual C++ interval operators against literal integer sets."""
import hashlib,json,random,subprocess,tempfile
from pathlib import Path

if not __debug__:
 raise RuntimeError("Run this exact verifier without Python -O or -OO.")
HERE=Path(__file__).resolve().parent

def intervals(items):
 out=[]
 for x in sorted(items):
  if out and out[-1][1]+1==x:out[-1][1]=x
  else:out.append([x,x])
 return out

def parse(line,skip=0):
 vals=list(map(int,line.split()));n=vals[skip];assert len(vals)==skip+1+2*n
 return [vals[k:k+2] for k in range(skip+1,len(vals),2)]

def main():
 rng=random.Random(135634);cases=[]
 for _ in range(10000):
  a={x for x in range(-15,31) if rng.random()<rng.random()};b={x for x in range(-15,31) if rng.random()<rng.random()};shift=rng.randrange(-12,13);p=rng.randrange(-20,40);cases.append((a,b,shift,p))
 payload=[]
 for a,b,shift,p in cases:
  aa,bb=intervals(a),intervals(b);payload.append(' '.join(map(str,[len(aa),len(bb),shift,p]+[x for r in aa+bb for x in r])))
 with tempfile.TemporaryDirectory() as d:
  exe=Path(d)/'interval-query';subprocess.run(['g++','-O3','-std=c++17',str(HERE/'interval_operations_query.cpp'),'-o',str(exe)],check=True)
  result=subprocess.run([str(exe)],input='\n'.join(payload)+'\n',text=True,capture_output=True,check=True).stdout.splitlines()
 assert len(result)==4*len(cases)
 for k,(a,b,shift,p) in enumerate(cases):
  b={x+shift for x in b};assert parse(result[4*k])==intervals(a|b);assert parse(result[4*k+1],1)==intervals(a-b);assert int(result[4*k+1].split()[0])==len(a&b);assert int(result[4*k+2])==int(p in a);assert parse(result[4*k+3])==intervals(a-{p})
 report={'status':'PASS','cases':len(cases),'checks_per_case':['union_with_shift','difference_with_shift','deleted_cardinality','membership','remove_single_integer'],'cpp_source_sha256':hashlib.sha256((HERE/'rle_equilateral135.cpp').read_bytes()).hexdigest()};(HERE/'interval_operators_verified.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()

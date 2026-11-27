"""Necessary short contours of any exterior-free positioned cut."""
from collections import Counter
from pathlib import Path
import json
import subprocess
from tempfile import TemporaryDirectory
from terminal import UNITS,add,scale,det,word_from_codes,width_obstruction
from review_terminal import exact_endpoint_test


def identity(word,a,b,c,modulus):
    stack=[]
    for token in word:
        j=token%6
        axis=(j-1)%6 if token<6 and modulus==a else j
        power=(b if modulus==a else a) if token<6 else c
        power*=1 if axis<3 else -1
        if stack and stack[-1][0]==axis%3:
            power+=stack.pop()[1]
        if power%modulus:
            stack.append((axis%3,power%modulus))
    return not stack


def signature(word):
    return min(tuple(6*(t//6)+(t-u)%6 for t in word[i:]+word[:i])
               for i,u in enumerate(word) if u<6 and word[i-1]>=6)


def accepted_words(binary,a,b,c,r):
    run=subprocess.run([str(binary),*map(str,(a,b,c,r))],check=True,text=True,capture_output=True)
    for line in run.stdout.splitlines():
        k,left,right=map(int,line.split())
        word=word_from_codes(left,right,r)
        p=(0,0)
        area=0
        seen=set()
        for t in word:
            j=t%6
            move=(add(scale(a,UNITS[j]),scale(b,UNITS[(j-1)%6])) if t<6 else scale(c,UNITS[j]))
            seen.add(p)
            area+=det(p,move)
            p=add(p,move)
        if p!=(0,0) or len(seen)!=len(word) or area!=2*k*c*a*b:
            continue
        if not all(identity(word,a,b,c,m) for m in (a,b)):
            continue
        assert exact_endpoint_test(a,b,c,word)
        if 2*r<16:
            # n=2c implies a single occupied lift. Only then use the pair test.
            assert k==1 and width_obstruction(a,b,c,word)
        yield k,signature(word)


def census(binary,a,b,c,r):
    shapes=set()
    counts=Counter()
    for k,word in accepted_words(binary,a,b,c,r):
        counts[k]+=1
        shapes.add((k,word))
    inventory=Counter((k,sum(t<6 for t in word)) for k,word in shapes)
    from nested_contacts import nested
    return dict(**({"nested_orientation_moment_width_counts":nested(shapes)} if c==37 and r==8 else {}),
                words_by_half_population_blocks=dict(sorted(counts.items())),
                shape_counts=[[2*k,low,n] for (k,low),n in sorted(inventory.items())],
                **({'normalized_words':[list(w) for _,w in sorted(shapes)]} if c==43 and r==8 else {}))


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    with TemporaryDirectory() as tmp:
        binary=Path(tmp)/'join'
        subprocess.run(['c++','-O3','-std=c++17',str(Path(__file__).with_name('word_join.cpp')),
                        '-o',str(binary)],check=True)
        print(json.dumps({c:{2*r:census(binary,a,b,c,r) for r in range(start,9)}
                          for a,b,c,start in ((33,7,37,5),(35,13,43,6))},indent=2))

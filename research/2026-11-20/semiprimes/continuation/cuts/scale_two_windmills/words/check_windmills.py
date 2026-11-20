"""Filter whole-board four-cell catalogs by independently reduced ordered words."""
from pathlib import Path
import argparse,json

def reduced(polygon,a,b,c,kill_a):
    order=a if kill_a else b
    multiplier=(b if kill_a else a)*pow(c,-1,order)%order
    assert multiplier*multiplier%order==1
    stack=[]
    for length,height,phase in polygon:
        phase=(phase+(height if kill_a else 0))%6
        k=length*(multiplier if height%2 else 1)*(1 if phase<3 else -1)
        axis=phase%3
        if stack and stack[-1][0]==axis:k+=stack.pop()[1]
        k%=order
        if k:stack.append((axis,k))
    return stack

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('catalog_folder',type=Path)
    opt=parser.parse_args()
    for N,(a,b,c) in ((3431,(33,7,37)),(5063,(35,13,43))):
        rows=json.loads((opt.catalog_folder/f'board_{N}.json').read_text())
        failed=0
        for i,row in enumerate(rows):
            found=None
            for cell,polygon in enumerate(row['shapes']):
                for kill_a in (True,False):
                    w=reduced(polygon,a,b,c,kill_a)
                    if w:
                        found=cell,(a if kill_a else b),w
                        break
                if found:break
            if found:
                failed+=1;print('row',i,'cell',found[0],'order',found[1],'reduced word',found[2])
        print(N,'examined',len(rows),'excluded',failed,'remaining',len(rows)-failed)
        assert (len(rows),failed)==((18,0) if N==3431 else (67,22))
if __name__=='__main__':main()

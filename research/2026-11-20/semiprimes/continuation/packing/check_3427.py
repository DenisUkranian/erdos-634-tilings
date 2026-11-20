"""Reconstruct and verify the full 3427-tile packing using exact coordinates."""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

from check_boards import check_pentagons, exchange, tile_key
from check_inventory import contained, overlap_pairs, replay
from packing_replay import add, area, edges, norm, pos, sub

HERE=Path(__file__).resolve().parent

def product(p,q):
    x,y=p
    u,v=q
    return x*u-y*v,x*v+y*u+y*v

def power(v,n):
    result=(1,0)
    while n:
        if n%2:
            result=product(result,v)
        v=product(v,v)
        n//=2
    return result

def in_pentagon(data):
    den=data['denominator']
    assert den==37**5
    result=[]
    for h,j,reflected,x,y in data['placements']:
        assert reflected in (0,1) and 0<=j<6
        z=(F(33,37),F(7,37)) if h>=0 else (F(40,37),F(-7,37))
        u=product(power(z,abs(h)),power((0,1),j))
        assert norm(u)==1
        origin=(F(x,den),F(y,den))
        short=(0,-7) if reflected else (-7,7)
        result.append(pos([origin,add(origin,product(u,(33,0))),add(origin,product(u,short))]))
    assert len(result)==14
    return result

def physical(shape):
    return [(F(x,37),F(y,37)) for x,y in shape]

def build(folder):
    inventory=json.loads((folder/'inventory_certificate.json').read_text())
    board,placed,ids=replay(33,7,37,inventory['3431'])
    original=[placed[i] for i in sorted(ids)]
    files=[p for p in folder.glob('exchange_3431*.json')
           if json.loads(p.read_text()).get('new_count')==3423]
    assert len(files)==1
    base=exchange(board,original,json.loads(files[0].read_text()),(33,7,37))
    check_pentagons(board,base)
    rows=(folder/'remaining_region.txt').read_text().splitlines()
    polygons=[]
    for row in rows[1:]:
        n,*a=map(int,row.split())
        p=list(zip(a[::2],a[1::2],strict=True))
        assert len(p)==n
        polygons.append(p)
    outside={tile_key(t):t for t in base}
    new=[]
    tile_data=json.loads((HERE/'pentagon14.json').read_text())
    local=in_pentagon(tile_data)
    for offset in ((0,0),(-4662,6105)):
        region=physical([add(p,offset) for p in polygons[0]])
        for tri in polygons[1:]:
            del outside[tile_key([add(p,offset)for p in tri])]
        for tr in local:
            moved=[add(p,(F(offset[0],37),F(offset[1],37))) for p in tr]
            assert contained(moved,region)
            new.append(moved)
    assert len(outside)==3399 and len(new)==28
    result=[physical(t) for t in outside.values()]+new
    target=physical(board)
    for t in result:
        assert area(t)==231 and contained(t,target)
        assert sorted(norm(sub(q,p)) for p,q in edges(t))==[49,1089,1369]
    assert next(overlap_pairs(result,range(len(result))),None) is None
    assert area(target)-sum(map(area,result))==4*231
    print('3427 congruent tiles inside the 3431 board; all pairs disjoint in their interiors.')
    print('Two area-16 pentagons hold 14 tiles each. Uncovered area: four tile areas.')
    print('Short heights in one added patch:',sorted({row[0] for row in tile_data['placements']}))
    return result

if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    from check_boards import HERE as support
    result=build(support)
    if len(sys.argv)==2:
        Path(sys.argv[1]).write_text(json.dumps([[[str(x),str(y)] for x,y in t] for t in result]))

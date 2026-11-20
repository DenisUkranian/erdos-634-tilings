"""Replay exact minimum median-path controls without nonstandard packages."""
from shortest_pentpath import scan
from path_bound import netmin

controls=[
    ((33,7,37,13,8,1),168,22),
    ((35,13,43,11,2,1),180,16),
    ((33,7,37,26,23,1),206,19),
    ((35,13,43,22,17,1),250,29),
]
for args,area,expected in controls:
    raw,_=netmin(*args)
    for length in range(raw,expected+1):
        n,results=scan(*args,ceiling=length,stop_after_witness=True)
        witnesses=[r[-1] for r in results if r[-1] is not None]
        assert bool(witnesses)==(length==expected)
        print(area,n,'inventories evaluated',len(results),'success',bool(witnesses),flush=True)
        if witnesses:print('first witness:',witnesses[0],flush=True)

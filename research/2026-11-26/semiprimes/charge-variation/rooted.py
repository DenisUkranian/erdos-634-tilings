"""Certified lower bounds for arbitrary exterior-free trees and forests."""
import numpy as np
from hull import ceil_div


def round_blocks(c, charge, tiles):
    blocks = ceil_div(tiles,c)
    return blocks + (charge-blocks)%2


def root_options(model, p, cap):
    c,d = model.c,model.d
    single,den = (3810,1002) if c==37 else (4304,1001)
    terminal,td = (91,22) if c==37 else (83,13)
    xs,ys = model.ranges[p],model.ranges[1-p]
    shape = (len(xs),len(ys),len(xs))
    one = np.full(shape,cap,dtype=int)
    many = np.full(shape,cap,dtype=int)
    leaf = np.full(shape[:2],cap,dtype=int)
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            if y==0 and x:
                # No nonzero child vector. Occupied neutral descendants
                # require an additional ordinary lift of at least two blocks.
                actual_terminal = round_blocks(c,x,ceil_div(c*abs(x)*terminal,td))
                neutral_children = round_blocks(c,x,ceil_div(c*abs(x)*single,den))+2
                leaf[i,j] = min(actual_terminal,neutral_children)
            for h,z in enumerate(xs):
                k = x-z
                u,v = c*x-d*y,d*y-c*z
                base = max(2,model.step_cost(x,y,z)//c)
                many[i,j,h] = base
                if (y,z)==(0,0):
                    continue
                tiles = max(base*c,model.cost(c*k,v,u))
                if (u==0 or v==0) and k:
                    tiles = max(tiles,ceil_div(c*abs(k)*single,den))
                one[i,j,h] = round_blocks(c,k,tiles)
    return one,many,leaf


def split_costs(model, p, first, forest, cap):
    """Minimize over one nonzero root vector and a nonzero remainder."""
    rest = forest.copy()
    xs,ys = model.ranges[p],model.ranges[1-p]
    rest[-xs.start,-ys.start] = cap
    result = np.full(first.shape,cap,dtype=int)
    nx,ny = result.shape
    for i,x in enumerate(xs):
        for j,y in enumerate(ys):
            if not (x or y) or first[i,j]>=cap:
                continue
            src = (slice(max(0,-x),min(nx,nx-x)),slice(max(0,-y),min(ny,ny-y)))
            dst = (slice(max(0,x),min(nx,nx+x)),slice(max(0,y),min(ny,ny+y)))
            np.minimum(result[dst],first[i,j]+rest[src],out=result[dst])
    return result


def branch_bounds(model, N):
    cap = 1+N//model.c
    transitions = [root_options(model,p,cap) for p in (0,1)]
    tree = [np.full(leaf.shape,2,dtype=int) for _,_,leaf in transitions]
    forest = [arr.copy() for arr in tree]
    iterations = 0
    while True:
        split = [split_costs(model,p,tree[p],forest[p],cap) for p in (0,1)]
        new_tree,new_forest = [],[]
        for p,(one,many,leaf) in enumerate(transitions):
            one_cost = (one+tree[1-p][None,:,:]).min(axis=2)
            many_cost = (many+split[1-p][None,:,:]).min(axis=2)
            t = np.minimum(cap,np.minimum(leaf,np.minimum(one_cost,many_cost)))
            f = np.minimum(t,split[p])
            zero = tuple(-model.ranges[q].start for q in (p,1-p))
            # This placeholder is excluded as a summand in all splits.
            t[zero] = f[zero] = 2
            new_tree.append(t)
            new_forest.append(f)
        iterations += 1
        pairs = list(zip(tree+forest,new_tree+new_forest))
        assert all(np.all(old<=new) for old,new in pairs)
        if all(np.array_equal(old,new) for old,new in pairs):
            break
        tree,forest = new_tree,new_forest
    for p in (0,1):
        zero = tuple(-model.ranges[q].start for q in (p,1-p))
        forest[p][zero] = 0
    return tree,forest,iterations

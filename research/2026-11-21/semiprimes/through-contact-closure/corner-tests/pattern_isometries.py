"""Exact isometric occurrences of a finite pattern in an existing catalogue.

Matching by itself makes no impossibility claim. A no-good is justified
only when the source pattern has a separately valid obstruction witness.
No missing placement is inserted and no symmetry of the board is used.
"""
from fractions import Fraction as F


def canonical_tile(g, tile):
    point,h,j,hand = tile
    assert hand in (-1,1)
    return g.point(*point),int(h),int(j)%6,int(hand)


def conjugate(g, point):
    x,y,e = point
    return g.point(x+y,-y,e)


def transform_point(g, point, transform):
    delta = g.sub(g.point(*point),tuple(transform['source_anchor']))
    if transform['reflected']:
        delta = conjugate(g,delta)
    unit = g.unit(transform['unit_height'],transform['unit_direction'])
    return g.add(tuple(transform['target_anchor']),g.mult(unit,delta))


def transform_tile(g, tile, transform):
    q,h,j,hand = canonical_tile(g,tile)
    sign = -1 if transform['reflected'] else 1
    return (transform_point(g,q,transform),
            transform['unit_height']+sign*h,
            (transform['unit_direction']+sign*j)%6,sign*hand)


def pattern_congruence_key(g, tiles, pattern_indices):
    """Canonical finite-pattern key under all direct/reflected isometries.

    Normalize each possible anchor to (q=0,h=0,j=0,s=1), and take the
    least unordered tile tuple. This is optional deduplication metadata;
    occurrence witnesses do not depend on trusting this key.
    """
    pattern = tuple(canonical_tile(g,tiles[i]) for i in pattern_indices)
    assert pattern
    forms = []
    for q,h,j,hand in pattern:
        transform = dict(reflected=hand == -1,unit_height=-hand*h,
                         unit_direction=(-hand*j)%6,
                         source_anchor=q,target_anchor=(0,0,0))
        forms.append(tuple(sorted(transform_tile(g,tile,transform) for tile in pattern)))
    return min(forms)


# Short public alias used by the search wrapper.
pattern_key = pattern_congruence_key


def pattern_isometries(g, tiles, index, pattern_indices, anchor=0):
    """All distinct isometric support sets already present in ``index``.

    ``tiles`` and ``index`` are the same globally canonical catalogue used
    by the solver. ``anchor`` is a position in ``pattern_indices``. Each
    occurrence stores image_indices in precisely the source pattern order.
    The candidate catalogue is read-only. There is no occurrence-count cap.
    """
    source_indices = tuple(pattern_indices)
    assert source_indices and len(set(source_indices)) == len(source_indices)
    assert 0 <= anchor < len(source_indices)
    pattern = tuple(canonical_tile(g,tiles[i]) for i in source_indices)
    q0,h0,j0,s0 = pattern[anchor]
    assert all(index.get(tile) == i for tile,i in zip(pattern,source_indices))
    offsets = tuple(g.sub(tile[0],q0) for tile in pattern)
    # A remote member tends to fail early. This only changes lookup order.
    def distance(position):
        x,y,e = offsets[position]
        return F(x*x+x*y+y*y,g.power(2*e))
    order = sorted((k for k in range(len(pattern)) if k != anchor),
                   key=lambda k:(distance(k),k),reverse=True)
    orientations = {}
    seen = set()
    answer = []
    for target_index,(q,h,j,hand) in enumerate(tiles):
        orientation = h,j,hand
        if orientation not in orientations:
            sign = 1 if hand == s0 else -1
            H,J = h-sign*h0,(j-sign*j0)%6
            unit = g.unit(H,J)
            mapped = []
            for k in order:
                delta = offsets[k] if sign == 1 else conjugate(g,offsets[k])
                _,hk,jk,sk = pattern[k]
                mapped.append((k,g.mult(unit,delta),H+sign*hk,(J+sign*jk)%6,sign*sk))
            orientations[orientation] = sign,H,J,mapped
        sign,H,J,mapped = orientations[orientation]
        hits = [(anchor,target_index)]
        for k,offset,hk,jk,sk in mapped:
            candidate = g.add(q,offset),hk,jk,sk
            found = index.get(candidate)
            if found is None:
                break
            assert tiles[found] == candidate
            hits.append((k,found))
        else:
            image_indices = [None]*len(pattern)
            for k,found in hits:
                image_indices[k] = found
            assert len(set(image_indices)) == len(pattern)
            support = tuple(sorted(image_indices))
            if support in seen:
                continue
            seen.add(support)
            answer.append(dict(
                pattern_indices=list(source_indices),image_indices=image_indices,
                indices=list(support),anchor_position=anchor,
                anchor_target_index=target_index,
                transform=dict(reflected=sign == -1,unit_height=H,unit_direction=J,
                               source_anchor=list(q0),target_anchor=list(q))))
    return answer


def transform_area_witness(g, source_witness, occurrence):
    """Expand an occurrence into the existing general-area-cut schema.

    The source must already be independently valid. This routine refuses a
    source with no recorded obstruction. The exported polygon and arithmetic
    can be checked directly, without trusting the pattern matching routine.
    """
    if not source_witness['budget']['violations']:
        raise ValueError('The source witness has no obstruction to propagate.')
    assert set(source_witness['indices']) == set(occurrence['pattern_indices'])
    mapping = dict(zip(occurrence['pattern_indices'],occurrence['image_indices']))
    transform = occurrence['transform']
    reflected = transform['reflected']
    edges = []
    for edge in source_witness['edges']:
        start = transform_point(g,edge['start'],transform)
        end = transform_point(g,edge['end'],transform)
        h,j = edge['direction']
        if reflected:
            start,end = end,start
            h = transform['unit_height']-h
            j = (transform['unit_direction']-j+3)%6
            side = (1-edge['side'])%3
        else:
            h += transform['unit_height']
            j = (j+transform['unit_direction'])%6
            side = edge['side']
        edges.append(dict(
            start=list(start),end=list(end),representative=mapping[edge['representative']],
            side=side,selected_owners=sorted({mapping[i] for i in edge['selected_owners'] if i in mapping}),
            length=edge['length'],direction=[h,j]))
    if reflected:
        edges.reverse()
    assert all(edges[k]['end'] == edges[(k+1)%len(edges)]['start'] for k in range(len(edges)))
    vertices = [edge['start'] for edge in edges]+[edges[-1]['end']]
    rational = [(F(x,g.power(e)),F(y,g.power(e))) for x,y,e in vertices]
    area2 = sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(rational,rational[1:]))
    assert area2 > 0 and area2 == F(source_witness['twice_axial_area'])
    area = area2/(g.a*g.b)
    W0 = sum(F(edge['length'])*(-1 if edge['direction'][1]%2 else 1) for edge in edges)
    W1 = sum(F(edge['length'])*(-1 if sum(edge['direction'])%2 else 1) for edge in edges)
    E0,E1 = W0/(g.a-g.b-g.c),W1/(g.a-g.b+g.c)
    even,odd = (E0+E1)/2,(E0-E1)/2
    failures = []
    for value,name in ((area,'nonintegral_area'),(even,'nonintegral_even_charge'),
                       (odd,'nonintegral_odd_charge')):
        if value.denominator != 1:
            failures.append(name)
    if area.denominator == even.denominator == odd.denominator == 1:
        if area < abs(even)+abs(odd):
            failures.append('insufficient_area_for_signed_population')
        if (area-even-odd)%2:
            failures.append('incompatible_population_parity')
    assert failures, 'The mapped support must preserve the obstruction.'
    indices = sorted({edge['representative'] for edge in edges})
    assert indices == occurrence['indices']
    return dict(
        indices=indices,vertices=vertices,edges=edges,
        twice_axial_area=str(area2),tile_area_ratio=str(area),
        budget=dict(W0=str(W0),W1=str(W1),even_charge=str(even),odd_charge=str(odd),
                    violations=failures),
        greedy_selected_count=len(indices))

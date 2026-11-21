"""Exact selected-long-side cycles and target-specific necessary no-goods.

The geometry must use the unrestricted global_core_sat.Geometry convention.
No height or translation bound is imposed. The public selected_long_cycles
function applies the supported-cycle theorem ONLY to its two target shapes.
Raw geometric detection is separately exposed for independent controls.
"""
from collections import defaultdict


TARGET_SHAPES = frozenset(((33, 7, 37), (35, 13, 43)))


def long_edge(g, tile):
    """Return (direction height, sorted exact endpoints) of a whole c side."""
    q, h, j, hand = tile
    q = g.point(*q)
    first = g.sub(q, g.scale(g.a, g.unit(h, j)))
    second = g.add(q, g.scale(g.b, g.unit(h, (j + hand) % 6)))
    return h + hand, tuple(sorted((first, second)))


def _one_cycle(adjacency, start):
    """A simple undirected cycle, plus its complete component vertex set.

    The graph is simple: opposite-bank copies have already been merged.
    A two-edge backtrack therefore cannot be mistaken for a cycle.
    """
    component = set()
    pending = [start]
    while pending:
        vertex = pending.pop()
        if vertex in component:
            continue
        component.add(vertex)
        pending.extend(adjacency[vertex])
    parent = {start: None}
    active = {start}
    finished = set()
    stack = [(start, iter(sorted(adjacency[start])))]
    while stack:
        vertex, neighbors = stack[-1]
        other = next(neighbors, None)
        if other is None:
            stack.pop()
            active.remove(vertex)
            finished.add(vertex)
            continue
        if other == parent[vertex]:
            continue
        if other not in parent:
            parent[other] = vertex
            active.add(other)
            stack.append((other, iter(sorted(adjacency[other]))))
        elif other in active:
            path = [vertex]
            while path[-1] != other:
                path.append(parent[path[-1]])
            path.reverse()
            path.append(other)
            assert len(path) >= 4 and len(set(path[:-1])) == len(path) - 1
            return path, component
    return None, component


def raw_selected_long_cycles(g, tiles, chosen):
    """Return one exact simple long-edge cycle per connected component.

    This is only a geometric detector. Its output on an arbitrary shape is
    NOT by itself a forbidden-configuration certificate. Each selected tile
    contributes its one whole long side. Identical undirected physical sides
    at the same height are merged before graph traversal.
    """
    edges_by_height = defaultdict(lambda: defaultdict(list))
    for index in sorted(set(chosen)):
        height, endpoints = long_edge(g, tiles[index])
        assert endpoints[0] != endpoints[1]
        edges_by_height[height][endpoints].append(index)
    answer = []
    for height, edges in sorted(edges_by_height.items()):
        adjacency = defaultdict(set)
        for first, second in edges:
            adjacency[first].add(second)
            adjacency[second].add(first)
        remaining = set(adjacency)
        while remaining:
            cycle, component = _one_cycle(adjacency, min(remaining))
            remaining.difference_update(component)
            if cycle is None:
                continue
            witnesses, indices = [], []
            for first, second in zip(cycle, cycle[1:]):
                owners = edges[tuple(sorted((first, second)))]
                representative = min(owners)
                indices.append(representative)
                witnesses.append({'from': list(first), 'to': list(second),
                                  'representative': representative,
                                  'selected_owners': list(owners)})
            assert len(set(indices)) == len(indices)
            answer.append({'height': height, 'indices': indices,
                           'vertices': [list(p) for p in cycle], 'edges': witnesses})
    return answer


def selected_long_cycles(g, tiles, chosen):
    """Return forbidden selected-index cycles for3431/5063, else an empty list.

    Every returned witness validates the permanent necessary clause
        not(and(x_i for i in witness['indices'])).
    It requires only the selected representative of each physical side.
    Other selected copies of that same side are not needed in the clause.
    The theorem applies at every integer height and every translation.
    """
    if (g.a, g.b, g.c) not in TARGET_SHAPES:
        return []
    return raw_selected_long_cycles(g, tiles, chosen)

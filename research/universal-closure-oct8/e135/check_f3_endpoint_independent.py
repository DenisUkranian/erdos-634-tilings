#!/usr/bin/env python3
"""Check cone witnesses and its endpoint using independent shortest paths."""
import heapq
import json
from pathlib import Path


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    source = Path(__file__).parents[1] / "global/f3_uniform_cone_verified.json"
    records = json.loads(source.read_text())["records"]
    for record in records:
        a, b, c = record["tile"]
        i, j, k = record["coefficients"]
        d = b*b + 2*a*b - a*a - c
        need(min(i,j,k) >= 0 and i*a+j*b+k*c == d, "Wrong direct witness")
        need(2*b < a and 1139*a < 2725*b and b < 22500, "Wrong cone")
        need(c*c == a*a+a*b+b*b, "Wrong tile")
    A, B, C, d = 2725, 1139, 3439, 75807
    distance = [10**30] * B
    distance[0] = 0
    queue = [(0, 0)]
    while queue:
        cost, residue = heapq.heappop(queue)
        if cost != distance[residue]:
            continue
        for edge_weight in (A, C):
            candidate = cost + edge_weight
            destination = (residue + edge_weight) % B
            if candidate < distance[destination]:
                distance[destination] = candidate
                heapq.heappush(queue, (candidate, destination))
    need(len(records) == 710 and distance[d % B] == 130479 > d, "Endpoint failure")
    out = {
        "status": "PASS", "direct_positive_witnesses_checked": len(records),
        "endpoint_residue_mod_1139": d % B, "D_minus_c": d,
        "least_endpoint_semigroup_representative": distance[d % B],
        "endpoint_method": "Dijkstra on residues modulo1139 with edge weights2725,3439",
        "endpoint_check_uses_apery_formula": False,
    }
    Path(__file__).with_name("f3_endpoint_independent_verified.json").write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

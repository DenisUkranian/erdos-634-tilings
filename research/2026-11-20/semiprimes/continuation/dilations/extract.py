"""Look for an intact unit F2 triangle in each positive scale-two construction."""
from double_exceptional import doubled
from scan_patches import patches
from controls.verify_grids import check

if __name__ == "__main__":
    for u in range(4,26,3):
        data = doubled(u)
        check(data)
        a,b,c = data["tile"]
        found = patches(data,1)
        print(f"u={u}, unit count={(a+2*b)*(2*a+b)}, intact unit copies={len(found)}", flush=True)
        if found:
            print(found)

"""Verify the fixed larger boards and scan each one for a complete unit F2 patch."""
from controls.dilation import instance, triple
from controls.verify_grids import check
from scan_patches import patches


def main():
    for u in (10, 6, 16, 12, 22, 18, 40):
        results = []
        for scale in (3, 4, 5, 6):
            data = triple(u, 1) if scale == 3 else instance(u, 1, scale)
            check(data)
            found = patches(data, 1)
            if found:
                print(f'Unit patch coordinates at u={u}, scale={scale}: {found}')
            results.append(len(found))
        a,b,_ = data['tile']
        print(f'{(a+2*b)*(2*a+b)}: unit patches at scales 3, 4, 5, 6: {results}', flush=True)


if __name__ == '__main__':
    main()
